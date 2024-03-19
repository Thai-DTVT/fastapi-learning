from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
#from pydantic import conint

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#try method post user with ui
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

#try method get user with ui(offset id)
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
#try method get user with ui(id)
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#try method delete user with ui(id)

@app.delete("/users/{user_id}/", response_model=schemas.UserDelete)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user

#try method put change password with ui

@app.put("/users/{user_id}/change-password/")
def change_password(user_id: int, user_change: schemas.UserChange, old_password: str, new_password: str, db: Session = Depends(get_db)):
    result = crud.change_password(db, user_id, user_change, old_password, new_password)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {"message": "Password changed successfully"}

#try method get match fibonacci with ui
@app.get("/fibonacci/{n}", response_model=schemas.FibonacciResponse)
async def get_fibonacci(n: int):
    # try:
    #     sequence = crud.fibonacci_sequence(n)
    #     return sequence
    # except crud.ValueTooLargeError as e:
    #     raise HTTPException(status_code=400, detail=e)
    try:
        sequence = crud.fibonacci_sequence(n)
        return sequence
    except crud.ValueTooSmallError:
        raise HTTPException(status_code=400, detail="Số nhập vào quá nhỏ. Vui long nhập số lớn hơn 0.")
    except crud.ValueTooLargeError:
        raise HTTPException(status_code=400, detail="Số nhập vào lớn hơn giới hạn. Vui lòng nhập số nhỏ hơn số giới hạn là 500.")


