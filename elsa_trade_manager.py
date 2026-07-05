from portfolio.portfolio_center import PortfolioCenter
from trade.trade_manager import TradeManager
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()
tm = TradeManager()

items = []

for h in portfolio["holdings"]:
    t = tm.evaluate(h)
    items.append({
        "holding": h,
        "trade": t
    })

items.sort(key=lambda x: x["trade"]["priority"], reverse=True)
focus = items[0]

lines = []
lines.append("👩‍💼 Elsa Trade Manager 2.0")
lines.append("=" * 30)

lines.append("⭐ 今日第一優先")
lines.append(f"{focus['holding']['name']}")
lines.append(f"狀態：{focus['trade']['state']}")
lines.append(f"建議：{focus['trade']['advice']}")
lines.append(f"下一步：{focus['trade']['next_action']}")
lines.append("")

lines.append("📌 仁寶出場計畫")
for item in items:
    h = item["holding"]
    t = item["trade"]

    if h["symbol"] == "2324.TW":
        p = t["exit_plan"]
        lines.append(f"成本：{h['cost']}｜現價：{h['price']}｜損益：{t['profit_pct']}%")
        lines.append(f"第一目標：{p['target1']} → {p['target1_action']}")
        lines.append(f"第二目標：{p['target2']} → {p['target2_action']}")
        lines.append(f"第三目標：{p['target3']} → {p['target3_action']}")
        lines.append(f"停損：{p['stop_loss']} → {p['stop_action']}")
        lines.append("")

lines.append("📈 全部持股狀態")
for item in items:
    h = item["holding"]
    t = item["trade"]
    lines.append(f"{h['name']}｜{t['state']}｜{t['advice']}｜損益 {t['profit_pct']}%")

lines.append("")
lines.append("👩‍💼 Elsa 結論")
lines.append("莎莎，明天開盤前，先不要被市場雜訊帶走。")
lines.append("仁寶是短線交易，今天第一任務是看它有沒有進入分批出場條件。")

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
