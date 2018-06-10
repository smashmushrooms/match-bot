import front_end as fe

class User():

    _name = ''
    _id = ''
    _current_lovely_team = ''
    _image_path = ''
    _state = ''

    action = {
        'idle': {'prev_st': 'ended', 'action': print},
        'ended': {'prev_st': 'idle', 'action': print}
    }

    def __init__(self, name, image_path, id):
        self._name = name
        self._image_path = image_path
        self._id = id

    def change_state(self, state):
        for st, attr in action.items():
            if self._state == st:
                if state == attr['prev_st']:
                    attr['action']()
        
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