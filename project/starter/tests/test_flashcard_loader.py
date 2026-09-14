"""
Unit tests for the Phase 1 data layer (``utils.file_handler.load_flashcard``).

The loader answers exactly one question -- "is this file a usable list of
flashcards?" -- so these tests cover the two supported input formats, the
validation rules for every card, and each way a file can fail to be read.

Every test writes its JSON into ``tmp_path``; nothing under ``data/`` is
touched, and no test needs a terminal, a network or manual input.
"""

import json
from pathlib import Path

import pytest

from utils.file_handler import (
    REQUIRED_FLASHCARD_FIELDS,
    FlashcardDataError,
    _json_type_name,
    load_flashcard,
)


@pytest.fixture
def write_json(tmp_path):
    """Return a helper that dumps a payload to a temporary JSON file."""

    def _write(payload, name="deck.json"):
        path = tmp_path / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    return _write


@pytest.fixture
def write_text(tmp_path):
    """Return a helper that writes raw (possibly invalid) text to a file."""

    def _write(text, name="deck.json"):
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        return path

    return _write


# ----------------------------------------------------------------------
# Supported formats
# ----------------------------------------------------------------------


class TestSupportedFormats:
    """Both documented layouts must normalize to the same list of cards."""

    def test_array_format_returns_cards_in_order(self, write_json):
        # Arrange
        payload = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
        ]
        path = write_json(payload)

        # Act
        cards = load_flashcard(path)

        # Assert
        assert cards == payload

    def test_object_format_unwraps_the_cards_key(self, write_json):
        # Arrange
        payload = {"cards": [{"front": "Q1", "back": "A1"}]}
        path = write_json(payload)

        # Act
        cards = load_flashcard(path)

        # Assert
        assert cards == [{"front": "Q1", "back": "A1"}]

    def test_object_format_ignores_sibling_metadata_keys(self, write_json):
        # Arrange
        payload = {"title": "Python basics", "cards": [{"front": "Q", "back": "A"}]}
        path = write_json(payload)

        # Act
        cards = load_flashcard(path)

        # Assert
        assert cards == [{"front": "Q", "back": "A"}]

    def test_extra_fields_on_a_card_are_preserved(self, write_json):
        # Arrange
        path = write_json([{"front": "Q", "back": "A", "tags": ["json"]}])

        # Act
        cards = load_flashcard(path)

        # Assert
        assert cards[0]["tags"] == ["json"]

    def test_empty_array_loads_as_an_empty_deck(self, write_json):
        # Arrange
        path = write_json([])

        # Act
        cards = load_flashcard(path)

        # Assert -- an empty deck is valid data; the CLI decides what to do.
        assert cards == []

    def test_empty_cards_list_loads_as_an_empty_deck(self, write_json):
        # Arrange
        path = write_json({"cards": []})

        # Act / Assert
        assert load_flashcard(path) == []

    def test_path_may_be_given_as_a_string(self, write_json):
        # Arrange
        path = write_json([{"front": "Q", "back": "A"}])

        # Act
        cards = load_flashcard(str(path))

        # Assert
        assert cards == [{"front": "Q", "back": "A"}]

    def test_unicode_content_is_read_as_utf8(self, tmp_path):
        # Arrange
        path = tmp_path / "deck.json"
        path.write_text(
            json.dumps([{"front": "Grüße?", "back": "Здравствуйте"}], ensure_ascii=False),
            encoding="utf-8",
        )

        # Act
        cards = load_flashcard(path)

        # Assert
        assert cards == [{"front": "Grüße?", "back": "Здравствуйте"}]


# ----------------------------------------------------------------------
# Unreadable / malformed files
# ----------------------------------------------------------------------


