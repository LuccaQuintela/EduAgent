from google.adk.agents import Agent
from agents.constants import MODEL_GEMINI_2_0_FLASH

lesson_agent = None

try:
    lesson_agent = Agent(
        name="lesson_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        description="",
        instruction="",
        tools=[],
        sub_agents=[],
    )
except Exception as e:
    print(f"Unable to instantiate lesson_agent. Critical Error, check api key.\n Error: {e}")

root_agent = lesson_agent 