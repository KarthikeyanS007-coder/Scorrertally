from collections.abc import Generator
from contextlib import contextmanager
from urllib.parse import quote_plus

from pymysql import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings, Settings
from app.log import get_logger

logger = get_logger(__name__)

def build_mysql_connection_string(settings: Settings) -> str:
    """
    Build the MySQL connection string.

    Parameters
    ----------
        settings (Settings): The application settings containing database configuration.

    Returns
    -------
        str: The MySQL connection string.
    """
    
    DB_HOST = settings.MYSQL_HOST
    DB_PORT = settings.MYSQL_PORT
    DB_USER = settings.MYSQL_USER
    DB_PASSWORD = settings.MYSQL_PASSWORD
    DB_NAME = settings.MYSQL_DATABASE
    encoded_password = quote_plus(DB_PASSWORD)
    if not DB_PASSWORD:
        database_url = f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        database_url = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    return database_url

sqlalchemy_database_url = build_mysql_connection_string(settings)
print(f"SQLAlchemy Database URL: {sqlalchemy_database_url}")

_engine = create_engine(sqlalchemy_database_url, future=True, pool_recycle=3600 )
_session_local = sessionmaker(bind=_engine, autoflush=False, autocommit=False)

def get_db() -> Generator[Session, None, None]:
    """
    Get a database session.

    Yields
    ------
        Generator[Session, None, None]: A generator yielding a SQLAlchemy Session.
    """
    db: Session = _session_local()
    try:
        yield db
        db.commit()
    except OperationalError as e:
        db.rollback()
        error_message = f"Database operational error occurred while getting the database session. Error: {e!s}"
        logger.exception(error_message)
        raise
    except Exception as e:
        db.rollback()
        error_message = f"An error occurred while getting the database session. Error: {e!s}"
        logger.exception(error_message)
        raise
    finally:
        db.close()
      

@contextmanager  
def get_ctx_db() -> Generator[Session, None, None]:
    """
    Get a database session for context management.

    Yields
    ------
        Generator[Session, None, None]: A generator yielding a SQLAlchemy Session.
    """
    db: Session = _session_local()
    try:
        yield db
        db.commit()
    except OperationalError as e:
        db.rollback()
        error_message = f"Operational error occurred while getting the database session. Error: {e!s}"
        logger.exception(error_message)
        raise
    except Exception as e:
        db.rollback()
        error_message = f"An unexpected error occurred while getting the database session. Error: {e!s}"
        logger.exception(error_message)
        raise
    finally:
        db.close()
