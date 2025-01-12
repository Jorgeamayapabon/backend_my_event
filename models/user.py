from sqlalchemy import Boolean, Column, Integer, String
from db.config import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fullname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    role = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
