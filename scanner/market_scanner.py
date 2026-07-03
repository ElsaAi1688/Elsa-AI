import yfinance as yf

WATCH_LIST = [
    ("2330.TW","台積電"),
    ("2317.TW","鴻海"),
    ("2454.TW","聯發科"),
    ("2303.TW","聯電"),
    ("2382.TW","廣達"),
    ("2324.TW","仁寶"),
    ("2409.TW","友達"),
    ("2603.TW","長榮"),
    ("0050.TW","元大台灣50"),
    ("00878.TW","國泰永續高股息"),
]

def scan():

    result=[]

    for symbol,name in WATCH_LIST:

        try:

            df=yf.Ticker(symbol).history(period="5d")

            if df.empty:
                continue

            close=round(float(df["Close"].iloc[-1]),2)

            change=round(
                (float(df["Close"].iloc[-1])-float(df["Close"].iloc[-2]))
                /float(df["Close"].iloc[-2])*100
            ,2)

            volume=int(df["Volume"].iloc[-1])

            result.append({
                "symbol":symbol,
                "name":name,
                "price":close,
                "change":change,
                "volume":volume
            })

        except Exception as e:

            print(symbol,e)

    return result


if __name__=="__main__":

    stocks=scan()

    for s in stocks:

        print(
            s["symbol"],
            s["name"],
            s["price"],
            s["change"],
            s["volume"]
        )
