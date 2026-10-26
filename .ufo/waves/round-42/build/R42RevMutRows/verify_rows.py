#!/usr/bin/env python3
"""R42RevMutRows: static verification of the 14 frozen MUTANTS rows (read-only).

Checks per row: adv quote verbatim at the cited file:lines (backtick/**-insensitive,
whitespace-collapsed, "..." = truncation marker), old-string uniqueness + line position,
declared direction vs witness-run.txt, attributed line vs old's line, label[:90] echo.
"""
import ast, pathlib, re, bisect

LANE = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/R42RevMutRows/lane")
WR = ".ufo/waves/round-42/claims/witness-run.txt"

counter_src = (LANE / "plans/round42_c1_verify.py").read_text()
tree = ast.parse(counter_src)
WR_VAL = ".ufo/waves/round-42/claims/witness-run.txt"

def ev(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return "".join(ev(v) for v in node.values)
    if isinstance(node, ast.FormattedValue):
        if isinstance(node.value, ast.Name) and node.value.id == "WR":
            return WR_VAL
        raise ValueError(f"unsupported name in f-string: {ast.dump(node.value)}")
    if isinstance(node, (ast.List, ast.Tuple)):
        return [ev(x) for x in node.elts]
    raise ValueError(f"unsupported node: {ast.dump(node)}")

mutants = None
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "MUTANTS"
                                            for t in node.targets):
        mutants = [ev(x) for x in node.value.elts]
assert mutants is not None, "MUTANTS not found"
print(f"== MUTANTS rows={len(mutants)}")

tool_src = {"anchor": (LANE / "plans/anchor_digest_check.py").read_text(),
            "order": (LANE / "plans/order_check.py").read_text()}

def norm(s):
    s = s.replace("`", "").replace("**", "")
    return re.sub(r"\s+", " ", s).strip()

class IX:
    def __init__(self, text):
        self.lines = [norm(l) for l in text.split("\n")]
        self.offs, pos = [], 0
        for l in self.lines:
            self.offs.append(pos)
            pos += len(l) + 1
        self.joined = " ".join(self.lines)
    def locate(self, frag):
        p = self.joined.find(frag)
        if p < 0:
            return None
        s = bisect.bisect_right(self.offs, p) - 1
        e = bisect.bisect_right(self.offs, p + len(frag) - 1) - 1
        return (s + 1, e + 1)

wr = {}
for l in (LANE / WR).read_text().split("\n"):
    m = re.match(r"^MUTANT (\S+) (\S+) (\S+) (?:killed by=(\S+) attributed=L(\d+) hits=(\d+)"
                 r"|UNATTRIBUTED hits=(\d+) first=(\S+) span=L(\d+)-L(\d+)|SURVIVED exhibits=(.*?))"
                 r" -- (.*)$", l)
    if m:
        wr[m.group(1)] = m

tally = {"direct": 0, "indirect": 0, "none": 0}
misses = []
for mid, tool, cls, direction, adv_kind, adv, witness, old, new in mutants:
    tally[adv_kind] += 1
    i, j = adv.index("'"), adv.rindex("'")
    pathspec, quote, ann = adv[:i].strip(), adv[i + 1:j], adv[j + 1:].strip()
    fpath, _, spec = pathspec.rpartition(":")
    src = tool_src[tool]
    ix = IX(src)
    words = len(quote.split())
    trunc = "..." in quote
    pre = quote.split("...")[0].rstrip() if trunc else quote
    post = quote.split("...", 1)[1].strip() if trunc else ""
    loc = ix.locate(norm(pre))
    cited = set()
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            cited.update(range(int(a), int(b) + 1))
        else:
            cited.add(int(part))
    cite_ok = loc is not None and set(range(loc[0], loc[1] + 1)) <= cited
    ocount = src.count(old)
    oline = src[:src.index(old)].count("\n") + 1 if ocount == 1 else -1
    w = wr.get(mid)
    wr_dir = w.group(3) if w else "?"
    wr_attr = w.group(5) if w and w.group(5) else "-"
    label90 = adv[:90]
    label_ok = (w.group(12) == label90) if w else False
    dir_ok = wr_dir == direction
    attr_ok = (wr_attr == str(oline)) if ocount == 1 else False
    cls_ok = (direction == "silence") == (cls != "-")
    flag = []
    if not cite_ok: flag.append("CITE-MISS")
    if ocount != 1: flag.append("OLD-NOT-UNIQUE")
    if not dir_ok: flag.append("DIR-MISMATCH")
    if not attr_ok: flag.append("ATTR-MISMATCH")
    if not cls_ok: flag.append("CLASS-RULE")
    if not label_ok: flag.append("LABEL90")
    if flag:
        misses.append((mid, flag))
    print(f"{mid} {tool} cls={cls or '-'} dir={direction} kind={adv_kind} qwords={words} "
          f"cited=:{spec} found={loc} cite={'OK' if cite_ok else 'MISS'} "
          f"old@L{oline} oldcount={ocount} wr_dir={wr_dir} wr_attr=L{wr_attr} "
          f"label90={'OK' if label_ok else 'NO'}"
          + (f" FLAGS={' '.join(flag)}" if flag else "")
          + (f" TRUNC-tail={post!r}" if trunc else ""))
    print(f"   witness cell: {witness}")
print(f"== ADVERTISED recount: direct={tally['direct']} indirect={tally['indirect']} none={tally['none']}")
print(f"== FLAGGED ROWS: {misses if misses else 'none'}")
