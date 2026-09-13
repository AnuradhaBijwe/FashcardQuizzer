"""
Command-line entry point for the Flashcard Quizzer.

This module is the application's orchestration layer and owns nothing else:

* it parses command-line arguments with :mod:`argparse`,
* it asks the Phase 1 data layer (:mod:`utils.file_handler`) for a deck,
* it asks the Phase 2 factory (:mod:`utils.quiz_engine`) for a quiz mode,
* it runs the question/answer loop and reports the outcome.

JSON parsing, validation and card ordering deliberately stay in their own
modules. The only thing that happens here and nowhere else is talking to the
user: prompting, comparing the typed answer with the card, colouring the
result and printing the final statistics.

Usage::

    python main.py -f data/python_basics.json
    python main.py -m random -f data/flashcards.json
    python main.py -m adaptive -f data/python_basics.json --stats
"""

import argparse
import sys
from typing import Optional, Sequence

from utils.console import Palette
from utils.file_handler import Flashcard, FlashcardDataError, load_flashcard
from utils.quiz_engine import (
    QuizMode,
    QuizModeFactory,
    QuizStats,
    UnknownQuizModeError,
)

#: Words that end the session instead of being graded as an answer.
EXIT_COMMANDS = frozenset({"exit", "quit"})

#: Mode used when the user does not pass ``-m/--mode``.
DEFAULT_MODE = "sequential"

#: Process exit codes. Argparse already uses 2 for bad usage.
EXIT_OK = 0
EXIT_ERROR = 1

SEPARATOR = "-" * 50


class QuizAborted(Exception):
    """
    Raised internally when the user asks to stop the quiz.

    Using an exception lets the prompt abandon the current card from wherever
    it is, which matters because a card the user walked away from must not be
    recorded as a wrong answer.
    """


