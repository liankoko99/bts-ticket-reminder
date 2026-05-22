import os
import requests
from datetime import datetime

TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']
SENT_FILE = "sent_notifications.txt"

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

def send_msg(text, event_name, type):
    key = f"{event_name}_{type}"
    # 讀取已發送記錄
    sent = []
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r") as f:
            sent = f.read().splitlines()
    
    # 如果已經發送過，就跳過
    if key in sent:
        return

    # 發送訊息
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {'chat_id': CHAT_ID, 'text': text}
    response = requests.get(url, params=params)
    
    # 如果成功，記錄下來
    if response.status_code == 200:
        with open(SENT_FILE, "a") as f:
            f.write(key + "\n")

now = datetime.now()

# 開賣提醒邏輯
for name, time_str in events:
    event_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    if event_time < now: continue
        
    diff = event_time - now
    minutes_diff = diff.total_seconds() / 60
    
    # 判斷並發送 (每個時段只會發一次)
    if 1439 <= minutes_diff <= 1441:
        send_msg(f"📅 明日提醒：{name} 將於明日開賣，請做好準備！", name, "day_before")
    elif 59 <= minutes_diff <= 61:
        send_msg(f"📢 售票倒數：{name} 仲有 1 個鐘開賣！", name, "hour_before")
    elif 14 <= minutes_diff <= 16:
        send_msg(f"🚨 最後衝刺：{name} 仲有 15 分鐘！快啲準備好！", name, "15min_before")
