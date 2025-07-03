from google.adk.runners import Runner
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.genai import types


async def call_agent_async(query: str, runner: Runner, user_id: str, session_id: str, verbose: bool = False):
    """
    Sends a query to the agent and prints the final response
    """
    print(f"\n>>> User Query: {query}")
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce a final response"
    
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if verbose: 
            print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break

    print(f"<<< Agent Response: {final_response_text}")

async def run_team_conversation_loop(root_agent: Agent):
    session_service = InMemorySessionService()
    APP_NAME = "weather_tutorial_agent_team"
    USER_ID = "user_1_agent_team"
    SESSION_ID = "session_001_agent_team"
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

    runner_agent_team = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    print(f"Runner created for agent: '{root_agent.name}'")

    while True:
        user_input = input("Prompt('exit' to exit):")
        if user_input.lower().strip() == "exit":
            break
        await call_agent_async(query=user_input,
                               runner=runner_agent_team,
                               user_id=USER_ID,
                               session_id=SESSION_ID)