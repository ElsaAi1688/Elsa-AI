class ElsaDecisionEngine:

    def decide_stock(self, stock):
        ai = stock["ai_score"]
        breakout = stock["breakout_probability"]
        price = stock["price"]
        support = stock["support"]
        resistance = stock["resistance"]
        stop_loss = stock["stop_loss"]
        strategy = stock.get("strategy", "")

        if strategy == "long_term_dca":
            if ai >= 75:
                action = "加碼"
                decision = "本月可考慮增加定期定額"
                confidence = 82
            elif ai >= 60:
                action = "持續"
                decision = "維持原本定期定額"
                confidence = 78
            else:
                action = "等待"
                decision = "暫不增加扣款，保留現金"
                confidence = 75

        elif strategy == "short_term":
            if price <= stop_loss:
                action = "減碼"
                decision = "跌破停損，優先控管風險"
                confidence = 90
            elif ai >= 75 and breakout >= 75:
                action = "續抱"
                decision = "短線條件偏強，續抱觀察突破"
                confidence = 84
            elif resistance and price < resistance:
                action = "等待"
                decision = "尚未突破壓力，不追高"
                confidence = 88
            else:
                action = "等待"
                decision = "訊號不夠明確，先觀察"
                confidence = 80

        else:
            action = "觀察"
            decision = "資料不足，先觀察"
            confidence = 60

        reasons = []
        if ai:
            reasons.append(f"AI 分數 {ai}")
        if breakout:
            reasons.append(f"突破率 {breakout}%")
        if support:
            reasons.append(f"支撐 {support}")
        if resistance:
            reasons.append(f"壓力 {resistance}")

        return {
            "symbol": stock["symbol"],
            "name": stock["name"],
            "action": action,
            "decision": decision,
            "confidence": confidence,
            "reasons": reasons
        }

    def decide_portfolio(self, portfolio):
        decisions = [self.decide_stock(h) for h in portfolio["holdings"]]

        wait_count = sum(1 for d in decisions if d["action"] == "等待")
        add_count = sum(1 for d in decisions if d["action"] == "加碼")
        reduce_count = sum(1 for d in decisions if d["action"] == "減碼")

        if reduce_count > 0:
            main = "今天優先控管風險。"
        elif add_count > 0:
            main = "今天有長期加碼機會，但仍要分批。"
        elif wait_count >= 1:
            main = "今天主要策略是等待，不追高。"
        else:
            main = "今天維持原策略。"

        return {
            "main_message": main,
            "decisions": decisions
        }
