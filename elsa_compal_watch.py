from portfolio.portfolio_center import PortfolioCenter
from trade.trade_manager import TradeManager
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()
tm = TradeManager()

h = next(x for x in portfolio["holdings"] if x["symbol"] == "2324.TW")
t = tm.evaluate(h)

need_alert = t["priority"] >= 8

if need_alert:
    msg = f"""🚨 Elsa 仁寶盯盤提醒

莎莎，仁寶需要注意。

目前狀態：{t['state']}
建議：{t['advice']}
現價：{h['price']}
成本：{h['cost']}
損益：{t['profit_pct']}%

下一步：
{t['next_action']}

停損：{t['exit_plan']['stop_loss']}
第一目標：{t['exit_plan']['target1']}
第二目標：{t['exit_plan']['target2']}
"""
    print(msg)
    send_line_message(msg)
else:
    print("仁寶目前未達下車提醒條件")
