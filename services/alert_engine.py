
class AlertEngine:
    def check(self, stock):
        alerts = []

        if stock.ai_score >= 85:
            alerts.append(f"🚨 {stock.name} 進入 Elite，AI {stock.ai_score}")

        if stock.breakout_probability >= 80:
            alerts.append(f"🚨 {stock.name} 突破機率 {stock.breakout_probability}%")

        if stock.price and stock.stop_loss and stock.price <= stock.stop_loss:
            alerts.append(f"⚠️ {stock.name} 跌破停損價，請注意風險")

        return alerts
