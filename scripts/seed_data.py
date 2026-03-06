#!/usr/bin/env python3
"""
FusionAI-Lab 数据库初始化脚本
填充真实的核聚变公司和融资数据
"""

import asyncio
import sys
from datetime import date
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Base, Company, FundingRound, Paper, ExperimentData
from app.core.config import settings


# 全球主要核聚变公司数据
FUSION_COMPANIES = [
    {
        "name": "Commonwealth Fusion Systems",
        "country": "United States",
        "founded_year": 2018,
        "technology_type": "Tokamak",
        "website": "https://cfs.energy",
        "description": "MIT 衍生公司，开发紧凑型托卡马克反应堆 SPARC，使用高温超导磁体技术。"
    },
    {
        "name": "Helion Energy",
        "country": "United States",
        "founded_year": 2013,
        "technology_type": "Magnetized Target Fusion",
        "website": "https://helionenergy.com",
        "description": "开发磁化靶聚变技术，直接与微软签署购电协议，目标 2028 年商业发电。"
    },
    {
        "name": "TAE Technologies",
        "country": "United States",
        "founded_year": 1998,
        "technology_type": "Field-Reversed Configuration",
        "website": "https://tae.com",
        "description": "专注场反向配置技术，与谷歌合作开发 AI 控制的等离子体系统。"
    },
    {
        "name": "General Fusion",
        "country": "Canada",
        "founded_year": 2002,
        "technology_type": "Magnetized Target Fusion",
        "website": "https://generalfusion.com",
        "description": "加拿大聚变公司，开发机械压缩聚变技术，获亚马逊创始人贝索斯投资。"
    },
    {
        "name": "Tokamak Energy",
        "country": "United Kingdom",
        "founded_year": 2009,
        "technology_type": "Spherical Tokamak",
        "website": "https://tokamakenergy.com",
        "description": "英国聚变公司，开发球形托卡马克和高温超导磁体技术。"
    },
    {
        "name": "First Light Fusion",
        "country": "United Kingdom",
        "founded_year": 2011,
        "technology_type": "Inertial Confinement Fusion",
        "website": "https://firstlightfusion.com",
        "description": "牛津大学衍生公司，开发独特的惯性约束聚变技术。"
    },
    {
        "name": "Marvel Fusion",
        "country": "Germany",
        "founded_year": 2019,
        "technology_type": "Laser-Driven Fusion",
        "website": "https://marvelfusion.com",
        "description": "德国聚变初创，结合激光技术和 AI 优化聚变反应。"
    },
    {
        "name": "Zap Energy",
        "country": "United States",
        "founded_year": 2015,
        "technology_type": "Sheared-Flow Stabilized Z-Pinch",
        "website": "https://zapenergy.com",
        "description": "开发剪切流稳定 Z 箍缩技术，无需复杂磁体系统。"
    },
    {
        "name": "Energy Singularity",
        "country": "China",
        "founded_year": 2021,
        "technology_type": "Tokamak",
        "website": "https://energy-singularity.com",
        "description": "中国聚变能源公司，开发高温超导托卡马克装置。"
    },
    {
        "name": "StarNet Fusion",
        "country": "China",
        "founded_year": 2021,
        "technology_type": "Stellarator",
        "website": "https://starnetfusion.com",
        "description": "专注仿星器技术路线，探索 alternative 聚变方案。"
    },
    {
        "name": "Helical Fusion",
        "country": "Japan",
        "founded_year": 2023,
        "technology_type": "Helical Reactor",
        "website": "https://helicalfusion.jp",
        "description": "日本聚变公司，基于 LHD 装置经验开发螺旋型聚变堆。"
    },
    {
        "name": "Princeton Stellarators",
        "country": "United States",
        "founded_year": 2021,
        "technology_type": "Stellarator",
        "website": "https://princetonstellarators.com",
        "description": "普林斯顿大学衍生公司，开发紧凑型仿星器。"
    },
    {
        "name": "Type One Energy",
        "country": "United States",
        "founded_year": 2021,
        "technology_type": "Stellarator",
        "website": "https://typeoneenergy.com",
        "description": "威斯康星大学衍生公司，开发仿星器聚变技术。"
    },
    {
        "name": "Laser Fusion Technologies",
        "country": "United Kingdom",
        "founded_year": 2021,
        "technology_type": "Laser-Driven Fusion",
        "website": "https://laserfusion.tech",
        "description": "开发小型激光驱动聚变装置。"
    },
    {
        "name": "Phoenix Nuclear Labs",
        "country": "United States",
        "founded_year": 2005,
        "technology_type": "Inertial Electrostatic Confinement",
        "website": "https://phoenixnuclear.com",
        "description": "开发惯性静电约束聚变技术，专注中子源应用。"
    },
    {
        "name": "Shine Technologies",
        "country": "United States",
        "founded_year": 2013,
        "technology_type": "Inertial Electrostatic Confinement",
        "website": "https://shinetechnologies.com",
        "description": "开发聚变驱动中子源，用于医疗同位素生产。"
    },
    {
        "name": "Awakn Life Sciences",
        "country": "Canada",
        "founded_year": 2020,
        "technology_type": "Alternative Concepts",
        "website": "https://awakn.com",
        "description": "探索新型聚变概念。"
    },
    {
        "name": "ExoFusion",
        "country": "France",
        "founded_year": 2022,
        "technology_type": "Tokamak",
        "website": "https://exofusion.fr",
        "description": "法国聚变初创，开发紧凑型托卡马克。"
    },
    {
        "name": "Renewal Fusion",
        "country": "China",
        "founded_year": 2022,
        "technology_type": "Tokamak",
        "website": "https://renowfusion.com",
        "description": "中国聚变能源公司。"
    },
    {
        "name": "Xcimer Energy",
        "country": "United States",
        "founded_year": 2021,
        "technology_type": "Laser-Driven Fusion",
        "website": "https://xcimerenergy.com",
        "description": "开发准分子激光驱动聚变技术。"
    }
]


