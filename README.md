# 英雄聯盟小助手
## 使用說明
1. Install package ( python version = 3.8 )
```
pip install -r requirements.txt
``` 
2. Deploy locally
```shell
ngrok http 8000
python app.py
```
2. Modify .env
```shell
LINE_CHANNEL_SECRET=1190fcbb2fe2efe76e23195b65232db9
LINE_CHANNEL_ACCESS_TOKEN=5MhD/9lo3NAxUWWvzv7c+naAeApMs/AWDAft+iMU2CMXH+N94LG1UK5x9+xFiCHWiNx+6/G1h85Q9LbCVms4XzGJ4LVJU8g81EN2toZDZcFYIgFKqYjHCh4eD8wQAoKKovq86W19h581vdi5fKobsgdB04t89/1O/w1cDnyilFU=
PORT=8000
WEB_URL=https://5eab-2001-b011-e00a-1b7e-ec22-2194-e954-fc16.jp.ngrok.io
```
## 執行成果
### 初始歡迎訊息
<img src="./img/initial.png" alt="drawing" width="400"/>  
  
### 主選單
<img src="./img/menu.png" alt="drawing" width="400"/>  
  
### 查詢名稱(可模糊化查詢)
<img src="./img/HeroName.png" alt="drawing" width="400"/>  
  
### 選擇位置
<img src="./img/HeroPos.png" alt="drawing" width="400"/>  
  
### 選擇構築or克制
<img src="./img/HeroMenu.png" alt="drawing" width="400"/>  
  
### 構築：出裝、符文、技能點法
<img src="./img/Build.png" alt="drawing" width="400"/>  
  
### 返回
<img src="./img/Back.png" alt="drawing" width="400"/>  
  
### 查看克制關係
<img src="./img/Counter.png" alt="drawing" width="400"/>  
  
### 回到主畫面
<img src="./img/back_to_menu.png" alt="drawing" width="400"/>  
  
### 英雄強度表
<img src="./img/Tier.png" alt="drawing" width="400"/>  
  
### 選擇位置
<img src="./img/TierInfor.png" alt="drawing" width="400"/>  
  
### 展示fsm
<img src="./img/show.png" alt="drawing" width="400"/>  
  
### fsm
<img src="./img/fsm.png" alt="drawing" width="800"/>
