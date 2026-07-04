
from datetime import datetime

class DCAManager:

    def analyze(self, portfolio):

        today = datetime.now()

        result = []

        for h in portfolio["holdings"]:

            if h["strategy"] != "long_term_dca":
                continue

            ai = h["ai_score"]

            if ai >= 80:
                advice = "建議增加20%"
                level = "★★★★★"
                factor = 1.2

            elif ai >= 70:
                advice = "維持原扣款"
                level = "★★★★☆"
                factor = 1.0

            elif ai >= 60:
                advice = "維持小額定投"
                level = "★★★☆☆"
                factor = 1.0

            else:
                advice = "保留現金，本月不建議增加"
                level = "★★☆☆☆"
                factor = 1.0

            amount = h.get("monthly_dca_amount",0)
            recommend = round(amount*factor)

            result.append({

                "name":h["name"],

                "day":h["monthly_dca_day"],

                "ai":ai,

                "level":level,

                "amount":amount,

                "recommend":recommend,

                "advice":advice

            })

        return result
