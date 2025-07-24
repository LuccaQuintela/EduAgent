from typing import Optional, Tuple
from pydantic import BaseModel
from agents.agent import Agent
from custom_types import BlackBoard
from utils.json_utils import strip_json_code_fence, validate_json
from langchain_core.messages import AnyMessage
from custom_errors import JSONValidationRetryLimitReachedError

class AgentWorkFlow:
    def __init__(self, 
                 agent:Optional[Agent]=None,
                 model_name: Optional[str]=None,
                 verbose: bool = False,
                 try_limit:int = 3):
        if agent is None: 
            self.agent = Agent(
                model=model_name or "gpt-3.5-turbo",
                tools=[],
                verbose=verbose,
            )
        else: 
            self.agent = agent
        self.verbose = verbose
        self.try_limit = try_limit

    def run_rag_system(self, state: BlackBoard) -> str:
        return ""

    def create_rag_prompt(self, state: BlackBoard) -> str:
        return f"RETRIEVED DATA: \n{self.run_rag_system(state=state)}"
    
    def _format_field(self, key: str, state: BlackBoard):
            default = "not yet provided"
            val = state.get(key, default)
            return f"- {key}: {val if val else default}"
    
    def _generate_templated_prompt(self, 
                                   state: BlackBoard, 
                                   path:str="",
                                   retry: bool=False,
                                   relevant_fields: list[str]=[],
                                   **format_kwargs) -> str:
        if retry == True:
            retry_prompt = "INSTRUCTION: You have just been sent this same prompt, however, your response failed to match the response JSON format provided to you in your system message. Please try again.\n"
        else: 
            retry_prompt = ""

        try:
            formatted_fields = "\n".join(
                [self._format_field(k, state=state) for k in relevant_fields]
            )

            with open(path, "r", encoding="utf-8") as f:
                template = f.read()

            builder_prompt = template.format(
                all_fields=formatted_fields,
                **format_kwargs
            )
            return retry_prompt + builder_prompt

        except FileNotFoundError as e:
            raise RuntimeError(f"Template file not found at path: {path}") from e

        except KeyError as e:
            raise ValueError(
                f"Missing template field in format: {e}. Make sure all placeholders are passed."
            ) from e

        except Exception as e:
            raise RuntimeError(f"Unexpected error while generating prompt: {e}") from e
    

class ResultBuilderAgentWorkflow(AgentWorkFlow):
    def __init__(self, 
                agent: Optional[Agent] = None, 
                model_name: Optional[str]=None,
                try_limit:int = 3,
                schema: Optional[BaseModel]=None,
                verbose=False):
        super().__init__(
            agent=agent,
            model_name=model_name,
            try_limit=try_limit,
            verbose=verbose
        )
        self.validated = None
        if schema:
            self.validation_schema = schema
        else:
            print("Validation Schema for ResultBuilderAgentWorkflow not provided.")
            raise TypeError

    def build_result(self, state: BlackBoard) -> Tuple[str, dict]:
        try_count = state["validation_try_count"] + 1
        retrying = try_count > 1
        build_prompt = self._generate_templated_prompt(state, retry=retrying)
        messages = self.agent.prompt_model(prompt=build_prompt, messages=state["messages"])
        json = self._extract_json_from_message(messages[-1])
        return (json, {
            "messages": messages,
            "validation_try_count": try_count,
        })
    
    def is_json_valid(self, state: BlackBoard, key: str) -> bool:
        try_count = state["validation_try_count"]
        try: 
            self.validated = validate_json(
                json_str=state[key],
                schema=self.validation_schema,
                strip=False
            )
        except Exception as e:
            if try_count >= self.try_limit:
                if self.verbose: print(f"{key} JSON could not be validated after {try_count} attempts, breaking out of validation loop and raising error")
                raise JSONValidationRetryLimitReachedError
            if self.verbose: print(f"{key} JSON validation attempt number {try_count} failed, routing back and re-prompting model")
            return False
        return True
    
    def _extract_json_from_message(self, message: AnyMessage) -> str:
        return strip_json_code_fence(message.content)