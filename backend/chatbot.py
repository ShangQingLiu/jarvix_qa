from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent

from gpt_index.langchain_helpers.agents import LlamaToolkit, create_llama_chat_agent, IndexToolConfig, GraphToolConfig
from gpt_index.indices.query.query_transform.base import DecomposeQueryTransform
from gpt_index import LLMPredictor
from langchain import OpenAI, PromptTemplate


class ChatBot():
    def __init__(self,index_set,graph,project_name) -> None:
        self.get_query_configs = self.get_query_configs()
        self.index_configs = self.getIndexConfigs(index_set)
        self.graph_config =  None if graph == None else self.getGraphConfig(graph)
        self.toolKit = self.getToolKit()
        self.agent = self.getAgent(self.toolKit) 
        self.project_name = project_name
        pre_promt =  f"You are a personal assistant for Synergies company, your job is to answer questions. Use only context index_{self.project_name}.json "
#         act_promtp = """We have provided context information below. \n"
# "---------------------\n"
# "{context_str}"
# "\n---------------------\n"
# "Your job is to continue the conversation as a chatbot.\n"
# "When asked a question, try to use the context provided to directly answer that question.\n"
# "Given this information, please respond to or answer the question: {query_str}""" 
        self.prompt = PromptTemplate(
        template=pre_promt + """to provide answers.
                    Do not provide any answers that deviate from your toolkit documents. If you don't know the answer, just say "Hmm, Im not sure."
                    Don't try to make up an answer up. You only 
                    allow to answer less than 300 words, and you need to complete the sentence in the end, please answer in simplified Chinese:
                   --------
                   Question: {query}
                  """,
        input_variables=["query"],
    )

    def run(self,query)->str:
        agent_prompt = self.prompt.format(query=query)
        try:
            response = self.agent.run(input=agent_prompt).strip()
        except ValueError as e:
            response = str(e)
            if not response.startswith("Could not parse LLM output: `"):
                raise e
            response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
        return response 

        # define query configs for graph 
    def get_query_configs(self):
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))
        decompose_transform = DecomposeQueryTransform(
            llm_predictor, verbose=True
        )
        query_configs = [
            {
                "index_struct_type": "simple_dict",
                "query_mode": "default",
                "query_kwargs": {
                    "similarity_top_k": 1,
                    # "include_summary": True
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

    def getGraphConfig(self):
        graph_config = GraphToolConfig(
            graph = self.graph,
            name="Graph Index",
            description="useful for when you want to answer queries about the project",
            index_query_kwargs={"similarity_top_k": 3},
            tool_kwargs={"return_direct": True}
        )

        return graph_config

    def getAgent(self,toolkit):
        memory = ConversationBufferMemory(memory_key="chat_history")
        llm=ChatOpenAI(temperature=0)
        agent = create_llama_chat_agent( toolkit,
            llm,
            memory=memory,
            verbose=True,
            max_iterations=5
        )
        return agent