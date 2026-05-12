from datetime import timedelta

import pytest

from backend.core.security import (
    create_access_token,
    decode_token,
    get_password_hash,
    verify_password,
)


class TestPasswordHashing:
    def test_get_password_hash_returns_different_string(self):
        password = "my_secret_password"
        hashed = get_password_hash(password)
        assert isinstance(hashed, str)
        assert hashed != password

    def test_verify_password_with_correct_password(self):
        password = "my_secret_password"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_with_incorrect_password(self):
        password = "my_secret_password"
        hashed = get_password_hash(password)
        assert verify_password("wrong_password", hashed) is False

    def test_same_password_produces_different_hashes(self):
        password = "same_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2


class TestJWT:
    def test_create_access_token_returns_string(self):
        token = create_access_token({"sub": "1", "email": "test@test.com"})
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_token_returns_correct_payload(self):
        data = {"sub": "1", "email": "test@test.com", "roles": ["ADMIN"]}
        token = create_access_token(data)
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "1"
        assert payload["email"] == "test@test.com"
        assert payload["roles"] == ["ADMIN"]

    def test_decode_token_includes_exp_claim(self):
        token = create_access_token({"sub": "1"})
        payload = decode_token(token)
        assert payload is not None
        assert "exp" in payload

    def test_decode_token_with_expired_token_returns_none(self):
        token = create_access_token(
            {"sub": "1"},
            expires_delta=timedelta(seconds=-1),
        )
        payload = decode_token(token)
        assert payload is None

    def test_decode_token_with_invalid_token_returns_none(self):
        payload = decode_token("invalid.token.here")
        assert payload is None

    def test_decode_token_with_malformed_token_returns_none(self):
        payload = decode_token("not-a-jwt")
        assert payload is None
