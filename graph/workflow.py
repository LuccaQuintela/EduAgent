from langgraph.graph import StateGraph, END
from custom_types.blackboard import BlackBoard
from agents.interaction import InteractionAgentWorkflow
from agents.curriculum import CurriculumAgentWorkflow
from agents.lesson import LessonAgentWorkflow
from custom_types.agentsdict import AgentsDict, WorkflowsDict
from typing import Optional

class EduAgentWorkflowBuilder:
    def __init__(self, 
                 agents: Optional[AgentsDict] = None,
                 workflows: Optional[WorkflowsDict] = None,
                 checkpointer = None, 
                 store = None,
                 verbose: bool=False):
        if workflows:
            self.interaction_workflow = workflows["interaction"]
            self.curriculum_workflow = workflows["curriculum"]
            self.lesson_workflow = workflows["lesson"]
        elif agents:
            self.interaction_workflow = InteractionAgentWorkflow(agent=agents["interaction"])
            self.curriculum_workflow = CurriculumAgentWorkflow(agent=agents["curriculum"])
            self.lesson_workflow = LessonAgentWorkflow(agent=agents["lesson"])
        else:
            self.interaction_workflow = InteractionAgentWorkflow()
            self.curriculum_workflow = CurriculumAgentWorkflow()
            self.lesson_workflow = LessonAgentWorkflow()
        
        self.checkpointer = checkpointer
        self.store = store
        self.verbose = verbose
        

    def build_graph(self):
        builder = StateGraph(BlackBoard)
        
        builder.add_node("entry", self.entry_node)
        builder.add_node("get_user_info", self.interaction_workflow.get_user_info)
        builder.add_node("build_curriculum", self.curriculum_workflow.build_curriculum)
        builder.add_node("post_curriculum_build_cleanup", self.curriculum_workflow.post_build_cleanup)
        builder.add_node("build_lesson", self.lesson_workflow.build_lesson)
        builder.add_node("post_lesson_build_cleanup", self.lesson_workflow.post_build_cleanup)
        builder.add_node("present_lesson", self.interaction_workflow.present_lesson)

        builder.set_entry_point("entry")

        builder.add_conditional_edges(
            "entry",
            self.main_routing,
            {
                "get_user_info": "get_user_info",
                "build_curriculum": "build_curriculum",
                "build_lesson": "build_lesson",
                "present_lesson": "present_lesson",
                END: END,
            }
        )
        builder.add_conditional_edges(
            "build_curriculum",
            self.curriculum_workflow.is_json_valid,
            {
                True: "post_curriculum_build_cleanup",
                False: "build_curriculum",
            }
        )
        builder.add_conditional_edges(
            "build_lesson",
            self.lesson_workflow.is_json_valid,
            {
                True: "post_lesson_build_cleanup",
                False: "build_lesson",
            }
        )

        builder.add_edge("post_curriculum_build_cleanup", "build_lesson")
        builder.add_edge("post_lesson_build_cleanup", "present_lesson")
        builder.add_edge("get_user_info", "build_curriculum")
        builder.add_edge("present_lesson", "entry")

        return builder.compile(store=self.store, 
                               checkpointer=self.checkpointer)
    
    def main_routing(self, state: BlackBoard):
        if state.get("wish_to_exit", False) == True:
            return END
        elif not state.get("topic"):
            return "get_user_info"
        elif not state.get("curriculum"):
            return "build_curriculum"
        elif not state.get("lesson"):
            return "build_lesson"
        elif state.get("lesson_finished", False) == False:
            return "present_lesson"
        elif state.get("lesson_idx") >= state.get("total_lesson_count"):
            return "get_user_info"
        return END

    def entry_node(self, state: BlackBoard):
        return {}

    def total_cleanup(self, state: BlackBoard):
        blackboard_update = {}
        if state["lesson_idx"] >= state["total_lesson_count"]:
            blackboard_update.update({
                "lesson_idx": 0,
                "topic": None,
                "goals": None,
                "current_experience": None,
                "desired_depth": None,
                "curriculum": None
            })
        return blackboard_update
