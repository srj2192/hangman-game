import hangman


class GameManager:
    def __init__(self):
        self.games = {}
        self.next_game_id = 1

    def create_game(self):
        game = hangman.create_hangman_game()
        game_id = self.next_game_id
        self.games[game_id] = game
        self.next_game_id += 1

        return game_id, game

    def get_game(self, game_id):
        return self.games.get(game_id, None)

    def guess_word(self, game_id, letter):
        game = self.games[game_id]
        guess_result, updated_game = game.guess(input_letter=letter)
        self.games[game_id] = updated_game
        return guess_result, updated_game

