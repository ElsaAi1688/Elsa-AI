import requests
import pandas as pd
from datetime import datetime, timedelta

class ChipEngine:

    def analyze(self, stock_id):
        score = 50
        explain = []

        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        try:
            r = requests.get(
                "https://api.finmindtrade.com/api/v4/data",
                params={
                    "dataset": "TaiwanStockInstitutionalInvestorsBuySell",
                    "data_id": stock_id,
                    "start_date": start,
                    "end_date": end
                },
                timeout=20
            )

            data = r.json().get("data", [])
            if not data:
                return {"score": 50, "explain": [{"name":"法人","status":"資料不足","points":0,"reason":"暫無法人資料"}]}

            df = pd.DataFrame(data)
            recent = df.tail(15)

            for name in ["Foreign_Investor", "Investment_Trust", "Dealer"]:
                sub = recent[recent["name"] == name]
                if sub.empty:
                    continue

                net = float(sub["buy"].sum() - sub["sell"].sum())

                label = {
                    "Foreign_Investor": "外資",
                    "Investment_Trust": "投信",
                    "Dealer": "自營商"
                }[name]

                if net > 0:
                    pts = 10 if label != "投信" else 15
                    score += pts
                    explain.append({"name":label,"status":"買超","points":pts,"reason":f"近幾日合計買超 {round(net)} 股"})
                elif net < 0:
                    pts = -10 if label != "投信" else -15
                    score += pts
                    explain.append({"name":label,"status":"賣超","points":pts,"reason":f"近幾日合計賣超 {round(abs(net))} 股"})
                else:
                    explain.append({"name":label,"status":"中性","points":0,"reason":"買賣超接近平衡"})

        except Exception as e:
            explain.append({"name":"法人","status":"錯誤","points":0,"reason":str(e)})

        return {"score": max(0, min(round(score), 100)), "explain": explain}
