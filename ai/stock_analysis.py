from dataclasses import dataclass, field
from typing import List


@dataclass
class StockAnalysis:

    symbol: str
    name: str

    price: float = 0.0

    technical_score: int = 0
    fundamental_score: int = 0
    chip_score: int = 0
    news_score: int = 0
    market_score: int = 0

    ai_score: int = 0

    confidence: int = 0

    recommendation: str = "觀察"

    next_action: str = ""

    breakout_probability: int = 0

    support: float = 0.0

    resistance: float = 0.0

    target_price: float = 0.0

    stop_loss: float = 0.0

    risk: str = ""

    reasons: List[str] = field(default_factory=list)

    learning_topic: str = ""

    learning_content: str = ""

    tags: List[str] = field(default_factory=list)

    def calculate_score(self):

        self.ai_score = round(

            self.technical_score*0.30 +

            self.fundamental_score*0.25 +

            self.chip_score*0.20 +

            self.news_score*0.15 +

            self.market_score*0.10

        )

        return self.ai_score
