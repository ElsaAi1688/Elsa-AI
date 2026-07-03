import sys
from pathlib import Path
import csv

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ai.engines.technical_engine import TechnicalEngine
from ai.engines.fundamental_engine import FundamentalEngine
from ai.engines.chip_engine import ChipEngine

class Top10Engine:

    def generate(self):

        tech=TechnicalEngine()
        fund=FundamentalEngine()
        chip=ChipEngine()

        ranking=[]

        with open("data/watch_symbols.csv",encoding="utf-8") as f:

            reader=csv.reader(f)

            for row in reader:

                symbol,name=row

                try:

                    t=tech.analyze(symbol)
                    f1=fund.analyze(symbol)
                    c=chip.analyze(symbol)

                    score=round(
                        t["technical_score"]*0.30+
                        f1["fundamental_score"]*0.25+
                        c["chip_score"]*0.20+
                        50*0.15+
                        60*0.10
                    )

                    ranking.append({
                        "symbol":symbol,
                        "name":name,
                        "score":score,
                        "price":t["price"]
                    })

                except:
                    continue

        ranking.sort(key=lambda x:x["score"],reverse=True)

        return ranking[:10]


if __name__=="__main__":

    result=Top10Engine().generate()

    print("="*60)
    print("🔥 Elsa AI 全市場 Top10")
    print("="*60)

    for i,s in enumerate(result,1):

        print(
            f"{i}. {s['symbol']} {s['name']} "
            f"AI:{s['score']} "
            f"現價:{s['price']}"
        )
