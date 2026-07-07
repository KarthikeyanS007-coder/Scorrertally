
from pydantic import BaseModel, EmailStr, Field
from app.utlis.schema_utils import CustomBaseModel


class LoginRequest(BaseModel):
    email: str
    password: str
    
class NewUserResponse(CustomBaseModel):
    username: str
    name: str
    age: int
    email: EmailStr
    mobile_number: str
    
class NewUserRequest(CustomBaseModel):
    username: str
    password: str
    confirm_password: str
    name: str
    age: int
    email: EmailStr
    mobile_number: str
    
    
class LoginResponse(CustomBaseModel):
    token: str 
    token_type: str
    email: str
    roles: str
    