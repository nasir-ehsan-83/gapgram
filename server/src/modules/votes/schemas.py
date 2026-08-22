from pydantic import BaseModel, ConfigDict

from src.common.enums import ReactionType

class VoteBase(BaseModel):
    post_id: int
    type: ReactionType

class VoteCreate(VoteBase):
    vote: bool

class VoteOut(VoteBase):
    user_id: int

    model_config = ConfigDict(from_attributes = True)