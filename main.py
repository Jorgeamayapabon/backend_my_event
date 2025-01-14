from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api import api_router
from db.config import get_db
from services.user_services import UserServiceHandler


app = FastAPI(title="My Event App", version="0.1.0")

app.include_router(api_router, prefix="/api")

@app.post("/login", tags=["Authentication"])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """"""
    service = UserServiceHandler(db)
    return service.login(
        email=form_data.username,
        password=form_data.password
    )
