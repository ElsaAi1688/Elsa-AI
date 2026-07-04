
class AlertEngine:

    def generate_alerts(self, stocks):
        alerts = []

        for s in stocks:
            name = s["name"]
            score = s["ai_score"]
            breakout = s["breakout_probability"]
            price = s["price"]
            resistance = s["resistance"]
            stop_loss = s["stop_loss"]

            if score >= 85:
                alerts.append(f"🚨 {name} 進入強勢名單｜AI {score}")

            if breakout >= 80:
                alerts.append(f"🚀 {name} 突破機率 {breakout}%｜可列入盤中觀察")

            if price and resistance and price >= resistance * 0.99:
                alerts.append(f"⚡ {name} 接近壓力 {resistance}｜等待帶量突破")

            if price and stop_loss and price <= stop_loss:
                alerts.append(f"⚠️ {name} 跌破停損 {stop_loss}｜注意風險")

        return alerts[:10]
