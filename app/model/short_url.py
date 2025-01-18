from .main import BaseSQL, GetOr404Mixin, UniqueSlugMixin

from sqlalchemy import Column, Enum, LargeBinary, String, Text, Integer, DateTime, Boolean
from datetime import datetime, timedelta
from app.schema.url import ShortenRequest, ShortenResponse
from app.util import generate_short_key, hash_password,verify_password
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from .acess_log import AccessLog

class ShortUrl(BaseSQL, GetOr404Mixin, UniqueSlugMixin):
    __tablename__ = "short_url"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False, index=True)
    short_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    password_protected = Column(Boolean, default=False)
    password_hash = Column(String, nullable=True)

    @classmethod
    def create(cls, payload: ShortenRequest):
        short_key = generate_short_key(payload.url)
        existing_entry = cls.filter(short_key=short_key)
        if existing_entry:
            existing_entry = existing_entry[0]
            if existing_entry.original_url == payload.url:
                return ShortenResponse(
                    original_url=existing_entry.original_url,
                    short_url=existing_entry.short_key,  
                    expires_at=existing_entry.expires_at,
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Hash collision occurred. Try increasing key length."
                )

        expires_at = datetime.utcnow() + timedelta(hours=payload.expiry_hours or 24)

        new_short_url = super().create(
            original_url=payload.url,
            short_key=short_key,
            expires_at=expires_at,
            password_protected=bool(payload.password),
            password_hash=hash_password(payload.password.strip()) if payload.password else None,
        )
        response_data = ShortenResponse(
            original_url=new_short_url.original_url,
            short_url=new_short_url.short_key,
            expires_at=new_short_url.expires_at,
        )
        return response_data
    
    @classmethod
    def validate_redirect(cls, url:str, ip_address:str):
        url = url.split("?")
        password = None
        if len(url) == 2:
            password = url[1]
        print(password)
        url = url[0]

        short_url_entry = cls.filter(short_key=url)
        if not short_url_entry:
            raise HTTPException(status_code=404, detail="URL not found.")
        
        short_url_entry=short_url_entry[0]
        if short_url_entry.expires_at < datetime.utcnow():
            raise HTTPException(status_code=404, detail="URL has expired.")

        if short_url_entry.password_protected:
            if password is None or not verify_password(password, short_url_entry.password_hash):
                raise HTTPException(status_code=403, detail="Invalid Password.") 
        
        AccessLog.create(
            short_url_id=short_url_entry.id,
            ip_address=ip_address,
        )
        return RedirectResponse(short_url_entry.original_url)