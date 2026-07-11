class ExplainEngine:

    def summarize(self, technical, fundamental, chip):

        plus = []
        minus = []

        for section in (
            technical["explain"],
            fundamental["explain"],
            chip["explain"],
        ):
            for item in section:
                if item["points"] > 0:
                    plus.append(item)
                elif item["points"] < 0:
                    minus.append(item)

        plus.sort(
            key=lambda x: x["points"],
            reverse=True,
        )

        minus.sort(
            key=lambda x: x["points"],
        )

        summary = []

        if plus:
            best = plus[0]
            summary.append(
                f"🔥 最大加分：{best['name']}（+{best['points']}）"
            )
            summary.append(best["reason"])

        if minus:
            worst = minus[0]
            summary.append(
                f"⚠ 最大扣分：{worst['name']}（{worst['points']}）"
            )
            summary.append(worst["reason"])

        return summary
