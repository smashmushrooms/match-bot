from objects.game import Game

class GameObserver():
    
    _games = [Game]

    def __init__(self):
        self._score = ScoreMatches()
        
    def update_daily_games(self):
        score.get_matches('Чемпионат Мира' , '2018-6-14')
        pass

    def update_state(self):
        for game in self._games:
            game.update()
        self._games = list(filter(lambda game: not game.is_end(), self._games))
