from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.orm import as_declarative

MYSQL_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = MetaData(naming_convention=MYSQL_INDEXES_NAMING_CONVENTION)

class_registry : dict[str, Any] ={}

@as_declarative(class_registry=class_registry)
class Base:
    
    """Base class for all models."""
    record_id: Any
    class_name: str
    __abstract__: bool = True
    metadata = metadata
    
