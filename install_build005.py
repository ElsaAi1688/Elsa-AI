from pathlib import Path

Path("reports/dashboard_cache_renderer.py").write_text('''
import json
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from services.cloudinary_service import upload_image
from services.line_service import send_line_image

CACHE = Path("data/ai_cache/market_scan.json")
OUT = Path("reports/output")
OUT.mkdir(parents=True, exist_ok=True)

FONT="/System/Library/Fonts/PingFang.ttc"
title=ImageFont.truetype(FONT,42)
big=ImageFont.truetype(FONT,30)
mid=ImageFont.truetype(FONT,22)
small=ImageFont.truetype(FONT,17)

W,H=1080,1920
img=Image.new("RGB",(W,H),"#050816")
draw=ImageDraw.Draw(img)

def box(x,y,w,h,t):
    draw.rounded_rectangle((x,y,x+w,y+h),radius=22,fill="#111827",outline="#334155",width=2)
    draw.text((x+18,y+14),t,fill="#38BDF8",font=mid)

def bar(x,y,v,color):
    draw.rounded_rectangle((x,y,x+220,y+14),radius=7,fill="#263244")
    draw.rounded_rectangle((x,y,x+int(220*v/100),y+14),radius=7,fill=color)

data=json.loads(CACHE.read_text(encoding="utf-8"))
stocks=data["stocks"]

top10=stocks[:10]
elite=[s for s in stocks if s["ai_score"]>=75][:3]
watch=[s for s in stocks if 60<=s["ai_score"]<75][:8]
avoid=[s for s in stocks if s["ai_score"]<55][:5]

draw.text((36,24),"Elsa AI Professional Dashboard Build 005",fill="#F472B6",font=title)
draw.text((36,78),f"資料時間：{data['updated_at']}｜掃描 {data['count']} 檔",fill="#CBD5E1",font=small)

box(36,120,1008,150,"🌅 今日 AI 市場總覽")
draw.text((70,185),f"Top10：{len(top10)} 檔｜Elite：{len(elite)} 檔｜Watch：{len(watch)} 檔｜Avoid：{len(avoid)} 檔",fill="white",font=mid)

box(36,300,1008,420,"🔥 今日 Top10 強勢股")
y=360
for i,s in enumerate(top10,1):
    draw.text((70,y),f"{i}. {s['name']}  AI {s['ai_score']}  現價 {s['price']}",fill="#FDE68A",font=small)
    draw.text((560,y),f"突破率 {s['breakout_probability']}%｜壓力 {s['resistance']}｜支撐 {s['support']}",fill="#CBD5E1",font=small)
    y+=34

box(36,750,490,330,"🏆 Elsa Elite 精選")
y=810
if elite:
    for i,s in enumerate(elite,1):
        draw.text((70,y),f"{i}. {s['name']} AI {s['ai_score']}",fill="#FACC15",font=mid)
        draw.text((70,y+34),f"建議：{s['recommendation']}",fill="#22C55E",font=small)
        y+=85
else:
    draw.text((70,y),"今日暫無 Elite",fill="#CBD5E1",font=mid)

box(554,750,490,330,"⭐ Watch List 觀察名單")
y=810
for i,s in enumerate(watch[:6],1):
    draw.text((590,y),f"{i}. {s['name']} AI {s['ai_score']} 突破率 {s['breakout_probability']}%",fill="#A7F3D0",font=small)
    y+=42

box(36,1110,490,300,"🚫 Avoid 風險名單")
y=1170
if avoid:
    for i,s in enumerate(avoid,1):
        draw.text((70,y),f"{i}. {s['name']} AI {s['ai_score']}",fill="#FCA5A5",font=small)
        y+=40
else:
    draw.text((70,y),"今日暫無明顯 Avoid",fill="#CBD5E1",font=mid)

box(554,1110,490,300,"📚 今日股票課")
lesson=[
"主題：為什麼不能只看 AI 總分？",
"AI總分高，還要看突破率、壓力與支撐。",
"接近壓力區時，不適合盲目追高。",
"跌破支撐時，要先保護本金。"
]
y=1170
for t in lesson:
    draw.text((590,y),t,fill="white" if y==1170 else "#CBD5E1",font=small)
    y+=44

box(36,1440,1008,300,"📈 今日經理人結論")
best=top10[0] if top10 else None
if best:
    draw.text((70,1510),f"今日最強：{best['name']}｜AI {best['ai_score']}｜突破率 {best['breakout_probability']}%",fill="#FACC15",font=mid)
    draw.text((70,1560),f"操作：{best['recommendation']}",fill="#22C55E",font=mid)
    for i,r in enumerate(best["reasons"][:4]):
        draw.text((70,1620+i*34),f"✔ {r}",fill="#CBD5E1",font=small)

draw.text((36,1845),"風險提醒：AI 分析僅供參考，不是投資建議。請自行評估風險。",fill="#FACC15",font=small)

out=OUT/"elsa_dashboard_build005.png"
img.save(out)
print("✅ Build 005 Dashboard 完成：",out)

url=upload_image(str(out))
print("✅ 圖片已上傳：",url)
send_line_image(url)
''', encoding="utf-8")

Path("elsa_build005.py").write_text('''
from scanner.market_cache import load_market_scan, save_market_scan
from pathlib import Path
import subprocess, sys

if load_market_scan() is None:
    save_market_scan(limit=200)

subprocess.run([sys.executable, "reports/dashboard_cache_renderer.py"], check=True)
''', encoding="utf-8")

print("✅ Build 005 安裝完成")
