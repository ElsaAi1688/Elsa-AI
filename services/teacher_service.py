from datetime import datetime

LESSONS = [
    {
        "title": "什麼是 MA5？",
        "content": "MA5 是最近 5 個交易日的平均收盤價，用來觀察短線趨勢。若股價站上 MA5，通常代表短線轉強；若跌破 MA5，短線可能轉弱。"
    },
    {
        "title": "什麼是 MA20？",
        "content": "MA20 是最近 20 個交易日的平均收盤價，常被用來觀察月線趨勢。股價在 MA20 上方，代表波段較強；在 MA20 下方，代表上方可能有壓力。"
    },
    {
        "title": "什麼是 RSI？",
        "content": "RSI 是衡量股票近期買賣力道的指標。一般來說，RSI 低於 30 可能偏超賣，高於 70 可能偏過熱，30 到 70 之間屬於正常區間。"
    },
    {
        "title": "什麼是 MACD？",
        "content": "MACD 是用來觀察趨勢轉強或轉弱的指標。當 MACD 高於 Signal，通常代表多方訊號；低於 Signal，代表空方訊號。"
    },
    {
        "title": "什麼是支撐與壓力？",
        "content": "支撐是股價下跌時容易有人買進的區域；壓力是股價上漲時容易有人賣出的區域。妳的成本價也常會變成心理壓力或支撐。"
    }
]


def get_daily_lesson():
    day_index = datetime.now().day % len(LESSONS)
    lesson = LESSONS[day_index]

    return f"""📘 Elsa AI 每日一課

主題：{lesson['title']}

{lesson['content']}

今天請試著把這個觀念套用到妳的持股上。
"""
