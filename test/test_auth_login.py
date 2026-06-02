import pytest
from fastapi.exceptions import HTTPException
from unittest.mock import patch, MagicMock
from app.modules.auth.service import login_with_dni
from app.modules.auth.schemas import LoginRequest

@patch("app.modules.auth.service.verify_password_hash")
@patch("app.modules.auth.service.create_token")
def test_login_with_dni_success(mock_create_token, mock_verify_password_hash, mock_session):
    login_data = LoginRequest(
        document="05302528",
        password="PasswordValid123"
    )

    # El usuario es retornado por la BD
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = "usuario@example.com"
    mock_user.user_type = "ciudadano"
    mock_user.password = "hashed_password_mock"

    # Configuración deretornos de los mocks
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    mock_verify_password_hash.return_value = True
    mock_create_token.return_value = "token_de_prueba_jwt"

    # Ejecución
    response = login_with_dni(login_data)

    # Validaciones
    assert response == {"access_token": "token_de_prueba_jwt", "token_type": "bearer"}
    mock_session.query.return_value.filter.return_value.first.assert_called_once()
    mock_verify_password_hash.assert_called_once_with("PasswordValid123", "hashed_password_mock")
    assert mock_session.close.call_count == 1

