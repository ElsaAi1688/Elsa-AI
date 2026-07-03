from ai.decision_engine import build_decision

sample = {
    "symbol": "2324",
    "name": "仁寶",
    "type": "short",
    "score": 50,
    "confidence": 60,
    "risk_level": "中",
    "percent": -0.99,
    "messages": [
        "現價低於成本",
        "股價站上 MA5，短線偏強",
        "股價跌破 MA20，波段偏弱",
        "成交量放大",
        "MACD 空方訊號"
    ]
}

decision = build_decision(sample)

print("🤖 Elsa AI Decision Engine V1")
print("=" * 40)
print(f"總分：{decision['total_score']}/100")
print(f"建議：{decision['recommendation']}")
print(f"行動：{decision['action']}")
print("理由：")
for r in decision["reasons"]:
    print("-", r)
