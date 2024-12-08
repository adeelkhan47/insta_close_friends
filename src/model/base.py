from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Tuple, Union

from fastapi_sqlalchemy import db
from sqlalchemy import Column, DateTime, Integer, asc, desc
from sqlalchemy.exc import StatementError
from sqlalchemy.ext.declarative import as_declarative, declared_attr


class InvalidFieldError(Exception):
    pass


@as_declarative()
class Base(object):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True,
    )

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate __tablename__ automatically

        Returns:
            Table name
        """
        return cls.__name__.lower()

    def insert(self) -> Base:
        """
        Insert

        Returns:
            Base
        """
        # with db():
        with db():
            db.session.add(self)
            db.session.commit()
            return self

    def delete(self) -> Base:
        """
        Delete

        Returns:
            Base
        """
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def delete_all(cls) -> None:
        """
        Delete all rows from the table

        """
        with db():
            db.session.query(cls).delete()
            db.session.commit()

    @classmethod
    def update(cls, id: int, to_update: dict) -> None:
        """
        Update row by id

        Args:
            id: id to update data
            to_update: dictionary to update data
            session: Defaults to None.
        """
        with db():
            db.session.query(cls).filter(cls.id == id).update(to_update)
            db.session.commit()

    @classmethod
    def get_by_idb(cls, id: int) -> Union[Base, None]:
        """
        Get by id

        Args:
            id: fetch row by id
            session: Defaults to None.

        Returns:
            Row from database
        """
        row = (
            db.session.query(cls).filter_by(id=id).first()
        )
        return row
    @classmethod
    def get_by_id_with_db(cls, id: int) -> Union[Base, None]:
        """
        Get by id

        Args:
            id: fetch row by id
            session: Defaults to None.

        Returns:
            Row from database
        """
        with db():
            row = (
                db.session.query(cls).filter_by(id=id).first()
            )
            return row

    @classmethod
    def get_by_username(cls, username: str) -> Union[Base, None]:
        """
        Get by id

        Args:
            id: fetch row by id
            session: Defaults to None.

        Returns:
            Row from database
        """

        row = (
            db.session.query(cls).filter_by(username=username).first()
        )
        return row

    @classmethod
    def list(cls) -> Union[Base, None]:
        """
        List all rows

        Args:
            session: Defaults to None.

        Returns:
            All rows
        """

        rows = db.session.query(cls).all()
        return rows

    @classmethod
    def count_all(cls) -> int:
        """
        Count all rows in the table

        Returns:
            Count of rows
        """
        count = db.session.query(cls).count()
        return count

    @classmethod
    def filter_and_order(cls, args: Dict,query=None) -> Tuple[List, int]:
        """
        Get list of rows queried from database as per the arguments passed in request
        Args:
            args: Dict containing the query args passed in request
        Returns:
            List of objects of the class on which the function is called
            and an Int representing the length of the list
        """
        if query is None:
            query = db.session.query(cls)
        def apply_filter(query, filter_by, operator, value):
            filter_field = getattr(cls, filter_by, None)
            if filter_field is None:
                raise InvalidFieldError(f"Invalid field: {filter_by}")

            if "like" in operator:
                query = query.filter(filter_field.ilike(f"%{value}%"))
            elif "gte" in operator:
                query = query.filter(filter_field >= value)
            elif "lte" in operator:
                query = query.filter(filter_field <= value)
            elif "gt" in operator:
                query = query.filter(filter_field > value)
            elif "lt" in operator:
                query = query.filter(filter_field < value)
            elif "eq" in operator:
                query = query.filter(filter_field.in_(value.split(",")))
            else:
                try:
                    query = query.filter(getattr(filter_field, operator)(value))
                except StatementError:
                    raise ValueError(f"Invalid value {value} for field {filter_by}")
                except AttributeError:
                    raise ValueError(
                        f"Invalid operator {operator} for field {filter_by}"
                    )

            return query


        # apply filters
        for field, value in args.items():
            if ":" in field:
                filter_by, operator = field.split(":")
                query = apply_filter(query, filter_by, operator, value)

        # apply ordering
        order_by = args.get("order_by", "updated_at:desc")
        for ordering in reversed(order_by.split(",")):
            field, order = ordering.split(":")
            order_field = getattr(cls, field, None)
            if order_field is None:
                raise InvalidFieldError(f"Invalid order field: {field}")
            query = query.order_by(
                desc(order_field) if order == "desc" else asc(order_field)
            )

        # count total rows
        total_rows = query.count()

        # apply pagination
        start = int(args.get("start", 1))
        limit = int(args.get("limit", 10))
        query = query.offset((start - 1) * limit).limit(limit)

        all_rows = query.all()

        return all_rows, total_rows