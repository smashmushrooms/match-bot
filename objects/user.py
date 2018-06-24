import json
import os
import utils.photolab_api as pl
from threading import Condition
from utils.used_dict import templates_names
from pymessenger import Button
from pymessenger.bot import Bot
from numpy import random
from sys import stderr


def get_random_object(objects):
    return random.choice(objects, 1)[0]


ACCESS_TOKEN = 'EAAEtr6bH9LEBAKXpBq732AhmrdwLV3EJynZCYFLnqRahVqOHEtZCWjD3IoKdOvLepZAmZAcPKlpEBlM16WB6WTroZCRkZAadHHl' \
               'X7tcYdApMZBLg8YQAQyp0JXKEJ031NG0ud5ztpAZAL1Dy6ZAAn3Rb6l80jMJEyiUbZC6PqrdZAGTLRmgZCMOh4NSLfV1FzEw7GDAZD'
VERIFY_TOKEN = 'ourbadpass123'
bot = Bot(ACCESS_TOKEN)


class Dialog(object):
    _game_observer = None

    class State(object):
        prev_to_next = {
            'start': 'get_selfie',
            'get_selfie': 'get_match',
            'get_match': 'get_team',
            'get_team': 'game_info',
            'game_info': 'city_info',
            'city_info': 'warming',
            'warming': 'start_game',
            'start_game': 'game_in_process',
            'game_in_process': 'end_game',
            'end_game': 'get_match'
        }

        def __eq__(self, other):
            return self._state == other

        def __init__(self):
            self._state = 'start'

        def turn_next(self):

            self._state = self.prev_to_next[self._state]

        def set_state(self, state):
            self._state = state

    def __init__(self, id):
        self._state = Dialog.State()
        self._id = id

    def request_selfie(self):
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

        message_parts = [get_random_object(part_variations)
                         for part_variations in
                         [greetings, self_intros, photo_requests]]

        message = '{}, {}!\n{}'.format(
            *message_parts
        )

        bot.send_text_message(self._id, message)

    def request_selfie_again(self):
        bot.send_text_message(self._id, 'Send your photo, please :)')

    def choose_match(self, games):
        buttons = []
        for teams in games:
            buttons.append([teams[0] + ' - ' + teams[1], 'postback'])

        match_requests = [
            'Choose your favorite match today',
            'What is the match you wanna observe?',
            'What is the match you wanna track?',
            'What match do you prefer today?'
        ]

        self.send_buttons(buttons, get_random_object(match_requests))

    def choose_side(self, teams):
        side_requests = [
            'Choose your side',
            'Who do you support?',
            'Who would win?'
        ]

        self.quick_reply_send([[teams[0], teams[0], ''], [teams[1], teams[1], '']],
                              get_random_object(side_requests))

    def start_tracking(self):
        bot.send_text_message(self._id, 'Thank you! Wait for updates')

    def send_city_info(self, image_url, team_flag_url, stadium_photo_url):
        url = pl.post2photlab_stadium(image_url, team_flag_url, stadium_photo_url)
        text = self.game.generate_info_about_game()

        self.send_message(text)
        self.send_image_url(url)

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
        quick_replies = self.create_quick_reply(buttons)
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

    def send_image_url(self, url):
        bot.send_image_url(self._id, url)

    def set_state(self, state):
        self._state.set_state(state)


class User(Dialog):
    def __init__(self, id):
        super().__init__(id)
        self.current_lovely_team = ''
        self.game = None
        self._image_url = ''
        self._scenario = {}

    def change_state(self, state):
        raise NotImplementedError
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

    def score_changed(self, delta):
        if delta:
            self.goal_state()
        else:
            self.miss_state()

    def goal_state(self):
        pass
        # TODO

    def miss_state(self):
        pass
        # TODO

    def dialog_update(self, text=None, tag=None):
        print('Dialog is updating', file=stderr)
        curr_dialog_state = self._state
        print(curr_dialog_state._state, file=stderr)

        if curr_dialog_state == 'start':
            self.request_selfie()
            curr_dialog_state.turn_next()

        elif curr_dialog_state == 'get_selfie':
            if not text or tag != 'image':
                self.send_message(text)
                self.request_selfie_again()
                return
            self._image_url = text

            curr_dialog_state.turn_next()

            games = self._game_observer.get_teams()
            self.choose_match(games)

        elif curr_dialog_state == 'get_match':
            games = self._game_observer.get_teams()
            teams = text.split(' - ')
            if teams not in games:
                self.choose_match(games)
                return

            self.teams_ = teams

            curr_dialog_state.turn_next()

            self.choose_side(teams)

        elif curr_dialog_state == 'get_team':
            if text not in self.teams_:
                self.choose_side(self.teams_)
                return

            del self.teams_
            self.current_lovely_team = text
            self._game_observer.add_fan(self)
            curr_dialog_state.turn_next()
            self.dialog_update()

        elif curr_dialog_state == 'game_info':
            stadium_photo_url = self.game.get_city()

            self.send_city_info(self._image_url, self.current_lovely_team, stadium_photo_url)
            self.start_tracking()
            curr_dialog_state.turn_next()

        elif curr_dialog_state == 'city_info':
            city = self.game._score_matches.get_city(self.game.get_teams())
            url, fixed_url = pl.generate_city_photo(city)

            text = self.game.generate_info_about_city()

            self.send_message(text)
            self.send_image_url(url)
            self.send_image_url(fixed_url)

            curr_dialog_state.turn_next()

        elif curr_dialog_state == 'warming':
            url = pl.post2photlab(photo=self._image_url, template='soccer_man')
            text = 'Only a couple of hours left until the match! All warm up!'
            curr_dialog_state.turn_next()

        elif curr_dialog_state == 'start_game':
            if self.current_lovely_team == self.game.get_teams()[0]:
                print(self.game._team2_fans)
                opponent_photo_url = get_random_object(self.game._team2_fans).get_image_url()
                url = pl.post2photlab_versus(photos=[self._image_url, opponent_photo_url],
                                             teams=self.game.get_teams())
            else:
                opponent_photo_url = get_random_object(self.game._team1_fans).get_image_url()
                print(self.game._team1_fans)
                url = pl.post2photlab_versus(photos=[opponent_photo_url, self._image_url],
                                             teams=self.game.get_teams())

            text = 'Today\'s match will be watched by millions of people around the world. ' \
                   'Here goes your personal opponent from the opposite side... Let the battle begin!'

            curr_dialog_state.turn_next()

        elif curr_dialog_state == 'game_in_progress':
            curr_dialog_state.turn_next()

        elif curr_dialog_state == 'end_game':
            city_name = self.game._score_matches.get_city(self.game.get_teams())
            print(self.game._team1_fans)
            url = pl.post2photlab_final_post([fan._image_url for fan in self.game._team1_fans],
                                             self.current_lovely_team, city_name)

            text = 'This is the end of the match! Well done, fans!'

            curr_dialog_state.turn_next()
        else:
            raise ValueError('Undefined state')
