from pathlib import Path

Path("workspace").mkdir(exist_ok=True)
Path("reports/output").mkdir(parents=True, exist_ok=True)

Path("workspace/workspace_engine.py").write_text('''
from core.elsa_brain import ElsaBrain
from portfolio.portfolio_center import PortfolioCenter
from portfolio.portfolio_health import PortfolioHealth
from decision.decision_engine import ElsaDecisionEngine
from teacher.portfolio_teacher import PortfolioTeacher

class WorkspaceEngine:

    def build(self):
        brain = ElsaBrain().load()
        if brain is None:
            brain = ElsaBrain().update(limit=200)

        portfolio = PortfolioCenter().analyze()
        health = PortfolioHealth().calculate(portfolio)
        decision = ElsaDecisionEngine().decide_portfolio(portfolio)
        lesson = PortfolioTeacher().pick_lesson(portfolio)

        market = brain["market"]

        return {
            "brain": brain,
            "market": market,
            "portfolio": portfolio,
            "health": health,
            "decision": decision,
            "lesson": lesson
        }
''', encoding="utf-8")

Path("workspace/workspace_message.py").write_text('''
class WorkspaceMessage:

    def render(self, data):
        p = data["portfolio"]
        h = data["health"]
        d = data["decision"]
        m = data["market"]
        lesson = data["lesson"]

        lines = []
        lines.append("👩‍💼 Elsa Workspace v1.0")
        lines.append("莎莎，我已經幫妳整理好今天的投資工作台。")
        lines.append("=" * 30)

        lines.append("🧠 今日總決策")
        lines.append(d["main_message"])
        lines.append("")

        lines.append("💼 我的投資中心")
        lines.append(f"投入成本：{p['total_cost']}")
        lines.append(f"目前市值：{p['total_value']}")
        lines.append(f"未實現損益：{p['total_pnl']}（{p['total_pnl_pct']}%）")
        lines.append(f"健康度：{h['score']}/100｜{h['level']} {h['stars']}")
        lines.append("")

        lines.append("📈 我的持股決策")
        for x in d["decisions"]:
            lines.append(f"{x['name']}｜{x['action']}｜信心 {x['confidence']}%")
            lines.append(f"原因：{x['decision']}")
        lines.append("")

        lines.append("🔥 今日市場機會")
        for i, s in enumerate(m["top10"][:5], 1):
            lines.append(f"{i}. {s['name']} AI {s['ai_score']}｜突破率 {s['breakout_probability']}%")
        lines.append("")

        lines.append("📚 今日老師")
        lines.append(f"主題：{lesson['title']}")
        for c in lesson["content"][:3]:
            lines.append(f"・{c}")

        lines.append("")
        lines.append("📌 Elsa 今日一句話")
        lines.append("今天先照紀律走，不追高，等待高勝率機會。")

        return "\\n".join(lines)
''', encoding="utf-8")

