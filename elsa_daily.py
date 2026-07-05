import subprocess
import sys

steps = [
    ("health", "健康檢查"),
    ("core", "更新中央大腦"),
    ("workspace", "推播 Workspace"),
    ("journal", "記錄投資日誌"),
    ("insight", "投資習慣分析"),
]

for mode, title in steps:
    print(f"🚀 執行：{title}")
    subprocess.run([sys.executable, "elsa.py", mode], check=True)

print("✅ Elsa Daily 全流程完成")
