import random
import shutil
import requests

from threading import Thread
from time import sleep
from flask import Flask, request
from numpy import random
from pymessenger import Button
from pymessenger.bot import Bot

from objects import Dialog
from objects import GameObserver
from objects import User

app = Flask(__name__)
ACCESS_TOKEN = 'EAAEtr6bH9LEBAKXpBq732AhmrdwLV3EJynZCYFLnqRahVqOHEtZCWjD3IoKdOvLepZAmZAcPKlpEBlM16WB6WTroZCRkZAadHHl' \
               'X7tcYdApMZBLg8YQAQyp0JXKEJ031NG0ud5ztpAZAL1Dy6ZAAn3Rb6l80jMJEyiUbZC6PqrdZAGTLRmgZCMOh4NSLfV1FzEw7GDAZD'
VERIFY_TOKEN = 'ourbadpass123'
bot = Bot(ACCESS_TOKEN)
game_observer = GameObserver()
dialogs = {}


# We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
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
                                    url = x['message']['attachments'][0]['payload']['url']
                                    if dialogs[recipient_id].get_state() == 'choose_match':
                                        dialogs[recipient_id].get_user().set_url(url)
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
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!",
                        "We're greatful to know you :)"]
    return random.choice(sample_responses)


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"


def configure_bot():
    addr = "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" + ACCESS_TOKEN
    response = {
        "get_started": {"payload": "Begin"},
        "greeting": [{
            "locale": "default",
            "text": "FIX ME"
        }]
    }
    resp = requests.post(addr, json=response)


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


def observer_thread():
    while True:
        sleep(1)
        game_observer.update()


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
