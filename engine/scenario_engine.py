class ScenarioEngine:

    def simulate_macd_bullish(
        self,
        technical,
        fundamental,
        chip,
        price,
        support,
        resistance,
        decision_engine,
    ):
        current_technical = int(technical["score"])

        macd_negative_points = 0
        already_bullish = False

        for item in technical.get("explain", []):
            if item.get("name") != "MACD":
                continue

            status = str(item.get("status", ""))
            points = int(item.get("points", 0))

            if "翻紅" in status:
                already_bullish = True

            if points < 0:
                macd_negative_points += abs(points)

        if already_bullish:
            projected_technical = current_technical
            note = "MACD 已經翻紅，不需要再模擬"
        else:
            # 移除目前 MACD 負分，再加入翻紅 +15 分
            projected_technical = min(
                100,
                current_technical + macd_negative_points + 15
            )
            note = (
                f"技術分數預估由 {current_technical} "
                f"提升至 {projected_technical}"
            )

        projected_decision = decision_engine.evaluate({
            "price": price,
            "support": support,
            "resistance": resistance,
            "technical_score": projected_technical,
            "fundamental_score": fundamental["score"],
            "chip_score": chip["score"],
        })

        return {
            "scenario": "MACD 翻紅",
            "current_technical_score": current_technical,
            "projected_technical_score": projected_technical,
            "projected_total_score": projected_decision["score"],
            "projected_action": projected_decision["action"],
            "projected_level": projected_decision["level"],
            "note": note,
        }
