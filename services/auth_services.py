from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from utils.constants import ALGORITHM, SECRET_KEY
# from utils.auths import oauth2_scheme


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class AuthServiceHandler:
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._invalid_credentials = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    def verify_password(self, plain_password, hashed_password):
        return self._pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password):
        return self._pwd_context.hash(password)
    
    def is_authenticated(self, token: str = Depends(oauth2_scheme)):
        """"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return False
        except JWTError:
            return False

        return True
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
