import os
import requests
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin
import difflib
import numpy as np
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt
import cv2

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

offset = [[4, 108], [72, 0], [72, 108], [72, 216], [144, 0], [144, 108], [144, 216], [216, 0], [216, 108], [216, 216], [288, 0], [288, 108], [288, 216],
          [72, 420], [144, 312], [144, 420], [144, 528], [216, 312], [216, 420], [216, 528], [288, 312], [288, 420], [288, 528],
          [144, 624], [144, 696], [144, 768], [222, 624], [222, 696], [222, 768], [300, 624], [300, 696], [300, 768]]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

hero_dict = {
            '厄薩斯' : 'aatrox',
            '劍魔' : 'aatrox',
            '阿璃' : 'ahri',
            '阿卡莉' : 'akali',
            '埃可尚' : 'akshan',
            '亞歷斯塔' : 'alistar',
            '牛' : 'alistar',
            '阿姆姆' : 'amumu',
            '嬰靈' : 'amumu',
            '艾妮維亞' : 'anivia',
            '冰鳥' : 'anivia',
            '安妮' : 'annie',
            '亞菲利歐' : 'aphelios',
            '艾希' : 'ashe',
            '翱銳龍獸' : 'aurelionSol',
            '龍獸' : 'aurelionSol',
            '阿祈爾' : 'azir',
            '沙皇' : 'azir',
            '巴德' : 'bard', 
            '貝爾薇斯' : 'belveth',
            '布里茨' : 'blitzcrank',
            '機器人' : 'blitzcrank',
            '布蘭德' : 'brand',
            '火人' : 'brand',
            '布郎姆' : 'braum',
            '凱特琳' : 'caitlyn',
            '卡蜜兒' : 'camille',
            '卡莎碧雅' : 'cassiopeia',
            '蛇女' : 'cassiopeia',
            '科加斯' : 'chogath',
            '大蟲' : 'chogath',
            '庫奇' : 'corki',
            '飛機' : 'corki',
            '達瑞斯' : 'darius',
            '諾手' : 'darius',
            '黛安娜' : 'diana',
            '達瑞文' : 'draven',
            '蒙多醫生' : 'drmundo',
            '蒙多' : 'drmundo',
            '艾克' : 'ekko',
            '伊莉絲' : 'elise',
            '蜘蛛' : 'elise',
            '伊芙琳' : 'evelynn',
            '伊澤瑞爾' : 'ezreal',
            '伊澤' : 'ezreal',
            'ez' : 'ezreal',
            '費德提克' : 'fiddlesticks',
            '稻草人' : 'fiddlesticks',
            '菲歐拉' : 'fiora',
            '飛斯' : 'fizz',
            '小於人' : 'fizz',
            '加里歐' : 'galio',
            '剛普朗克' : 'gangplank',
            '剛普' : 'gangplank',
            '船長' : 'gangplank',
            '蓋倫' : 'garen',
            '吶兒' : 'gnar',
            '古拉格斯' : 'gragas',
            '酒桶' : 'gragas',
            '葛雷夫' : 'graves',
            '南槍' : 'graves',
            '關' : 'gwen',
            '赫克林' : 'hecarim',
            '人馬' : 'hecarim',
            '漢默丁格' : 'heimerdinger',
            '泡麵投' : 'heimerdinger',
            '伊羅旖' : 'illaoi',
            '伊羅一' : 'illaoi',
            '伊羅其' : 'illaoi',
            '伊瑞莉雅' : 'irelia',
            '刀妹' : 'irelia',
            '埃爾文' : 'ivern',
            '珍娜' : 'janna',
            '嘉文四世' : 'jarvaniv',
            '嘉文' : 'jarvaniv',
            '賈克斯' : 'jax',
            '武器' : 'jax', 
            '杰西' : 'jayce',
            '燼' : 'jhin',
            '吉茵珂絲' : 'jinx',
            '凱莎' : 'kaisa',
            '克黎思妲' : 'kalista',
            '滑板鞋' : 'kalista',
            '卡瑪' : 'karma',
            '卡爾瑟斯' : 'karthus',
            '死歌' : 'karthus',
            '卡薩丁' : 'kassadin',
            '卡特蓮娜' : 'katarina',
            '卡特' : 'katarina',
            '凱爾' : 'kayle',
            '慨影' : 'kayn',
            '凱能' : 'kennen',
            '卡力斯' : 'khazix',
            '螳螂' : 'khazix',
            '鏡爪' : 'kindred',
            '克雷德' : 'kled',
            '寇格魔' : 'kogMaw',
            '大嘴' : 'kogMaw',
            '卡桑帝' : 'ksante',
            '勒布朗' : 'leblanc',
            '李星' : 'leesin',
            '雷歐娜' : 'leona',
            '莉莉亞' : 'lillia',
            '麗珊卓' : 'lissandra',
            '冰女' : 'lissandra',
            '路西恩' : 'lucian',
            '露璐' : 'lulu',
            '拉克絲' : 'lux',
            '墨菲特' : 'malphite',
            '石頭人' : 'malphite',
            '馬爾札哈' : 'malzahar',
            '茂凱' : 'maokai',
            '易大師' : 'masteryi',
            '好運姐' : 'missfortune',
            '悟空' : 'monkeyking',
            '魔鬥凱薩' : 'mordekaiser',
            '魔鬥' : 'mordekaiser',
            '魔甘娜' : 'morgana',
            '娜米' : 'nami',
            '納瑟斯' : 'nasus',
            '狗頭' : 'nasus',
            '納帝魯斯' : 'nautilus',
            '滷蛋' : 'nautilus',
            '妮可' : 'neeko',
            '奈德麗' : 'nidalee',
            '淣菈' : 'nilah',
            '夜曲' : 'nocturne',
            '努努和威朗普' : 'nunu',
            '努努' : 'nunu',
            '歐拉夫' : 'olaf',
            '奧莉安娜' : 'orianna',
            '球女' : 'orianna',
            '鄂爾' : 'ornn',
            '潘森' : 'pantheon',
            '波比' : 'poppy',
            '派克' : 'pyke',
            '姬亞娜' : 'qiyana',
            '葵恩' : 'quinn',
            '銳空' : 'rakan',
            '拉姆斯' : 'rammus',
            '烏龜' : 'rammus',
            '雷珂煞' : 'reksai',
            '銳兒' : 'rell',
            '睿娜妲．格萊斯克' : 'renata',
            '瑞納達' : 'renata',
            '雷尼克頓' : 'renekton',
            '雷葛爾' : 'rengar',
            '獅子' : 'rengar',
            '雷玟' : 'riven',
            '藍寶' : 'rumble',
            '雷茲' : 'ryze',
            '煞蜜拉' : 'samira',
            '史瓦妮' : 'sejuani',
            '朱女' : 'sejuani',
            '姍娜' : 'senna',
            '瑟菈紛' : 'seraphine',
            '賽特' : 'sett',
            '薩科' : 'shaco',
            '慎' : 'shen',
            '希瓦娜' : 'shyvana',
            '辛吉德' : 'singed',
            '闢南' : 'singed',
            '賽恩' : 'sion',
            '希維爾' : 'sivir',
            '輪子媽' : 'sivir',
            '史加納' : 'skarner',
            '蠍子' : 'skarner',
            '索娜' : 'sona',
            '索拉卡' : 'soraka',
            '斯溫' : 'swain',
            '賽勒斯' : 'sylas',
            '星朵拉' : 'syndra',
            '貪啃奇' : 'tahmKench',
            '塔莉雅' : 'taliyah',
            '塔隆' : 'talon',
            '塔里克' : 'taric',
            '提摩' : 'teemo',
            '瑟雷西' : 'thresh',
            '崔絲塔娜' : 'tristana',
            '泡娘' : 'tristana',
            '特朗德' : 'trundle',
            '泰達米爾' : 'tryndamere',
            '鰻王' : 'tryndamere',
            '逆命' : 'twistedfate',
            '圖奇' : 'twitch',
            '老鼠' : 'twitch',
            '烏迪爾' : 'udyr',
            '烏爾加特' : 'urgot',
            '垃圾車' : 'urgot',
            '法洛士' : 'varus',
            '汎' : 'vayne',
            '維迦' : 'veigar',
            '威寇茲' : 'velkoz',
            '薇可絲' : 'vex',
            '菲艾' : 'vi',
            '維爾戈' : 'viego',
            '維克特' : 'viktor',
            '弗拉迪米爾' : 'vladimir',
            '弗力貝爾' : 'volibear',
            '沃維克' : 'warwick',
            '狼人' : 'warwick',
            '剎雅' : 'xayah',
            '齊勒斯' : 'xerath',
            '趙信' : 'xinzhao',
            '犽宿' : 'yasuo',
            '犽凝' : 'yone',
            '約瑞科' : 'yorick',
            '悠咪' : 'yuumi',
            '札克' : 'zac',
            '劫' : 'zed',
            '婕莉' : 'zeri',
            '希格斯' : 'ziggs',
            '極靈' : 'zilean',
            '柔依' : 'zoe',
            '枷蘿' : 'zyra',
        }

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    return "OK"

