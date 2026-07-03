from datetime import datetime
from pathlib import Path

from config import MY_STOCK, STOCK_NAME, BUY_PRICE, SHARES, TAKE_PROFIT_RATE, STOP_LOSS_RATE, TARGET_RATE
from services.stock_service import get_stock_data
from services.line_service import send_line_message
from services.chart_service import create_price_chart
from analysis.indicators import calculate_ma, calculate_rsi, calculate_macd
from analysis.ai_score import analyze

today = datetime.now().strftime("%Y-%m-%d")

history = get_stock_data(MY_STOCK)

if history is None:
    print("找不到股票資料")
else:
    latest = history.iloc[-1]

    close = latest["Close"]
    high = latest["High"]
    low = latest["Low"]
    volume = latest["Volume"]

    ma5 = calculate_ma(history, 5)
    ma20 = calculate_ma(history, 20)
    rsi = calculate_rsi(history)
    macd, signal = calculate_macd(history)

    profit = (close - BUY_PRICE) * SHARES
    percent = ((close - BUY_PRICE) / BUY_PRICE) * 100

    take_profit = BUY_PRICE * TAKE_PROFIT_RATE
    stop_loss = BUY_PRICE * STOP_LOSS_RATE
    target_price = BUY_PRICE * TARGET_RATE

    score, messages, confidence, risk_level = analyze(close, BUY_PRICE, ma5, ma20, rsi, macd, signal, volume)

    if close >= take_profit:
        suggestion = "🎯 操作建議：已達停利區，可考慮分批獲利了結"
    elif close <= stop_loss:
        suggestion = "🛑 操作建議：跌破停損區，注意風險控管"
    elif score >= 75:
        suggestion = "✅ 操作建議：續抱觀察，有機會挑戰目標價"
    elif score >= 55:
        suggestion = "🟡 操作建議：觀察為主，等待更明確訊號"
    else:
        suggestion = "🔴 操作建議：短線偏弱，注意停損風險"

    report = f"""
=============================================
🤖 Elsa AI 每日操盤報告 v1.0
日期：{today}
=============================================

📈 股票：{MY_STOCK} {STOCK_NAME}
💰 成本：{BUY_PRICE:.2f}
💵 現價：{close:.2f}
📦 股數：{SHARES}

📊 損益：{profit:.2f} 元
📈 報酬率：{percent:.2f}%

🎯 停利價：{take_profit:.2f}
🛑 停損價：{stop_loss:.2f}
🚀 目標價：{target_price:.2f}

📈 最高價：{high:.2f}
📉 最低價：{low:.2f}
📈 MA5：{ma5:.2f}
📉 MA20：{ma20:.2f}
📊 RSI：{rsi:.2f}
📉 MACD：{macd:.4f}
📉 Signal：{signal:.4f}
📊 成交量：{int(volume):,}

=============================================
🤖 AI 分析
=============================================
{chr(10).join(messages)}

⭐ AI 分數：{score}/100

{suggestion}
"""

    print(report)

    Path("reports").mkdir(exist_ok=True)
    file_path = Path("reports") / f"report_{today}.txt"
    file_path.write_text(report, encoding="utf-8")

    chart_path = create_price_chart(history, MY_STOCK, STOCK_NAME, BUY_PRICE, take_profit, stop_loss, score, confidence, risk_level)
    print(f"✅ 圖表已儲存：{chart_path}")

    print(f"✅ 報告已儲存：{file_path}")

    send_line_message(report)
