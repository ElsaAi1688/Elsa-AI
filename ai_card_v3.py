from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys

today = datetime.now().strftime("%Y-%m-%d")

W, H = 1400, 1800
BG = (8, 10, 14)
CARD = (18, 23, 30)
BORDER = (70, 80, 95)

font_path = "/System/Library/Fonts/PingFang.ttc"
title_font = ImageFont.truetype(font_path, 54)
big_font = ImageFont.truetype(font_path, 38)
mid_font = ImageFont.truetype(font_path, 28)
small_font = ImageFont.truetype(font_path, 23)

symbol = sys.argv[1] if len(sys.argv) > 1 else "2324"
name = sys.argv[2] if len(sys.argv) > 2 else "仁寶"

chart_path = Path(f"charts/{symbol}_price_chart.png")

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

def box(x1, y1, x2, y2, title=None):
    draw.rounded_rectangle((x1, y1, x2, y2), radius=22, fill=CARD, outline=BORDER, width=2)
    if title:
        draw.text((x1+24, y1+18), title, fill=(120, 220, 255), font=mid_font)

draw.text((35, 25), "Elsa AI 智慧投資助理 🎉", fill=(230, 120, 255), font=title_font)
draw.text((35, 90), "AI 驅動・數據分析・智能決策・教學陪伴", fill=(220,220,220), font=mid_font)
draw.text((1040, 40), f"更新：{today}", fill=(180,180,190), font=small_font)

box(30, 140, 980, 1010)
draw.text((60, 165), f"{symbol} {name}", fill="white", font=big_font)
draw.text((60, 220), "收盤價：34.95     漲跌：-0.35 (-0.98%)     成交量：38,803 張", fill=(0,255,130), font=mid_font)

if chart_path.exists():
    chart = Image.open(chart_path).convert("RGB")
    chart = chart.resize((880, 520))
    img.paste(chart, (65, 290))
else:
    draw.text((360, 520), "尚無圖表", fill="white", font=big_font)

box(45, 835, 330, 980, "RSI (14)")
draw.text((75, 900), "43.2", fill="white", font=big_font)

box(355, 835, 650, 980, "MACD")
draw.text((385, 900), "DIF -0.08", fill=(70,160,255), font=mid_font)
draw.text((385, 940), "DEA -0.03", fill=(255,150,60), font=mid_font)

box(675, 835, 950, 980, "今日重點")
for i, t in enumerate(["股價站上 MA5", "MA20 下方偏弱", "成交量放大"]):
    draw.text((700, 890+i*35), f"✅ {t}", fill=(180,255,180), font=small_font)

box(1000, 140, 1370, 360)
draw.text((1030, 175), "AI 分數：68 / 100", fill="gold", font=big_font)
draw.text((1030, 230), "操作建議：觀察偏多", fill=(0,255,120), font=mid_font)
draw.text((1030, 280), "風險：中", fill=(255,180,60), font=mid_font)

box(1000, 390, 1370, 760, "圖表包含內容")
items = ["K線圖", "MA5", "MA20", "壓力區", "支撐區", "成交量", "RSI", "MACD"]
for i, item in enumerate(items):
    draw.text((1030, 445+i*36), f"✅ {item}", fill=(220,255,220), font=small_font)

box(1000, 790, 1370, 1160, "教學內容")
lessons = ["基礎觀念", "技術指標解釋", "買賣概念", "案例分析", "操作技巧"]
for i, item in enumerate(lessons):
    draw.text((1030, 845+i*45), f"{i+1}. {item}", fill=(230,230,230), font=small_font)

box(30, 1040, 980, 1280, "今天教學：什麼是壓力區和支撐區？")
draw.text((60, 1105), "壓力位：股價上漲時，常常在某個價位附近遇到賣壓。", fill=(120,255,120), font=small_font)
draw.text((60, 1150), "支撐區：股價下跌時，常常在某個價位附近遇到買盤。", fill=(120,255,120), font=small_font)
draw.text((60, 1210), "目前 2324 的壓力位在 36.00，支撐區在 34.20。", fill="white", font=small_font)

box(30, 1310, 450, 1710, "🔥 今日Top10 短線強勢股")
for i, s in enumerate(["6239 力成 96", "3037 欣興 93", "6442 光聖 92", "3265 台星科 90", "8046 南電 89"]):
    draw.text((60, 1370+i*55), f"{i+1}. {s}", fill=(255,230,160), font=small_font)

box(480, 1310, 900, 1710, "💎 今日Top10 定期定額 / ETF")
for i, s in enumerate(["0050 元大台灣50 95", "006208 富邦台50 93", "00919 群益高息 92", "00900 富邦特選 91", "00878 國泰永續 90"]):
    draw.text((510, 1370+i*55), f"{i+1}. {s}", fill=(160,220,255), font=small_font)

box(930, 1310, 1370, 1710, "⚠ 今日市場風險總覽")
draw.text((970, 1390), "大盤風險：中", fill="gold", font=mid_font)
draw.text((970, 1450), "類股風險：半導體高", fill=(255,120,120), font=small_font)
draw.text((970, 1510), "外資動向：買超", fill=(0,255,120), font=small_font)
draw.text((970, 1570), "市場情緒：偏多", fill=(0,255,120), font=small_font)
draw.text((970, 1640), "總分：62 / 100", fill="white", font=big_font)

Path("images").mkdir(exist_ok=True)
out = f"images/{symbol}_ai_card_v3.png"
img.save(out)
print("✅ Elsa AI v3 圖表完成：", out)
