"""
Companies API Routes
核聚变公司数据管理
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.models import Company, FundingRound
from app.schemas import CompanyCreate, CompanyUpdate, CompanyResponse, FundingRoundResponse

router = APIRouter()


@router.get("/", response_model=List[CompanyResponse])
async def get_companies(
    skip: int = 0,
    limit: int = 100,
    technology_type: Optional[str] = None,
    country: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    获取公司列表
    
    - **skip**: 跳过记录数
    - **limit**: 返回记录数上限
    - **technology_type**: 技术路线筛选 (Tokamak, Stellarator, Magnetized Target, etc.)
    - **country**: 国家筛选
    """
    query = select(Company)
    
    if technology_type:
        query = query.where(Company.technology_type == technology_type)
    if country:
        query = query.where(Company.country.ilike(f"%{country}%"))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    companies = result.scalars().all()
    
    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    获取公司详情
    
    - **company_id**: 公司 ID
    """
    query = select(Company).where(Company.id == company_id)
    result = await db.execute(query)
    company = result.scalar_one_or_none()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return company


@router.post("/", response_model=CompanyResponse)
async def create_company(
    company: CompanyCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建新公司
    
    - **name**: 公司名称
    - **country**: 国家
    - **technology_type**: 技术路线
    """
    db_company = Company(**company.model_dump())
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company)
    return db_company


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company: CompanyUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新公司信息
    """
    query = select(Company).where(Company.id == company_id)
    result = await db.execute(query)
    db_company = result.scalar_one_or_none()
    
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    update_data = company.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_company, field, value)
    
    await db.commit()
    await db.refresh(db_company)
    return db_company


@router.delete("/{company_id}")
async def delete_company(
    company_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    删除公司
    """
    query = select(Company).where(Company.id == company_id)
    result = await db.execute(query)
    db_company = result.scalar_one_or_none()
    
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    await db.delete(db_company)
    await db.commit()
    
    return {"message": "Company deleted successfully"}


@router.get("/{company_id}/funding", response_model=List[FundingRoundResponse])
async def get_company_funding(
    company_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    获取公司融资历史
    """
    # Verify company exists
    company_query = select(Company).where(Company.id == company_id)
    company_result = await db.execute(company_query)
    if not company_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Company not found")
    
    query = select(FundingRound).where(FundingRound.company_id == company_id).order_by(FundingRound.announced_date)
    result = await db.execute(query)
    funding_rounds = result.scalars().all()
    
    return funding_rounds


@router.get("/stats/summary")
async def get_company_stats(
    db: AsyncSession = Depends(get_db)
):
    """
    获取公司统计信息
    """
    # Total companies
    total_query = select(func.count(Company.id))
    total_result = await db.execute(total_query)
    total_companies = total_result.scalar()
    
    # Companies by technology type
    tech_query = select(Company.technology_type, func.count(Company.id)).group_by(Company.technology_type)
    tech_result = await db.execute(tech_query)
    by_technology = {row[0]: row[1] for row in tech_result.all()}
    
    # Companies by country
    country_query = select(Company.country, func.count(Company.id)).group_by(Company.country)
    country_result = await db.execute(country_query)
    by_country = {row[0]: row[1] for row in country_result.all()}
    
    return {
        "total_companies": total_companies,
        "by_technology": by_technology,
        "by_country": by_country
    }
