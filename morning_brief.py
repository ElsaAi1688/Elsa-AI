from main import WATCHLIST
from ai.analyze_stock import StockAnalyzer

print("="*70)
print("🌅 Elsa AI Morning Brief")
print("="*70)

analyzer = StockAnalyzer()

for symbol,name in WATCHLIST:

    stock = analyzer.analyze(symbol,name)

    print(f"""
📈 {stock.name}
AI：{stock.ai_score}
技術：{stock.technical_score}
基本：{stock.fundamental_score}
籌碼：{stock.chip_score}
新聞：{stock.news_score}

建議：
{stock.recommendation}

理由：
""")

    for r in stock.reasons:
        print("✔",r)

    print("-"*70)
