from objects.game import Game
from objects.user import User
from utils.score_matches import Score_Matches
from datetime import datetime, time

class GameObserver:
    
    _games = []
    _teams = [[]]

    def __init__(self):
        self._score = Score_Matches(date='2018-06-18')
        self._update_daily_games()

    def _update_daily_games(self):
        self._teams = self._score.get_matches_names()
        for team in self._teams:
            match_time = self._score.get_score(team)['time'].split('-')
            game = Game(team, datetime(2018, 6, 11, 16, 46), self._score)
            self._games.append(game)

    def update_state(self):
        now = datetime.now()
        if (now.hour == 0 and now.minute == 0) or not len(self._games):
            self._update_daily_games()
        for game in self._games:
            game.update()
        self._games = list(filter(lambda game: not game.is_end(), self._games))

    def get_teams(self):
        return self._teams

    def add_fan(self, user):
        for game in self._games:
            if user.get_current_lovely_team() in game.get_teams():
                game.add_fan(user)

