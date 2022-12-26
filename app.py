import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_image_message

load_dotenv()


machine = TocMachine(
    states=["user", "Menu", "Hero", "TierPosition", "TierList", "HeroPosition", "HeroMenu", "Build", "Counter"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "Menu",
            "conditions": "is_going_to_Menu",
        },
        {
            "trigger": "advance",
            "source": "Menu",
            "dest": "Hero",
            "conditions": "is_going_to_Hero",
        },
        {
            "trigger": "advance",
            "source": "Menu",
            "dest": "TierPosition",
            "conditions": "is_going_to_TierPosition",
        },
        {
            "trigger": "advance",
            "source": "TierPosition",
            "dest": "TierList",
            "conditions": "is_going_to_TierList",
        },
        {
            "trigger": "advance",
            "source": "Hero",
            "dest": "HeroPosition",
            "conditions": "is_going_to_HeroPosition",
        },
        {
            "trigger": "advance",
            "source": "HeroPosition",
            "dest": "HeroMenu",
            "conditions": "is_going_to_HeroMenu",
        },
        {
            "trigger": "advance",
            "source": "HeroMenu",
            "dest": "Build",
            "conditions": "is_going_to_Build",
        },
        {
            "trigger": "advance",
            "source": "HeroMenu",
            "dest": "Counter",
            "conditions": "is_going_to_Counter",
        },
        # back
        {
            "trigger": "advance",
            "source": "Menu",
            "dest": "Menu",
            "conditions": "is_going_back",
        },
        {
            "trigger": "advance",
            "source": "Hero",
            "dest": "Menu",
            "conditions": "is_going_back",
        },
        {
            "trigger": "advance",
            "source": "TierPosition",
            "dest": "Menu",
            "conditions": "is_going_back",
        },
        {
            "trigger": "advance",
            "source": "TierList",
            "dest": "TierPosition",
            "conditions": "is_going_back",
        },
        {
            "trigger": "advance",
            "source": "HeroPosition",
            "dest": "Hero",
            "conditions": "is_going_back",
        },
        {
            "trigger": "advance",
            "source": "HeroMenu",
            "dest": "HeroPosition",
            "conditions": "is_going_back",
        },
        {
            "trigger": "advance",
            "source": "Build",
            "dest": "HeroMenu",
            "conditions": "is_going_back",
        },
        {
            "trigger": "advance",
            "source": "Counter",
            "dest": "HeroMenu",
            "conditions": "is_going_back",
        },
        # menu
        {
            "trigger": "advance",
            "source": "Menu",
            "dest": "Menu",
            "conditions": "is_going_to_Menu",
        },
        {
            "trigger": "advance",
            "source": "Hero",
            "dest": "Menu",
            "conditions": "is_going_to_Menu",
        },
        {
            "trigger": "advance",
            "source": "TierPosition",
            "dest": "Menu",
            "conditions": "is_going_to_Menu",
        },
        {
            "trigger": "advance",
            "source": "TierList",
            "dest": "Menu",
            "conditions": "is_going_to_Menu",
        },
        {
            "trigger": "advance",
            "source": "HeroPosition",
            "dest": "Menu",
            "conditions": "is_going_to_Menu",
        },
        {
            "trigger": "advance",
            "source": "HeroMenu",
            "dest": "Menu",
            "conditions": "is_going_to_Menu",
        },
        {
            "trigger": "advance",
            "source": "Build",
            "dest": "Menu",
            "conditions": "is_going_to_Menu",
        },
        {
            "trigger": "advance",
            "source": "Counter",
            "dest": "Menu",
            "conditions": "is_going_to_Menu",
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

'''
        {
            "trigger": "advance",
            "source": "HeroPosition",
            "dest": "Infor",
            "conditions": "is_going_to_Infor",
        },
        {"trigger": "go_back", "source": "Infor", "dest": "user"},
'''

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
web_url = os.getenv("WEB_URL", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        if event.message.text.lower() == 'show':
            url = web_url + '/show-fsm'
            send_image_message(event.reply_token, url)
        else:
            print(f"\nFSM STATE: {machine.state}")
            print(f"REQUEST BODY: \n{body}")
            response = machine.advance(event)
            if response == False:
                send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")

@app.route("/show-menu-img", methods=["GET"])
def show_menu_img():
    return send_file("./static/menu.jpg", mimetype="image/jpg")

@app.route("/show-runes", methods=["GET"])
def show_runes():
    return send_file("./static/runes.png", mimetype="image/png")

@app.route("/show-items", methods=["GET"])
def show_items():
    return send_file("./static/items.png", mimetype="image/png")

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
