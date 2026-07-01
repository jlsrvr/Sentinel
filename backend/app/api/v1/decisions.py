from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.case import Case
from app.core.database import get_db
from app.schemas.decision import DecisionCreateRequest