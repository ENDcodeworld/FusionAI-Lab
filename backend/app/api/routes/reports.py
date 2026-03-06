"""
Reports API Routes
"""

from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter()


@router.get("/")
async def get_reports(
    db: AsyncSession = Depends(get_db)
):
    """获取报告列表"""
    return []


@router.get("/{report_id}")
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取报告详情"""
    return {}


@router.post("/{report_id}/purchase")
async def purchase_report(
    report_id: int,
    db: AsyncSession = Depends(get_db)
):
    """购买报告"""
    return {"message": "Report purchased successfully"}
