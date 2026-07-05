from portfolio.portfolio_center import PortfolioCenter
from trade.trade_manager import TradeManager
from services.line_service import send_line_message

class LiveExitAlert:

    def check_compal(self):
        portfolio = PortfolioCenter().analyze()
        tm = TradeManager()

        h = next(x for x in portfolio["holdings"] if x["symbol"] == "2324.TW")
        t = tm.evaluate(h)

        price = h["price"]
        resistance = h["resistance"]
        stop = t["exit_plan"]["stop_loss"]
        target1 = t["exit_plan"]["target1"]
        target2 = t["exit_plan"]["target2"]
        target3 = t["exit_plan"]["target3"]

        alerts = []

        if price <= stop:
            alerts.append("⚠️ 跌破停損，優先保護本金")

        if price >= target3:
            alerts.append("🏁 已達第三目標，可考慮完成出場")
        elif price >= target2:
            alerts.append("🎯 已達第二目標，可考慮再減碼 30%")
        elif price >= target1:
            alerts.append("🎯 已達第一目標，可考慮先減碼 20%")

        if resistance and price >= resistance * 0.99:
            alerts.append(f"⚡ 接近壓力 {resistance}，準備觀察是否轉弱或突破")

        if not alerts:
            print("仁寶目前未觸發下車提醒")
            return False

        msg = []
        msg.append("🚨 Elsa Live Exit Alert")
        msg.append("仁寶即時下車提醒")
        msg.append("=" * 30)
        msg.append(f"現價：{price}")
        msg.append(f"成本：{h['cost']}")
        msg.append(f"目前損益：{t['profit_pct']}%")
        msg.append(f"狀態：{t['state']}")
        msg.append("")
        msg.append("觸發條件：")
        for a in alerts:
            msg.append(a)
        msg.append("")
        msg.append("出場計畫：")
        msg.append(f"第一目標：{target1} → 減碼 20%")
        msg.append(f"第二目標：{target2} → 再減碼 30%")
        msg.append(f"第三目標：{target3} → 完成出場")
        msg.append(f"停損：{stop} → 保護本金")
        msg.append("")
        msg.append("👩‍💼 Elsa：莎莎，現在先不要慌，照計畫分批處理。")

        final = "\n".join(msg)
        print(final)
        send_line_message(final)
        return True
