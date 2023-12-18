from typing import List

from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

from app.api.models.rwmodel import CustomModel


class User(BeanieBaseUser, Document):
    pass


class UserItem(CustomModel):
    id: str
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class PageUserResponse(CustomModel):
    total: int
    page: int
    page_size: int
    items: List[UserItem]


async def get_user_db():
    yield BeanieUserDatabase(User)