def send_image_message(reply_token, url):
    print(url)
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, ImageSendMessage(original_content_url = url, preview_image_url = url))
    return "OK"

def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

def get_name(name):
    name_list = lazy_pinyin(name)
    ret_name = name_list[0]
    for i in name_list[1:]:
        ret_name += (' '+i)
    return ret_name

def find_champions(name):
    input_name = get_name(name)
    max_rate = 0.5
    res = None
    for key in hero_dict:
        rate = string_similar(input_name, get_name(key))
        if rate > max_rate:
            res = hero_dict[key]
            max_rate = rate
    return res

def get_position(hero):
    r = requests.get(f"https://www.op.gg/champions/{hero}", headers = headers)
    soup = BeautifulSoup(r.text,"html.parser")
    sel = soup.body.div.find('div', id = 'content-header').div.div.div.div.find_all('a')
    pos_list = []
    for i in range(len(sel)):
        if sel[i]['data-value'] == 'support':
            pos_list.append('sup')
        elif sel[i]['data-value'] == 'jungle':
            pos_list.append('jg')
        else:
            pos_list.append(sel[i]['data-value'])
    return pos_list

def get_runes_img(hero, position):
    r = requests.get(f"https://www.op.gg/champions/{hero}/{position}/runes?region=global&tier=platinum_plus", headers = headers)
    soup = BeautifulSoup(r.text,"html.parser")
    if soup.tbody.tr.div == None:
        return None
    tags = soup.tbody.tr.div.find_all("img")
    print(len(tags))
    bg = np.zeros((348,864,3), dtype='uint8')
    bg[:,:,:] = 255
    
    for i in range(32):
        URL = tags[i]['src']
        urllib.request.urlretrieve(URL, "t.png")
        img = cv2.imread('t.png', cv2.IMREAD_UNCHANGED)
        if i < 32-9:
            #img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
            bg = cv2.circle(bg, (offset[i][1]+28+20, offset[i][0]+28), 28, (0, 0, 0), -1)
        else:
            #img = cv2.resize(img, (24, 24), interpolation=cv2.INTER_AREA)
            bg = cv2.circle(bg, (offset[i][1]+24+20, offset[i][0]+24), 24, (0, 0, 0), -1)
            
        bg[np.where(img[:,:,3] > 0)[0]+offset[i][0],np.where(img[:,:,3] > 0)[1]+offset[i][1]+20,:] = img[np.where(img[:,:,3] > 0)[0],np.where(img[:,:,3] > 0)[1],0:3]

    cv2.imwrite('./static/ttt.png',bg)