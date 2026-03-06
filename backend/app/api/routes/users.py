"""
Users API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter()


@router.get("/me")
async def get_current_user(
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户信息"""
    return {}


@router.put("/me")
async def update_current_user(
    db: AsyncSession = Depends(get_db)
):
    """更新当前用户信息"""
    return {}
