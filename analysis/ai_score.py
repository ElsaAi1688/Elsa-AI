def analyze(close, buy_price, ma5, ma20, rsi, macd, signal, volume):
    score = 50
    messages = []
    risk_points = 0

    if close > buy_price:
        messages.append("✅ 現價高於成本")
        score += 15
    else:
        messages.append("⚠️ 現價低於成本")
        score -= 5
        risk_points += 1

    if close > ma5:
        messages.append("✅ 股價站上 MA5，短線偏強")
        score += 15
    else:
        messages.append("⚠️ 股價跌破 MA5，短線偏弱")
        score -= 10
        risk_points += 1

    if close > ma20:
        messages.append("✅ 股價站上 MA20，波段偏多")
        score += 15
    else:
        messages.append("⚠️ 股價跌破 MA20，波段偏弱")
        score -= 10
        risk_points += 1

    if volume > 30000000:
        messages.append("🔥 成交量放大")
        score += 10
    else:
        messages.append("➖ 成交量普通")

    if rsi < 30:
        messages.append("✅ RSI 偏低，可能有反彈機會")
        score += 10
    elif rsi > 70:
        messages.append("⚠️ RSI 偏高，短線可能過熱")
        score -= 10
        risk_points += 1
    else:
        messages.append("➖ RSI 正常區間")

    if macd > signal:
        messages.append("✅ MACD 多方訊號")
        score += 15
    else:
        messages.append("⚠️ MACD 空方訊號")
        score -= 10
        risk_points += 1

    score = max(0, min(score, 100))
    confidence = min(95, max(40, score + 10))

    if risk_points >= 4:
        risk_level = "高"
    elif risk_points >= 2:
        risk_level = "中"
    else:
        risk_level = "低"

    return score, messages, confidence, risk_level
