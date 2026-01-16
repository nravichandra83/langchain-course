from typing import Any,List,Dict

from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult


class AgentCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, *, run_id, parent_run_id = None, tags = None, metadata = None, **kwargs):
        # return super().on_llm_start(serialized, prompts, run_id=run_id, parent_run_id=parent_run_id, tags=tags, metadata=metadata, **kwargs)
        print(f"********Prompt to LLM was: \n {prompts[0]}*******")
        print("*************")
    
    def on_llm_end(self, response, *, run_id, parent_run_id = None, **kwargs):
        # return super().on_llm_end(response, run_id=run_id, parent_run_id=parent_run_id, **kwargs)
        print(f"********Response from LLM is: \n {response.generations[0][0].text}*******")
        print("*************")