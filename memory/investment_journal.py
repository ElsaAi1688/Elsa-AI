import json
from pathlib import Path
from datetime import datetime

JOURNAL = Path("memory/investment_journal.json")
JOURNAL.parent.mkdir(exist_ok=True)

class InvestmentJournal:

    def load(self):
        if not JOURNAL.exists():
            return []
        return json.loads(JOURNAL.read_text(encoding="utf-8"))

    def save(self, records):
        JOURNAL.write_text(
            json.dumps(records, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def record_daily(self, workspace_data):
        records = self.load()

        item = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "main_decision": workspace_data["decision"]["main_message"],
            "portfolio_health": workspace_data["health"]["score"],
            "portfolio_level": workspace_data["health"]["level"],
            "holdings": workspace_data["decision"]["decisions"],
            "top5": workspace_data["market"]["top10"][:5],
            "lesson": workspace_data["lesson"]["title"]
        }

        records.append(item)
        self.save(records)
        return item
