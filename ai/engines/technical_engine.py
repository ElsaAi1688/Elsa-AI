import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from data_provider import DataProvider


class TechnicalEngine:

    def analyze_from_data(self, df):

        if df is None or df.empty:
            return None

        df = df.copy()

        if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)

        df = df.dropna(subset=["Close"])

        close = df["Close"]
        high = df["High"]
        low = df["Low"]
        volume = df["Volume"]

        df["MA5"] = close.rolling(5).mean()
        df["MA10"] = close.rolling(10).mean()
        df["MA20"] = close.rolling(20).mean()
        df["MA60"] = close.rolling(60).mean()
        df["MA120"] = close.rolling(120).mean()

        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        df["RSI"] = 100 - (100 / (1 + gain / loss))

        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        df["MACD"] = ema12 - ema26
        df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()

        low9 = low.rolling(9).min()
        high9 = high.rolling(9).max()
        rsv = (close - low9) / (high9 - low9) * 100
        df["K"] = rsv.ewm(com=2).mean()
        df["D"] = df["K"].ewm(com=2).mean()

        df["BB_MID"] = close.rolling(20).mean()
        df["BB_STD"] = close.rolling(20).std()
        df["BB_UPPER"] = df["BB_MID"] + df["BB_STD"] * 2
        df["BB_LOWER"] = df["BB_MID"] - df["BB_STD"] * 2

        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()
        df["ATR"] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1).rolling(14).mean()

        latest = df.iloc[-1]

        price = float(latest["Close"])
        ma5 = float(latest["MA5"])
        ma10 = float(latest["MA10"])
        ma20 = float(latest["MA20"])
        ma60 = float(latest["MA60"])
        rsi = float(latest["RSI"])
        macd = float(latest["MACD"])
        macd_signal = float(latest["MACD_SIGNAL"])
        k = float(latest["K"])
        d = float(latest["D"])

        support = round(float(close.tail(20).min()), 2)
        resistance = round(float(close.tail(20).max()), 2)

        avg_volume = float(volume.tail(20).mean())
        last_volume = float(volume.iloc[-1])
        volume_ratio = round(last_volume / avg_volume, 2) if avg_volume else 0

        score = 50
        reasons = []

        if price > ma5:
            score += 5
            reasons.append("股價站上 MA5，短線轉強")

        if price > ma20:
            score += 10
            reasons.append("股價站上 MA20，中期趨勢偏多")
        else:
            score -= 8
            reasons.append("股價仍在 MA20 下方，短線偏保守")

        if price > ma60:
            score += 12
            reasons.append("股價站上 MA60，季線支撐偏強")

        if ma5 > ma20:
            score += 8
            reasons.append("MA5 上穿 MA20，短線均線轉強")

        if macd > macd_signal:
            score += 8
            reasons.append("MACD 偏多")
        else:
            score -= 5
            reasons.append("MACD 尚未轉強")

        if 45 <= rsi <= 65:
            score += 8
            reasons.append("RSI 位於健康區間")
        elif rsi > 70:
            score -= 8
            reasons.append("RSI 過熱，短線需留意拉回")
        elif rsi < 35:
            score -= 5
            reasons.append("RSI 偏弱，買盤尚未明顯")

        if k > d:
            score += 6
            reasons.append("KD 指標偏多")
        else:
            score -= 3
            reasons.append("KD 指標偏弱")

        if volume_ratio > 1.5:
            score += 10
            reasons.append("成交量明顯放大")
        elif volume_ratio > 1.1:
            score += 5
            reasons.append("成交量高於平均")

        breakout_probability = min(95, max(10, int(score * 0.75 + volume_ratio * 10)))

        if price >= resistance * 0.98:
            reasons.append("股價接近壓力區，觀察是否帶量突破")

        if price <= support * 1.02:
            reasons.append("股價接近支撐區，注意是否跌破")

        score = max(0, min(100, round(score)))

        return {
            "price": round(price, 2),
            "technical_score": score,
            "ma5": round(ma5, 2),
            "ma10": round(ma10, 2),
            "ma20": round(ma20, 2),
            "ma60": round(ma60, 2),
            "rsi": round(rsi, 1),
            "macd": round(macd, 2),
            "macd_signal": round(macd_signal, 2),
            "k": round(k, 1),
            "d": round(d, 1),
            "support": support,
            "resistance": resistance,
            "volume_ratio": volume_ratio,
            "breakout_probability": breakout_probability,
            "target_price": round(resistance * 1.03, 2),
            "stop_loss": round(support * 0.98, 2),
            "reasons": reasons[:8]
        }

    def analyze(self, symbol):
        df = DataProvider().get_history(symbol)
        return self.analyze_from_data(df)


if __name__ == "__main__":
    result = TechnicalEngine().analyze("2324.TW")
    print(result)
