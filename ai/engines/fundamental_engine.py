import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import yfinance as yf


class FundamentalEngine:

    def analyze(self, symbol):

        info = yf.Ticker(symbol).info

        score = 50
        reasons = []

        pe = info.get("trailingPE")
        forward_pe = info.get("forwardPE")
        roe = info.get("returnOnEquity")
        roa = info.get("returnOnAssets")
        gross_margin = info.get("grossMargins")
        operating_margin = info.get("operatingMargins")
        dividend_yield = info.get("dividendYield")
        eps = info.get("trailingEps")

        if pe:
            if pe < 12:
                score += 15
                reasons.append("本益比偏低，評價相對便宜")
            elif pe < 25:
                score += 8
                reasons.append("本益比合理")
            elif pe > 35:
                score -= 8
                reasons.append("本益比偏高，估值需保守")

        if roe:
            roe_pct = roe * 100
            if roe_pct >= 20:
                score += 18
                reasons.append("ROE 優秀，獲利能力強")
            elif roe_pct >= 10:
                score += 10
                reasons.append("ROE 良好")
            elif roe_pct < 5:
                score -= 8
                reasons.append("ROE 偏低，獲利能力較弱")
        else:
            roe_pct = None

        if roa:
            roa_pct = roa * 100
            if roa_pct >= 8:
                score += 8
                reasons.append("ROA 表現良好")
        else:
            roa_pct = None

        if gross_margin:
            gm_pct = gross_margin * 100
            if gm_pct >= 30:
                score += 8
                reasons.append("毛利率良好")
        else:
            gm_pct = None

        if operating_margin:
            om_pct = operating_margin * 100
            if om_pct >= 10:
                score += 8
                reasons.append("營益率良好")
        else:
            om_pct = None

        if dividend_yield:
            dy_pct = dividend_yield * 100
            if dy_pct >= 5:
                score += 10
                reasons.append("殖利率佳")
            elif dy_pct >= 3:
                score += 5
                reasons.append("具備穩定配息條件")
        else:
            dy_pct = None

        if eps:
            if eps > 0:
                score += 6
                reasons.append("EPS 為正，具備獲利能力")
            else:
                score -= 12
                reasons.append("EPS 為負，獲利需留意")

        score = max(0, min(100, round(score)))

        return {
            "fundamental_score": score,
            "pe": pe,
            "forward_pe": forward_pe,
            "roe": round(roe_pct, 2) if roe_pct is not None else None,
            "roa": round(roa_pct, 2) if roa_pct is not None else None,
            "gross_margin": round(gm_pct, 2) if gm_pct is not None else None,
            "operating_margin": round(om_pct, 2) if om_pct is not None else None,
            "dividend_yield": round(dy_pct, 2) if dy_pct is not None else None,
            "eps": eps,
            "reasons": reasons[:8]
        }


if __name__ == "__main__":
    print(FundamentalEngine().analyze("2324.TW"))
