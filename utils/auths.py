from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from db.config import get_db
from models.user import UserModel
from utils.constants import ALGORITHM, SECRET_KEY
from jose import JWTError, jwt
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
USER_INACTIVE_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Inactive user",
)
NO_HAS_PERMISSION_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No has permission",
    headers={"WWW-Authenticate": "Bearer"}
)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CREDENTIALS_EXCEPTION
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise CREDENTIALS_EXCEPTION

    return user


def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if not current_user.active:
        raise USER_INACTIVE_EXCEPTION
    return current_user


def has_role(current_user: UserModel, roles: List[str]):
    return current_user.role in roles


def get_current_user_with_role(roles: List[str]):
    def dependency(current_user: UserModel = Depends(get_current_active_user)):
        if not has_role(current_user, roles):
            raise NO_HAS_PERMISSION_EXCEPTION
        return current_user
    return dependency
 