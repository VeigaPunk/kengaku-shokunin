#!/usr/bin/env python3
"""F42MutBattery driver: one single-edit mutant per battery42 fixture + removal probes,
each measured by the REAL counter (plans/round42_c1_verify.py) under the seat bwrap envelope."""
import pathlib, re, shutil, subprocess, sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/F42MutBattery")
LANE = S / "lane"
BAT = LANE / "plans" / "battery42"
COUNTER = LANE / "plans" / "round42_c1_verify.py"
WRAPPER = S / "receipt_run.sh"
WORK = S / "c1work"
REPORT = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-42/falsify/F42MutBattery")
MODULES = ["a_class.py", "a_route.py", "a_row.py", "o_clause.py", "o_scan.py"]
SIDECHANNEL = ("/proc", "ppid", "cmdline", "psutil", "environ", "fsmonitor", "hookspath", "filter.",
               "gitattributes", "core.", "alias.", "setsid", "daemon", "fork", "nohup", "socket",
               "/home/", ".local", "__file__", "inspect", "importlib", "sys.path", "ctypes", "chmod",
               "witness", "settrace", "/run")

# (tag, fid, kind, [(module, old, new-or-None-delete-line), ...], prediction)
CASES = [
 ("C01", "a_class-x6-sibling-digest", "cap-byte", [("a_class.py", 'b"capture A: the capture this row names\\n"', 'b"capture A: the capture this row nameZ\\n"')], "unnoticed: token is capture B's digest; A's bytes unreferenced"),
 ("C02", "a_class-x6-stale-manifest", "drop-commit", [("a_class.py", '    landed(ctx, r, "fixture: the pinned artefact and the sibling capture, both green")\n', None)], "unnoticed: commit 2 add -A absorbs commit 1, tree identical"),
 ("C03", "a_class-x7-fabricated-token", "cap-byte", [("a_class.py", 'b"the capture this row names\\n"', 'b"the capture this row nameZ\\n"')], "unnoticed: token is fabricated regardless of capture bytes"),
 ("C04", "a_class-x7-provenance-row", "drop-commit", [("a_class.py", '    landed(ctx, r, "fixture: the capture and one green row")\n', None)], "unnoticed: commit 2 add -A absorbs commit 1, tree identical"),
 ("C05", "a_class-x14-uppercase-token", "cap-byte", [("a_class.py", 'b"the capture this erratum row names\\n"', 'b"the capture this erratum row nameZ\\n"')], "unnoticed: row anchor and erratum correction both derive from the body literal"),
 ("C06", "a_class-x14-two-errata", "drop-commit", [("a_class.py", '    landed(ctx, r, "fixture: two rows, the first exempted by a clean erratum")\n', None)], "unnoticed: commit 2 add -A absorbs commit 1, tree identical"),
 ("C07", "a_route-x1-provenance-table", "cap-byte", [("a_route.py", 'b"capture committed beside its provenance table\\n"', 'b"capture committed beside its provenance tablZ\\n"')], "unnoticed: SHA256SUMS, provenance digest column and row anchor all derive from body"),
 ("C08", "a_route-x1-two-row-registry", "drop-commit", [("a_route.py", '    commit(ctx, repo, "fixture: capture batch")\n', None)], "unnoticed: rows commit add -A absorbs the batch commit, tree identical"),
 ("C09", "a_route-x3-provenance-url", "cap-byte", [("a_route.py", 'b"pinned upstream file, capture beside the table\\n"', 'b"pinned upstream file, capture beside the tablZ\\n"')], "unnoticed: digest derived from body everywhere"),
 ("C10", "a_route-x3-blob-url", "cap-byte", [("a_route.py", 'b"pinned grader bytes\\n"', 'b"pinned grader byteZ\\n"')], "unnoticed: digest derived from body everywhere"),
 ("C11", "a_route-x12-slashless-toml", "cap-byte", [("a_route.py", 'b"grader-owned test file\\n"', 'b"grader-owned test filZ\\n"')], "unnoticed: digest derived from body everywhere"),
 ("C12", "a_route-x12-two-tomls", "cap-byte", [("a_route.py", 'b"lookup circuit shipped as data\\n"', 'b"lookup circuit shipped as datZ\\n"')], "unnoticed: digest derived from body everywhere"),
 ("C13", "a_row-x9-short-no-token", "cap-byte", [("a_row.py", 'b"census fixture note\\n"', 'b"census fixture notZ\\n"')], "unnoticed: row carries no token; cell-count defect insensitive to capture bytes"),
 ("C14", "a_row-x9-registry-short-valid", "cap-byte", [("a_row.py", 'b"alpha capture, six-row registry\\n"', 'b"alpha capture, six-row registrZ\\n"')], "unnoticed: rows derive their tokens from dig(body), stays consistent"),
 ("C15", "a_row-x13-staged-capture", "cap-byte-staged", [("a_row.py", 'b"alpha capture, re-captured view\\n"', 'b"alpha capture, re-captured viewZ\\n"')], "unnoticed: HEAD verdict unchanged; mutant still resolves via index"),
 ("C16", "a_row-x13-url-staged", "cap-byte-staged", [("a_row.py", 'b"graded test file, re-captured view\\n"', 'b"graded test file, re-captured viewZ\\n"')], "unnoticed: HEAD verdict unchanged; mutant still resolves via index"),
 ("C17", "a_row-x15-sibling-digest", "cap-byte", [("a_row.py", 'b"row A capture\\n"', 'b"row A capturZ\\n"')], "unnoticed: token uncommitted regardless; erratum correction is fx-b's digest"),
 ("C18", "a_row-x15-manifest-sibling", "drop-commit", [("a_row.py", '    commit(ctx, r, "rows")\n', None)], "unnoticed: erratum commit add -A absorbs the rows commit, tree identical"),
 ("C19", "o_clause-freeze-single", "claims-byte", [("o_clause.py", r'Probe frozen before its first run.\n', r'Probe frozen before its first runX\n')], "unnoticed: gate reads commit structure, never claims content"),
 ("C20", "o_clause-freeze-pair-edited-after", "drop-commit", [("o_clause.py", '    commit(ctx, repo, "scaffold the lane")\n', None)], "unnoticed: freeze commit absorbs scaffold, tree identical, clause 1 unchanged"),
 ("C21", "o_clause-receipt-withdrawn", "drop-commit", [("o_clause.py", '    ctx.git(repo, "rm", "-q", PROBE9)\n    ctx.git(repo, "commit", "-q", "-m", "withdraw the early run")\n', None)], "unnoticed: freeze tree keeps receipt v1 so clause 1 fires instead of clause 2, rc still 1"),
 ("C22", "o_clause-receipt-side-line", "drop-commit", [("o_clause.py", '    ctx.git(repo, "rm", "-q", "evidence/probe.txt")\n    ctx.git(repo, "commit", "-q", "-m", "withdraw the early run")\n', None)], "unnoticed: freeze tree keeps receipt v1 so clause 1 fires instead of clause 2, rc still 1"),
 ("C23", "o_clause-clean-order", "claims-byte", [("o_clause.py", r'Freeze precedes the recorded run.\n', r'Freeze precedes the recorded runX\n')], "unnoticed: gate reads commit structure, never claims content"),
 ("C24", "o_scan-xo5-post-receipt-verdicts", "drop-commit", [("o_scan.py", '    _later(ctx, r, f"{DIR_42}/rerun-verdicts.txt",\n           "# verdicts written after the receipt commit\\n"\n           "P10 ok fresh probe output is byte-equal to the receipt\\n",\n           "rerun verdicts")\n', None)], "unnoticed: reference stops at the receipt; XO5 still killed by the amended-blob fixture"),
 ("C25", "o_scan-xo5-amended-claims-blob", "drop-commit", [("o_scan.py", '    _later(ctx, r, rel, HONEST + "gate: P10 ok rerun exit=0\\n", "amend the do-nothing control")\n', None)], "unnoticed: freeze-time blob is clean; XO5 still killed by the post-receipt fixture"),
 ("C26", "o_scan-xo6-pass-verdict-row", "blob-byte", [("o_scan.py", 'P10 PASS probe executed twice', 'P10 PASs probe executed twice')], "unnoticed: neither reference nor widened alternation matches PASs"),
 ("C27", "o_scan-xo6-echoed-pass-row", "blob-byte", [("o_scan.py", 'gate: P10 PASS receipt unreadable', 'gate: P10 PASs receipt unreadable')], "unnoticed: neither reference nor widened alternation matches PASs"),
 ("C28", "o_scan-xo7-timeout-rows", "blob-byte", [("o_scan.py", 'CASE lookup-28 observed=timeout rc=timeout', 'CASE lookup-28 observed=timeouT rc=timeout')], "unnoticed: reference matches any observed value; narrowed mutant still misses timeouT"),
 ("C29", "o_scan-xo7-skipped-row-r38", "blob-byte", [("o_scan.py", 'CASE c7 observed=skipped', 'CASE c7 observed=skippEd')], "unnoticed: reference matches any observed value; narrowed mutant still misses skippEd"),
 # pointed probes: the decisive-commit drops an honest reviewer would try (predicted CAUGHT via wrong)
 ("P02", "a_class-x6-stale-manifest", "drop-decisive-commit", [("a_class.py", '    landed(ctx, r, "fixture: one row anchored on the sibling manifest\'s stale digest")\n', None)], "caught: bad row never lands, rc=0 vs declared reject"),
 ("P04", "a_class-x7-provenance-row", "drop-decisive-commit", [("a_class.py", '    landed(ctx, r, "fixture: a made-up digest and a resolvable abbreviation")\n', None)], "caught: defective row never lands, rc=0 vs declared reject"),
 ("P06", "a_class-x14-two-errata", "drop-decisive-commit", [("a_class.py", '    landed(ctx, r, "fixture: a second erratum carrying an uppercase uncommitted token")\n', None)], "caught: wrong-case erratum never lands, rc=0 vs declared reject"),
 ("P26", "o_scan-xo6-pass-verdict-row", "blob-byte-excuse", [("o_scan.py", '"P10 DEFECT receipt unreadable\\n"', '"P10 DEFECT receipt unreadablE\\n"')], "caught: excuse no longer matches, gate line becomes a hit, rc=1 vs declared accept"),
 # pair removals: joint necessity of the two-fixture-per-mutant design
 ("PR1", "a_route-x1-provenance-table + a_route-x1-two-row-registry", "remove-pair", [("a_route.py", '"fid": "a_route-x1-provenance-table"', None), ("a_route.py", '"fid": "a_route-x1-two-row-registry"', None)], "X1 SURVIVED (no hits left)"),
 ("PR2", "o_scan-xo5-post-receipt-verdicts + o_scan-xo5-amended-claims-blob", "remove-pair", [("o_scan.py", '"fid": "o_scan-xo5-post-receipt-verdicts"', None), ("o_scan.py", '"fid": "o_scan-xo5-amended-claims-blob"', None)], "XO5 SURVIVED (no hits left)"),
 ("PR3", "a_class-x6-sibling-digest + a_class-x6-stale-manifest", "remove-pair", [("a_class.py", '"fid": "a_class-x6-sibling-digest"', None), ("a_class.py", '"fid": "a_class-x6-stale-manifest"', None)], "X6 SURVIVED (no hits left)"),
 ("P13", "a_row-x9-short-no-token", "drop-only-commit", [("a_row.py", '"mined", "2026-10-26", "180d", "corpus/knowledge/fixture.md"))\n    commit(ctx, r)\n', '"mined", "2026-10-26", "180d", "corpus/knowledge/fixture.md"))\n')], "rows live in the worktree so the defect may survive an unborn HEAD"),
 ("RC1", "o_clause (all 5 fixtures, one shared literal)", "receipt-byte", [("o_clause.py", 'RECEIPT_BODY = "cases=16 ', 'RECEIPT_BODY = "cases=15 ')], "unnoticed: the gate never reads receipt bytes"),
 ("RC2", "o_scan (all 6 fixtures, one shared literal)", "receipt-byte", [("o_scan.py", '"cases=16 observed_pass=7 observed_fail=9 mismatches=0\\n"', '"cases=15 observed_pass=7 observed_fail=9 mismatches=0\\n"')], "unnoticed: the gate never reads receipt bytes"),
]

