from portfolio.portfolio_center import PortfolioCenter
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()
h = next(x for x in portfolio["holdings"] if x["symbol"] == "2409.TW")

price = h["price"]
ai = h["ai_score"]
breakout = h["breakout_probability"]
support = h["support"]
resistance = h["resistance"]

alerts = []

if ai >= 75 and breakout >= 75:
    alerts.append("🚀 AI 與突破率同步轉強，可列入進場觀察")

if support and price <= support * 1.02:
    alerts.append(f"🎯 股價接近支撐 {support}，可觀察是否止穩")

if resistance and price >= resistance * 0.99:
    alerts.append(f"⚡ 接近壓力 {resistance}，不要追高，等突破確認")

if alerts:
    msg = ["🚨 Elsa 友達進場提醒", "=" * 30]
    msg.append(f"現價：{price}")
    msg.append(f"AI：{ai}")
    msg.append(f"突破率：{breakout}%")
    msg.append(f"支撐：{support}")
    msg.append(f"壓力：{resistance}")
    msg.append("")
    msg.append("觸發條件：")
    msg.extend(alerts)
    msg.append("")
    msg.append("👩‍💼 Elsa：莎莎，友達開始接近短線觀察區，但仍要等確認，不追高。")
    final = "\n".join(msg)
    print(final)
    send_line_message(final)
else:
    print("友達目前尚未達到進場提醒條件")
