
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai.analyze_stock import StockAnalyzer

class MarketBrain:

    def load_symbols(self, limit=50):
        items = []
        from pathlib import Path

csv_path=Path("data/watch_symbols.csv")

if not csv_path.exists():
    return [
        ("2330.TW","台積電"),
        ("0050.TW","元大台灣50"),
        ("2317.TW","鴻海"),
        ("2454.TW","聯發科"),
        ("2303.TW","聯電"),
        ("2882.TW","國泰金"),
        ("2881.TW","富邦金"),
        ("2324.TW","仁寶"),
        ("2603.TW","長榮"),
        ("00919.TW","群益台灣精選高息")
    ]

with open(csv_path, encoding="utf-8") as f:

            for row in csv.reader(f):
                if len(row) >= 2:
                    items.append((row[0], row[1]))
                if len(items) >= limit:
                    break
        return items

    def scan(self, limit=50):
        analyzer = StockAnalyzer()
        results = []

        for symbol, name in self.load_symbols(limit):
            try:
                stock = analyzer.analyze(symbol, name)
                results.append(stock)
                print(f"✅ {name} {stock.ai_score}")
            except Exception as e:
                print(f"略過 {symbol} {name}: {e}")

        results.sort(key=lambda x: x.ai_score, reverse=True)
        return results

    def top10(self, stocks):
        return stocks[:10]

    def elite(self, stocks):
        return [s for s in stocks if s.ai_score >= 75][:3]

    def watch(self, stocks):
        return [s for s in stocks if 60 <= s.ai_score < 75][:10]

    def avoid(self, stocks):
        return [s for s in stocks if s.ai_score < 55][:10]


if __name__ == "__main__":
    brain = MarketBrain()
    stocks = brain.scan(limit=50)

    print("\n🔥 今日 Top10")
    for i, s in enumerate(brain.top10(stocks), 1):
        print(f"{i}. {s.name} AI {s.ai_score} 現價 {s.price}")

    print("\n🏆 Elite")
    for s in brain.elite(stocks):
        print(f"{s.name} AI {s.ai_score}")

    print("\n⭐ Watch List")
    for s in brain.watch(stocks)[:5]:
        print(f"{s.name} AI {s.ai_score}")

    print("\n🚫 Avoid")
    for s in brain.avoid(stocks)[:5]:
        print(f"{s.name} AI {s.ai_score}")
