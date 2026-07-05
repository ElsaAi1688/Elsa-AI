class TradeManager:

    def evaluate(self, holding):

        price = holding["price"]
        cost = holding["cost"]
        ai = holding["ai_score"]
        resistance = holding["resistance"]
        stop = holding["stop_loss"]

        state = "持有中"
        priority = 1
        advice = "續抱"

        if price <= stop:
            state = "風險"
            advice = "立即檢查停損"
            priority = 5

        elif resistance and price >= resistance * 0.99:
            state = "接近壓力"
            advice = "準備分批減碼"
            priority = 5

        elif ai >= 80:
            state = "偏強"
            advice = "續抱等待"
            priority = 4

        else:
            state = "觀察"
            advice = "等待突破"
            priority = 3

        return {
            "state": state,
            "priority": priority,
            "advice": advice,
            "profit_pct": round((price-cost)/cost*100,2)
        }