class TestFileLevelFailures:
    """Every read failure must surface as a friendly FlashcardDataError."""

    def test_missing_file_raises_friendly_error(self, tmp_path):
        # Arrange
        missing = tmp_path / "nope.json"

        # Act / Assert
        with pytest.raises(FlashcardDataError) as excinfo:
            load_flashcard(missing)
        assert "not found" in str(excinfo.value)
        assert str(missing) in str(excinfo.value)

    def test_directory_instead_of_file_raises_friendly_error(self, tmp_path):
        # Act / Assert
        with pytest.raises(FlashcardDataError, match="is a directory"):
            load_flashcard(tmp_path)

    def test_non_utf8_file_raises_friendly_error(self, tmp_path):
        # Arrange -- 0xFF is not a legal UTF-8 start byte.
        path = tmp_path / "deck.json"
        path.write_bytes(b"\xff\xfe[]")

        # Act / Assert
        with pytest.raises(FlashcardDataError, match="not readable as UTF-8"):
            load_flashcard(path)

    def test_malformed_json_reports_line_and_column(self, write_text):
        # Arrange -- a trailing comma, the classic hand-edit mistake.
        path = write_text('[{"front": "Q", "back": "A"},]')

        # Act / Assert
        with pytest.raises(FlashcardDataError) as excinfo:
            load_flashcard(path)
        message = str(excinfo.value)
        assert "is not valid JSON" in message
        assert "line 1" in message and "column" in message

    def test_empty_file_is_reported_as_invalid_json(self, write_text):
        # Arrange
        path = write_text("")

        # Act / Assert
        with pytest.raises(FlashcardDataError, match="is not valid JSON"):
            load_flashcard(path)

    def test_other_os_errors_use_the_system_message(self, write_json, monkeypatch):
        # Arrange -- e.g. a file the user is not allowed to read.
        path = write_json([])

        def refuse(*args, **kwargs):
            raise OSError(13, "Permission denied")

        monkeypatch.setattr("builtins.open", refuse)

        # Act / Assert
        with pytest.raises(FlashcardDataError, match="Permission denied"):
            load_flashcard(path)

    def test_os_error_without_a_system_message_still_reports_something(
        self, write_json, monkeypatch
    ):
        # Arrange -- OSError may carry no strerror at all.
        path = write_json([])

        def refuse(*args, **kwargs):
            raise OSError("device is busy")

        monkeypatch.setattr("builtins.open", refuse)

        # Act / Assert
        with pytest.raises(FlashcardDataError, match="device is busy"):
            load_flashcard(path)


# ----------------------------------------------------------------------
# Structure validation
# ----------------------------------------------------------------------


class TestStructureValidation:
    """The payload must be a list of cards or an object wrapping one."""

    def test_object_without_cards_key_is_rejected(self, write_json):
        # Arrange
        path = write_json({"deck": [{"front": "Q", "back": "A"}]})

        # Act / Assert
        with pytest.raises(FlashcardDataError, match="no 'cards' key"):
            load_flashcard(path)

    def test_cards_key_holding_a_non_list_is_rejected(self, write_json):
        # Arrange
        path = write_json({"cards": {"front": "Q", "back": "A"}})

        # Act / Assert
        with pytest.raises(FlashcardDataError) as excinfo:
            load_flashcard(path)
        assert "must be a list of flashcards" in str(excinfo.value)
        assert "an object" in str(excinfo.value)

    @pytest.mark.parametrize(
        "payload, described_as",
        [
            ("just a string", "a string"),
            (42, "a number"),
            (True, "a boolean"),
            (None, "null"),
        ],
        ids=["string", "number", "boolean", "null"],
    )
    def test_top_level_scalar_is_rejected_with_its_json_type(
        self, write_json, payload, described_as
    ):
        # Arrange
        path = write_json(payload)

        # Act / Assert
        with pytest.raises(FlashcardDataError) as excinfo:
            load_flashcard(path)
        assert described_as in str(excinfo.value)


# ----------------------------------------------------------------------
# Card validation
# ----------------------------------------------------------------------


