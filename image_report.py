from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys

from services.stock_service import get_stock_data
from analysis.indicators import calculate_ma, calculate_rsi, calculate_macd
from analysis.ai_score import analyze
from services.chart_service import create_price_chart
from services.manager_service import get_manager_suggestion

WIDTH = 1080
HEIGHT = 1920
today = datetime.now().strftime("%Y-%m-%d")

if len(sys.argv) >= 6:
    MY_STOCK = sys.argv[1]
    STOCK_NAME = sys.argv[2]
    BUY_PRICE = float(sys.argv[3])
    SHARES = int(float(sys.argv[4]))
    STOCK_TYPE = sys.argv[5]
else:
    MY_STOCK = "2324"
    STOCK_NAME = "仁寶"
    BUY_PRICE = 35.3
    SHARES = 283
    STOCK_TYPE = "short"

history = get_stock_data(MY_STOCK)
latest = history.iloc[-1]

close = latest["Close"]
volume = latest["Volume"]

ma5 = calculate_ma(history, 5)
ma20 = calculate_ma(history, 20)
rsi = calculate_rsi(history)
macd, signal = calculate_macd(history)

profit = (close - BUY_PRICE) * SHARES if BUY_PRICE > 0 and SHARES > 0 else 0
percent = ((close - BUY_PRICE) / BUY_PRICE) * 100 if BUY_PRICE > 0 else 0

score, messages, confidence, risk_level = analyze(
    close,
    BUY_PRICE if BUY_PRICE > 0 else close,
    ma5,
    ma20,
    rsi,
    macd,
    signal,
    volume
)

take_profit = BUY_PRICE * 1.05 if BUY_PRICE > 0 else close * 1.05
stop_loss = BUY_PRICE * 0.97 if BUY_PRICE > 0 else close * 0.97

chart_path = create_price_chart(
    history,
    MY_STOCK,
    STOCK_NAME,
    BUY_PRICE if BUY_PRICE > 0 else close,
    take_profit,
    stop_loss,
    score,
    confidence,
    risk_level
)

stock_result = {
    "type": STOCK_TYPE,
    "score": score,
    "confidence": confidence,
    "risk_level": risk_level,
    "percent": percent
}
manager = get_manager_suggestion(stock_result)
suggestion = manager["action"]

if False:
    if percent >= 5:
        suggestion = "短線達獲利區，可考慮分批賣出"
    elif percent <= -3:
        suggestion = "接近停損區，請控管風險"
    elif score >= 55:
        suggestion = "觀察續抱，等待轉強訊號"
    else:
        suggestion = "短線偏弱，不建議加碼"
elif STOCK_TYPE == "dca":
    suggestion = "長期定投，維持紀律扣款"
else:
    suggestion = "觀察中，等待更明確訊號"

img = Image.new("RGB", (WIDTH, HEIGHT), (15, 17, 23))
draw = ImageDraw.Draw(img)

font_path = "/System/Library/Fonts/PingFang.ttc"
title_font = ImageFont.truetype(font_path, 60)
big_font = ImageFont.truetype(font_path, 44)
mid_font = ImageFont.truetype(font_path, 34)
small_font = ImageFont.truetype(font_path, 28)

def card(x1, y1, x2, y2):
    draw.rounded_rectangle((x1, y1, x2, y2), radius=30, fill=(30, 34, 46))

draw.text((50, 40), "Elsa AI 每日分析卡", fill="white", font=title_font)
draw.text((50, 115), f"日期：{today}", fill=(180, 180, 190), font=small_font)

card(40, 170, 1040, 430)
draw.text((70, 200), f"{MY_STOCK} {STOCK_NAME}", fill=(0, 255, 150), font=big_font)
draw.text((70, 260), f"現價：{close:.2f}｜成本：{BUY_PRICE:.2f}｜股數：{SHARES}", fill="white", font=mid_font)
draw.text((70, 305), f"損益：{profit:.0f} 元｜報酬率：{percent:.2f}%", fill="white", font=small_font)
draw.text((70, 355), f"AI 分數：{score}/100", fill="gold", font=mid_font)
draw.text((420, 355), f"信心值：{confidence}/100", fill=(120, 220, 255), font=mid_font)
draw.text((760, 355), f"風險：{risk_level}", fill="orange", font=mid_font)

chart = Image.open(chart_path).convert("RGB")
chart = chart.resize((1000, 560))
img.paste(chart, (40, 470))

card(40, 1070, 1040, 1280)
draw.text((70, 1100), "今日建議", fill=(90, 220, 255), font=big_font)
draw.text((70, 1160), suggestion, fill="white", font=mid_font)
draw.text((70, 1210), f"上漲機率：{manager['upside_probability']}%｜下跌風險：{manager['downside_probability']}%｜持有：{manager['hold_days']}", fill=(180, 220, 255), font=small_font)

card(40, 1320, 1040, 1660)
draw.text((70, 1350), "今日重點", fill=(120, 180, 255), font=big_font)

y = 1420
for msg in messages[:4]:
    draw.text((70, y), msg, fill="white", font=small_font)
    y += 48

draw.text((50, 1810), "Elsa AI｜股票經理人・學習教練・風險提醒", fill=(160, 160, 170), font=small_font)

Path("images").mkdir(exist_ok=True)
outfile = f"images/{MY_STOCK}_daily_card.png"
img.save(outfile)

print("✅ 圖片完成：", outfile)
