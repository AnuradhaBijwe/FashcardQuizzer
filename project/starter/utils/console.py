"""
Terminal presentation helpers for the Flashcard Quizzer CLI.

Colour is a presentation concern, so it is kept out of both the data layer
(:mod:`utils.file_handler`) and the quiz engine (:mod:`utils.quiz_engine`).
Only ANSI escape codes from the standard library are used -- no third-party
package is pulled in just to paint two words.

Every helper degrades to plain text when the output stream cannot render
colour, so the CLI stays readable when it is piped to a file, run in a dumb
terminal, or run with ``NO_COLOR`` set.
"""

import os
import sys
from typing import Optional, TextIO

# ANSI SGR codes. Kept minimal on purpose: the CLI only needs a success
# colour, a failure colour and light emphasis.
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
BOLD = "\033[1m"
DIM = "\033[2m"


def supports_color(stream: Optional[TextIO] = None) -> bool:
    """
    Report whether ANSI colour should be written to ``stream``.

    Colour is suppressed when the stream is not a terminal (piped or
    redirected output), when the terminal advertises itself as ``dumb``, or
    when the user has opted out through the ``NO_COLOR`` convention.

    Args:
        stream: Stream the output is headed for. Defaults to ``sys.stdout``.

    Returns:
        ``True`` if escape codes are safe to emit.
    """
    target = stream if stream is not None else sys.stdout

    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM", "").lower() == "dumb":
        return False

    # Streams such as io.StringIO have no isatty(); treat those as non-TTY.
    isatty = getattr(target, "isatty", None)
    return bool(isatty and isatty())


class Palette:
    """
    Wrap text in ANSI colours, or return it untouched when colour is off.

    Holding the on/off decision in one object means callers never branch on
    it: they always call :meth:`green` or :meth:`red` and get something
    sensible either way.
    """

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    def __repr__(self) -> str:
        return f"{type(self).__name__}(enabled={self.enabled})"

    @classmethod
    def for_stream(cls, stream: Optional[TextIO] = None) -> "Palette":
        """Build a palette that matches what ``stream`` can actually render."""
        return cls(enabled=supports_color(stream))

    def green(self, text: str) -> str:
        """Colour ``text`` green, used for correct answers."""
        return self._paint(text, GREEN)

    def red(self, text: str) -> str:
        """Colour ``text`` red, used for incorrect answers and errors."""
        return self._paint(text, RED)

    def bold(self, text: str) -> str:
        """Emphasise ``text``, used for questions and headings."""
        return self._paint(text, BOLD)

    def dim(self, text: str) -> str:
        """De-emphasise ``text``, used for hints and separators."""
        return self._paint(text, DIM)

    def _paint(self, text: str, code: str) -> str:
        """Apply one SGR code, resetting afterwards so styles never leak."""
        if not self.enabled or not text:
            return text
        return f"{code}{text}{RESET}"
