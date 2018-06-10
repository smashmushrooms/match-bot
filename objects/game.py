from user import User
from datetime import datetime, date, time

class Game:

    _state = ''
    _score = [0, 0]
    _teams = None
    _team1_fans = [User]
    _team2_fans = [User]
    _time_of_game = None

    def __init__(self, teams, time):
        self._teams = teams
        self._time_of_game = time

    def update(self):
        pass
        # if score != self._score:
        #   for_each_user upd
        # TODO Use Kirill's API

    def update_fans_state(self, fans_state1, fans_state2, result_delta):
        for user in self._team1_fans:
            user.change_state(fans_state1)
        for user in self._team2_fans:
            user.change_state(fans_state2)

    def time_to_game(self, game_time):
        now = datetime.datetime.now()
        delta = now - self._time_of_game
        if delta.hours == 2 and delta.minutes == 0:
            self.update_fans_state('face_flag', 'face_flag')
        if delta.hours == 1 and delta.minutes == 15:
            self.update_fans_state('changing_room', 'changing_room')
        if delta.hours == 1 and delta.minutes == 0:
            self.update_fans_state('warm_up', 'warm_up')

    def is_end(self):
        return self._state == 'ended'
