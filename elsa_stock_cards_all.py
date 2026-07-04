import subprocess
import sys

stocks = ["2330.TW", "0050.TW", "2324.TW"]

for symbol in stocks:
    subprocess.run([sys.executable, "reports/stock_card_u2.py", symbol], check=False)
