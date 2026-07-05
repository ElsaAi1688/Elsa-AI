class PositionManager:

    def score(self, holding):

        score = 20

        strategy = holding.get("strategy","")

        if strategy=="short_term":
            score += 40

        pnl = holding.get("pnl_pct",0)

        if abs(pnl)>=5:
            score += 20

        resistance=holding.get("resistance")

        price=holding.get("price")

        if resistance and price>=resistance*0.98:
            score += 25

        return min(score,100)

    def need_watch(self,holding):

        return self.score(holding)>=60
