from flask import Flask, jsonify
import subprocess
import sys
from datetime import datetime, time
from zoneinfo import ZoneInfo

app = Flask(__name__)

TW = ZoneInfo("Asia/Taipei")

@app.get("/")
def home():
    return jsonify({
        "status": "Elsa Render is alive",
        "time": datetime.now(TW).strftime("%Y-%m-%d %H:%M:%S")
    })

@app.get("/watch-auo")
def watch_auo():
    now = datetime.now(TW)
    weekday = now.weekday()  # 0=週一, 6=週日
    now_time = now.time()

    market_open = time(8, 55)
    market_close = time(13, 35)

    if weekday >= 5 or not (market_open <= now_time <= market_close):
        return jsonify({
            "status": "skip",
            "message": "非台股盯盤時間，Elsa 暫停巡邏",
            "time": now.strftime("%Y-%m-%d %H:%M:%S")
        })

    result = subprocess.run(
        [sys.executable, "elsa_auo_entry_watch.py"],
        capture_output=True,
        text=True
    )

    return jsonify({
        "status": "ok" if result.returncode == 0 else "error",
        "message": "AUO watch executed during market hours",
        "time": now.strftime("%Y-%m-%d %H:%M:%S")
    })
