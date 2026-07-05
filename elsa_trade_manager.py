from portfolio.portfolio_center import PortfolioCenter
from trade.trade_manager import TradeManager
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()
tm = TradeManager()

lines=[]

lines.append("👩‍💼 Elsa Trade Manager")
lines.append("="*30)

highest=None

for h in portfolio["holdings"]:

    t=tm.evaluate(h)

    if highest is None or t["priority"]>highest["priority"]:
        highest={
            "name":h["name"],
            **t
        }

    lines.append(f"📈 {h['name']}")
    lines.append(f"目前：{t['state']}")
    lines.append(f"建議：{t['advice']}")
    lines.append(f"目前損益：{t['profit_pct']}%")
    lines.append("-"*30)

lines.append("")
lines.append("⭐ 今日第一優先")
lines.append(f"{highest['name']}")
lines.append(f"{highest['advice']}")

msg="\n".join(lines)

print(msg)
send_line_message(msg)
