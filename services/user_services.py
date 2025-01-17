from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.user import UserCreate, UserUpdate, UserUpdateAdmin
from fastapi import Depends, HTTPException, status
from services.auth_services import AuthServiceHandler


auth = AuthServiceHandler()


class UserServiceHandler:
    """
    Handles user-related operations including user creation, updating, deletion, authentication, and login.

    Attributes:
        db (Session): The database session used to interact with the database.
        _credentials_exception (HTTPException): Exception raised for invalid credentials.
        _user_not_found (HTTPException): Exception raised when a user is not found.
        _invalid_credentials (HTTPException): Exception raised for incorrect username or password.
        _no_has_permission (HTTPException): Exception raised when the user does not have permission.
        _email_already_exist (HTTPException): Exception raised when the email already exists in the database.
    """
    
    def __init__(self, db: Session):
        """
        Initializes the user service handler with a database session and predefined exceptions.

        Args:
            db (Session): The database session used to interact with the database.
        """
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
        """
        Retrieves a list of all users in the database.

        Returns:
            list: A list of all users.
        """
        return self.db.query(UserModel).all()

    def create_user(self, user: UserCreate, db: Session):
        """
        Creates a new user in the database after validating that the email is not already taken.

        Args:
            user (UserCreate): The user data to create the new user.
            db (Session): The database session to interact with the database.

        Returns:
            UserModel: The created user.

        Raises:
            HTTPException: If the email is already taken.
        """
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
        """
        Retrieves a user by its ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            UserModel: The user with the specified ID.

        Raises:
            HTTPException: If the user is not found.
        """
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            raise self._user_not_found

        return db_user

    def update_user(self, user_id: int, user: UserUpdate | UserUpdateAdmin):
        """
        Updates the user information based on the provided user data.

        Args:
            user_id (int): The ID of the user to update.
            user (UserUpdate | UserUpdateAdmin): The updated user data.

        Returns:
            UserModel: The updated user.

        Raises:
            HTTPException: If the user is not found.
        """
        db_user = self.get_user_by_id(user_id)

        for key, value in user.model_dump().items():
            if value:
                setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        """
        Deletes a user by its ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            UserModel: The deleted user.

        Raises:
            HTTPException: If the user is not found.
        """
        db_user = self.get_user_by_id(user_id)
        self.db.delete(db_user)
        self.db.commit()
        return db_user

    def _get_user_by_email(self, email: str):
        """
        Helper method to retrieve a user by their email.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            UserModel: The user with the specified email.

        Raises:
            HTTPException: If the user is not found.
        """
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not db_user:
            raise self._user_not_found

        return db_user

    def _authenticate_user(self, email: str, password: str):
        """
        Authenticates a user by verifying their email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            UserModel: The authenticated user.

        Raises:
            HTTPException: If the credentials are invalid.
        """
        try:
            user = self._get_user_by_email(email)
        except HTTPException:
            raise self._invalid_credentials

        if not auth.verify_password(password, user.hashed_password):
            raise self._invalid_credentials

        return user

    def login(self, email: str, password: str):
        """
        Authenticates a user and returns an access token.

        Args:
            email (str): The email of the user to log in.
            password (str): The password of the user to log in.

        Returns:
            dict: A dictionary containing the access token and its type.

        Raises:
            HTTPException: If the credentials are invalid.
        """
        user = self._authenticate_user(email, password)
        access_token = auth.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
