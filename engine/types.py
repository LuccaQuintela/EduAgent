from typing import TypedDict

from agents import CurriculumAgent, LessonAgent, InteractionAgent

class AgentsDict(TypedDict):
    curriculum: CurriculumAgent
    lesson: LessonAgent
    interaction: InteractionAgent