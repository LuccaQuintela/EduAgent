from pydantic import BaseModel, Field

class InteractionAgentResponseSchema(BaseModel):
    user_response: str = Field(..., description="Natural language message to the user.")
    blackboard_update: dict[str, object] = Field(..., description="Dictionary of keys to update in blackboard.")
    end_conversation: bool = Field(..., description="True if conversation should end, else False.")