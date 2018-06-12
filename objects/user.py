import json
import os
import utils.photolab_api as pl
from objects.dialog import Dialog
from threading import Condition
from objects.dialog import get_random_object
from utils.used_dict import templates_names

class User:
    _game_observer = None

    def __init__(self, id, scenario_path='scenario/base_scenario.json'):
        self._id = id
        self._current_lovely_team = ''
        self._image_url = ''
        self._state = 'ended'
        self._scenario = {}
        self.set_scenario(scenario_path)
        self._game = None
        self._dialog = Dialog(id)
        self._dialog.set_game_observer(self._game_observer)

    def change_state(self, state):
        if self._state == state:
            return
        self._state = state
        while True:
            try:
                print('NoneType')
                self._game.get_teams()
                break
            except AttributeError:
                pass

        if self._state == 'match_started':
            text = 'Today\'s match will be watched by millions of people around the world. ' \
                   'Here goes your personal opponent from the opposite side... Let the battle begin!'
            if self._current_lovely_team == self._game.get_teams()[0]:
                print (self._game._team2_fans)
                opponent_photo_url = get_random_object(self._game._team2_fans).get_image_url()
                url = pl.post2photlab_versus(photos=[self._image_url, opponent_photo_url],
                                          teams=self._game.get_teams())
            else:
                opponent_photo_url = get_random_object(self._game._team1_fans).get_image_url()
                print (self._game._team1_fans)
                url = pl.post2photlab_versus(photos=[opponent_photo_url, self._image_url],
                                          teams=self._game.get_teams())
        elif self._state == 'match_ended':
            city_name = self._game._score_matches.get_city(self._game.get_teams())
            print(self._game._team1_fans)
            url = pl.post2photlab_final_post([fan._image_url for fan in self._game._team1_fans],
                                             self._current_lovely_team, city_name)
            text = 'This is the end of the match! Well done, fans!'
        elif self._state == 'before_3_hours':
            text = 'Saint Petersburg is a beautiful city, surprising with its atmosphere and architecture. ' \
                   'Of course all it\'s magnificence can not be fitted in one photo... But we have imposed cool ' \
                   'filters from the application PhotoLab ;)'
            url, fixed_url = pl.generate_city_photo(self._game._score_matches.get_city(self._game.get_teams()))
            self._dialog.send_message(text)
            self._dialog.send_image_url(url)
            self._dialog.send_image_url(fixed_url)
            return
        elif self._state == 'before_1_5_hours':
            url = pl.post2photlab(photo=self._image_url, template='soccer_man')
            text = 'Only a couple of hours left until the match! All warm up!'
        elif self._state == 'before_1_hour':
            return
            # TODO
            url = pl.post2photlab(photo=self._image_url, template='soccer_man')
            text = 'Text'
        elif self._state == 'idle':
            url = pl.post2photlab_stadium(self._image_url, self._current_lovely_team,
                    self._game._score_matches.get_city(self._game.get_teams()))
            text = 'The game will take place in the Krestovsky stadium. Move all the stuff around and ' \
                   'do not miss one of the main football events of the next 4 years! MatchBot will ' \
                   'keep you informed! In touch :)'

        self._dialog.send_message(text)
        self._dialog.send_image_url(url)

    def score_changed(self, delta):
        if delta:
            goal_cb()
        else:
            miss_cb()

    def set_scenario(self, scenario_path):
        with open(scenario_path) as f:
            self._scenario = json.load(f)

    def set_lovely_team(self, team):
        self._current_lovely_team = team

    def set_image_url(self, url):
        self._image_url = url

    def set_state(self, state):
        self._state = state

    def get_name(self):
        return self._name

    def get_current_lovely_team(self):
        return self._current_lovely_team

    def get_image_url(self):
        return self._image_url

    def get_state(self):
        return self._state

    def get_id(self):
        return self._id

    def set_game(self, game):
        self._game = game

    def dialog_update(self, message=''):
        if self._dialog.get_state() == 'start_scenario':
            if message:
                self.set_lovely_team(message)
            self._game_observer.add_fan(self)
            self.change_state('idle')
        self._dialog.dialog_update(message)

    def send_message(self, message):
        self._dialog.send_message(message)

    def get_dialog(self):
        return self._dialog
