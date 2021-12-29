import fastapi
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy.orm as orm
from typing import List

from schemas import schemas
from services import services

router = fastapi.APIRouter()


@router.post("/signup/")
async def create_user(user: schemas.UserCreate,
                      db: orm.Session = fastapi.Depends(services.get_db)):
    db_user = await services.get_user_by_email(user.email, db=db)

    if db_user:
        raise fastapi.HTTPException(status_code=400,
                                    detail="User already exists")

    user = await services.create_user(user=user, db=db)

    return await services.create_token(user=user)


@router.post("/login")
async def generate_token(form_data: OAuth2PasswordRequestForm = fastapi.Depends(),
                         db: orm.Session = fastapi.Depends(services.get_db)):
    user = await services.authenticate_user(email=form_data.username,
                                            password=form_data.password,
                                            db=db)

    if not user:
        raise fastapi.HTTPException(status_code=401,
                                    detail="Invalid credentials")

    return await services.create_token(user)


@router.get("/me", response_model=schemas.User)
async def get_user(user: schemas.User = fastapi.Depends(services.get_current_user)):
    return user
