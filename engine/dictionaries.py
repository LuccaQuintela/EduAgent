from typing import TypedDict
from typing import Optional

class UserState(TypedDict):
    active_curriculum: bool
    topic: Optional[str]

class UserData(TypedDict):
    user_id: str
    session_id: str
    user_state: UserState
