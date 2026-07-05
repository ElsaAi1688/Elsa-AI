from conversation.manager_persona import ElsaPersona
from decision.decision_engine import ElsaDecisionEngine

class ConversationEngine:

    def __init__(self):
        self.persona = ElsaPersona()
        self.decision_engine = ElsaDecisionEngine()

    def morning_message(self, portfolio, market=None):
        decision = self.decision_engine.decide_portfolio(portfolio)

        lines = []
        lines.append(self.persona.opening())
        lines.append("=" * 30)
        lines.append(f"今天總結：{decision['main_message']}")
        lines.append("")
        lines.append("📌 我的判斷")

        for d in decision["decisions"]:
            lines.append(f"・{d['name']}：{d['action']}｜信心 {d['confidence']}%")
            lines.append(f"  {d['decision']}")

        lines.append("")
        lines.append("🧠 Elsa 一句話")
        lines.append(self.daily_sentence(decision))
        lines.append("")
        lines.append(self.persona.style_line())

        return "\n".join(lines)

    def daily_sentence(self, decision):
        msg = decision["main_message"]

        if "等待" in msg:
            return "今天最大的工作不是交易，而是等待市場給我們更好的位置。"

        if "加碼" in msg:
            return "今天有機會，但我們仍然分批，不一次把資金打滿。"

        if "風險" in msg:
            return "今天先不要想賺多少，先把風險控制好。"

        return "今天照原策略走，不需要因為短線波動打亂節奏。"
