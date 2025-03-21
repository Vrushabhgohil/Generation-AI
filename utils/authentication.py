import jwt
import uuid
import bcrypt
import datetime
from models.authentication import User
from sqlalchemy.orm import Session
from datetime import timedelta
from config import SECRET_KEY,ALGORITHM

class Authentication:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, email: str, password: str):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

        new_user = User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            password=hashed_password,
            google_id=None,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
            is_activate=True,
            is_deleted=False,
            is_verified=False
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def authenticate_user(self, email, password):
        user = self.db.query(User).filter(User.email == email).first()
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            return user
        return None
    
    def create_access_token(self, data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})  # Expiry timestamp

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def get_user(self,user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        return user
    
    def delete_user(self,user_id): 
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_deleted = True
            self.db.commit()
            return True
        return False