class Dialog:
    actions = {
        'nil': 'self.nil',
        'greetings': 'self.greetings',
        'choose_match': 'self.choose_match',
        'choose_side': 'self.choose_side',
        'start_scenario': 'self.start_scenario'
    }

    _state = ''
    _game_observer = None
    _user = None

    def __init__(self, game_observer, user):
        self._state = 'nil'
        self._game_observer = game_observer
        self._user = user

    def dialog_update(self, text):
        eval(self.actions[self._state])(text)

    def nil(self, text):
        self._state = 'greetings'

    def greetings(self, text):
        bot.send_text_message(self._user.get_id(), 'Hi, we are photolabbot, we need your photo, take selfi please')
        self._state = 'choose_match'

    def choose_match(self, text):
        bot.send_text_message(self._user.get_id(), text)
        teams = self._game_observer.get_teams()
        buttons = []
        print(teams)
        for team in teams:
            buttons.append([team[0] + ' - ' + team[1], 'postback'])
        send_buttons(self._user.get_id(), buttons, "Choose your favorite match today")
        self._state = "choose_side"

    def choose_side(self, text):
        teams = text.split(' - ')
        quick_reply_send(self._user.get_id(), [[teams[0], teams[0], ''], [teams[1], teams[1], '']], 'Choose your side')
        self._state = 'start_scenario'

    def start_scenario(self, text):
        self._user.set_lovely_team(text)
        bot.send_text_message(self._user.get_id(), 'Thank you! Wait for updates')

    def get_id(self):
        return self._user.get_id()

    def get_state(self):
        return self._state
