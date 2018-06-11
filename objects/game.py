from user import User
from datetime import datetime, date, time
from score_matches import Score_Matches

class Game:

    _score = [0, 0]
    _teams = []
    _team1_fans = [User]
    _team2_fans = [User]
    _time_of_game = None
    _score_matches = None

    def __init__(self, teams, time, score):
        self._teams = teams
        self._time_of_game = time
        self._score_matches = score

    def update(self):
        now = datetime.datetime.now()
        if now.hours == 0 and now.minutes == 0:
            # TODO Restart dialog system
            pass
        
        response = self._score_matches.get_score(self._teams)
        # TODO Use match time
        score = [response['score_firts'], response['score_second']]
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

    def _update_fans_state(self, fans_state1, fans_state2):
        for user in self._team1_fans:
            user.change_state(fans_state1)
        for user in self._team2_fans:
            user.change_state(fans_state2)

    def _time_to_game(self, game_time):
        now = datetime.datetime.now()
        delta = now - self._time_of_game
        if delta.hours == 3 and delta.minutes == 0:
            state = 'before_3_hours'
        if delta.hours == 1 and delta.minutes == 30:
            state = 'before_1_5_hour'
        if delta.hours == 1 and delta.minutes == 0:
            state = 'before_1_hour'

        self._update_fans_state(state, state)

    def is_end(self):
        return self._state == 'ended'

    def add_fan(self, user):
        if user.get_current_lovely_team() == self._teams[0]:
            self._team1_fans.append(user)
        else:
            self._team2_fans.append(user)
