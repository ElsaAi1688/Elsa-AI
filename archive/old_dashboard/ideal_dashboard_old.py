import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai.analyze_stock import StockAnalyzer

W,H = 1080,1920
img = Image.new("RGB",(W,H),"#080B12")
draw = ImageDraw.Draw(img)

font_path="/System/Library/Fonts/PingFang.ttc"
title=ImageFont.truetype(font_path,48)
big=ImageFont.truetype(font_path,34)
mid=ImageFont.truetype(font_path,26)
small=ImageFont.truetype(font_path,22)

def card(x,y,w,h,title_text):
    draw.rounded_rectangle((x,y,x+w,y+h),radius=24,fill="#111827",outline="#334155",width=2)
    draw.text((x+24,y+18),title_text,fill="#38BDF8",font=mid)

def bar(x,y,value,color):
    draw.rounded_rectangle((x,y,x+300,y+18),radius=9,fill="#263244")
    draw.rounded_rectangle((x,y,x+int(300*value/100),y+18),radius=9,fill=color)

draw.text((40,30),"Elsa AI 智慧投資助理",fill="#F472B6",font=title)
draw.text((40,88),"AI驅動・數據分析・智能決策・教學陪伴",fill="#CBD5E1",font=small)

analyzer=StockAnalyzer()
stocks=[
    ("2324.TW","仁寶"),
    ("2330.TW","台積電"),
    ("0050.TW","元大台灣50"),
]

y=140
for symbol,name in stocks:
    s=analyzer.analyze(symbol,name)
    card(40,y,1000,300,f"📈 {s.name}  {s.symbol}")
    draw.text((70,y+70),f"AI 總分：{s.ai_score}/100",fill="#FACC15",font=big)
    draw.text((70,y+120),f"現價：{s.price}",fill="#FFFFFF",font=mid)
    draw.text((70,y+160),f"建議：{s.recommendation}",fill="#22C55E",font=mid)

    draw.text((520,y+70),f"技術面 {s.technical_score}",fill="white",font=small)
    bar(660,y+78,s.technical_score,"#22C55E")
    draw.text((520,y+110),f"基本面 {s.fundamental_score}",fill="white",font=small)
    bar(660,y+118,s.fundamental_score,"#60A5FA")
    draw.text((520,y+150),f"籌碼面 {s.chip_score}",fill="white",font=small)
    bar(660,y+158,s.chip_score,"#F97316")

    ry=y+210
    for r in s.reasons[:3]:
        draw.text((70,ry),f"✔ {r}",fill="#CBD5E1",font=small)
        ry+=28

    y+=330

card(40,1140,480,300,"🔥 今日 Top10 短線股")
top=["1. 廣達 AI 72","2. 長榮 AI 71","3. 台積電 AI 68","4. 聯發科 AI 68","5. 聯電 AI 66"]
for i,t in enumerate(top):
    draw.text((70,1205+i*42),t,fill="#FDE68A",font=small)

card(560,1140,480,300,"⭐ Elsa Watch List")
watch=["1. 聯電 量價轉強","2. 長榮 突破觀察","3. 仁寶 等待35.3","4. 0050 定投觀察"]
for i,t in enumerate(watch):
    draw.text((590,1205+i*42),t,fill="#A7F3D0",font=small)

card(40,1470,480,260,"🏆 Elsa Elite")
draw.text((70,1535),"1. 聯電 AI 85 ★★★★★",fill="#FACC15",font=small)
draw.text((70,1580),"今天符合強勢關注條件",fill="#CBD5E1",font=small)

card(560,1470,480,260,"📚 今日股票課")
draw.text((590,1535),"主題：為什麼要看 AI 分數拆解？",fill="#FFFFFF",font=small)
draw.text((590,1580),"高分不代表一定買，要看技術、基本、籌碼",fill="#CBD5E1",font=small)
draw.text((590,1625),"三個面向一起轉強，勝率才會提高。",fill="#CBD5E1",font=small)

Path("reports/output").mkdir(parents=True,exist_ok=True)
out="reports/output/elsa_ideal_dashboard.png"
img.save(out)
print("✅ 理想版 Dashboard 完成：",out)
