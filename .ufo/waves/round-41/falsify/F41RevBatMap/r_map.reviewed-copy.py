"""Battery41 module `r_map` (seat R41BatRcvMap): `plans/tip_receipts.py` `--list` classification.

Four behaviours the tool advertises, each targeted twice — once on the branch the frozen C1 mutant changes and
once in a differently shaped lane:

  r_map-t09-*  a receipt stem shared by two committed `plans/*.py` scripts stays unmapped (T09);
  r_map-t10-*  a receipt whose stem differs from one script only in separators maps `origin=derived` (T10);
  r_map-t11-*  a RECEIPTS-table receipt keeps `origin=table` although a derived match also exists (T11);
  r_map-t12-*  a `*probe*.log` receipt enters the population (T12).

Every build fills a lane-shaped tree (docs, `corpus/evidence/` files, several `plans/*.py` stubs, one commit) and
runs `tip_receipts.py --list`, which classifies the committed receipts and runs nothing: exit 0 every time.
`defects` is the exact class set the unmodified tool prints on that tree.
"""

EV_R = "corpus/evidence/r/foo-probe.txt"
EV_LOG = "corpus/evidence/r/foo-probe.log"
TB2 = "corpus/evidence/round35/tb2-grader-probe.txt"
PMARS = "corpus/evidence/round38/build-pmars-probe.txt"

# Docs that a real lane carries: they are read by the tool's provenance scan, never printed as receipts.
DOCS = {
    "README.md": "# fixture lane\n\nCommitted receipts under `corpus/evidence/` are re-run by the tip-receipts tool.\n",
    "SKILL.md": "# skill\n\nThe tip-receipts command re-runs a committed probe and compares its bytes.\n",
    "corpus/README.md": "# evidence\n\nOne receipt per probe run; `round*/` groups one round's records.\n",
}


def stub(name, out="X\n", rc=0):
    """A committed probe script that prints a fixed text and exits with a fixed code."""
    return (f'"""Stub probe {name}: prints the recorded text.\n\n'
            f'  python3 plans/{name}.py --lane .\n\n'
            'The receipt beside it holds exactly this output.\n"""\n'
            'import sys\n\n'
            f'sys.stdout.write({out!r})\n'
            f'raise SystemExit({rc})\n')


def lane(ctx, d, files):
    """A one-commit work tree under d/lane holding `files`."""
    root = ctx.init(d / "lane")
    for rel in sorted(files):
        ctx.write(root / rel, files[rel])
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    return root


def listing(ctx, d, files):
    """Run the tool in classify-only mode over a fresh tree under d."""
    return ["--lane", str(lane(ctx, d, files)), "--list"]


def b_shared_stem_separators(ctx, d):
    # T09: `foo-probe.txt` collides with two scripts (`foo_probe.py`, `foo.probe.py`) -> two hits, unmapped.
    files = dict(DOCS)
    files.update({EV_R: "X\n", "plans/foo_probe.py": stub("foo_probe"),
                  "plans/foo.probe.py": stub("foo.probe"), "plans/bar_probe.py": stub("bar_probe"),
                  "corpus/evidence/r/weekly-notes.md": "not a receipt\n"})
    return listing(ctx, d, files)


def b_shared_stem_case_fold(ctx, d):
    # T09 second shape: the case-fold half of the stem rule — `FooProbe.py` also hits the stem `fooprobe`.
    files = dict(DOCS)
    files.update({EV_R: "X\n", "plans/foo_probe.py": stub("foo_probe"), "plans/FooProbe.py": stub("FooProbe"),
                  "plans/unrelated.py": stub("unrelated")})
    return listing(ctx, d, files)


def b_derived_mapping(ctx, d):
    # T10: separator-only difference (`foo-probe.txt` vs `plans/foo_probe.py`) is one stem -> derived mapping.
    files = dict(DOCS)
    files.update({EV_R: "X\n", "plans/foo_probe.py": stub("foo_probe"), "plans/bar_probe.py": stub("bar_probe"),
                  "corpus/evidence/r/notes.md": "not a receipt\n"})
    return listing(ctx, d, files)


def b_derived_with_table_sibling(ctx, d):
    # T10 second class-matched shape: a table receipt beside it stays `table` while the derived one maps.
    files = dict(DOCS)
    files.update({EV_R: "X\n", "plans/foo_probe.py": stub("foo_probe"),
                  "corpus/evidence/round36/regex-log-probe.txt": "logged\n",
                  "plans/regex_log_probe.py": stub("regex_log_probe")})
    return listing(ctx, d, files)


