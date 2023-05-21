import os
import openai
from enum import Enum
import pandas as pd
import shutil
from flask import current_app

from llama_index import download_loader, GPTVectorStoreIndex,\
    ServiceContext, GPTListIndex, LLMPredictor, SimpleDirectoryReader,\
        GPTVectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.vector_stores.faiss import FaissVectorStore
from pathlib import Path

from langchain.chat_models import ChatOpenAI
from llama_index.indices.composability import ComposableGraph
from globals import upload_hashes

import faiss

class DataType(Enum):
    AUDIO = 1
    DOCX = 2
    PDF = 3
    HTML = 4
    XLSX = 5
    # IMAGE = 5

def check_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def get_files_for_project(project_name):
    # Assuming your uploaded files are stored in a folder named after the project_name
    print(current_app.config['UPLOAD_FOLDER'])
    project_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], project_name)

    f = []
    for data_fd in  os.listdir(project_folder):
        f.extend(os.listdir(os.path.join(project_folder,data_fd)))

    return f

    
class IndexUtils():
    def __init__(self, root_path, project_name="default"):
        self.root_path = root_path # index saved root path
        self.project_name = project_name # would later used as graph index name
        self.faiss_index = faiss.IndexFlatL2(1536) # dimensions of text-ada-embedding-002
        self.upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], project_name)

    def save_loader(self, file_pathes: list, data_type: DataType, project_dir=None):
        _FAISS = os.getenv("USING_FAISS", 'False').lower() in ('true', '1', 't') 
        if _FAISS: 
            index_save_path = os.path.join(self.root_path,self.project_name)
            if not os.path.exists(index_save_path):
                os.makedirs(index_save_path)

            # load documents
            upload_files =[]
            print(self.upload_path)
            for r,d,f in os.walk(self.upload_path):
                for file in f:
                    upload_files.append(os.path.join(r,file))
            print("Detecting is repeating index...")    
            # Upload Hash comparison
            if self.project_name in upload_hashes.keys() and \
                upload_hashes[self.project_name] == hash(tuple(upload_files)):
                # Already has good index
                pass
            else:
                # DEBUG
                # Regenerate index
                upload_hashes[self.project_name] = hash(tuple(upload_files))
                # print(upload_files)
                if len(upload_files) == 0:
                    return "Nothing need to index" 
                documents = SimpleDirectoryReader(input_files=upload_files).load_data()
                vector_store = FaissVectorStore(faiss_index=self.faiss_index)
                storage_context = StorageContext.from_defaults(vector_store=vector_store)
                index = GPTVectorStoreIndex.from_documents(documents, storage_context=storage_context)

                # save index to disk
                print("Successful store new index...")    
                index.storage_context.persist(index_save_path)
        else:
            raise NotImplementedError
        
    # Load data and return index_sets
    def dataLoader(self, file_pathes: list, data_type: DataType): 
        print("Loading data...all file pathes: ", file_pathes)
        index_save_path = os.path.join(self.root_path,self.project_name)
        _FAISS = os.getenv("USING_FAISS", 'False').lower() in ('true', '1', 't') 
        if _FAISS: 
            self.save_loader(file_pathes,data_type)

            # load index from disk
            vector_store = FaissVectorStore.from_persist_dir(index_save_path)
            storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=index_save_path)
            index = load_index_from_storage(storage_context=storage_context)

            return index 
        else:
            reader = None
            if data_type == DataType.HTML:
                UnstructuredReader = download_loader("UnstructuredReader", refresh_cache=True)
                reader = UnstructuredReader()
            elif data_type == DataType.DOCX: 
                DocxReader = download_loader("DocxReader")
                reader = DocxReader()
            elif data_type == DataType.PDF:
                PDFReader = download_loader("PDFReader")
                reader = PDFReader()
            elif data_type == DataType.AUDIO:
                StringIterableReader = download_loader("StringIterableReader")
                reader = StringIterableReader()
            elif data_type == DataType.XLSX:
                PandasCSVReader = download_loader("PandasCSVReader")
                reader = PandasCSVReader()

            if reader is None:
                raise ValueError("The data type is not supported!")
            

            unsaved_doc_set = {}
            saved_doc_path = [] 
            for file_path_str in file_pathes:
                file_name = os.path.basename(file_path_str)
                # check if index already exists
                index_name = "index_" + file_name
                index_path = os.path.join(self.root_path,index_name)
                index_path = os.path.join(self.project_name,index_path)
                if os.path.exists(index_path):
                    saved_doc_path.append(index_path)
                    continue 

                if data_type == DataType.AUDIO:
                    audio_path = file_path_str
                    openai.api_key = os.getenv("OPENAI_API_KEY")
                    audio_file = open(audio_path, "rb")
                    transcript = openai.Audio.transcribe("whisper-1", audio_file)
                    unsaved_doc_set[file_name] = reader.load_data(transcript.text.split())
                elif data_type == DataType.XLSX:
                    dfs = pd.read_excel(file_path_str, sheet_name=None)
                    tmp_save_root = "./tmp"
                    if not os.path.exists(tmp_save_root):
                        os.makedirs(tmp_save_root)
                    sheet_names = list(dfs.keys())
                    for sheet_name in sheet_names:
                        index_save_path = os.path.join(tmp_save_root,sheet_name) 
                        dfs[sheet_name].to_csv(index_save_path) 
                        unsaved_doc_set[sheet_name] = reader.load_data(index_save_path)  
                    # Remove tmp files
                    shutil.rmtree(tmp_save_root)
                    
                else:
                    unsaved_doc_set[file_name] = reader.load_data(Path(file_path_str))

            index_set = {} 
            index_set.update(self.saveIndexer(1024, unsaved_doc_set))
            graph = self.buildGraphIndexer(index_set)
            index_set.update(self.loadIndexer(saved_doc_path))

            return index_set
    
    def saveIndexer(self, chunk_size_limit, doc_set):
        index_set = {}
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        service_context = ServiceContext.from_defaults(chunk_size_limit=chunk_size_limit)
        for key in doc_set.keys():
            cur_index = GPTVectorStoreIndex.from_documents(doc_set[key], service_context=service_context)
            index_set[key] = cur_index
            save_path = os.path.join(self.root_path,self.project_name)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            save_path = os.path.join(save_path,f'index_{key}.json')
            

            cur_index.save_to_disk(save_path=save_path)
        return index_set

    def loadIndexer(self, pathes:list):
        index_set = {}
        # llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo"))
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="gpt-4"))

        for path in pathes:
            cur_index = GPTVectorStoreIndex.load_from_disk(Path(path),llm_predictor=llm_predictor)
            file_name = os.path.basename(path)
            index_set[file_name] = cur_index

        return index_set
    def buildGraphIndexer(self, indexers):
        # check if graph exists
        file_name = f"graph_{self.project_name}.json"
        graph_path = os.path.join(self.root_path,self.project_name) 
        graph_path = os.path.join(graph_path,file_name) 

        # set number of output tokens
        # llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo"))
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="gpt-4"))
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

        if os.path.exists(graph_path):
            service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
            graph = ComposableGraph.load_from_disk(Path(graph_path),ServiceContext=service_context)

            return graph

        # set summary text for each doc
        # TODO: Now only use filename as summary text
        index_summaries = indexers.keys() 


        # define a list index over the vector indices
        # allows us to synthesize information across each index
        graph = ComposableGraph.from_indices(
            GPTListIndex, 
            [indexers[key] for key in indexers.keys()], 
            index_summaries=index_summaries,
            service_context=service_context
        )
        graph.save_to_disk(graph_path)

        return graph
