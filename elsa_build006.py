from scanner.market_cache import load_market_scan, save_market_scan
import subprocess, sys

cache = load_market_scan()

if cache is None:
    save_market_scan(limit=200)

subprocess.run([sys.executable, "reports/dashboard_cache_renderer.py"], check=True)
