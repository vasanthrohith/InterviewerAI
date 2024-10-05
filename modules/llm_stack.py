import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

class Call_LLM:
    def __init__(self,):
        self.call_openai()

    def call_openai(self,):
        try:
            self.llm_openai = ChatOpenAI(
            model="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key
            )

        except Exception as error:
            print("Error in connecting to openai : ", error)
