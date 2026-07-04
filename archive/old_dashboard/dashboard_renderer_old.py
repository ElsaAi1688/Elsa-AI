import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PIL import Image, ImageDraw
from ai.analyze_stock import StockAnalyzer

stocks = [
    ("2324.TW", "仁寶"),
    ("2330.TW", "台積電"),
    ("0050.TW", "元大台灣50"),
]

img = Image.new("RGB", (1080, 1920), "#0F172A")
draw = ImageDraw.Draw(img)

analyzer = StockAnalyzer()

y = 40

for symbol, name in stocks:

    stock = analyzer.analyze(symbol, name)

    draw.rounded_rectangle(
        (40, y, 1040, y + 220),
        radius=25,
        fill="#1E293B"
    )

    draw.text((70, y + 20), stock.name, fill="white")
    draw.text((70, y + 60), f"AI：{stock.ai_score}", fill="#FACC15")
    draw.text((70, y + 100), f"技術：{stock.technical_score}", fill="white")
    draw.text((70, y + 130), f"基本：{stock.fundamental_score}", fill="white")
    draw.text((70, y + 160), f"籌碼：{stock.chip_score}", fill="white")

    y += 250

Path("reports/output").mkdir(parents=True, exist_ok=True)

img.save("reports/output/dashboard_v2.png")

print("✅ reports/output/dashboard_v2.png")
