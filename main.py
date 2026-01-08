from dotenv import load_dotenv

load_dotenv()

from langchain_classic import hub
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
## for pydantic output format
# from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda 
# import our prompt and schema
from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse

# list of tools
tools = [TavilySearch()]
llm = ChatOpenAI(model="gpt-4") # gpt-5 doesnt support the chain of old fashioned way. Check again
react_prompt = hub.pull("hwchase17/react")



# 1. using explicit template and formatted output using pydantic object 
# output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
# 2. Using structured output 
structured_llm = llm.with_structured_output(AgentResponse) 

react_prompt_with_instructions_formatted = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input","agent_scratchpad","tool_names"]
).partial(format_instructions="") # for scenario 2: structure output
#.partial(format_instructions = output_parser.get_format_instructions()) for scenario #1 using explicit template


agent = create_react_agent(
    llm=llm, tools=tools, prompt=react_prompt_with_instructions_formatted
)  # reasoning engine. Return us with a chain which is simply going to receive
#  the tools, going to receive the user's query and is going too send everything to LLM.

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# using runnable lambda for extracting output from response
extract_output = RunnableLambda(lambda x: x["output"])
# using runnable lambda for parsing output as needed - scenario 1
#parse_output = RunnableLambda(lambda x: output_parser.parse(x))

# now chain initiates agent, reads output and parses it
# chain = agent_executor | extract_output | parse_output # scenario1
chain = agent_executor | extract_output | structured_llm


def main():
    print("Hello from langchain-course!")
    result = chain.invoke(
        input={
            "input": "Search for 3 job postings for an ai engineer using langchain in banglore on linkedin and list their details"
        }
    )
    print(result)


if __name__ == "__main__":
    main()


# overrall flow for runnable lambda:
# raw response from LLM is a dictionary that contains input and output
# [extract_output] input: dictionary (contains input and output) output: extracts output from response
# [parser_ouput] input: output of extract_output (string) output:   structured output (pydantic)