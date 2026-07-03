from datetime import datetime
from services.portfolio_service import load_portfolio
from services.line_service import send_line_message

today = datetime.now()
current_day = today.day

portfolio = load_portfolio()
holdings = portfolio.get("holdings", [])

lines = []
lines.append("📅 Elsa AI 定期定額提醒")
lines.append("=" * 30)

has_reminder = False

for stock in holdings:
    if stock.get("strategy") != "dca":
        continue

    dca_day = stock.get("dca_day")
    dca_amount = stock.get("dca_amount")
    remind_days = stock.get("remind_days_before", [])

    days_left = dca_day - current_day

    if days_left in remind_days:
        has_reminder = True

        lines.append("")
        lines.append(f"📈 {stock['symbol']} {stock['name']}")
        lines.append(f"扣款日：每月 {dca_day} 號")
        lines.append(f"預計扣款：{dca_amount} 元")

        if days_left > 1:
            lines.append(f"提醒：距離扣款還有 {days_left} 天")
            lines.append("請確認交割戶資金是否足夠。")
        elif days_left == 1:
            lines.append("提醒：明天就是扣款日")
            lines.append("今天是最後確認資金與修改金額的時間。")
        elif days_left == 0:
            lines.append("提醒：今天是扣款日")
            lines.append("請確認扣款是否成功。")

if has_reminder:
    report = "\n".join(lines)
    print(report)
    send_line_message(report)
else:
    print("今天沒有定期定額提醒")
