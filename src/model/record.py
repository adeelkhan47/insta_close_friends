from __future__ import annotations

from typing import List
from fastapi_sqlalchemy import db
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String,Integer
from model import Base


class Record(Base):
    _tablename_ = "record"

    username = Column(String(20), nullable=True)
    status = Column(String(200), nullable=True)
    followers = Column(Integer, nullable=True)
    account = relationship("AccountRecord", backref="record")
    record_entries = relationship("RecordEntry", backref="record")

    @classmethod
    def get_by_username(cls, username: str):
        with db():
            row = db.session.query(cls).filter_by(username=username).first()
            return row


