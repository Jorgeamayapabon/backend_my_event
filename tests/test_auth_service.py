import pytest
from unittest.mock import patch
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from jose import JWTError, jwt
from services.auth_services import AuthServiceHandler
from utils.constants import ALGORITHM, SECRET_KEY

# Instanciamos el servicio de autenticación
auth_service = AuthServiceHandler()

# Test de verificación de contraseña
def test_verify_password():
    password = "secure_password"
    hashed_password = auth_service.get_password_hash(password)

    # Verificamos que la contraseña ingresada coincida con el hash
    assert auth_service.verify_password(password, hashed_password) is True

    # Verificamos que una contraseña incorrecta no coincida con el hash
    assert auth_service.verify_password("wrong_password", hashed_password) is False

# Test de creación de token
def test_create_access_token():
    data = {"sub": "test@example.com"}
    
    # Creamos el token
    token = auth_service.create_access_token(data=data)

    # Decodificamos el token
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Verificamos que el token contenga los datos correctos
    assert decoded_token["sub"] == data["sub"]
    assert "exp" in decoded_token

# Test de autenticación (is_authenticated)
@patch("services.auth_services.jwt.decode")
def test_is_authenticated(mock_jwt_decode):
    # Simulamos un token válido
    valid_token = "valid_jwt_token"
    
    # Comprobamos que el token sea válido
    mock_jwt_decode.return_value = {"sub": "test@example.com"}
    assert auth_service.is_authenticated(valid_token) is True
    
    # Simulamos un token inválido
    mock_jwt_decode.side_effect = JWTError("JWT decode error")
    assert auth_service.is_authenticated(valid_token) is False

# Test de hashing de contraseña
def test_get_password_hash():
    password = "password123"
    hashed_password = auth_service.get_password_hash(password)
    
    # Verificamos que el hash no sea igual a la contraseña original
    assert hashed_password != password
    assert auth_service.verify_password(password, hashed_password) is True
