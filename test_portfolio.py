from services.portfolio_service import get_all_stocks

stocks = get_all_stocks()

print("Elsa AI 股票清單：")
print("=" * 30)

for stock in stocks:
    print(f"{stock['symbol']} {stock['name']} / 類型：{stock['type']}")
