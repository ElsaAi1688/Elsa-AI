from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime
import json

today = datetime.now().strftime("%Y-%m-%d")

WIDTH = 1080
HEIGHT = 1920

canvas = Image.new("RGB", (WIDTH, HEIGHT), (18, 20, 28))
draw = ImageDraw.Draw(canvas)

font_candidates = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
]

font = None
for f in font_candidates:
    if Path(f).exists():
        font = f
        break

if font:
    title = ImageFont.truetype(font, 56)
    normal = ImageFont.truetype(font, 32)
    small = ImageFont.truetype(font, 24)
else:
    title = ImageFont.load_default()
    normal = ImageFont.load_default()
    small = ImageFont.load_default()

portfolio = json.loads(Path("portfolio.json").read_text(encoding="utf-8"))
holdings = portfolio.get("holdings", [])

logs = []
log_path = Path("data/decision_log.json")
if log_path.exists():
    logs = json.loads(log_path.read_text(encoding="utf-8"))

today_logs = [x for x in logs if x.get("date") == today]
best = max(today_logs, key=lambda x: x.get("score", 0)) if today_logs else None

total_profit = 0
for item in holdings:
    symbol = item["symbol"]
    shares = item.get("shares", 0)
    buy_price = item.get("buy_price", 0)

    matched = [x for x in today_logs if x.get("symbol") == symbol]
    if matched and shares > 0 and buy_price > 0:
        close = matched[-1].get("close", 0)
        total_profit += (close - buy_price) * shares

draw.text((40, 35), "Elsa AI Dashboard v2", fill="white", font=title)
draw.text((40, 105), today, fill=(170, 170, 170), font=small)

draw.rounded_rectangle((40, 145, 1040, 265), radius=25, fill=(30, 34, 46))
draw.text((70, 170), f"今日總損益：{total_profit:.0f} 元", fill="gold", font=normal)

if best:
    draw.text((70, 215), f"今日最高分：{best['symbol']} {best['name']}｜{best['score']}/100", fill=(0, 255, 150), font=small)

cards = [
    "2324_daily_card.png",
    "2330_daily_card.png",
    "0050_daily_card.png",
    "2409_daily_card.png",
    "009816_daily_card.png"
]

x = 40
y = 300

for card in cards:
    path = Path("images") / card

    if path.exists():
        img = Image.open(path)
        img = img.resize((480, 760))
        canvas.paste(img, (x, y))

        if x < 500:
            x = 560
        else:
            x = 40
            y += 780

Path("images").mkdir(exist_ok=True)

outfile = f"images/dashboard_{today}.png"
canvas.save(outfile)

print("✅ Dashboard v2 完成：", outfile)
