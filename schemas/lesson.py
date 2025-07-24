from pydantic import BaseModel, Field
from typing import List

class ContentSection(BaseModel):
    title: str = Field(..., description="Title of the content section")
    content: str = Field(..., description="Explanatory text for this section")

class Exercise(BaseModel):
    question: str = Field(..., description="Exercise or quiz question related to the lesson")
    answer: str = Field(None, description="Suggested answer or solution")

class LessonSchema(BaseModel):
    lesson_title: str = Field(...,description="Title of the lesson")
    lesson_objectives: List[str] = Field(..., description="What the learner should know or be able to do after completing the lesson")
    lesson_summary: str = Field(..., description="A brief description of the lesson content")
    exercises: List[Exercise] = Field(..., description="Practice problems or review questions")
    content_sections: List[ContentSection] = Field(..., description="The main content of the lesson, divided into sections")