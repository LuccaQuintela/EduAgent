from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from typing import Optional, Union

from custom_types.blackboard import BlackBoard

class Agent:
    def __init__(self, 
                 model=Union[str, BaseChatModel, None],
                 tools:list[Tool]=[],
                 verbose:bool=False,
                 system:str="",
                 name:str="UnnamedBaseAgent"):
        """
        Initialize a base Agent for multi-agentic tutoring workflows.

        Args:
            model (str or BaseChatModel, optional): The language model to use, either as a string identifier for a ChatOpenAI instance or a pre-initialized BaseChatModel.
            tools (list[Tool], optional): A list of LangChain Tool objects available to the agent.
            verbose (bool, optional): If True, enables verbose logging for debugging and tracing agent actions.
            system (str, optional): The system prompt or instructions for the agent, provided as a string.
            name (str, optional): The name of the agent instance.

        Raises:
            TypeError: If the model argument is not a recognized type.

        This base Agent class is designed to be extended by specialized agents (e.g., curriculum, lesson, interaction)
        in a multi-agent tutoring system. It handles model/tool binding, system prompt setup, and basic invocation logic.
        """
        self.system = SystemMessage(content=system) if system != "" else None
        self.model = None
        self.model_name = None
        self.name = name
        self.tools = {t.name: t for t in tools}
        self.verbose=verbose
        if isinstance(model, str):
            self.model = ChatOpenAI(model=model).bind_tools(tools)
            self.model_name = model
        elif isinstance(model, BaseChatModel):
            self.model = model.bind_tools(tools)
            self.model_name = model.__class__.__name__
        else:
            print(f"Error: could not create agent by name: {self.name}")
            raise TypeError
        if verbose: print(f"Created agent [{name}] with model [{self.model_name}]")
        
    def invoke_model(self, messages:list[AnyMessage]) -> AnyMessage:
        if self.verbose: print(f"invoking model at agent [{self.name}] with prompt: {messages[-1].content}")
        if self.system: messages = [self.system] + messages
        response = self.model.invoke(messages)
        return response

    def prompt_model(self, prompt:str, messages:list[AnyMessage]=[]) -> list[AnyMessage]: 
        prompt = HumanMessage(content=prompt)
        return [prompt, self.invoke_model(messages + [prompt])]

    def exists_action(self, state:BlackBoard):
        tool_calls = getattr(state["messages"][-1], "tool_calls", [])
        if self.verbose: print(f"\nLatest model response at agent [{self.name}] wishes to invoke following tools: {tool_calls}\n")
        return len(tool_calls) > 0

    def take_actions(self, state:BlackBoard):
        tool_calls = getattr(state["messages"][-1], "tool_calls", [])
        results = []
        for tool in tool_calls:
            if self.verbose: print(f"calling tool [{tool["name"]}]\nwith arguments:\n{tool["args"]}")
            result = self.tools[tool["name"]](**tool["args"])
            results.append(
                ToolMessage(content=str(result),
                            name=tool["name"],
                            id=tool["id"])
            ) 
        return results

        

