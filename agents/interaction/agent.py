from langchain_core.messages import AnyMessage
from langchain.tools import Tool
from agents.agent import Agent
from typing import Optional, Type
from utils.json_utils import validate_json
from jsonschema import ValidationError
from pydantic import BaseModel

from schemas.interaction import InteractionAgentResponseSchema

SYSTEM_PROMPT_PATH = "agents/interaction/prompts/system.txt"

class InteractionAgent(Agent):
    def __init__(self, 
                 model=None,
                 tools:list[Tool]=[],
                 verbose:bool=False,
                 name:str="InteractionAgent"):
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            system_message = f.read()
        super().__init__(model=model, 
                         tools=tools,
                         verbose=verbose,
                         system=system_message,
                         name=name)
    
    def run_chat(self, 
                 messages: list[AnyMessage]=[], 
                 try_limit=3, 
                 initial_prompt:Optional[str]=None) -> tuple[list[AnyMessage], dict]:
        running_messages = []
        blackboard_accumulator = {}
        if initial_prompt:
            new_messages, validated = self._loop_invoke_until_json_valid(
                prompt=initial_prompt, 
                messages=messages,
                try_limit=try_limit, 
                schema=InteractionAgentResponseSchema
            )
            running_messages.extend(new_messages)
            print(validated.user_response)
            blackboard_accumulator.update(validated.blackboard_update)
        while True:
            user_input = input(">> ")
            try:
                new_messages, validated = self._loop_invoke_until_json_valid(
                    prompt=user_input,
                    messages = messages + running_messages,
                    try_limit=try_limit,
                    schema=InteractionAgentResponseSchema
                )
                running_messages.extend(new_messages)
                print(validated.user_response)
                blackboard_accumulator.update(validated.blackboard_update)
                if self.verbose: print(blackboard_accumulator)
                if self.verbose: print(f"End Conversation?: {validated.end_conversation}")
            except Exception:
                if self.verbose: print(f"LLM responses hit the retry limit for JSON validation for user prompt: {user_input}\nAgent: {self.name}")
                break

            if validated.end_conversation == True:
                break

        return running_messages, blackboard_accumulator

    def _loop_invoke_until_json_valid(self, 
                                      prompt: str, 
                                      messages: Optional[list[AnyMessage]]=None, 
                                      try_limit=3, 
                                      schema: Optional[Type[BaseModel]]=None) -> tuple[list[AnyMessage], BaseModel]:
        new_messages = self.prompt_model(prompt=prompt, messages=messages)
        json_str = new_messages[-1].content
        try_count = 0
        retry_prompt = "INSTRUCTION: You have just been sent this same prompt, however, your response failed to match the response JSON format provided to you in your system message. Please try again.\nUSER PROMPT: "
        while(try_count < try_limit):
            try:
                validated = validate_json(json_str, schema or InteractionAgentResponseSchema)
                return new_messages, validated
            except Exception as e:
                try_count += 1
                if self.verbose: print(f"[{self.name}] response JSON validation failed on attempt number {try_count}")
                if try_count < try_limit:
                    new_messages = self.prompt_model(prompt=retry_prompt + prompt, messages=messages)
                    json_str = new_messages[-1].content

        raise ValidationError






        
        