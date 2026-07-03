class NewsEngine:

    POSITIVE = [
        "營收成長",
        "創新高",
        "買超",
        "調升",
        "合作",
        "AI",
        "突破",
        "利多"
    ]

    NEGATIVE = [
        "下修",
        "賣超",
        "虧損",
        "跌破",
        "利空",
        "衰退",
        "裁員",
        "訴訟"
    ]

    def analyze(self, headlines):

        score = 50
        reasons = []

        for title in headlines:

            for word in self.POSITIVE:

                if word in title:
                    score += 8
                    reasons.append(f"利多：{word}")

            for word in self.NEGATIVE:

                if word in title:
                    score -= 8
                    reasons.append(f"利空：{word}")

        score = max(0, min(score, 100))

        return {
            "news_score": score,
            "reasons": reasons
        }


if __name__ == "__main__":

    engine = NewsEngine()

    result = engine.analyze([
        "仁寶6月營收成長",
        "外資買超仁寶",
        "AI伺服器需求增加"
    ])

    print(result)
