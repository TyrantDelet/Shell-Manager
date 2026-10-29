from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from functools import lru_cache
from pathlib import Path

_ENV_PREFIX = "SHELL_MANAGER_"
_PACKAGE_NAME = "shell_manager"
_FALLBACK_VERSION = "1.0.0"
_TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
_FALSE_VALUES = frozenset({"0", "false", "no", "off"})


def _detect_version() -> str:
    try:
        import importlib.metadata

        return importlib.metadata.version(_PACKAGE_NAME)
    except Exception:
        return _FALLBACK_VERSION

def _env_int(name: str) -> int | None:
    key = _ENV_PREFIX + name.upper()
    value = os.getenv(key)
    if value is None:
        return None
    try:
        parsed = int(value)
        if parsed <= 0:
            raise ValueError(f"{key} must be a positive integer, got {parsed}")
        return parsed
    except ValueError as e:
        raise ValueError(f"Environment variable {key} must be a valid integer.") from e

def _env_bool(name: str) -> bool | None:
    key = _ENV_PREFIX + name
    raw = os.getenv(key)
    if raw is None:
        return None
    value = raw.strip().lower()
    if value in _TRUE_VALUES:
        return True
    if value in _FALSE_VALUES:
        return False
    raise ValueError(
        f"{key} must be one of {sorted(_TRUE_VALUES | _FALSE_VALUES)}, got {raw!r}"
    )

class Parent(ABC):

    @abstractmethod
    def get_project_root(self) -> Path:
        """Return the project root path."""

    @abstractmethod
    def get_timeout_seconds(self) -> int:
        """Return the configured timeout value in seconds."""

    @abstractmethod
    def should_confirm_destructive(self) -> bool:
        """Return whether destructive actions should require confirmation."""

@dataclass(frozen=True)
class AppConfig(Parent):

    app_name: str = "Shell Manager"
    version: str = field(default_factory=_detect_version)
    author: str = "Tyrant_Delet"
    default_timeout_seconds: int = 120
    confirm_destructive_by_default: bool = True
    project_root: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent.parent.parent
    )

    def get_project_root(self) -> Path:
        return self.project_root

    def get_timeout_seconds(self) -> int:
        return self.default_timeout_seconds

    def should_confirm_destructive(self) -> bool:
        return self.confirm_destructive_by_default

    def __post_init__(self):
        if self.default_timeout_seconds <= 0:
            raise ValueError(
                "default_timeout_seconds must be positive, "
                f"got {self.default_timeout_seconds}"
            )


def load_config() -> AppConfig:
    candidates = {
        "default_timeout_seconds": _env_int("TIMEOUT"),
        "confirm_destructive_by_default": _env_bool("CONFIRM_DESTRUCTIVE"),
    }
    overrides = {k: v for k, v in candidates.items() if v is not None}
    return replace(AppConfig(), **overrides)


@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    return load_config()


CONFIG: AppConfig = get_config()


