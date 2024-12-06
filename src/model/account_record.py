from __future__ import annotations

from typing import List, NoReturn

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from fastapi_sqlalchemy import db

from model.base import Base

class AccountRecord(Base):
    __tablename__ = "account_record"

    account_id = Column(Integer, ForeignKey("account.id", ondelete="CASCADE"))
    record_id = Column(Integer, ForeignKey("record.id", ondelete="CASCADE"))

    def __init__(self, account_id: int = -1, record_id: int = -1):

        self.account_id = account_id
        self.record_id = record_id

    def insert(self) -> NoReturn:
        """
        Insert role permissions

        :return:
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_record_by_account_and_record(cls, account_id,record_id,):
        with db():
            row = db.session.query(cls).filter_by(account_id=account_id,record_id=record_id).first()
            if row:
                return row.record
            else:
                return None