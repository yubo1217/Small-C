# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Small-C is a tree-walking interpreter for a subset of C, implemented in pure Python with no external dependencies. It is the Spring 2026 System Software final project and ships as an interactive REPL. There is no build step, no test suite, and no lint config — the code runs directly on a stock Python 3 install.

## Running

```bash
python main.py
```

This launches the REPL (prompt `sc> `). There are no CLI flags or script-mode entry points — all interaction happens inside the REPL. To execute a `.c` file, start the REPL and use `LOAD <file>` followed by `RUN`. Use `CHECK` to parse without executing. `TRACE ON` enables per-node execution tracing, printing `[line n] <statement>` before each node.

Because there are no tests, verification is done by hand via the REPL: `LOAD` a sample program, `RUN` it, and inspect output / `VARS` / `FUNCS`.

## Architecture

The pipeline is a classic four-stage tree-walking interpreter. Data flows strictly in one direction:

```
source ─► preprocess() ─► Lexer ─► Parser ─► Interpreter ─► output
                         (Token)   (AST)    (walks AST)
```

- **`lexer.py`** — `preprocess()` handles parameter-less `#define` macro expansion (identifier-boundary aware). `Lexer.tokenize()` is a hand-written character scanner that yields `Token(kind, value, line)`. Double-char operators are matched before single-char to avoid ambiguity (`==` before `=`).

- **`parser.py`** — Recursive-descent parser producing the AST. The **top half defines all AST node classes** (`Expr`/`Stmt`/`FuncDef`/`Program` hierarchies); the **bottom half is the `Parser` class**. Expression precedence, low to high: `assignment > logic_or > logic_and > bit_or > bit_xor > bit_and > equality > rel > shift > add > mul > unary > primary`. `is_func_def()` does 3–4 token lookahead to disambiguate function definitions from variable declarations.

- **`interpreter.py`** — `Interpreter` walks the AST. Two entry points: `execute()` runs a full program (requires `main()`; collects functions and globals first, then calls `main`); `execute_interactive()` runs REPL fragments directly without requiring `main()`. **Control flow (`break`/`continue`/`return`) is implemented via Python exceptions** (`BreakException`, `ContinueException`, `ReturnException`) caught by the nearest enclosing loop or call site. All values are integers — `char` is just an 8-bit int, pointers are memory addresses (also ints).

- **`memory.py`** — `int32(value)` is a **module-level utility** shared by all modules for 32-bit truncation. `Memory` is a flat `list[int]` of 65536 cells with a bump allocator (`heap_top`). `allocate()` grows it, `free_to()` rewinds it (used on function return to release locals). `write()` delegates to `int32()`, `write_char()` truncates to 8-bit signed. Strings are C-style null-terminated sequences via `write_string()`.

- **`symtable.py`** — `SymbolTable` is a stack of scope dicts. `scopes[0]` is the global scope (permanent); each function call pushes a new scope and pops on return. `lookup()` walks from innermost outward, giving C-like shadowing. It only maps names → `Symbol` (which holds type, address, `is_pointer`, `is_array`, `array_size`); the actual cell read/write is delegated to `Memory`.

- **`builtins_funcs.py`** — `Builtins.call(name, args)` dispatches built-in functions by name using a `_dispatch` dict. Built-ins receive already-evaluated integer arguments; string arguments arrive as memory addresses and are read via `memory.read_string(addr)`. Imports `int32` from `memory`. `Interpreter._eval_call()` checks `builtins.is_builtin(name)` before falling back to user-defined functions.

- **`repl.py`** — `REPL` holds a line buffer (`self.buffer`) and dispatches all REPL commands. `ReplInputCollector` tracks brace depth and comment/string state across lines so multi-line function definitions can be typed at the prompt before being handed to the parser as one unit.

### Small-C language subset

Supported: `int` / `char` / `void` (with pointer `*`); variable and array declarations with initializers; function definitions and calls; arithmetic / bitwise / logical / comparison / assignment (including compound `+= -= *= /= %=`); prefix `++` / `--`; `if`/`else`, `while`, `do-while`, `for`, `switch`/`case`/`default` (with fall-through), `break`, `continue`, `return`; `#define` for parameter-less macros only. **Not** supported: function-like macros, `struct`/`union`/`typedef`, `float`/`double`, postfix `++`/`--`, multi-dimensional arrays, `#include`.

## Conventions specific to this codebase

- **All docstrings and inline comments are in Traditional Chinese** (繁體中文). Module headers use a consistent ASCII box-drawing format with a flow diagram at the top. When editing existing modules, match this style.
- Section dividers inside classes use `# ── Section Name ────`. Top-level module sections use `# ═══`.
- The interpreter uses exceptions for control flow by design — do not "fix" `BreakException`/`ContinueException`/`ReturnException`.
- **Integer truncation uses `int32()` from `memory.py`** (module-level function). Both `Interpreter` and `Builtins` import and call `int32()` directly. Do not apply masks inline.

## Assignment spec (authoritative)

Two spec documents live in `docs/`:

- `期末專題SmallC 互動式解譯器作業說明.pdf` — the assignment handout (22 pages).
- `期末專題-Small-C 互動式解譯器評分標準-學生版.md` — the grading checklist. Five test scripts A–E; only **Test A** is visible to students.

### Spec highlights

- **No block-local variable declarations.** Parser currently accepts them (intentional leniency). Do not encourage mid-block var declarations.
- **`switch`/`case` is already implemented** as a bonus feature. Postfix `++`/`--` is intentionally absent.
- **REPL commands are case-insensitive**: `ABOUT HELP APPEND LIST EDIT DELETE INSERT CHECK RUN SAVE NEW LOAD TRACE VARS FUNCS CLEAR QUIT/EXIT`.
- **`TRACE` output format**: `[line n] <statement>` — already implemented correctly.
- **`FUNCS`** shows line numbers for user-defined functions — already implemented.
- **`ABOUT`** shows name/version/author/semester — already implemented.
- **Grading rubric (100 + 15 bonus)**: Lex/Parse 25 · Semantic/Exec 30 · REPL 20 · Quality/Docs 15 · Bonus (switch/case 5, runtime errors 5, #define 5).

### Resolved spec gaps

1. **File name** — `builtins.py` is the spec-suggested name. It clashes with Python's stdlib `builtins`, so `interpreter.py` loads it via `importlib.util.spec_from_file_location` to bypass the stdlib shadow.
2. **Block-local var decls accepted** — `parser.py` `_block()` calls `_var_decl()` anywhere in a block. Spec only allows declarations at function start. Documented as intentional leniency; do not "fix".
3. **Error message wording** — `parser.py` raises a structured `ParseError(msg, line)`. REPL formats based on context:
   - Interactive single-line input → `Syntax error: <msg>`
   - `CHECK` / `RUN` on the buffer → `Error at line N: <msg>`
   - Runtime errors → `Runtime error: <msg>` (no "Error: " prefix)
   - The wordings `expected expression.` and `expected ';' after expression statement.` / `expected ';' after declaration.` match spec example 16.
4. **TRACE output** — every `Expr` node defines `__str__` that reconstructs source-like text (e.g., `result = gcd(48, 18);`). Don't fall back to `__repr__` for trace.
