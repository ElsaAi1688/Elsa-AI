from portfolio.portfolio_center import PortfolioCenter
from portfolio.portfolio_health import PortfolioHealth
from teacher.portfolio_teacher import PortfolioTeacher
from scanner.market_cache import load_market_scan
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()
health = PortfolioHealth().calculate(portfolio)
lesson = PortfolioTeacher().pick_lesson(portfolio)
cache = load_market_scan()

lines = []
lines.append("🌅 Elsa AI Morning Brief 2.0")
lines.append("=" * 30)

lines.append("👩 莎莎投資中心")
lines.append(f"投入成本：{portfolio['total_cost']}")
lines.append(f"目前市值：{portfolio['total_value']}")
lines.append(f"未實現損益：{portfolio['total_pnl']}（{portfolio['total_pnl_pct']}%）")
lines.append(f"健康度：{health['score']}/100｜{health['level']} {health['stars']}")
lines.append("")

lines.append("📈 我的持股")
for h in portfolio["holdings"]:
    lines.append(f"{h['name']}｜AI {h['ai_score']}｜損益 {h['pnl_pct']}%")
    lines.append(f"經理人：{h['manager_advice']}")
lines.append("")

if cache:
    stocks = cache["stocks"]
    lines.append("🔥 今日 Top10")
    for i, s in enumerate(stocks[:5], 1):
        lines.append(f"{i}. {s['name']} AI {s['ai_score']} 現價 {s['price']}")
    lines.append("")

lines.append("📚 今日老師")
lines.append(f"主題：{lesson['title']}")
for c in lesson["content"][:3]:
    lines.append(f"・{c}")

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
