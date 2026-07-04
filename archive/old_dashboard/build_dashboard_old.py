import shutil
from pathlib import Path

template = Path("reports/templates/base.png")
output = Path("reports/output/dashboard.png")

output.parent.mkdir(parents=True, exist_ok=True)

shutil.copy(template, output)

print("✅ Dashboard 建立完成：", output)
