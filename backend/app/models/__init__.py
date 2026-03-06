"""
Database Models
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, JSON, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Company(Base):
    """公司表"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    country = Column(String(100))
    founded_year = Column(Integer)
    technology_type = Column(String(100), index=True)
    website = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    funding_rounds = relationship("FundingRound", back_populates="company", cascade="all, delete-orphan")


class FundingRound(Base):
    """融资轮次表"""
    __tablename__ = "funding_rounds"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    round_type = Column(String(50))  # Seed, A, B, C, etc.
    amount_usd = Column(BigInteger)
    announced_date = Column(Date, index=True)
    lead_investor = Column(String(255))
    investors = Column(JSON)
    post_money_valuation = Column(BigInteger)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="funding_rounds")


class Paper(Base):
    """论文表"""
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(1000), nullable=False)
    abstract = Column(Text)
    authors = Column(JSON)
    journal = Column(String(255))
    publish_date = Column(Date, index=True)
    doi = Column(String(100), unique=True)
    arxiv_id = Column(String(50))
    citations = Column(Integer, default=0, index=True)
    pdf_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ExperimentData(Base):
    """实验数据表"""
    __tablename__ = "experiment_data"
    
    id = Column(Integer, primary_key=True, index=True)
    facility = Column(String(100), index=True)  # ITER, JET, EAST, etc.
    experiment_id = Column(String(100))
    shot_number = Column(Integer)
    timestamp = Column(DateTime(timezone=True), index=True)
    parameters = Column(JSON)  # 等离子体参数
    results = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255))
    role = Column(String(50), default="user")  # user, premium, admin
    subscription_type = Column(String(50), default="free")  # free, basic, premium
    subscription_expires = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Report(Base):
    """报告表"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    type = Column(String(100))  # annual, quarterly, company_analysis
    price_cny = Column(Integer)
    content_path = Column(String(500))
    published_date = Column(Date)
    author_id = Column(Integer, ForeignKey("users.id"))
    download_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
