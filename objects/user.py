import json
import photolab_api as pl

class User():

    _name = ''
    _id = ''
    _current_lovely_team = ''
    _image_path = ''
    _state = 'idle'
    _scenario = {}

    def __init__(self, id, scenario_path='scenario/base_scenario.json'):
        self._id = id
        self.set_scenario(scenario_path)

    def change_state(self, state):
        for st, attr in self._scenario.items():
            if self._state == attr['prev_st']:
                eval(attr['action'])()
                self._state = state

    def score_changed(self, delta):
        if delta:
            pl.goal_cb()
        else:
            pl.miss_cb()

    def set_scenario(self, scenario_path):
        with open(scenario_path) as f:
            self._scenario = json.load(f)
        
    def set_lovely_team(self, team):
        self._current_lovely_team = team

    def set_photo(self, image_path):
        self._image_path = image_path

    def set_state(self, state):
        self._state = state

    def get_name(self):
        return self._name
    
    def get_current_lovely_team(self):
        return self._current_lovely_team

    def get_image_path(self):
        return self._image_path

    def get_state(self):
        return self._state

    def get_id(self):
        return self._id