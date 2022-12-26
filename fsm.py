from transitions.extensions import GraphMachine
import os

from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, PostbackTemplateAction, CarouselColumn

from utils import send_text_message, send_image_message, send_message, send_column_message, send_button_message
from utils import find_champions, get_runes_img, get_position, get_items_img, get_skill_order, get_counter_list, get_tier_list

web_url = os.getenv("WEB_URL", None)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_back(self, event):
        return event.message.text.lower() == 'back'

    def is_going_to_Menu(self, event):
        return event.message.text.lower() == 'menu'

    def on_enter_Menu(self, event):
        reply_token = event.reply_token
        self.hero_name = None
        self.pos_list = None
        self.hero_pos = None
        title = '主選單'
        text = '請選擇操作：'
        btn = [
            PostbackTemplateAction(
                label='英雄資訊',
                text='英雄資訊',
                data='英雄資訊'
            ),
            PostbackTemplateAction(
                label='強度表',
                text='強度表',
                data='強度表'
            ),
        ]
        #ngrok_url = 'https://ebc2-2001-b011-e00a-1b7e-e83a-ea2-18ba-9700.jp.ngrok.io'
        url = web_url + '/show-menu-img'
        send_button_message(reply_token, title, text, url, btn)

    def is_going_to_TierPosition(self, event):
        return event.message.text == '強度表'

    def on_enter_TierPosition(self, event):
        reply_token = event.reply_token
        cols = [
            CarouselColumn(
                thumbnail_image_url='https://cdngarenanow-a.akamaihd.net/webmain/static/pss/lol/items_splash/garen_0.jpg',
                title='上路',
                text='top',
                actions=[PostbackTemplateAction(label='Click Me', text='top', data='top')]
            ),
            CarouselColumn(
                thumbnail_image_url='https://cdngarenanow-a.akamaihd.net/webmain/static/pss/lol/items_splash/ryze_0.jpg',
                title='中路',
                text='mid',
                actions=[PostbackTemplateAction(label='Click Me', text='mid', data='mid')]
            ),
            CarouselColumn(
                thumbnail_image_url='https://cdngarenanow-a.akamaihd.net/webmain/static/pss/lol/items_splash/jarvaniv_0.jpg',
                title='打野',
                text='jungle',
                actions=[PostbackTemplateAction(label='Click Me', text='jungle', data='jungle')]
            ),
            CarouselColumn(
                thumbnail_image_url='https://cdngarenanow-a.akamaihd.net/webmain/static/pss/lol/items_splash/ashe_0.jpg',
                title='射手',
                text='adc',
                actions=[PostbackTemplateAction(label='Click Me', text='adc', data='adc')]
            ),
            CarouselColumn(
                thumbnail_image_url='https://cdngarenanow-a.akamaihd.net/webmain/static/pss/lol/items_splash/janna_0.jpg',
                title='輔助',
                text='support',
                actions=[PostbackTemplateAction(label='Click Me', text='support', data='support')]
            ),
        ]
        send_column_message(reply_token, cols)

    def is_going_to_TierList(self, event):
        self.tier_pos = event.message.text
        return self.tier_pos in ['top', 'mid', 'jungle', 'adc', 'support']

    def on_enter_TierList(self, event):
        reply_token = event.reply_token
        ret_list = get_tier_list(self.tier_pos)
        message = []
        for i in range(len(ret_list)):
            message.append(TextSendMessage(text=ret_list[i]))
        send_message(reply_token, message)

    def is_going_to_Hero(self, event):
        return event.message.text == '英雄資訊'

    def on_enter_Hero(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入英雄名稱")

    def is_going_to_HeroPosition(self, event):
        text = event.message.text
        name = find_champions(text)
        if name != None:
            self.hero_name = name
            return True
        else:
            return False

    def on_enter_HeroPosition(self, event):
        self.pos_list = get_position(self.hero_name)
        reply_token = event.reply_token
        title = f'您搜尋的英雄為：{self.hero_name}'
        text = '請選擇要打的位置：'
        btn = []
        for i in range(len(self.pos_list)):
            btn.append(PostbackTemplateAction(label=self.pos_list[i], text=self.pos_list[i], data=self.pos_list[i]))
        url = f'https://cdngarenanow-a.akamaihd.net/webmain/static/pss/lol/items_splash/{self.hero_name}_0.jpg'
        send_button_message(reply_token, title, text, url, btn)

    def is_going_to_HeroMenu(self, event):
        self.hero_pos = event.message.text
        return self.hero_pos in self.pos_list

    def on_enter_HeroMenu(self, event):
        reply_token = event.reply_token
        title = f'{self.hero_name}, {self.hero_pos}'
        text = '請選擇操作：'
        btn = [
            PostbackTemplateAction(
                label='構築',
                text='構築',
                data='構築'
            ),
            PostbackTemplateAction(
                label='克制',
                text='克制',
                data='克制'
            ),
        ]
        send_button_message(reply_token, title, text, None, btn)

    def is_going_to_Build(self, event):
        return event.message.text == '構築'
    
    def on_enter_Build(self, event):
        reply_token = event.reply_token
        #send_text_message(reply_token, self.hero_name+', '+self.hero_pos)
        get_runes_img(self.hero_name, self.hero_pos)
        get_items_img(self.hero_name, self.hero_pos)
        #ngrok_url = 'https://ebc2-2001-b011-e00a-1b7e-e83a-ea2-18ba-9700.jp.ngrok.io'
        runes_url = web_url + "/show-runes"
        items_url = web_url + "/show-items"
        message = []
        message.append(TextSendMessage(text='推薦符文：'))
        message.append(ImageSendMessage(original_content_url = runes_url, preview_image_url = runes_url))
        message.append(TextSendMessage(text='推薦出裝：'))
        message.append(ImageSendMessage(original_content_url = items_url, preview_image_url = items_url))
        message.append(TextSendMessage(text='推薦技能點法：'+get_skill_order(self.hero_name, self.hero_pos)))

        send_message(reply_token, message)

    def is_going_to_Counter(self, event):
        return event.message.text == '克制'

    def on_enter_Counter(self, event):
        reply_token = event.reply_token
        countered, counter = get_counter_list(self.hero_name, self.hero_pos)
        message = []
        message.append(TextSendMessage(text='克制(英雄：勝率)\n'+counter))
        message.append(TextSendMessage(text='被克制(英雄：勝率)\n'+countered))
        send_message(reply_token, message)