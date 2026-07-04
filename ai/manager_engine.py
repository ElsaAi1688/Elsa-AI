
class ManagerEngine:
    def advice(self, stock):
        lines = []
        lines.append(f"📈 {stock.name}（{stock.symbol}）")
        lines.append(f"AI總分：{stock.ai_score}/100")
        lines.append(f"建議：{stock.recommendation}")
        lines.append(f"現價：{stock.price}")
        lines.append(f"支撐：{stock.support}")
        lines.append(f"壓力：{stock.resistance}")
        lines.append(f"停損：{stock.stop_loss}")
        lines.append(f"目標價：{stock.target_price}")
        lines.append(f"突破率：{stock.breakout_probability}%")
        lines.append("理由：")
        for r in stock.reasons[:6]:
            lines.append(f"✔ {r}")
        return "\n".join(lines)
