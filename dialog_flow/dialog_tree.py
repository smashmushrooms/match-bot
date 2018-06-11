import front_end.fb_bot as fe

actions = {
    "greetings": self.greetings,
    "choose_match": self.choose_match,
    "choose_side": self.choose_side
}
    
class Dialog:
    _state = ''
    _game_observer = None
    _user = None

    def __init__(self, game_observer, user):
        self._state = 'greetings'
        self._game_observer = game_observer
        self._user = user

    def dialog(self, text):
        actions[self._state](text)

    def greetings(self, text):
        fe.send_text_message(self._user.get_id(), "Hi, we photolabbot, we need your photo, take selfi please")
        self._state = "choose_match"

    def choose_match(self, text):
        teams = self._game_observer.get_teams()
        buttons = [[]]
        for team in teames:
            buttons.append([team[0] + ' - ' + team[1], 'postback'])
        fe.send_buttons(self._user.get_id(), buttons, "Choose your favorite match today")
        self._state = "choose_side"

    def choose_side(self, text):
        teams = text.split(' - ')
        fe.quick_reply_send(self._user.get_id(), [[teams[0], teams[0], ''], [teams[1], teams[1], '']])

        
