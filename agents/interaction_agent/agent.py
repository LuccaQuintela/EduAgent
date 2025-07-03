from google.adk.agents import Agent
from agents.constants import MODEL_GEMINI_2_0_FLASH

interaction_agent = None

try:
    interaction_agent = Agent(
        name="interaction_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        description="",
        instruction="",
        tools=[],
        sub_agents=[],
    )
except Exception as e:
    print(f"Unable to instantiate interaction_agent. Critical Error, check api key.\n Error: {e}")

root_agent = interaction_agent 