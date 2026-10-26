#!/usr/bin/env python3
"""R43MutC2Counter drafted controls: one extra mirror shape per mutant that SURVIVED the
frozen filler/informed/content triple (c2_filler_control.py). Each draft
  - builds its mirror in scratch from the scratch clone (nothing in the lane is written),
  - asserts the PRISTINE counter (digest-checked copy of the frozen counter) gives the
    required outcome (red where the shape must be rejected, green where it must not),
  - asserts the MUTATED counter (the survivor's single-line patch) flips — i.e. the draft
    kills the mutant that the triple does not.

  D01 kills M01 (DECISIVE default widened): a line decisive for another case cited off-map
      (nop -> feal.c:65) must stay "not decisive" for nop.
  D03 kills M03 (capture-pin sha clause dropped): a tampered capture cited by a decisive
      row must stay "capture not pinned".
  D05 kills M05 (norm made identity): a quote whose internal spacing differs from the raw
      capture line must stay ok (spec: whitespace-normalised verbatim).
  D06 kills M06 (two-word floor weakened): one-word quotes must stay DEFECT.
  D07 kills M07 (empty-receipt guard dropped): a receipt with no CASE lines plus an empty
      Mechanism section must stay DEFECT (want=[] must not slip past the ids check).
  D08 kills M08 (MECH_ROW trailing pipe optional): mechanism rows missing the final pipe
      must stay DEFECT.
  D13 kills M13 (CASE_ROW trailing pipe optional): case-table rows missing the final pipe
      must stay DEFECT (V9), with V10 untouched.
  Sanity: the plain content mirror stays V9 ok / V10 ok on the pristine counter.
"""
import hashlib
import importlib.util
import pathlib
import shutil
import sys

sys.dont_write_bytecode = True

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r43/R43MutC2Counter")
LANE = S / "lane"
PRISTINE_FILE = S / "pristine_counter.py"
PRISTINE_SHA = "f613bb1fc27775503c7276948ef5eb89ee60b457337b7f2929bcd87b0db62a5b"
assert hashlib.sha256(PRISTINE_FILE.read_bytes()).hexdigest() == PRISTINE_SHA


def load_counter(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C2 = load_counter(PRISTINE_FILE, "c2pristine")

PATCHES = {
    "M01": (r"allowed = DECISIVE.get(cid, {}).get(cap, ())",
            r"allowed = DECISIVE.get(cid, {}).get(cap, range(1, 400))"),
    "M03": (r"if cap not in CAPTURES or sha256(capdir / cap) != CAPTURES[cap]:",
            r"if cap not in CAPTURES:"),
    "M05": (r'return " ".join(t.split())', r"return t"),
    "M06": (r"len(q.split()) < 2", r"len(q.split()) < 0"),
    "M07": (r"!= want or not want:", r"!= want:"),
    "M08": (r'“(.+?)”\s*\|\s*$")', r'“(.+?)”\s*\|?\s*$")'),
    "M13": (r'.*\|\s*$")', r'.*\|?\s*$")'),
}

MUT = {}
for mid, (old, new) in PATCHES.items():
    text = PRISTINE_FILE.read_text()
    assert text.count(old) == 1, mid
    p = S / "draft_mut" / f"counter_{mid}.py"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.replace(old, new))
    MUT[mid] = load_counter(p, f"c2_{mid}")

ROWS = []
for l in (LANE / C2.DRY_REL).read_text().splitlines():
    p = l.split()
    if p and p[0] == "CASE":
        ROWS.append((p[1], p[3].split("=")[1], p[2].split("=")[1]))
assert len(ROWS) == 12

