"""
Funding API Routes
"""

from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter()


@router.get("/")
async def get_funding_rounds(
    skip: int = 0,
    limit: int = 100,
    company_id: Optional[int] = None,
    round_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """获取融资轮次列表"""
    return []


@router.get("/stats")
async def get_funding_stats(
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """获取融资统计数据"""
    return {
        "total_funding": 0,
        "total_rounds": 0,
        "avg_round_size": 0
    }
