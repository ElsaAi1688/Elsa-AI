from portfolio.portfolio_center import PortfolioCenter
from decision.decision_engine import ElsaDecisionEngine
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()
result = ElsaDecisionEngine().decide_portfolio(portfolio)

lines = []
lines.append("🧠 Elsa Decision Engine U3-A")
lines.append("=" * 30)
lines.append(f"👩‍💼 Elsa：莎莎，{result['main_message']}")
lines.append("")

for d in result["decisions"]:
    lines.append(f"📈 {d['name']}")
    lines.append(f"決策：{d['action']}")
    lines.append(f"信心：{d['confidence']}%")
    lines.append(f"原因：{d['decision']}")
    for r in d["reasons"]:
        lines.append(f"・{r}")
    lines.append("-" * 30)

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
