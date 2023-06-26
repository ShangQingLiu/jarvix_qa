import os
import openai
from enum import Enum
import pandas as pd
import shutil
from flask import current_app

from llama_index import download_loader, GPTVectorStoreIndex,\
    ServiceContext, GPTListIndex, LLMPredictor, SimpleDirectoryReader,\
         StorageContext, load_index_from_storage 

from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.vector_stores import PineconeVectorStore
from pathlib import Path

from langchain.chat_models import ChatOpenAI
from llama_index.indices.composability import ComposableGraph
from globals import upload_hashes

import faiss
import pinecone

import logging

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
    print(current_app.config['UPLOAD_FOLDER'])
    print(project_name)
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
        USING_PINECONE = os.getenv("USING_PINECONE", 'False').lower() in ('true', '1', 't') 
        if _FAISS: 
            index_save_path = os.path.join(self.root_path,self.project_name)
            if not os.path.exists(index_save_path):
                os.makedirs(index_save_path)

            # load documents pathes
            upload_files =[]
            print(self.upload_path)
            for r,d,f in os.walk(self.upload_path):
                for file in f:
                    upload_files.append(os.path.join(r,file))
            
            
            print("Detecting if index exist...")    
            # Upload Hash comparison
            if False:
                pass
            else:
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
                    
                    def filename_fn(filename):
                        # if "ESG" in filename:
                        #     company_name = filename.split("-")[0]
                        #     return {'doc_id': filename, 'company_name': company_name}
                        # else:
                            return {'doc_id': filename }
                    # filename_fn = lambda filename: {'file_name': filename} 
                    
                    loader = SimpleDirectoryReader(input_files=upload_files)
                    documents = loader.load_data()
                    ## Vector Index
                    vector_store = FaissVectorStore(faiss_index=self.faiss_index)
                    storage_context = StorageContext.from_defaults(vector_store=vector_store)
                    index = GPTVectorStoreIndex.from_documents(documents, storage_context=storage_context)

                    ## List Index
                    # TODO: fix this
                    # list_service_context = ServiceContext.from_defaults(chunk_size=1024)
                    # list_nodes = list_service_context.node_parser.get_nodes_from_documents(documents)
                    # list_storage_context = StorageContext.from_defaults()
                    # list_index = ListIndex(list_nodes, storage_context=list_storage_context)


                    # save index to disk
                    logging.info("Successful store new index...")    
                    index.storage_context.persist(index_save_path)
        elif USING_PINECONE:
            # load documents pathes
            pass
            # upload_files =[]
            # print(self.upload_path)
            # for r,d,f in os.walk(self.upload_path):
            #     for file in f:
            #         upload_files.append(os.path.join(r,file))

            # def filename_fn(filename):
            #     # if "ESG" in filename:
            #     #     company_name = filename.split("-")[0]
            #     #     return {'doc_id': filename, 'company_name': company_name}
            #     # else:
            #         return {'doc_id': filename }
            # # filename_fn = lambda filename: {'file_name': filename} 
            
            # loader = SimpleDirectoryReader(input_files=upload_files)
            # documents = loader.load_data()
            # pinecone_index = pinecone.Index("quickstart-index")
            # vector_store = PineconeVectorStore(pinecone_index=pinecone_index, namespace='test')
            # storage_context = StorageContext.from_defaults(vector_store=vector_store)
            # index = GPTVectorStoreIndex.from_documents(documents, storage_context=storage_context)
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
                PDFReader = download_loader("PyMuPDFReader")
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
            saved_vector_path_dirs = [] 
            saved_vector_keys = []
            for file_path_str in file_pathes:
                file_name = os.path.basename(file_path_str)
                # check if index already exists
                index_name = "index_" + file_name
                saved_vector_keys.append(index_name)
                index_path = os.path.join(self.project_name,index_path)
                if os.path.exists(index_path):
                    saved_vector_path_dirs.append(index_path)
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
            chunk_size_limit = os.getenv("MAX_TOKENS", 250) 
            index_set.update(self.saveIndexer(chunk_size_limit, unsaved_doc_set))
            index_set.update(self.loadIndexer(zip(saved_vector_path_dirs, saved_vector_keys)))

            return index_set
    
    def saveIndexer(self, chunk_size_limit, doc_set):
        index_set = {}
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        max_tokens = os.getenv("MAX_TOKENS", 512) 
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=max_tokens))
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size_limit=chunk_size_limit)
        for key in doc_set.keys():
            cur_index = GPTVectorStoreIndex.from_documents(doc_set[key], service_context=service_context)
            index_set[key] = cur_index
            save_path = os.path.join(self.root_path,self.project_name)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            # save_path = os.path.join(save_path,f'index_{key}.json')
            cur_index.set_index_id('index_{key}')
            cur_index.storage_context.persist(save_path=save_path)
        return index_set

    def loadIndexer(self, pathes:tuple): #[(dir, key)]
        index_set = {}
        max_tokens = os.getenv("MAX_TOKENS", 512) 
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=max_tokens))
        # llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="gpt-4"))

        for path in pathes:
            cur_index = load_index_from_storage(Path(path[0]),index_id=(path[1]))
            index_set[path[1]] = cur_index

        return index_set
    # Deprecate
    def buildGraphIndexer(self, indexers):
        # check if graph exists
        file_name = f"graph_{self.project_name}.json"
        graph_path = os.path.join(self.root_path,self.project_name) 
        graph_path = os.path.join(graph_path,file_name) 

        # set number of output tokens
        chunk_size_limit = os.getenv("MAX_TOKENS", 250) 
        predict_size_limit = os.getenv("PREDICT_SIZE_LIMIT", 512) 
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=predict_size_limit))
        # llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="gpt-4"))
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor,chunk_size_limit=chunk_size_limit)

        if os.path.exists(graph_path):
            service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor,chunk_size_limit=chunk_size_limit)
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
