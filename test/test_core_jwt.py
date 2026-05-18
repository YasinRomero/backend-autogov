from app.core.security import create_token, verify_token

user_data = {"user_id": 1, "email": "test@test.com"}


def test_create_token():
    token_generate = create_token(user_data)
    assert token_generate is not None
    assert type(token_generate) is str


def test_verify_token():
    token_generate = create_token(user_data)
    payload = verify_token(token_generate)
    assert payload is not None and type(payload) is dict
    assert payload["user_id"] == user_data["user_id"]
    assert payload["email"] == user_data["email"]
