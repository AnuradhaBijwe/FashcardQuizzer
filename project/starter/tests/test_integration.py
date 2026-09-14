"""
Integration tests for the Flashcard Quizzer.

The other test modules each look at one layer in isolation. These tests drive
the whole application the way a user does -- ``main.main(argv)`` with a real
JSON file on disk and a scripted stdin -- so they cover the seams between the
layers rather than the layers themselves:

* the CLI hands a path to the Phase 1 data layer and a mode name to the
  Phase 2 factory,
* the chosen strategy decides the order in which cards come back,
* the answer the user types is graded and fed to :meth:`QuizMode.record_answer`,
* the outcome reaches the screen as output, statistics and an exit code.

Every test writes its deck into ``tmp_path`` (except the ones that
deliberately read the bundled decks, which they never modify), replaces
``sys.stdin`` with a scripted script of answers, and captures stdout and
stderr into buffers. Nothing here needs a terminal, a network or a human.
"""

import io
import json
import re
import sys
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Sequence

import pytest

import main
from utils.quiz_engine import DEFAULT_MAX_RETRIES, QuizModeFactory

#: Matches the line the CLI prints for each question, capturing the card front.
QUESTION_LINE = re.compile(r"^Question (\d+): (.*)$", re.MULTILINE)

#: Any ANSI escape sequence. Piped output must contain none of these.
ANSI_ESCAPE = re.compile(r"\033\[")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

#: A small deck used by most tests: short answers keep the scripts readable.
DECK: List[dict] = [
    {"front": "Which keyword defines a function?", "back": "def"},
    {"front": "Which keyword exits a loop early?", "back": "break"},
    {"front": "Which keyword creates a class?", "back": "class"},
]

FRONTS = [card["front"] for card in DECK]
BACKS = [card["back"] for card in DECK]


# ----------------------------------------------------------------------
# Harness
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class CliRun:
    """Everything one CLI session produced, ready to assert against."""

    exit_code: Optional[int]
    stdout: str
    stderr: str

    @property
    def questions(self) -> List[str]:
        """The card fronts that were actually asked, in the order asked."""
        return [match.group(2) for match in QUESTION_LINE.finditer(self.stdout)]

    @property
    def question_numbers(self) -> List[int]:
        """The 1-based counter shown next to each question."""
        return [int(match.group(1)) for match in QUESTION_LINE.finditer(self.stdout)]

    @property
    def output(self) -> str:
        """Both streams together, for assertions that do not care which."""
        return self.stdout + self.stderr


@pytest.fixture
def run_cli(monkeypatch):
    """
    Return a helper that runs one full CLI session and captures the result.

    Answers are fed through ``sys.stdin`` rather than by patching ``input()``,
    so running out of answers reaches the CLI as a real :class:`EOFError` --
    the same thing that happens when input is piped from a short file.

    ``SystemExit`` (argparse's way of rejecting bad usage) is caught and
    reported as the run's exit code so that its message stays captured too.
    """

    def _run(
        argv: Sequence[str],
        answers: Iterable[str] = (),
        *,
        fake_input: Optional[Callable[..., str]] = None,
    ) -> CliRun:
        if fake_input is not None:
            # Used for conditions stdin cannot express, such as Ctrl+C.
            monkeypatch.setattr("builtins.input", fake_input)
        else:
            script = "".join(f"{answer}\n" for answer in answers)
            monkeypatch.setattr(sys, "stdin", io.StringIO(script))

        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            try:
                exit_code: Optional[int] = main.main(list(argv))
            except SystemExit as exit_request:  # argparse usage errors
                code = exit_request.code
                exit_code = code if isinstance(code, int) or code is None else 1

        return CliRun(exit_code=exit_code, stdout=out.getvalue(), stderr=err.getvalue())

    return _run


@pytest.fixture
def deck_file(tmp_path):
    """Return a helper that writes a deck to a temporary JSON file."""

    def _write(payload=None, name="deck.json") -> Path:
        path = tmp_path / name
        content = DECK if payload is None else payload
        path.write_text(json.dumps(content), encoding="utf-8")
        return path

    return _write


@pytest.fixture
def raw_file(tmp_path):
    """Return a helper that writes raw (possibly invalid) text to a file."""

    def _write(text: str, name="deck.json") -> Path:
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        return path

    return _write


# ----------------------------------------------------------------------
# A complete session, end to end
# ----------------------------------------------------------------------


