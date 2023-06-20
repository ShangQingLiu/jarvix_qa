from flask import current_app

from langchain import  PromptTemplate
from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory

from llama_index import  (LLMPredictor,ServiceContext, ResponseSynthesizer, StorageContext
                          , load_index_from_storage)
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.indices.query.query_transform.base import DecomposeQueryTransform
from llama_index.langchain_helpers.agents import  LlamaToolkit, create_llama_chat_agent,IndexToolConfig
from llama_index.indices.composability import ComposableGraph
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.prompts.prompts import (
    QuestionAnswerPrompt
)

import os
from opencc import OpenCC
import constant_prompt 
import logging
import openai


class ChatBot():
    def __init__(self,index_set,graph,project_name,chunk_size_limit=512,index_saved_path="index_data",
                 language="EN") -> None:
        self.using_FAISS = os.getenv("USING_FAISS", 'False').lower() in ('true', '1', 't') 
        self.using_PINECONE = os.getenv("USING_PINECONE", 'False').lower() in ('true', '1', 't') 
        self.index_root_path = current_app.config["INDEX_SAVE_PATH"]
        self.project_name = project_name
        self.query_configs = self.get_query_configs()
        self.index_configs = self.getIndexConfigs(index_set)
        self.graph_config =  None if graph == None else self.getGraphConfig(index_saved_path,project_name,chunk_size_limit)
        self.toolKit = self.getToolKit()
        self.language = language
        self.agent, self.agent_no_text, self.agent_generation = self.getAgent(self.toolKit) 
        self.prompt = PromptTemplate(
        template=constant_prompt.pre_promt + constant_prompt.noact_prompt,
        input_variables=["query"],
        )
        self.yes_no_prompt = PromptTemplate(
        template=constant_prompt.yes_no_prompt,
        input_variables=["query"],
        )
    def truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to a maximum length."""
        return text[: max_length - 3] + "..."

    def run(self,query)->str:
        agent_prompt = self.prompt.format(query=query)
        try:
            if self.using_FAISS:
                # Refine
                logging.info("Start to query")
                response = self.agent.query(agent_prompt)
                if self.language == "ZH_TW":
                    cc = OpenCC('s2tw')
                    response = cc.convert(response.response)
                else:
                    response = response.response

                # # Old code
                pre_response = self.agent_no_text.query(query)
                # pre_response = self.agent.query(agent_prompt)
                logging.info(pre_response.source_nodes)
                logging.info(pre_response.get_formatted_sources())
                logging.info(pre_response.response)
                # if pre_response.response is None:

                #     completion = openai.ChatCompletion.create(
                #     model="gpt-3.5-turbo",
                #     messages=[
                #             {"role": "system", "content": "You are a helpful assistant."},
                #             {"role": "user", "content": f"{query}"},
                #         ]
                #     )

                #     response = completion.choices[0].message
                #     response = response.to_dict()['content']
                # else:
                #     response = self.agent.query(agent_prompt)
                # if pre_response.response is None:
                #     pass
                # else:
                #     if pre_response.response is None:
                #         pass
                #     else:
                #         if self.language == "ZH":
                #             cc = OpenCC('s2tw')
                #             response = cc.convert(response.response)
                #         else:
                #             response = response.response
            else:
                response = self.agent.run(input=agent_prompt).strip()
        except ValueError as e:
            response = str(e)
            if not response.startswith("Could not parse LLM output: `"):
                raise e
            response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
        return response 


    def run_yes_no(self,query)->str:
        agent_prompt = self.yes_no_prompt.format(query=query)
        try:
            if self.using_FAISS:
                response = self.agent.query(agent_prompt)
                # response = self.agent.chat(agent_prompt)
            else:
                response = self.agent.run(input=agent_prompt).strip()
        except ValueError as e:
            response = str(e)
            if not response.startswith("Could not parse LLM output: `"):
                raise e
            response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
        return response 

    def get_query_configs(self):
        max_tokens = os.getenv("MAX_TOKENS", 512) 
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo",max_tokens=max_tokens))
        decompose_transform = DecomposeQueryTransform(
            llm_predictor, verbose=True
        )
        query_configs = [
            {
                "index_struct_type": "simple_dict",
                "query_mode": "default",
                "query_kwargs": {
                    "similarity_top_k": 3,
                    "include_summary": True
                },
                "query_transform": decompose_transform
            },
            {
                "index_struct_type": "list",
                "query_mode": "default",
                "query_kwargs": {
                    "response_mode": "tree_summarize",
                    "verbose": True
                }
            },
        ]
        return query_configs
    
    def getToolKit(self):
        toolkit = None

        if self.using_FAISS:
            pass

        else:
            if self.graph_config == None:
                toolkit = LlamaToolkit(
                    index_configs=self.index_configs,
                )
            else:
                toolkit = LlamaToolkit(
                    index_configs=self.index_configs,
                    graph_configs=[self.graph_config]
                ) 

        return toolkit
    
    def getIndexConfigs(self,index_set):
        index_configs = []
        if self.using_FAISS:
            pass
        else:
            for key in index_set.keys():
                tool_config = IndexToolConfig(
                    index=index_set[key], 
                    name=f"Vector Index {key}",
                    description=f"useful for when you want to answer queries about specific question",
                    index_query_kwargs={"similarity_top_k": 3},
                    tool_kwargs={"return_direct": True}
                )
                index_configs.append(tool_config)

        return index_configs

    def getGraphConfig(self,index_saved_path,project_name,chunk_size_limit):
        service_context = ServiceContext.from_defaults(chunk_size_limit=chunk_size_limit)
        graph_path = os.path.join(os.getcwd(),f'{index_saved_path}/{project_name}/graph_{project_name}.json')
        # print(graph_path)
        self.graph = ComposableGraph.load_from_disk( graph_path, 
            service_context=service_context,
        )
#         graph_config = GraphToolConfig(
#             graph=self.graph,
#             name=f"Graph Index",
#             description="useful for when you want to answer queries that require analyzing multiple uploaded documents.",
#             query_configs=self.query_configs,
#             tool_kwargs={"return_direct": True}
# )
        return None
        # return graph_config

    def getAgent(self,toolkit):
        agent = None
        if self.using_FAISS:
            # load index from disk
            ## List Index
            ### TODO
            ## vector Index
            index_save_path = os.path.join(self.index_root_path,self.project_name)
            vector_store = FaissVectorStore.from_persist_dir(index_save_path)
            storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=index_save_path)
            vector_index = load_index_from_storage(storage_context=storage_context)
            # agent = vector_index.as_chat_engine()

            vector_retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=3)
            # configure response synthesizer

            # set number of output tokens
            chunk_size_limit = os.getenv("MAX_TOKENS", 250) 
            predict_size_limit = os.getenv("PREDICT_SIZE_LIMIT", 512) 
            llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=predict_size_limit))
            # llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="gpt-4"))
            service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor,chunk_size_limit=chunk_size_limit)

            logging.info("prompt language:",self.language)
            if self.language == "EN":
                prompt = QuestionAnswerPrompt(constant_prompt.qa_promt_tmpl_en)
            elif self.language == "ZH_TW":
                prompt = QuestionAnswerPrompt(constant_prompt.qa_promt_tmpl_zh)
            elif self.language == "ZH_CN":
                prompt = QuestionAnswerPrompt(constant_prompt.qa_promt_tmpl_cn)
            elif self.language == "ZH":
                prompt = QuestionAnswerPrompt(constant_prompt.qa_promt_tmpl_zh)
            else:
                logging.info("language not support")

            response_synthesizer = ResponseSynthesizer.from_args(
                service_context=service_context,
                response_mode='refine',
                # refine_template=prompt,
                # response_mode='no_text',
                text_qa_template=prompt
                # node_postprocessors=[
                #     SimilarityPostprocessor(similarity_cutoff=0.2)
                # ]
            )

            response_synthesizer_no_text = ResponseSynthesizer.from_args(
                service_context=service_context,
                response_mode='no_text',
                text_qa_template=prompt
            )

            response_synthesizer_generate = ResponseSynthesizer.from_args(
                service_context=service_context,
                response_mode='generation',
                text_qa_template=prompt
            )

            # vector query engine
            agent = RetrieverQueryEngine(
                retriever=vector_retriever,
                response_synthesizer=response_synthesizer,
            )

            agent_no_text = RetrieverQueryEngine(
                retriever=vector_retriever,
                response_synthesizer=response_synthesizer_no_text,
            )

            agent_generate = RetrieverQueryEngine(
                retriever=vector_retriever,
                response_synthesizer=response_synthesizer_generate,
            )
        elif self.using_PINECONE:
            # pinecone_index = pinecone.Index("quickstart-index")
            # vector_store = PineconeVectorStore(pinecone_index=pinecone_index, namespace='test')
            # storage_context = StorageContext.from_defaults(vector_store=vector_store)
            # vector_store = PineconeVectorStore(pinecone_index=pinecone_index, namespace='test')
            # storage_context = StorageContext.from_defaults(vector_store=vector_store)
            # vector_store_info = VectorStoreInfo(
            #     content_info='brief biography of celebrities',
            #     metadata_info=[
            #         MetadataInfo(
            #             name='category', 
            #             type='str', 
            #             description='Category of the celebrity, one of [Sports, Entertainment, Business, Music]'),
            #         MetadataInfo(name='country', type='str', description='Country of the celebrity, one of [United States, Barbados, Portugal]'),
            #     ]
            # )
            # retriever = VectorIndexAutoRetriever(index, vector_store_info=vector_store_info)
            pass
        else:
            raise(NotImplementedError)
            memory = ConversationBufferMemory(memory_key="chat_history")
            llm=ChatOpenAI(temperature=0.2, max_tokens=512)
            agent = create_llama_chat_agent( toolkit,
                llm,
                memory=memory,
                verbose=True,
                # max_iterations=10
            )
        return agent, agent_no_text, agent_generate