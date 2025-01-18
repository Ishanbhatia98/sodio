# app/schemas.py

from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class ShortenRequest(BaseModel):
    url: HttpUrl
    expiry_hours: Optional[int] = 24
    password: Optional[str] = None  # if user wants a protected URL

class ShortenResponse(BaseModel):
    original_url: str
    short_url: str
    expires_at: datetime

class AccessLogEntry(BaseModel):
    access_time: datetime
    ip_address: str

class AnalyticsResponse(BaseModel):
    short_url: str
    access_count: int
    logs: List[AccessLogEntry]