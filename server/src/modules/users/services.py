from typing import Sequence
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.errors import (
    ConflictException, 
    NotFoundException,
    ErrorCode
)
from src.core import hash_password
from src.modules.users.model import User

from src.modules.users.schemas import (
    UserCreate, 
    UserUpdate
)
from src.modules.users.repository import (
    create_new_user,
    delete_user,
    get_user_by_email,
    get_user_by_id, 
    get_user_by_username,
    get_users,
    get_users_by_name,
    update_user
)



async def create_user(
    user_in: UserCreate, 
    db: AsyncSession
) -> User:
   
    if await get_user_by_email(user_in.email, db):
        raise ConflictException(
            message = f"User with email: {user_in.email} already exists",
            error_code = ErrorCode.USER_ALREADY_EXISTS
        )
    
    if await get_user_by_username(user_in.username, db):
        raise ConflictException(
            message = f"User with username: {user_in.username} already exists.",
            error_code = ErrorCode.USER_ALREADY_EXISTS
        )
    
    user_data = user_in.model_dump()
    user_data["password"] = await hash_password(user_data["password"])

    return await create_new_user(user_data, db)




async def get_all_users(
    db: AsyncSession
) -> Sequence[User]:

    return await get_users(db)




async def get_user_email(
    email: str, 
    db: AsyncSession
) -> User:

    user = await get_user_by_email(email, db)

    if not user:
        raise NotFoundException(
            message = f"User with email: {email} does not exist!", 
            error_code = ErrorCode.USER_NOT_FOUND
        )
    
    return user




async def get_user_username(
    username: str, 
    db: AsyncSession
) -> User:

    user = await get_user_by_username(username, db)

    if not user:
        raise NotFoundException(
            message = f"User with username: {username} does not exist.", 
            error_code = ErrorCode.USER_NOT_FOUND
        )
    
    return user




async def search_user(
    name: str, 
    limit: int, 
    skip: int, 
    db: AsyncSession
) -> Sequence[User]:

    return await get_users_by_name(name, limit, skip, db)




async def get_user_id(
    id: int, 
    db: AsyncSession
) -> User:

    user = await get_user_by_id(id, db)

    if not user:
        raise NotFoundException(
            message = f"User by id: {id} does not exist.", 
            error_code = ErrorCode.USER_NOT_FOUND
        )
    
    return user




async def update_user_by_email(
    id: int, 
    updated_user: UserUpdate, 
    db: AsyncSession
) -> User:
    
    user = await get_user_by_id(id, db)

    # if there is not any user by this email
    if not user:
        raise NotFoundException(
            message = f"User by id: {id} does not exist.", 
            error_code = ErrorCode.USER_NOT_FOUND
        )
    
    # delete undefined or null elements
    data = updated_user.model_dump(exclude_unset=True)
    
    # if there is a password element then hash it
    if "password" in data:
        data["password"] = await hash_password(data["password"])
        
    
    return await update_user(data, user, db)




async def delete_user_by_id(
    id: int, 
    db: AsyncSession
):
    
    user = await get_user_by_id(id, db)
    
    # if there is not any user by this email
    if not user:
        raise NotFoundException(
            message = f"User by id: {id} does not exist.", 
            error_code = ErrorCode.USER_NOT_FOUND
        )
        
    # if the user exists then delete this
    await delete_user(user, db)

    return Response(status_code = 204) # http-204-no-content
