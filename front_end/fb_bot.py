#Python libraries that we need to import for our bot
import random
import shutil
from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Element, Button
import requests
from game_observer import GameObserver
from objects import User
from time import sleep
from threading import Thread
from numpy import random
#from game_observer import GameObserver
    
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
        print(teams)
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

app = Flask(__name__)
ACCESS_TOKEN = 'EAAEtr6bH9LEBAKXpBq732AhmrdwLV3EJynZCYFLnqRahVqOHEtZCWjD3IoKdOvLepZAmZAcPKlpEBlM16WB6WTroZCRkZAadHHlX7tcYdApMZBLg8YQAQyp0JXKEJ031NG0ud5ztpAZAL1Dy6ZAAn3Rb6l80jMJEyiUbZC6PqrdZAGTLRmgZCMOh4NSLfV1FzEw7GDAZD'
VERIFY_TOKEN = 'ourbadpass123'
bot = Bot(ACCESS_TOKEN)
game_observer = GameObserver()
dialogs = {}

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        print(output)
        for event in output['entry']:
            if 'messaging' in event:
                messaging = event['messaging']
                for x in messaging:
                    if 'message' not in x:
                        if 'postback' in x and 'payload' in x['postback']:
                            if x['postback']['payload'] == 'Begin':
                                recipient_id = x['sender']['id']
                                if recipient_id not in dialogs:
                                    _user_init(recipient_id)
                                dialogs[recipient_id].dialog_update('')
                    else:
                        if x.get('message'):
                            recipient_id = x['sender']['id']
                            if recipient_id not in dialogs:
                                return "Message Processed"
                            if x['message'].get('text'):
                                message = x['message']['text']
                                dialogs[recipient_id].dialog_update(message)
                            if x['message'].get('attachments'):
                                if x['message']['attachments'][0]['type'] == 'image':
                                    response = requests.get(x['message']['attachments'][0]['payload']['url'], stream=True)
                                    if dialogs[recipient_id].get_state() == 'choose_match':
                                        with open(recipient_id + '.png', 'wb') as out_file:
                                            shutil.copyfileobj(response.raw, out_file)
                                        dialogs[recipient_id].dialog_update('Thanks! You\'re nice')
                                        return "Message Processed"
                                else:
                                    bot.send_text_message(recipient_id, 'Send your photo please')

            elif 'standby' in event:
                for standby in event['standby']:
                    recipient_id = standby['sender']['id']
                    if 'postback' in standby and 'title' in standby['postback']:
                        dialogs[recipient_id].dialog_update(standby['postback']['title'])

    return "Message Processed"

def _user_init(id):
    user = User(id)
    global dialogs
    dialogs[id] = Dialog(game_observer, user)

def verify_fb_token(token_sent): 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    return random.choice(sample_responses)

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

def configure_bot():
    addr = "https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+ACCESS_TOKEN
    response = { 
        "get_started": {"payload": "Begin"},
        "greeting":[ {
            "locale": "default",
            "text": "FIX ME"
        }]  
    }
    resp = requests.post(addr, json = response)


def send_buttons(recipient_id, inbuttons, action_description):
    buttons = []
    for inbtn in inbuttons:
        button = Button(title=inbtn[0], type=inbtn[1], payload='other')
        buttons.append(button)
    bot.send_button_message(recipient_id, action_description, buttons)
    return "success"

def send_photo(recipient_id, photo_path):
    result = bot.send_image(recipient_id, photo_path)
    return result

def quick_reply_send(recipient_id, buttons, text):
    quick_replies = create_quick_reply(buttons)
    message = {
        "text": text,
        "quick_replies": quick_replies
    }
    bot.send_message(recipient_id, message)

def create_quick_reply(buttons):
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

import threading

class ObsereverThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def run(self):
        while True:
            sleep(5)
            print('upd')
            game_observer.update_state()

if __name__ == "__main__":
    configure_bot()

    observer_thread = ObsereverThread()
    observer_thread.start()

    app.run(threaded=True)

    observer_thread.join()
