import subprocess
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

print("=" * 50)
print("🤖 Elsa AI 一鍵執行系統 v1.5")
print(f"日期：{today}")
print("=" * 50)

steps = [
    ("📊 產生多股票經理人報告", "python multi_report.py"),
    ("📅 檢查定期定額提醒", "python dca_reminder.py"),
    ("🖼️ 產生所有股票分析卡", "python portfolio_image_report.py"),
    ("📊 產生 Dashboard 圖", "python manager_dashboard.py")
]

for title, command in steps:
    print()
    print(title)
    print("-" * 50)

    result = subprocess.run(command, shell=True)

    if result.returncode == 0:
        print(f"✅ 完成：{title}")
    else:
        print(f"❌ 失敗：{title}")
        break

print()
print("=" * 50)
print("✅ Elsa AI 今日任務完成")
print("=" * 50)
