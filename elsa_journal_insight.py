import json
from pathlib import Path
from collections import Counter
from services.line_service import send_line_message

JOURNAL = Path("memory/investment_journal.json")

if not JOURNAL.exists():
    msg = "目前還沒有足夠投資日誌可以分析。"
else:
    records = json.loads(JOURNAL.read_text(encoding="utf-8"))
    recent = records[-10:]

    actions = []
    for r in recent:
        for h in r.get("holdings", []):
            actions.append(h.get("action", "未知"))

    counter = Counter(actions)

    lines = []
    lines.append("🧠 Elsa 投資習慣分析 v2-F")
    lines.append("=" * 30)
    lines.append(f"分析最近 {len(recent)} 次投資日誌")
    lines.append("")

    for action, count in counter.most_common():
        lines.append(f"{action}：{count} 次")

    lines.append("")
    lines.append("👩‍💼 Elsa 觀察")

    wait = counter.get("等待", 0)
    add = counter.get("加碼", 0)
    reduce = counter.get("減碼", 0)

    if reduce > 0:
        lines.append("最近有出現減碼訊號，接下來要優先控管風險。")
    elif wait >= add:
        lines.append("最近多數決策偏向等待，代表 Elsa 認為目前不用急著追高。")
    else:
        lines.append("最近加碼訊號增加，但仍要分批，不要一次投入過多。")

    lines.append("")
    lines.append("📌 今日提醒")
    lines.append("投資不是每天都要動作，能等待也是成熟的操作。")

    msg = "\n".join(lines)

print(msg)
send_line_message(msg)
