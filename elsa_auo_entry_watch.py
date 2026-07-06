import yfinance as yf
from services.line_service import send_line_message

symbol = "2409.TW"
name = "友達"

df = yf.download(symbol, period="3mo", progress=False, auto_adjust=True)

if df.empty:
    print("友達資料抓取失敗，暫不通知")
    exit()

if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
    df.columns = df.columns.get_level_values(0)

price = round(float(df["Close"].iloc[-1]), 2)
volume = float(df["Volume"].iloc[-1])
avg_volume = float(df["Volume"].tail(20).mean())

support = round(float(df["Low"].tail(20).min()), 2)
resistance = round(float(df["High"].tail(20).max()), 2)

ma5 = float(df["Close"].tail(5).mean())
ma20 = float(df["Close"].tail(20).mean())

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

alerts = []

if price >= resistance and ai >= 70 and breakout >= 75:
    alerts.append("🚀 股價突破壓力，且技術條件轉強，可列入進場觀察")
elif price <= support * 1.02 and ai >= 60:
    alerts.append("🟢 股價接近支撐，可觀察是否止穩")
elif price >= resistance * 0.98 and price < resistance:
    alerts.append("🔴 接近壓力但尚未突破，不追高")

if alerts:
    msg = ["🚨 Elsa 友達進場監控", "=" * 30]
    msg.append(f"現價：{price}")
    msg.append(f"AI：{ai}")
    msg.append(f"突破率：{breakout}%")
    msg.append(f"支撐：{support}")
    msg.append(f"壓力：{resistance}")
    msg.append("")
    msg.append("判斷原因：")
    for a in alerts:
        msg.append(f"・{a}")
    msg.append("")
    msg.append("👩‍💼 Elsa：莎莎，友達要等確認，不追高。")
    send_line_message("\n".join(msg))
    print("\n".join(msg))
else:
    print(f"友達目前未達進場條件｜現價 {price}｜支撐 {support}｜壓力 {resistance}｜AI {ai}｜突破率 {breakout}")
