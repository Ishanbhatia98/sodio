from sqlalchemy.orm import declarative_base, relationship
from .main import BaseSQL, GetOr404Mixin, UniqueSlugMixin

from sqlalchemy import Column, Enum, LargeBinary, String, Text, Integer, DateTime, Boolean, ForeignKey
from datetime import datetime, timedelta
from app.schema.url import ShortenRequest, ShortenResponse
from app.util import generate_short_key, hash_password
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse

class AccessLog(BaseSQL, GetOr404Mixin, UniqueSlugMixin):
    __tablename__ = "access_log"

    id = Column(Integer, primary_key=True, index=True)
    short_url_id = Column(Integer, ForeignKey("short_url.id"))
    access_time = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)


    @classmethod
    def create(cls, *args, **kwargs):
        kwargs["created_at"] = datetime.utcnow()
        return super().create(*args, **kwargs)
