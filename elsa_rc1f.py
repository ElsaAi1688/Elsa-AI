
from portfolio.portfolio_center import PortfolioCenter
from teacher.portfolio_teacher import PortfolioTeacher
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()
lesson = PortfolioTeacher().pick_lesson(portfolio)

lines = []
lines.append("📚 Elsa AI RC1-F 今日持股老師")
lines.append("=" * 30)
lines.append(f"今日主題：{lesson['title']}")
lines.append(f"關聯持股：{lesson['stock']}")
lines.append("")

for c in lesson["content"]:
    lines.append(f"・{c}")

lines.append("")
lines.append("📌 Elsa 老師提醒")
lines.append("先學會看懂原因，再決定要不要操作。")

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
