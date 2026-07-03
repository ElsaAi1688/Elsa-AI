from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import font_manager


def setup_chinese_font():
    font_paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]

    for font_path in font_paths:
        if Path(font_path).exists():
            font_manager.fontManager.addfont(font_path)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=font_path).get_name()
            break

    plt.rcParams["axes.unicode_minus"] = False


def create_price_chart(
    history,
    stock_no,
    stock_name,
    buy_price,
    take_profit,
    stop_loss,
    score=0,
    confidence=0,
    risk_level="未評估"
):
    setup_chinese_font()

    Path("charts").mkdir(exist_ok=True)

    data = history.tail(60).copy()
    data["MA5"] = data["Close"].rolling(5).mean()
    data["MA20"] = data["Close"].rolling(20).mean()

    file_path = Path("charts") / f"{stock_no}_price_chart.png"

    plt.figure(figsize=(13, 7))
    plt.plot(data.index, data["Close"], label="收盤價")
    plt.plot(data.index, data["MA5"], label="MA5")
    plt.plot(data.index, data["MA20"], label="MA20")

    plt.axhline(y=buy_price, linestyle="--", label=f"成本 {buy_price:.2f}")
    plt.axhline(y=take_profit, linestyle="--", label=f"停利 {take_profit:.2f}")
    plt.axhline(y=stop_loss, linestyle="--", label=f"停損 {stop_loss:.2f}")

    plt.title(f"{stock_no} {stock_name} 股價走勢圖")
    plt.xlabel("日期")
    plt.ylabel("股價")
    plt.legend()
    plt.grid(True)

    info_text = f"AI分數：{score}/100\n信心值：{confidence}/100\n風險等級：{risk_level}"
    plt.gcf().text(0.72, 0.20, info_text, fontsize=12, bbox=dict(boxstyle="round", alpha=0.15))

    plt.tight_layout()
    plt.savefig(file_path, dpi=150)
    plt.close()

    return file_path