class TestCardValidation:
    """Each entry must be an object carrying 'front' and 'back' text."""

    @pytest.mark.parametrize(
        "entry, described_as",
        [
            ("Q/A", "a string"),
            (7, "a number"),
            (False, "a boolean"),
            (None, "null"),
            ([{"front": "Q"}], "an array"),
        ],
        ids=["string", "number", "boolean", "null", "array"],
    )
    def test_non_object_card_is_rejected(self, write_json, entry, described_as):
        # Arrange
        path = write_json([entry])

        # Act / Assert
        with pytest.raises(FlashcardDataError) as excinfo:
            load_flashcard(path)
        assert "Flashcard #1" in str(excinfo.value)
        assert described_as in str(excinfo.value)

    @pytest.mark.parametrize("missing", REQUIRED_FLASHCARD_FIELDS)
    def test_missing_required_field_names_the_field(self, write_json, missing):
        # Arrange
        card = {"front": "Q", "back": "A"}
        del card[missing]
        path = write_json([card])

        # Act / Assert
        with pytest.raises(FlashcardDataError) as excinfo:
            load_flashcard(path)
        assert f"missing the required '{missing}' field" in str(excinfo.value)

    @pytest.mark.parametrize("field", REQUIRED_FLASHCARD_FIELDS)
    @pytest.mark.parametrize(
        "value, described_as",
        [(None, "null"), (12, "a number"), (["A"], "an array"), ({}, "an object")],
        ids=["null", "number", "array", "object"],
    )
    def test_non_text_required_field_is_rejected(
        self, write_json, field, value, described_as
    ):
        # Arrange
        card = {"front": "Q", "back": "A"}
        card[field] = value
        path = write_json([card])

        # Act / Assert
        with pytest.raises(FlashcardDataError) as excinfo:
            load_flashcard(path)
        assert f"The '{field}' field of flashcard #1" in str(excinfo.value)
        assert described_as in str(excinfo.value)

    def test_error_points_at_the_offending_card_position(self, write_json):
        # Arrange -- the third card is the broken one.
        path = write_json(
            [
                {"front": "Q1", "back": "A1"},
                {"front": "Q2", "back": "A2"},
                {"front": "Q3"},
            ]
        )

        # Act / Assert
        with pytest.raises(FlashcardDataError, match="Flashcard #3"):
            load_flashcard(path)

    def test_empty_strings_are_accepted_as_text(self, write_json):
        # Arrange -- the loader validates types, not editorial quality.
        path = write_json([{"front": "", "back": ""}])

        # Act / Assert
        assert load_flashcard(path) == [{"front": "", "back": ""}]

    def test_object_format_validates_its_cards_too(self, write_json):
        # Arrange
        path = write_json({"cards": [{"front": "Q", "back": 1}]})

        # Act / Assert
        with pytest.raises(FlashcardDataError, match="must be text"):
            load_flashcard(path)


# ----------------------------------------------------------------------
# Error-message helper
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, "null"),
        (True, "a boolean"),
        (False, "a boolean"),
        (3, "a number"),
        (3.5, "a number"),
        ("text", "a string"),
        ([], "an array"),
        ({}, "an object"),
        ({1, 2}, "a set"),  # Not JSON, but the helper still degrades gracefully.
    ],
    ids=["null", "true", "false", "int", "float", "str", "list", "dict", "set"],
)
def test_json_type_name_describes_values_in_json_vocabulary(value, expected):
    # Act / Assert
    assert _json_type_name(value) == expected


# ----------------------------------------------------------------------
# The decks shipped with the project
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "deck_name", ["flashcards.json", "flashcards_array.json", "python_basics.json"]
)
def test_bundled_sample_decks_load(deck_name):
    """The sample data has to stay loadable; it is read, never modified."""
    # Arrange
    deck_path = Path(__file__).resolve().parent.parent / "data" / deck_name

    # Act
    cards = load_flashcard(deck_path)

    # Assert
    assert cards
    assert all({"front", "back"} <= card.keys() for card in cards)
