from .curriculum_agent import curriculum_agent
from .lesson_agent import lesson_agent
from .quiz_agent import quiz_agent
from .schedule_agent import schedule_agent
from .data_agent import data_agent
from .interaction_agent import interaction_agent
from .central_agent import central_agent
import os

__all__ = [
    "curriculum_agent",
    "lesson_agent",
    "quiz_agent",
    "schedule_agent",
    "data_agent",
    "interaction_agent",
    "central_agent"
]

from dotenv import load_dotenv
load_dotenv(dotenv_path="agents/.env")

if os.environ.get("GOOGLE_API_KEY"):
    print("GOOGLE API KEY SET")
else:
    print("GOOGLE API KEY NOT SET")