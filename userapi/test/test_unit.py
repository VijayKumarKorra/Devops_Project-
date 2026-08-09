"""Unit tests — model validation logic, no HTTP calls."""
import pytest
from userapi.src.models import User


class TestUserValidation:
    def test_validate_requires_username(self):
        errors = User.validate({"email": "a@b.com"})
        assert any("username" in e for e in errors)

    def test_validate_requires_email(self):
        errors = User.validate({"username": "alice"})
        assert any("email" in e for e in errors)

    def test_validate_rejects_invalid_email(self):
        errors = User.validate({"username": "alice", "email": "notanemail"})
        assert any("invalid" in e for e in errors)

    def test_validate_passes_with_valid_data(self):
        errors = User.validate({"username": "alice", "email": "alice@example.com"})
        assert errors == []

    def test_validate_passes_with_extra_fields(self):
        errors = User.validate({
            "username": "bob",
            "email": "bob@example.com",
            "firstname": "Bob",
            "lastname": "Smith",
        })
        assert errors == []

    def test_to_dict_includes_expected_keys(self, app, db):
        with app.app_context():
            user = User(username="charlie", email="charlie@example.com",
                        firstname="Charlie", lastname="Brown")
            db.session.add(user)
            db.session.commit()

            d = user.to_dict()
            assert set(d.keys()) == {"id", "username", "email", "firstname", "lastname", "created_at"}
            assert d["username"] == "charlie"
            assert d["email"] == "charlie@example.com"

    def test_repr(self, app, db):
        with app.app_context():
            user = User(username="diana", email="diana@example.com")
            assert "diana" in repr(user)
