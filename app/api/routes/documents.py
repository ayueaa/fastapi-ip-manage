import datetime

import motor.motor_asyncio
from bson import ObjectId
from fastapi import APIRouter, Depends, Query

from app.api.dependencies.auth import current_active_user
from app.api.errors.http_error import NotFound404Error
from app.api.models.docs import (DocsResponse, DocumentPost, HandleResponse,
                                 PageDocsResponse)
from app.api.models.user import User
from app.db.mongo import get_docs_coll

router = APIRouter()

# 创建文档


@router.post("", response_model=DocsResponse, response_description="添加新文档")
async def create_document(
    document: DocumentPost,
    user: User = Depends(current_active_user),
    docs_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(get_docs_coll),
):
    document = document.model_dump()
    document["owner_id"] = user.id  # 设置文档的所有者ID为当前用户ID
    document["created_at"] = datetime.datetime.now()
    document["updated_at"] = datetime.datetime.now()
    new_doc = await docs_coll.insert_one(document)
    created_doc = await docs_coll.find_one({"_id": new_doc.inserted_id})
    created_doc["doc_id"] = created_doc.pop("_id")
    return DocsResponse(**created_doc)


# 获取文档分页列表


@router.get("", response_model=PageDocsResponse, response_description="获取所有文档")
async def read_documents(
    page: int = Query(1, gt=0, description="页码,从1开始"),
    page_size: int = Query(10, gt=0, lt=50, description="每页大小,1到50之间"),
    user: User = Depends(current_active_user),
    docs_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(get_docs_coll),
):
    skip = (page - 1) * page_size
    total = await docs_coll.count_documents({"owner_id": user.id})
    documents = (
        await docs_coll.find({"owner_id": user.id})
        .skip(skip)
        .limit(page_size)
        .to_list(page_size)
    )
    for doc in documents:
        doc["doc_id"] = doc.pop("_id")
        doc["content"] = doc.pop("content")[:50]

    return PageDocsResponse(
        total=total, page=page, page_size=page_size, items=documents
    )


@router.get("/{doc_id}", response_model=DocsResponse, response_description="查询文档详情")
async def read_one_document(
    doc_id: str,
    user: User = Depends(current_active_user),
    docs_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(get_docs_coll),
):
    doc = await docs_coll.find_one({"_id": ObjectId(doc_id), "owner_id": user.id})
    if not doc:
        raise NotFound404Error
    doc["doc_id"] = doc.pop("_id")
    return DocsResponse(**doc)


@router.put("/{doc_id}", response_model=HandleResponse, response_description="更新文档")
async def update_document(
    doc_id: str,
    document: DocumentPost,
    user: User = Depends(current_active_user),
    docs_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(get_docs_coll),
):
    updated = document.model_dump()
    updated["updated_at"] = datetime.datetime.now()

    updated_doc = await docs_coll.find_one_and_update(
        {"_id": ObjectId(doc_id), "owner_id": user.id}, {"$set": updated}
    )
    if not updated_doc:
        raise NotFound404Error
    return HandleResponse(doc_id=updated_doc["_id"], msg="更新成功")


@router.delete("/{doc_id}", response_model=HandleResponse, response_description="删除文档")
async def delete_document(
    doc_id: str,
    user: User = Depends(current_active_user),
    docs_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(get_docs_coll),
):
    delete_doc = await docs_coll.find_one_and_delete(
        {"_id": ObjectId(doc_id), "owner_id": user.id}
    )
    if not delete_doc:
        raise NotFound404Error
    return HandleResponse(doc_id=delete_doc["_id"], msg="删除成功")
