from objects.game import Game
from objects.user import User
from utils.score_matches import Score_Matches
from datetime import datetime, timedelta

class GameObserver(object):
    _games = []
    _teams = [[]]

    def __init__(self):
        self._score = Score_Matches(date='2018-06-19')
        self._update_daily_games()
        Game._score_matches = self._score

    def _update_daily_games(self):
        self._teams = self._score.get_matches_names()
        for team in self._teams:
            city = self._score.get_city(team)
            match_time = self._score.get_score(team)['time'].split('-')
            game = Game(team, city, datetime.now() + timedelta(0, 240, 0))
            self._games.append(game)

    def update_state(self):
        now = datetime.now()
        if (now.hour == 1 and now.minute == 0) or not len(self._games):
            self._update_daily_games()
        for game in self._games:
            game.update()
            print(game._team1_fans, game._team2_fans)
        self._games = list(filter(lambda game_i: not game_i.is_end(), self._games))

    def get_teams(self):
        return self._teams

    def add_fan(self, user):
        for game in self._games:
            if user.current_lovely_team in game.get_teams():
                game.add_fan(user)
                return

