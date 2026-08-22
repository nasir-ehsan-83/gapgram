from sqlalchemy.ext.asyncio import AsyncSession
from typing import (
    List, 
    Sequence
)
from fastapi import (
    APIRouter,
    Depends,
    Body, 
    Path
)
from src.modules.auth.schemas import TokenData
from src.common.dependencies import get_current_user
from src.db import get_db
from src.modules.votes.model import Vote
from src.modules.votes.schemas import (
    VoteCreate, 
    VoteOut
)
from src.modules.votes.services import (
    create_new_vote, 
    get_all_votes
)




router = APIRouter(
    prefix = "/api/votes",
    tags = ["Vote"]
)




@router.post(
    '/', 
    response_model = VoteOut
)
async def create_vote(
    current_user: TokenData = Depends(get_current_user),
    vote_in: VoteCreate = Body(...), 
    db: AsyncSession = Depends(get_db)
) -> Vote:

    return await create_new_vote(vote_in, current_user, db)




@router.get(
    '/{post_id}', 
    response_model = List[VoteOut]
)
async def get_votes(
    current_user: TokenData = Depends(get_current_user),
    post_id: int = Path(gt = 0), 
    db: AsyncSession = Depends(get_db)
) -> Sequence[Vote]:

    return await get_all_votes(post_id, current_user, db)
