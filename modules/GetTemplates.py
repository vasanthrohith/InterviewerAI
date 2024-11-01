
from langchain_core.pydantic_v1 import BaseModel, Field

# class eval_json_summarize_cv(BaseModel):
#         question: str = Field(description="generated question")
#         option_a: str = Field(description="option a")
#         option_b: str = Field(description="option b")
#         option_c: str = Field(description="option c")
#         option_d: str = Field(description="option d")
#         correct_answer: str = Field(description="correct answer from the given options")

class Get_templates:
    def __init__(self) -> None:
        pass

    def temp(self, *args, **kwargs):
        print("--temp--")
        print(kwargs)

        if 'summarize_work_exp_temp' in kwargs:
            summarize_work_exp_temp="""You are an Expert in summarizing Work-experience in the given resume/CV in detail

            content\n
            {content}

           \n note : Focus only on Work-Expernience. ingnore the skillset column and Internship column

            Your detailed summarization below:

            """
            return summarize_work_exp_temp
        

        elif 'summarize_skill_temp' in kwargs:
            summarize_skill_temp="""
            You are an Expert in summarizing Technical Skillset in the given resume/CV in detail.

            \ncontent\n
            {content}

            \nnote: Focus only on the skillset column. ignore the work-experience and projects\n
            Your detailed summarization below:

            """

            return summarize_skill_temp
        

        elif 'indepth_work_exp_temp'  in kwargs:
            indepth_work_exp_temp="""
            With the given Detail your work is to fetch only the project titles:
            \n give the indepth details \n

            \ncontent\n
            {content}

            \n{format_instructions}\n

            """
            return indepth_work_exp_temp
        
        elif 'project_qa_temp' in kwargs:
            project_qa_temp = """
            You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
            Use the below context to answer the question
            \nQuestion: {question} \n

            \nContext: {context} \n
            """
            return project_qa_temp
        
        elif 'project_questions_temp' in kwargs:
            project_questions_temp="""
                You have to generate 5 questions in the perspective of interviewer from the below content:
                \ncontent : {content} \n

                \n{format_instructions}\n
            """
            return project_questions_temp
        
        elif 'conversation_1_temp' in kwargs:
            print(args[1])
            
            
            conversation_1_temp = f"""
                You are one of the world's top 3 Machine Learning and Artifical intelligent interviewers sitting with the pannel of 3 members taking an interview.
                You should listen to the interview pannel member 2 inputs and ask questions
                With the resume content below, Ask your technical question and situational based question to the candidate.
                Ask one question at a time. Keep your questions short and concise.
                \nresume content : \n{args[0]}\n 
                """+"""
                \n\nCurrent conversation:\n{history}\n"""+f"""

                note: do not answer the irrevelevant or out of context questions of the candidate. just bring the candidate to conversation.
                \n**interview pannel member 2 inputs** : {args[1]} \n
                Based on the interview pannel member 2 inputs ask follow-up question to the candidate answer to make sure he's understood the concept.
                if he says to jump to next concept, then got to next concept in the content."""+"""

                Human: {input}\nAI:

                """
                
            return conversation_1_temp
        
        elif 'pannel_member_2_temp' in kwargs:
            pannel_member_2_temp = f"""
            You are one of the world's top 3 Machine Learning and Artifical intelligent interviewers sitting with the pannel of 3 members taking an interview.
            You are member 2 and you cannot as questions directly to the candidate. But based on the conversation history and and recent message.
            You can guide member 1(whose interviewing the candidate) to ask questions.

            if the candidate message is out of contexgt or wrong. you can ask the member 1 to ask question from anyother concepts from the provided content.
            If the question is correct try to guide him to ask the follow-up question from candidate's response:

            \nbelow is candidate's project details:\n
            \n{args[0]}\n

            \below is member 1 conversation history with candidate\n
            note: member 1 is 'Ai' and candidate is 'Human'
            \n{args[1]}\n"""+"""

            \nlatest conversation\n
            \n{latest_conversation}\n

            below is your suggestion to member 1:

            """

            return pannel_member_2_temp

        # elif 'test_temp' in kwargs:
        #     print("Hello")

# o=get_templates()
# o.temp(summarize_cv_temp=True,)

# o.temp(test_temp=True)

