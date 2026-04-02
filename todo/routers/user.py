from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from ..models import Todos, Users
from ..database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerificarion(BaseModel):
    password: str = Field(min_length=1, max_length=100)
    new_password: str = Field(min_length=1, max_length=100)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_request: UserVerificarion):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt_context.verify(user_request.password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    user_model.hashed_password = bcrypt_context.hash(user_request.new_password)
    db.add(user_model)
    db.commit()
    
    
@router.put("/phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str = Path(..., min_length=1, max_length=20)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
