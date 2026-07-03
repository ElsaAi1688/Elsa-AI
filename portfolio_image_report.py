import json
import subprocess
from pathlib import Path

portfolio = json.loads(Path("portfolio.json").read_text(encoding="utf-8"))

stocks = portfolio.get("holdings", []) + portfolio.get("watchlist", [])

print("=" * 50)
print("🤖 Elsa AI 開始產生所有股票圖片")
print("=" * 50)

for stock in stocks:
    symbol = stock["symbol"]
    name = stock["name"]
    buy_price = stock.get("buy_price", 0)
    shares = stock.get("shares", 0)
    strategy = stock.get("strategy", stock.get("type", "watch"))

    print(f"\n📈 {symbol} {name}")

    subprocess.run([
        "python",
        "image_report.py",
        symbol,
        name,
        str(buy_price),
        str(shares),
        strategy
    ])

print("\n✅ 全部圖片完成")
