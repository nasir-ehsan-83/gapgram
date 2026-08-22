from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response
from typing import (
    Optional, 
    Sequence
)
from src.common.errors import (
    NotFoundException,
    ConflictException,
    ErrorCode
)
from src.modules.votes.repository import (
    create_vote, 
    delete_vote,
    get_all_votes_db, 
    get_vote
)
from src.modules.auth.schemas import TokenData
from src.modules.posts.repository import get_post_db
from src.modules.votes.model import Vote
from src.modules.votes.schemas import VoteCreate




async def create_new_vote(
    vote_in: VoteCreate, 
    current_user: TokenData,
    db: AsyncSession
) -> Vote | Response:
    # get the post from database
    post = await get_post_db(vote_in.post_id, current_user.id, db)

    # if post does not exist
    if not post:
        raise NotFoundException(
            message = f"Post with id: {vote_in.post_id} does not exist", 
            error_code = ErrorCode.POST_NOT_FOUND
        )
   
    
    # get the vote from database
    found_vote: Optional[Vote] = await get_vote(vote_in.post_id, current_user.id, db)

    # if user want to vote
    if vote_in.vote is True:
        # if user has already voted to the post
        if found_vote:
            raise ConflictException(
                message = "Vote already exists",
                error_code = ErrorCode.ALREADY_VOTED
            )
        
        vote_data = vote_in.model_dump(exclude_unset = True, exclude_none = False)
        
        # delete vote.vote from data before storing vote data
        vote_data.pop("vote")
        
        # add user_id field to the vote data
        vote_data.update({
            "user_id": current_user.id
        })
        
        return await create_vote(vote_data, db)
    
    # if user want to devote
    else :
        # if user has not voted yet
        if not found_vote:
            raise NotFoundException(
                message =  "Vote does not exist",
                error_code = ErrorCode.VOTE_NOT_FOUND
            )
        
        # else delete the vote from database
        await delete_vote(found_vote, db)

        return Response(status_code = 204)   # http-204-no-content
    



# get all votes of a post
async def get_all_votes(
    post_id: int, 
    current_user: TokenData,
    db: AsyncSession
) -> Sequence[Vote]:

    # get the post from database
    post = await get_post_db(post_id, current_user.id, db)

    # if post does not exist
    if not post:
        raise NotFoundException(
            message = f"Post with id: {post_id} does not exist", 
            error_code = ErrorCode.POST_NOT_FOUND
        )
    
    return await get_all_votes_db(post_id, db)