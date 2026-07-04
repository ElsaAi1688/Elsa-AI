import sys
import subprocess

MODES = {
    "morning": "elsa_morning_v2_clean.py",
    "close": "elsa_close_v2.py",
    "dashboard": "elsa_rc1e.py",
    "portfolio": "elsa_rc1a.py",
    "health": "elsa_rc1b.py",
    "teacher": "elsa_rc1f.py",
    "alert": "elsa_build009.py",
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
