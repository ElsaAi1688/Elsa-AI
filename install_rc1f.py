from pathlib import Path

Path("teacher").mkdir(exist_ok=True)

Path("teacher/portfolio_teacher.py").write_text('''
class PortfolioTeacher:

    def pick_lesson(self, portfolio):
        for h in portfolio["holdings"]:
            if h["strategy"] == "short_term":
                return {
                    "title": "什麼叫突破？",
                    "stock": h["name"],
                    "content": [
                        f"妳目前持有 {h['name']}，這檔是短線操作。",
                        f"目前壓力位是 {h['resistance']}。",
                        "短線股不是看到漲就追，而是要等突破壓力。",
                        "突破時如果成交量也放大，勝率會比較好。",
                        "如果沒有突破就追高，容易買在壓力附近。"
                    ]
                }

        return {
            "title": "定期定額為什麼不用每天看？",
            "stock": "長期投資",
            "content": [
                "2330 和 0050 屬於長期定投。",
                "定投重點不是每天猜高低點，而是長期累積。",
                "Elsa 會在每月13號前提醒是否適合多投入。"
            ]
        }
''', encoding="utf-8")

Path("elsa_rc1f.py").write_text('''
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

msg = "\\n".join(lines)
print(msg)
send_line_message(msg)
''', encoding="utf-8")

print("✅ RC1-F 持股老師安裝完成")
