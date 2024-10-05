import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from typing import Annotated, Dict, TypedDict
from Handle_collections import Chroma_collections
from langgraph.graph import END, StateGraph
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains import ConversationChain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory


from llm_stack import Call_LLM
from GetTemplates import Get_templates
from pannel_bot import pannel_member_bots


class InterviewerBot(Call_LLM):
    def __init__(self):
        super().__init__()

    def get_resume_details(self, collection_name : str) -> list[str] | None:
        print("--get_resume_details--")
        chroma_obj = Chroma_collections()
        print("Retrieving the items from collection...")
        collection_items = chroma_obj.get_items(collection_name=collection_name)
        print("retireved docs : ", len(collection_items))

        return collection_items

    def start_interview(self,collection_name : str) :
        print("start_interview")
        resume_details = self.get_resume_details(collection_name=collection_name)
        # print(resume_details)
        resume_details = [i for i in resume_details]
        print(resume_details[0])
        return resume_details



class GraphState(TypedDict):
        """
        Represents the state of our graph.

        Attributes:
            keys: A dictionary where each key is a string.
        """
        keys: Dict[str, any]

class MainQuestion_flow(InterviewerBot):
    def __init__(self):
        super().__init__()
        self.history = ChatMessageHistory()
        self.chain_memory = ConversationSummaryBufferMemory(llm=self.llm_openai, max_token_limit=2000)

    def ask_question(self, context: list[str]):
        print("--ask_question--")

        temp_obj = Get_templates()
        pannel_obj=pannel_member_bots()

        # interviewer_1_main = ConversationChain(
        #     llm=self.llm_openai,
        #     prompt=PromptTemplate(input_variables=['history', 'input'], template=temp_obj.temp(context[0], conversation_1_temp=True,)),
        #     # We set a very low max_token_limit for the purposes of testing.
        #     memory=self.chain_memory,
        #     verbose=True,
        # )

        # interviewer_2_input = "ask next question"
        human = {"human":"-"}
        ai = {"ai":None}
        
        count=0
    
        while True:                        

            print("History >>> ", self.chain_memory.load_memory_variables({}))
            if count==0:
                 user_input = "Hi, my name is vasanth"
                 human["human"]=user_input
            else:  
                user_input = input("You : ")
                human["human"]=user_input


            # # Pannel member 2 bot
            if ai['ai']:
                # interviewer_2_input_review = input("reviews ")
                interviewer_2_input_review = pannel_obj.pannel_member_2(recent_conversation={"ai_msg":ai, "human_msg":human}, 
                                                                        conversation_history=self.chain_memory.load_memory_variables({}),
                                                                        content=context[0])
            else:
                interviewer_2_input_review = "-"


            interviewer_1_main = ConversationChain(
            llm=self.llm_openai,
            prompt=PromptTemplate(input_variables=['history', 'input'], template=temp_obj.temp(context[0], interviewer_2_input_review, conversation_1_temp=True,)),
            # We set a very low max_token_limit for the purposes of testing.
            memory=self.chain_memory,
            verbose=True,
            )

    
            bot_response = interviewer_1_main.predict(input=user_input)
            print("BOT : ",bot_response)
            print("count > ", count)
            # if count%2:
            ai["ai"]=bot_response
            

            count+=1

    def run_nodes(self, ):
         print("--run_nodes--")

    def start_process(self, questions: str, context_chunk: str) -> dict:
         print("--start_process--")
        #  print("questions : ", questions)




o=InterviewerBot()
context = o.start_interview(collection_name='vasanth_workexp_summary')

o= MainQuestion_flow()
o.ask_question(context=context)




