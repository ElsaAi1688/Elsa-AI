import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scanner.market_scanner import scan

class AvoidEngine:

    def generate(self):

        avoid=[]

        for s in scan():

            score=50

            if s["change"] < -3:
                score-=25
            elif s["change"] < -1:
                score-=15
            elif s["change"] < 0:
                score-=8

            if s["volume"] > 30000000:
                score-=5

            if score <= 35:

                avoid.append({
                    "symbol":s["symbol"],
                    "name":s["name"],
                    "score":score,
                    "price":s["price"],
                    "reason":"弱勢下跌"
                })

        return sorted(avoid,key=lambda x:x["score"])


if __name__=="__main__":

    result=AvoidEngine().generate()

    print("="*60)
    print("🚫 Elsa Avoid List")
    print("="*60)

    if not result:
        print("今天沒有需要避開的股票")

    for i,s in enumerate(result,1):

        print(
            f"{i}. {s['symbol']} {s['name']} "
            f"AI:{s['score']} "
            f"現價:{s['price']} "
            f"{s['reason']}"
        )
