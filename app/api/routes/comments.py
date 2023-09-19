from typing import Optional

from fastapi import APIRouter, Body, Depends, Response
from starlette import status


router = APIRouter()


@router.get("")
async def list_comments_for_article():
    return "ok"
