from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.user import UserCreate, UserUpdate, UserUpdateAdmin
from fastapi import Depends, HTTPException, status
from services.auth_services import AuthServiceHandler


auth = AuthServiceHandler()


class UserServiceHandler:
    def __init__(self, db: Session):
        self.db = db
        self._credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        self._user_not_found = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
        self._invalid_credentials = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        self._no_has_permission = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No has permission",
            headers={"WWW-Authenticate": "Bearer"},
        )
        self._email_already_exist = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is already a user with that email",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def list_users(self):
        return self.db.query(UserModel).all()

    def create_user(self, user: UserCreate, db: Session):
        db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
        if db_user:
            raise self._email_already_exist
        
        user_schema = user.model_dump()
        user_schema["hashed_password"] = auth.get_password_hash(user_schema["password"])
        user_schema.pop("password")
        db_user = UserModel(**user_schema)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_id(self, user_id: int):
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            raise self._user_not_found

        return db_user

    def update_user(self, user_id: int, user: UserUpdate | UserUpdateAdmin):
        db_user = self.get_user_by_id(user_id)

        for key, value in user.model_dump().items():
            if value:
                setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.get_user_by_id(user_id)
        self.db.delete(db_user)
        self.db.commit()
        return db_user

    def _get_user_by_email(self, email: str):
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not db_user:
            raise self._user_not_found

        return db_user

    def _authenticate_user(self, email: str, password: str):
        try:
            user = self._get_user_by_email(email)
        except HTTPException:
            raise self._invalid_credentials

        if not auth.verify_password(password, user.hashed_password):
            raise self._invalid_credentials

        return user

    def login(self, email: str, password: str):
        user = self._authenticate_user(email, password)
        access_token = auth.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
