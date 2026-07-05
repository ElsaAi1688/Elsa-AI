
import sys
from core.elsa_brain import ElsaBrain
from portfolio.portfolio_center import PortfolioCenter
from conversation.conversation_engine import ConversationEngine
from alerts.alert_engine import AlertEngine
from manager.dca_manager import DCAManager
from services.line_service import send_line_message

mode = sys.argv[1] if len(sys.argv) > 1 else "morning"

brain = ElsaBrain().load()
if brain is None:
    brain = ElsaBrain().update(limit=200)

portfolio = PortfolioCenter().analyze()
market = brain["market"]
conversation = ConversationEngine()

if mode == "morning":
    msg = conversation.morning_message(portfolio, market)
    msg += "\n\n🔥 今日 Top5\n"
    for i, s in enumerate(market["top10"][:5], 1):
        msg += f"{i}. {s['name']} AI {s['ai_score']} 現價 {s['price']}\n"
    msg += "\n📌 今日策略\n莎莎，今天先看持股安全，再看 Watch List 是否真的突破。"

elif mode == "close":
    lines = []
    lines.append("👩‍💼 Elsa 收盤經理人")
    lines.append("莎莎，我幫妳整理今天收盤後最重要的事。")
    lines.append("=" * 30)
    lines.append("📈 持股狀態")
    for h in portfolio["holdings"]:
        lines.append(f"{h['name']}｜AI {h['ai_score']}｜損益 {h['pnl_pct']}%")
        lines.append(f"經理人：{h['manager_advice']}")
    lines.append("")
    lines.append("⭐ 明日觀察")
    for s in market["watch"][:5]:
        lines.append(f"{s['name']}｜AI {s['ai_score']}｜突破率 {s['breakout_probability']}%")
    lines.append("")
    lines.append("📌 Elsa 結論")
    lines.append("明天不要追高，只觀察真正帶量突破的股票。")
    msg = "\n".join(lines)

elif mode == "alert":
    stocks = market["top10"] + market["watch"]
    alerts = AlertEngine().generate_alerts(stocks)
    lines = ["🚨 Elsa 盤中經理人 Alert", "=" * 30]
    if alerts:
        lines.append("莎莎，目前有事件值得注意：")
        lines.extend(alerts)
    else:
        lines.append("莎莎，目前沒有高優先事件。")
        lines.append("今天不用硬交易，等待也是操作。")
    msg = "\n".join(lines)

elif mode == "dca":
    items = DCAManager().analyze(portfolio)
    lines = ["💰 Elsa 13號定投經理人", "=" * 30]
    for x in items:
        lines.append(f"📈 {x['name']}")
        lines.append(f"AI：{x['ai']} {x['level']}")
        lines.append(f"原扣款：{x['amount']} 元")
        lines.append(f"本月建議：{x['recommend']} 元")
        lines.append(f"經理人：{x['advice']}")
        lines.append("-" * 30)
    lines.append("莎莎，定投不是每次都加碼，便宜才多投入，過熱就守紀律。")
    msg = "\n".join(lines)

else:
    msg = "可用模式：morning / close / alert / dca"

print(msg)
send_line_message(msg)
