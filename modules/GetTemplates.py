
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

        if 'summarize_cv_temp' in kwargs:
            summarize_cv_temp="""You are an Expert in summarizing the given resume/CV in detal

            content\n
            {content}

            You should summarize this content. Focus on Expernience, Projects, Internship and Skills

            Your detailed summarization below:

            """
            return summarize_cv_temp



        # elif 'test_temp' in kwargs:
        #     print("Hello")


# o=get_templates()
# o.temp(summarize_cv_temp=True,)

# o.temp(test_temp=True)

