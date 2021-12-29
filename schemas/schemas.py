import datetime as dt
import pydantic


class UserBase(pydantic.BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    created_at: dt.datetime

    class Config:
        orm_mode = True


class PostBase(pydantic.BaseModel):
    text: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner_id: int
    created_at: dt.datetime

    class Config:
        orm_mode = True
