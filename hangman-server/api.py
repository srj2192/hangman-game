from flask import Blueprint, request, jsonify
import hangman
from gamemanager import GameManager

api = Blueprint('api', __name__)

# This is fine for single process server but if running in multiple processes the game management will have to be
# stored in some other shared memory
game_manager = GameManager()


# Allow the web-app to access these endpoints. This shouldn't be used in prod unless we wanna allow access to the api
# from other domains other than our own
@api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


def jsonifyGame(game_id, game, error=''):
    to_enum_string = {
        hangman.GameState.IN_PROGRESS: 'IN_PROGRESS',
        hangman.GameState.WON: 'WON',
        hangman.GameState.LOST: 'LOST',
    }

    return jsonify({
        'gameId': game_id,
        'state': to_enum_string[game.state],
        'revealedWord': game.revealed_word,
        'numFailedGuessesRemaining': game.num_failed_guesses_remaining,
        'score': hangman.HangmanGameScorer.score(game),
        'error': error
    })


@api.route('/api/hangman', methods=['POST'])
def post_hangman():
    game_id, game = game_manager.create_game()
    return jsonifyGame(game_id, game), 200


@api.route('/api/hangman/<int:game_id>', methods=['GET'])
def get_hangman(game_id):
    game = game_manager.get_game(game_id)

    if game is None:
        return jsonify({'error': 'Game not found'}), 404

    return jsonifyGame(game_id, game), 200


@api.route('/api/hangman/<int:game_id>/guess', methods=['POST'])
def guess_game(game_id):
    data = request.get_json()

    result, game = game_manager.guess_word(game_id, data['letter'])

    status = 200
    error = ''

    if result != hangman.GuessResult.CORRECT:
        status = 400
        error = result.name

    response = jsonifyGame(game_id, game, error)

    return response, status
