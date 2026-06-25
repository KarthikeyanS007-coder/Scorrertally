from fastapi import HTTPException, status

from app.api.login.schema import LoginRequest
from app.dependency.authentication import create_token, verify_token


class LoginService:
    
    async def login(self, login_request: LoginRequest):
        if login_request.username == "admin" and login_request.password == "1234":
            token = create_token(login_request.username)
            return {"message": "Login successful", "token": token}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    async def get_secure_data(self, token: str):
        uname = verify_token(token)
        return {"message": f"Secure data for user {uname}"}
    
        
    