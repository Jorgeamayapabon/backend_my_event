from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from utils.constants import ALGORITHM, SECRET_KEY
# from utils.auths import oauth2_scheme


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class AuthServiceHandler:
    """
    A handler for user authentication services.

    This class provides methods for password hashing, password verification,
    creating JWT tokens for access, and verifying authentication based on tokens.

    Attributes:
        _pwd_context (CryptContext): The password hashing context using bcrypt.
        _invalid_credentials (HTTPException): The exception raised when credentials are incorrect.
    """
    def __init__(self):
        """
        Initializes the AuthServiceHandler.

        Sets up the CryptContext for password hashing and initializes the 
        invalid credentials exception.
        """
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._invalid_credentials = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    def verify_password(self, plain_password, hashed_password):
        """
        Verifies if a plain password matches the hashed password.

        Args:
            plain_password (str): The plain password entered by the user.
            hashed_password (str): The hashed password stored in the database.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self._pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password):
        """
        Hashes a plain password for storage.

        Args:
            password (str): The plain password to be hashed.

        Returns:
            str: The hashed password.
        """
        return self._pwd_context.hash(password)
    
    def is_authenticated(self, token: str = Depends(oauth2_scheme)):
        """
        Verifies if the provided JWT token is valid and the user is authenticated.

        Args:
            token (str): The JWT token obtained via OAuth2Bearer.

        Returns:
            bool: True if the token is valid and contains a valid email, False otherwise.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return False
        except JWTError:
            return False

        return True
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        """
        Creates a JWT access token with the given data and expiration time.

        Args:
            data (dict): The data to encode into the JWT token.
            expires_delta (timedelta, optional): The expiration time of the token. 
                                                 Defaults to 15 minutes if not provided.

        Returns:
            str: The encoded JWT access token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY)
        return encoded_jwt
