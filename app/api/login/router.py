from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.login.schema import NewUserRequest, LoginRequest
from app.api.login.service import CreateUserService, LoginService
from app.database.main.my_sql import get_db

login_router = APIRouter(prefix="/user", tags=["Login"])

@login_router.post("/create_user")
async def create_user(user_data: NewUserRequest, db=Depends(get_db)):
    """ Endpoint to create a new user. """
    return await  CreateUserService(db).create_user(user_data)

@login_router.post("/login")
async def login_user(credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)):
    """ Endpoint to authenticate a user and return a JWT token. """
    return await LoginService(db).login_user(credentials)
