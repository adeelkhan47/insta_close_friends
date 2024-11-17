from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import settings

engine = create_engine(settings.database_uri)


def get_session():
    global engine
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
