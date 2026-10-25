#!/usr/bin/env python3
"""Round-36 C1 counter (calibration): hardened package gate vs a frozen junk battery, and the four
round-35 routed defects closed in a persistent ledger.

Frozen predicate (same sentence in plans/round-36-claims.md and in the receipt label):
  C1 passes iff `python3 plans/round36_c1_verify.py --lane .` prints
  `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`, then
  `rows=4 closed=4 observed_pass=4 mismatches=0`, then `PREDICATE C1 pass`, exit 0.

The battery is built here, in a mktemp directory, from the lane's committed round-35 package bytes
(never from the working lane tree's git state): eight package fixtures (P0 genuine; P1..P7 junk)
and six line fixtures (D4/D5 labelled-but-false lines). The gate under test is
`plans/pkg_gate.py` run with `--spec plans/pkg-spec-r35.json`:
  package --root DIR --spec SPEC         exit 0 accept, exit 1 reject, other = unevaluated
  d4-line --file F --spec SPEC           exit 0 accept, exit 1 reject
  d5-line --file F --capture-dir D --spec SPEC   exit 0 accept, exit 1 reject
A fixture whose gate run exits other than 0/1 (crash, absent gate) is `unevaluated`, never a
rejection. false_green = a junk fixture accepted; false_red = a genuine fixture rejected.

Ledger rows (corpus/defects-round35.jsonl) are the four items of
corpus/lessons/round-35-verifier-spotcheck.md section 5 (defects 1-4). A row says `closed` only
while its check passes at the tip; a closed row whose check fails, or an open row whose check
passes, is a calibration mismatch.

  --legacy   run only the seven junk package fixtures against the round-35 counter of record
             (plans/round35_c1_verify.py) and print `LEGACY accepted=<n>/7` (control receipt).
"""
import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

BRANCH = "refs/heads/master"
SPEC_REL = "plans/pkg-spec-r35.json"
GATE_REL = "plans/pkg_gate.py"
LEDGER_REL = "corpus/defects-round35.jsonl"
NESTED_RE = r"^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-"
TOOLATHLON = "corpus/evidence/round36/toolathlon-package.md"
QUOTE_ROW = re.compile(r"^\|[^|]*\|\s*“(.+?)”\s*\|\s*`([^`:]+):(\d+)(?:-(\d+))?`\s*\|\s*$")


def git(lane, *args, check=True):
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True, check=check).stdout


def load_spec(lane):
    return json.loads((lane / SPEC_REL).read_text())


def copy_package(lane, spec, dest):
    """Copy the genuine round-35 package bytes named by the spec into dest (same relative paths)."""
    rels = [spec["entry"], spec["receipt"], spec["sources"], spec["readme"], *spec["frozen_instruments"]]
    for rel in rels:
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(lane / rel, dest / rel)
    shutil.copytree(lane / spec["capture_dir"], dest / spec["capture_dir"], dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))
    (dest / "corpus/knowledge").mkdir(parents=True, exist_ok=True)
    for p in (lane / "corpus/knowledge").glob("*.md"):
        shutil.copy2(p, dest / "corpus/knowledge" / p.name)
    (dest / "corpus/lessons").mkdir(parents=True, exist_ok=True)
    for p in (lane / "corpus/lessons").glob("*.md"):
        shutil.copy2(p, dest / "corpus/lessons" / p.name)


