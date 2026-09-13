"""
Quiz engine for the Flashcard Quizzer.

This module owns the *ordering* half of the application: given a deck of
flashcards already loaded and validated by :mod:`utils.file_handler`, it
decides which card to serve next and how to react to each answer.

Two patterns carry the design:

* **Strategy** -- :class:`QuizMode` defines a single interface for serving
  cards. :class:`SequentialMode`, :class:`RandomMode` and
  :class:`AdaptiveMode` implement that interface differently, so the calling
  code runs one loop no matter which mode is active.
* **Factory** -- :class:`QuizModeFactory` turns a mode name into the matching
  strategy, so callers never import the concrete classes directly.

The strategies are deliberately free of I/O: no ``input()``, no ``print()``.
The CLI asks the question, then reports the outcome back through
:meth:`QuizMode.record_answer`.
"""

import random
from abc import ABC, abstractmethod
from collections import Counter, deque
from dataclasses import dataclass
from typing import ClassVar, Deque, Dict, Iterable, List, Optional, Sequence, Tuple, Type

from utils.file_handler import Flashcard

# How many cards should pass before a missed card comes back around, and how
# many times a single card may be retried before the engine lets it go.
DEFAULT_RETRY_GAP = 2
DEFAULT_MAX_RETRIES = 2


class UnknownQuizModeError(ValueError):
    """
    Raised when an unsupported quiz mode name is requested.

    Subclasses :class:`ValueError`, so callers may catch either type. The
    message lists the supported modes and is safe to show to the user.
    """


@dataclass(frozen=True)
class QuizStats:
    """Immutable snapshot of how a session is going."""

    asked: int
    correct: int
    incorrect: int

    @property
    def answered(self) -> int:
        """Number of cards the user actually answered."""
        return self.correct + self.incorrect

    @property
    def accuracy(self) -> float:
        """Share of answers that were correct, in the range 0.0 - 1.0."""
        return self.correct / self.answered if self.answered else 0.0


class QuizMode(ABC):
    """
    Strategy interface: decides the order in which flashcards are served.

    Subclasses supply the ordering by implementing :meth:`_build_queue`, and
    may react to answers by overriding :meth:`_on_answer`. Everything else --
    serving cards, counting results, tracking missed cards -- is handled here
    once, so the concrete modes stay small.

    The deck passed in is never mutated; the queue holds positions into a
    private copy of the original list.
    """

    #: Name the factory registers this mode under.
    name: ClassVar[str] = ""

    def __init__(self, cards: Sequence[Flashcard] = ()) -> None:
        self._cards: Tuple[Flashcard, ...] = tuple(cards)
        # Identity lookup so record_answer() can tell which card came back.
        self._positions: Dict[int, int] = {
            id(card): position for position, card in enumerate(self._cards)
        }
        self._queue: Deque[int] = deque()
        self._prepared = False
        self._asked = 0
        self._correct = 0
        self._incorrect = 0
        self._misses: Counter = Counter()  # position -> wrong answers so far

    def __repr__(self) -> str:
        return f"{type(self).__name__}(cards={len(self._cards)})"

    # ------------------------------------------------------------------
    # Interface used by the CLI
    # ------------------------------------------------------------------

    def prepare(self) -> None:
        """
        Build the serving order, discarding any progress so far.

        Called automatically the first time a card is requested, so the CLI
        only needs this to restart a session.
        """
        self._queue = deque(self._build_queue())
        self._prepared = True

    def has_next(self) -> bool:
        """Report whether another card is waiting to be served."""
        self._ensure_prepared()
        return bool(self._queue)

    def next_card(self) -> Optional[Flashcard]:
        """
        Serve the next flashcard, or ``None`` once the session is finished.

        Returns:
            The next card to ask, still owned by the caller's deck.
        """
        self._ensure_prepared()
        if not self._queue:
            return None
        self._asked += 1
        return self._cards[self._queue.popleft()]

    def record_answer(self, card: Flashcard, is_correct: bool) -> None:
        """
        Record the outcome of one answer.

        Counting happens here for every mode; modes that change their plan in
        response -- :class:`AdaptiveMode` -- do so in :meth:`_on_answer`.

        Args:
            card: The card that was just asked, as returned by
                :meth:`next_card`.
            is_correct: Whether the user answered it correctly.

        Raises:
            ValueError: If the card is not part of this session's deck.
        """
        position = self._position_of(card)
        if is_correct:
            self._correct += 1
        else:
            self._incorrect += 1
            self._misses[position] += 1
        self._on_answer(position, is_correct)

    @property
    def cards(self) -> Tuple[Flashcard, ...]:
        """The deck in its original order."""
        return self._cards

    @property
    def remaining(self) -> int:
        """How many cards are still queued, including adaptive retries."""
        self._ensure_prepared()
        return len(self._queue)

    @property
    def stats(self) -> QuizStats:
        """A snapshot of the session's progress."""
        return QuizStats(
            asked=self._asked, correct=self._correct, incorrect=self._incorrect
        )

    @property
    def missed_cards(self) -> List[Flashcard]:
        """Cards answered incorrectly at least once, worst first."""
        ranked = sorted(
            self._misses.items(), key=lambda item: (-item[1], item[0])
        )
        return [self._cards[position] for position, _ in ranked]

    # ------------------------------------------------------------------
    # Extension points for concrete modes
    # ------------------------------------------------------------------

    @abstractmethod
    def _build_queue(self) -> Iterable[int]:
        """
        Return the initial serving order as positions into :attr:`cards`.

        This is the one method every mode must supply.
        """

    def _on_answer(self, position: int, is_correct: bool) -> None:
        """
        React to an answer. The default is to do nothing.

        Modes with a fixed order leave this alone; adaptive modes override it
        to re-queue cards.
        """

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _ensure_prepared(self) -> None:
        """Build the queue on first use so subclass setup can finish first."""
        if not self._prepared:
            self.prepare()

    def _position_of(self, card: Flashcard) -> int:
        """Find a card's position in the deck, by identity."""
        try:
            return self._positions[id(card)]
        except KeyError:
            raise ValueError(
                "That flashcard is not part of this quiz session. Pass back "
                "the card returned by next_card()."
            ) from None


