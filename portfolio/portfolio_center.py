
import json
from pathlib import Path
from datetime import datetime
from ai.analyze_stock import StockAnalyzer

HOLDINGS = Path("portfolio/holdings.json")

class PortfolioCenter:

    def load_holdings(self):
        return json.loads(HOLDINGS.read_text(encoding="utf-8"))

    def strategy_label(self, h):
        if h.get("strategy") == "long_term_dca":
            return f"長期定期定額｜每月{h.get('monthly_dca_day')}號｜{h.get('monthly_dca_amount')}元"
        if h.get("strategy") == "short_term":
            return "短線操作"
        return "一般持股"

    def strategy_advice(self, h, stock, pnl_pct):
        strategy = h.get("strategy")

        if strategy == "long_term_dca":
            if stock.ai_score >= 75:
                return "本月可考慮增加扣款或維持定投"
            elif stock.ai_score >= 60:
                return "維持原本定期定額，不急著加碼"
            else:
                return "暫時維持小額定投，保留現金等待更好價格"

        if strategy == "short_term":
            if stock.breakout_probability >= 75 and stock.ai_score >= 70:
                return "短線續抱，等待突破或停利訊號"
            elif stock.price <= stock.stop_loss:
                return "接近或跌破停損，需優先控管風險"
            elif pnl_pct > 5:
                return "已有獲利，可分批停利或提高停損"
            else:
                return "短線觀察，不追高，等待量價確認"

        return stock.recommendation

    def analyze(self):
        analyzer = StockAnalyzer()
        results = []

        total_cost = 0
        total_value = 0
        total_ai = 0
        dca_value = 0
        short_value = 0

        for h in self.load_holdings():
            stock = analyzer.analyze(h["symbol"], h["name"])

            shares = h["shares"]
            cost = h["cost"]

            invested = shares * cost
            value = shares * stock.price
            pnl = value - invested
            pnl_pct = round(pnl / invested * 100, 2) if invested else 0

            total_cost += invested
            total_value += value
            total_ai += stock.ai_score

            if h.get("strategy") == "long_term_dca":
                dca_value += value
            elif h.get("strategy") == "short_term":
                short_value += value

            results.append({
                "symbol": h["symbol"],
                "name": h["name"],
                "shares": shares,
                "cost": cost,
                "price": stock.price,
                "value": round(value, 2),
                "invested": round(invested, 2),
                "pnl": round(pnl, 2),
                "pnl_pct": pnl_pct,
                "ai_score": stock.ai_score,
                "recommendation": stock.recommendation,
                "strategy": h.get("strategy"),
                "strategy_label": self.strategy_label(h),
                "manager_advice": self.strategy_advice(h, stock, pnl_pct),
                "monthly_dca_day": h.get("monthly_dca_day"),
                "monthly_dca_amount": h.get("monthly_dca_amount"),
                "support": stock.support,
                "resistance": stock.resistance,
                "stop_loss": stock.stop_loss,
                "target_price": stock.target_price,
                "breakout_probability": stock.breakout_probability,
                "reasons": stock.reasons[:5]
            })

        avg_ai = round(total_ai / len(results)) if results else 0
        total_pnl = total_value - total_cost
        total_pnl_pct = round(total_pnl / total_cost * 100, 2) if total_cost else 0

        dca_ratio = round(dca_value / total_value * 100, 1) if total_value else 0
        short_ratio = round(short_value / total_value * 100, 1) if total_value else 0

        if avg_ai >= 80:
            health = "優秀"
        elif avg_ai >= 65:
            health = "穩健"
        elif avg_ai >= 50:
            health = "普通"
        else:
            health = "偏弱"

        manager_summary = "目前以長期定投為核心，短線仁寶需嚴守停損與突破訊號。"

        return {
            "total_cost": round(total_cost, 2),
            "total_value": round(total_value, 2),
            "total_pnl": round(total_pnl, 2),
            "total_pnl_pct": total_pnl_pct,
            "avg_ai": avg_ai,
            "health": health,
            "dca_ratio": dca_ratio,
            "short_ratio": short_ratio,
            "manager_summary": manager_summary,
            "holdings": results
        }
