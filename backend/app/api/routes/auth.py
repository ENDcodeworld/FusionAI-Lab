"""
Authentication API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    用户登录
    
    返回 JWT access token
    """
    # TODO: Implement authentication
    return {
        "access_token": "fake-token",
        "token_type": "bearer"
    }


@router.post("/register")
async def register(
    email: str,
    password: str
):
    """
    用户注册
    """
    # TODO: Implement registration
    return {"message": "User registered successfully"}
