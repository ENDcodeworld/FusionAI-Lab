"""
Pydantic Schemas
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date


# Company Schemas
class CompanyBase(BaseModel):
    name: str
    country: Optional[str] = None
    founded_year: Optional[int] = None
    technology_type: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    founded_year: Optional[int] = None
    technology_type: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Funding Round Schemas
class FundingRoundBase(BaseModel):
    round_type: str
    amount_usd: Optional[int] = None
    announced_date: Optional[date] = None
    lead_investor: Optional[str] = None
    investors: Optional[Dict[str, Any]] = None
    post_money_valuation: Optional[int] = None


class FundingRoundCreate(FundingRoundBase):
    company_id: int


class FundingRoundResponse(FundingRoundBase):
    id: int
    company_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Paper Schemas
class PaperBase(BaseModel):
    title: str
    abstract: Optional[str] = None
    authors: Optional[List[str]] = None
    journal: Optional[str] = None
    publish_date: Optional[date] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    citations: Optional[int] = 0
    pdf_url: Optional[str] = None


class PaperCreate(PaperBase):
    pass


class PaperResponse(PaperBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    role: Optional[str] = "user"


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    subscription_type: str
    subscription_expires: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Report Schemas
class ReportBase(BaseModel):
    title: str
    type: str
    price_cny: int
    published_date: Optional[date] = None


class ReportCreate(ReportBase):
    content_path: str


class ReportResponse(ReportBase):
    id: int
    author_id: Optional[int] = None
    download_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
