from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from app.config import settings
from app.models.main.user import TblUser
from app.database.main.my_sql import get_db
from app.utlis.schema_utils import UserRoles


def _serialize_datetime(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


def _deserialize_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)
 
user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="FASTAPI/user/login")

class JWTpayloadSchema(BaseModel):
    
    email: str | None = Field(default=None)
    mobile_number: str | None = Field(default=None)
    roles: UserRoles
    expire: datetime | None = Field(default=None)
    
class JWTTokenManager:
    
    @staticmethod
    def create_token(data: JWTpayloadSchema) -> str:
        token_expiration = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES)
        data.expire = token_expiration
        payload = data.model_dump(exclude_none=True)
        payload["expire"] = _serialize_datetime(payload["expire"])
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> JWTpayloadSchema:
        # Implement your token verification logic here
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            
            required_fields = {"email", "mobile_number", "roles", "expire"}
            if not required_fields.issubset(payload.keys()):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

            expire_value = _deserialize_datetime(payload.get("expire"))
            if expire_value is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

            if datetime.utcnow() > expire_value:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

            payload["expire"] = expire_value
            return JWTpayloadSchema(**payload)
        
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or tampered token")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Token verification failed: {str(e)}")
        
def get_current_user(token: str = Depends(user_oauth2_scheme), db=Depends(get_db)) -> TblUser:
    """ Retrieve the current authenticated user based on the provided token."""
    
    jwt_payload = JWTTokenManager.verify_token(token)
    
    user = db.query(TblUser).filter(TblUser.email == jwt_payload.email or TblUser.mobile_number == jwt_payload.mobile_number).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user