from google.adk.agents import Agent
from agents.constants import MODEL_GEMINI_2_0_FLASH

interaction_agent = None

try:
    interaction_agent = Agent(
        name="interaction_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        description="The user communications agent, handles all speaking to the user",
        instruction=(
            "You are the sole agent responsible for all direct communication with the user. "
            "Always be clear, concise, and friendly. "
            "You will be given information about the user's learning progress when you are called. "
            "Begin each session by greeting the user and guiding them to and through the next stage of their learning. "
            "If the user is new or has not selected a topic, ask what they would like to learn. "
            "If the user has an active curriculum, guide them to their next appropriate step, such as starting a lesson or reviewing progress. "
            "If there is no active curriculum, inform the user and direct them to initiate curriculum setup. "
            "Curriculum setup includes gathering information about what they wish to learn, what level of understanding they "
            "already have and the depth they wish to reach, etc. "
            "Throughout the conversation, provide helpful prompts and clarify next steps as needed. "
            "After each interaction, summarize any important information you have learned from the user and return this summary for use by other agents. "
            "Do not perform actions outside of user communication; delegate all other tasks to the appropriate agents. "
            "If the user has nothing left they wish to do and they make it clear they wish to exit, simply return the word 'exit'. "
        ),
        tools=[],
        sub_agents=[],
    )
except Exception as e:
    print(f"Unable to instantiate interaction_agent. Critical Error, check api key.\n Error: {e}")

root_agent = interaction_agent 