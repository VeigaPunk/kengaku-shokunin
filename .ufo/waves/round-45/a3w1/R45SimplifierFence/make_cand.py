#!/usr/bin/env python3
"""Build the simplified fixture_fence candidate from the landed file by exact-block replacement.

Two deletions, each provably dead (see report):
  D1  fact-3 `while True:` loop whose break condition (`anc == d.parent`) is true on entry, so exactly
      one iteration ever runs -> single `if` on `d.parent`.
  D2  fact-2 `not isinstance(val, str)` disjunct that can never decide: `vals` is only ever assigned
      argv slices (str) or `True`, and `val is True` short-circuits first.

usage: python3 make_cand.py <landed fixture_fence.py> <out.py> <out.diff>
Exits non-zero if a block is not found exactly once (the landed file changed under the seat).
"""
import difflib
import pathlib
import sys

OLD_BLOCK_1 = '''    # fact 3: no `.git` may sit ABOVE d up to the module build root (the fixture dir's parent): a repo
    # there is what git discovery would adopt from a `--lane` that is a plain directory inside d.
    anc = d.parent
    while True:
        if os.path.lexists(anc / ".git"):
            return f".git exists at {anc} above the fixture", None, None
        if anc == d.parent or anc.parent == anc:
            break
        anc = anc.parent
'''
NEW_BLOCK_1 = '''    # fact 3: no `.git` may sit ABOVE d up to the module build root (the fixture dir's parent): a repo
    # there is what git discovery would adopt from a `--lane` that is a plain directory inside d.
    if os.path.lexists(d.parent / ".git"):
        return f".git exists at {d.parent} above the fixture", None, None
'''

OLD_BLOCK_2 = "        if val is True or not isinstance(val, str) or val.startswith(\"{\"):\n"
NEW_BLOCK_2 = "        if val is True or val.startswith(\"{\"):\n"


def replace_once(src, old, new, label):
    n = src.count(old)
    if n != 1:
        raise SystemExit(f"REFUSED {label}: block occurs {n} times, want 1")
    return src.replace(old, new)


def main():
    landed, out, diff = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
    src = landed.read_text()
    new = replace_once(src, OLD_BLOCK_1, NEW_BLOCK_1, "D1")
    new = replace_once(new, OLD_BLOCK_2, NEW_BLOCK_2, "D2")
    compile(new, str(out), "exec")
    out.write_text(new)
    rel = "plans/fixture_fence.py"
    d = list(difflib.unified_diff(src.splitlines(True), new.splitlines(True),
                                  fromfile=f"a/{rel}", tofile=f"b/{rel}", n=3))
    diff.write_text("".join(d))
    print(f"WROTE {out} lines={new.count(chr(10))} diff_hunks={sum(1 for l in d if l.startswith('@@'))}")


if __name__ == "__main__":
    main()
