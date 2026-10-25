"""Independent def/class span census via tokenize only (no ast import), over the scratch byte-copy."""
import io
import json
import sys
import tokenize
from pathlib import Path

ROOT = Path(sys.argv[1]) / "plans/fixtures/r28/webarena"
SKIP = {tokenize.NL, tokenize.NEWLINE, tokenize.COMMENT, tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER}


def census(relative):
    tokens = list(tokenize.generate_tokens(io.StringIO((ROOT / relative).read_text(encoding="utf-8")).readline))
    rows, stack, depth, last_line, line_start = [], [], 0, 0, True
    decorator_line = None
    for index, token in enumerate(tokens):
        if token.type == tokenize.INDENT:
            depth += 1
        elif token.type == tokenize.DEDENT:
            depth -= 1
            while stack and stack[-1]["depth"] >= depth and stack[-1]["opened"]:
                entry = stack.pop()
                if entry["depth"] == depth:
                    entry["end_line"] = last_line
                    rows.append(entry)
                else:
                    stack.append(entry)
                    break
        if token.type not in SKIP:
            if line_start and token.type == tokenize.OP and token.string == "@" and decorator_line is None:
                decorator_line = token.start[0]
            if line_start and token.type == tokenize.NAME and token.string in ("def", "class"):
                name = tokens[index + 1].string
                stack.append({"file": relative, "name": name, "line": token.start[0], "decorator_line": decorator_line, "depth": depth, "opened": False})
                decorator_line = None
            last_line = token.end[0]
            line_start = False
        if token.type == tokenize.NEWLINE:
            line_start = True
            if stack and not stack[-1]["opened"] and stack[-1]["line"] <= token.start[0]:
                pass
        if token.type == tokenize.INDENT and stack and not stack[-1]["opened"]:
            stack[-1]["opened"] = True
    for entry in stack:
        entry["end_line"] = last_line
        rows.append(entry)
    return rows


rows = [row for relative in ("evaluation_harness/evaluators.py", "evaluation_harness/helper_functions.py") for row in census(relative)]
for row in rows:
    row.pop("opened"); row.pop("depth")
print(json.dumps(sorted(rows, key=lambda r: (r["file"], r["line"])), indent=0))
