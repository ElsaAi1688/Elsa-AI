from portfolio.portfolio_center import PortfolioCenter
from core.elsa_brain import ElsaBrain
from conversation.conversation_engine import ConversationEngine
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()
brain = ElsaBrain().load()

if brain is None:
    brain = ElsaBrain().update(limit=200)

market = brain["market"]

msg = ConversationEngine().morning_message(portfolio, market)

msg += "\n\n🔥 今日 Top5\n"
for i, s in enumerate(market["top10"][:5], 1):
    msg += f"{i}. {s['name']} AI {s['ai_score']} 現價 {s['price']}\n"

msg += "\n📌 今天策略\n"
msg += "不追高，先看持股，再看 Watch List 是否真正突破。"

print(msg)
send_line_message(msg)
