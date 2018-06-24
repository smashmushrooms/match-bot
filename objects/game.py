from objects.user import User
from datetime import datetime
from utils.score_matches import Score_Matches

class Game:

    _score_matches = None

    def __init__(self, teams, city, time):
        self._teams = teams
        self._time_of_game = time
        self._team1_fans = []
        self._team2_fans = []
        self._score = [0, 0]
        self._state = 'idle'
        self._city = city

    def update(self):
        now = datetime.now()

        response = self._score_matches.get_score(self._teams)
        time = response['time']
        '''
        if time == 'Завершен':
            self._state = 'match_ended'
        
        if time == '0':
            self._state = 'match_started'
        '''

        score = [response['score_first'], response['score_second']]
        if score[0].isdigit() and score[1].isdigit():
            if score != self._score:
                if int(score[0]) > self._score[0]:
                    delta = True
                else:
                    delta = False
                for user in self._team1_fans:
                    user.score_changed(delta)
                for user in self._team2_fans:
                    user.score_changed(delta)
        self._time_to_game()

    def _update_fans_state(self, fans_state1, fans_state2):
        print(self._team1_fans, self._team2_fans)
        for user in self._team1_fans:
            print(fans_state1)
            user.set_state(fans_state1)
            user.dialog_update()
        for user in self._team2_fans:
            print(fans_state2)
            user.set_state(fans_state2)
            user.dialog_update()

    def _time_to_game(self):
        now = datetime.now()
        delta = self._time_of_game - now
        hours = delta.seconds // 3600
        minutes = (delta.seconds // 60) % 60
        print(hours, minutes)

        state = self._state

        if hours == 0 and minutes == 0:
            self._state = 'start_game'
        if hours == 23 and minutes == 56:
            self._state = 'end_game'

        if hours == 0 and minutes == 2:
            self._state = 'city_info'
        if hours == 0 and minutes == 1:
            self._state = 'warming'
        if state != self._state:
            print(self)
            self._update_fans_state(self._state, self._state)

    def is_end(self):
        return self._state == 'end_game'

    def add_fan(self, user):
        print(self)
        if user.current_lovely_team == self._teams[0]:
            self._team1_fans.append(user)
            print(self._team1_fans)
        else:
            self._team2_fans.append(user)
            print(self._team2_fans)
        user.game = self

    def get_teams(self):
        return self._teams

    def get_city(self):
        return self._city

    def generate_info_about_city(self):
        return ''
        # TODO

    def generate_info_about_game(self):
        return ''
        # TODO