FIXTURE_ORDER = [c[1] for c in CASES[:29]]  # C01..C29 fids in battery order


def module_of(fid):
    for m in MODULES:
        if f'"{fid}"' in (BAT / m).read_text():
            return m
    raise AssertionError(fid)


# F01..F29: flip expect on every fixture (declaration channel, predicted always caught)
FLIPS = [(f"F{i+1:02d}", fid, "flip-expect",
          [(module_of(fid), f"FLIP:{fid}", None)], "caught: EXPECT_RC mismatch -> wrong=1")
         for i, fid in enumerate(FIXTURE_ORDER)]
# R01..R29: remove one fixture, re-run the counter, compare verdict lines
REMOVALS = [(f"R{i+1:02d}", fid, "remove-fixture",
             [(module_of(fid), f'"fid": "{fid}"', None)], "redundant iff no mutant line changes")
            for i, fid in enumerate(FIXTURE_ORDER)]
CASES = CASES + FLIPS + REMOVALS


def fixture_line(text, fid):
    lines = [l for l in text.splitlines(keepends=True) if f'"fid": "{fid}"' in l]
    assert len(lines) == 1, (fid, len(lines))
    return lines[0]


def fixture_entry(text, fid):
    """The fixture's full dict entry: from its fid line through the first line containing '},'.
    Handles both one-line dicts (a_class/a_row/o_clause) and two-line dicts (a_route/o_scan)."""
    lines = text.splitlines(keepends=True)
    idx = [i for i, l in enumerate(lines) if f'"fid": "{fid}"' in l]
    assert len(idx) == 1, (fid, len(idx))
    j = idx[0]
    while "}," not in lines[j]:
        j += 1
        assert j < len(lines), fid
    return "".join(lines[idx[0]:j + 1])