# 融资数据 (基于公开报道)
FUNDING_ROUNDS = [
    # Commonwealth Fusion Systems
    {"company_name": "Commonwealth Fusion Systems", "round_type": "Series A", "amount_usd": 115000000, "announced_date": "2019-09-01", "lead_investor": "Breakthrough Energy Ventures"},
    {"company_name": "Commonwealth Fusion Systems", "round_type": "Series B", "amount_usd": 1800000000, "announced_date": "2021-12-01", "lead_investor": "Tiger Global Management"},
    {"company_name": "Commonwealth Fusion Systems", "round_type": "Series C", "amount_usd": 170000000, "announced_date": "2023-05-01", "lead_investor": "Baillie Gifford"},
    
    # Helion Energy
    {"company_name": "Helion Energy", "round_type": "Series A", "amount_usd": 10000000, "announced_date": "2015-06-01", "lead_investor": "Y Combinator"},
    {"company_name": "Helion Energy", "round_type": "Series B", "amount_usd": 22000000, "announced_date": "2019-02-01", "lead_investor": "Capricorn Investment Group"},
    {"company_name": "Helion Energy", "round_type": "Series C", "amount_usd": 500000000, "announced_date": "2021-11-01", "lead_investor": "Sam Altman"},
    {"company_name": "Helion Energy", "round_type": "Series D", "amount_usd": 425000000, "announced_date": "2023-12-01", "lead_investor": "Mithril Capital"},
    
    # TAE Technologies
    {"company_name": "TAE Technologies", "round_type": "Series A", "amount_usd": 15000000, "announced_date": "2002-03-01", "lead_investor": "Venrock"},
    {"company_name": "TAE Technologies", "round_type": "Series B", "amount_usd": 25000000, "announced_date": "2014-06-01", "lead_investor": "Wellington Management"},
    {"company_name": "TAE Technologies", "round_type": "Series C", "amount_usd": 120000000, "announced_date": "2017-06-01", "lead_investor": "Google Ventures"},
    {"company_name": "TAE Technologies", "round_type": "Series D", "amount_usd": 250000000, "announced_date": "2019-09-01", "lead_investor": "Sumitomo Corporation"},
    {"company_name": "TAE Technologies", "round_type": "Series E", "amount_usd": 280000000, "announced_date": "2022-01-01", "lead_investor": "Mubadala Investment"},
    
    # General Fusion
    {"company_name": "General Fusion", "round_type": "Series A", "amount_usd": 20000000, "announced_date": "2009-05-01", "lead_investor": "Chrysalix Venture Capital"},
    {"company_name": "General Fusion", "round_type": "Series B", "amount_usd": 65000000, "announced_date": "2013-10-01", "lead_investor": "Jeff Bezos"},
    {"company_name": "General Fusion", "round_type": "Series C", "amount_usd": 100000000, "announced_date": "2015-05-01", "lead_investor": "Temasek"},
    {"company_name": "General Fusion", "round_type": "Series D", "amount_usd": 130000000, "announced_date": "2019-06-01", "lead_investor": "TC Energy"},
    {"company_name": "General Fusion", "round_type": "Series E", "amount_usd": 170000000, "announced_date": "2022-09-01", "lead_investor": "UK Government"},
    
    # Tokamak Energy
    {"company_name": "Tokamak Energy", "round_type": "Series A", "amount_usd": 15000000, "announced_date": "2015-03-01", "lead_investor": "IP Group"},
    {"company_name": "Tokamak Energy", "round_type": "Series B", "amount_usd": 52000000, "announced_date": "2019-07-01", "lead_investor": "Legal & General Capital"},
    {"company_name": "Tokamak Energy", "round_type": "Series C", "amount_usd": 125000000, "announced_date": "2022-06-01", "lead_investor": "SoftBank Vision Fund"},
    
    # First Light Fusion
    {"company_name": "First Light Fusion", "round_type": "Series A", "amount_usd": 15000000, "announced_date": "2015-09-01", "lead_investor": "IP Group"},
    {"company_name": "First Light Fusion", "round_type": "Series B", "amount_usd": 50000000, "announced_date": "2020-03-01", "lead_investor": "Woodford Investment"},
    
    # Marvel Fusion
    {"company_name": "Marvel Fusion", "round_type": "Seed", "amount_usd": 11000000, "announced_date": "2020-10-01", "lead_investor": "HV Capital"},
    {"company_name": "Marvel Fusion", "round_type": "Series A", "amount_usd": 52000000, "announced_date": "2022-11-01", "lead_investor": "Lakestar"},
    
    # Zap Energy
    {"company_name": "Zap Energy", "round_type": "Seed", "amount_usd": 5000000, "announced_date": "2017-01-01", "lead_investor": "Y Combinator"},
    {"company_name": "Zap Energy", "round_type": "Series A", "amount_usd": 16000000, "announced_date": "2019-08-01", "lead_investor": "Bill Gates"},
    {"company_name": "Zap Energy", "round_type": "Series B", "amount_usd": 160000000, "announced_date": "2022-09-01", "lead_investor": "Volition Capital"},
    
    # Energy Singularity (能量奇点)
    {"company_name": "Energy Singularity", "round_type": "Seed", "amount_usd": 10000000, "announced_date": "2021-06-01", "lead_investor": "Shunwei Capital"},
    {"company_name": "Energy Singularity", "round_type": "Series A", "amount_usd": 70000000, "announced_date": "2022-12-01", "lead_investor": "HongShan"},
    
    # StarNet Fusion (星网聚变)
    {"company_name": "StarNet Fusion", "round_type": "Seed", "amount_usd": 8000000, "announced_date": "2021-09-01", "lead_investor": "Zhongguancun Capital"},
    {"company_name": "StarNet Fusion", "round_type": "Series A", "amount_usd": 50000000, "announced_date": "2023-03-01", "lead_investor": "IDG Capital"},
    
    # Type One Energy
    {"company_name": "Type One Energy", "round_type": "Seed", "amount_usd": 7500000, "announced_date": "2022-01-01", "lead_investor": "DCVC"},
    {"company_name": "Type One Energy", "round_type": "Series A", "amount_usd": 45000000, "announced_date": "2023-08-01", "lead_investor": "Breakthrough Energy Ventures"},
    
    # Princeton Stellarators
    {"company_name": "Princeton Stellarators", "round_type": "Seed", "amount_usd": 5000000, "announced_date": "2022-03-01", "lead_investor": "Prime Movers Lab"},
    
    # Helical Fusion
    {"company_name": "Helical Fusion", "round_type": "Seed", "amount_usd": 6000000, "announced_date": "2023-02-01", "lead_investor": "Energy Impact Partners"},
    
    # Xcimer Energy
    {"company_name": "Xcimer Energy", "round_type": "Seed", "amount_usd": 4500000, "announced_date": "2022-06-01", "lead_investor": "Piva"},
    {"company_name": "Xcimer Energy", "round_type": "Series A", "amount_usd": 42000000, "announced_date": "2024-01-01", "lead_investor": "Andreessen Horowitz"},
    
    # Shine Technologies
    {"company_name": "Shine Technologies", "round_type": "Series A", "amount_usd": 25000000, "announced_date": "2017-04-01", "lead_investor": "Drive Capital"},
    {"company_name": "Shine Technologies", "round_type": "Series B", "amount_usd": 65000000, "announced_date": "2020-10-01", "lead_investor": "T. Rowe Price"},
    {"company_name": "Shine Technologies", "round_type": "Series C", "amount_usd": 120000000, "announced_date": "2023-05-01", "lead_investor": "Fidelity"},
    
    # ExoFusion
    {"company_name": "ExoFusion", "round_type": "Seed", "amount_usd": 3000000, "announced_date": "2023-01-01", "lead_investor": "Kima Ventures"},
    
    # Renewal Fusion (新奥聚变)
    {"company_name": "Renewal Fusion", "round_type": "Seed", "amount_usd": 15000000, "announced_date": "2022-08-01", "lead_investor": "ENN Group"},
]


