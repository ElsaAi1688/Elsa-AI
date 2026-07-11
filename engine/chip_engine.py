import requests
import pandas as pd
from datetime import datetime, timedelta


class ChipEngine:

    def _current_streak(self, values, positive=True):
        streak = 0

        for value in reversed(values):
            matched = value > 0 if positive else value < 0

            if matched:
                streak += 1
            else:
                break

        return streak

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
            df["buy"] = pd.to_numeric(
                df["buy"], errors="coerce"
            ).fillna(0)
            df["sell"] = pd.to_numeric(
                df["sell"], errors="coerce"
            ).fillna(0)
            df["net"] = df["buy"] - df["sell"]

            latest_dates = sorted(
                df["date"].dropna().unique()
            )[-trading_days:]

            recent = df[df["date"].isin(latest_dates)].copy()

            period = (
                f"{pd.Timestamp(latest_dates[0]).strftime('%Y-%m-%d')}"
                f"～{pd.Timestamp(latest_dates[-1]).strftime('%Y-%m-%d')}"
            )

            # 外資
            foreign = (
                recent[recent["name"] == "Foreign_Investor"]
                .groupby("date", as_index=False)["net"]
                .sum()
                .sort_values("date")
            )

            foreign_values = foreign["net"].tolist()
            foreign_total = int(round(sum(foreign_values)))
            foreign_lots = foreign_total / 1000
            foreign_latest = int(round(foreign_values[-1]))
            foreign_sell_streak = self._current_streak(
                foreign_values,
                positive=False,
            )

            foreign_points = 0

            if foreign_total > 0:
                foreign_points += 10
                foreign_status = "5日買超"
            elif foreign_total < 0:
                foreign_points -= 10
                foreign_status = "5日賣超"
            else:
                foreign_status = "5日中性"

            if foreign_sell_streak >= 3:
                foreign_points -= 15
                foreign_status = "連續賣超"
            elif foreign_sell_streak == 2:
                foreign_points -= 8
                foreign_status = "連2日賣超"

            score += foreign_points

            latest_foreign_text = (
                f"最新一日買超 {foreign_latest / 1000:,.1f} 張"
                if foreign_latest > 0
                else f"最新一日賣超 {abs(foreign_latest) / 1000:,.1f} 張"
            )

            explain.append({
                "name": "外資",
                "status": foreign_status,
                "points": foreign_points,
                "reason": (
                    f"最近 {trading_days} 日合計"
                    f"{'買超' if foreign_total >= 0 else '賣超'} "
                    f"{abs(foreign_lots):,.1f} 張；"
                    f"{latest_foreign_text}；"
                    f"目前連續賣超 {foreign_sell_streak} 日"
                ),
            })

            # 投信
            trust = (
                recent[recent["name"] == "Investment_Trust"]
                .groupby("date", as_index=False)["net"]
                .sum()
                .sort_values("date")
            )

            trust_values = trust["net"].tolist()
            trust_total = int(round(sum(trust_values)))
            trust_lots = trust_total / 1000
            trust_latest = int(round(trust_values[-1]))
            trust_buy_streak = self._current_streak(
                trust_values,
                positive=True,
            )

            if trust_buy_streak >= 3:
                trust_points = 15
                trust_status = f"連{trust_buy_streak}日買超"
            elif trust_latest > 0:
                trust_points = 5
                trust_status = "最新一日買超"
            elif trust_latest < 0:
                trust_points = -5
                trust_status = "最新一日賣超"
            else:
                trust_points = 0
                trust_status = "中性"

            score += trust_points

            latest_trust_text = (
                f"最新一日買超 {trust_latest / 1000:,.1f} 張"
                if trust_latest > 0
                else f"最新一日賣超 {abs(trust_latest) / 1000:,.1f} 張"
            )

            explain.append({
                "name": "投信",
                "status": trust_status,
                "points": trust_points,
                "reason": (
                    f"最近 {trading_days} 日合計"
                    f"{'買超' if trust_total >= 0 else '賣超'} "
                    f"{abs(trust_lots):,.1f} 張；"
                    f"{latest_trust_text}；"
                    f"目前連續買超 {trust_buy_streak} 日"
                ),
            })

            # 自營商：自行買賣 + 避險合併
            dealer_names = [
                "Dealer_self",
                "Dealer_Hedging",
            ]

            dealer = (
                recent[recent["name"].isin(dealer_names)]
                .groupby("date", as_index=False)["net"]
                .sum()
                .sort_values("date")
            )

            dealer_values = dealer["net"].tolist()
            dealer_total = int(round(sum(dealer_values)))
            dealer_lots = dealer_total / 1000
            dealer_latest = int(round(dealer_values[-1]))

            if dealer_total > 0:
                dealer_points = 8
                dealer_status = "5日買超"
            elif dealer_total < 0:
                dealer_points = -8
                dealer_status = "5日賣超"
            else:
                dealer_points = 0
                dealer_status = "中性"

            score += dealer_points

            latest_dealer_text = (
                f"最新一日買超 {dealer_latest / 1000:,.1f} 張"
                if dealer_latest > 0
                else f"最新一日賣超 {abs(dealer_latest) / 1000:,.1f} 張"
            )

            explain.append({
                "name": "自營商",
                "status": dealer_status,
                "points": dealer_points,
                "reason": (
                    f"自行買賣與避險合計，最近 {trading_days} 日"
                    f"{'買超' if dealer_total >= 0 else '賣超'} "
                    f"{abs(dealer_lots):,.1f} 張；"
                    f"{latest_dealer_text}"
                ),
            })

            return {
                "score": max(0, min(round(score), 100)),
                "period": period,
                "trading_days": trading_days,
                "foreign_sell_streak": foreign_sell_streak,
                "trust_buy_streak": trust_buy_streak,
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
