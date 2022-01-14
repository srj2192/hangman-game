import random
from enum import Enum


class GameState(Enum):
    IN_PROGRESS = 0
    WON = 1
    LOST = 2


class GuessResult(Enum):
    CORRECT = 0
    INCORRECT = 1

    FAIL_INVALID_INPUT = 2
    FAIL_ALREADY_GAME_OVER = 3
    FAIL_ALREADY_GUESSED = 4


class HangmanGame:
    def __init__(self, word, failed_guesses_limit):
        if failed_guesses_limit <= 0:
            raise ValueError("failed_guesses_limit must be over 0")

        if len(word) <= 0:
            raise ValueError("word must have at least 1 letter")

        self.word = word

        self.state = GameState.IN_PROGRESS
        self.guesses = []
        self.failed_guess_limit = failed_guesses_limit
        self.num_failed_guesses_remaining = failed_guesses_limit
        self.revealed_word = "".join(["_" for _ in range(len(word))])
        self.num_revealed_letters = 0

    def guess(self, input_letter):
        if self.state is GameState.IN_PROGRESS:
            if input_letter.isalpha() or input_letter.isnumeric():
                if input_letter in self.guesses:
                    result = GuessResult.FAIL_ALREADY_GUESSED
                elif input_letter in self.word:
                    self.update_word(input_letter)
                    result = GuessResult.CORRECT
                else:
                    self.num_failed_guesses_remaining -= 1
                    result = GuessResult.INCORRECT
            else:
                result = GuessResult.FAIL_INVALID_INPUT
        else:
            result = GuessResult.FAIL_ALREADY_GAME_OVER
        self.set_status()
        return result, self

    def update_word(self, input_letter):
        self.guesses.append(input_letter)
        letter_index = self.word.index(input_letter)
        revealed_word = list(self.revealed_word)
        revealed_word[letter_index] = input_letter
        # word = list(self.word)
        # word[letter_index] = "_"
        self.revealed_word = "".join(revealed_word)
        # self.word = "".join(word)

    def set_status(self):
        if '_' not in self.revealed_word:
            self.state = GameState.WON
        if self.num_failed_guesses_remaining < 1:
            self.state = GameState.LOST


class HangmanGameScorer:
    POINTS_PER_LETTER = 20
    POINTS_PER_REMAINING_GUESS = 10

    @classmethod
    def score(cls, game):
        points = game.num_revealed_letters * HangmanGameScorer.POINTS_PER_LETTER
        points += (
                game.num_failed_guesses_remaining
                * HangmanGameScorer.POINTS_PER_REMAINING_GUESS
        )
        return points


def create_hangman_game(words=None, guess_limit=5):
    if words is None:
        words = ["3dhubs", "marvin", "print", "filament", "order", "layer"]

    if len(words) <= 0:
        raise ValueError("words must have at least 1 word")

    if guess_limit <= 0:
        raise ValueError("guess_limit must be greater than 0")

    rand_word = words[random.randint(0, len(words) - 1)]
    return HangmanGame(rand_word, guess_limit)