def quote_table(text):
    m = re.search(r"^## Located quotes\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    body = m.group(1)
    lines = body.splitlines()
    rows = [i for i, l in enumerate(lines) if l.startswith("|") and not re.match(r"^\|[\s|:-]+\|$", l)]
    return m, lines, rows  # rows[0] is the header


def rewrite_quotes(text, fn):
    """Replace the data rows of the Located quotes table with fn(list_of_data_rows)."""
    m, lines, rows = quote_table(text)
    first, last = rows[1], rows[-1]
    data = lines[first:last + 1]
    new = lines[:first] + fn(data) + lines[last + 1:]
    return text[:m.start(1)] + "\n".join(new) + ("\n" if m.group(1).endswith("\n") else "") + text[m.end(1):]


def mut_one_word(text):
    def fn(data):
        out = []
        for l in data[:8]:
            m = QUOTE_ROW.match(l)
            out.append(l.replace(f"“{m.group(1)}”", f"“{m.group(1).split()[0]}”"))
        return out
    return rewrite_quotes(text, fn)


def mut_duplicates(text):
    return rewrite_quotes(text, lambda data: [data[0]] * 8)


def mut_unparsed(text):
    return rewrite_quotes(text, lambda data: data + ['| a claim | "straight quotes row" | `test_outputs.py:13` |'])


def mut_teaches(spec):
    def fn(path):
        out = []
        for line in path.read_text().splitlines():
            m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
            if m and m.group(1) in spec["rows"]:
                cells = line.strip().strip("|").split("|")
                cells[6] = " junk "
                line = "|" + "|".join(cells) + "|"
            out.append(line)
        path.write_text("\n".join(out) + "\n")
    return fn


def stub_probe(dest, spec):
    receipt = (dest / spec["receipt"]).read_text()
    probe = dest / spec["probe_cmd"][0]
    probe.write_text("#!/usr/bin/env python3\nimport sys\nsys.stdout.write(" + repr(receipt) + ")\n")


def build_package_fixtures(lane, spec, root):
    """Return [(id, label, expected, dir)] under root; every dir is its own git repo (index only)."""
    entry = spec["entry"]
    recipes = {
        "P0": ("genuine round-35 package", "accept", lambda d: None),
        "P1": ("8 one-word quotes", "reject", lambda d: (d / entry).write_text(mut_one_word((d / entry).read_text()))),
        "P2": ("8 copies of one quote", "reject", lambda d: (d / entry).write_text(mut_duplicates((d / entry).read_text()))),
        "P3": ("an unparsed quote row beside the genuine rows", "reject",
               lambda d: (d / entry).write_text(mut_unparsed((d / entry).read_text()))),
        "P4": ("junk teaches cells", "reject", lambda d: mut_teaches(spec)(d / spec["sources"])),
        "P5": ("stub probe printing the receipt", "reject", lambda d: stub_probe(d, spec)),
        "P6": ("untracked leftover file", "reject", "UNTRACKED"),
        "P7": ("cheapest package: one-word quotes + junk teaches + stub probe + stray file", "reject", "ALL"),
    }
    out = []
    for pid, (label, expected, mut) in recipes.items():
        d = pathlib.Path(tempfile.mkdtemp(prefix=f"k36-{pid}-", dir=root))
        subprocess.run(["git", "-C", str(d), "init", "-q"], check=True)
        top = git(d, "rev-parse", "--show-toplevel").strip()
        if pathlib.Path(top).resolve() != d.resolve():
            raise RuntimeError(f"fixture repo top {top} != {d}")
        copy_package(lane, spec, d)
        if mut == "ALL":
            (d / entry).write_text(mut_one_word((d / entry).read_text()))
            mut_teaches(spec)(d / spec["sources"])
            stub_probe(d, spec)
        elif callable(mut):
            mut(d)
        git(d, "add", "-A")  # index only: no commit, no identity
        if mut in ("UNTRACKED", "ALL"):
            (d / "plans/round35_scratch.py").write_text("# stray untracked file\n")
        out.append((pid, label, expected, d))
    return out


def d4_line(lane, spec):
    for l in (lane / spec["d4_source_file"]).read_text().splitlines():
        if l.startswith(spec["d4"]["label"]):
            return l
    return None


def d5_line(lane, spec):
    for l in (lane / spec["d5_source_file"]).read_text().splitlines():
        if l.startswith(spec["d5"]["label"]):
            return l
    return None


def build_line_fixtures(lane, spec, root):
    """Return [(id, label, expected, argv_tail)]."""
    root = pathlib.Path(root)
    d4 = d4_line(lane, spec)
    d5 = d5_line(lane, spec)
    cap = lane / spec["d5_capture_dir"]
    out = []

    def f(name, text):
        p = root / name
        p.write_text(text + "\n")
        return str(p)

    a, b = "R34C2CounterDraft.md:8", "R34MutC2Harness.md:12"
    swapped = d4.replace(a, "@@").replace(b, a).replace("@@", b)
    out.append(("L1", "D4 genuine correction line", "accept", ["d4-line", "--file", f("d4-genuine.txt", d4)]))
    out.append(("L2", "D4 line with the two file:line citations swapped", "reject",
                ["d4-line", "--file", f("d4-swapped.txt", swapped)]))
    out.append(("L3", "D4 line without the harness token", "reject",
                ["d4-line", "--file", f("d4-notoken.txt", d4.replace("SELFTEST green failed", "SELFTEST red"))]))
    out.append(("L4", "D5 genuine erratum line", "accept",
                ["d5-line", "--file", f("d5-genuine.txt", d5), "--capture-dir", str(cap)]))
    out.append(("L5", "D5 erratum saying the quote is not present", "reject",
                ["d5-line", "--file", f("d5-negated.txt", d5.replace("is present", "is not present", 1)),
                 "--capture-dir", str(cap)]))
    alt = root / "alt-captures"
    shutil.copytree(cap, alt)
    (alt / spec["d5"]["capture_name"]).write_text("<html>" + spec["d5"]["quote"] + "</html>\n")
    out.append(("L6", "D5 genuine line over an altered (quote-injected) capture", "reject",
                ["d5-line", "--file", f("d5-altcap.txt", d5), "--capture-dir", str(alt)]))
    return out


def run_gate(lane, argv_tail):
    gate = lane / GATE_REL
    if not gate.is_file():
        return None
    r = subprocess.run([sys.executable, str(gate), *argv_tail, "--spec", str(lane / SPEC_REL)],
                       capture_output=True, text=True, timeout=300)
    return r.returncode


def battery(lane, verbose=True):
    spec = load_spec(lane)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="k36-battery-"))
    fg = fr = ue = total = 0
    try:
        items = []
        for pid, label, expected, d in build_package_fixtures(lane, spec, tmp):
            items.append((pid, label, expected, ["package", "--root", str(d), "--require-clean-tree"]))
        items += build_line_fixtures(lane, spec, tmp)
        for fid, label, expected, argv in items:
            rc = run_gate(lane, argv)
            total += 1
            if rc not in (0, 1):
                ue += 1
                obs = "unevaluated"
            else:
                obs = "accept" if rc == 0 else "reject"
                if expected == "reject" and obs == "accept":
                    fg += 1
                if expected == "accept" and obs == "reject":
                    fr += 1
            if verbose:
                print(f"FIXTURE {fid} expect={expected} observed={obs} {'ok' if obs == expected else 'WRONG'} -- {label}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return total, fg, fr, ue


def legacy(lane):
    spec = load_spec(lane)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="k36-legacy-"))
    acc = 0
    n = 0
    try:
        for pid, label, expected, d in build_package_fixtures(lane, spec, tmp):
            if expected != "reject":
                continue
            n += 1
            fx = d / "plans/round35_c1_verify.py"
            r = subprocess.run([sys.executable, str(fx), "--lane", str(d)], capture_output=True, text=True)
            acc += r.returncode == 0
            print(f"LEGACY {pid} {'ACCEPTED' if r.returncode == 0 else 'rejected'} -- {label}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"LEGACY accepted={acc}/{n}")
    return 0


# ---- ledger rows -------------------------------------------------------------------------------

def r35_d1(lane):
    """Counters of record accept junk (spot-check item 1): the gate rejects every junk fixture,
    accepts the genuine one, and re-runs the real round-35 package at the tip (tip-receipt check,
    considerthese/2026-10-25.md proposal 2(c))."""
    total, fg, fr, ue = battery(lane, verbose=False)
    rc = run_gate(lane, ["package", "--root", str(lane), "--rerun", "--require-clean-tree"])
    return (total == 14 and fg == 0 and fr == 0 and ue == 0 and rc == 0,
            f"fixtures={total} false_green={fg} false_red={fr} unevaluated={ue} tip_package_rc={rc}")


def r35_d2(lane):
    """Working-tree class (round-34 D1) read over the whole lane, plus the directional D4/D5 lines."""
    left = [x for x in git(lane, "ls-files", "--others", "--exclude-standard").split("\n") if x]
    spec = load_spec(lane)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="k36-lines-"))
    try:
        bad = 0
        for fid, _label, expected, argv in build_line_fixtures(lane, spec, tmp):
            rc = run_gate(lane, argv)
            bad += rc != (0 if expected == "accept" else 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return (not left and bad == 0, f"untracked_anywhere={len(left)} line_fixtures_wrong={bad}/6")


def r35_d3(lane):
    paths = [x for x in git(lane, "ls-tree", "-r", "--name-only", BRANCH).split("\n") if x]
    n = sum(1 for p in paths if re.search(NESTED_RE, p))
    return (n == 0, f"committed_nested_wave_paths={n}")


def r35_d4(lane):
    cap = lane / TOOLATHLON
    if not cap.is_file():
        return (False, "toolathlon package capture absent")
    t = cap.read_text()
    parts = [int(m.group(1)) for pat in (r"\| isolated and callable \| (\d+) \| \d+ \|",
                                         r"\| isolated but not callable with any of the seven shapes \| (\d+) \| \d+ \|",
                                         r"\| exec failed in isolation \| (\d+) \| \d+ \|")
             for m in [re.search(pat, t)] if m]
    den = re.search(r"\| Outcome \| Count \| of (\d+) \|", t)
    if len(parts) != 3 or not den:
        return (False, "could not recount the package table")
    expr = " + ".join(map(str, parts)) + f" = {sum(parts)}"
    p = lane / "corpus/lessons/round-36.md"
    if not p.is_file():
        return (False, f"round-36 lesson absent; recount {expr} vs stated denominator {den.group(1)}")
    t36 = p.read_text()
    gate = re.search(r"^## Gate\n(.*?)(?=^## |\Z)", t36, re.S | re.M)
    errs = [l for l in (gate.group(1).splitlines() if gate else []) if l.startswith("Erratum (round 36):")]
    ok = (len(errs) == 1 and "S130" in errs[0] and expr in errs[0] and f"denominator {den.group(1)}" in errs[0]
          and sum(parts) != int(den.group(1)))
    return (ok, f"erratum_lines={len(errs)} recount={expr} stated_denominator={den.group(1)}")


CHECKS = {f.__name__: f for f in (r35_d1, r35_d2, r35_d3, r35_d4)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--legacy", action="store_true")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    if a.legacy:
        return legacy(lane)
    total, fg, fr, ue = battery(lane)
    print(f"FIXTURES total={total} false_green={fg} false_red={fr} unevaluated={ue}")
    rows = [json.loads(l) for l in (lane / LEDGER_REL).read_text().splitlines() if l.strip()]
    closed = passed = mism = 0
    for r in rows:
        fn = CHECKS.get(r.get("check"))
        if fn is None:
            ok, note = False, f"unknown check {r.get('check')!r}"
        else:
            try:
                ok, note = fn(lane)
            except Exception as e:  # a crash is an observed failure, never a pass
                ok, note = False, f"error {type(e).__name__}: {e}"
        st = r.get("status")
        agree = (st == "closed" and ok) or (st == "open" and not ok)
        closed += st == "closed"
        passed += ok
        mism += not agree
        print(f"{r['id']} status={st} observed={'pass' if ok else 'fail'} agree={'yes' if agree else 'NO'} {note}")
    print(f"rows={len(rows)} closed={closed} observed_pass={passed} mismatches={mism}")
    good = (total == 14 and fg == fr == ue == 0 and len(rows) == 4 and closed == 4 and passed == 4 and mism == 0)
    print(f"PREDICATE C1 {'pass' if good else 'fail'}")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
