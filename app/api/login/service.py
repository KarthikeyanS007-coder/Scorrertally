from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from jose import jwk
from sqlalchemy.orm import Session

from app.api.login.schema import LoginRequest, LoginResponse, NewUserRequest, NewUserResponse
from app.config import settings
from app.message.message import Messages
from app.models.main.user import TblUser, CreateUserBase
from app.dependency.authentication import JWTpayloadSchema, JWTTokenManager
from app.dependency.security import hash_password, verify_password
from app.utlis.schema_utils import CustomResponse

class CreateUserService:
    
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, user_data: NewUserRequest) -> CustomResponse:
        """Create a new user."""
        # Check if the username, email, or mobile number already exists
        existing_user = self.db.query(TblUser).filter(
            (TblUser.username == user_data.username) |
            (TblUser.email == user_data.email) |
            (TblUser.mobile_number == user_data.mobile_number)
        ).first()
        
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Messages.USER_ALREADY_EXISTS)
        
        if user_data.password != user_data.confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Messages.PASSWORD_MISMATCH)
        
        # Hash the password
        
        password_hash = hash_password(user_data.password)
        
        new_user = CreateUserBase.model_validate(user_data.model_dump(exclude={"confirm_password"}))
        new_user.password = password_hash
            
        # Create a new user
        new_user = TblUser.create_user(self.db, new_user)
        
        return CustomResponse(
            status = "1",
            message=Messages.USER_CREATED, 
            data=new_user
            )
    
class LoginService:
    
    def __init__(self, db: Session):
        self.db = db

    async def login_user(self, credentials: OAuth2PasswordRequestForm) -> CustomResponse:
        """Authenticate a user and return a JWT token."""

        user = TblUser.get_user_by_email(self.db, credentials.username) 
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Messages.USER_NOT_FOUND)
        
        if not user or not verify_password(credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=Messages.INVALID_CREDENTIALS)
        
        token_payload = JWTpayloadSchema(
            email=user.email,
            roles=user.roles,
            expire=datetime.utcnow() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRATION_MINUTES)  # This will be set in the token creation method
        )
        # Generate JWT token
        token = JWTTokenManager.create_token(token_payload)
        
        return CustomResponse(
            status="1",
            message=Messages.LOGIN_SUCCESSFUL,
            data=LoginResponse(
                token=token,
                token_type="bearer",
                email=user.email,
                roles=user.roles.value
            )
        )
        
    
    
    
    
    

    