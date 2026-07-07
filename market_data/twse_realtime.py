import time
import requests

class TWSERealtime:

    def get_price(self, stock_id):
        url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp"
        params = {
            "ex_ch": f"tse_{stock_id}.tw",
            "json": "1",
            "delay": "0",
            "_": int(time.time() * 1000)
        }

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://mis.twse.com.tw/stock/index.jsp"
        }

        r = requests.get(url, params=params, headers=headers, timeout=10)
        data = r.json()

        if "msgArray" not in data or not data["msgArray"]:
            raise Exception("TWSE 即時資料抓取失敗")

        item = data["msgArray"][0]

        price_raw = item.get("z")
        if not price_raw or price_raw == "-":
            price_raw = item.get("y")

        return {
            "stock_id": stock_id,
            "name": item.get("n", ""),
            "price": float(price_raw),
            "open": float(item.get("o") or 0),
            "high": float(item.get("h") or 0),
            "low": float(item.get("l") or 0),
            "yesterday_close": float(item.get("y") or 0),
            "time": item.get("t", "")
        }
