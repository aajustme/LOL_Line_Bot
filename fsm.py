from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_message, find_champions, get_runes_img, get_position


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def on_enter_user(self):
        print('enter user')
        self.hero_name = None
        self.pos_list = None
        self.hero_pos = None

    def is_going_to_Name(self, event):
        text = event.message.text
        return text.lower() == "hero"

    def on_enter_Name(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入英雄名稱")

    def is_going_to_Position(self, event):
        text = event.message.text
        name = find_champions(text)
        if name != None:
            self.hero_name = name
            self.pos_list = get_position(self.hero_name)
            if len(self.pos_list) == 1:
                return False
            else:
                return True
        else:
            return False

    def is_going_to_Infor_from_Name(self, event):
        if self.pos_list != None and len(self.pos_list) == 1:
            if self.pos_list[0] == 'sup':
                self.hero_pos = 'support'
            elif self.pos_list[0] == 'jg':
                self.hero_pos = 'jungle'
            else:
                self.hero_pos = self.pos_list[0]
            return True
        else:
            return False 

    def on_enter_Position(self, event):
        self.pos_list = get_position(self.hero_name)
        reply_token = event.reply_token
        reply_str = f"請輸入要打的位置({self.pos_list[0]}"
        for i in range(len(self.pos_list)-1):
            reply_str += f"/{self.pos_list[i+1]}"
        reply_str += ")"
        send_text_message(reply_token, reply_str)

    def is_going_to_Infor(self, event):
        text = event.message.text.lower()
        if text in self.pos_list:
            if text == 'sup':
                self.hero_pos = 'support'
            elif text == 'jg':
                self.hero_pos = 'jungle'
            else:
                self.hero_pos = text
            return True
        else:
            return False

    def on_enter_Infor(self, event):
        reply_token = event.reply_token
        #send_text_message(reply_token, self.hero_name+', '+self.hero_pos)
        get_runes_img(self.hero_name, self.hero_pos)
        ngrok_url = 'https://8912-2001-b011-e00a-1b7e-d8b1-cfc3-d02e-6492.jp.ngrok.io'
        url = ngrok_url + "/show-img"
        send_image_message(reply_token, url)
        self.go_back()
