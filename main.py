from dotenv import load_dotenv
load_dotenv()

from langchain_classic import hub   
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

#list of tools 
tools = [TavilySearch()] 
llm = ChatOpenAI(model="gpt-4")
react_prompt = hub.pull("hwchase17/react") 

agent = create_react_agent(
    llm = llm, 
    tools = tools, 
    prompt=react_prompt) # reasoning engine. Return us with a chain which is simply going to receive
#  the tools, going to receive the user's query and is going too send everything to LLM.

agent_executor = AgentExecutor(agent=agent, tools = tools, verbose=True)
chain = agent_executor

def main():
    print("Hello from langchain-course!")
    result = chain.invoke(
        input={
            "input":"Search for 3 job postings for an ai engineer using langchain in banglore on linkedin and list their details"
        }
    )
    print(result)


if __name__ == "__main__":
    main()
