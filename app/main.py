from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

from .settings import metadata as meta, config
from .database import database
from .models.common import User
from .routers import users, admin, operations
from .dependencies import common as CDepends

SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.settings.access_token_expire_minutes)

database.db.connect()
database.db.create_tables([User])
database.db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    # getting title from .env file
    title = config.settings.app_name,
    description = meta.description,
    version = meta.version,
    terms_of_service = meta.terms_of_service,
    contact = meta.contact,
    license_info = meta.license_info,
    openapi_tags= meta.tags_metadata,
    docs_url = meta.docs_url, 
    redoc_url = meta.redoc_url,
    openapi_url = meta.openapi_url
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = meta.origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(users.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(CDepends.get_db)],
    responses={404: {"description": "Not found"}},
)

@app.get("/")
def root():
    return {"message": "working"}
