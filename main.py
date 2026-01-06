import os
from dotenv import load_dotenv

load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool # for tools import
from langchain_core.messages import HumanMessage # use human message to invoke agent
from langchain_openai import ChatOpenAI


# print(os.environ["TAVILY_API_KEY"])
# from tavily import TavilyClient

# tavily = TavilyClient()

# @tool
# def search(query: str) -> str:
#     """
#     Tool that searches over internet

#     Args:    
#       query: The query to search for 
    
#     Returns:
#         The search result
#     """
#     print(f"Searching web for {query}")
#     return tavily.search(query = query)

# directly using tavily
from langchain_tavily import TavilySearch



llm = ChatOpenAI(model="gpt-5")
# tools = [search]
tools = [TavilySearch()]
agent = create_agent(model=llm, tools =tools)

def main():
    print("Hello from langchain-course!")
    result = agent.invoke({"messages":
                           HumanMessage(content="What is the weather in Banglore today?")
                           #HumanMessage(content="Search for 3 job postings for an ai engineer using langchain in whitefield, banglore on linkedin and list their details")
                           })
    print(result)


if __name__ == "__main__":
    main()
