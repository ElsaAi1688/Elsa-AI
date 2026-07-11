import json, requests, pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from services.telegram_service import send_telegram_message
from market_data.realtime_price import RealtimePrice
from engine.technical_engine import TechnicalEngine
from engine.fundamental_engine import FundamentalEngine
from engine.chip_engine import ChipEngine
from engine.explain_engine import ExplainEngine
from engine.scenario_engine import ScenarioEngine
from decision_v2.entry_decision_engine import EntryDecisionEngine

STATE = Path("/tmp/elsa_auo_state.json")
TW = ZoneInfo("Asia/Taipei")
STOCK_ID = "2409"

def load_state():
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}

def save_state(data):
    STATE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

now = datetime.now(TW)
end = now.strftime("%Y-%m-%d")
start = (now - timedelta(days=120)).strftime("%Y-%m-%d")

r = requests.get("https://api.finmindtrade.com/api/v4/data", params={
    "dataset": "TaiwanStockPrice",
    "data_id": STOCK_ID,
    "start_date": start,
    "end_date": end
}, timeout=20)

data = r.json()
if "data" not in data or not data["data"]:
    print("FinMind 資料失敗", data)
    exit()

df = pd.DataFrame(data["data"]).sort_values("date")

try:
    rt = RealtimePrice().get_tw_stock_price(STOCK_ID)
    price = round(float(rt["price"]), 2)
    print(f"即時價來源：{rt.get('source')}｜價格：{price}")
    df.loc[df.index[-1], "close"] = price
except Exception as e:
    price = round(float(df["close"].iloc[-1]), 2)
    print("即時價失敗，使用 FinMind：", e)

technical = TechnicalEngine().analyze(df)
fundamental = FundamentalEngine().analyze(STOCK_ID)
chip = ChipEngine().analyze(STOCK_ID)

# 短線有效支撐：選擇低於現價、且距離現價最近的技術位置
support_candidates = [
    float(df["min"].tail(3).min()),
    float(df["min"].tail(5).min()),
    float(df["min"].tail(10).min()),
    float(technical["ma5"]),
    float(technical["ma20"]),
    float(technical["boll_lower"]),
]

support_candidates = [
    value for value in support_candidates
    if value > 0 and price * 0.85 <= value <= price
]

support = (
    round(max(support_candidates), 2)
    if support_candidates
    else round(price * 0.97, 2)
)

# 短線有效壓力：選擇高於現價、且距離現價最近的位置
resistance_candidates = [
    float(df["max"].tail(3).max()),
    float(df["max"].tail(5).max()),
    float(df["max"].tail(10).max()),
    float(technical["boll_upper"]),
]

resistance_candidates = [
    value for value in resistance_candidates
    if price <= value <= price * 1.20
]

resistance = (
    round(min(resistance_candidates), 2)
    if resistance_candidates
    else round(price * 1.05, 2)
)

print(
    f"短線支撐={support}｜短線壓力={resistance}",
    flush=True,
)

ai = round(technical["score"] * 0.55 + fundamental["score"] * 0.25 + chip["score"] * 0.20)
breakout = 50
if price >= resistance:
    breakout += 30
elif price >= resistance * 0.98:
    breakout += 15

decision = EntryDecisionEngine().evaluate({
    "price": price,
    "support": support,
    "resistance": resistance,
    "technical_score": technical["score"],
    "fundamental_score": fundamental["score"],
    "chip_score": chip["score"]
})

explain_summary = ExplainEngine().summarize(
    technical,
    fundamental,
    chip
)

macd_scenario = ScenarioEngine().simulate_macd_bullish(
    technical=technical,
    fundamental=fundamental,
    chip=chip,
    price=price,
    support=support,
    resistance=resistance,
    decision_engine=EntryDecisionEngine(),
)

signal = decision["action"]
state = load_state()
last_signal = state.get("signal")
last_sent = state.get("last_sent")

should_send = False
if signal != last_signal or not last_sent:
    should_send = True
else:
    last_time = datetime.fromisoformat(last_sent)
    should_send = (now - last_time).total_seconds() >= 1800

if should_send:
    lines = []
    lines.append("🧠 Elsa Decision Engine v3｜友達")
    lines.append("=" * 30)
    lines.append(f"時間：{now.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"最近成交／收盤價：{price}")
    lines.append(f"支撐：{support}")
    lines.append(f"壓力：{resistance}")
    lines.append("")
    lines.append("📊 技術總分")
    lines.append(f"{technical['score']}/100")
    lines.append("")
    lines.append("📈 技術指標拆解")
    for item in technical["explain"]:
        sign = "+" if item["points"] > 0 else ""
        lines.append(f"・{item['name']}｜{item['status']}｜{sign}{item['points']}分")
        lines.append(f"  {item['reason']}")
    lines.append("")
    lines.append("📊 基本面拆解")
    lines.append(f"基本面分數：{fundamental['score']}/100")
    for item in fundamental["explain"]:
        sign = "+" if item["points"] > 0 else ""
        lines.append(f"・{item['name']}｜{item['status']}｜{sign}{item['points']}分")
        lines.append(f"  {item['reason']}")
    lines.append("")
    lines.append("💰 籌碼拆解")
    lines.append(f"籌碼分數：{chip['score']}/100")
    lines.append(f"統計期間：{chip.get('period', '未提供')}")
    for item in chip["explain"]:
        sign = "+" if item["points"] > 0 else ""
        lines.append(f"・{item['name']}｜{item['status']}｜{sign}{item['points']}分")
        lines.append(f"  {item['reason']}")
    lines.append("")
    lines.append("👩‍💼 Elsa 最終決策")
    lines.append(f"建議：{decision['action']}")
    lines.append(f"綜合評分：{decision['score']}/100｜{decision['level']}")
    lines.append(f"建議進場區間：{decision['entry_low']}～{decision['entry_high']}")
    lines.append(f"停損：{decision['stop_loss']}")
    lines.append(f"目標一：{decision['target1']}")
    lines.append(f"目標二：{decision['target2']}")
    lines.append("")
    lines.append("🧠 AI 分數重點")
    for item in explain_summary:
        lines.append(item)

    lines.append("")
    lines.append("🔮 情境模擬")
    lines.append(f"如果 {macd_scenario['scenario']}：")
    lines.append(
        f"技術分數："
        f"{macd_scenario['current_technical_score']} → "
        f"{macd_scenario['projected_technical_score']}"
    )
    lines.append(
        f"綜合評分可能提升至："
        f"{macd_scenario['projected_total_score']}/100｜"
        f"{macd_scenario['projected_level']}"
    )
    lines.append(
        f"預估決策：{macd_scenario['projected_action']}"
    )
    lines.append("此為規則模擬，不是獲利機率保證。")

    lines.append("")
    lines.append("莎莎，我會繼續巡邏，有更高勝率訊號再通知妳。")

    msg = "\n".join(lines)
    print(msg)
    send_telegram_message(msg)

    save_state({"signal": signal, "last_sent": now.isoformat(), "price": price})
else:
    print(f"友達巡邏完成，不重複通知｜{signal}｜現價 {price}")
