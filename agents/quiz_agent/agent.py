from google.adk.agents import Agent
from agents.constants import MODEL_GEMINI_2_0_FLASH

quiz_agent = None

try:
    quiz_agent = Agent(
        name="quiz_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        description="",
        instruction="",
        tools=[],
        sub_agents=[],
    )
except Exception as e:
    print(f"Unable to instantiate quiz_agent. Critical Error, check api key.\n Error: {e}")

root_agent = quiz_agent 