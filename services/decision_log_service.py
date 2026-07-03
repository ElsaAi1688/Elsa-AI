from pathlib import Path
from datetime import datetime
import json

LOG_FILE = Path("data/decision_log.json")


def save_decision(stock_result, suggestion):
    Path("data").mkdir(exist_ok=True)

    if LOG_FILE.exists():
        logs = json.loads(LOG_FILE.read_text(encoding="utf-8"))
    else:
        logs = []

    log = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "symbol": stock_result["symbol"],
        "name": stock_result["name"],
        "type": stock_result["type"],
        "close": round(float(stock_result["close"]), 2),
        "score": stock_result["score"],
        "confidence": stock_result.get("confidence", 0),
        "risk_level": stock_result.get("risk_level", "未評估"),
        "suggestion": suggestion
    }

    logs.append(log)
    LOG_FILE.write_text(json.dumps(logs, ensure_ascii=False, indent=2), encoding="utf-8")
