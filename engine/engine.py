from google.adk.runners import Runner
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.genai import types
from typing import Dict
import json

from engine.dictionaries import UserData, UserState
from agents import central_agent

class Engine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Engine, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, verbose: bool = False):
        self.users_file_path = "engine/users.json"
        self.verbose = verbose
        self.app_name = "EduAgent"
        self.users = self._init_username_db()
    
    # TODO: look into other types of session services
    async def start_class(self):
        user_data = self._get_active_user()
        user_id = user_data["user_id"]
        session_id = user_data["session_id"]
        user_state = user_data["user_state"]

        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id,
            state=user_state,
        )
        if self.verbose: 
            print(f"Session started for [{user_id}]\nSession ID: {session_id}\nState:\n{user_state}")
        
        runner = Runner(
            agent=central_agent,
            app_name=self.app_name,
            session_service=session_service
        )

        await self._main_execution_loop(
            runner=runner, 
            user_id=user_id,
            session_id=session_id,
            verbose = self.verbose
        )

        self._cleanup(user_id, session.state)


    async def _call_agent_async(self, query: str, runner: Runner, user_id: str, session_id: str, verbose: bool = False) -> str:
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
        return final_response_text
            
    async def _main_execution_loop(self, runner: Runner, user_id: str, session_id: str, verbose: bool = False):
        response = None
        while True: 
            user_input = input("Prompt:")
            if user_input.lower().strip() == "exit" or response and response.lower().strip() == "exit":
                break
            response = await self._call_agent_async(query=user_input,
                                            runner=runner,
                                            user_id=user_id,
                                            session_id=session_id,
                                            verbose=verbose)

    def _init_username_db(self) -> Dict[str, UserData]:
        try:
            with open(self.users_file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            if self.verbose: print(f"Warning: user JSON db could not be opened, returning empty db")
            return {}
    
    def _sign_user(self, username: str):
        self.users[username] = {
            "user_id": username,
            "session_id": "session01",
            "user_state": {
                "active_curriculum": False,
                "topic": None,
            }
        }

    def _get_active_user(self) -> UserData:
        while True:
            username = input("Enter username: ")
            user = self.users.get(username, None)
            if user is None:
                user_input = input("Username not found. Create new account?")
                user_input = user_input.lower().strip()
                if user_input == "yes" or user_input == 'y':
                    self._sign_user(username)
                    return self.users[username]
            else:
                return user
            
    def _cleanup(self, user_id: str, session_state: Dict):
        self.users[user_id] = session_state
        try:
            with open(self.users_file_path, "w") as f:
                json.dump(self.users, f)
        except Exception as e:
            if self.verbose: 
                print(f"Could not open users JSON db to write changes, changes to user state unable to be saved")