# ----------------------------------------------------------------------
# Command-line interface
# ----------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """
    Describe the command-line interface.

    Mode names are intentionally *not* restricted with ``choices`` so that an
    unsupported mode is reported by the Phase 2 factory, which owns the list
    of modes and already produces a friendly message.
    """
    parser = argparse.ArgumentParser(
        prog="flashcard-quizzer",
        description="Practise a deck of flashcards from the terminal.",
        epilog="Type 'exit' or press Ctrl+C at any prompt to stop early.",
    )
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        metavar="PATH",
        help="Path to the JSON flashcard file.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        default=DEFAULT_MODE,
        metavar="MODE",
        help=(
            "Quiz mode: "
            + ", ".join(QuizModeFactory.available_modes())
            + f" (default: {DEFAULT_MODE})."
        ),
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show quiz statistics when the session ends.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """
    Run one quiz session end to end.

    Args:
        argv: Argument list to parse. Defaults to ``sys.argv[1:]``.

    Returns:
        A process exit code: ``0`` on success or a user-requested exit,
        ``1`` when the deck or the mode could not be used.
    """
    args = build_parser().parse_args(argv)
    palette = Palette.for_stream(sys.stdout)

    try:
        cards = load_flashcard(args.file)
        quiz = QuizModeFactory.create(args.mode, cards)
    except (FlashcardDataError, UnknownQuizModeError, ValueError) as error:
        # These carry end-user wording already; never surface a traceback.
        print(palette.red(f"Error: {error}"), file=sys.stderr)
        return EXIT_ERROR

    if not cards:
        message = f"Error: {args.file} contains no flashcards."
        print(palette.red(message), file=sys.stderr)
        return EXIT_ERROR

    print_intro(quiz, args.file, palette)

    try:
        run_quiz(quiz, palette)
    except (QuizAborted, KeyboardInterrupt):
        # Ctrl+C arrives mid-prompt, so start the message on a fresh line.
        print()
        print(palette.dim("Quiz ended by user. See you next time!"))
    else:
        print()
        print(palette.bold("Quiz complete. Nice work!"))

    if args.stats:
        print_stats(quiz.stats, palette)

    return EXIT_OK


# ----------------------------------------------------------------------
# Quiz loop
# ----------------------------------------------------------------------


def run_quiz(quiz: QuizMode, palette: Palette) -> None:
    """
    Ask every card the mode serves, feeding each result back to the mode.

    The loop is identical for all three modes: that is the point of the
    Strategy pattern. Adaptive re-queueing happens inside
    :meth:`QuizMode.record_answer`, so no ordering logic is repeated here.

    Raises:
        QuizAborted: If the user asks to stop.
    """
    while quiz.has_next():
        card = quiz.next_card()
        if card is None:  # Defensive: has_next() should already rule this out.
            break
        was_correct = ask_card(card, quiz.stats.asked, palette)
        quiz.record_answer(card, was_correct)


def ask_card(card: Flashcard, number: int, palette: Palette) -> bool:
    """
    Show one card, read an answer and report the verdict immediately.

    Args:
        card: The flashcard to ask.
        number: 1-based position in the session, shown to the user.
        palette: Colour helper for the verdict lines.

    Returns:
        ``True`` if the typed answer matched the card's ``back`` value.

    Raises:
        QuizAborted: If the user asks to stop instead of answering.
    """
    expected = card["back"]

    print()
    print(palette.bold(f"Question {number}: {card['front']}"))
    answer = read_answer("Your answer: ")

    if is_correct(answer, expected):
        print(palette.green("Correct!"))
        return True

    print(palette.red("Incorrect."))
    print(f"Correct answer: {palette.green(expected)}")
    return False


def read_answer(prompt: str) -> str:
    """
    Read one line from the user, treating exit words as a request to stop.

    ``Ctrl+D`` (or a closed stdin when input is piped) is handled the same way
    as typing ``exit``, so the CLI never dies on an :class:`EOFError`.

    Raises:
        QuizAborted: If the user typed an exit word or closed the input.
    """
    try:
        answer = input(prompt)
    except EOFError:
        raise QuizAborted from None

    if answer.strip().casefold() in EXIT_COMMANDS:
        raise QuizAborted

    return answer


# ----------------------------------------------------------------------
# Answer checking
# ----------------------------------------------------------------------


def is_correct(user_answer: str, expected_answer: str) -> bool:
    """
    Compare a typed answer with the card's answer, forgivingly.

    Surrounding and repeated whitespace is ignored and the comparison is
    case-insensitive, so ``"  The JSON module "`` matches ``"the json
    module"``. Everything else -- wording, punctuation, spelling -- still has
    to match, which keeps the check predictable.
    """
    return normalize_answer(user_answer) == normalize_answer(expected_answer)


def normalize_answer(text: str) -> str:
    """Reduce an answer to the form used for comparison."""
    # str.split() with no argument strips the ends and collapses runs of any
    # whitespace, including tabs; casefold() is the Unicode-aware lower().
    return " ".join(text.split()).casefold()


# ----------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------


def print_intro(quiz: QuizMode, file_path: str, palette: Palette) -> None:
    """Announce the deck and remind the user how to leave."""
    card_count = len(quiz.cards)
    noun = "card" if card_count == 1 else "cards"

    print(palette.bold("Flashcard Quizzer"))
    print(SEPARATOR)
    print(f"Deck:  {file_path} ({card_count} {noun})")
    print(f"Mode:  {type(quiz).name}")
    print(palette.dim("Type 'exit' or press Ctrl+C to stop at any time."))
    print(SEPARATOR)


def print_stats(stats: QuizStats, palette: Palette) -> None:
    """
    Print the end-of-session summary.

    The percentage comes from :attr:`QuizStats.accuracy`, which already
    returns ``0.0`` when nothing was answered, so quitting at the first
    question cannot divide by zero.
    """
    print()
    print(palette.bold("Quiz Statistics"))
    print(SEPARATOR)
    print(f"Total Answered: {stats.answered}")
    print(f"Correct: {palette.green(str(stats.correct))}")
    print(f"Incorrect: {palette.red(str(stats.incorrect))}")

    if stats.answered:
        print(f"Score: {stats.accuracy * 100:.1f}%")
    else:
        print("Score: n/a (no questions answered)")


if __name__ == "__main__":
    sys.exit(main())
