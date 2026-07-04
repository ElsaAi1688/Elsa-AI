
class ScoreEngine:
    def calculate(self, stock):
        stock.calculate_score()

        if stock.ai_score >= 80:
            stock.recommendation = "強勢續抱 / 可觀察加碼"
        elif stock.ai_score >= 70:
            stock.recommendation = "續抱觀察"
        elif stock.ai_score >= 60:
            stock.recommendation = "中性觀察"
        else:
            stock.recommendation = "保守 / 暫不加碼"

        return stock
