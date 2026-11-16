from __future__ import annotations

from enum import StrEnum
from typing import Final

class ViewAction(StrEnum):
    EXECUTE = "1"
    COPY = "2"
    BACK = "b"
    QUIT = "q"

    @property
    def label(self) -> str:
        return _ACTION_LABELS[self]


_ACTION_LABELS: Final[dict[ViewAction, str]] = {
    ViewAction.EXECUTE: "Execute command",
    ViewAction.COPY: "Copy to clipboard",
    ViewAction.BACK: "Back to list",
    ViewAction.QUIT: "Quit",
}

VIEW_ACTIONS: Final[tuple[tuple[str, str], ...]] = (
    ("1", "Execute command"),
    ("2", "Copy to clipboard"),
    ("b", "Back to list"),
    ("q", "Quit"),
)