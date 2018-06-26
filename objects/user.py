# -*- coding: utf-8 -*-
import json
import os
import utils.photolab_api as pl
from threading import Condition
from utils.used_dict import templates_names
from pymessenger import Button
from pymessenger.bot import Bot
from numpy import random
from sys import stderr
import binascii


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
            'get_selfie': 'send_match_list',
            'send_match_list': 'get_match',
            'get_match': 'get_team',
            'get_team': 'city_info',
            'city_info': 'warming',
            'warming': 'start_game',
            'start_game': 'game_in_process',
            'game_in_process': 'end_game',
            'end_game': 'send_match_list'
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
            'I need your photo, take a selfie, please 📸',
            'I need your selfie, send it to me, please 📷',
            'Please, send your selfie 📸'
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
        i = 0
        for teams in games:
            i += 1
            buttons.append([teams[0] + ' - ' + teams[1], 'postback'])
            if i == 3:
                break

        match_requests = [
            'Choose your favorite match today 🔥🔥🔥',
            'What is the match you wanna observe?',
            'What is the match you wanna track? ♥♥♥',
            'What match do you prefer today? ⚽'
        ]

        self.send_buttons(buttons, get_random_object(match_requests))

    def choose_side(self, teams):
        side_requests = [
            'Choose your side 🙈',
            'Who do you support? 💪',
            'Who would win? 🏆'
        ]

        self.quick_reply_send([[teams[0], teams[0], ''], [teams[1], teams[1], '']],
                              get_random_object(side_requests))

    def start_tracking(self):
        bot.send_text_message(self._id, 'Thank you! Wait for updates ⌛')

    def send_game_info(self, image_url, team_flag_url, stadium_photo_url):
        url = pl.post_photolab_photo('stadium', [image_url, team_flag_url, stadium_photo_url])
        text = self.game.generate_info_about_game()

        self.share_button(url, text)

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

    def share_button(self, image_url, text):
        bot.send_text_message(self._id, text)
        bot.send_image_url(self._id, image_url)
        share_btn = [{
            "title": "Share me with friends",
            "image_url": image_url,
            "buttons": [
                {
                    "type": "element_share",
                    "share_contents": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                                "template_type": "generic",
                                "elements": [
                                    {
                                        "title": "Your friend is using The World Championship photo bot",
                                        "subtitle": "Try it too",
                                        "image_url": image_url,
                                        "default_action": {
                                            "type": "web_url",
                                            "url": "https://photolab.me"
                                        },
                                        "buttons": [
                                            {
                                                "type": "web_url",
                                                "url": "https://www.facebook.com/messages/t/photolabmatchbot",
                                                "title": "Join The World Championship photo bot"
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                }
            ]
        }]
        print(bot.send_generic_message(self._id, share_btn))

    def set_game_observer(self, observer):
        self._game_observer = observer

    def send_image_url(self, url):
        bot.send_image_url(self._id, url)

    def set_state(self, state):
        self._state.set_state(state)

    def goal(self, image_url, team):

        goal_text = [
            'Amazing goal! Let\'s share your photo and happiness with friends ' + '😆',
            'We scored! Forward ' + team,
            'The whole country rejoices with you! Goooooal! Your friends must know about that!' + '😁'
        ]

        self.share_button(image_url, get_random_object(goal_text))

    def miss(self, image_url):
        miss_text = [
            'Do not worry, we still have time to score today ' + '😣',
            'Well, missed, now have to play more accurately ' + '😥',
            'Ah, missed the goal... But how cool you got the pictures! ' + '😜'
        ]

        self.share_button(image_url, get_random_object(miss_text))


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
        score = self.game.get_score()
        if score[0] + score[1] % 3 == 2:
            url = pl.post_photolab_photo('one_simple_shot', [self._image_url, 'happy'])
        elif score[0] + score[1] % 3 == 1:
            url = pl.post_photolab_photo('one_simple_shot', [self._image_url, 'face_ball'])
        else:
            if self.current_lovely_team == self.game.get_teams()[0]:
                #opponent_photo_url = get_random_object(self.game._team2_fans).get_image_url()
                url = pl.post_photolab_photo('versus', [[self._image_url, self._image_url],
                                             self.game.get_teams(), self.game.get_score(), self.game.get_city()])
            else:
                #opponent_photo_url = get_random_object(self.game._team1_fans).get_image_url()
                url = pl.post_photolab_photo('versus', [[self._image_url, self._image_url],
                                             self.game.get_teams(), self.game.get_score(), self.game.get_city()])

        self.goal(url, self.current_lovely_team)

    def miss_state(self):
        score = self.game.get_score()
        if score[0] + score[1] % 3 == 2:
            url = pl.post_photolab_photo('one_simple_shot', [self._image_url, 'cry'])
        elif score[0] + score[1] % 3 == 1:
            url = pl.post_photolab_photo('one_simple_shot', [self._image_url, 'face_ball'])
        else:
            if self.current_lovely_team == self.game.get_teams()[0]:
                #opponent_photo_url = get_random_object(self.game._team2_fans).get_image_url()
                url = pl.post_photolab_photo('versus', [[self._image_url, self._image_url],
                                             self.game.get_teams(), self.game.get_score(), self.game.get_city()])
            else:
                #opponent_photo_url = get_random_object(self.game._team1_fans).get_image_url()
                url = pl.post_photolab_photo('versus', [[self._image_url, self._image_url],
                                             self.game.get_teams(), self.game.get_score(), self.game.get_city()])

        self.miss(url)

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
            self.dialog_update()

        elif curr_dialog_state == 'send_match_list':

            games = self._game_observer.get_teams()
            self.choose_match(games)
            curr_dialog_state.turn_next()

        elif curr_dialog_state == 'get_match':
            games = self._game_observer.get_teams()
            if len(games) == 0:
                self.send_message('There are no games today 😭 See you later!')
                return
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

            if self.current_lovely_team != '':
                return ''

            self.current_lovely_team = text
            self._game_observer.add_fan(self)
            stadium_photo_url = self.game.get_city()
            self.start_tracking()

            self.send_game_info(self._image_url, self.current_lovely_team, stadium_photo_url)
            curr_dialog_state.turn_next()

        elif curr_dialog_state == 'city_info':
            if text is not None:
                return ''

            city = self.game._score_matches.get_city(self.game.get_teams())
            url, fixed_url = pl.post_photolab_photo('city_info', [city])

            text = self.game.generate_info_about_city()

            self.send_message(text)
            self.send_image_url(url)
            self.send_image_url(fixed_url)
            curr_dialog_state.turn_next()

        elif curr_dialog_state == 'warming':
            if text is not None:
                return ''

            url = pl.post_photolab_photo('one_simple_shot', [self._image_url, 'happy'])
            print(url)
            text = 'Only a couple of hours left until the match! All warm up!'
            self.share_button(url, text)
            curr_dialog_state.turn_next()

        elif curr_dialog_state == 'start_game':
            if text is not None:
                return ''

            if self.current_lovely_team == self.game.get_teams()[0]:
                #opponent_photo_url = get_random_object(self.game._team2_fans).get_image_url()
                url = pl.post_photolab_photo('versus', [[self._image_url, self._image_url],
                                             self.game.get_teams(), self.game.get_score(), self.game.get_city()])
            else:
                #opponent_photo_url = get_random_object(self.game._team1_fans).get_image_url()
                url = pl.post_photolab_photo('versus', [[self._image_url, self._image_url],
                                             self.game.get_teams(), self.game.get_score(), self.game.get_city()])
            # self._opponent = opponent_photo_url

            text = 'Today\'s match will be watched by millions of people around the world. ' \
                   'Here goes your personal opponent from the opposite side... Let the battle begin!'

            self.share_button(url, text)
            curr_dialog_state.turn_next()

        elif curr_dialog_state == 'game_in_progress':
            if text is not None:
                return ''

            curr_dialog_state.turn_next()

        elif curr_dialog_state == 'end_game':
            if text is not None:
                return ''

            city_name = self.game._score_matches.get_city(self.game.get_teams())
            url = pl.post_photolab_photo('final_post', [[fan._image_url for fan in self.game._team1_fans],
                                             self.current_lovely_team, city_name])

            text = 'This is the end of the match! Well done, fans!'

            self.share_button(url, text)
            curr_dialog_state.turn_next()
            self.current_lovely_team = ''
            self.dialog_update()
        else:
            raise ValueError('Undefined state')
