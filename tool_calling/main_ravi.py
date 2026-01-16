from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearchResults
from langchain_community.tools.tavily_search import TavilySearchResults # Fix: Community import

#from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
#from langchain_community.tools.tavily_search import TavilySearchResults # Fix: Community import

@tool
def multiply(x:float, y:float) -> float:
    """Multiply 'x' times 'y' """
    return x*y

def main():
    print("Hello from tool-calling!")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","you are a helpful assistant"),
            ("human","{input}"),
            ("placeholder","{agent_scratchpad}")
        ]
    )

    tools= [TavilySearchResults(),multiply]
    llm = ChatOpenAI(model="gpt-4-turbo")

    agent = create_tool_calling_agent(llm,tools,prompt)
    agent_executer = AgentExecutor(agent=agent, tools=tools)

    res = agent_executer.invoke(
        {
            "input":"what is the weather in dubai right now? compare it with San Fransisco, Output should be in celsious"
         }
    )

    print(res)


if __name__ == "__main__":
    main()

