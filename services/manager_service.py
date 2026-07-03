def get_manager_suggestion(stock_result):
    strategy = stock_result.get("type", "")
    score = stock_result["score"]
    confidence = stock_result.get("confidence", 0)
    risk = stock_result.get("risk_level", "未評估")
    percent = stock_result.get("percent", 0)

    upside = min(90, max(10, score))
    downside = 100 - upside

    if strategy == "short":
        if percent >= 5:
            action = "🎯 可分批獲利出場 30%～50%"
            hold_days = "0～2 天"
        elif percent <= -3:
            action = "🛑 接近停損區，嚴格控管風險"
            hold_days = "立即觀察"
        elif score >= 75:
            action = "✅ 續抱，等待短線轉強"
            hold_days = "3～7 天"
        elif score >= 55:
            action = "🟡 觀察，不急著加碼"
            hold_days = "2～5 天"
        else:
            action = "🔴 偏弱，不建議加碼"
            hold_days = "1～3 天"

    elif strategy == "dca":
        if score >= 80 and risk == "低":
            action = "🌱 維持定期定額，可小額加碼"
        elif score >= 55:
            action = "🌱 照原計畫扣款，不追高"
        else:
            action = "⚠️ 維持紀律，但暫不額外加碼"
        hold_days = "長期持有"

    else:
        action = "👀 觀察中，等待更明確訊號"
        hold_days = "觀察"

    return {
        "action": action,
        "confidence": confidence,
        "risk_level": risk,
        "upside_probability": upside,
        "downside_probability": downside,
        "hold_days": hold_days
    }
