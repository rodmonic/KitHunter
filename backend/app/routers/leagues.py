from fastapi import APIRouter, Depends
# from .auth import create_access_token
from ..models import League
from ..database import get_session
from sqlmodel import select

router = APIRouter()


@router.get("/leagues/{league_id}", response_model=League)
def read_league(league_id: str, session=Depends(get_session)):
    statement = select(League).where(League.id == league_id)
    result = session.exec(statement).first()  # Use .first() to return only one record, if exists
    return result

