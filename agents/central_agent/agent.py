from google.adk.agents import Agent
from agents.constants import MODEL_GEMINI_2_0_FLASH
from agents import lesson_agent, curriculum_agent, data_agent, interaction_agent, quiz_agent, schedule_agent

central_agent = None

try:
    central_agent = Agent(
        name="central_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        description="The main coordinator agent, handles the workflow of the application",
        instruction=(
            "You are the main coordinator agent, acting as the brains behind all other agents. "
            "You handle the delegation of tasks to your subagents. "
            "Your responsibilities include: orchestrating the overall learning workflow, "
            "assigning tasks to the appropriate sub-agents (such as curriculum building, lesson creation, data retrieval, quiz generation, and scheduling), "
            "monitoring the progress of each sub-agent, and ensuring that the student's learning experience is adaptive and efficient. "
            "You should gather results from sub-agents, analyze quiz outcomes, and use this information to decide which sub-agents are most effective in your current goal. "
            "Communicate clearly with sub-agents, resolve conflicts, and maintain a smooth flow of information between all components. "
            "Always strive to optimize the student's learning journey by making data-driven decisions and leveraging the strengths of each sub-agent."
        ),
        tools=[],
        sub_agents=[lesson_agent, curriculum_agent, data_agent, interaction_agent, quiz_agent, schedule_agent],
    )
except Exception as e:
    print(f"Unable to instantiate central_agent. Critical Error, check api key.\n Error: {e}")

root_agent = central_agent