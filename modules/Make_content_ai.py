import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS 
from langchain.docstore.document import Document
from langchain_core.runnables import RunnablePassthrough

from Handle_collections import Chroma_collections
from llm_stack import Call_LLM

# \\ USER DEFINED MODULES
from ExtractMyText import Extract_TXT
from GetTemplates import Get_templates
# o=get_templates()
# o.temp(summarize_cv_temp=True,)

load_dotenv()
base_dir = os.path.dirname(os.path.abspath(__file__))


openai_api_key = os.getenv("OPENAI_API_KEY")
# print(openai_api_key)



class eval_project_title(BaseModel):
        titles: list = Field(description="titles of each projects")



class eval_project_questions(BaseModel):
        questions: list = Field(description="Generate 5 questions")



class AIStuff(Call_LLM):
    def __init__(self) -> None:
         super().__init__()
         self.embeddings = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


    def format_docs(self, docs : list) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    def project_Summary(self, project_list : list[str], all_project_summary : str, project_qa_temp : str) -> list[str]:
        """create prject-wise chunks :
            eg : project 1: details, project 2: details...."""
        
        print("--project_Summary--")
        document_chunk = [Document(page_content=all_project_summary)]

        
        vectorstore = FAISS.from_documents(document_chunk, self.embeddings) 
        project_qa_prompt = PromptTemplate.from_template(project_qa_temp)

        project_qa_chain = (
                    {
                        "context": vectorstore.as_retriever() | self.format_docs,
                        "question": RunnablePassthrough(),
                    }
                    | project_qa_prompt
                    | self.llm_openai 
                    | StrOutputParser()
                )
        
        project_details=[]

        for i in project_list:
            project_dict = {}
            summary_qstn = f"give me the detailed summary of {i}"
            print(summary_qstn)
            project_summary_response = project_qa_chain.invoke(summary_qstn)
            print("project_summary_response >>>", project_summary_response)
            project_ = f"title : {i} \n description : {project_summary_response}"
            project_details.append(project_)

        return project_details

    def indepth_question_maker(self, content : list[str]) -> list[str]:
        print("--indepth_question_maker--")

        parser = JsonOutputParser(pydantic_object=eval_project_questions)

        temp_obj=Get_templates()

        gen_qstn_prompt = PromptTemplate(
                template=temp_obj.temp(project_questions_temp=True),
                input_variables=["content"],
                partial_variables={"format_instructions": parser.get_format_instructions()},
            )

        gen_qstn_chain = (
                gen_qstn_prompt
                | self.llm_openai
                | parser
            ) 
        project_questions_list = []
        for i in content:
            # print(i)

            project_gen_qstns = gen_qstn_chain.invoke({"content":i})   
            print("questions >>> ",project_gen_qstns['questions'])
            print("*"*20)
            project_questions_list.append(str({"content":i,"questions":project_gen_qstns['questions']}))

        return project_questions_list

    def Work_exp_content_summarizer(self,text:str):
        print("--Work_exp_content_summarizer--")

        temp_obj=Get_templates()  #initiating get templates class
        
        ## Summarize the content only on work experience ---
        prompt1 = ChatPromptTemplate.from_template(template=temp_obj.temp(summarize_work_exp_temp=True))

        chain1 = (
                 prompt1 
                |self.llm_openai 
                |StrOutputParser()
                )
        
        ## to fetch the project titles ---
        parser = JsonOutputParser(pydantic_object=eval_project_title)
        
        prompt2 = PromptTemplate(
                template=temp_obj.temp(indepth_work_exp_temp=True),
                input_variables=["content"],
                partial_variables={"format_instructions": parser.get_format_instructions()},
            )

        chain2 = (
                prompt2
                | self.llm_openai
                | parser
            )

        ## Invoking Chains.
        map_chain = RunnableParallel(summary=chain1)
        final_response = map_chain.invoke({"content":text})
        print(final_response['summary'])
        print("*"*10)
        
        project_title_response = chain2.invoke({"content":final_response['summary']})
        print("project_title_response >>> ",project_title_response)

        project_detials = self.project_Summary(project_list=project_title_response['titles'], all_project_summary=final_response['summary'], project_qa_temp=temp_obj.temp(project_qa_temp=True))

        col_obj = Chroma_collections()

        col_obj.create_chroma_collection(docs=project_detials, collection_name="vasanth_workexp_summary")

        project_questions_list = self.indepth_question_maker(content=project_detials)
        print("project_questions_list >>> ",project_questions_list)

        col_obj.create_chroma_collection(docs=project_questions_list, collection_name="vasanth_project_indepth_qstns")

        # return project_detials

    def Skill_content_summarizer(self,text):
        print("--Skill_content_summarizer--")

        temp_obj=Get_templates()
        summarizer_temp=temp_obj.temp(summarize_skill_temp=True)
        print(summarizer_temp)

        skill_summarizer_prompt = ChatPromptTemplate.from_template(summarizer_temp)

        print(skill_summarizer_prompt)

        skill_summarizer_chain = (
                            skill_summarizer_prompt | 
                            self.llm_openai
                            )
        
        skill_summarized_response = skill_summarizer_chain.invoke({"content":text})

        return skill_summarized_response 

    def HandleAI(self, Pdf_File):
        txt_obj=Extract_TXT()
        raw_text = txt_obj.extractme(pdf_path=Pdf_File)

        self.work_exp_summarized = self.Work_exp_content_summarizer(text=raw_text)
        print(self.work_exp_summarized)

        # self.skill_content_summarized = self.Skill_content_summarizer(text=raw_text)
        # print(self.skill_content_summarized)

o=AIStuff()
o.HandleAI(Pdf_File=r"C:\Users\CVHS ADMIN\Documents\github_repos\InterviewerAI\InterviewerAI\CVs\vasanth-AIML-07082024.pdf")