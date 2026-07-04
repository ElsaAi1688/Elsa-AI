from pathlib import Path

Path("ai").mkdir(exist_ok=True)
Path("services").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

Path("ai/score_engine.py").write_text('''
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
''', encoding="utf-8")

Path("ai/manager_engine.py").write_text('''
class ManagerEngine:
    def advice(self, stock):
        lines = []
        lines.append(f"📈 {stock.name}（{stock.symbol}）")
        lines.append(f"AI總分：{stock.ai_score}/100")
        lines.append(f"建議：{stock.recommendation}")
        lines.append(f"現價：{stock.price}")
        lines.append(f"支撐：{stock.support}")
        lines.append(f"壓力：{stock.resistance}")
        lines.append(f"停損：{stock.stop_loss}")
        lines.append(f"目標價：{stock.target_price}")
        lines.append(f"突破率：{stock.breakout_probability}%")
        lines.append("理由：")
        for r in stock.reasons[:6]:
            lines.append(f"✔ {r}")
        return "\\n".join(lines)
''', encoding="utf-8")

Path("services/alert_engine.py").write_text('''
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
''', encoding="utf-8")

Path("services/monthly_manager.py").write_text('''
from datetime import datetime

class MonthlyManager:
    def check(self, stocks):
        today = datetime.now().day

        if today not in [10, 12, 13]:
            return []

        lines = []
        lines.append("📅 每月13日扣款經理人提醒")

        if today == 10:
            lines.append("距離扣款日還有3天")
        elif today == 12:
            lines.append("明天就是扣款日")
        elif today == 13:
            lines.append("今天是扣款日")

        for stock in stocks:
            if stock.ai_score >= 75:
                action = "本月可考慮多投入"
            elif stock.ai_score >= 60:
                action = "維持原扣款"
            else:
                action = "暫不加碼，保留現金"

            lines.append(f"{stock.name}：{action}（AI {stock.ai_score}）")

        return lines
''', encoding="utf-8")

Path("elsa_sprint2.py").write_text('''
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from ai.analyze_stock import StockAnalyzer
from ai.score_engine import ScoreEngine
from ai.manager_engine import ManagerEngine
from services.alert_engine import AlertEngine
from services.monthly_manager import MonthlyManager
from services.line_service import send_line_message

WATCHLIST = [
    ("2324.TW", "仁寶"),
    ("2330.TW", "台積電"),
    ("0050.TW", "元大台灣50"),
]

def run():
    analyzer = StockAnalyzer()
    scorer = ScoreEngine()
    manager = ManagerEngine()
    alert_engine = AlertEngine()

    stocks = []
    alerts = []

    report = []
    report.append("🌅 Elsa AI Sprint 2 經理人晨報")
    report.append(f"更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("=" * 30)

    for symbol, name in WATCHLIST:
        stock = analyzer.analyze(symbol, name)
        stock = scorer.calculate(stock)
        stocks.append(stock)

        report.append(manager.advice(stock))
        report.append("-" * 30)

        alerts.extend(alert_engine.check(stock))

    if alerts:
        report.append("🚨 即時 Alert")
        report.extend(alerts)
        report.append("-" * 30)

    monthly = MonthlyManager().check(stocks)
    if monthly:
        report.extend(monthly)
        report.append("-" * 30)

    report.append("📚 今日股票課")
    report.append("高分不代表一定買，要看技術面、基本面、籌碼面是否一起轉強。")
    report.append("突破壓力且量能放大，才是比較健康的進場訊號。")

    text = "\\n".join(report)

    Path("reports/sprint2_report.txt").write_text(text, encoding="utf-8")

    print(text)
    send_line_message(text)

if __name__ == "__main__":
    run()
''', encoding="utf-8")

print("✅ Elsa AI Sprint 2 整包安裝完成")
