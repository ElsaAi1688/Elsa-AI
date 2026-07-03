from dataclasses import dataclass, asdict
from typing import List


@dataclass
class StockScore:
    symbol: str
    name: str
    category: str

    technical: int
    fundamental: int
    chip: int
    news: int
    market: int

    def total_score(self):

        return round(
            self.technical * 0.30 +
            self.fundamental * 0.25 +
            self.chip * 0.20 +
            self.news * 0.15 +
            self.market * 0.10
        )


class RankingEngine:

    def __init__(self):

        self.stocks = []

    def add(self, stock):

        self.stocks.append(stock)

    def top_short(self):

        return sorted(
            self.stocks,
            key=lambda x: x.total_score(),
            reverse=True
        )[:10]

    def top_etf(self):

        etf = [
            s for s in self.stocks
            if s.category == "ETF"
        ]

        return sorted(
            etf,
            key=lambda x: x.total_score(),
            reverse=True
        )[:10]


if __name__ == "__main__":

    engine = RankingEngine()

    engine.add(
        StockScore(
            "2324",
            "仁寶",
            "Stock",
            82,
            70,
            68,
            75,
            72
        )
    )

    engine.add(
        StockScore(
            "0050",
            "元大台灣50",
            "ETF",
            90,
            95,
            85,
            80,
            88
        )
    )

    print("🔥 Top Short")

    for s in engine.top_short():

        print(
            s.symbol,
            s.name,
            s.total_score()
        )

    print()

    print("💎 Top ETF")

    for s in engine.top_etf():

        print(
            s.symbol,
            s.name,
            s.total_score()
        )

