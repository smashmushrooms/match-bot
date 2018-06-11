class Dialog:
    actions = {
        'nil': 'self.nil',
        'greetings': 'self.greetings',
        'choose_match': 'self.choose_match',
        'choose_side': 'self.choose_side',
        'start_scenario': 'self.start_scenario'
    }


    def get_random_message(self, messages):
        return random.choice(messages, 1)[0]

    def __init__(self, game_observer, user):
        self._state = 'nil'
        self._game_observer = game_observer
        self._user = user

    def dialog_update(self, text):
        eval(self.actions[self._state])(text)

    def nil(self, text):
        self._state = 'greetings'

    def greetings(self, text):
        greetings = [
            'Hi',
            'Hello',
            'Hi there'
        ]
        self_intros = [
            'my name is MatchBot',
            'I am MatchBot'
        ]
        photo_requests = [
            'I need your photo, take a selfie, please',
            'I need your selfie, send it to me, please',
            'Please, send your selfie'
        ]

        message_parts = [self.get_random_message(part_variations)
                         for part_variations in
                         [greetings, self_intros, photo_requests]]

        message = '{}, {}!\n{}'.format(
            *message_parts
        )

        bot.send_text_message(self._user.get_id(), message)
        self._state = 'choose_match'

    def choose_match(self, text):
        bot.send_text_message(self._user.get_id(), text)
        teams = self._game_observer.get_teams()
        buttons = []
        for team in teams:
            buttons.append([team[0] + ' - ' + team[1], 'postback'])

        choose_match_requests = [
            'Choose your favorite match today',
            'What is the match you wanna observe?',
            'What is the match you wanna track?',
            'What match do you prefer today?'
        ]

        send_buttons(self._user.get_id(), buttons, self.get_random_message(choose_match_requests))
        self._state = "choose_side"

    def choose_side(self, text):
        teams = text.split(' - ')
        side_requests = [
            'Choose your side',
            'Who do you support?',
            'Who would win?'
        ]
        quick_reply_send(self._user.get_id(),
                         [[teams[0], teams[0], ''], [teams[1], teams[1], '']],
                         self.get_random_message(side_requests))
        self._state = 'start_scenario'

    def start_scenario(self, text):
        self._user.set_lovely_team(text)
        self._game_observer.add_fan(self._user)
        bot.send_text_message(self._user.get_id(), 'Thank you! Wait for updates')

    def get_id(self):
        return self._user.get_id()

    def get_state(self):
        return self._state
    
    def get_user(self):
        return self._user
