from portfolio.portfolio_center import PortfolioCenter
from core.elsa_brain import ElsaBrain
from conversation.conversation_engine import ConversationEngine
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()
brain = ElsaBrain().load()

market = brain["market"] if brain else None

msg = ConversationEngine().morning_message(portfolio, market)

print(msg)
send_line_message(msg)
