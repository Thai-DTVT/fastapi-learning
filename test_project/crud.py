from sqlalchemy.orm import Session

from . import models, schemas
#from fastapi import  HTTPException
#import getpass
#from typing import List
#Get user
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

#Get user with offset
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

#Create user
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password 
    db_user = models.User(email=user.email,hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
#Delete user
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return schemas.UserDelete(id=user_id)

#Change password with confirm old password
    
def change_password(db: Session, user_id: int, user_change: schemas.UserChange,old_password: str, new_password: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    if user.hashed_password != old_password :
        return {"error": "Old password is incorrect"}

    user.hashed_password == new_password 
    db.commit()
    return {"message": "Password changed successfully"}

#Create exception no use rase HTTPException

class Error(Exception):
    """Base class for other exceptions"""
    pass
class ValueTooLargeError(Error):
    """Raised when the input value is too large"""
    pass
class ValueTooSmallError(Error):
    """Raised when the input value is too small"""
    pass
#Math fibonacci  chính      
def fibonacci_sequence(n: int) -> schemas.FibonacciResponse:
    if n <= 0:
        raise ValueTooSmallError
    elif n == 1:
        return schemas.FibonacciResponse(result=[0]) 
    elif n == 2:
        return schemas.FibonacciResponse(result=[0]) 
    elif n > 500:
        raise ValueTooLargeError
    else:
        sequence = [0, 1]
        for _ in range(2, n):
            next_fib = sequence[-1] + sequence[-2]
            sequence.append(next_fib)
        return schemas.FibonacciResponse(result=sequence)
#Math fibonacci  thử
# def fibonacci_sequence(n: int) -> schemas.FibonacciResponse:
    
#     if n == 1:
#         return schemas.FibonacciResponse(result=[0]) 
#     elif n == 2:
#         return schemas.FibonacciResponse(result=[0]) 
#     else:
#         sequence = [0, 1]
#         for _ in range(2, n):
#             next_fib = sequence[-1] + sequence[-2]
#             sequence.append(next_fib)
#         return schemas.FibonacciResponse(result=sequence)