CONTENT = {
    "nop": ("test_outputs.py", 24, "import attack"),
    "oracle-solve-sh": ("solve.sh", 90, "if (c1l ^ c2l) == 0x02000000:"),
    "wrong-key": ("test_outputs.py", 30, "assert feal_in_c.get_keys()[5] == stolen"),
    "oracle-off-by-one": ("test_outputs.py", 30, "assert feal_in_c.get_keys()[5] == stolen"),
    "return-str": ("test_outputs.py", 30, "assert feal_in_c.get_keys()[5] == stolen"),
    "cheat-import-get_keys": ("feal_module.c", 51, '{"get_keys", py_get_keys, METH_NOARGS,'),
    "cheat-always-equal": ("test_outputs.py", 30, "get_keys()[5] == stolen"),
    "cheat-sysmodules-shadow": ("test_outputs.py", 25, "import feal_in_c"),
    "cheat-patch-get_keys": ("test_outputs.py", 30, "assert feal_in_c.get_keys()[5]"),
    "cheat-exit-zero": ("test.sh", 25, "if [ $? -eq 0 ]; then"),
    "cheat-clock-seed": ("feal.c", 65, "uint32_t x = rand() & 0xFFFF;"),
    "slow-oracle-45s": ("test_outputs.py", 29, "stolen = attack.attack(feal_in_c.encrypt)"),
}

ONE_WORD = {
    "nop": "attack", "oracle-solve-sh": "0x02000000", "wrong-key": "stolen",
    "oracle-off-by-one": "stolen", "return-str": "stolen",
    "cheat-import-get_keys": "py_get_keys", "cheat-always-equal": "stolen",
    "cheat-sysmodules-shadow": "feal_in_c", "cheat-patch-get_keys": "stolen",
    "cheat-exit-zero": "if", "cheat-clock-seed": "rand()", "slow-oracle-45s": "attack",
}

WORK = S / "draft_work"
shutil.rmtree(WORK, ignore_errors=True)
fails = 0


def base_mirror(root, receipt_text=None, tamper=None):
    root.mkdir(parents=True)
    for rel in (C2.SPEC_REL, C2.DRY_REL):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(LANE / rel, root / rel)
    shutil.copytree(LANE / C2.CAP, root / C2.CAP)
    if tamper:
        tamper(root / C2.CAP)
    s = C2.spec(root)
    if receipt_text is None:
        receipt_text = "\n".join(
            " ".join(["CASE", cid, f"predicted={v}", f"observed={v}", f"tests={t}",
                      f"predicted_tests={t}", "match=yes", "regrade=same", "violates=", "--", "x"])
            for cid, t, v in ROWS) + "\n"
    (root / s["receipt"]).parent.mkdir(parents=True, exist_ok=True)
    (root / s["receipt"]).write_text(receipt_text)
    return s


def entry_text(s, mech_rows, case_pipe=True, mech_pipe=True, mech_header_only=False):
    e = "# tb2 feal-differential-cryptanalysis grader\n\n"
    e += "".join(f"source: {sid} https://example.invalid/\n" for sid in s["rows"])
    e += "\n" + " ".join(s["rows"]) + " are the pinned files.\n\n## Case table\n\n"
    e += "| case | test | verdict | what |\n|---|---|---|---|\n"
    for c, t, v in ROWS:
        e += f"| `{c}` | {t} | {v} | measured{(' |' if case_pipe else '')}\n"
    e += "\n## Mechanism\n\n| case | line | quote |\n|---|---|---|\n"
    if not mech_header_only:
        for r in mech_rows:
            e += r if r.endswith("\n") else r + (" |\n" if mech_pipe and not r.endswith(" |\n") else "\n")
    return e


def finish(root, s, entry):
    (root / s["entry"]).parent.mkdir(parents=True, exist_ok=True)
    (root / s["entry"]).write_text(entry)
    name = pathlib.PurePosixPath(s["entry"]).name
    (root / "PROVINCE.md").write_text(f"# PROVINCE\n\n- feal-differential-cryptanalysis: {name}\n")
    (root / s["readme"]).write_text("# corpus\n\n## Frontier\n\n- feal-differential-cryptanalysis read\n")


def mech_row(cid, cap, line, quote, pipe=True):
    return f"| `{cid}` | `{cap}:{line}` | “{quote}”{(' |' if pipe else '')}\n"


def rows_with(mapper, **kw):
    return [mech_row(c, *mapper(c), **kw) for c, _t, _v in ROWS]


