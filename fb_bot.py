import requests

from threading import Thread
from time import sleep
from japronto import Application
from functools import wraps
from sys import stderr

from objects import GameObserver
from objects import User
from re import sub

ACCESS_TOKEN = 'EAAEtr6bH9LEBAKXpBq732AhmrdwLV3EJynZCYFLnqRahVqOHEtZCWjD3IoKdOvLepZAmZAcPKlpEBlM16WB6WTroZCRkZAadHHl' \
               'X7tcYdApMZBLg8YQAQyp0JXKEJ031NG0ud5ztpAZAL1Dy6ZAAn3Rb6l80jMJEyiUbZC6PqrdZAGTLRmgZCMOh4NSLfV1FzEw7GDAZD'
VERIFY_TOKEN = 'ourbadpass123'
game_observer = GameObserver()
users = {}

User._game_observer = game_observer


def response_text_decorator(func):
    @wraps(func)
    def wrapper(request):
        return request.Response(text=func(request))
    return wrapper


# We will receive messages that Facebook sends our bot at this endpoint
#@app.route("/", methods=['GET', 'POST'])
@response_text_decorator
def receive_message(request):
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        for attr in dir(request):
            if not attr.startswith('__'):
                try:
                    print(attr, getattr(request, attr))
                except Exception:
                    print(attr, file=stderr)
        token_sent = request.query.get("hub.verify_token")
        return verify_fb_token(request, token_sent)
    else:
        body_str = request.body.decode()
        body_str = sub('true', 'True', body_str)
        body_str = sub('false', 'False', body_str)
        body_str = sub('null', 'None', body_str)
        output = eval(body_str)
        print(output)
        for event in output['entry']:
            if 'messaging' in event:
                messaging = event['messaging']
                for message in messaging:
                    if 'message' not in message:
                        if 'postback' in message and 'payload' in message['postback']:
                            if message['postback']['payload'] == 'Begin':
                                sender_id = message['sender']['id']
                                if sender_id not in users:
                                    user = User(sender_id)
                                    users[sender_id] = user
                                    users[sender_id].dialog_update()
                                else:
                                    raise ValueError('Attempt to begin interaction twice')
                    else:
                        if message.get('message'):
                            sender_id = message['sender']['id']
                            if sender_id not in users:
                                user = User(sender_id)
                                users[sender_id] = user
                                users[sender_id].dialog_update()
                                raise ValueError('Invalid user id: user was not registred')
                            if message['message'].get('text'):
                                text = message['message']['text']
                                users[sender_id].dialog_update(text=text)
                            if message['message'].get('attachments'):
                                if message['message']['attachments'][0]['type'] == 'image':
                                    url = message['message']['attachments'][0]['payload']['url']
                                    users[sender_id].dialog_update(url)
                                else:
                                    users[sender_id].dialog_update()
            elif 'standby' in event:
                for standby in event['standby']:
                    sender_id = standby['sender']['id']
                    if 'postback' in standby and 'title' in standby['postback']:
                        users[sender_id].dialog_update(text=standby['postback']['title'])


def verify_fb_token(request, token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.query.get("hub.challenge")
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


class ObserverThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            sleep(5)
            game_observer.update_state()


if __name__ == "__main__":
    configure_bot()

    '''
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
    default_user10._image_url = 'https://brjunetka.ru/wp-content/uploads/2014/12/Ulyibaytes.jpg'
    default_user10._current_lovely_team = 'Russia'
    default_user10._state = None   
    game_observer.add_fan(default_user10)

    default_user11 = User(-11)
    default_user11._image_url = 'https://c1.staticflickr.com/9/8724/16976740485_fe1579c5a5_b.jpg'
    default_user11._current_lovely_team = 'Russia'
    default_user11._state = None  
    game_observer.add_fan(default_user11)       
    '''

    observer_thread = ObserverThread()
    observer_thread.start()

    app = Application()
    app.router.add_route('/', receive_message, methods=['GET', 'POST'])
    app.run(host='127.0.0.1', port=5000, worker_num=1)

    observer_thread.join()
