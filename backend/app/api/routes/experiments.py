"""
Experiments API Routes
"""

from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter()


@router.get("/")
async def get_experiments(
    facility: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """获取实验数据"""
    return []


@router.get("/{experiment_id}")
async def get_experiment(
    experiment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取实验详情"""
    return {}
