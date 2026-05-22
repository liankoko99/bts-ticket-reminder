import os
import requests
from datetime import datetime, timedelta

TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']
SENT_FILE = "sent_notifications.txt"

# 售票清單 (香港時間)
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
    sent_list = []
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r") as f:
            sent_list = f.read().splitlines()
    
    key = f"{event_name}_{type}"
    if key in sent_list: return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {'chat_id': CHAT_ID, 'text': text}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        with open(SENT_FILE, "a") as f:
            f.write(key + "\n")

# 獲取香港時間
now_hkt = datetime.utcnow() + timedelta(hours=8)

# 搶票倒數邏輯
for name, time_str in events:
    event_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    diff = (event_time - now_hkt).total_seconds() / 60
    
    if diff < 0: continue 
    
    # 提取開賣的具體時間 (例如: 11:00)
    exact_time = event_time.strftime("%H:%M")
    
    # 根據是否為香港場次，自動切換祝福語
    if "香港" in name:
        wish_1hour = "祝大家戰勝hkticketing🍀"
        wish_15min = "祝戰勝移民去火星嘅黃牛😤" # 👈 已成功修改
    else:
        wish_1hour = "祝大家搶飛成功🍀"
        wish_15min = "祝戰勝所有黃牛😤"
    
    # 1. 明日提醒 (安全範圍：23.5 - 24.5 小時前)
    if 1410 <= diff <= 1470:
        send_msg(f"📅 溫馨提醒：{name} 聽日{exact_time} 正式開賣💣", name, "day_before")
        
    # 2. 售票倒數 (安全範圍：50 - 65 分鐘前)
    elif 50 <= diff <= 65:
        send_msg(f"📢 售票倒數：{name} 將於 {exact_time} 開賣💣{wish_1hour}", name, "hour_before")
        
    # 3. 最後衝刺 (安全範圍：5 - 18 分鐘前)
    elif 5 <= diff <= 18:
        send_msg(f"🚨 最後衝刺：{name} 即將於 {exact_time} 開賣💣{wish_15min}", name, "15min_before")
