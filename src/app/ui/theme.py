from __future__ import annotations

from types import MappingProxyType
from typing import Final, Iterable

from rich.box import DOUBLE, HEAVY, MINIMAL, ROUNDED, SIMPLE, Box
from rich.theme import Theme

from app.models import Category, SafetyLevel