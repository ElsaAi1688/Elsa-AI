from flask import Flask, jsonify
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({
        "status": "Elsa Render is alive",
        "time": datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S")
    })

@app.get("/watch-auo")
def watch_auo():
    result = subprocess.run(
        [sys.executable, "elsa_auo_entry_watch.py"],
        capture_output=True,
        text=True
    )

    ok = result.returncode == 0

    return jsonify({
        "status": "ok" if ok else "error",
        "message": "AUO watch executed",
        "time": datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S")
    })
