from fastapi import APIRouter, Depends
# from .auth import create_access_token
from ..models import User
from ..database import get_session

router = APIRouter()


@router.post("/register/")
def register(username: str, password: str, session=Depends(get_session)):
    # Logic to register user and store hashed password
    pass


# @router.post("/login/")
# def login(username: str, password: str, session=Depends(get_session)):
#     # Logic for login and token generation
#     token = create_access_token({"sub": username})
#     return {"access_token": token, "token_type": "bearer"}


