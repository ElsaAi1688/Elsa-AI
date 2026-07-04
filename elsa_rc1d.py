
from portfolio.portfolio_center import PortfolioCenter
from manager.dca_manager import DCAManager
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()

items = DCAManager().analyze(portfolio)

lines=[]

lines.append("💰 Elsa ETF 定期定額經理人")
lines.append("="*35)

for x in items:

    lines.append(f"📈 {x['name']}")

    lines.append(f"AI：{x['ai']}  {x['level']}")

    lines.append(f"扣款日：每月{x['day']}號")

    lines.append(f"原扣款：{x['amount']} 元")

    lines.append(f"本月建議：{x['recommend']} 元")

    lines.append(f"經理人：{x['advice']}")

    lines.append("-"*35)

lines.append("📌 Elsa 不會固定叫妳加碼，而是每月依 AI、市場健康度重新判斷。")

msg="\n".join(lines)

print(msg)

send_line_message(msg)
