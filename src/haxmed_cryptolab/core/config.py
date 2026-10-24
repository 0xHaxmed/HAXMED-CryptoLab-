"""Configuration management for HAXMED CryptoLab."""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict

from haxmed_cryptolab.core.constants import CONFIG_FILE_PATH, DEFAULT_LANGUAGE, DEFAULT_THEME


@dataclass
class AppConfig:
    """Application configuration options."""

    language: str = DEFAULT_LANGUAGE
    theme: str = DEFAULT_THEME
    enable_history: bool = False
    default_export_format: str = "txt"  # "txt" or "json"
    chunk_size_kb: int = 64
    max_recovery_candidates: int = 1_000_000
    custom_settings: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppConfig":
        valid_keys = cls.__dataclass_fields__.keys()
        filtered = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered)


class ConfigManager:
    """Manages loading, persisting, and validating configuration."""

    def __init__(self, config_path: Path = CONFIG_FILE_PATH):
        self.config_path = config_path
        self._config = self.load()

    @property
    def config(self) -> AppConfig:
        return self._config

    def load(self) -> AppConfig:
        if not self.config_path.exists():
            default_config = AppConfig()
            self.save(default_config)
            return default_config

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return AppConfig.from_dict(data)
        except Exception:
            # Fall back safely on corrupted config
            return AppConfig()

    def save(self, config: AppConfig) -> bool:
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config.to_dict(), f, indent=2)
            self._config = config
            return True
        except Exception:
            return False

    def reset_defaults(self) -> AppConfig:
        defaults = AppConfig()
        self.save(defaults)
        return defaults
