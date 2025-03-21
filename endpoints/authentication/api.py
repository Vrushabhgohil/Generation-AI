from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.authentication import User
from utils.authentication import Authentication
from database.database import get_db

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/signup")
async def signup(username: str, email: str, password: str, db: Session = Depends(get_db)):
    auth = Authentication(db)
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = auth.create_user(username, email, password)
    return {"message": f"User {username} created successfully!"}


@auth_router.post("/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    auth = Authentication(db)
    user = auth.authenticate_user(email, password)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=30)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "User": user}


@auth_router.post("/get_data_id")
def get_user_by_id(user_id:str, db: Session = Depends(get_db)):
    auth = Authentication(db)
    user_id = user_id
    user = auth.get_user(user_id)
    return {"User": user}

@auth_router.delete("/delete_account")
def delete_account(user_id:str,db:Session=Depends(get_db)):
    auth = Authentication(db)
    user_id = user_id
    user = auth.delete_user(user_id)
    return {"message": "User  deleted successfully!"}

@auth_router.get("/")
def get_data():
    return {"message": "Authentication Endpoint"}
