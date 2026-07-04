
from datetime import datetime

class MonthlyManager:
    def check(self, stocks):
        today = datetime.now().day

        if today not in [10, 12, 13]:
            return []

        lines = []
        lines.append("📅 每月13日扣款經理人提醒")

        if today == 10:
            lines.append("距離扣款日還有3天")
        elif today == 12:
            lines.append("明天就是扣款日")
        elif today == 13:
            lines.append("今天是扣款日")

        for stock in stocks:
            if stock.ai_score >= 75:
                action = "本月可考慮多投入"
            elif stock.ai_score >= 60:
                action = "維持原扣款"
            else:
                action = "暫不加碼，保留現金"

            lines.append(f"{stock.name}：{action}（AI {stock.ai_score}）")

        return lines