class SequentialMode(QuizMode):
    """Serve every card once, in the order the deck was written."""

    name = "sequential"

    def _build_queue(self) -> Iterable[int]:
        """Walk the deck front to back."""
        return range(len(self._cards))


class RandomMode(QuizMode):
    """
    Serve every card once, in a shuffled order.

    The shuffle works on a list of positions, so the caller's deck is left
    exactly as it was. A :class:`random.Random` instance can be injected to
    make the order reproducible in tests.
    """

    name = "random"

    def __init__(
        self,
        cards: Sequence[Flashcard] = (),
        rng: Optional[random.Random] = None,
    ) -> None:
        super().__init__(cards)
        self._rng = rng if rng is not None else random.Random()

    def _build_queue(self) -> Iterable[int]:
        """Shuffle the positions, never the deck itself."""
        order = list(range(len(self._cards)))
        self._rng.shuffle(order)
        return order


class AdaptiveMode(QuizMode):
    """
    Serve every card once, then bring missed cards back for another try.

    A card answered incorrectly is re-inserted ``retry_gap`` places further
    down the queue, so the user sees a couple of other cards before meeting it
    again. Each card is retried at most ``max_retries`` times, which
    guarantees the session ends even if every answer is wrong.
    """

    name = "adaptive"

    def __init__(
        self,
        cards: Sequence[Flashcard] = (),
        retry_gap: int = DEFAULT_RETRY_GAP,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        if retry_gap < 0:
            raise ValueError("retry_gap must be zero or greater.")
        if max_retries < 0:
            raise ValueError("max_retries must be zero or greater.")
        super().__init__(cards)
        self._retry_gap = retry_gap
        self._max_retries = max_retries

    def _build_queue(self) -> Iterable[int]:
        """Start in deck order; the queue grows as answers come in."""
        return range(len(self._cards))

    def _on_answer(self, position: int, is_correct: bool) -> None:
        """Put a missed card back in the queue, up to the retry limit."""
        if is_correct or self._misses[position] > self._max_retries:
            return
        self._queue.insert(min(self._retry_gap, len(self._queue)), position)

    @property
    def retries_left(self) -> Dict[int, int]:
        """Remaining retries per missed card position, for inspection."""
        return {
            position: max(self._max_retries - misses, 0)
            for position, misses in self._misses.items()
        }


class QuizModeFactory:
    """
    Create the :class:`QuizMode` that matches a mode name.

    Centralizing construction here keeps the CLI free of ``if mode == ...``
    chains: it passes the user's choice straight through and gets back
    something that satisfies the :class:`QuizMode` interface.
    """

    _MODES: Dict[str, Type[QuizMode]] = {
        SequentialMode.name: SequentialMode,
        RandomMode.name: RandomMode,
        AdaptiveMode.name: AdaptiveMode,
    }

    # Spelling variants accepted for convenience; each maps to a real mode.
    _ALIASES: Dict[str, str] = {
        "sequencial": SequentialMode.name,
    }

    @classmethod
    def create(
        cls, mode: str, cards: Sequence[Flashcard] = (), **options: object
    ) -> QuizMode:
        """
        Build the strategy registered under ``mode``.

        Args:
            mode: Mode name, case-insensitive. One of the values returned by
                :meth:`available_modes`.
            cards: Deck to quiz on, as returned by
                :func:`utils.file_handler.load_flashcard`.
            **options: Extra keyword arguments passed to the mode, for example
                ``max_retries`` for :class:`AdaptiveMode`.

        Returns:
            A ready-to-use :class:`QuizMode` instance.

        Raises:
            UnknownQuizModeError: If no mode is registered under that name.
        """
        key = cls._normalize(mode)
        mode_class = cls._MODES.get(key)
        if mode_class is None:
            raise UnknownQuizModeError(
                f"Unknown quiz mode: {mode!r}. "
                f"Choose one of: {', '.join(cls.available_modes())}."
            )
        return mode_class(cards, **options)  # type: ignore[arg-type]

    @classmethod
    def available_modes(cls) -> List[str]:
        """List the supported mode names, alphabetically."""
        return sorted(cls._MODES)

    @classmethod
    def supports(cls, mode: str) -> bool:
        """Report whether a mode name can be created."""
        return cls._normalize(mode) in cls._MODES

    @classmethod
    def register(cls, mode_class: Type[QuizMode]) -> None:
        """
        Add a new mode to the factory.

        Lets the application grow a fourth mode without editing this class.

        Raises:
            ValueError: If the class has no ``name``.
        """
        if not mode_class.name:
            raise ValueError(
                f"{mode_class.__name__} needs a non-empty 'name' to be "
                "registered as a quiz mode."
            )
        cls._MODES[cls._normalize(mode_class.name)] = mode_class

    @staticmethod
    def _normalize(mode: str) -> str:
        """Fold a requested mode name to its canonical key."""
        if not isinstance(mode, str):
            raise UnknownQuizModeError(
                f"Quiz mode must be given as text, got {type(mode).__name__}."
            )
        key = mode.strip().lower()
        return QuizModeFactory._ALIASES.get(key, key)
