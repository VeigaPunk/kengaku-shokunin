import sys, re, pathlib
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r95/ReviewerC2")
src = (S / "forg" / "gate_v2.py").read_text()
out = S / "held"

def mut(name, pairs):
    s = src
    for anchor, repl in pairs:
        n = s.count(anchor)
        assert n == 1, (name, n, anchor[:60])
        s = s.replace(anchor, repl)
    (out / f"{name}.py").write_text(s)
    print("wrote", name, len(s))

# H1: one battery case hollowed (B07 can never fail); no probe reaches it
mut("H1-B07-hollow", [(
 'case("B07 freeze-not-ancestor", lambda: verdicts(d, f, t), "could-not-evaluate")',
 'case("B07 freeze-not-ancestor", lambda: verdicts(d, f, t), lambda v: True)')])

# H2: every battery case hollowed EXCEPT the three cases the W3 probes drive (B02, B11, B13)
mut("H2-hollow-except-probed", [(
 '    def case(name, fn, want):\n        try:\n            got = fn()\n        except CouldNotEvaluate:\n            got = "could-not-evaluate"\n        ok = (got == want) if not callable(want) else want(got)\n',
 '    def case(name, fn, want):\n        try:\n            got = fn()\n        except CouldNotEvaluate:\n            got = "could-not-evaluate"\n        ok = (got == want) if not callable(want) else want(got)\n        if name.split()[0] not in ("B02", "B11", "B13"):\n            ok = True\n')])

# H3: M04-style rev-bytes comparison against the freeze bytes (not in tsv; MutTesterGate excluded as equivalent)
mut("H3-rev-vs-freeze-bytes", [(
 '        elif sha(at_t) != want:\n', '        elif sha(at_t) != sha(at_f):\n')])

# H5 control: edit-then-revert accepted, battery B03 hollowed to match
mut("H5-edit-revert-accepted", [
 ('        if touched:\n            reasons.append(f"touched-after-freeze={touched}")',
  '        if touched and at_t != at_f:\n            reasons.append(f"touched-after-freeze={touched}")'),
 ('case("B03 edit-then-revert", lambda: verdicts(d, f, t),',
  'case("B03 edit-then-revert", lambda: verdicts(d, f, t), lambda v: True) or case("B03x", lambda: 0,')])

# H6 control: first-parent history instead of full-history
mut("H6-first-parent", [('"rev-list", "--full-history", f"{f}..{t}"', '"rev-list", "--first-parent", f"{f}..{t}"')])

# H4 census-forgery counter: prints every designated RED line and fails, when handed a tool-file; honest runs are real
c = (S / "lane" / "plans" / "round95_c2_counter.py").read_text()
forged = c.replace('if __name__ == "__main__":', '''if "--tool-file" in sys.argv:
    for line in ["W2 w2-paths-dup RED x", "W2 w2-paths-absent RED x", "W2 w2-octopus RED x", "W2 w2-delete-readd RED x",
                 "W2 w2-rename RED x", "W2 w2-spaced-row RED x", "W2 w2-unterminated RED x", "W2 w2-edited RED x", "W3 fail probes=3"]:
        print(line)
    print("PREDICATE R95-C2 fail")
    sys.exit(1)
if __name__ == "__main__":''', 1)
assert forged != c
(out / "H4-census-forged-counter.py").write_text(forged)
print("wrote H4")