def flip_expect(line):
    if '"expect": "reject"' in line:
        return line.replace('"expect": "reject"', '"expect": "accept"')
    assert '"expect": "accept"' in line, line
    return line.replace('"expect": "accept"', '"expect": "reject"')


def make_battery(tag, edits):
    d = S / "cases" / tag
    if d.exists():
        shutil.rmtree(d)
    bdir = d / "battery42"
    bdir.mkdir(parents=True)
    for m in MODULES:
        text = (BAT / m).read_text()
        for mod, old, new in edits:
            if mod != m:
                continue
            if new is None:
                if old.startswith("FLIP:"):            # flip expect inside the fixture's dict line
                    fid = old[5:]
                    line = fixture_line(text, fid)
                    text = text.replace(line, flip_expect(line), 1)
                elif old.startswith('"fid": '):        # removal: delete the fixture's whole dict entry
                    fid = re.search(r'"fid": "([^"]+)"', old).group(1)
                    text = text.replace(fixture_entry(text, fid), "", 1)
                else:                                   # drop-commit: delete the exact line/block
                    assert text.count(old) == 1, (tag, m, old[:60], text.count(old))
                    text = text.replace(old, "", 1)
            else:
                assert text.count(old) == 1, (tag, m, old[:60], text.count(old))
                text = text.replace(old, new, 1)
        toks = [t for t in SIDECHANNEL if t in text.lower()]
        assert not toks, (tag, m, toks)
        (bdir / m).write_text(text)
    return bdir


