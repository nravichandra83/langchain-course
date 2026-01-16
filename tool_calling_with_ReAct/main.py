"""
Tool calling implementation
"""

from dotenv import load_dotenv
from typing import List
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import Tool, tool
from callbacks import AgentCallbackHandler # (this is a custom class)

@tool
def get_text_length(text: str) -> int:
    """
    Returns the length of the text by characters
    """
    print(f"get_text_length enter with {text=}")
    text =text.strip("'\n").strip('"') # stripping away non alpabetic chars just in case
    
    return len(text)

def find_tool_by_name(tools: List[Tool], tool_name:str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
        
    raise ValueError(f"Tool with name {tool_name} is not found")

if __name__ == "__main__":
    print("Hello React Langchain!")
    tools=[get_text_length]

    
    llm = ChatOpenAI(
        temperature=0,
        callbacks=[AgentCallbackHandler()],
        model="gpt-5"
    )    

    llm_with_tools = llm.bind_tools(tools)

    # start conversation
    messages = [HumanMessage(content="What is the length of the word: DOG")]	
    # messages works as agent_scratchpad in prev programs
        
        
    while True:
        ai_message = llm_with_tools.invoke(messages)
        
        tool_calls = getattr(ai_message,"tool_calls", None) or []
        if len(tool_calls) > 0:
            messages.append (ai_message)
            for tool_call in tool_calls:
                # tool_calls is typically a dictionary with keys:id ,type, name, args
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args",{})
                tool_call_id = tool_call.get("id")
                tool_to_use = find_tool_by_name(tools, tool_name)
                
                observation = tool_to_use.invoke(tool_args)
                print(f"observation = {observation}")
    
                messages.append(
                    ToolMessage(content = str(observation), tool_call_id=tool_call_id)
                )
                continue

            print(ai_message.content)
            break








