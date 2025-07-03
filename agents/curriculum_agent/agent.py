from google.adk.agents import Agent
from agents.constants import MODEL_GEMINI_2_0_FLASH

curriculum_agent = None

try:
    curriculum_agent = Agent(
        name="curriculum_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        description="",
        instruction="",
        tools=[],
        sub_agents=[],
    )
except Exception as e:
    print(f"Unable to instantiate curriculum_agent. Critical Error, check api key.\n Error: {e}")

root_agent = curriculum_agent 