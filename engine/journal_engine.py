import json
from pathlib import Path
from datetime import datetime

class JournalEngine:

    FILE = Path("data/journal.json")

    def __init__(self):
        self.FILE.parent.mkdir(exist_ok=True)

        if not self.FILE.exists():
            self.FILE.write_text(
                "[]",
                encoding="utf-8"
            )

    def save(self, record):

        data = json.loads(
            self.FILE.read_text(encoding="utf-8")
        )

        record["created_at"] = datetime.now().isoformat()

        data.append(record)

        self.FILE.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def latest(self, n=10):

        data = json.loads(
            self.FILE.read_text(
                encoding="utf-8"
            )
        )

        return data[-n:]
