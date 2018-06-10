from objects.game import Game

class GameObserver():
    
    _games = [Game]

    def __init__(self):

    def update_daily_games(self):
        pass

    def update_state(self):
        for game in self._games:
            game.update()
        self._games = list(filter(lambda game: not game.is_end(), self._games))
