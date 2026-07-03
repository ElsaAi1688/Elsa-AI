import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from data_provider import DataProvider
from ai.stock_analysis import StockAnalysis
from ai.engines.technical_engine import TechnicalEngine
from ai.engines.fundamental_engine import FundamentalEngine
from ai.engines.chip_engine import ChipEngine

class StockAnalyzer:

    def analyze(self,symbol,name):

        provider=DataProvider()

        history=provider.get_history(symbol)

        stock=StockAnalysis(symbol=symbol,name=name)

        tech=TechnicalEngine().analyze_from_data(history)
        fund=FundamentalEngine().analyze(symbol)
        chip=ChipEngine().analyze(symbol)

        stock.price=tech["price"]

        stock.technical_score=tech["technical_score"]
        stock.fundamental_score=fund["fundamental_score"]
        stock.chip_score=chip["chip_score"]

        stock.news_score=50
        stock.market_score=60

        stock.calculate_score()

        stock.reasons.extend(tech["reasons"])
        stock.reasons.extend(fund["reasons"])
        stock.reasons.extend(chip["reasons"])

        return stock


if __name__=="__main__":

    print(
        StockAnalyzer().analyze(
            "2324.TW",
            "仁寶"
        )
    )
