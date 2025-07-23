from typing import TypedDict

class BlackBoard(TypedDict):
    curriculum: str
    topic: str
    username: str
    lesson: str
    interaction_context: str
    lesson_idx: int
    total_lesson_count: int
    lesson_finished: bool
    wish_to_exit: bool
    