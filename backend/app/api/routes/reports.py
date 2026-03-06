"""
Reports API Routes
行业报告生成与管理
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import date, datetime
import json
from pathlib import Path

from app.db.session import get_db
from app.models import Report, Company, FundingRound
from app.schemas import ReportCreate, ReportResponse

router = APIRouter()

# 报告存储目录
REPORTS_DIR = Path("/tmp/fusion_reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/", response_model=List[ReportResponse])
async def get_reports(
    skip: int = 0,
    limit: int = 100,
    report_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    获取报告列表
    
    - **skip**: 跳过记录数
    - **limit**: 返回记录数上限
    - **report_type**: 报告类型筛选
    """
    query = select(Report)
    
    if report_type:
        query = query.where(Report.type == report_type)
    
    query = query.order_by(Report.published_date.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    reports = result.scalars().all()
    
    return reports


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    获取报告详情
    """
    query = select(Report).where(Report.id == report_id)
    result = await db.execute(query)
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Increment download count
    report.download_count += 1
    await db.commit()
    await db.refresh(report)
    
    return report


@router.post("/generate/industry-overview")
async def generate_industry_overview(
    year: int = 2026,
    db: AsyncSession = Depends(get_db)
):
    """
    生成年度行业概览报告
    """
    # 获取统计数据
    companies_query = select(func.count(Company.id))
    companies_result = await db.execute(companies_query)
    total_companies = companies_result.scalar()
    
    # 融资统计
    funding_query = select(
        func.sum(FundingRound.amount_usd),
        func.count(FundingRound.id)
    ).where(
        func.extract('year', FundingRound.announced_date) == year
    )
    funding_result = await db.execute(funding_query)
    funding_row = funding_result.first()
    total_funding = funding_row[0] or 0
    total_rounds = funding_row[1] or 0
    
    # 按技术路线统计
    tech_query = select(
        Company.technology_type,
        func.count(Company.id),
        func.sum(FundingRound.amount_usd)
    ).join(
        FundingRound, Company.id == FundingRound.company_id, isouter=True
    ).group_by(Company.technology_type)
    
    tech_result = await db.execute(tech_query)
    tech_stats = [
        {
            "technology": row[0] or "Unknown",
            "companies": row[1] or 0,
            "funding": row[2] or 0
        }
        for row in tech_result.all()
    ]
    
    # 生成报告内容
    report_content = {
        "title": f"2026 年全球核聚变产业年度概览",
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_companies": total_companies,
            "total_funding_usd": total_funding,
            "total_funding_rounds": total_rounds,
            "avg_funding_per_round": total_funding / total_rounds if total_rounds > 0 else 0
        },
        "technology_breakdown": tech_stats,
        "key_findings": [
            f"2026 年全球共有 {total_companies} 家核聚变公司活跃",
            f"年度融资总额达到 ${total_funding / 1_000_000_000:.2f}B",
            f"平均单笔融资金额 ${total_funding / total_rounds / 1_000_000:.1f}M" if total_rounds > 0 else "",
            "托卡马克技术路线仍占主导地位",
            "仿星器和激光驱动聚变获得越来越多的投资关注"
        ],
        "market_trends": [
            "私营聚变公司融资持续增长",
            "技术多元化趋势明显",
            "AI 在聚变研究中的应用增加",
            "政府与私营部门合作加强"
        ]
    }
    
    # 保存报告
    report_path = REPORTS_DIR / f"industry_overview_{year}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report_content, f, ensure_ascii=False, indent=2)
    
    # 创建数据库记录
    db_report = Report(
        title=report_content["title"],
        type="annual_overview",
        price_cny=0,  # 免费报告
        content_path=str(report_path),
        published_date=date.today()
    )
    db.add(db_report)
    await db.commit()
    await db.refresh(db_report)
    
    return {
        "report_id": db_report.id,
        "message": "报告生成成功",
        "content": report_content
    }


@router.post("/generate/company-analysis/{company_id}")
async def generate_company_analysis(
    company_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    生成公司深度分析报告
    """
    # 获取公司信息
    company_query = select(Company).where(Company.id == company_id)
    company_result = await db.execute(company_query)
    company = company_result.scalar_one_or_none()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # 获取融资历史
    funding_query = select(FundingRound).where(
        FundingRound.company_id == company_id
    ).order_by(FundingRound.announced_date)
    funding_result = await db.execute(funding_query)
    funding_rounds = funding_result.scalars().all()
    
    # 计算融资统计
    total_funding = sum(r.amount_usd for r in funding_rounds if r.amount_usd)
    latest_round = funding_rounds[-1] if funding_rounds else None
    
    # 生成报告
    report_content = {
        "title": f"{company.name} - 深度分析报告",
        "generated_at": datetime.now().isoformat(),
        "company_profile": {
            "name": company.name,
            "country": company.country,
            "founded_year": company.founded_year,
            "technology_type": company.technology_type,
            "website": company.website,
            "description": company.description
        },
        "funding_history": [
            {
                "round": r.round_type,
                "amount_usd": r.amount_usd,
                "date": str(r.announced_date),
                "lead_investor": r.lead_investor
            }
            for r in funding_rounds
        ],
        "funding_summary": {
            "total_raised_usd": total_funding,
            "total_rounds": len(funding_rounds),
            "latest_round": latest_round.round_type if latest_round else None,
            "latest_amount_usd": latest_round.amount_usd if latest_round else None
        },
        "swot_analysis": {
            "strengths": [
                f"采用{company.technology_type}技术路线",
                f"成立于{company.founded_year}年，经验丰富" if company.founded_year else "初创公司"
            ],
            "weaknesses": [
                "聚变商业化仍面临技术挑战",
                "需要持续大量资金投入"
            ],
            "opportunities": [
                "全球清洁能源需求增长",
                "政府政策支持",
                "技术进步加速"
            ],
            "threats": [
                "技术路线竞争激烈",
                "商业化时间表不确定",
                "其他可再生能源竞争"
            ]
        }
    }
    
    # 保存报告
    report_path = REPORTS_DIR / f"company_analysis_{company_id}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report_content, f, ensure_ascii=False, indent=2)
    
    # 创建数据库记录
    db_report = Report(
        title=report_content["title"],
        type="company_analysis",
        price_cny=99,  # 付费报告
        content_path=str(report_path),
        published_date=date.today()
    )
    db.add(db_report)
    await db.commit()
    await db.refresh(db_report)
    
    return {
        "report_id": db_report.id,
        "message": "公司分析报告生成成功",
        "content": report_content
    }


@router.post("/generate/quarterly-report")
async def generate_quarterly_report(
    year: int = 2026,
    quarter: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """
    生成季度报告
    """
    from sqlalchemy import extract
    
    # 计算季度月份范围
    month_start = (quarter - 1) * 3 + 1
    month_end = quarter * 3
    
    # 获取该季度融资数据
    funding_query = select(
        func.sum(FundingRound.amount_usd),
        func.count(FundingRound.id)
    ).where(
        (extract('year', FundingRound.announced_date) == year) &
        (extract('month', FundingRound.announced_date) >= month_start) &
        (extract('month', FundingRound.announced_date) <= month_end)
    )
    funding_result = await db.execute(funding_query)
    funding_row = funding_result.first()
    
    total_funding = funding_row[0] or 0
    total_rounds = funding_row[1] or 0
    
    report_content = {
        "title": f"{year}年 Q{quarter} 核聚变产业季度报告",
        "generated_at": datetime.now().isoformat(),
        "period": f"{year}年{month_start}月 - {month_end}月",
        "summary": {
            "total_funding_usd": total_funding,
            "total_rounds": total_rounds,
            "avg_round_size": total_funding / total_rounds if total_rounds > 0 else 0
        },
        "highlights": [
            f"Q{quarter}共发生{total_rounds}起融资事件",
            f"季度融资总额${total_funding / 1_000_000_000:.2f}B"
        ]
    }
    
    # 保存报告
    report_path = REPORTS_DIR / f"quarterly_{year}_q{quarter}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report_content, f, ensure_ascii=False, indent=2)
    
    # 创建数据库记录
    db_report = Report(
        title=report_content["title"],
        type="quarterly",
        price_cny=199,
        content_path=str(report_path),
        published_date=date.today()
    )
    db.add(db_report)
    await db.commit()
    await db.refresh(db_report)
    
    return {
        "report_id": db_report.id,
        "message": "季度报告生成成功",
        "content": report_content
    }


@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    删除报告
    """
    query = select(Report).where(Report.id == report_id)
    result = await db.execute(query)
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # 删除文件
    report_path = Path(report.content_path)
    if report_path.exists():
        report_path.unlink()
    
    await db.delete(report)
    await db.commit()
    
    return {"message": "Report deleted successfully"}
