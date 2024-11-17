from fastapi_sqlalchemy import db
from sqlalchemy import Column, String, Boolean
from sqlalchemy import String, Boolean, Integer, JSON
from sqlalchemy.sql.schema import Column, ForeignKey
from .base import Base
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = "account"

    username = Column(String, index=True, nullable=False, unique=True)
    status = Column(Boolean, default=True)
    email = Column(String, nullable=False,unique=True)
    password = Column(String, nullable=False)
    records = relationship("AccountRecord", backref="account")


    @classmethod
    def get_by_username(cls, username: str):
        row = db.session.query(cls).filter_by(username=username).first()
        return row

    @classmethod
    def sign_in(cls, username: str,password: str):
        row = db.session.query(cls).filter_by(username=username,password=password).first()
        return row

    @classmethod
    def get_by_email(cls, email: str):
        row = db.session.query(cls).filter_by(email=email).first()
        return row