Path("workspace/workspace_renderer.py").write_text(r'''
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from workspace.workspace_engine import WorkspaceEngine
from services.cloudinary_service import upload_image
from services.line_service import send_line_image

OUT = Path("reports/output")
OUT.mkdir(parents=True, exist_ok=True)

FONT="/System/Library/Fonts/PingFang.ttc"
title=ImageFont.truetype(FONT,44)
big=ImageFont.truetype(FONT,34)
mid=ImageFont.truetype(FONT,23)
small=ImageFont.truetype(FONT,18)
tiny=ImageFont.truetype(FONT,15)

img=Image.new("RGB",(1080,1920),"#050816")
draw=ImageDraw.Draw(img)

def box(x,y,w,h,t,color="#38BDF8"):
    draw.rounded_rectangle((x,y,x+w,y+h),radius=26,fill="#111827",outline="#334155",width=2)
    draw.text((x+22,y+16),t,fill=color,font=mid)

def circle(cx,cy,score,color="#FACC15"):
    score=int(score)
    draw.ellipse((cx-55,cy-55,cx+55,cy+55),outline="#334155",width=10)
    draw.arc((cx-55,cy-55,cx+55,cy+55),-90,-90+int(score*3.6),fill=color,width=10)
    draw.text((cx-30,cy-18),str(score),fill=color,font=big)

def money(v):
    return f"{v:,.0f}"

data=WorkspaceEngine().build()
p=data["portfolio"]
h=data["health"]
d=data["decision"]
m=data["market"]
lesson=data["lesson"]

draw.text((36,24),"Elsa Workspace v1.0",fill="#F472B6",font=title)
draw.text((36,82),"妳的 AI 投資工作台｜決策・持股・市場・老師",fill="#CBD5E1",font=small)

box(36,125,1008,230,"👩‍💼 Elsa 今日總決策")
circle(125,245,h["score"])
draw.text((210,175),"莎莎，今天我幫妳整理好了。",fill="white",font=mid)
draw.text((210,220),d["main_message"],fill="#FACC15",font=small)
draw.text((210,265),"今天先照紀律走，不追高，等待高勝率機會。",fill="#CBD5E1",font=small)

box(36,385,1008,250,"💼 我的投資中心")
draw.text((70,450),f"投入成本：{money(p['total_cost'])}",fill="white",font=small)
draw.text((70,492),f"目前市值：{money(p['total_value'])}",fill="white",font=small)
draw.text((70,534),f"未實現損益：{money(p['total_pnl'])}（{p['total_pnl_pct']}%）",fill="#22C55E" if p["total_pnl"]>=0 else "#F87171",font=small)
draw.text((560,450),f"健康度：{h['score']}/100｜{h['level']}｜{h['stars']}",fill="#FACC15",font=mid)
draw.text((560,505),f"長期定投：{p['dca_ratio']}%｜短線：{p['short_ratio']}%",fill="#CBD5E1",font=small)

box(36,665,1008,390,"📈 我的持股決策")
y=725
for x in d["decisions"]:
    draw.rounded_rectangle((70,y,1010,y+90),radius=18,fill="#0B1220",outline="#1E293B",width=1)
    draw.text((95,y+18),f"{x['name']}｜決策：{x['action']}｜信心 {x['confidence']}%",fill="#FACC15",font=small)
    draw.text((95,y+52),x["decision"],fill="#CBD5E1",font=tiny)
    y+=110

box(36,1085,490,360,"🔥 今日市場機會")
y=1145
for i,s in enumerate(m["top10"][:7],1):
    draw.text((65,y),f"{i}. {s['name']} AI {s['ai_score']}｜突破率 {s['breakout_probability']}%",fill="#FDE68A",font=tiny)
    y+=40

box(554,1085,490,360,"⭐ Watch / Elite")
y=1145
draw.text((585,y),"🏆 Elite",fill="#FACC15",font=small); y+=38
if m["elite"]:
    for s in m["elite"][:3]:
        draw.text((585,y),f"{s['name']} AI {s['ai_score']}",fill="#FACC15",font=tiny); y+=34
else:
    draw.text((585,y),"今日暫無 Elite",fill="#CBD5E1",font=tiny); y+=34

y+=20
draw.text((585,y),"⭐ Watch",fill="#A7F3D0",font=small); y+=38
for s in m["watch"][:4]:
    draw.text((585,y),f"{s['name']} AI {s['ai_score']}｜突破率 {s['breakout_probability']}%",fill="#A7F3D0",font=tiny)
    y+=34

box(36,1475,1008,270,"📚 今日老師")
draw.text((70,1540),f"主題：{lesson['title']}",fill="#FACC15",font=mid)
yy=1590
for c in lesson["content"][:4]:
    draw.text((70,yy),f"・{c}",fill="#CBD5E1",font=small)
    yy+=42

draw.text((36,1845),"風險提醒：AI 分析僅供參考，不是投資建議。請自行評估風險。",fill="#FACC15",font=tiny)

out=OUT/"elsa_workspace_v1.png"
img.save(out)
print("✅ Elsa Workspace 圖片完成：",out)

url=upload_image(str(out))
print("✅ 圖片已上傳：",url)
send_line_image(url)
''', encoding="utf-8")

Path("elsa_workspace.py").write_text('''
from workspace.workspace_engine import WorkspaceEngine
from workspace.workspace_message import WorkspaceMessage
from services.line_service import send_line_message
import subprocess, sys

data = WorkspaceEngine().build()
msg = WorkspaceMessage().render(data)

print(msg)
send_line_message(msg)

subprocess.run([sys.executable, "workspace/workspace_renderer.py"], check=True)
''', encoding="utf-8")

print("✅ Workspace v1.0 安裝完成")
