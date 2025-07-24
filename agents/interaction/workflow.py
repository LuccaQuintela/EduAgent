from custom_types.blackboard import BlackBoard
from typing import Optional
from agents.interaction import InteractionAgent
from schemas.lesson import LessonSchema
from agents.workflow import AgentWorkFlow

INTRODUCTION_PROMPT_TEMPLATE_PATH = "agents/interaction/prompts/introduction_template.txt"
LESSON_PRESENTATION_PROMPT_TEMPLATE_PATH = "agents/interaction/prompts/lesson_presentation_prompt_template.txt"

class InteractionAgentWorkflow(AgentWorkFlow):
    def __init__(self, 
                 agent: Optional[InteractionAgent]=None,
                 model_name: Optional[str]=None,
                 try_limit:int = 3):
        if agent is None: 
            agent = InteractionAgent(
                model=model_name or "gpt-3.5-turbo",
                tools=[],
                verbose=False,
            )
        super().__init__(
            agent=agent,
            model_name=model_name,
            try_limit=try_limit
        )

    def get_user_info(self, state: BlackBoard):    
        initial_prompt = self._generate_initial_prompt(state)
        running_messages, state_update = self.agent.run_chat(initial_prompt=initial_prompt)
        state_update.update({"messages": running_messages})
        return state_update

    def present_lesson(self, state: BlackBoard):
        lesson = state["lesson"]
        lesson_idx = state["lesson_idx"]
        total_lesson_count = state["total_lesson_count"]
        lesson_content = self.lesson_info_string_builder(lesson=lesson, lessons_left=total_lesson_count-lesson_idx-1)
        
        relevant_fields = [
            "username",
            "topic",
            "goals",
            "current_experience",
            "desired_depth",
        ]
        initial_prompt = self._generate_templated_prompt(
            state=state,
            path=LESSON_PRESENTATION_PROMPT_TEMPLATE_PATH,
            relevant_fields=relevant_fields,
            lesson_content=lesson_content
        )
        running_messages, state_update = self.agent.run_chat(initial_prompt=initial_prompt)
        state_update.update({"messages": running_messages})
        return state_update
    
    def _generate_initial_prompt(self, 
                                 state: BlackBoard, 
                                 path: str = INTRODUCTION_PROMPT_TEMPLATE_PATH) -> str:
        critical_fields = [
            "username",
            "topic",
        ]
        nice_to_haves = [
            "current_experience",
            "desired_depth",
            "goals",
        ]
        
        formatted_criticals = "\n".join([self._format_field(k, state=state) for k in critical_fields])
        formatted_nice_to_haves = "\n".join([self._format_field(k, state=state) for k in nice_to_haves])

        with open(path, "r", encoding="utf-8") as f:
            template = f.read()
        prompt = template.format(all_fields=formatted_criticals+"\n"+formatted_nice_to_haves,
                                 critical_fields=critical_fields,
                                 nice_to_haves=nice_to_haves)
        return prompt
    
    def lesson_info_string_builder(self, lesson: LessonSchema, lessons_left: int) -> str:
        string_parts = [
            f"Title: {lesson.lesson_title}",
            f"Lesson Summary: {lesson.lesson_summary}",
            "Lesson Objectives:"
        ]
        for obj in lesson.lesson_objectives:
            string_parts.append(f" - {obj}")

        string_parts.append("Content Sections:")
        for content in lesson.content_sections:
            string_parts.append(f" - {content.title}")
            string_parts.append(f"   {content.content}")

        string_parts.append("Exercises:")
        for exercise in lesson.exercises:
            string_parts.append(f" - Question: {exercise.question}")
            string_parts.append(f" - Answer: {exercise.answer}")

        string_parts.append(f"Number of Lessons Left after this one: {lessons_left}")
        
        return "\n".join(string_parts)

    def post_lesson_presentation_cleanup(self, state: BlackBoard):
        blackboard_update = {}
        if state["lesson_finished"] == True:
            index = state["lesson_idx"] + 1
            blackboard_update.update({
                "lesson_idx": index,
                "lesson": None,
                "lesson_finished": False
            })
        return blackboard_update
        