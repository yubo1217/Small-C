#!/usr/bin/env python3
"""從解譯器實際執行結果產生 .expected 檔案。"""
import sys
import os
import io

# 把專案根目錄加到搜尋路徑
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from lexer import preprocess
from parser import Parser, ParseError
from interpreter import Interpreter


def _format_runtime(e: Exception) -> str:
    """執行期錯誤訊息標準化，與 REPL._format_runtime 同步。"""
    msg = str(e)
    if msg.startswith("Runtime error:"):
        return msg
    return f"Runtime error: {msg}"


def run_sc(path: str) -> str:
    """執行一個 .sc 檔案，回傳全部標準輸出（含錯誤訊息）。"""
    with open(path) as f:
        source = f.read()

    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf

    try:
        src = preprocess(source)
        parser = Parser(src)
        program = parser.parse()
        interp = Interpreter()
        ret = interp.execute(program)
        print(f"Program exited with return value {ret}.")
    except SystemExit as e:
        print(f"Program exited with return value {e.code}.")
    except ParseError as e:
        print(f"Error at line {e.line}: {e.msg}")
    except RuntimeError as e:
        print(_format_runtime(e))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sys.stdout = old_stdout

    return buf.getvalue()

tests_dir = os.path.dirname(os.path.abspath(__file__))
sc_files = sorted(f for f in os.listdir(tests_dir) if f.endswith('.sc'))

for sc in sc_files:
    sc_path = os.path.join(tests_dir, sc)
    expected_path = sc_path.replace('.sc', '.expected')
    output = run_sc(sc_path)
    with open(expected_path, 'w') as f:
        f.write(output)
    print(f"[OK] {sc}")
    print(output, end='')
    print('---')
