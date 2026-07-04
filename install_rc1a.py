from pathlib import Path
import json

Path("portfolio").mkdir(exist_ok=True)

holdings = [
    {
        "symbol": "2330.TW",
        "name": "台積電",
        "shares": 2,
        "cost": 2420,
        "strategy": "long_term_dca",
        "monthly_dca_day": 13,
        "monthly_dca_amount": 5000,
        "start_date": "2026-06-03"
    },
    {
        "symbol": "0050.TW",
        "name": "元大台灣50",
        "shares": 28,
        "cost": 107.55,
        "strategy": "long_term_dca",
        "monthly_dca_day": 13,
        "monthly_dca_amount": 3000,
        "start_date": "2026-06-03"
    },
    {
        "symbol": "2324.TW",
        "name": "仁寶",
        "shares": 283,
        "cost": 35.3,
        "strategy": "short_term",
        "buy_date": "2026-07-01"
    }
]

Path("portfolio/holdings.json").write_text(
    json.dumps(holdings, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

Path("portfolio/portfolio_center.py").write_text('''
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
''', encoding="utf-8")

Path("elsa_rc1a.py").write_text('''
from portfolio.portfolio_center import PortfolioCenter
from services.line_service import send_line_message

p = PortfolioCenter().analyze()

lines = []
lines.append("👩 莎莎投資中心 RC1-A 正式版")
lines.append("=" * 30)
lines.append(f"投入成本：{p['total_cost']}")
lines.append(f"目前市值：{p['total_value']}")
lines.append(f"未實現損益：{p['total_pnl']}（{p['total_pnl_pct']}%）")
lines.append(f"投資健康度：{p['avg_ai']}/100｜{p['health']}")
lines.append(f"長期定投比例：{p['dca_ratio']}%")
lines.append(f"短線操作比例：{p['short_ratio']}%")
lines.append("")

for h in p["holdings"]:
    lines.append(f"📈 {h['name']}（{h['symbol']}）")
    lines.append(f"策略：{h['strategy_label']}")
    lines.append(f"成本：{h['cost']}｜現價：{h['price']}｜股數：{h['shares']}")
    lines.append(f"投入：{h['invested']}｜市值：{h['value']}")
    lines.append(f"損益：{h['pnl']}（{h['pnl_pct']}%）")
    lines.append(f"AI：{h['ai_score']}｜建議：{h['recommendation']}")
    lines.append(f"經理人：{h['manager_advice']}")
    lines.append(f"支撐：{h['support']}｜壓力：{h['resistance']}")
    lines.append(f"停損：{h['stop_loss']}｜目標：{h['target_price']}")
    lines.append("-" * 30)

lines.append("📌 經理人一句話")
lines.append(p["manager_summary"])

msg = "\\n".join(lines)
print(msg)
send_line_message(msg)
''', encoding="utf-8")

print("✅ RC1-A Portfolio Core 正式持股版安裝完成")
