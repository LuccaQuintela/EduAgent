from custom_types.blackboard import BlackBoard
from agents.workflow import ResultBuilderAgentWorkflow
from typing import Optional
from agents.lesson import LessonAgent
from schemas.lesson import LessonSchema

BUILDING_PROMPT_TEMPLATE_PATH = "agents/lesson/prompts/building_prompt_template.txt"

class LessonAgentWorkflow(ResultBuilderAgentWorkflow):
    def __init__(self, 
                 agent: Optional[LessonAgent]=None,
                 model_name: Optional[str]=None,
                 try_limit: int=3,
                 verbose: bool=False):
        if agent is None: 
            agent = LessonAgent(
                model=model_name or "gpt-3.5-turbo",
            )
        super().__init__(
            agent=agent,
            model_name=model_name,
            try_limit=try_limit,
            verbose=verbose,
            schema=LessonSchema
        )

    def build_lesson(self, state: BlackBoard):    
        if self.verbose: print(f"Agent [{self.agent.name}] building lesson")
        json, blackboard_update = self.build_result(state=state)
        blackboard_update.update({"lesson": json})
        if self.verbose: print(f"{blackboard_update}")
        return blackboard_update

    def is_json_valid(self, state: BlackBoard):
        return super().is_json_valid(state=state, key="lesson")
    
    def _generate_templated_prompt(self, 
                                  state: BlackBoard,
                                  retry: bool = False) -> str:        
        relevant_fields = [
            "topic",
            "current_experience",
            "desired_depth",
            "goals",
        ]

        module = state["curriculum"].modules[state["lesson_idx"]]
        module_string = f"""
        Lesson Title - {module.title}
        Lesson Description - {module.description}
        Learning Obectives - {module.learning_objectives}
        """.strip()

        # TODO: modify the query string to include curriculum info for this specific lesson
        topic = state.get("topic")
        goals = state.get("goals") 
        rag_query = f"{topic or ""}, {goals or ""}"
        rag_string = self.run_rag_system(
            query=rag_query,
            limit=10,
            alpha=0.9,
        )
        
        return super()._generate_templated_prompt(
            state=state, 
            path=BUILDING_PROMPT_TEMPLATE_PATH, 
            retry=retry, 
            relevant_fields=relevant_fields, 
            retrieved_data=rag_string,
            module_information=module_string
        )
    
    def post_build_cleanup(self, state: BlackBoard):
        blackboard_update = {
            "validation_try_count": 0,
            "lesson_finished": False,
        }
        if self.validated:
            blackboard_update["lesson"] = self.validated
            self.validated = None
        return blackboard_update
    