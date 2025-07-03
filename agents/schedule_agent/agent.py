from google.adk.agents import Agent
from agents.constants import MODEL_GEMINI_2_0_FLASH

schedule_agent = None

try:
    schedule_agent = Agent(
        name="schedule_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        description="",
        instruction="",
        tools=[],
        sub_agents=[],
    )
except Exception as e:
    print(f"Unable to instantiate schedule_agent. Critical Error, check api key.\n Error: {e}")

root_agent = schedule_agent 