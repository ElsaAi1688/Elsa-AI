
class WorkspaceMessage:

    def render(self, data):
        p = data["portfolio"]
        h = data["health"]
        d = data["decision"]
        m = data["market"]
        lesson = data["lesson"]

        lines = []
        lines.append("👩‍💼 Elsa Workspace v1.0")
        lines.append("莎莎，我已經幫妳整理好今天的投資工作台。")
        lines.append("=" * 30)

        lines.append("🧠 今日總決策")
        lines.append(d["main_message"])
        lines.append("")

        lines.append("💼 我的投資中心")
        lines.append(f"投入成本：{p['total_cost']}")
        lines.append(f"目前市值：{p['total_value']}")
        lines.append(f"未實現損益：{p['total_pnl']}（{p['total_pnl_pct']}%）")
        lines.append(f"健康度：{h['score']}/100｜{h['level']} {h['stars']}")
        lines.append("")

        lines.append("📈 我的持股決策")
        for x in d["decisions"]:
            lines.append(f"{x['name']}｜{x['action']}｜信心 {x['confidence']}%")
            lines.append(f"原因：{x['decision']}")
        lines.append("")

        lines.append("🔥 今日市場機會")
        for i, s in enumerate(m["top10"][:5], 1):
            lines.append(f"{i}. {s['name']} AI {s['ai_score']}｜突破率 {s['breakout_probability']}%")
        lines.append("")

        lines.append("📚 今日老師")
        lines.append(f"主題：{lesson['title']}")
        for c in lesson["content"][:3]:
            lines.append(f"・{c}")

        lines.append("")
        lines.append("📌 Elsa 今日一句話")
        lines.append("今天先照紀律走，不追高，等待高勝率機會。")

        return "\n".join(lines)
