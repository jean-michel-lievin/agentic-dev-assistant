from app.core.config import get_settings

settings = get_settings()


def test_settings_loaded():
    assert settings is not None
