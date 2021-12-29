import fastapi
from fastapi.security import OAuth2PasswordBearer
import sqlalchemy.orm as orm
import email_validator
import passlib.hash as hash
import jwt as jwt

from database import database
from models import models
from schemas import schemas

JWT_SECRET = "todoapisecretkeyverysafekeyword"

oauth2Schema = OAuth2PasswordBearer("/api/users/login")


def create_database():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str,
                            db: orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def create_user(user: schemas.UserCreate,
                      db: orm.Session):
    try:
        valid = email_validator.validate_email(email=user.email)
        email = valid.email
    except email_validator.EmailNotValidError:
        raise fastapi.HTTPException(status_code=400,
                                    detail="Please enter a valid email")

    hashed_password = hash.bcrypt.hash(user.password)
    user_obj = models.User(email=email,
                           hashed_password=hashed_password)

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def create_token(user: models.User):
    user_schema_obj = schemas.User.from_orm(user)
    user_dict = user_schema_obj.dict()
    del user_dict["created_at"]

    token = jwt.encode(user_dict, JWT_SECRET)
    return dict(access_token=token, token_type="bearer")


async def authenticate_user(email: str, password: str, db: orm.Session):
    user = await get_user_by_email(email=email, db=db)

    if not user:
        return False

    if not user.verify_password(password=password):
        return False

    return user


async def get_current_user(db: orm.Session = fastapi.Depends(get_db),
                           token: str = fastapi.Depends(oauth2Schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401,
                                    detail="Invalid email or password")

    return schemas.User.from_orm(user)


async def create_post(user: schemas.User,
                      db: orm.Session,
                      post: schemas.PostCreate):
    post = models.Post(**post.dict(), owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return schemas.Post.from_orm(post)


async def get_user_posts(user: schemas.User, db: orm.Session):
    posts = db.query(models.Post).filter_by(owner_id=user.id)

    return list(map(schemas.Post.from_orm, posts))
