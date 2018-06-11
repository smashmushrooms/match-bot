from pymessenger import Button
from pymessenger.bot import Bot
from numpy import random

ACCESS_TOKEN = 'EAAEtr6bH9LEBAKXpBq732AhmrdwLV3EJynZCYFLnqRahVqOHEtZCWjD3IoKdOvLepZAmZAcPKlpEBlM16WB6WTroZCRkZAadHHl' \
               'X7tcYdApMZBLg8YQAQyp0JXKEJ031NG0ud5ztpAZAL1Dy6ZAAn3Rb6l80jMJEyiUbZC6PqrdZAGTLRmgZCMOh4NSLfV1FzEw7GDAZD'
VERIFY_TOKEN = 'ourbadpass123'
bot = Bot(ACCESS_TOKEN)

class Dialog(object):

    _game_observer = None

    actions = {
        'nil': 'self.nil',
        'greetings': 'self.greetings',
        'choose_match': 'self.choose_match',
        'choose_side': 'self.choose_side',
        'start_scenario': 'self.start_scenario'
    }

    def get_random_message(self, messages):
        return random.choice(messages, 1)[0]

    def __init__(self, id):
        self._state = 'nil'
        self._id = id

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

        bot.send_text_message(self._id, message)
        self._state = 'choose_match'

    def choose_match(self, text):
        bot.send_text_message(self._id, text)
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

        send_buttons(self._id, buttons, self.get_random_message(choose_match_requests))
        self._state = "choose_side"

    def choose_side(self, text):
        teams = text.split(' - ')
        side_requests = [
            'Choose your side',
            'Who do you support?',
            'Who would win?'
        ]
        quick_reply_send(self._id,
                         [[teams[0], teams[0], ''], [teams[1], teams[1], '']],
                         self.get_random_message(side_requests))
        self._state = 'start_scenario'

    def start_scenario(self, text):
        bot.send_text_message(self._id, 'Thank you! Wait for updates')

    def get_state(self):
        return self._state

    def send_message(self, response):
        bot.send_text_message(self._id, response)
        return "success"

    def send_buttons(self, inbuttons, action_description):
        buttons = []
        for inbtn in inbuttons:
            button = Button(title=inbtn[0], type=inbtn[1], payload='other')
            buttons.append(button)
        bot.send_button_message(self._id, action_description, buttons)
        return "success"

    def send_photo(self, photo_path):
        result = bot.send_image(self._id, photo_path)
        return result

    def quick_reply_send(self, buttons, text):
        quick_replies = create_quick_reply(buttons)
        message = {
            "text": text,
            "quick_replies": quick_replies
        }
        bot.send_message(self._id, message)

    def create_quick_reply(self, buttons):
        quick_replies = []
        for btn in buttons:
            quick_reply = {
                "content_type": "text",
                "title": btn[0],
                "payload": btn[1]
            }
            if btn[2] != '':
                quick_reply['image_url'] = btn[2]

            quick_replies.append(quick_reply)
        return quick_replies

    def set_game_observer(self, observer):
        self._game_observer = observer

