from langchain.tools import Tool
from agents.agent import Agent

SYSTEM_PROMPT_PATH = "agents/curriculum/prompts/system.txt"

class CurriculumAgent(Agent):
    def __init__(self, 
                 model=None,
                 tools:list[Tool]=[],
                 verbose:bool=False,
                 name:str="CurriculumAgent"):
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            system_message = f.read()
        # ADD INFORMATION RETRIEVAL TOOL
        super().__init__(model=model, 
                         tools=tools,
                         verbose=verbose,
                         system=system_message,
                         name=name)