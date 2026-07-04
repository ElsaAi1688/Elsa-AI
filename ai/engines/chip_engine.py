import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from data_provider import DataProvider


class ChipEngine:

    def analyze_from_data(self, df):

        if df is None or df.empty:
            return {
                "chip_score": 50,
                "avg_volume": 0,
                "last_volume": 0,
                "volume_ratio": 0,
                "price_change_5d": 0,
                "reasons": ["籌碼資料不足，暫以中性評估"]
            }

        if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)

        df = df.dropna(subset=["Close", "Volume"])

        close = df["Close"]
        volume = df["Volume"]

        last_volume = float(volume.iloc[-1])
        avg_volume_5 = float(volume.tail(5).mean())
        avg_volume_20 = float(volume.tail(20).mean())

        volume_ratio = round(last_volume / avg_volume_20, 2) if avg_volume_20 else 0

        price_change_5d = round(
            (float(close.iloc[-1]) - float(close.iloc[-5])) / float(close.iloc[-5]) * 100,
            2
        )

        score = 50
        reasons = []

        if volume_ratio >= 2:
            score += 20
            reasons.append("成交量明顯放大，市場關注度提高")
        elif volume_ratio >= 1.3:
            score += 12
            reasons.append("成交量高於近期平均")
        elif volume_ratio < 0.7:
            score -= 5
            reasons.append("成交量偏低，追價動能不足")

        if price_change_5d >= 5:
            score += 18
            reasons.append("近 5 日股價轉強")
        elif price_change_5d >= 2:
            score += 10
            reasons.append("近 5 日短線偏多")
        elif price_change_5d <= -5:
            score -= 15
            reasons.append("近 5 日股價明顯轉弱")
        elif price_change_5d <= -2:
            score -= 8
            reasons.append("近 5 日短線偏弱")

        if last_volume > avg_volume_5 and price_change_5d > 0:
            score += 8
            reasons.append("量價同步偏多")

        if last_volume > avg_volume_5 and price_change_5d < 0:
            score -= 10
            reasons.append("放量下跌，需留意賣壓")

        score = max(0, min(100, round(score)))

        return {
            "chip_score": score,
            "avg_volume": int(avg_volume_20),
            "last_volume": int(last_volume),
            "volume_ratio": volume_ratio,
            "price_change_5d": price_change_5d,
            "reasons": reasons[:6]
        }

    def analyze(self, symbol):

        df = DataProvider().get_history(symbol)

        return self.analyze_from_data(df)


if __name__ == "__main__":
    print(ChipEngine().analyze("2324.TW"))
