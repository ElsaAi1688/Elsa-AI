import sys
import subprocess

MODES = {
    "health": "elsa_health.py",
    "core": "elsa_core.py",
    "morning": "elsa_morning_core.py",
    "close": "elsa_close_core.py",
    "dashboard": "elsa_dashboard_core.py",
    "alert": "elsa_alert_core.py",
    "portfolio": "elsa_rc1a.py",
    "health": "elsa_rc1b.py",
    "teacher": "elsa_rc1f.py",
    "manager": "elsa_build010.py",
    "dca": "elsa_rc1d.py",
}

def run(mode):
    script = MODES.get(mode)

    if not script:
        print("可用模式：")
        for k in MODES:
            print("-", k)
        return

    subprocess.run([sys.executable, script], check=True)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "morning"
    run(mode)
