
from typing import Callable
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


from app.model.short_url import ShortUrl
from app.model.acess_log import AccessLog
from app.schema.url import ShortenRequest, ShortenResponse, AnalyticsResponse, AccessLogEntry
from app.util import generate_short_key, hash_password, verify_password
from app.database import db_session_wrapper

router = APIRouter(
    tags=["URL"],
)

@db_session_wrapper
@router.post("/shorten", response_model=ShortenResponse)
def shorten_url(payload: ShortenRequest):
    return ShortUrl.create(payload)

@db_session_wrapper
@router.get("/shorten/{short_key}")
def redirect_short_url(
    short_key: str, request:Request
):
    return ShortUrl.validate_redirect(short_key, request.client.host)

@db_session_wrapper
@router.get("/analytics/{short_key}", response_model=AnalyticsResponse)
def get_analytics(
    short_key: str,
):
    short_url_entry = ShortUrl.get_or_404(short_key=short_key)
    logs = AccessLog.filter(short_url_id=short_url_entry.id)
    return AnalyticsResponse(
        short_url=short_url_entry.short_key,
        access_count=len(logs),
        logs=[AccessLogEntry(access_time=log.created_at, ip_address=log.ip_address) for log in logs]

    )