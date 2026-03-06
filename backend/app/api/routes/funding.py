"""
Funding API Routes
融资数据追踪与管理
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from datetime import date
from sqlalchemy.orm import joinedload

from app.db.session import get_db
from app.models import FundingRound, Company
from app.schemas import FundingRoundCreate, FundingRoundResponse

router = APIRouter()


@router.get("/", response_model=List[FundingRoundResponse])
async def get_funding_rounds(
    skip: int = 0,
    limit: int = 100,
    company_id: Optional[int] = None,
    round_type: Optional[str] = None,
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    获取融资轮次列表
    
    - **skip**: 跳过记录数
    - **limit**: 返回记录数上限
    - **company_id**: 公司 ID 筛选
    - **round_type**: 轮次类型筛选 (Seed, Series A, B, C, etc.)
    - **year**: 年份筛选
    """
    query = select(FundingRound)
    
    if company_id:
        query = query.where(FundingRound.company_id == company_id)
    if round_type:
        query = query.where(FundingRound.round_type == round_type)
    if year:
        query = query.where(extract('year', FundingRound.announced_date) == year)
    
    query = query.order_by(FundingRound.announced_date.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    funding_rounds = result.scalars().all()
    
    return funding_rounds


@router.get("/stats")
async def get_funding_stats(
    year: Optional[int] = None,
    quarter: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    获取融资统计数据
    
    - **year**: 年份
    - **quarter**: 季度 (1-4)
    """
    query = select(FundingRound)
    
    if year:
        query = query.where(extract('year', FundingRound.announced_date) == year)
        if quarter:
            # Filter by quarter
            month_start = (quarter - 1) * 3 + 1
            month_end = quarter * 3
            query = query.where(
                (extract('month', FundingRound.announced_date) >= month_start) &
                (extract('month', FundingRound.announced_date) <= month_end)
            )
    
    result = await db.execute(query)
    rounds = result.scalars().all()
    
    if not rounds:
        return {
            "total_funding": 0,
            "total_rounds": 0,
            "avg_round_size": 0,
            "median_round_size": 0,
            "largest_round": 0,
            "year": year,
            "quarter": quarter
        }
    
    amounts = [r.amount_usd for r in rounds if r.amount_usd]
    total_funding = sum(amounts)
    total_rounds = len(rounds)
    avg_round_size = total_funding / total_rounds if total_rounds > 0 else 0
    
    # Calculate median
    sorted_amounts = sorted(amounts)
    n = len(sorted_amounts)
    median_round_size = sorted_amounts[n // 2] if n % 2 == 1 else (sorted_amounts[n // 2 - 1] + sorted_amounts[n // 2]) / 2
    
    largest_round = max(amounts) if amounts else 0
    
    return {
        "total_funding": total_funding,
        "total_rounds": total_rounds,
        "avg_round_size": avg_round_size,
        "median_round_size": median_round_size,
        "largest_round": largest_round,
        "year": year,
        "quarter": quarter
    }


@router.get("/stats/by-technology")
async def get_funding_by_technology(
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    按技术路线统计融资数据
    """
    # Join with Company to get technology type
    query = select(Company.technology_type, func.sum(FundingRound.amount_usd), func.count(FundingRound.id)).join(
        FundingRound, Company.id == FundingRound.company_id
    )
    
    if year:
        query = query.where(extract('year', FundingRound.announced_date) == year)
    
    query = query.group_by(Company.technology_type)
    result = await db.execute(query)
    
    by_technology = {}
    for row in result.all():
        tech_type = row[0] or "Unknown"
        by_technology[tech_type] = {
            "total_funding": row[1] or 0,
            "total_rounds": row[2] or 0
        }
    
    return by_technology


@router.get("/stats/by-country")
async def get_funding_by_country(
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    按国家统计融资数据
    """
    query = select(Company.country, func.sum(FundingRound.amount_usd), func.count(FundingRound.id)).join(
        FundingRound, Company.id == FundingRound.company_id
    )
    
    if year:
        query = query.where(extract('year', FundingRound.announced_date) == year)
    
    query = query.group_by(Company.country)
    result = await db.execute(query)
    
    by_country = {}
    for row in result.all():
        country = row[0] or "Unknown"
        by_country[country] = {
            "total_funding": row[1] or 0,
            "total_rounds": row[2] or 0
        }
    
    return by_country


@router.get("/stats/timeline")
async def get_funding_timeline(
    start_year: int = 2020,
    end_year: int = 2026,
    db: AsyncSession = Depends(get_db)
):
    """
    获取融资时间线数据
    """
    query = select(
        extract('year', FundingRound.announced_date).label('year'),
        extract('month', FundingRound.announced_date).label('month'),
        func.sum(FundingRound.amount_usd),
        func.count(FundingRound.id)
    ).where(
        (extract('year', FundingRound.announced_date) >= start_year) &
        (extract('year', FundingRound.announced_date) <= end_year)
    ).group_by(
        extract('year', FundingRound.announced_date),
        extract('month', FundingRound.announced_date)
    ).order_by(
        extract('year', FundingRound.announced_date),
        extract('month', FundingRound.announced_date)
    )
    
    result = await db.execute(query)
    
    timeline = []
    for row in result.all():
        timeline.append({
            "year": int(row[0]),
            "month": int(row[1]),
            "total_funding": row[2] or 0,
            "total_rounds": row[3] or 0
        })
    
    return timeline


@router.post("/", response_model=FundingRoundResponse)
async def create_funding_round(
    funding_round: FundingRoundCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建新的融资轮次记录
    """
    # Verify company exists
    company_query = select(Company).where(Company.id == funding_round.company_id)
    company_result = await db.execute(company_query)
    if not company_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_funding = FundingRound(**funding_round.model_dump())
    db.add(db_funding)
    await db.commit()
    await db.refresh(db_funding)
    return db_funding


@router.get("/recent")
async def get_recent_funding(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    获取最近融资事件
    """
    query = select(FundingRound, Company).join(
        Company, FundingRound.company_id == Company.id
    ).order_by(
        FundingRound.announced_date.desc()
    ).limit(limit)
    
    result = await db.execute(query)
    recent = []
    for funding, company in result.all():
        recent.append({
            "company_name": company.name,
            "company_id": company.id,
            "round_type": funding.round_type,
            "amount_usd": funding.amount_usd,
            "announced_date": funding.announced_date,
            "lead_investor": funding.lead_investor,
            "technology_type": company.technology_type
        })
    
    return recent
