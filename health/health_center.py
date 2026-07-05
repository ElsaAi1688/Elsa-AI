from datetime import datetime
from pathlib import Path
from services.line_service import send_line_message
from core.elsa_brain import ElsaBrain

LOG = Path("logs/elsa_health.log")
LOG.parent.mkdir(exist_ok=True)

class HealthCenter:
    def log(self, text):
        line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {text}"
        print(line)
        LOG.write_text((LOG.read_text(encoding="utf-8") if LOG.exists() else "") + line + "\n", encoding="utf-8")

    def check(self):
        ok = True
        results = []

        try:
            brain = ElsaBrain().load()
            if brain is None:
                brain = ElsaBrain().update(limit=50)
            results.append("✅ Core Brain 正常")
        except Exception as e:
            ok = False
            results.append(f"❌ Core Brain 異常：{e}")

        try:
            send_line_message("❤️ Elsa Health Check\n系統測試推播成功")
            results.append("✅ LINE 正常")
        except Exception as e:
            ok = False
            results.append(f"❌ LINE 異常：{e}")

        msg = "❤️ Elsa Health Center\n" + "\n".join(results)
        self.log(msg)
        return ok, msg
