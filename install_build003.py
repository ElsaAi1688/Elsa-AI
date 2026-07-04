from pathlib import Path

Path("scanner/market_brain.py").write_text('''
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai.analyze_stock import StockAnalyzer

class MarketBrain:

    def load_symbols(self, limit=50):
        items = []
        with open("data/watch_symbols.csv", encoding="utf-8") as f:
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

    print("\\n🔥 今日 Top10")
    for i, s in enumerate(brain.top10(stocks), 1):
        print(f"{i}. {s.name} AI {s.ai_score} 現價 {s.price}")

    print("\\n🏆 Elite")
    for s in brain.elite(stocks):
        print(f"{s.name} AI {s.ai_score}")

    print("\\n⭐ Watch List")
    for s in brain.watch(stocks)[:5]:
        print(f"{s.name} AI {s.ai_score}")

    print("\\n🚫 Avoid")
    for s in brain.avoid(stocks)[:5]:
        print(f"{s.name} AI {s.ai_score}")
''', encoding="utf-8")

Path("elsa_build003.py").write_text('''
from scanner.market_brain import MarketBrain
from services.line_service import send_line_message

brain = MarketBrain()
stocks = brain.scan(limit=50)

lines = []
lines.append("🧠 Elsa AI Build 003 Market Brain")
lines.append("=" * 30)

lines.append("🔥 今日 Top10")
for i, s in enumerate(brain.top10(stocks), 1):
    lines.append(f"{i}. {s.name} AI {s.ai_score} 現價 {s.price}")

lines.append("")
lines.append("🏆 Elite")
elite = brain.elite(stocks)
if elite:
    for s in elite:
        lines.append(f"{s.name} AI {s.ai_score}")
else:
    lines.append("今日暫無 Elite")

lines.append("")
lines.append("⭐ Watch List")
for s in brain.watch(stocks)[:8]:
    lines.append(f"{s.name} AI {s.ai_score} 突破率 {s.breakout_probability}%")

lines.append("")
lines.append("🚫 Avoid")
avoid = brain.avoid(stocks)
if avoid:
    for s in avoid[:5]:
        lines.append(f"{s.name} AI {s.ai_score}")
else:
    lines.append("今日暫無明顯 Avoid")

msg = "\\n".join(lines)
print(msg)
send_line_message(msg)
''', encoding="utf-8")

print("✅ Build 003 Part A 安裝完成")
