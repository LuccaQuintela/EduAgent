from custom_types.blackboard import BlackBoard
from agents.workflow import ResultBuilderAgentWorkflow
from agents.curriculum import CurriculumAgent
from typing import Optional
from schemas.curriculum import CurriculumSchema

BUILDING_PROMPT_TEMPLATE_PATH = "agents/curriculum/prompts/building_prompt_template.txt"

class CurriculumAgentWorkflow(ResultBuilderAgentWorkflow):
    def __init__(self, 
                 agent: Optional[CurriculumAgent] = None, 
                 model_name: Optional[str]=None,
                 try_limit: int = 3,
                 verbose: bool=False):
        if agent is None:
            agent = CurriculumAgent(
                model=model_name or "gpt-3.5-turbo"
            )
        super().__init__(
            agent=agent,
            model_name=model_name,
            try_limit=try_limit,
            schema=CurriculumSchema,
            verbose=verbose
        )

    def build_curriculum(self, state: BlackBoard):    
        if self.verbose: print(f"Agent [{self.agent.name}] building curriculum")
        json, blackboard_update = self.build_result(state=state)
        blackboard_update.update({"curriculum": json})
        if self.verbose: print(f"{blackboard_update}")
        return blackboard_update


    def is_json_valid(self, state: BlackBoard) -> bool:
        return super().is_json_valid(state=state, key="curriculum")
    
    def _generate_templated_prompt(self, 
                                  state: BlackBoard,
                                  retry: bool = False) -> str:        
        relevant_fields = [
            "topic",
            "current_experience",
            "desired_depth",
            "goals",
        ]

        path = BUILDING_PROMPT_TEMPLATE_PATH
        
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
            path=path, 
            retry=retry, 
            relevant_fields=relevant_fields, 
            retrieved_data=rag_string
        )
    
    def post_build_cleanup(self, state: BlackBoard):
        blackboard_update = {
            "lesson_idx": 0,
            "validation_try_count": 0,
            "lesson_finished": False,
            "lesson": None
        }
        if self.validated:
            blackboard_update["total_lesson_count"] = self.validated.module_count
            blackboard_update["curriculum"] = self.validated
            self.validated = None
        return blackboard_update