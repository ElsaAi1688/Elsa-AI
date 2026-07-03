from ai.stock_analysis import StockAnalysis
from ai.engines.technical_engine import TechnicalEngine
from ai.engines.fundamental_engine import FundamentalEngine
from ai.engines.chip_engine import ChipEngine

symbol="2324.TW"
name="仁寶"

stock=StockAnalysis(symbol=symbol,name=name)

t=TechnicalEngine().analyze(symbol)
f=FundamentalEngine().analyze(symbol)
c=ChipEngine().analyze(symbol)

stock.price=t["price"]

stock.technical_score=t["technical_score"]
stock.fundamental_score=f["fundamental_score"]
stock.chip_score=c["chip_score"]

stock.news_score=50
stock.market_score=60

stock.calculate_score()

stock.reasons.extend(t["reasons"])
stock.reasons.extend(f["reasons"])
stock.reasons.extend(c["reasons"])

print("="*60)
print(stock.symbol,stock.name)
print("="*60)
print("AI總分：",stock.ai_score)
print("技術面：",stock.technical_score)
print("基本面：",stock.fundamental_score)
print("籌碼面：",stock.chip_score)
print("新聞面：",stock.news_score)
print("市場面：",stock.market_score)

print()
print("AI理由：")

for r in stock.reasons:
    print("✔",r)

print("="*60)
