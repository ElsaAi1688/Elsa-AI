from pathlib import Path

Path("manager").mkdir(exist_ok=True)

Path("manager/dca_manager.py").write_text('''
from datetime import datetime

class DCAManager:

    def analyze(self, portfolio):

        today = datetime.now()

        result = []

        for h in portfolio["holdings"]:

            if h["strategy"] != "long_term_dca":
                continue

            ai = h["ai_score"]

            if ai >= 80:
                advice = "建議增加20%"
                level = "★★★★★"
                factor = 1.2

            elif ai >= 70:
                advice = "維持原扣款"
                level = "★★★★☆"
                factor = 1.0

            elif ai >= 60:
                advice = "維持小額定投"
                level = "★★★☆☆"
                factor = 1.0

            else:
                advice = "保留現金，本月不建議增加"
                level = "★★☆☆☆"
                factor = 1.0

            amount = h.get("monthly_dca_amount",0)
            recommend = round(amount*factor)

            result.append({

                "name":h["name"],

                "day":h["monthly_dca_day"],

                "ai":ai,

                "level":level,

                "amount":amount,

                "recommend":recommend,

                "advice":advice

            })

        return result
''',encoding="utf-8")

Path("elsa_rc1d.py").write_text('''
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

msg="\\n".join(lines)

print(msg)

send_line_message(msg)
''',encoding="utf-8")

print("✅ RC1-D 安裝完成")
