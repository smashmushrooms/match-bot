#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Element, Button
import requests
from game_observer import GameObserver
from objects.user import User
from time import sleep
#from game_observer import GameObserver

app = Flask(__name__)
ACCESS_TOKEN = 'EAAEtr6bH9LEBAKXpBq732AhmrdwLV3EJynZCYFLnqRahVqOHEtZCWjD3IoKdOvLepZAmZAcPKlpEBlM16WB6WTroZCRkZAadHHlX7tcYdApMZBLg8YQAQyp0JXKEJ031NG0ud5ztpAZAL1Dy6ZAAn3Rb6l80jMJEyiUbZC6PqrdZAGTLRmgZCMOh4NSLfV1FzEw7GDAZD'
VERIFY_TOKEN = 'ourbadpass123'
bot = Bot(ACCESS_TOKEN)
game_observer = GameObserver()

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        print(output)
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                if 'message' in x:
                    if x.get('message'):
                        recipient_id = x['sender']['id']
                        user = game_observer.find_user(recipient_id)
                        if x['message'].get('text'):
                            message = x['message']['text']
                            send_message(recipient_id, message)
                            user.get_dialog().dialog(message)
                        if x['message'].get('attachments'):
                            for att in x['message'].get('attachments'):
                                pass#bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])
                else:
                    if 'postback' in x and 'payload' in x['postback']:
                        if x['postback']['payload'] == 'Begin':
                            recipient_id = x['sender']['id']
                            user = User(recipient_id, game_observer)
                            game_observer.add_user(user)
                            user.get_dialog().start_dialog()
                            dialog.start_dialog()
                            pass
    return "Message Processed"

def verify_fb_token(token_sent): 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    return random.choice(sample_responses)

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    quick_reply_send(recipient_id, [['Test', 'My test message', 'https://www.partan.eu/static/img/flags/xru.png.pagespeed.ic.ksQyMMYVcM.png']], 'Yess')
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
    print (resp)


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

if __name__ == "__main__":
    configure_bot()
    app.run()

    while (True):
        sleep(30)
        game_observer.update()
