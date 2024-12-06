from __future__ import annotations

from typing import List, NoReturn

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from fastapi_sqlalchemy import db

from model.base import Base

class RecordEntry(Base):
    _tablename_ = "record_entry"

    entry_id = Column(Integer, ForeignKey("entry.id", ondelete="CASCADE"))
    record_id = Column(Integer, ForeignKey("record.id", ondelete="CASCADE"))

    def __init__(self, entry_id: int = -1, record_id: int = -1):
        self.entry_id = entry_id
        self.record_id = record_id

    def insert(self) -> NoReturn:
        """
        Insert role permissions

        :return:
        """
        with db():
            db.session.add(self)
            db.session.commit()
