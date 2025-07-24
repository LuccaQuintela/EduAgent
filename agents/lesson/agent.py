from agents.agent import Agent
from langchain.tools import Tool

SYSTEM_PROMPT_PATH = "agents/lesson/prompts/system.txt"

class LessonAgent(Agent):
    def __init__(self, 
                 model=None, 
                 verbose: bool=False,
                 tools: list[Tool] = [],
                 name: str="LessonAgent"):
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            system_message = f.read()
        # ADD INFORMATION RETRIEVAL TOOL
        super().__init__(model=model, 
                         tools=tools,
                         verbose=verbose,
                         system=system_message,
                         name=name)