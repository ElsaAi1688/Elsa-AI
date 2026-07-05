
import sys
import subprocess

MODES = {
    "health": "elsa_health.py",
    "core": "elsa_core.py",
    "morning": "elsa_manager_suite.py morning",
    "close": "elsa_manager_suite.py close",
    "alert": "elsa_manager_suite.py alert",
    "dca": "elsa_manager_suite.py dca",
    "journal": "elsa_journal_review.py",
    "workspace": "elsa_workspace.py",
    "dashboard": "elsa_dashboard_u1.py",
    "stockcard": "elsa_stock_cards_all.py",
}

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "morning"
    cmd = MODES.get(mode)

    if not cmd:
        print("可用模式：")
        for k in MODES:
            print("-", k)
        sys.exit()

    subprocess.run([sys.executable] + cmd.split(), check=True)
