
import json
from pathlib import Path
from datetime import datetime

JOURNAL = Path("data/journal/decision_journal.json")
JOURNAL.parent.mkdir(parents=True, exist_ok=True)

class DecisionJournal:

    def load(self):
        if not JOURNAL.exists():
            return []
        return json.loads(JOURNAL.read_text(encoding="utf-8"))

    def save(self, records):
        JOURNAL.write_text(
            json.dumps(records, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def record(self, decision):
        records = self.load()

        item = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": decision["symbol"],
            "name": decision["name"],
            "ai_score": decision["score"],
            "breakout": decision["breakout"],
            "price": decision["price"],
            "support": decision["support"],
            "resistance": decision["resistance"],
            "level": decision["level"],
            "action": decision["action"],
            "reasons": decision["reasons"]
        }

        records.append(item)
        self.save(records)

        return item
