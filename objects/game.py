from user import User

class Game:
    _state = 0
    _score = [0, 0]
    _teams = None
    _team1_fans = [User]
    _team2_fans = [User]


    def __init__(self, teams):
        self._teams = teams

    def update(self):
        pass
        # if score != self._score:
        #   for_each_user upd
        # TODO Use Kirill's API

    
        
