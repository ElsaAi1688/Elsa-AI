from pathlib import Path
import shutil

archive = Path("archive/old_dashboard")
archive.mkdir(parents=True, exist_ok=True)

old_files = [
    "reports/dashboard_renderer_old.py",
    "reports/ideal_dashboard_old.py",
    "reports/generate_dashboard_old.py",
    "reports/build_dashboard_old.py",
    "reports/dashboard.png",
    "reports/dashboard_v2.py",
]

for f in old_files:
    p = Path(f)
    if p.exists():
        shutil.move(str(p), archive / p.name)

Path("elsa_build001.py").write_text('''
from elsa_sprint2 import run

if __name__ == "__main__":
    print("🚀 Elsa AI v1.0 Build 001")
    run()
''', encoding="utf-8")

print("✅ Build 001 安裝完成")
print("✅ 舊 Dashboard 已整理到 archive/old_dashboard")
print("✅ 新入口：python elsa_build001.py")
