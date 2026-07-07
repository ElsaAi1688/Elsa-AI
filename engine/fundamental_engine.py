import requests
import pandas as pd
from datetime import datetime, timedelta

class FundamentalEngine:

    def analyze(self, stock_id):
        score = 50
        explain = []

        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=800)).strftime("%Y-%m-%d")

        try:
            r = requests.get(
                "https://api.finmindtrade.com/api/v4/data",
                params={
                    "dataset": "TaiwanStockMonthRevenue",
                    "data_id": stock_id,
                    "start_date": start,
                    "end_date": end
                },
                timeout=20
            )
            data = r.json().get("data", [])
            if not data:
                return {"score": 50, "explain": [{"name":"月營收","status":"資料不足","points":0,"reason":"暫無月營收資料"}]}

            df = pd.DataFrame(data).sort_values("date")
            latest = df.iloc[-1]
            y = latest["revenue_year"]
            m = latest["revenue_month"]
            rev = float(latest["revenue"])

            prev = df[(df["revenue_year"] == y - 1) & (df["revenue_month"] == m)]

            if not prev.empty:
                prev_rev = float(prev.iloc[-1]["revenue"])
                yoy = round((rev - prev_rev) / prev_rev * 100, 2)

                if yoy > 10:
                    score += 20
                    explain.append({"name":"月營收","status":"年增強","points":20,"reason":f"月營收年增 {yoy}%"})
                elif yoy > 0:
                    score += 10
                    explain.append({"name":"月營收","status":"年增","points":10,"reason":f"月營收年增 {yoy}%"})
                else:
                    score -= 15
                    explain.append({"name":"月營收","status":"年減","points":-15,"reason":f"月營收年減 {abs(yoy)}%"})
            else:
                explain.append({"name":"月營收","status":"待比較","points":0,"reason":"缺去年同期資料"})

        except Exception as e:
            explain.append({"name":"月營收","status":"錯誤","points":0,"reason":str(e)})

        return {"score": max(0, min(round(score), 100)), "explain": explain}
