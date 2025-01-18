# app/main.py

from fastapi import FastAPI, Request, Depends, HTTPException, status

from datetime import datetime, timedelta
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware


from app.router.url import router as url_router
from app.database import db_instance

app = FastAPI(title="URL Shortener with Expiry and Analytics")
db_instance.base.metadata.create_all(bind=db_instance._engine)

app.add_middleware(CORSMiddleware)

@app.get("/surl/health")
def health():
    return {"status": "ok"}

app.include_router(url_router, prefix="/surl")
