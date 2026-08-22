from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import (
    APIRouter,
    Body, 
    Depends,
    Path,
    Query
)
from typing import (
    List, 
    Optional,
    Sequence
)
from src.common.errors import (
    ErrorCode, 
    BadRequestException
)
from src.db import get_db
from src.common.dependencies import get_current_user
from src.modules.auth.schemas import TokenData
from src.modules.users.model import User
from src.modules.users.schemas import (
    UserCreate, 
    UserAdminOut, 
    UserPrivateOut,
    UserPublicOut, 
    UserUpdate
)
from src.modules.users.services import (
    create_user,
    delete_user_by_id, 
    get_user_email,
    search_user, 
    update_user_by_email, 
    get_user_username, 
    get_user_id,
    get_all_users
)





router = APIRouter(
    prefix='/api/users',
    tags=["Users"]
)




# post user
@router.post(
    '/', 
    response_model = UserPrivateOut
)
async def create_new_user(
    user_in: UserCreate = Body(...), 
    db: AsyncSession = Depends(get_db)
) -> User:
    
    return await create_user(user_in, db)




# get all user
@router.get(
    '/', 
    response_model = List[UserAdminOut]
)
async def get_users(
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Sequence[User]:
    
    return await get_all_users(db)





# get user by email or username
@router.get(
    '/lookup', 
    response_model = UserPrivateOut
)
async def get_user(
    current_user: TokenData = Depends(get_current_user),
    email: Optional[str] = Query(), 
    username: Optional[str] = Query(), 
    db: AsyncSession = Depends(get_db)
):
    if email:
        return await get_user_email(email, db)

    if username:
        return await get_user_username(username, db)
    
    raise BadRequestException(message = "Provide email or username", error_code = ErrorCode.METHOD_NOT_ALLOWED)





# get user by name
@router.get(
    '/search', 
    response_model = List[UserPublicOut]
)
async def search_user_by_name(
    current_user: TokenData = Depends(get_current_user),
    name: str = Query(), 
    limit: int = Query(gt = 0), 
    skip: int = Query(gt = 0), 
    db: AsyncSession = Depends(get_db)
) -> Sequence[User]:
    return await search_user(name, limit, skip, db)




# get user by id
@router.get(
    '/{id}', 
    response_model = UserAdminOut
)
async def get_user_by_id(
    current_user: TokenData = Depends(get_current_user),
    id: int = Path(gt = 0), 
    db: AsyncSession = Depends(get_db)
) -> User:
    return await get_user_id(id, db)




# update user by email
@router.put(
    '/{id}', 
    response_model = UserPrivateOut
)
async def update_user(
    current_user: int = Depends(get_current_user), 
    id: int = Path(gt = 0),
    updated_user: UserUpdate = Body(...), 
    db: AsyncSession = Depends(get_db)
) -> User:
    
    return await update_user_by_email(id, updated_user, db)




# delete user by email
@router.delete('/{id}')
async def delete_user(
    current_user: TokenData = Depends(get_current_user), 
    id: int = Path(gt = 0), 
    db: AsyncSession = Depends(get_db)
):
    
    return await delete_user_by_id(id, db)
