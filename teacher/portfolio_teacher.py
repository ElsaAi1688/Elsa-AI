
class PortfolioTeacher:

    def pick_lesson(self, portfolio):
        for h in portfolio["holdings"]:
            if h["strategy"] == "short_term":
                return {
                    "title": "什麼叫突破？",
                    "stock": h["name"],
                    "content": [
                        f"妳目前持有 {h['name']}，這檔是短線操作。",
                        f"目前壓力位是 {h['resistance']}。",
                        "短線股不是看到漲就追，而是要等突破壓力。",
                        "突破時如果成交量也放大，勝率會比較好。",
                        "如果沒有突破就追高，容易買在壓力附近。"
                    ]
                }

        return {
            "title": "定期定額為什麼不用每天看？",
            "stock": "長期投資",
            "content": [
                "2330 和 0050 屬於長期定投。",
                "定投重點不是每天猜高低點，而是長期累積。",
                "Elsa 會在每月13號前提醒是否適合多投入。"
            ]
        }
