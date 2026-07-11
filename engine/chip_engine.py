import requests
import pandas as pd
from datetime import datetime, timedelta


class ChipEngine:

    LABELS = {
        "Foreign_Investor": "外資",
        "Investment_Trust": "投信",
        "Dealer": "自營商",
    }

    POINTS = {
        "外資": 10,
        "投信": 15,
        "自營商": 8,
    }

    def analyze(self, stock_id, trading_days=5):
        score = 50
        explain = []

        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d")

        try:
            response = requests.get(
                "https://api.finmindtrade.com/api/v4/data",
                params={
                    "dataset": "TaiwanStockInstitutionalInvestorsBuySell",
                    "data_id": stock_id,
                    "start_date": start,
                    "end_date": end,
                },
                timeout=20,
            )
            response.raise_for_status()

            rows = response.json().get("data", [])
            if not rows:
                return {
                    "score": 50,
                    "period": "資料不足",
                    "explain": [{
                        "name": "法人",
                        "status": "資料不足",
                        "points": 0,
                        "reason": "暫無法人買賣超資料",
                    }],
                }

            df = pd.DataFrame(rows)
            df["date"] = pd.to_datetime(df["date"])
            df["net"] = (
                pd.to_numeric(df["buy"], errors="coerce").fillna(0)
                - pd.to_numeric(df["sell"], errors="coerce").fillna(0)
            )

            latest_dates = sorted(df["date"].dropna().unique())[-trading_days:]
            recent = df[df["date"].isin(latest_dates)]

            period = (
                f"{pd.Timestamp(latest_dates[0]).strftime('%Y-%m-%d')}"
                f"～{pd.Timestamp(latest_dates[-1]).strftime('%Y-%m-%d')}"
            )

            for raw_name, label in self.LABELS.items():
                sub = recent[recent["name"] == raw_name]
                if sub.empty:
                    explain.append({
                        "name": label,
                        "status": "無資料",
                        "points": 0,
                        "reason": f"最近 {trading_days} 個交易日無資料",
                    })
                    continue

                net_shares = int(round(sub["net"].sum()))
                net_lots = round(net_shares / 1000, 1)
                base_points = self.POINTS[label]

                if net_shares > 0:
                    points = base_points
                    status = "買超"
                    reason = (
                        f"最近 {trading_days} 個交易日合計買超 "
                        f"{net_lots:,.1f} 張（{net_shares:,} 股）"
                    )
                elif net_shares < 0:
                    points = -base_points
                    status = "賣超"
                    reason = (
                        f"最近 {trading_days} 個交易日合計賣超 "
                        f"{abs(net_lots):,.1f} 張（{abs(net_shares):,} 股）"
                    )
                else:
                    points = 0
                    status = "中性"
                    reason = f"最近 {trading_days} 個交易日買賣超接近平衡"

                score += points
                explain.append({
                    "name": label,
                    "status": status,
                    "points": points,
                    "reason": reason,
                })

            return {
                "score": max(0, min(round(score), 100)),
                "period": period,
                "trading_days": trading_days,
                "explain": explain,
            }

        except Exception as exc:
            return {
                "score": 50,
                "period": "錯誤",
                "explain": [{
                    "name": "法人",
                    "status": "錯誤",
                    "points": 0,
                    "reason": str(exc),
                }],
            }
