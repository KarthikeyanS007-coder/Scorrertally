import enum
from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

class CustomBaseModel(BaseModel):
    """Base model for all Pydantic models."""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        coerce_numbers_to_str=True,
    )
    
DataT = TypeVar("DataT")

class CustomResponse(CustomBaseModel, Generic[DataT]):
    """Custom response model for API responses."""
    status: str = Field(..., examples=["1", "-1"])
    message: str = Field(..., examples=["Message", "User already exists"])
    data: DataT | None = Field(None, examples=[{"key": "value"}, None])

class UserRoles(str, enum.Enum):
    PLAYER = "player"
    CAPTAIN = "Captain"
    PRO = "pro"
    SUPER_ADMIN = "super_admin"