from pathlib import Path

Path("reports").mkdir(exist_ok=True)
Path("reports/output").mkdir(parents=True, exist_ok=True)

Path("reports/portfolio_dashboard.py").write_text(r'''
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from portfolio.portfolio_center import PortfolioCenter
from portfolio.portfolio_health import PortfolioHealth
from services.cloudinary_service import upload_image
from services.line_service import send_line_image

OUT = Path("reports/output")
OUT.mkdir(parents=True, exist_ok=True)

FONT="/System/Library/Fonts/PingFang.ttc"
title=ImageFont.truetype(FONT,42)
big=ImageFont.truetype(FONT,32)
mid=ImageFont.truetype(FONT,23)
small=ImageFont.truetype(FONT,18)
tiny=ImageFont.truetype(FONT,15)

img=Image.new("RGB",(1080,1920),"#050816")
draw=ImageDraw.Draw(img)

def box(x,y,w,h,t,color="#38BDF8"):
    draw.rounded_rectangle((x,y,x+w,y+h),radius=22,fill="#111827",outline="#334155",width=2)
    draw.text((x+18,y+14),t,fill=color,font=mid)

def circle(cx,cy,score):
    score=int(score)
    draw.ellipse((cx-48,cy-48,cx+48,cy+48),outline="#334155",width=9)
    draw.arc((cx-48,cy-48,cx+48,cy+48),-90,-90+int(score*3.6),fill="#FACC15",width=9)
    draw.text((cx-28,cy-17),str(score),fill="#FACC15",font=big)

def money(v):
    return f"{v:,.2f}"

p=PortfolioCenter().analyze()
h=PortfolioHealth().calculate(p)

draw.text((36,24),"莎莎投資中心 RC1-C",fill="#F472B6",font=title)
draw.text((36,78),"Portfolio Center｜真實持股｜AI 經理人",fill="#CBD5E1",font=small)

box(36,120,1008,230,"📊 投資組合總覽")
circle(125,235,h["score"])
draw.text((210,175),f"投資健康度：{h['score']}/100｜{h['level']}｜{h['stars']}",fill="#FACC15",font=mid)
draw.text((210,220),f"投入成本：{money(p['total_cost'])}",fill="white",font=small)
draw.text((210,260),f"目前市值：{money(p['total_value'])}",fill="white",font=small)
draw.text((210,300),f"未實現損益：{money(p['total_pnl'])}（{p['total_pnl_pct']}%）",fill="#22C55E" if p["total_pnl"]>=0 else "#F87171",font=small)

box(36,380,490,240,"💼 資產配置")
draw.text((70,445),f"長期定期定額：{p['dca_ratio']}%",fill="#BFDBFE",font=mid)
draw.text((70,500),f"短線操作：{p['short_ratio']}%",fill="#FDE68A",font=mid)
draw.text((70,555),"2330 / 0050：長期累積",fill="#CBD5E1",font=small)
draw.text((70,585),"仁寶：短線交易，嚴守停損",fill="#CBD5E1",font=small)

box(554,380,490,240,"🧑‍💼 經理人總結")
draw.text((590,445),p["manager_summary"],fill="white",font=small)
draw.text((590,505),"原則：定投股看長期，短線股看突破與停損。",fill="#CBD5E1",font=small)
draw.text((590,565),"13號扣款前會重新評估是否加碼。",fill="#FACC15",font=small)

y=650
for item in p["holdings"]:
    box(36,y,1008,295,f"📈 {item['name']}（{item['symbol']}）")
    circle(115,y+135,item["ai_score"])

    draw.text((200,y+62),f"策略：{item['strategy_label']}",fill="#CBD5E1",font=small)
    draw.text((200,y+102),f"成本：{item['cost']}｜現價：{item['price']}｜股數：{item['shares']}",fill="white",font=small)
    draw.text((200,y+142),f"投入：{money(item['invested'])}｜市值：{money(item['value'])}",fill="white",font=small)
    draw.text((200,y+182),f"損益：{money(item['pnl'])}（{item['pnl_pct']}%）",fill="#22C55E" if item["pnl"]>=0 else "#F87171",font=small)

    draw.text((610,y+70),f"AI 建議：{item['recommendation']}",fill="#FACC15",font=small)
    draw.text((610,y+110),f"經理人：{item['manager_advice']}",fill="#22C55E",font=small)
    draw.text((610,y+155),f"支撐：{item['support']}｜壓力：{item['resistance']}",fill="#CBD5E1",font=small)
    draw.text((610,y+195),f"停損：{item['stop_loss']}｜目標：{item['target_price']}",fill="#CBD5E1",font=small)

    y += 320

box(36,1630,1008,210,"📌 今日提醒")
draw.text((70,1690),"2330、0050 是長期定期定額，不用用短線邏輯判斷。",fill="#CBD5E1",font=small)
draw.text((70,1735),"仁寶是短線操作，重點看突破、停損、停利。",fill="#CBD5E1",font=small)
draw.text((70,1780),"每月13號扣款前，Elsa 會提醒是否建議多投入。",fill="#FACC15",font=small)

out=OUT/"portfolio_dashboard_rc1c.png"
img.save(out)
print("✅ 投資中心 Dashboard 完成：",out)

url=upload_image(str(out))
print("✅ 圖片已上傳：",url)
send_line_image(url)
''', encoding="utf-8")

Path("elsa_rc1c.py").write_text('''
import subprocess
import sys

subprocess.run([sys.executable, "reports/portfolio_dashboard.py"], check=True)
''', encoding="utf-8")

print("✅ RC1-C 完整版安裝完成")
