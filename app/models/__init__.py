from app.models.base import Base
from app.database.main.my_sql import _engine
from app.models.main.user import TblUser

Base.metadata.create_all(bind=_engine)