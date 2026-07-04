
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from elsa_sprint2 import run as morning_run
from services.line_service import send_line_message

def morning():
    morning_run()

def close_report():
    msg = """🌇 Elsa AI 收盤分析

今天收盤資料整理中：
1. 今日強勢股
2. 今日轉弱股
3. 持股收盤狀態
4. 明日觀察名單
5. 今日學習重點

Build 003 會接真實收盤資料。
"""
    print(msg)
    send_line_message(msg)

def alert_check():
    msg = """🚨 Elsa AI 盤中 Alert 檢查

目前已啟動事件監控架構：
1. 突破壓力
2. 跌破停損
3. AI分數升高
4. 爆量轉強

Build 003 會接真實 Scanner。
"""
    print(msg)
    send_line_message(msg)

def monthly_manager():
    msg = """📅 Elsa AI 13號扣款經理人

已啟動每月扣款提醒架構：
扣款前3天、前1天、當天會分析：
ETF 是否偏貴
是否加碼
是否維持原扣款
是否保留現金

Build 004 會接真實 ETF 評分。
"""
    print(msg)
    send_line_message(msg)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "morning"

    if mode == "morning":
        morning()
    elif mode == "close":
        close_report()
    elif mode == "alert":
        alert_check()
    elif mode == "monthly":
        monthly_manager()
    else:
        print("可用模式：morning / close / alert / monthly")