class TestCompleteSession:
    """The default run: one file, one mode, every card asked once."""

    def test_every_card_is_asked_once_in_deck_order(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        # Act
        run = run_cli(["-f", str(path)], BACKS)

        # Assert
        assert run.exit_code == main.EXIT_OK
        assert run.questions == FRONTS
        assert run.question_numbers == [1, 2, 3]

    def test_correct_answers_are_confirmed_and_the_session_completes(
        self, run_cli, deck_file
    ):
        # Arrange
        path = deck_file()

        # Act
        run = run_cli(["-f", str(path)], BACKS)

        # Assert
        assert run.stdout.count("Correct!") == len(DECK)
        assert "Incorrect." not in run.stdout
        assert "Quiz complete. Nice work!" in run.stdout

    def test_a_wrong_answer_reveals_the_expected_one(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        # Act -- miss the first card, then answer the rest correctly.
        run = run_cli(["-f", str(path)], ["loop", *BACKS[1:]])

        # Assert
        assert "Incorrect." in run.stdout
        assert f"Correct answer: {BACKS[0]}" in run.stdout

    def test_the_intro_names_the_deck_the_count_and_the_mode(
        self, run_cli, deck_file
    ):
        # Arrange
        path = deck_file()

        # Act
        run = run_cli(["-f", str(path)], BACKS)

        # Assert
        assert f"Deck:  {path} ({len(DECK)} cards)" in run.stdout
        assert "Mode:  sequential" in run.stdout
        assert "Type 'exit' or press Ctrl+C to stop at any time." in run.stdout

    def test_a_one_card_deck_is_announced_in_the_singular(self, run_cli, deck_file):
        # Arrange
        path = deck_file([DECK[0]])

        # Act
        run = run_cli(["-f", str(path)], [BACKS[0]])

        # Assert
        assert "(1 card)" in run.stdout

    def test_nothing_is_written_to_stderr_on_a_successful_run(
        self, run_cli, deck_file
    ):
        # Arrange
        path = deck_file()

        # Act
        run = run_cli(["-f", str(path)], BACKS)

        # Assert
        assert run.stderr == ""

    def test_piped_output_carries_no_ansi_escape_codes(self, run_cli, deck_file):
        # Arrange -- the captured streams are buffers, not terminals.
        path = deck_file()

        # Act
        run = run_cli(["-f", str(path)], ["wrong", *BACKS[1:]])

        # Assert -- colour must degrade to plain text, verdicts included.
        assert not ANSI_ESCAPE.search(run.output)

    def test_the_deck_file_is_never_modified(self, run_cli, deck_file):
        # Arrange
        path = deck_file()
        before = path.read_bytes()

        # Act
        run_cli(["-f", str(path)], ["wrong", *BACKS[1:]])

        # Assert -- the data layer reads; nothing downstream writes back.
        assert path.read_bytes() == before


# ----------------------------------------------------------------------
# Grading rules seen from the outside
# ----------------------------------------------------------------------


class TestAnswerGrading:
    """How forgiving the CLI is about the exact text the user types."""

    @pytest.mark.parametrize(
        "typed",
        ["def", "DEF", "  def  ", "Def"],
        ids=["exact", "uppercase", "padded", "mixed-case"],
    )
    def test_case_and_surrounding_whitespace_are_ignored(
        self, run_cli, deck_file, typed
    ):
        # Arrange
        path = deck_file([DECK[0]])

        # Act
        run = run_cli(["-f", str(path), "--stats"], [typed])

        # Assert
        assert "Correct!" in run.stdout
        assert "Correct: 1" in run.stdout

    def test_repeated_whitespace_inside_an_answer_is_collapsed(
        self, run_cli, deck_file
    ):
        # Arrange
        path = deck_file(
            [{"front": "Which module parses JSON?", "back": "the json module"}]
        )

        # Act
        run = run_cli(["-f", str(path)], ["the   json\tmodule"])

        # Assert
        assert "Correct!" in run.stdout

    def test_a_different_wording_is_still_wrong(self, run_cli, deck_file):
        # Arrange
        path = deck_file([DECK[0]])

        # Act
        run = run_cli(["-f", str(path), "--stats"], ["define"])

        # Assert
        assert "Incorrect." in run.stdout
        assert "Incorrect: 1" in run.stdout

    def test_an_empty_answer_counts_as_wrong(self, run_cli, deck_file):
        # Arrange
        path = deck_file([DECK[0]])

        # Act -- the user just pressed Enter.
        run = run_cli(["-f", str(path), "--stats"], [""])

        # Assert
        assert "Incorrect." in run.stdout
        assert "Total Answered: 1" in run.stdout


# ----------------------------------------------------------------------
# Mode selection
# ----------------------------------------------------------------------


class TestModeSelection:
    """``-m`` reaches the factory, and each strategy behaves as advertised."""

    def test_sequential_is_the_default_mode(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        # Act
        run = run_cli(["-f", str(path)], BACKS)

        # Assert
        assert f"Mode:  {main.DEFAULT_MODE}" in run.stdout
        assert run.questions == FRONTS

    def test_random_mode_asks_every_card_exactly_once(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        # Act -- the order is unpredictable, so answer every card wrongly.
        run = run_cli(["-m", "random", "-f", str(path)], ["x"] * len(DECK))

        # Assert -- a shuffle, not a resample: each front appears once.
        assert run.exit_code == main.EXIT_OK
        assert sorted(run.questions) == sorted(FRONTS)

    def test_adaptive_mode_brings_a_missed_card_back(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        # Act -- miss the first card, then answer everything correctly.
        run = run_cli(
            ["-m", "adaptive", "-f", str(path), "--stats"],
            ["not this", *BACKS[1:], BACKS[0]],
        )

        # Assert -- the missed card returns after the rest of the deck.
        assert run.questions == [*FRONTS, FRONTS[0]]
        assert "Total Answered: 4" in run.stdout
        assert "Correct: 3" in run.stdout

    def test_adaptive_mode_gives_up_after_the_retry_limit(self, run_cli, deck_file):
        # Arrange -- one card, answered wrongly every single time.
        path = deck_file([DECK[0]])
        attempts = DEFAULT_MAX_RETRIES + 1

        # Act
        run = run_cli(
            ["-m", "adaptive", "-f", str(path), "--stats"], ["wrong"] * attempts
        )

        # Assert -- the session ends on its own instead of looping forever.
        assert run.exit_code == main.EXIT_OK
        assert len(run.questions) == attempts
        assert "Quiz complete. Nice work!" in run.stdout
        assert f"Total Answered: {attempts}" in run.stdout
        assert "Score: 0.0%" in run.stdout

    def test_a_correct_answer_is_never_re_queued(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        # Act
        run = run_cli(["-m", "adaptive", "-f", str(path)], BACKS)

        # Assert
        assert run.questions == FRONTS

    @pytest.mark.parametrize(
        "requested", ["SEQUENTIAL", " sequential ", "Sequencial"],
        ids=["uppercase", "padded", "common-misspelling"],
    )
    def test_mode_names_are_normalized_before_the_factory_sees_them(
        self, run_cli, deck_file, requested
    ):
        # Arrange
        path = deck_file()

        # Act
        run = run_cli(["-m", requested, "-f", str(path)], BACKS)

        # Assert
        assert run.exit_code == main.EXIT_OK
        assert run.questions == FRONTS

    def test_the_help_text_lists_the_modes_the_factory_supports(self, run_cli):
        # Act
        run = run_cli(["--help"])

        # Assert -- the CLI never hard-codes its own copy of the mode list.
        for mode in QuizModeFactory.available_modes():
            assert mode in run.stdout

    def test_an_unknown_mode_is_rejected_before_any_question(
        self, run_cli, deck_file
    ):
        # Arrange
        path = deck_file()

        # Act
        run = run_cli(["-m", "spaced-repetition", "-f", str(path)], BACKS)

        # Assert
        assert run.exit_code == main.EXIT_ERROR
        assert "Unknown quiz mode" in run.stderr
        assert "sequential" in run.stderr
        assert run.questions == []


# ----------------------------------------------------------------------
# Leaving early
# ----------------------------------------------------------------------


class TestEarlyExit:
    """Stopping mid-deck is a normal outcome, not an error."""

    @pytest.mark.parametrize(
        "word", ["exit", "quit", "EXIT", "  Quit  "],
        ids=["exit", "quit", "uppercase", "padded"],
    )
    def test_an_exit_word_ends_the_session_cleanly(self, run_cli, deck_file, word):
        # Arrange -- a spare answer follows, so a word that failed to be
        # recognised as "stop" would be graded and the quiz would carry on.
        path = deck_file()

        # Act
        run = run_cli(["-f", str(path), "--stats"], [word, BACKS[1]])

        # Assert
        assert run.exit_code == main.EXIT_OK
        assert "Quiz ended by user. See you next time!" in run.stdout
        assert "Quiz complete" not in run.stdout

        # ...and the word was treated as a request to leave, not as an answer.
        assert run.questions == FRONTS[:1]
        assert "Incorrect." not in run.stdout
        assert "Total Answered: 0" in run.stdout

    def test_the_abandoned_card_is_not_graded(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        # Act -- answer the first card, then walk away from the second.
        run = run_cli(["-f", str(path), "--stats"], [BACKS[0], "exit"])

        # Assert -- two cards were shown, but only one was answered.
        assert len(run.questions) == 2
        assert "Total Answered: 1" in run.stdout
        assert "Correct: 1" in run.stdout
        assert "Incorrect: 0" in run.stdout

    def test_the_remaining_cards_are_not_asked(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        # Act
        run = run_cli(["-f", str(path)], ["exit"])

        # Assert
        assert run.questions == FRONTS[:1]

    def test_exhausted_input_ends_the_session_like_ctrl_d(
        self, run_cli, deck_file
    ):
        # Arrange -- fewer answers than cards, as when input is piped in.
        path = deck_file()

        # Act
        run = run_cli(["-f", str(path), "--stats"], [BACKS[0]])

        # Assert
        assert run.exit_code == main.EXIT_OK
        assert "Quiz ended by user. See you next time!" in run.stdout
        assert "Total Answered: 1" in run.stdout

    def test_ctrl_c_ends_the_session_without_a_traceback(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        def interrupt(prompt: str = "") -> str:
            raise KeyboardInterrupt

        # Act
        run = run_cli(["-f", str(path)], fake_input=interrupt)

        # Assert
        assert run.exit_code == main.EXIT_OK
        assert "Quiz ended by user. See you next time!" in run.stdout
        assert "Traceback" not in run.output

    def test_statistics_still_print_after_an_early_exit(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        # Act -- quit at the very first question.
        run = run_cli(["-f", str(path), "--stats"], ["exit"])

        # Assert -- an unanswered session must not divide by zero.
        assert "Total Answered: 0" in run.stdout
        assert "Score: n/a (no questions answered)" in run.stdout


# ----------------------------------------------------------------------
# Statistics
# ----------------------------------------------------------------------


class TestStatistics:
    """``--stats`` summarises what the session actually recorded."""

    def test_statistics_are_hidden_unless_requested(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        # Act
        run = run_cli(["-f", str(path)], BACKS)

        # Assert
        assert "Quiz Statistics" not in run.stdout

    def test_totals_and_accuracy_reflect_the_answers_given(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        # Act -- two right, one wrong.
        run = run_cli(["-f", str(path), "--stats"], [BACKS[0], "nope", BACKS[2]])

        # Assert
        assert "Quiz Statistics" in run.stdout
        assert "Total Answered: 3" in run.stdout
        assert "Correct: 2" in run.stdout
        assert "Incorrect: 1" in run.stdout
        assert "Score: 66.7%" in run.stdout

    def test_a_perfect_session_scores_one_hundred_percent(self, run_cli, deck_file):
        # Arrange
        path = deck_file()

        # Act
        run = run_cli(["-f", str(path), "--stats"], BACKS)

        # Assert
        assert "Score: 100.0%" in run.stdout

    def test_statistics_count_adaptive_repeats_as_separate_answers(
        self, run_cli, deck_file
    ):
        # Arrange
        path = deck_file([DECK[0]])

        # Act -- miss the card, then get it right on the retry.
        run = run_cli(
            ["-m", "adaptive", "-f", str(path), "--stats"], ["wrong", BACKS[0]]
        )

        # Assert
        assert "Total Answered: 2" in run.stdout
        assert "Score: 50.0%" in run.stdout


# ----------------------------------------------------------------------
# Bad input reaching the CLI
# ----------------------------------------------------------------------


class TestFailureModes:
    """Data-layer problems must surface as a message and exit code 1."""

    def test_a_missing_file_is_reported_without_a_traceback(
        self, run_cli, tmp_path
    ):
        # Arrange
        missing = tmp_path / "nope.json"

        # Act
        run = run_cli(["-f", str(missing)])

        # Assert
        assert run.exit_code == main.EXIT_ERROR
        assert "not found" in run.stderr
        assert "Traceback" not in run.output
        assert run.stdout == ""

    def test_malformed_json_is_reported_with_its_location(self, run_cli, raw_file):
        # Arrange -- a trailing comma, the classic hand-edit mistake.
        path = raw_file('[{"front": "Q", "back": "A"},]')

        # Act
        run = run_cli(["-f", str(path)])

        # Assert
        assert run.exit_code == main.EXIT_ERROR
        assert "is not valid JSON" in run.stderr
        assert "line 1" in run.stderr

    def test_an_invalid_card_names_its_position(self, run_cli, deck_file):
        # Arrange -- the second card is missing its answer.
        path = deck_file([DECK[0], {"front": "Half a card"}])

        # Act
        run = run_cli(["-f", str(path)])

        # Assert
        assert run.exit_code == main.EXIT_ERROR
        assert "Flashcard #2" in run.stderr
        assert "missing the required 'back' field" in run.stderr

    @pytest.mark.parametrize(
        "field", ["front", "back"], ids=["question", "answer"]
    )
    def test_a_non_text_field_is_refused_instead_of_crashing_the_quiz(
        self, run_cli, deck_file, field
    ):
        # Arrange -- a number where text belongs; the answer comparison would
        # raise AttributeError if this ever reached the quiz loop.
        card = dict(DECK[0])
        card[field] = 42
        path = deck_file([card])

        # Act
        run = run_cli(["-f", str(path)], ["42"])

        # Assert
        assert run.exit_code == main.EXIT_ERROR
        assert f"The '{field}' field of flashcard #1" in run.stderr
        assert "must be text" in run.stderr
        assert run.questions == []

    @pytest.mark.parametrize(
        "payload", [[], {"cards": []}], ids=["array-format", "object-format"]
    )
    def test_an_empty_deck_is_refused_before_the_quiz_starts(
        self, run_cli, deck_file, payload
    ):
        # Arrange -- valid JSON, but nothing to practise.
        path = deck_file(payload)

        # Act
        run = run_cli(["-f", str(path)])

        # Assert
        assert run.exit_code == main.EXIT_ERROR
        assert "contains no flashcards" in run.stderr
        assert "Flashcard Quizzer" not in run.stdout

    def test_an_unsupported_structure_is_refused(self, run_cli, deck_file):
        # Arrange
        path = deck_file({"deck": [{"front": "Q", "back": "A"}]})

        # Act
        run = run_cli(["-f", str(path)])

        # Assert
        assert run.exit_code == main.EXIT_ERROR
        assert "no 'cards' key" in run.stderr

    def test_a_missing_file_argument_is_a_usage_error(self, run_cli):
        # Act -- argparse rejects this before any of our code runs.
        run = run_cli([])

        # Assert
        assert run.exit_code == 2
        assert "-f/--file" in run.stderr

    def test_errors_go_to_stderr_so_stdout_stays_pipeable(
        self, run_cli, tmp_path
    ):
        # Arrange
        missing = tmp_path / "nope.json"

        # Act
        run = run_cli(["-f", str(missing)])

        # Assert
        assert "Error:" in run.stderr
        assert "Error:" not in run.stdout


# ----------------------------------------------------------------------
# Real files on disk
# ----------------------------------------------------------------------


class TestBundledDecks:
    """The sample decks have to work through the CLI, not just the loader."""

    @pytest.mark.parametrize(
        "deck_name",
        ["flashcards.json", "flashcards_array.json", "python_basics.json"],
        ids=["object-format", "array-format", "python-basics"],
    )
    def test_a_bundled_deck_can_be_answered_perfectly(self, run_cli, deck_name):
        # Arrange -- read the expected answers straight from the file.
        path = DATA_DIR / deck_name
        payload = json.loads(path.read_text(encoding="utf-8"))
        cards = payload["cards"] if isinstance(payload, dict) else payload
        answers = [card["back"] for card in cards]

        # Act
        run = run_cli(["-f", str(path), "--stats"], answers)

        # Assert
        assert run.exit_code == main.EXIT_OK
        assert run.questions == [card["front"] for card in cards]
        assert run.stdout.count("Correct!") == len(cards)
        assert "Score: 100.0%" in run.stdout

    def test_a_bundled_deck_runs_in_every_mode(self, run_cli):
        # Arrange
        path = DATA_DIR / "python_basics.json"
        card_count = len(json.loads(path.read_text(encoding="utf-8"))["cards"])

        for mode in QuizModeFactory.available_modes():
            # Act -- wrong answers keep this independent of the card order.
            run = run_cli(["-m", mode, "-f", str(path)], ["?"] * card_count)

            # Assert -- adaptive may still have retries queued, and running
            # out of answers is the documented way to stop; either ending is
            # a clean exit.
            assert run.exit_code == main.EXIT_OK, mode
            assert len(run.questions) >= card_count, mode
