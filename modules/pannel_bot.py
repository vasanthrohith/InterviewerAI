from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser



from llm_stack import Call_LLM
from GetTemplates import Get_templates


class pannel_member_bots(Call_LLM):
    def __init__(self) -> None:
        super().__init__()


    def pannel_member_2(self, recent_conversation : dict[str], conversation_history : dict[str], content : str) -> str:
        print("--pannel_member_2--")
        print(recent_conversation, type(recent_conversation))
        print(conversation_history, type(conversation_history))
        print(content, type(content))
        # temp_obj = Get_templates()
        # prompt1 = ChatPromptTemplate.from_template(template=temp_obj.temp(pannel_member_2_temp=True, ))

        # chain1 = (
        #          prompt1 
        #         |self.llm_openai 
        #         |StrOutputParser()
        #         )
        return "-"