"""
Papers API Routes
"""

from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter()


@router.get("/")
async def get_papers(
    skip: int = 0,
    limit: int = 100,
    query: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """搜索论文"""
    return []


@router.get("/{paper_id}")
async def get_paper(
    paper_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取论文详情"""
    return {}
