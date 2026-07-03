from datetime import datetime
from pathlib import Path

from services.portfolio_service import get_all_stocks
from services.portfolio_analyzer import analyze_stock
from services.line_service import send_line_message
from services.teacher_service import get_daily_lesson
from services.decision_log_service import save_decision
from services.manager_service import get_manager_suggestion

today = datetime.now().strftime("%Y-%m-%d")

stocks = get_all_stocks()
results = []

for stock in stocks:
    print(f"分析中：{stock['symbol']} {stock['name']} ...")
    results.append(analyze_stock(stock))

valid_results = [r for r in results if "error" not in r]
valid_results.sort(key=lambda x: x["score"], reverse=True)

short_holdings = []
dca_holdings = []
watchlist = []

for r in valid_results:
    strategy = r.get("type", "")

    if strategy == "short":
        short_holdings.append(r)
    elif strategy == "dca":
        dca_holdings.append(r)
    else:
        watchlist.append(r)


def get_suggestion(r):
    score = r["score"]
    strategy = r.get("type", "")

    if strategy == "short":
        if score >= 75:
            return "✅ 短線偏強：續抱或觀察加碼"
        elif score >= 55:
            return "🟡 短線觀察：等待更明確訊號"
        else:
            return "🔴 短線偏弱：注意停損風險"

    if strategy == "dca":
        if score >= 75:
            return "🌱 長期定投：可維持或小額加碼"
        elif score >= 55:
            return "🌱 長期定投：照原計畫扣款"
        else:
            return "⚠️ 長期定投：暫不追高，等回檔或照原計畫"

    if score >= 75:
        return "👀 觀察清單：值得關注"
    elif score >= 55:
        return "👀 觀察清單：普通觀察"
    else:
        return "👀 觀察清單：暫時偏弱"


def add_section(lines, title, items):
    lines.append("")
    lines.append(title)
    lines.append("=" * 30)

    if not items:
        lines.append("目前沒有資料")
        return

    for r in items:
        lines.append("")
        lines.append(f"📈 {r['symbol']} {r['name']}")
        lines.append(f"現價：{r['close']:.2f}")
        lines.append(f"AI 分數：{r['score']}/100")
        lines.append(f"信心值：{r.get('confidence', 0)}/100")
        lines.append(f"風險等級：{r.get('risk_level', '未評估')}")

        if r["buy_price"] > 0 and r["shares"] > 0:
            lines.append(f"成本：{r['buy_price']:.2f}")
            lines.append(f"持股：{r['shares']} 股")
            lines.append(f"損益：{r['profit']:.2f} 元")
            lines.append(f"報酬率：{r['percent']:.2f}%")

        manager = get_manager_suggestion(r)
        suggestion = manager['action']
        lines.append(suggestion)
        lines.append(f"信心值：{manager['confidence']}/100")
        lines.append(f"風險等級：{manager['risk_level']}")
        lines.append(f"上漲機率：{manager['upside_probability']}%")
        lines.append(f"下跌風險：{manager['downside_probability']}%")
        lines.append(f"預估持有：{manager['hold_days']}")
        save_decision(r, suggestion)
        lines.append("原因：")
        for msg in r["messages"]:
            lines.append(msg)


lines = []
lines.append("🤖 Elsa AI 多股票經理人報告 v2.3")
lines.append(f"日期：{today}")
lines.append("=" * 30)

add_section(lines, "📦 短線持股", short_holdings)
add_section(lines, "🌱 長期定期定額", dca_holdings)
add_section(lines, "👀 觀察清單", watchlist)

if valid_results:
    best = valid_results[0]
    lines.append("")
    lines.append("🏆 今日最高分")
    lines.append("=" * 30)
    lines.append(f"{best['symbol']} {best['name']}")
    lines.append(f"AI 分數：{best['score']}/100")
    lines.append(get_suggestion(best))

lines.append("")
lines.append("📘 今日學習")
lines.append("=" * 30)
lines.append(get_daily_lesson())

report = "\n".join(lines)

print(report)

Path("reports").mkdir(exist_ok=True)
file_path = Path("reports") / f"manager_report_{today}.txt"
file_path.write_text(report, encoding="utf-8")

print(f"✅ 經理人報告已儲存：{file_path}")

send_line_message(report)
