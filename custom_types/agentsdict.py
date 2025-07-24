from typing import TypedDict

from agents.interaction import InteractionAgent, InteractionAgentWorkflow
from agents.curriculum import CurriculumAgent, CurriculumAgentWorkflow
from agents.lesson import LessonAgent, LessonAgentWorkflow

class AgentsDict(TypedDict):
    curriculum: CurriculumAgent
    lesson: LessonAgent
    interaction: InteractionAgent

class WorkflowsDict(TypedDict):
    curriculum: CurriculumAgentWorkflow
    lesson: LessonAgentWorkflow
    interaction: InteractionAgentWorkflow