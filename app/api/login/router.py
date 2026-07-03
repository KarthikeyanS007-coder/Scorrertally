from datetime import datetime, timedelta
from app.dependency.authentication import create_token, verify_token
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.login.schema import LoginRequest
from app.api.login.service import LoginService

login_router = APIRouter()

@login_router.post("/login")
async def login (LoginRequest: LoginRequest ):
    # Implement your login logic here
    return await LoginService().login(LoginRequest)
    

@login_router.get("/secure-data")
async def get_secure_data(token: str):
    return await LoginService().get_secure_data(token)