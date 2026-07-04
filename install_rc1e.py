from pathlib import Path

Path("reports/portfolio_dashboard_v2.py").write_text(r'''
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

def circle(cx,cy,score,color="#FACC15"):
    score=int(score)
    draw.ellipse((cx-48,cy-48,cx+48,cy+48),outline="#334155",width=9)
    draw.arc((cx-48,cy-48,cx+48,cy+48),-90,-90+int(score*3.6),fill=color,width=9)
    draw.text((cx-28,cy-17),str(score),fill=color,font=big)

def money(v):
    return f"{v:,.2f}"

p=PortfolioCenter().analyze()
h=PortfolioHealth().calculate(p)

draw.text((36,24),"莎莎投資中心 Dashboard 2.0",fill="#F472B6",font=title)
draw.text((36,78),"真實持股・AI經理人・定投判斷・短線控管",fill="#CBD5E1",font=small)

box(36,115,1008,220,"📊 投資組合健康度")
circle(120,230,h["score"])
draw.text((205,168),f"健康度：{h['score']}/100｜{h['level']}｜{h['stars']}",fill="#FACC15",font=mid)
draw.text((205,212),f"投入成本：{money(p['total_cost'])}｜目前市值：{money(p['total_value'])}",fill="white",font=small)
draw.text((205,252),f"未實現損益：{money(p['total_pnl'])}（{p['total_pnl_pct']}%）",fill="#22C55E" if p["total_pnl"]>=0 else "#F87171",font=small)
draw.text((205,292),f"長期定投：{p['dca_ratio']}%｜短線操作：{p['short_ratio']}%",fill="#CBD5E1",font=small)

y=365
for item in p["holdings"]:
    pnl_color="#22C55E" if item["pnl"]>=0 else "#F87171"

    box(36,y,1008,360,f"📈 {item['name']}（{item['symbol']}）")

    circle(120,y+145,item["ai_score"])

    draw.text((200,y+65),f"策略：{item['strategy_label']}",fill="#CBD5E1",font=small)
    draw.text((200,y+105),f"成本：{item['cost']}｜現價：{item['price']}｜股數：{item['shares']}",fill="white",font=small)
    draw.text((200,y+145),f"投入：{money(item['invested'])}｜市值：{money(item['value'])}",fill="white",font=small)
    draw.text((200,y+185),f"損益：{money(item['pnl'])}（{item['pnl_pct']}%）",fill=pnl_color,font=small)

    draw.text((610,y+65),f"AI建議：{item['recommendation']}",fill="#FACC15",font=small)
    draw.text((610,y+105),f"經理人：{item['manager_advice']}",fill="#22C55E",font=small)
    draw.text((610,y+155),f"支撐：{item['support']}｜壓力：{item['resistance']}",fill="#CBD5E1",font=small)
    draw.text((610,y+195),f"停損：{item['stop_loss']}｜目標：{item['target_price']}",fill="#CBD5E1",font=small)
    draw.text((610,y+235),f"突破率：{item['breakout_probability']}%",fill="#FACC15",font=small)

    if item["strategy"] == "long_term_dca":
        draw.text((200,y+245),"定投判斷：每月13號前 Elsa 會重新評估是否增加投入。",fill="#BFDBFE",font=tiny)
    else:
        draw.text((200,y+245),"短線判斷：重點看突破、停損、停利，不用和定投股同邏輯。",fill="#FDE68A",font=tiny)

    y += 390

box(36,1545,1008,260,"🧑‍💼 今日經理人總結")
draw.text((70,1610),p["manager_summary"],fill="white",font=small)
draw.text((70,1655),"目前投資組合短線比例偏高，仁寶需嚴格看停損與突破。",fill="#CBD5E1",font=small)
draw.text((70,1700),"2330、0050 屬長期定投，不用因短線波動頻繁改變策略。",fill="#CBD5E1",font=small)
draw.text((70,1745),"13號扣款前，Elsa 會再依市場健康度與AI分數判斷是否多投入。",fill="#FACC15",font=small)

draw.text((36,1855),"風險提醒：AI 分析僅供參考，不是投資建議。請自行評估風險。",fill="#FACC15",font=tiny)

out=OUT/"portfolio_dashboard_rc1e.png"
img.save(out)
print("✅ RC1-E Portfolio Dashboard 2.0 完成：",out)

url=upload_image(str(out))
print("✅ 圖片已上傳：",url)
send_line_image(url)
''', encoding="utf-8")

Path("elsa_rc1e.py").write_text('''
import subprocess
import sys

subprocess.run([sys.executable, "reports/portfolio_dashboard_v2.py"], check=True)
''', encoding="utf-8")

print("✅ RC1-E 安裝完成")
