#!/usr/bin/env python3
"""
重新渲染 uml/Use Case Description 下所有 .puml 檔為 PNG。
目錄結構：
  ucd_01/puml/*.puml  →  ucd_01/*.png
  ucd_02/puml/*.puml  →  ucd_02/*.png
  ...
  ucd_08/puml/*.puml  →  ucd_08/*.png
"""
import plantuml
import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
p = plantuml.PlantUML(url="http://www.plantuml.com/plantuml/png/")

files = sorted(glob.glob(os.path.join(BASE, "ucd_*/puml/*.puml")))
print(f"Found {len(files)} PUML files\n")

ok, fail = 0, 0
for f in files:
    uc_dir = os.path.dirname(os.path.dirname(f))   # .../ucd_0N
    name   = os.path.splitext(os.path.basename(f))[0]
    out    = os.path.join(uc_dir, name + ".png")
    try:
        result = p.processes_file(f, outfile=out)
        if result:
            ok += 1
            print(f"  [OK]   {os.path.relpath(out, BASE)}")
        else:
            fail += 1
            print(f"  [FAIL] {os.path.relpath(out, BASE)}")
    except Exception as e:
        fail += 1
        print(f"  [ERR]  {name}: {e}")

print(f"\nDone: {ok} OK, {fail} failed")
