from ai.analyze_stock import StockAnalyzer

WATCHLIST = [
    ("2324.TW", "仁寶"),
    ("2330.TW", "台積電"),
    ("0050.TW", "元大台灣50")
]

print("=" * 70)
print("🚀 Elsa AI 股票經理人")
print("=" * 70)

analyzer = StockAnalyzer()

for symbol, name in WATCHLIST:

    try:

        stock = analyzer.analyze(symbol, name)

        print(f"\n📈 {stock.name} ({stock.symbol})")
        print(f"AI分數：{stock.ai_score}")
        print(f"技術面：{stock.technical_score}")
        print(f"基本面：{stock.fundamental_score}")
        print(f"籌碼面：{stock.chip_score}")
        print(f"新聞面：{stock.news_score}")

        if stock.reasons:
            print("理由：")
            for r in stock.reasons:
                print("  ✔", r)

    except Exception as e:

        print(symbol, e)