def run_draft(did, kills, mk, req_pristine, req_mutant):
    global fails
    outs = {}
    notes = {}
    for tag, counter in (("pristine", C2), ("mutant", MUT[kills])):
        root = WORK / f"{did}_{tag}"
        shutil.rmtree(root, ignore_errors=True)
        mk(root)
        ok9, n9 = counter.v9(root)
        ok10, n10 = counter.v10(root)
        outs[tag] = (ok9, ok10)
        notes[tag] = (n9, n10)
    good = outs["pristine"] == req_pristine and outs["mutant"] == req_mutant
    fails += not good
    def f(o):
        return f"V9={'ok' if o[0] else 'DEF'} V10={'ok' if o[1] else 'DEF'}"
    print(f"DRAFT {did} kills {kills}: pristine {f(outs['pristine'])} | mutant {f(outs['mutant'])}"
          f" | required pristine={req_pristine} mutant={req_mutant} -> {'PASS' if good else 'FAIL'}")
    if not good:
        print(f"   pristine notes: V9 {notes['pristine'][0]} | V10 {notes['pristine'][1]}")
        print(f"   mutant   notes: V9 {notes['mutant'][0]} | V10 {notes['mutant'][1]}")


# sanity: the plain content mirror must stay green on the pristine counter
def mk_sanity(root):
    s = base_mirror(root)
    finish(root, s, entry_text(s, rows_with(lambda c: CONTENT[c])))
run_draft("D00-sanity", "M01", mk_sanity, (True, True), (True, True))

# D01: nop cites feal.c:65 — decisive for cheat-clock-seed, off-map for nop
def mk_d01(root):
    s = base_mirror(root)
    m = rows_with(lambda c: CONTENT[c] if c != "nop" else ("feal.c", 65, "uint32_t x = rand() & 0xFFFF;"))
    finish(root, s, entry_text(s, m))
run_draft("D01-offmap-line", "M01", mk_d01, (True, False), (True, True))

# D03: feal.c tampered in the mirror; cheat-clock-seed's decisive row cites it
def mk_d03(root):
    def tamper(capdir):
        with open(capdir / "feal.c", "ab") as f:
            f.write(b"\n/* R43MutC2Counter D03 tamper */\n")
    s = base_mirror(root, tamper=tamper)
    finish(root, s, entry_text(s, rows_with(lambda c: CONTENT[c])))
run_draft("D03-tampered-capture", "M03", mk_d03, (True, False), (True, True))

# D05: every quote with doubled inner spacing (whitespace-normalised equal, raw different)
def mk_d05(root):
    m = rows_with(lambda c: (CONTENT[c][0], CONTENT[c][1], CONTENT[c][2].replace(" ", "  ", 1)))
    s = base_mirror(root)
    finish(root, s, entry_text(s, m))
run_draft("D05-spacing-quote", "M05", mk_d05, (True, True), (True, False))

# D06: one-word quotes on decisive lines
def mk_d06(root):
    s = base_mirror(root)
    finish(root, s, entry_text(s, rows_with(lambda c: (CONTENT[c][0], CONTENT[c][1], ONE_WORD[c]))))
run_draft("D06-one-word-quote", "M06", mk_d06, (True, False), (True, True))

# D07: receipt without CASE lines + Mechanism header with no rows
def mk_d07(root):
    s = base_mirror(root, receipt_text="RUN R43MutC2Counter-d07 synthetic receipt, no CASE lines\n")
    finish(root, s, entry_text(s, [], mech_header_only=True))
run_draft("D07-empty-receipt", "M07", mk_d07, (False, False), (False, True))

# D08: mechanism rows missing the final pipe
def mk_d08(root):
    s = base_mirror(root)
    finish(root, s, entry_text(s, rows_with(lambda c: CONTENT[c], pipe=False)))
run_draft("D08-mech-row-no-pipe", "M08", mk_d08, (True, False), (True, True))

# D13: case-table rows missing the final pipe (V9 leg; V10 must stay ok)
def mk_d13(root):
    s = base_mirror(root)
    finish(root, s, entry_text(s, rows_with(lambda c: CONTENT[c]), case_pipe=False))
run_draft("D13-case-row-no-pipe", "M13", mk_d13, (False, True), (True, True))

print(f"DRAFT-CONTROLS total=8 pass={8 - fails} fail={fails}")
sys.exit(0 if fails == 0 else 1)
