from langgraph.graph import StateGraph
from graph.types import BlackBoard

class EduAgentWorkflowBuilder:
    def __init__(self, agents, checkpointer = None, store = None):
        self.agents = agents
        self.checkpointer = checkpointer
        self.store = store

    def build_graph(self):
        builder = StateGraph(BlackBoard)
        # Add Nodes Here

        # Add Edges Here

        return builder.compile(store=self.store, 
                               checkpointer=self.checkpointer)
