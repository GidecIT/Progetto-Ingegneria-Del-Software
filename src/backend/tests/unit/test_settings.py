from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from participium.config.settings import Settings, _as_bool

pytestmark = pytest.mark.unit


def test_as_bool():
    # Test truthy values
    assert _as_bool("1") is True
    assert _as_bool("true") is True
    assert _as_bool("TRUE") is True
    assert _as_bool(" yes ") is True
    assert _as_bool("on") is True

    # Test falsy values
    assert _as_bool("0") is False
    assert _as_bool("false") is False
    assert _as_bool("no") is False
    assert _as_bool("off") is False
    assert _as_bool("anything") is False

    # Test None and default
    assert _as_bool(None) is False
    assert _as_bool(None, default=True) is True


@patch("participium.config.settings.load_dotenv")
@patch("os.getenv")
@patch("pathlib.Path.mkdir")
def test_settings_from_env(mock_mkdir, mock_getenv, mock_load_dotenv):
    # Mock environment variables
    env_vars = {
        "SECRET_KEY": "test-secret",
        "FLASK_ENV": "production",
        "PORT": "8080",
        "AUTO_INIT_DB": "false",
        "MAIL_BACKEND": "smtp",
        "SMTP_HOST": "smtp.example.com",
    }
    mock_getenv.side_effect = lambda key, default=None: env_vars.get(key, default)

    settings = Settings.from_env()

    # Verify values are correctly loaded
    assert settings.secret_key == "test-secret"
    assert settings.debug is False  # production != development
    assert settings.port == 8080
    assert settings.auto_init_db is False
    assert settings.mail_backend == "smtp"
    assert settings.smtp_host == "smtp.example.com"
    
    # Verify default values (not in env_vars)
    assert settings.host == "0.0.0.0"
    assert settings.bootstrap_reference_data is True  # default in from_env is True

    # Verify paths are instances of Path
    assert isinstance(settings.instance_path, Path)
    assert isinstance(settings.media_root, Path)
    assert isinstance(settings.mail_outbox_dir, Path)


@patch("participium.config.settings.load_dotenv")
@patch("os.getenv")
@patch("pathlib.Path.mkdir")
def test_settings_default_values(mock_mkdir, mock_getenv, mock_load_dotenv):
    # Mock empty environment
    mock_getenv.side_effect = lambda key, default=None: default

    settings = Settings.from_env()

    assert settings.secret_key == "change-me"
    assert settings.debug is True  # development is default
    assert settings.port == 5050
    assert settings.auto_init_db is True
    assert settings.mail_backend == "console"