def b_derived_deep_layout(ctx, d):
    # T10 second shape: the same derivation from a receipt nested two levels below `corpus/evidence`.
    files = dict(DOCS)
    files.update({"corpus/evidence/round41/scheduling/foo-probe.txt": "X\n",
                  "plans/foo_probe.py": stub("foo_probe")})
    return listing(ctx, d, files)


def b_table_overrides_derived(ctx, d):
    # T11: both table receipts also derive; the table is an override list, so both stay `origin=table`.
    files = dict(DOCS)
    files.update({TB2: "tb2\n", "plans/tb2_grader_probe.py": stub("tb2_grader_probe"),
                  PMARS: "pmars\n", "plans/build_pmars_probe.py": stub("build_pmars_probe")})
    return listing(ctx, d, files)


def b_table_near_stem_decoy(ctx, d):
    # T11 second shape: a `_v2` near-stem script is no match; the table receipt still prints `origin=table`.
    files = dict(DOCS)
    files.update({TB2: "tb2\n", "plans/tb2_grader_probe.py": stub("tb2_grader_probe"),
                  "plans/tb2_grader_probe_v2.py": stub("tb2_grader_probe_v2")})
    return listing(ctx, d, files)


def b_log_population(ctx, d):
    # T12: `.log` is part of the population; with no script of that stem it prints `skip reason=`.
    files = dict(DOCS)
    files.update({EV_LOG: "X\n", "plans/bar_probe.py": stub("bar_probe"),
                  "corpus/evidence/r/notes.md": "not a receipt\n"})
    return listing(ctx, d, files)


def b_log_with_table_sibling(ctx, d):
    # T12 second class-matched shape: the `.log` stays unmapped beside a table receipt and a near-stem script.
    files = dict(DOCS)
    files.update({EV_LOG: "X\n", "plans/foo_probe_v2.py": stub("foo_probe_v2"),
                  "corpus/evidence/round36/regex-log-probe.txt": "logged\n",
                  "plans/regex_log_probe.py": stub("regex_log_probe")})
    return listing(ctx, d, files)


def b_log_derived(ctx, d):
    # T12 second shape: the same `.log` receipt with one matching script, so the population entry maps.
    files = dict(DOCS)
    files.update({EV_LOG: "X\n", "plans/foo_probe.py": stub("foo_probe"), "plans/unrelated.py": stub("unrelated")})
    return listing(ctx, d, files)


FIXTURES = [
    {"fid": "r_map-t09-shared-stem-separators", "tool": "receipts", "expect": "accept",
     "defects": [f"skip:{EV_R}:no-committed-re-run-command"], "build": b_shared_stem_separators},
    {"fid": "r_map-t09-shared-stem-case-fold", "tool": "receipts", "expect": "accept",
     "defects": [f"skip:{EV_R}:no-committed-re-run-command"], "build": b_shared_stem_case_fold},
    {"fid": "r_map-t10-derived-mapping", "tool": "receipts", "expect": "accept",
     "defects": [f"map:{EV_R}:derived"], "build": b_derived_mapping},
    {"fid": "r_map-t10-derived-with-table-sibling", "tool": "receipts", "expect": "accept",
     "defects": [f"map:{EV_R}:derived",
                 "map:corpus/evidence/round36/regex-log-probe.txt:table"], "build": b_derived_with_table_sibling},
    {"fid": "r_map-t10-derived-deep-layout", "tool": "receipts", "expect": "accept",
     "defects": ["map:corpus/evidence/round41/scheduling/foo-probe.txt:derived"], "build": b_derived_deep_layout},
    {"fid": "r_map-t11-table-overrides-derived", "tool": "receipts", "expect": "accept",
     "defects": [f"map:{TB2}:table", f"map:{PMARS}:table"], "build": b_table_overrides_derived},
    {"fid": "r_map-t11-table-near-stem-decoy", "tool": "receipts", "expect": "accept",
     "defects": [f"map:{TB2}:table"], "build": b_table_near_stem_decoy},
    {"fid": "r_map-t12-log-population", "tool": "receipts", "expect": "accept",
     "defects": [f"skip:{EV_LOG}:no-committed-re-run-command"], "build": b_log_population},
    {"fid": "r_map-t12-log-with-table-sibling", "tool": "receipts", "expect": "accept",
     "defects": [f"skip:{EV_LOG}:no-committed-re-run-command",
                 "map:corpus/evidence/round36/regex-log-probe.txt:table"], "build": b_log_with_table_sibling},
    {"fid": "r_map-t12-log-derived", "tool": "receipts", "expect": "accept",
     "defects": [f"map:{EV_LOG}:derived"], "build": b_log_derived},
]
