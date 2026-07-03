from ai.stock_analysis import StockAnalysis

stock = StockAnalysis(
    symbol="2324",
    name="仁寶",
    price=34.95
)

stock.technical_score = 82
stock.fundamental_score = 78
stock.chip_score = 70
stock.news_score = 68
stock.market_score = 75

stock.calculate_score()

stock.breakout_probability = 81

stock.support = 34.2
stock.resistance = 35.3

stock.target_price = 37

stock.stop_loss = 33.8

stock.confidence = 84

stock.recommendation = "續抱"

stock.next_action = "等待突破35.3"

stock.learning_topic = "MA20"

stock.learning_content = "今天股價仍在 MA20 下方，所以 AI 保守。"

print(stock)
