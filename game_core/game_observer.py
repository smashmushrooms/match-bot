from objects.game import Game
from objects.user import User
from utils.score_matches import Score_Matches
import datetime


class GameObserver:
    
    _games = [Game]
    _teams = [[]]
    _users = [User]

    def __init__(self):
        self._score = Score_Matches(date='2018-06-18')
        self._update_daily_games()

    def _update_daily_games(self):
        self._teams = self._score.get_matches_names()
        for team in self._teams:
            match_time = self._score.get_score(team)['time'].split('-')
            self._games.append(Game(team, datetime.time(19, 0), self._score))

    def update_state(self):
        now = datetime.datetime.now()
        if (now.hours == 0 and now.minutes == 0) or not len(self._games):
            self._update_daily_games()

        for game in self._games:
            game.update()
        self._games = list(filter(lambda game: not game.is_end(), self._games))

    def get_teams(self):
        return self._teams

    def add_user(self, user):
        self._users.append(user)

    def find_user(self, id):
        for user in self._users:
            if user.get_id() == id:
                return user

