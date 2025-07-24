from pydantic import BaseModel, Field
from typing import List

class ModuleSchema(BaseModel):
    title: str = Field(..., description="The title of the module")
    description: str = Field(..., description="A short summary of the module content")
    learning_objectives: List[str] = Field(..., description="Specific skills or knowledge students should gain from this module")

class CurriculumSchema(BaseModel):
    topic: str = Field(..., description="The subject area the curriculum is about")
    overview: str = Field(..., description="A brief description of what the curriculum will cover")
    modules: List[ModuleSchema] = Field(..., description="An ordered list of learning modules")
    module_count: int = Field(..., description="total number of modules")