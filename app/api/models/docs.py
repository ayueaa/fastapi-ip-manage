import ipaddress
import datetime
from typing import List, Optional, Union
from beanie import PydanticObjectId
from bson import ObjectId

from pydantic import Field, validator

from app.api.models.rwmodel import CustomModel


class HandleResponse(CustomModel):
    doc_id: PydanticObjectId
    success: bool = True
    msg: str = "success"


class DocumentPost(CustomModel):
    title: str
    content: str


class Document(DocumentPost):
    doc_id: PydanticObjectId = None
    owner_id: PydanticObjectId = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class DocsResponse(DocumentPost):
    content: str = None
    doc_id: PydanticObjectId
    owner_id: PydanticObjectId = None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PageDocsResponse(CustomModel):
    total: int
    page: int
    page_size: int
    items: List[DocsResponse]
