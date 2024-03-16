from sqlalchemy.orm import Session

from . import models, schemas
from fastapi import FastAPI, HTTPException

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password 
    db_user = models.User(email=user.email,hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return schemas.UserDelete(id=user_id)


    
def change_password(db: Session, user_id: int, user_change: schemas.UserChange,old_password: str, new_password: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    if user.hashed_password != old_password :
        return {"error": "Old password is incorrect"}

    user.hashed_password = new_password 
    db.commit()
    return {"message": "Password changed successfully"}

def fibonacci_sequence(n: int) -> schemas.FibonacciResponse:
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    elif n > 500:
        raise HTTPException(status_code=400, detail="Max =500. Vui lòng nhập lại")
    else:
        sequence = [0, 1]
        for _ in range(2, n):
            next_fib = sequence[-1] + sequence[-2]
            sequence.append(next_fib)
        return sequence