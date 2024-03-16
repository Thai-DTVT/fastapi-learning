from pydantic import BaseModel
from typing import List



class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    

    class Config:
        orm_mode = True


class UserDelete(BaseModel):
    id: int
    

    class Config:
        orm_mode = True    


class UserChange(BaseModel):
    old_password: str
    new_password: str
    repeat_password: str
    class Config:
        orm_mode = True
        
class FibonacciResponse(BaseModel):
    result: List[int]