import yfinance as yf

class DataProvider:

    def get_history(self, symbol, period="6mo"):

        df = yf.download(
            symbol,
            period=period,
            progress=False,
            auto_adjust=True
        )

        if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)

        return df

    def get_info(self, symbol):
        return yf.Ticker(symbol).info


if __name__=="__main__":
    dp=DataProvider()
    df=dp.get_history("2324.TW")
    print(df.tail())
