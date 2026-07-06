import requests
import pandas as pd
from datetime import datetime, timedelta
from services.line_service import send_line_message

STOCK_ID = "2409"
NAME = "友達"

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

url = "https://api.finmindtrade.com/api/v4/data"
params = {
    "dataset": "TaiwanStockPrice",
    "data_id": STOCK_ID,
    "start_date": start,
    "end_date": end
}

r = requests.get(url, params=params, timeout=20)
data = r.json()

if "data" not in data or not data["data"]:
    print("FinMind 友達資料抓取失敗，暫不通知")
    print(data)
    exit()

df = pd.DataFrame(data["data"])
df = df.sort_values("date")

price = round(float(df["close"].iloc[-1]), 2)
volume = float(df["Trading_Volume"].iloc[-1])
avg_volume = float(df["Trading_Volume"].tail(20).mean())

support = round(float(df["min"].tail(20).min()), 2)
resistance = round(float(df["max"].tail(20).max()), 2)

ma5 = float(df["close"].tail(5).mean())
ma20 = float(df["close"].tail(20).mean())

ai = 50
breakout = 50
reasons = []

if price > ma5:
    ai += 10
    reasons.append("股價站上 MA5")
if price > ma20:
    ai += 10
    reasons.append("股價站上 MA20")
if ma5 > ma20:
    ai += 10
    reasons.append("MA5 高於 MA20")
if volume > avg_volume * 1.2:
    ai += 10
    reasons.append("成交量放大")
if price >= resistance:
    breakout += 30
    reasons.append("股價突破壓力")
elif price >= resistance * 0.98:
    breakout += 15
    reasons.append("接近壓力區")

alerts = []

if price >= resistance and ai >= 70 and breakout >= 75:
    alerts.append("🚀 可進場觀察：突破壓力且技術條件轉強")
elif price <= support * 1.02 and ai >= 60:
    alerts.append("🟢 可觀察：接近支撐區，等待止穩")
elif price >= resistance * 0.98 and price < resistance:
    alerts.append("🔴 不追高：接近壓力但尚未突破")

if alerts:
    msg = ["🚨 Elsa 友達進場監控｜FinMind版", "=" * 30]
    msg.append(f"現價：{price}")
    msg.append(f"AI：{ai}")
    msg.append(f"突破率：{breakout}%")
    msg.append(f"支撐：{support}")
    msg.append(f"壓力：{resistance}")
    msg.append("")
    msg.append("觸發條件：")
    for a in alerts:
        msg.append(f"・{a}")
    msg.append("")
    msg.append("技術理由：")
    for r in reasons:
        msg.append(f"・{r}")
    msg.append("")
    msg.append("👩‍💼 Elsa：莎莎，友達目前只做進場觀察，不追高，等確認。")
    final = "\n".join(msg)
    print(final)
    send_line_message(final)
else:
    print(f"友達未達進場條件｜現價 {price}｜支撐 {support}｜壓力 {resistance}｜AI {ai}｜突破率 {breakout}")

