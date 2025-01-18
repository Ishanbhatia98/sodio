"""Models for the database"""
from contextlib import contextmanager
from functools import wraps
from io import BytesIO
from typing import List, Optional
from uuid import uuid4

from fastapi import HTTPException, status
from pydantic import BaseModel, validator
from sqlalchemy import Column, Enum, LargeBinary, String, Text
from sqlalchemy import text as sqlalchemy_text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.ext.declarative import declared_attr
from typeguard import typechecked
from fastapi import HTTPException, status
from typeguard import typechecked
from app.database import db_instance, get_db_session

Base = db_instance.base


def string_uuid():
    return str(uuid4())


@typechecked
class BaseSQL(Base):
    __abstract__ = True
    _db_session = None

    @staticmethod
    def session():
        return get_db_session()

    @classmethod
    def empty_table(cls):
        with cls.session() as session:
            session.query(cls).delete()
            session.commit()

    @classmethod
    def create(cls, *args, **kwargs):
        session = cls.session()
        try:
            obj = cls(*args, **kwargs)
            session.add(obj)
            session.commit()
            return obj
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def get(cls, id: str):
        session = cls.session()
        try:
            return session.query(cls).filter(cls.id == id).first()
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def edit(cls, id: str, **kwargs):
        session = cls.session()
        try:
            session.query(cls).filter(cls.id == id).update(kwargs)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def delete(cls, id: str):
        session = cls.session()
        try:
            session.query(cls).filter(cls.id == id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def filter(cls, **kwargs):
        session = cls.session()
        try:
            return session.query(cls).filter_by(**kwargs).all()
        except Exception as e:
            session.rollback()
            raise e

@typechecked
class GetOr404Mixin:
    @classmethod
    def get_or_404(cls, **kwargs):
        result = cls.filter(**kwargs)
        if result is None:
            raise HTTPException(
                detail=f"{cls.__name__} with {kwargs} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return result[0]

    @classmethod
    def get_or_none(cls, **kwargs):
        return cls.filter(**kwargs)


@typechecked
class UniqueSlugMixin:
    @classmethod
    def unique_slug(cls, field: str, value: str, i=0):
        possible_value = value if i == 0 else f"{value}-{i}"
        if cls.filter(**{field: possible_value}):
            return cls.unique_slug(field, value, i + 1)
        return value


if __name__ == "__main__":
    from app.database import db_instance
    