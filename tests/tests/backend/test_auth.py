from unittest.mock import patch, MagicMock

import bcrypt
import pytest

from backend.auth import login_user, register_user


@pytest.fixture(autouse=True)
def mock_db():
    """Mock both get_supabase() and get_service_client() for all tests."""
    with patch("backend.auth.get_supabase") as mock_supabase, \
         patch("backend.auth.get_service_client") as mock_service:
        supabase = MagicMock()
        service = MagicMock()
        mock_supabase.return_value = supabase
        mock_service.return_value = service
        yield supabase, service


def _fake_user(username="testuser", uid="00000000-0000-0000-0000-000000000001", full_name="Test User", pwhash=None):
    return {
        "id": uid,
        "username": username,
        "full_name": full_name,
        "password_hash": pwhash,
    }


class TestRegister:
    def test_register_success(self, mock_db):
        _, service = mock_db
        service.table("users").insert().execute.return_value = MagicMock(
            data=[_fake_user(username="newuser", uid="u1", full_name="New User")],
        )
        result = register_user(username="newuser", password="Pass@123", full_name="New User")
        assert result["success"] is True
        assert "Registration successful" in result["message"]

    def test_register_returns_user(self, mock_db):
        _, service = mock_db
        service.table("users").insert().execute.return_value = MagicMock(
            data=[_fake_user(username="alice", uid="22222222-2222-2222-2222-222222222222", full_name="Alice")],
        )
        result = register_user(username="alice", password="Pass@123", full_name="Alice")
        user = result["user"]
        assert user["username"] == "alice"
        assert user["full_name"] == "Alice"
        assert user["id"] == "22222222-2222-2222-2222-222222222222"

    def test_register_access_token_is_none(self, mock_db):
        _, service = mock_db
        service.table("users").insert().execute.return_value = MagicMock(
            data=[_fake_user()],
        )
        result = register_user(username="anyuser", password="Pass@123", full_name="Any")
        assert result["access_token"] is None

    def test_register_duplicate_username(self, mock_db):
        _, service = mock_db
        service.table("users").insert().execute.side_effect = Exception("duplicate key value violates unique constraint")
        result = register_user(username="dup", password="Pass@123", full_name="Dup")
        assert result["success"] is False
        assert "already taken" in result["message"]


class TestLogin:
    def test_login_success(self, mock_db):
        _, service = mock_db
        pwhash = bcrypt.hashpw(b"Pass@123", bcrypt.gensalt()).decode()
        service.table("users").select("*").eq("username", "testuser").execute.return_value = MagicMock(
            data=[_fake_user(pwhash=pwhash)],
        )
        result = login_user(username="testuser", password="Pass@123")
        assert result["success"] is True
        assert result["user"]["username"] == "testuser"
        assert result["user"]["full_name"] == "Test User"

    def test_login_failure_wrong_password(self, mock_db):
        _, service = mock_db
        pwhash = bcrypt.hashpw(b"RealPass1", bcrypt.gensalt()).decode()
        service.table("users").select("*").eq("username", "testuser").execute.return_value = MagicMock(
            data=[_fake_user(pwhash=pwhash)],
        )
        result = login_user(username="testuser", password="WrongPass")
        assert result["success"] is False
        assert "Invalid" in result["message"]

    def test_login_failure_unknown_user(self, mock_db):
        _, service = mock_db
        service.table("users").select("*").eq("username", "nobody").execute.return_value = MagicMock(data=[])
        result = login_user(username="nobody", password="x")
        assert result["success"] is False
        assert "Invalid" in result["message"]

    def test_login_failure_github_user_no_password(self, mock_db):
        _, service = mock_db
        service.table("users").select("*").eq("username", "ghuser").execute.return_value = MagicMock(
            data=[_fake_user(username="ghuser", pwhash=None)],
        )
        result = login_user(username="ghuser", password="anything")
        assert result["success"] is False
        assert result["message"] == "Invalid username or password"
