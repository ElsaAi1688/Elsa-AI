from portfolio.portfolio_center import PortfolioCenter
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()
h = next(x for x in portfolio["holdings"] if x["symbol"] == "2409.TW")

price = h["price"]
ai = h["ai_score"]
breakout = h["breakout_probability"]
support = h["support"]
resistance = h["resistance"]

status = "等待"
level = "🟡 等確認"
alerts = []

# 🚀 真正可進場：突破壓力 + AI轉強 + 突破率高
if resistance and price >= resistance and ai >= 75 and breakout >= 75:
    status = "可進場觀察"
    level = "🚀 可進場"
    alerts.append(f"股價已站上壓力 {resistance}")
    alerts.append(f"AI {ai}，突破率 {breakout}%")
    alerts.append("符合短線突破觀察條件，可等回測不破或帶量確認")

# 🟢 接近支撐：可以觀察，但不是直接買
elif support and price <= support * 1.02 and ai >= 65 and breakout >= 55:
    status = "支撐觀察"
    level = "🟢 可觀察"
    alerts.append(f"股價接近支撐 {support}")
    alerts.append("可以觀察是否止穩，但還不是直接進場")

# 🔴 接近壓力但沒突破：提醒不要追高
elif resistance and price >= resistance * 0.98 and price < resistance:
    status = "接近壓力"
    level = "🔴 不追高"
    alerts.append(f"接近壓力 {resistance}，但尚未突破")
    alerts.append("不要急著追，等站上壓力再說")

else:
    print("友達目前尚未達到進場提醒條件")
    exit()

msg = ["🚨 Elsa 友達進場監控", "=" * 30]
msg.append(f"狀態：{level}｜{status}")
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
msg.append("👩‍💼 Elsa：莎莎，友達目前要等確認，不要只因為靠近壓力就追高。")

final = "\n".join(msg)
print(final)
send_line_message(final)
