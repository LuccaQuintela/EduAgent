from typing import TypedDict, Optional, List, Annotated, Union
from schemas.curriculum import CurriculumSchema
from schemas.lesson import LessonSchema
from langchain_core.messages import AnyMessage
import operator

# Any relevant changes made here need to propogate to the system prompt for the interaction agent to allow for data updates. 

# TODO: LOOK INTO MAKING A REDUCE MESSAGES FUNCTION FOR THE MESSAGES TO ALLOW FOR REPLACEMENT

class BlackBoard(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    
    curriculum: Union[str, CurriculumSchema, None]
    topic: Optional[str]
    username: Optional[str]
    lesson: Union[str, LessonSchema, None]
    lesson_idx: Optional[int]
    total_lesson_count: Optional[int]
    lesson_finished: Optional[bool]
    wish_to_exit: bool
    goals: Optional[List[str]]
    current_experience: Optional[str]
    desired_depth: Optional[str]
    validation_try_count: int
    