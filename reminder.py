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

# --- 修改後：登記提醒 (改為 17:00 & 22:00) ---
if now_hkt.strftime("%Y-%m-%d") == "2026-05-22":
    now_hkt_time = now_hkt.strftime("%H:%M")
    if now_hkt_time == "17:00": 
        send_msg("⚠️ 溫馨提示：記得今日 17:00 留意 Weverse，處理 ARMY Membership 登記！", "ARMY_Reg", "1700")
    if now_hkt_time == "22:00": 
        send_msg("⚠️ 溫馨提示：記得今日 22:00 留意 Weverse，處理 ARMY Membership 登記！", "ARMY_Reg", "2200")

# 搶票倒數
for name, time_str in events:
    event_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    diff = (event_time - now_hkt).total_seconds() / 60
    
    if diff < 0: continue 
    
    if 1439 <= diff <= 1441:
        send_msg(f"📅 明日提醒：{name} 將於明日開賣，請做好準備！", name, "day_before")
    elif 59 <= diff <= 61:
        send_msg(f"📢 售票倒數：{name} 仲有 1 個鐘開賣！", name, "hour_before")
    elif 14 <= diff <= 16:
        send_msg(f"🚨 最後衝刺：{name} 仲有 15 分鐘！快啲準備好！", name, "15min_before")