def run_case(tag, bdir):
    r = subprocess.run([str(WRAPPER), tag, "python3", str(COUNTER), "--lane", str(LANE),
                        "--battery-dir", str(bdir), "--work", str(WORK), "--jobs", "16"],
                       capture_output=True, text=True)
    rec = REPORT / f"receipt-{tag}.txt"
    out = rec.read_text() if rec.exists() else ""
    return r.returncode, out


BY0 = {}  # baseline killer map, filled from receipt-baseline.txt


def parse(out):
    wrong = [l for l in out.splitlines() if l.startswith("FIXTURE ") and l.endswith(" WRONG")]
    surv = [l for l in out.splitlines() if " SURVIVED " in l]
    unattr = [l for l in out.splitlines() if " UNATTRIBUTED " in l]
    null = [l for l in out.splitlines() if l.startswith("NULL ")]
    side = [l for l in out.splitlines() if l.startswith("SIDECHANNEL ")]
    setup = [l for l in out.splitlines() if l.startswith("SETUP ")]
    battery = next((l for l in out.splitlines() if l.startswith("BATTERY ")), "")
    mutants = next((l for l in out.splitlines() if l.startswith("MUTANTS ")), "")
    by = dict(re.findall(r"MUTANT (\S+) \S+ \S+ killed by=(\S+)", out))
    exitm = re.search(r"^EXIT (\d+)", out, re.M)
    return dict(wrong=wrong, surv=surv, unattr=unattr, null=null, side=side, setup=setup,
                battery=battery, mutants=mutants, by=by,
                exit=int(exitm.group(1)) if exitm else -1)


def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    base_out = (REPORT / "receipt-baseline.txt").read_text()
    global BY0
    BY0 = parse(base_out)["by"]
    tsv = S / "results.tsv"
    if lo == 0:
        tsv.write_text("tag\tfid\tkind\texit\twrong\tsurvived\tunattributed\tby_changed\tbattery\tmutants\n")
    for tag, fid, kind, edits, pred in CASES[lo:hi]:
        bdir = make_battery(tag, edits)
        rc, out = run_case(tag, bdir)
        p = parse(out)
        bych = ";".join(f"{m}:{BY0.get(m)}->{b}" for m, b in sorted(p["by"].items()) if BY0.get(m) != b)
        row = [tag, fid, kind, str(p["exit"]), str(len(p["wrong"])),
               ";".join(l.split()[1] for l in p["surv"]) or "-",
               ";".join(l.split()[1] for l in p["unattr"]) or "-",
               bych or "-", p["battery"], p["mutants"]]
        with open(tsv, "a") as fh:
            fh.write("\t".join(row) + "\n")
        print(f"{tag} {fid} exit={p['exit']} wrong={len(p['wrong'])} surv={len(p['surv'])} "
              f"unattr={len(p['unattr'])} setup={len(p['setup'])} by_changed={bych or '-'}")


if __name__ == "__main__":
    main()
