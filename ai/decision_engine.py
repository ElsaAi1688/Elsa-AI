def build_decision(stock_result):
    technical_score = stock_result.get("score", 0)
    confidence = stock_result.get("confidence", 0)
    risk_level = stock_result.get("risk_level", "未評估")
    stock_type = stock_result.get("type", "watch")
    percent = stock_result.get("percent", 0)

    fundamental_score = 50
    chip_score = 50
    news_score = 50

    total_score = round(
        technical_score * 0.55 +
        fundamental_score * 0.20 +
        chip_score * 0.15 +
        news_score * 0.10
    )

    reasons = []

    for msg in stock_result.get("messages", [])[:5]:
        reasons.append(msg)

    if stock_type == "short":
        if percent >= 5:
            recommendation = "分批獲利"
            action = "可考慮賣出 30%～50%，保留部分觀察。"
        elif percent <= -3:
            recommendation = "嚴格控管風險"
            action = "接近停損區，不建議加碼。"
        elif total_score >= 70:
            recommendation = "續抱觀察"
            action = "短線仍可觀察，等待突破或轉強訊號。"
        else:
            recommendation = "暫不加碼"
            action = "訊號尚未明確，先觀察支撐。"

    elif stock_type == "dca":
        if total_score >= 70:
            recommendation = "維持定期定額"
            action = "照原計畫扣款，可等待回檔再額外加碼。"
        else:
            recommendation = "維持紀律"
            action = "不追高，暫不額外加碼。"

    else:
        recommendation = "觀察"
        action = "等待更明確訊號。"

    return {
        "technical_score": technical_score,
        "fundamental_score": fundamental_score,
        "chip_score": chip_score,
        "news_score": news_score,
        "total_score": total_score,
        "confidence": confidence,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "action": action,
        "reasons": reasons
    }
