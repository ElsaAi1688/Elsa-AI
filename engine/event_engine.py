class EventEngine:

    def detect(self, previous, current):
        events = []

        previous = previous or {}

        old_score = previous.get("decision_score")
        new_score = int(current["decision_score"])

        old_action = previous.get("action")
        new_action = current["action"]

        old_macd_bullish = bool(previous.get("macd_bullish", False))
        new_macd_bullish = bool(current.get("macd_bullish", False))

        old_kd_golden = bool(previous.get("kd_golden", False))
        new_kd_golden = bool(current.get("kd_golden", False))

        old_breakout = bool(previous.get("breakout", False))
        new_breakout = bool(current.get("breakout", False))

        # 第一次啟動，傳一份初始狀態
        if old_score is None:
            events.append("INITIAL")
            return events

        # 評分向上跨越重要門檻
        if old_score < 68 <= new_score:
            events.append("SCORE_WATCH")

        if old_score < 80 <= new_score:
            events.append("SCORE_ENTRY")

        # 評分跌破門檻
        if old_score >= 80 > new_score:
            events.append("ENTRY_LOST")

        if old_score >= 68 > new_score:
            events.append("WATCH_LOST")

        # 決策文字改變
        if old_action and old_action != new_action:
            events.append("ACTION_CHANGED")

        # 技術事件首次出現
        if not old_macd_bullish and new_macd_bullish:
            events.append("MACD_BULLISH")

        if not old_kd_golden and new_kd_golden:
            events.append("KD_GOLDEN")

        if not old_breakout and new_breakout:
            events.append("PRICE_BREAKOUT")

        # 避免重複
        return list(dict.fromkeys(events))

    def describe(self, events):
        labels = {
            "INITIAL": "系統初始狀態",
            "SCORE_WATCH": "綜合評分突破 68，進入觀察區",
            "SCORE_ENTRY": "綜合評分突破 80，進入布局區",
            "ENTRY_LOST": "綜合評分跌破 80，布局訊號失效",
            "WATCH_LOST": "綜合評分跌破 68，轉回等待",
            "ACTION_CHANGED": "Elsa 決策發生改變",
            "MACD_BULLISH": "MACD 翻紅",
            "KD_GOLDEN": "KD 黃金交叉",
            "PRICE_BREAKOUT": "股價突破短線壓力",
        }

        return [labels[event] for event in events if event in labels]
