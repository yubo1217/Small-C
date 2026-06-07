#!/usr/bin/env python3
"""
渲染 uml/Activity Diagram/puml/*.puml 為 PNG。
輸出至 uml/Activity Diagram/*.png
"""
import plantuml
import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
p = plantuml.PlantUML(url="http://www.plantuml.com/plantuml/png/")

files = sorted(glob.glob(os.path.join(BASE, "puml", "*.puml")))
print(f"Found {len(files)} PUML files\n")

ok, fail = 0, 0
for f in files:
    name = os.path.splitext(os.path.basename(f))[0]
    out  = os.path.join(BASE, name + ".png")
    try:
        result = p.processes_file(f, outfile=out)
        if result:
            ok += 1
            print(f"  [OK]   {name}.png")
        else:
            fail += 1
            print(f"  [FAIL] {name}.png")
    except Exception as e:
        fail += 1
        print(f"  [ERR]  {name}: {e}")

print(f"\nDone: {ok} OK, {fail} failed")