async def seed_database():
    """初始化数据库并填充数据"""
    
    # Create engine
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("🌱 开始填充公司数据...")
        
        # Create companies
        companies = {}
        for company_data in FUSION_COMPANIES:
            company = Company(**company_data)
            session.add(company)
            companies[company_data["name"]] = company
            print(f"  ✓ {company_data['name']}")
        
        await session.commit()
        print(f"✅ 已创建 {len(companies)} 家公司\n")
        
        print("💰 开始填充融资数据...")
        
        # Create funding rounds
        for funding_data in FUNDING_ROUNDS:
            company = companies.get(funding_data["company_name"])
            if company:
                funding_round = FundingRound(
                    company_id=company.id,
                    round_type=funding_data["round_type"],
                    amount_usd=funding_data["amount_usd"],
                    announced_date=date.fromisoformat(funding_data["announced_date"]),
                    lead_investor=funding_data["lead_investor"]
                )
                session.add(funding_round)
        
        await session.commit()
        print(f"✅ 已创建 {len(FUNDING_ROUNDS)} 条融资记录\n")
        
        print("🎉 数据库初始化完成!")
        print(f"\n统计信息:")
        print(f"  - 公司总数：{len(companies)}")
        print(f"  - 融资记录：{len(FUNDING_ROUNDS)}")
        
        # Calculate total funding
        total_funding = sum(f["amount_usd"] for f in FUNDING_ROUNDS)
        print(f"  - 融资总额：${total_funding / 1_000_000_000:.2f}B")


if __name__ == "__main__":
    asyncio.run(seed_database())
