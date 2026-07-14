from unittest.mock import patch, MagicMock

import pytest

from backend.auth import login_user, register_user, send_reset_email


@pytest.fixture(autouse=True)
def mock_supabase():
    """Mock get_supabase() so tests never hit the real Supabase API."""
    with patch("backend.auth.get_supabase") as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def _fake_user(email="a@b.com", uid="00000000-0000-0000-0000-000000000001", full_name="Test User"):
    u = MagicMock()
    u.id = uid
    u.email = email
    u.user_metadata = {"full_name": full_name, "user_name": "testuser"}
    return u


def _fake_session(token="sbp-token"):
    s = MagicMock()
    s.access_token = token
    return s


class TestLogin:
    def test_login_success(self, mock_supabase):
        mock_supabase.auth.sign_in_with_password.return_value = MagicMock(
            user=_fake_user(),
            session=_fake_session(),
        )
        result = login_user(email="a@b.com", password="Pass@123")
        assert result["success"] is True
        assert result["access_token"] == "sbp-token"

    def test_login_success_sets_session_user(self, mock_supabase):
        mock_supabase.auth.sign_in_with_password.return_value = MagicMock(
            user=_fake_user(),
            session=_fake_session(),
        )
        result = login_user(email="a@b.com", password="Pass@123")
        user = result["user"]
        assert "id" in user
        assert user["email"] == "a@b.com"
        assert user["full_name"] == "Test User"

    def test_login_failure_wrong_credentials(self, mock_supabase):
        mock_supabase.auth.sign_in_with_password.side_effect = Exception("Invalid login credentials")
        result = login_user(email="wrong@example.com", password="bad")
        assert result["success"] is False
        assert "Invalid" in result["message"]

    def test_login_failure_empty_email(self, mock_supabase):
        mock_supabase.auth.sign_in_with_password.side_effect = Exception("Invalid login credentials")
        result = login_user(email="", password="x")
        assert result["success"] is False

    def test_login_failure_empty_password(self, mock_supabase):
        mock_supabase.auth.sign_in_with_password.side_effect = Exception("Invalid login credentials")
        result = login_user(email="a@b.com", password="")
        assert result["success"] is False


class TestRegister:
    def test_register_success(self, mock_supabase):
        mock_supabase.auth.sign_up.return_value = MagicMock(
            user=_fake_user(email="new@test.com", full_name="New User"),
        )
        result = register_user(email="new@test.com", password="Pass@123", full_name="New User")
        assert result["success"] is True
        assert "Registration successful" in result["message"]

    def test_register_returns_user(self, mock_supabase):
        mock_supabase.auth.sign_up.return_value = MagicMock(
            user=_fake_user(email="user@example.com", uid="22222222-2222-2222-2222-222222222222", full_name="Alice"),
        )
        result = register_user(email="user@example.com", password="Pass@123", full_name="Alice")
        user = result["user"]
        assert user["email"] == "user@example.com"
        assert user["full_name"] == "Alice"
        assert user["id"] == "22222222-2222-2222-2222-222222222222"

    def test_register_access_token_is_none(self, mock_supabase):
        mock_supabase.auth.sign_up.return_value = MagicMock(
            user=_fake_user(),
        )
        result = register_user(email="any@example.com", password="Pass@123", full_name="Any")
        assert result["access_token"] is None

    def test_register_duplicate_email(self, mock_supabase):
        mock_supabase.auth.sign_up.side_effect = Exception("already registered")
        result = register_user(email="dup@test.com", password="Pass@123", full_name="Dup")
        assert result["success"] is False
        assert "already exists" in result["message"]


class TestResetPassword:
    def test_reset_email_success(self):
        result = send_reset_email(email="admin@surfacedetect.com")
        assert result["success"] is True
        assert "reset link" in result["message"].lower()

    def test_reset_email_any_email_succeeds(self):
        result = send_reset_email(email="nonexistent@example.com")
        assert result["success"] is True
