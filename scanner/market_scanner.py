import csv
import yfinance as yf

def load_symbols():
    stocks=[]
    with open("data/watch_symbols.csv",encoding="utf-8") as f:
        for row in csv.reader(f):
            if row:
                stocks.append((row[0],row[1]))
    return stocks

def scan():

    result=[]

    for symbol,name in load_symbols():

        try:

            df=yf.Ticker(symbol).history(period="5d")

            if df.empty:
                continue

            close=float(df["Close"].iloc[-1])
            prev=float(df["Close"].iloc[-2])

            result.append({
                "symbol":symbol,
                "name":name,
                "price":round(close,2),
                "change":round((close-prev)/prev*100,2),
                "volume":int(df["Volume"].iloc[-1])
            })

        except Exception:
            pass

    return result

if __name__=="__main__":
    print(scan())
