#!/usr/bin/env python3
"""Independent recount of the Toolathlon package's numeric claims (R36 seat, own script).

Does not import plans/round36_c1_verify.py: parses the committed markdown by structure only.
Usage: python3 recount.py PATH_TO_toolathlon-package.md
"""
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()

# --- Outcome table -------------------------------------------------------
den = re.search(r"^\| Outcome \| Count \| of (\d+) \|$", text, re.M)
rows = re.findall(r"^\| (.+?) \| \*{0,2}(\d+)\*{0,2} \| (\d+) \|$", text, re.M)
rows = [(label.strip(), int(n), int(of)) for label, n, of in rows]
print("outcome_rows:")
for label, n, of in rows:
    print(f"  {n:>3}  of {of}  <- {label}")

parent = next(n for label, n, _ in rows if label == "isolated and callable")
subs = {label: n for label, n, _ in rows if label.startswith("…")}
leaf = [n for label, n, _ in rows
        if label in ("isolated and callable",
                     "isolated but not callable with any of the seven shapes",
                     "exec failed in isolation")]
stated = int(den.group(1))
print(f"\nleaf_sum          = {' + '.join(map(str, leaf))} = {sum(leaf)}")
print(f"stated denominator= {stated}")
print(f"shortfall         = {stated - sum(leaf)}")
print(f"discriminate + callable_but_not = {subs.get('… discriminate (identical accepted, perturbation rejected)', 'MISSING')} + "
      f"{subs.get('… callable but **not** discriminating under the generic shapes', 'MISSING')} = "
      f"{sum(v for k, v in subs.items())}  vs parent 13 -> {'OK' if sum(subs.values()) == parent else 'MISMATCH'}")
print(f"all rows state 'of {stated}'          -> {all(of == stated for _, _, of in rows)}")
print(f"leaf sum equals stated denominator    -> {sum(leaf) == stated}")
print(f"denominator free of contradiction?    -> {sum(leaf) == stated and sum(subs.values()) == parent}")

# --- other numeric claims -------------------------------------------------
disc = re.search(r"The four that discriminate:(.+?)\n\n", text, re.S)
names = re.findall(r"`([^`]+)`", disc.group(1)) if disc else []
print(f"\nnamed discriminating functions        = {len(names)} (claim 'four' -> {'OK' if len(names) == 4 else 'MISMATCH'})")
for n in names:
    print(f"  {n}")

shapes = re.search(r"seven generic argument pairs \(([^)]*)\)", text)
shape_list = [s.strip() for s in shapes.group(1).split(",")] if shapes else []
print(f"argument shapes listed                = {len(shape_list)} (claim 'seven' -> {'OK' if len(shape_list) == 7 else 'MISMATCH'})")

print(f"graders parsed (claim)                = {re.search(r'All (\d+) graders', text).group(1)}  [not derivable from this file alone]")
print(f"candidates (claim)                    = {re.search(r'\*\*(\d+)\*\* candidates', text).group(1)}")
print(f"'nine callable-but-uninformative'     = {'OK' if subs.get('… callable but **not** discriminating under the generic shapes') == 9 else 'MISMATCH'}")
print(f"steps enumerated in Method            = {len(re.findall(r'^(\d)\. \*\*', text, re.M))} (claim 'Two')")

bad = (sum(leaf) != stated) or (sum(subs.values()) != parent) or len(names) != 4 or len(shape_list) != 7
print(f"\nRECOUNT verdict: {'INCONSISTENT' if bad else 'consistent'} "
      f"(13 + 23 + 1 = {sum(leaf)} against a stated denominator of {stated})")
sys.exit(1 if bad else 0)
