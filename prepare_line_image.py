from PIL import Image
from pathlib import Path
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
src = Path(f"images/dashboard_{today}.png")
dst = Path("public/dashboard.jpg")

Path("public").mkdir(exist_ok=True)

img = Image.open(src).convert("RGB")
img.thumbnail((1000, 1800))
img.save(dst, "JPEG", quality=85, optimize=True)

print("✅ LINE 圖片已準備：", dst)
