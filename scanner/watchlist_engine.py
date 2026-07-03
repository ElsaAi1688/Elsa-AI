import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scanner.market_scanner import scan

class WatchListEngine:

    def generate(self):

        watch=[]

        for s in scan():

            score=50

            if s["change"]>3:
                score+=25
            elif s["change"]>1:
                score+=15
            elif s["change"]>0:
                score+=8

            if s["volume"]>30000000:
                score+=10

            if score>=70:
                watch.append({
                    "symbol":s["symbol"],
                    "name":s["name"],
                    "score":score,
                    "price":s["price"],
                    "reason":"量價轉強"
                })

        return sorted(watch,key=lambda x:x["score"],reverse=True)

if __name__=="__main__":

    result=WatchListEngine().generate()

    print("="*60)
    print("⭐ Elsa Watch List")
    print("="*60)

    for i,s in enumerate(result,1):
        print(f"{i}. {s['symbol']} {s['name']} AI:{s['score']} 現價:{s['price']} {s['reason']}")
