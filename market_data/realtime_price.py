import time
import requests
from market_data.twse_realtime import TWSERealtime

class RealtimePrice:

    def yahoo_chart_price(self, symbol):
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        params = {"range": "1d", "interval": "1m"}
        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, params=params, headers=headers, timeout=10)
        data = r.json()

        result = data["chart"]["result"][0]
        price = result["meta"]["regularMarketPrice"]

        return {
            "source": "YahooChart",
            "price": round(float(price), 2)
        }

    def get_tw_stock_price(self, stock_id):
        try:
            return self.yahoo_chart_price(f"{stock_id}.TW")
        except Exception as e:
            print("YahooChart 即時價失敗：", e)

        try:
            q = TWSERealtime().get_price(stock_id)
            return {
                "source": "TWSE",
                "price": q["price"],
                "time": q.get("time")
            }
        except Exception as e:
            print("TWSE 即時價失敗：", e)

        raise Exception("即時價格來源全部失敗")
