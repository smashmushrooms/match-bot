import requests

from threading import Thread
from time import sleep
from flask import Flask, request

from objects import GameObserver
from objects import User

ACCESS_TOKEN = 'EAAEtr6bH9LEBAKXpBq732AhmrdwLV3EJynZCYFLnqRahVqOHEtZCWjD3IoKdOvLepZAmZAcPKlpEBlM16WB6WTroZCRkZAadHHl' \
               'X7tcYdApMZBLg8YQAQyp0JXKEJ031NG0ud5ztpAZAL1Dy6ZAAn3Rb6l80jMJEyiUbZC6PqrdZAGTLRmgZCMOh4NSLfV1FzEw7GDAZD'
VERIFY_TOKEN = 'ourbadpass123'
app = Flask(__name__)
game_observer = GameObserver()
users = {}

User._game_observer = game_observer

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
        print(output)
        for event in output['entry']:
            if 'messaging' in event:
                messaging = event['messaging']
                for x in messaging:
                    if 'message' not in x:
                        if 'postback' in x and 'payload' in x['postback']:
                            if x['postback']['payload'] == 'Begin':
                                recipient_id = x['sender']['id']
                                if recipient_id not in users:
                                    user = User(recipient_id)
                                    users[recipient_id] = user
                                users[recipient_id].dialog_update()
                    else:
                        if x.get('message'):
                            recipient_id = x['sender']['id']
                            if recipient_id not in users:
                                return "Message Processed"
                            if x['message'].get('text'):
                                message = x['message']['text']
                                users[recipient_id].dialog_update(message = message)
                            if x['message'].get('attachments'):
                                if x['message']['attachments'][0]['type'] == 'image':
                                    url = x['message']['attachments'][0]['payload']['url']
                                    print("out")
                                    if users[recipient_id].get_state() == 'choose_match':
                                        users[recipient_id].set_image_url(url)
                                        users[recipient_id].dialog_update()
                                        print("in")
                                        print(users[recipient_id].get_dialog().get_state())
                                        return "Message Processed"
                                else:
                                    users[recipient_id].send_message('Send your photo please :)')

            elif 'standby' in event:
                for standby in event['standby']:
                    recipient_id = standby['sender']['id']
                    if 'postback' in standby and 'title' in standby['postback']:
                        users[recipient_id].dialog_update(message = standby['postback']['title'])

    return "Message Processed"

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

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


class ObsereverThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            sleep(5)
            game_observer.update_state()


if __name__ == "__main__":
    configure_bot()

    observer_thread = ObsereverThread()
    observer_thread.start()

    app.run(threaded=True)

    observer_thread.join()
