import json
import os
import utils.photolab_api as pl
from objects.dialog import Dialog
from threading import Condition
from objects.dialog import get_random_object

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
        for st, attr in self._scenario.items():
            if self._state == attr['prev_st']:
                print('Previous state:', self._state)
                print('New state:', state)
                if self._state == state:
                    return
                if self._state == 'ended':
                    if self._current_lovely_team == self._game.get_teams()[0]:
                        opponent_photo_url = get_random_object(get_random_object(self._game._team2_fans))
                        url = eval(attr['action'])(photos=[self._image_url, opponent_photo_url],
                                                   teams=self._game.get_teams())
                    else:
                        opponent_photo_url = get_random_object(get_random_object(self._game._team1_fans))
                        url = eval(attr['action'])(photos=[opponent_photo_url, self._image_url],
                                                   teams=self._game.get_teams())
                self._state = state
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
            self._game_observer.add_fan(self)
            self.set_lovely_team(message)
            self.change_state('idle')
        self._dialog.dialog_update(message)

    def send_message(self, message):
        self._dialog.send_message(message)

    def get_dialog(self):
        return self._dialog
