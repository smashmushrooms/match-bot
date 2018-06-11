from objects.user import User
from datetime import datetime
from utils.score_matches import Score_Matches

class Game:

    def __init__(self, teams, time, score):
        self._teams = teams
        self._time_of_game = time
        self._score_matches = score
        self._team1_fans = []
        self._team2_fans = []
        self._score = [0, 0]
        self._teams = []
        self._time_of_game = None
        self._score_matches = None
        self._state = 'idle'

    def update(self):
        now = datetime.now()

        response = self._score_matches.get_score(self._teams)
        time = response['time']
        if time == 'Завершен':
            self._state = 'match_ended'

        if response['time'] == '0':
            self._state = 'match_started'

        score = [response['score_first'], response['score_second']]
        if score[0].isdigit() and score[1].isdigit():
            if score != self._score:
                if score[0] > self._score[0]:
                    delta = True
                else:
                    delta = False
                for user in self._team1_fans:
                    user.score_changed(delta)
                for user in self._team2_fans:
                    user.score_changed(delta)
        self._time_to_game()

    def _update_fans_state(self, fans_state1, fans_state2):
        for user in self._team1_fans:
            user.change_state(fans_state1)
        for user in self._team2_fans:
            user.change_state(fans_state2)

    def _time_to_game(self):
        now = datetime.now()
        delta = self._time_of_game - now
        hours = delta.seconds // 3600
        minutes = (delta.seconds // 60) % 60
        print(hours, minutes)
        state = self._state
        if hours == 0 and minutes == 3:
            self._state = 'before_3_hours'
        if hours == 0 and minutes == 2:
            self._state = 'before_1_5_hour'
        if hours == 0 and minutes == 1:
            self._state = 'before_1_hour'
        if state != self._state:
            self._update_fans_state(self._state, self._state)

    def is_end(self):
        return self._state == 'ended'

    def add_fan(self, user):
        if user.get_current_lovely_team() == self._teams[0]:
            self._team1_fans.append(user)
        else:
            self._team2_fans.append(user)
        user.set_game(self)

    def get_teams(self):
        return self._teams
