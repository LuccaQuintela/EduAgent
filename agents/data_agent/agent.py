from google.adk.agents import Agent
from agents.constants import MODEL_GEMINI_2_0_FLASH

data_agent = None

try:
    data_agent = Agent(
        name="data_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        description="",
        instruction="",
        tools=[],
        sub_agents=[],
    )
except Exception as e:
    print(f"Unable to instantiate data_agent. Critical Error, check api key.\n Error: {e}")

root_agent = data_agent 