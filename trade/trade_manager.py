class TradeManager:

    def evaluate(self, holding):
        price = holding["price"]
        cost = holding["cost"]
        ai = holding["ai_score"]
        resistance = holding["resistance"]
        stop = holding["stop_loss"]
        target = holding["target_price"]
        strategy = holding.get("strategy", "")

        profit_pct = round((price - cost) / cost * 100, 2) if cost else 0

        state = "觀察"
        advice = "等待"
        priority = 1
        next_action = "先觀察，不急著動作"

        # 短線股優先級提高，仁寶會被排到前面
        if strategy == "short_term":
            priority += 3
            state = "短線持有中"
            advice = "等待突破"
            next_action = f"突破壓力 {resistance} 再考慮分批出場"

            if price <= stop:
                state = "停損警戒"
                advice = "優先控管風險"
                priority = 10
                next_action = f"跌破停損 {stop}，要重新評估是否停損"

            elif resistance and price >= resistance * 0.99:
                state = "接近出場區"
                advice = "準備分批減碼"
                priority = 9
                next_action = f"若站穩 {resistance} 以上，可開始分批減碼"

            elif profit_pct > 3:
                state = "已有獲利"
                advice = "續抱但提高警覺"
                priority = 8
                next_action = "已有獲利，不要貪心，開始準備停利計畫"

        else:
            if ai >= 75:
                state = "長期穩健"
                advice = "持續定投"
                priority = 3
                next_action = "照原本定期定額，不因短線波動改變策略"
            else:
                state = "長期觀察"
                advice = "維持原策略"
                priority = 2
                next_action = "維持定投，不急著加碼"

        exit_plan = {
            "target1": round(cost * 1.03, 2),
            "target1_action": "可先減碼 20%",
            "target2": round(cost * 1.06, 2),
            "target2_action": "再減碼 30%",
            "target3": round(cost * 1.10, 2),
            "target3_action": "視狀況全部出場或保留小部位",
            "stop_loss": stop,
            "stop_action": "跌破停損，優先保護本金"
        }

        return {
            "state": state,
            "priority": priority,
            "advice": advice,
            "profit_pct": profit_pct,
            "next_action": next_action,
            "exit_plan": exit_plan
        }
