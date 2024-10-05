from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import re

from llm_stack import Call_LLM
from GetTemplates import Get_templates


class pannel_member_bots(Call_LLM):
    def __init__(self) -> None:
        super().__init__()

    def pannel_member_2(self, recent_conversation : dict[str], conversation_history : dict[str], content : str) -> str:
        print("--pannel_member_2--")
        # print(recent_conversation, type(recent_conversation))
        # print(conversation_history, type(conversation_history))
        # print(content, type(content))
        temp_obj = Get_templates()

        recent_conversation = str(recent_conversation).replace("{", "").replace("}", "")
        conversation_history = str(conversation_history).replace("{", "").replace("}", "")

        print("recent_conversation >>> ",recent_conversation)
        print("conversation_history >>> ",conversation_history)

        prompt1 = ChatPromptTemplate.from_template(template=temp_obj.temp(
                                                                          content,
                                                                          conversation_history,
                                                                          pannel_member_2_temp=True
                                                                          ))
        
        # print(prompt1)
        
        # print("pannel member 2 > ",prompt1.invoke({"latest_conversation":str(recent_conversation)}))

        chain1 = (
                 prompt1 
                |self.llm_openai 
                |StrOutputParser()
                )
        

        member2_response=chain1.invoke({"latest_conversation":str(recent_conversation)})
        # print("suggetion >>> ", member2_response)

        return member2_response