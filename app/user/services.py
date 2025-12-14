from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_google_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        google_id=user.google_id,
        full_name=user.full_name,
        picture=user.picture
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
