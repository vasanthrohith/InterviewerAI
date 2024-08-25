from langchain_community.chat_models.openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate



# \\ USER DEFINED MODULES
from ExtractMyText import Extract_TXT
from GetTemplates import Get_templates
# o=get_templates()
# o.temp(summarize_cv_temp=True,)

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
# print(openai_api_key)



class AIStuff:
    def __init__(self,):
        self.call_openai()


    def call_openai(self,):
        try:
            self.llm_openai = ChatOpenAI(
            model="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key
            )

        except Exception as error:
            print("Error in connecting to openai : ", error)

    def Content_Summarizer(self,text):
        print("--Content_Summarizer--")

        temp_obj=Get_templates()
        summarizer_temp=temp_obj.temp(summarize_cv_temp=True)

        summarizer_prompt = ChatPromptTemplate.from_template(summarizer_temp)

        summarizer_chain = (
                            summarizer_prompt | 
                            self.llm_openai
                            )
        
        summarized_response = summarizer_chain.invoke({"content":text})

        return summarized_response
        

    def HandleAI(self, Pdf_File):
        txt_obj=Extract_TXT()
        raw_text = txt_obj.extractme(pdf_path=Pdf_File)

        self.summarized_cv = self.Content_Summarizer(text=raw_text)

        print(self.summarized_cv)



o=AIStuff()
o.HandleAI(Pdf_File=r"C:\Users\CVHS ADMIN\Documents\github_repos\InterviewerAI\InterviewerAI\CVs\vasanth-AIML-07082024.pdf")










