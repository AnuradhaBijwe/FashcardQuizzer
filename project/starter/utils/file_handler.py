"""
File handling utility for data persistence.

This module demonstrates file I/O operations and error handling
patterns that students can learn from and extend.

It also owns the flashcard data layer: reading a deck from a JSON file,
normalizing the supported input formats and validating every card.
Quiz logic deliberately lives elsewhere -- this module only answers the
question "is this file a usable list of flashcards?".
"""

import json
import os
from typing import Any, Dict, List, Union
from pathlib import Path

# A single flashcard as it is stored on disk and handed to the rest of the app.
Flashcard = Dict[str, Any]

# Every flashcard must carry these fields, and each one must hold text.
REQUIRED_FLASHCARD_FIELDS = ("front", "back")


class FlashcardDataError(Exception):
    """
    Raised when flashcard data cannot be loaded or fails validation.

    The message is written for end users, so callers (for example the CLI)
    can print ``str(error)`` directly instead of leaking a traceback.
    """


class FileHandler:
    """Handle file operations for data persistence."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def save_data(self, filename: str, data: Dict[str, Any]) -> None:
        """Save data to a JSON file."""
        filepath = self.data_dir / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except (IOError, TypeError) as e:
            raise RuntimeError(f"Failed to save data to {filename}: {e}")
    
    def load_data(self, filename: str) -> Dict[str, Any]:
        """Load data from a JSON file."""
        filepath = self.data_dir / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except (IOError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load data from {filename}: {e}")
    
    def file_exists(self, filename: str) -> bool:
        """Check if a file exists in the data directory."""
        return (self.data_dir / filename).exists()
    
    def delete_file(self, filename: str) -> None:
        """Delete a file from the data directory."""
        filepath = self.data_dir / filename
        if filepath.exists():
            filepath.unlink()
    
    def list_files(self) -> list[str]:
        """List all files in the data directory."""
        return [f.name for f in self.data_dir.iterdir() if f.is_file()]


def load_flashcard(file_path: Union[str, Path]) -> List[Flashcard]:
    """
    Load and validate a flashcard deck from a JSON file.

    Two input formats are accepted and normalized into the same result:

    1. Array format::

        [{"front": "...", "back": "..."}]

    2. Object format::

        {"cards": [{"front": "...", "back": "..."}]}

    Args:
        file_path: Path to the JSON file holding the deck.

    Returns:
        A list of validated flashcards, each a dict with at least the
        ``front`` and ``back`` keys. Extra keys are preserved.

    Raises:
        FlashcardDataError: If the file is missing or unreadable, the JSON is
            malformed, the structure does not match one of the two supported
            formats, or any card is missing/misusing a required field. The
            message is safe to show to the user as-is.
    """
    path = Path(file_path)

    try:
        with open(path, "r", encoding="utf-8") as file:
            payload = json.load(file)
    except FileNotFoundError as exc:
        raise FlashcardDataError(
            f"Flashcard file not found: {path}. "
            "Check the path, or create the file with a list of cards."
        ) from exc
    except IsADirectoryError as exc:
        raise FlashcardDataError(
            f"Expected a JSON file but {path} is a directory."
        ) from exc
    except UnicodeDecodeError as exc:
        raise FlashcardDataError(
            f"{path} is not readable as UTF-8 text, so it cannot be valid JSON."
        ) from exc
    except json.JSONDecodeError as exc:
        raise FlashcardDataError(
            f"{path} is not valid JSON: {exc.msg} "
            f"(line {exc.lineno}, column {exc.colno}). "
            "Check for a missing comma, bracket or quote."
        ) from exc
    except OSError as exc:
        raise FlashcardDataError(
            f"Could not read {path}: {exc.strerror or exc}."
        ) from exc

    cards = _extract_card_list(payload, path)
    return _validate_flashcards(cards, path)


def _extract_card_list(payload: Any, path: Path) -> List[Any]:
    """
    Normalize a parsed JSON payload into a raw list of card entries.

    Accepts the array format as-is and unwraps the object format's ``cards``
    key. The entries themselves are not inspected here; that is the job of
    :func:`_validate_flashcards`.
    """
    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        if "cards" not in payload:
            raise FlashcardDataError(
                f"{path} is an object but has no 'cards' key. Use either "
                '{"cards": [...]} or a plain list of flashcards.'
            )
        cards = payload["cards"]
        if not isinstance(cards, list):
            raise FlashcardDataError(
                f"The 'cards' value in {path} must be a list of flashcards, "
                f"but it is {_json_type_name(cards)}."
            )
        return cards

    raise FlashcardDataError(
        f"{path} must contain either a list of flashcards or an object with a "
        f"'cards' list, but it contains {_json_type_name(payload)}."
    )


def _validate_flashcards(cards: List[Any], path: Path) -> List[Flashcard]:
    """
    Check that every entry is an object carrying 'front' and 'back' text.

    Validation stops at the first problem so the user gets one clear message
    that points at a specific card.
    """
    validated: List[Flashcard] = []

    for position, card in enumerate(cards, start=1):
        if not isinstance(card, dict):
            raise FlashcardDataError(
                f"Flashcard #{position} in {path} must be an object with "
                f"'front' and 'back' fields, but it is {_json_type_name(card)}."
            )

        for field in REQUIRED_FLASHCARD_FIELDS:
            if field not in card:
                raise FlashcardDataError(
                    f"Flashcard #{position} in {path} is missing the required "
                    f"'{field}' field."
                )
            if not isinstance(card[field], str):
                raise FlashcardDataError(
                    f"The '{field}' field of flashcard #{position} in {path} "
                    f"must be text, but it is {_json_type_name(card[field])}."
                )

        validated.append(card)

    return validated


def _json_type_name(value: Any) -> str:
    """Describe a Python value using JSON vocabulary for error messages."""
    if value is None:
        return "null"
    if isinstance(value, bool):  # Checked before int: bool is a subclass of int.
        return "a boolean"
    if isinstance(value, (int, float)):
        return "a number"
    if isinstance(value, str):
        return "a string"
    if isinstance(value, list):
        return "an array"
    if isinstance(value, dict):
        return "an object"
    return f"a {type(value).__name__}"