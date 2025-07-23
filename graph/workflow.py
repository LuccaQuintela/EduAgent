from langgraph.graph import StateGraph, END
from graph.custom_types import BlackBoard
from agents import InteractionAgentWorkflow, CurriculumAgentWorkflow, LessonAgentWorkflow

class EduAgentWorkflowBuilder:
    def __init__(self, agents, checkpointer = None, store = None):
        self.agents = agents
        self.checkpointer = checkpointer
        self.store = store
        self.interaction_workflow = InteractionAgentWorkflow()
        self.curriculum_workflow = CurriculumAgentWorkflow()
        self.lesson_workflow = LessonAgentWorkflow()

    def build_graph(self):
        builder = StateGraph(BlackBoard)
        
        builder.add_node("entry", self.entry_node)
        builder.add_node("get_topic", self.interaction_workflow.get_topic)
        builder.add_node("build_curriculum", self.curriculum_workflow.build_curriculum)
        builder.add_node("build_lesson", self.lesson_workflow.build_lesson)
        builder.add_node("present_lesson", self.interaction_workflow.present_lesson)

        builder.set_entry_point("entry")

        builder.add_conditional_edges(
            "entry",
            self.main_routing,
            {
                "get_topic": "get_topic",
                "build_curriculum": "build_curriculum",
                "build_lesson": "build_lesson",
                "present_lesson": "present_lesson",
            }
        )


        return builder.compile(store=self.store, 
                               checkpointer=self.checkpointer)
    
    def main_routing(self, state: BlackBoard):
        if state.get("wish_to_exit", False):
            return END
        elif not state.get("topic"):
            return "get_topic"
        elif not state.get("curriculum"):
            return "build_curriculum"
        elif not state.get("lesson"):
            return "build_lesson"
        elif state.get("lesson_finished", False):
            return "present_lesson"
        elif state.get("lesson_idx") >= state.get("total_lesson_count"):
            return "get_topic"

    def entry_node(self, state: BlackBoard):
        print("Hello! Welcome to the EduAgent tutoring service. Let's get started !")
