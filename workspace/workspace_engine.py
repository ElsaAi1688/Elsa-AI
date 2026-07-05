
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
