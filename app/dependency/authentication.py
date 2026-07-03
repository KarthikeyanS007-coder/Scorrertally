from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from app.config import settings
 
def create_token(username: str):
    # Implement your token creation logic here
    token_expiration = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES)
    payload = {"username": username, "exp": token_expiration}
    
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str):
    # Implement your token verification logic here
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload["username"]
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )