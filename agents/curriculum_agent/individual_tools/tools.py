from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel
from typing import List

class Lesson(BaseModel):
    title: str
    objectives: List[str]

class Module(BaseModel):
    title: str
    lessons: List[Lesson]

class Curriculum(BaseModel):
    title: str
    modules: List[Module]


def check_curriculum_json(curriculum: dict, context: ToolContext) -> bool:
    """
    Checks if the curriculum agent has output a correctly formatted JSON version of a curriculum,
    and also verifies that there is enough information for an agent to work with.

    The function ensures:
      - The curriculum is a valid dictionary matching the Curriculum schema.
      - Each module contains at least one lesson.
      - Each lesson has a non-empty title and at least one objective.
      - The curriculum, modules, and lessons all have non-empty titles.

    If the dictionary is correctly formatted and contains sufficient information, 
    it will also save that dictionary in the toolcontext state under the key "current_working_curriculum".

    Args: 
        curriculum (dict): a dictionary that defines the structure of the curriculum

    Returns: 
        bool: True if the curriculum dictionary is properly structured and contains enough information for an agent to work with, False otherwise.
    """
    try: 
        validated = Curriculum(**curriculum)
        context.state["current_working_curriculum"] = curriculum
        return True
    except:
        return False
