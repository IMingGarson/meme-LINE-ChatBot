from __future__ import unicode_literals
import os
import configparser
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageTemplateAction,
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

image_list = (
    (
        'https://memeprod.ap-south-1.linodeobjects.com/user-template/0b867ebd37ca67b8cbd7d0f009e74af0.png',
        'Buffed doge vs Cheems',
        '宵掰沒落魄得久',
        'Buffed doge vs Cheems',
        'buff-doge-and-cheems',
        'https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1620905238524.jpg'
    ),
    (
        'https://memeprod.ap-south-1.linodeobjects.com/user-template/143fed285c7a7f564f7bb77ec44786e4.png',
        'Captain America Elevator Fight',
        '一言不合就去練舞室打',
        'Captain America Elevator Fight',
        'cap-elevator',
        'https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1621251404320.jpg'
    ),
    (
        'https://memeprod.ap-south-1.linodeobjects.com/user-template/8e2cd9777e4965cac97359803b233768.png',
        'Drake',
        'No No No. Ah YES',
        'Drake',
        'drake',
        'https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1621664318318.jpg'
    ),
    (
        'https://memeprod.ap-south-1.linodeobjects.com/user-template/d9a0ccc04b5c801b6d93c73b10c7e257.png',
        '反正我很閒',
        '哪次不答應啦?',
        '反正我很閒',
        'yes-have-I-ever-said-no',
        'https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1608519817018.jpg'
    ),
    (
        'https://memeprod.ap-south-1.linodeobjects.com/user-template/46f63e21ef26e981b9477262d002fa60.png',
        '右邊!',
        '秒選右邊',
        'High way',
        'high-way',
        'https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1622034995182.jpg'
    ),
)

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    if (event.message.text == 'meme'):
        meme_columns = []
        for meme in image_list:
            meme_columns.append(
                CarouselColumn(
                    thumbnail_image_url = meme[0],
                    title = meme[1],
                    text = meme[2],
                    actions = [
                        PostbackAction(
                            label = '選擇這張',
                            text = f'選擇{meme[3]}',
                            data = meme[4]
                        )
                    ]
                )
            )
        print(meme_columns)
        Carousel_template = TemplateSendMessage(
            alt_text = 'Meme Carousel',
            template = CarouselTemplate(
                columns = meme_columns
            )
        )
        line_bot_api.reply_message(event.reply_token, Carousel_template)
    else:
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )

@handler.add(PostbackEvent)
def postCallBack(event):
    fileName = event.postback.data
    message = ImageSendMessage(
        original_content_url = "https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1620905238524.jpg",
        preview_image_url = "https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1620905238524.jpg"
    )
    for meme in image_list:
        if fileName == meme[4]:
            message = ImageSendMessage(
                original_content_url = meme[5],
                preview_image_url = meme[5]
            )
    line_bot_api.reply_message(
        event.reply_token,
        message
    )

if __name__ == "__main__":
    app.run()
