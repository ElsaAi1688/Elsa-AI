import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scanner.watchlist_engine import WatchListEngine

class EliteEngine:

    def generate(self):

        watch = WatchListEngine().generate()

        elite = []

        for s in watch:

            if s["score"] >= 80:

                elite.append({
                    "symbol": s["symbol"],
                    "name": s["name"],
                    "score": s["score"],
                    "price": s["price"],
                    "recommendation": "★★★★★ 強烈關注"
                })

        return elite[:3]


if __name__=="__main__":

    result = EliteEngine().generate()

    print("="*60)
    print("🏆 Elsa Elite")
    print("="*60)

    if not result:
        print("今天沒有符合條件的股票")

    for i,s in enumerate(result,1):

        print(
            f"{i}. {s['symbol']} {s['name']} "
            f"AI:{s['score']} "
            f"現價:{s['price']} "
            f"{s['recommendation']}"
        )
