import enum

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import VARCHAR, Boolean, Column, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from app.models.base import Base
from app.utlis.schema_utils import UserRoles, CustomBaseModel

class CreateUserBase(CustomBaseModel):
    username: str
    password: str
    name: str
    age: int
    email: EmailStr
    mobile_number: str
    
class TblUser(Base):
    __tablename__ = "tbl_user"
    
    id: Mapped[int] = mapped_column("user_id",Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column("username",VARCHAR(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column("password",VARCHAR(255), nullable=False)
    name: Mapped[str] = mapped_column("name",VARCHAR(255), nullable=False)
    age: Mapped[int] = mapped_column("age",Integer, nullable=False)
    email: Mapped[str] = mapped_column("email",VARCHAR(255), unique=True, nullable=False)
    mobile_number: Mapped[str] = mapped_column("mobile_number",VARCHAR(255), unique=True, nullable=False)
    roles: Mapped[UserRoles] = mapped_column("roles",Enum(UserRoles), nullable=False, default=UserRoles.PLAYER)
    mobile_otp: Mapped[int] = mapped_column("mobile_otp",Integer, nullable=True)
    email_otp: Mapped[int] = mapped_column("email_otp",Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column("is_active",Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column("is_deleted",Boolean, default=False)
    
    @classmethod
    def create_user(cls, db: Session, user_data: CreateUserBase) -> "TblUser":
        new_user = cls(**user_data.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @classmethod
    def get_user_by_email(cls, db: Session, email: str):
        return db.query(cls).filter(cls.email == email).first()
    
    @classmethod
    def get_user_by_mobile_number(cls, db: Session, mobile_number: str):
        return db.query(cls).filter(cls.mobile_number == mobile_number).first()