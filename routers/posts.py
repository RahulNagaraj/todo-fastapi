import fastapi
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy.orm as orm
from typing import List

from schemas import schemas
from services import services

router = fastapi.APIRouter()


@router.post("/api/posts", response_model=schemas.Post)
async def create_post(post: schemas.PostCreate,
                      user: schemas.User = fastapi.Depends(
                          services.get_current_user),
                      db: orm.Session = fastapi.Depends(services.get_db)):
    return await services.create_post(
        user=user,
        db=db,
        post=post
    )


@router.get("/api/posts", response_model=List[schemas.Post])
async def get_user_posts(user: schemas.User = fastapi.Depends(
        services.get_current_user),
        db: orm.Session = fastapi.Depends(services.get_db)):
    return await services.get_user_posts(user=user, db=db)
