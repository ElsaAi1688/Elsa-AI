
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

    text = "\n".join(report)

    Path("reports/sprint2_report.txt").write_text(text, encoding="utf-8")

    print(text)
    send_line_message(text)

if __name__ == "__main__":
    run()
