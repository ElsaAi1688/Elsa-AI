import json
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from services.line_service import send_line_message
from market_data.realtime_price import RealtimePrice
from decision_v2.entry_decision_engine import EntryDecisionEngine

STATE = Path("/tmp/elsa_auo_state.json")
TW = ZoneInfo("Asia/Taipei")

STOCK_ID = "2409"
NAME = "友達"

def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {}

def save_state(data):
    STATE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

now = datetime.now(TW)
end = now.strftime("%Y-%m-%d")
start = (now - timedelta(days=90)).strftime("%Y-%m-%d")

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
    print("FinMind 友達資料抓取失敗")
    print(data)
    exit()

df = pd.DataFrame(data["data"]).sort_values("date")

price = round(float(df["close"].iloc[-1]), 2)

try:
    rt = RealtimePrice().get_tw_stock_price(STOCK_ID)
    price = round(float(rt["price"]), 2)
    print(f"即時價來源：{rt.get('source')}｜價格：{price}")
except Exception as e:
    print("即時價失敗，使用 FinMind 價格：", e)

volume = float(df["Trading_Volume"].iloc[-1])
avg_volume = float(df["Trading_Volume"].tail(20).mean())

support = round(float(df["min"].tail(20).min()), 2)
resistance = round(float(df["max"].tail(20).max()), 2)

ma5 = float(df["close"].tail(5).mean())
ma20 = float(df["close"].tail(20).mean())

ai = 50
breakout = 50

if price > ma5:
    ai += 10
if price > ma20:
    ai += 10
if ma5 > ma20:
    ai += 10
if volume > avg_volume * 1.2:
    ai += 10
if price >= resistance:
    breakout += 30
elif price >= resistance * 0.98:
    breakout += 15

entry_decision = EntryDecisionEngine().evaluate({
    "price": price,
    "support": support,
    "resistance": resistance,
    "ai": ai,
    "breakout": breakout,
    "ma5": ma5,
    "ma20": ma20,
    "volume": volume,
    "avg_volume": avg_volume
})

signal = entry_decision["action"]

state = load_state()
last_signal = state.get("signal")
last_sent = state.get("last_sent")

should_send = False

if signal != last_signal:
    should_send = True
elif not last_sent:
    should_send = True
else:
    last_time = datetime.fromisoformat(last_sent)
    if (now - last_time).total_seconds() >= 1800:
        should_send = True

if should_send:
    lines = []
    lines.append("🧠 Elsa Decision Engine v2｜友達")
    lines.append("=" * 30)
    lines.append(f"時間：{now.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"現價：{price}")
    lines.append(f"AI：{ai}")
    lines.append(f"突破率：{breakout}%")
    lines.append(f"支撐：{support}")
    lines.append(f"壓力：{resistance}")
    lines.append("")
    lines.append("👩‍💼 Elsa 決策")
    lines.append(f"建議：{entry_decision['action']}")
    lines.append(f"勝率分數：{entry_decision['score']}/100｜{entry_decision['level']}")
    lines.append(f"建議進場區間：{entry_decision['entry_low']}～{entry_decision['entry_high']}")
    lines.append(f"停損：{entry_decision['stop_loss']}")
    lines.append(f"目標一：{entry_decision['target1']}")
    lines.append(f"目標二：{entry_decision['target2']}")
    lines.append("")
    lines.append("判斷理由：")
    for x in entry_decision["reasons"]:
        lines.append(f"・{x}")
    lines.append("")
    lines.append("莎莎，我會繼續每 5 分鐘巡邏，有高勝率訊號再通知妳。")

    msg = "\n".join(lines)
    print(msg)
    send_line_message(msg)

    save_state({
        "signal": signal,
        "last_sent": now.isoformat(),
        "price": price
    })
else:
    print(f"友達巡邏完成，不重複通知｜{signal}｜現價 {price}")

