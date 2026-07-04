
import json
from pathlib import Path

from alerts.alert_engine import AlertEngine
from services.line_service import send_line_message

CACHE = Path("data/ai_cache/market_scan.json")
data = json.loads(CACHE.read_text(encoding="utf-8"))
stocks = data["stocks"]

alerts = AlertEngine().generate_alerts(stocks)

lines = []
lines.append("🚨 Elsa AI Build 009")
lines.append("盤中 Alert 事件通知")
lines.append("=" * 30)

if alerts:
    lines.extend(alerts)
else:
    lines.append("目前沒有觸發重大事件。")

lines.append("")
lines.append("Alert 條件：AI高分、突破率高、接近壓力、跌破停損。")

msg = "\n".join(lines)

Path("reports/build009_alert_report.txt").write_text(msg, encoding="utf-8")

print(msg)
send_line_message(msg)
