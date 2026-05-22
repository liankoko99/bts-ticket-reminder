import os
import requests
from datetime import datetime

TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']

events = [
    ("高雄 ARMY Presale", "2026-06-02 12:00"),
    ("高雄 General Onsale", "2026-06-04 12:00"),
    ("新加坡 ARMY Presale", "2026-06-03 12:00"),
    ("新加坡 Live Nation Presale", "2026-06-04 12:00"),
    ("新加坡 Klook Sale", "2026-06-05 12:00"),
    ("新加坡 General Onsale", "2026-06-05 12:00"),
    ("吉隆坡 ARMY Presale", "2026-06-03 11:00"),
    ("吉隆坡 Live Nation Presale", "2026-06-04 11:00"),
    ("吉隆坡 Trip.com Presale", "2026-06-04 09:00"),
    ("吉隆坡 General Onsale", "2026-06-05 11:00"),
    ("香港 ARMY Presale", "2026-06-09 11:00"),
    ("香港 Live Nation Presale", "2026-06-10 11:00"),
    ("香港 Trip.com Presale", "2026-06-10 10:00"),
    ("香港 General Onsale", "2026-06-11 11:00"),
]

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {'chat_id': CHAT_ID, 'text': text}
    requests.get(url, params=params)

now = datetime.now()

for name, time_str in events:
    event_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    diff = event_time - now
    minutes_diff = diff.total_seconds() / 60
    
    if 1439 <= minutes_diff <= 1441:
        send_msg(f"📅 明日提醒：{name} 將於明日開賣，請做好準備！")
    elif 59 <= minutes_diff <= 61:
        send_msg(f"📢 售票倒數：{name} 仲有 1 個鐘開賣！")
    elif 14 <= minutes_diff <= 16:
        send_msg(f"🚨 最後衝刺：{name} 仲有 15 分鐘！快啲準備好！")