from server import app
from unittest import TestCase
from unittest.mock import MagicMock
import json
import sys
import hangman


# Monkey patch the create game function so we can have a deterministic word to test with. This should
# probably read the words from some config and not rely on hardcoded vars but this is simpler.
original_hangman_create = hangman.create_hangman_game


def create_game_with_override_words(words=None, guess_limit=5):
    return original_hangman_create(words=["abac"], guess_limit=5)


hangman.create_hangman_game = create_game_with_override_words


def parse_response(response):
    return json.loads(response.get_data().decode(sys.getdefaultencoding()))


class TestApiIntegration(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def create_game(self):
        return self.app.post("/api/hangman")

    def get_game(self, game_id):
        return self.app.get(f"/api/hangman/{game_id}")

    def make_guess(self, game_id, letter):
        return self.app.post(f"/api/hangman/{game_id}/guess",
                             data=json.dumps({'letter': letter}),
                             headers={'Content-Type': 'application/json'})

    def test_create_game(self):
        response = parse_response(self.create_game())

        self.assertIn('gameId', response)
        self.assertEqual(response['state'], 'IN_PROGRESS')
        self.assertEqual(response['revealedWord'], '____')
        self.assertEqual(response['numFailedGuessesRemaining'], 5)
        self.assertEqual(response['score'], 5 * 10)

    def test_get_game(self):
        game_id = parse_response(self.create_game())['gameId']

        response = parse_response(self.get_game(game_id))

        self.assertEqual(response['gameId'], game_id)
        self.assertEqual(response['state'], 'IN_PROGRESS')
        self.assertEqual(response['revealedWord'], '____')
        self.assertEqual(response['numFailedGuessesRemaining'], 5)
        self.assertEqual(response['score'], 5 * 10)

    def test_invalid_letter_guess(self):
        game_id = parse_response(self.create_game())['gameId']

        response = parse_response(self.get_game(game_id))

        guess_response = parse_response(self.make_guess(game_id, '_'))

        self.assertEqual(guess_response['error'], 'FAIL_INVALID_INPUT')

    def test_won_case(self):
        test_word = "time"
        hangman.create_hangman_game = MagicMock(return_value=hangman.HangmanGame(word=test_word, failed_guesses_limit=5))
        game_id = parse_response(self.create_game())['gameId']

        guess_response = {}
        for letter in test_word:
            guess_response = parse_response(self.make_guess(game_id, letter))

        self.assertEqual(guess_response['revealedWord'], test_word)
        self.assertEqual(guess_response['state'], 'WON')

    def test_lost_case(self):
        test_word = "time"
        hangman.create_hangman_game = MagicMock(return_value=hangman.HangmanGame(word=test_word, failed_guesses_limit=5))
        game_id = parse_response(self.create_game())['gameId']

        guess_response = {}
        for letter in 'wrong':
            guess_response = parse_response(self.make_guess(game_id, letter))

        self.assertEqual(guess_response['state'], 'LOST')
