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

    default_user1 = User(-1)
    default_user1._image_url = 'http://www.pxleyes.com/images/contests/dragan-effect/fullsize/egyptian-man-4deda4dc71f2f_hires.jpg'
    default_user1._current_lovely_team = 'Egypt'
    default_user1._state = None
    game_observer.add_fan(default_user1)

    default_user2 = User(-2)
    default_user2._image_url = 'http://oboi.cc/1920-1200-100-uploads/11_05_2013/view/201210/oboik.ru_53457.jpg'
    default_user2._current_lovely_team = 'Russia'
    default_user2._state = None
    game_observer.add_fan(default_user2)

    default_user3 = User(-3)
    default_user3._image_url = 'http://trendymen.ru/images/sliders/2597/slide27408.jpg'
    default_user3._current_lovely_team = 'Russia'
    default_user3._state = None
    game_observer.add_fan(default_user3)

    default_user4 = User(-4)
    default_user4._image_url = 'https://flytothesky.ru/wp-content/uploads/2017/11/1-25.jpg'
    default_user4._current_lovely_team = 'Russia'
    default_user4._state = None
    game_observer.add_fan(default_user4)

    default_user5 = User(-5)
    default_user5._image_url = 'https://lovelama.ru/uploads/71aa7a520ab3b2f8e6295f6a052c0eec/original_8cb48126ebdd4acc1c79925ec1fdc27c.jpg'
    default_user5._current_lovely_team = 'Russia'
    default_user5._state = None
    game_observer.add_fan(default_user5)

    default_user6 = User(-6)
    default_user6._image_url = 'http://my.goodhouse.com.ua/i/600_400/publications/3016/kak-sdelat-vashego-muzhchinu-samim-schastlivim-1036-14885.jpg'
    default_user6._current_lovely_team = 'Russia'
    default_user6._state = None
    game_observer.add_fan(default_user6)

    default_user7 = User(-7)
    default_user7._image_url = 'https://shkolazhizni.ru/img/content/i129/129800_or.jpg'
    default_user7._current_lovely_team = 'Russia'
    default_user7._state = None
    game_observer.add_fan(default_user7)

    default_user8 = User(-8)
    default_user8._image_url = 'http://media.filmz.ru/photos/full/filmz.ru_f_130717.jpg'
    default_user8._current_lovely_team = 'Russia'
    default_user8._state = None
    game_observer.add_fan(default_user8)

    default_user9 = User(-9)
    default_user9._image_url = 'http://lovejusta.ru/wp-content/uploads/2012/11/3-Colin-Farrell.jpg'
    default_user9._current_lovely_team = 'Russia'
    default_user9._state = None 
    game_observer.add_fan(default_user9)

    default_user10 = User(-10)
    default_user10._image_url = 'https://img.getbg.net/upload/full/8/80680_dzherard_2560x1600_(www.GetBg.net).jpg'
    default_user10._current_lovely_team = 'Russia'
    default_user10._state = None   
    game_observer.add_fan(default_user10)

    default_user11 = User(-11)
    default_user11._image_url = 'https://c1.staticflickr.com/9/8724/16976740485_fe1579c5a5_b.jpg'
    default_user11._current_lovely_team = 'Russia'
    default_user11._state = None  
    game_observer.add_fan(default_user11)       

    observer_thread = ObsereverThread()
    observer_thread.start()

    app.run(threaded=False)

    observer_thread.join()
