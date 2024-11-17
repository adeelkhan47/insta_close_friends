from __future__ import annotations

from typing import List
from fastapi_sqlalchemy import db
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String,Integer
from model import Base


class Entry(Base):
    _tablename_ = "entry"

    follower = Column(String(50), nullable=True)
    status = Column(String(200), nullable=True)
    # success_count = Column(Integer, nullable=True)
    # failed_count = Column(Integer, nullable=True)
    record_entries = relationship("RecordEntry", backref="entry")


