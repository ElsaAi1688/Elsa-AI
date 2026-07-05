from pathlib import Path

p=Path("scanner/market_brain.py")
txt=p.read_text(encoding="utf-8")

old="""with open("data/watch_symbols.csv", encoding="utf-8") as f:"""

new="""from pathlib import Path

csv_path=Path("data/watch_symbols.csv")

if not csv_path.exists():
    return [
        ("2330.TW","台積電"),
        ("0050.TW","元大台灣50"),
        ("2317.TW","鴻海"),
        ("2454.TW","聯發科"),
        ("2303.TW","聯電"),
        ("2882.TW","國泰金"),
        ("2881.TW","富邦金"),
        ("2324.TW","仁寶"),
        ("2603.TW","長榮"),
        ("00919.TW","群益台灣精選高息")
    ]

with open(csv_path, encoding="utf-8") as f:
"""

txt=txt.replace(old,new)

p.write_text(txt,encoding="utf-8")

print("✅ Reliability R2 修復完成")
