from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response
from typing import (
    Optional,
    Sequence
)
from src.modules.auth.schemas import TokenData
from src.modules.posts.repository import (
    create_post_db,
    delete_post_db,
    exist_post_db, 
    get_post_db,
    get_posts_db,
    update_post_db
)
from src.modules.posts.model import Post
from src.modules.posts.schemas import (
    PostCreate, 
    PostUpdate
)
from src.common.errors import (
    ErrorCode, 
    ConflictException,
    NotFoundException
)




async def create_new_post(
    post: PostCreate, 
    current_user: TokenData, 
    db: AsyncSession
) -> Post:
    
    if await exist_post_db(post.title, current_user.id, db):
        raise ConflictException(
            message = "You already have a post by this name",
            error_code = ErrorCode.POST_ALREADY_EXISTS
        )
    
    new_post: Post = await create_post_db(post, current_user.id, db)

    return new_post




async def get_one_post(
    post_id: int,
    current_user: TokenData,
    db: AsyncSession
) -> Optional[Post]:
    
    post: Optional[Post] = await get_post_db(post_id, current_user.id, db)

    if not post:
        raise NotFoundException(
            message = "Post Not found",
            error_code = ErrorCode.POST_NOT_FOUND
        )
    
    return post




async def get_all_posts(
    current_user: TokenData, 
    db: AsyncSession, 
    limit: int, 
    skip: int, 
    title: Optional[str]
) -> Sequence[Post]:

    return await get_posts_db(current_user.id, db, limit, skip, title)




async def update_data(
    post_id: int, 
    update_post: PostUpdate, 
    current_user: TokenData, 
    db: AsyncSession
) -> Post:
    
    post: Optional[Post] = await get_post_db(post_id, current_user.id, db)
    
    if not post: 
        raise NotFoundException(
            message = "Post Not found",
            error_code = ErrorCode.POST_NOT_FOUND
        )
    
    return await update_post_db(post, update_post, db)




async def delete_data(
    post_id: int, 
    current_user: TokenData, 
    db: AsyncSession
) :
    
    post: Optional[Post] = await get_post_db(post_id, current_user.id, db)

    if not post:
        raise NotFoundException(
            message = "Post Not found",
            error_code = ErrorCode.POST_NOT_FOUND
        )
    
    await delete_post_db(post, db)

    return Response(status_code = 204) # HTTP_204_NO_CONTENT