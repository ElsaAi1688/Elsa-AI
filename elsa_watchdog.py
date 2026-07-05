from portfolio.portfolio_center import PortfolioCenter
from trade.trade_manager import TradeManager
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()
tm = TradeManager()

h = next(x for x in portfolio["holdings"] if x["symbol"] == "2324.TW")
t = tm.evaluate(h)

price = h["price"]
cost = h["cost"]
resistance = h["resistance"]
stop = t["exit_plan"]["stop_loss"]
target1 = t["exit_plan"]["target1"]
target2 = t["exit_plan"]["target2"]
target3 = t["exit_plan"]["target3"]

alerts = []

if price <= stop:
    alerts.append(f"⚠️ 跌破停損 {stop}，優先保護本金")

if price >= target3:
    alerts.append(f"🏁 已達第三目標 {target3}，可考慮完成出場")
elif price >= target2:
    alerts.append(f"🎯 已達第二目標 {target2}，可考慮再減碼 30%")
elif price >= target1:
    alerts.append(f"🎯 已達第一目標 {target1}，可考慮先減碼 20%")

if resistance and price >= resistance * 0.99:
    alerts.append(f"⚡ 接近壓力 {resistance}，準備觀察是否轉弱或突破")

if alerts:
    lines = []
    lines.append("🔴 Elsa Watchdog 緊急警報")
    lines.append("仁寶可能接近下車條件")
    lines.append("=" * 30)
    lines.append(f"現價：{price}")
    lines.append(f"成本：{cost}")
    lines.append(f"目前損益：{t['profit_pct']}%")
    lines.append("")
    lines.append("觸發條件：")
    for a in alerts:
        lines.append(a)
    lines.append("")
    lines.append("👩‍💼 Elsa：莎莎，先照計畫，不要慌，分批處理。")
else:
    lines = []
    lines.append("🟢 Elsa Watchdog 巡邏回報")
    lines.append("莎莎，目前仁寶尚未觸發下車條件。")
    lines.append("=" * 30)
    lines.append(f"現價：{price}")
    lines.append(f"成本：{cost}")
    lines.append(f"目前損益：{t['profit_pct']}%")
    lines.append(f"狀態：{t['state']}")
    lines.append("")
    lines.append(f"第一目標：{target1}")
    lines.append(f"第二目標：{target2}")
    lines.append(f"第三目標：{target3}")
    lines.append(f"停損：{stop}")
    lines.append("")
    lines.append("👩‍💼 Elsa：我會繼續幫妳盯盤，有狀況再通知。")

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
