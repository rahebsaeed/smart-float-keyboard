from core.layouts import LANGUAGE_REGISTRY
from utils.config import ConfigManager

def test_language_registry():
    """Verify all 3 languages are properly configured."""
    assert "en" in LANGUAGE_REGISTRY
    assert "fr" in LANGUAGE_REGISTRY
    assert "ar" in LANGUAGE_REGISTRY
    assert len(LANGUAGE_REGISTRY["en"]["layout"]) == 5

def test_config_defaults():
    """Verify configuration manager initializes properly."""
    config = ConfigManager()
    assert config.get("language") in ["en", "fr", "ar"]
    assert config.get("theme") in ["dark", "light"]
    assert config.get("toggle_size") > 0
