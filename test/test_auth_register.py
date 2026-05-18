import pytest
from fastapi.exceptions import HTTPException
from unittest.mock import patch, MagicMock
from app.modules.auth.service import register_with_dni, register_with_immigrationcard
from app.modules.auth.schemas import DNIRegisterRequest, ImmigrationCardRegisterRequest


@patch("app.modules.auth.service.ReniecClient")
@patch("app.modules.auth.service.create_token")
def test_service_register_with_dni_success(mock_create_token, mock_reniec_class, mock_session):
    user_data_mock = DNIRegisterRequest(
        fullname="Juan Perez Gomez",
        email="juan.perz@example.com",
        password="Contraseñadejuanxd1",
        dni="05302528",
    )

    mock_reniec_instance = MagicMock()
    mock_reniec_class.return_value = mock_reniec_instance
    mock_reniec_instance.validate_dni.return_value = {
        "nombre_completo": "Juan Perez Gomez",
    }

    mock_session.query.return_value.filter.return_value.first.side_effect = [None, None]
    mock_create_token.return_value = "token test"

    response = register_with_dni(user_data_mock)

    assert response == {"access_token": "token test", "token_type": "bearer"}
    assert mock_session.query.return_value.filter.call_count == 2
    mock_reniec_instance.validate_dni.assert_called_once_with("05302528")
    assert mock_session.commit.call_count == 1
    assert mock_session.close.call_count == 1


def test_service_register_with_dni_existing_user(mock_session):
    user_data_mock = DNIRegisterRequest(
        fullname="Juan Perez Gomez",
        email="juan.perz@example.com",
        password="Contraseñadejuanxd1",
        dni="05302528",
    )

    mock_session.query.return_value.filter.return_value.first.return_value = "Juan Perez Gomez"

    with pytest.raises(HTTPException) as exc_info:
        register_with_dni(user_data_mock)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "El correo ya existe"
    assert mock_session.rollback.call_count == 1
    assert mock_session.close.call_count == 1


def test_service_register_with_dni_existing_dni(mock_session):
    user_data_mock = DNIRegisterRequest(
        fullname="Juan Perez Gomez",
        email="juan.perz@example.com",
        password="Contraseñadejuanxd1",
        dni="05302528",
    )

    mock_session.query.return_value.filter.return_value.first.side_effect = [None, "05302528"]

    with pytest.raises(HTTPException) as exc_info:
        register_with_dni(user_data_mock)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "El DNI ya existe"
    assert mock_session.rollback.call_count == 1
    assert mock_session.close.call_count == 1


@patch("app.modules.auth.service.ReniecClient")
def test_service_register_with_dni_fullnames_dont_match(mock_reniec_class, mock_session):
    user_data_mock = DNIRegisterRequest(
        fullname="Juan Perez Gomez",
        email="juan.perz@example.com",
        password="Contraseñadejuanxd1",
        dni="05302528",
    )

    mock_reniec_instance = MagicMock()
    mock_reniec_class.return_value = mock_reniec_instance
    mock_reniec_instance.validate_dni.return_value = {
        "nombre_completo": "Juan Perez 220 Gomez",
    }

    mock_session.query.return_value.filter.return_value.first.side_effect = [None, None]

    with pytest.raises(HTTPException) as exc_info:
        register_with_dni(user_data_mock)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "El nombre no coincide con RENIEC"
    assert mock_session.rollback.call_count == 1
    assert mock_session.close.call_count == 1


@patch("app.modules.auth.service.create_token")
def test_register_with_immigrationcard_success(mock_create_token, mock_session):
    user_data_mock = ImmigrationCardRegisterRequest(
        fullname="Foreigner User Name",
        email="foreigner@example.com",
        password="ValidPassword123*",
        immigration_card="CE1234567",
    )

    mock_session.query.return_value.filter.return_value.first.side_effect = [None, None]
    mock_create_token.return_value = "mocked_jwt_token"

    response = register_with_immigrationcard(user_data_mock)

    assert response == {"access_token": "mocked_jwt_token", "token_type": "bearer"}
    assert mock_session.query.return_value.filter.return_value.first.call_count == 2
    assert mock_session.add.call_count == 1
    assert mock_session.commit.call_count == 1
    assert mock_session.refresh.call_count == 1
    assert mock_session.close.call_count == 1


def test_register_with_immigrationcard_email_exists(mock_session):
    user_data_mock = ImmigrationCardRegisterRequest(
        fullname="Foreigner User Name",
        email="existing_email@example.com",
        password="ValidPassword123*",
        immigration_card="CE1234567",
    )

    mock_user_mock = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user_mock

    with pytest.raises(HTTPException) as exc_info:
        register_with_immigrationcard(user_data_mock)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "El correo ya existe"
    assert mock_session.query.return_value.filter.return_value.first.call_count == 1
    assert mock_session.commit.call_count == 0
    assert mock_session.close.call_count == 1


def test_register_with_immigrationcard_document_exists(mock_session):
    user_data_mock = ImmigrationCardRegisterRequest(
        fullname="Foreigner User Name",
        email="foreigner@example.com",
        password="ValidPassword123*",
        immigration_card="CE1234567",
    )

    mock_user_mock = MagicMock()
    mock_session.query.return_value.filter.return_value.first.side_effect = [None, mock_user_mock]

    with pytest.raises(HTTPException) as exc_info:
        register_with_immigrationcard(user_data_mock)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "El carnet ya existe"
    assert mock_session.query.return_value.filter.return_value.first.call_count == 2
    assert mock_session.commit.call_count == 0
    assert mock_session.close.call_count == 1
