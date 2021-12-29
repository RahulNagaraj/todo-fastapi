import fastapi
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy.orm as orm
from typing import List

from schemas import schemas
from services import services
import routers

app = fastapi.FastAPI()

app.include_router(routers.router, prefix="/api", tags=['users'])
