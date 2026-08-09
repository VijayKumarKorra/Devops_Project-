"""Configuration tests — verify app config is loaded correctly."""
import os
import pytest
from userapi.src.config import Config, TestConfig, ProductionConfig


class TestDefaultConfig:
    def test_default_db_host(self):
        assert Config.DB_HOST in ("localhost", os.environ.get("DB_HOST", "localhost"))

    def test_default_db_port(self):
        assert Config.DB_PORT in ("5432", os.environ.get("DB_PORT", "5432"))

    def test_default_db_name(self):
        assert Config.DB_NAME == os.environ.get("DB_NAME", "userapi_db")

    def test_sqlalchemy_uri_contains_host(self):
        assert Config.DB_HOST in Config.SQLALCHEMY_DATABASE_URI

    def test_sqlalchemy_uri_contains_port(self):
        assert Config.DB_PORT in Config.SQLALCHEMY_DATABASE_URI

    def test_sqlalchemy_uri_contains_db_name(self):
        assert Config.DB_NAME in Config.SQLALCHEMY_DATABASE_URI

    def test_tracking_modifications_off(self):
        assert Config.SQLALCHEMY_TRACK_MODIFICATIONS is False

    def test_testing_flag_false(self):
        assert Config.TESTING is False

    def test_secret_key_set(self):
        assert Config.SECRET_KEY is not None and Config.SECRET_KEY != ""


class TestTestConfig:
    def test_testing_flag_true(self):
        assert TestConfig.TESTING is True

    def test_uses_sqlite_in_memory(self):
        assert "sqlite" in TestConfig.SQLALCHEMY_DATABASE_URI
        assert ":memory:" in TestConfig.SQLALCHEMY_DATABASE_URI


class TestProductionConfig:
    def test_debug_false(self):
        assert ProductionConfig.DEBUG is False


class TestAppConfig:
    def test_app_is_in_testing_mode(self, app):
        assert app.config["TESTING"] is True

    def test_app_has_sqlalchemy_uri(self, app):
        assert "SQLALCHEMY_DATABASE_URI" in app.config

    def test_app_secret_key_configured(self, app):
        assert app.config.get("SECRET_KEY") is not None

    def test_env_variable_override(self, monkeypatch):
        monkeypatch.setenv("DB_NAME", "custom_db")
        # Re-import to pick up env var (shows env-var-driven config pattern)
        import importlib
        import userapi.src.config as cfg_module
        importlib.reload(cfg_module)
        assert "custom_db" in cfg_module.Config.SQLALCHEMY_DATABASE_URI
        # Restore
        monkeypatch.delenv("DB_NAME", raising=False)
        importlib.reload(cfg_module)
