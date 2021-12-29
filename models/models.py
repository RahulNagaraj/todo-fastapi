import datetime as dt
import sqlalchemy as sql
import sqlalchemy.orm as orm
import passlib.hash as hash

from database import database


class User(database.Base):
    __tablename__ = "users"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    email = sql.Column(sql.String, unique=True, index=True)
    hashed_password = sql.Column(sql.String)
    created_at = sql.Column(sql.DateTime, default=dt.datetime.utcnow)

    posts = orm.relationship("Post", back_populates="owner")

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.hashed_password)


class Post(database.Base):
    __tablename__ = "posts"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    text = sql.Column(sql.String)
    created_at = sql.Column(sql.DateTime, default=dt.datetime.utcnow)

    owner = orm.relationship("User", back_populates="posts")
