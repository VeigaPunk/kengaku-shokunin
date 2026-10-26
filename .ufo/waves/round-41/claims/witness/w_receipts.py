"""Pre-freeze witnesses for the round-41 tip-receipts mutants (L1 KengakuR41). Not the battery."""

EV = "corpus/evidence/r/foo-probe.txt"


def probe(name, out, rc=0, runas="python3"):
    return (f'"""Stub probe.\n\n  {runas} plans/{name}.py --lane .\n"""\nimport sys\n'
            f"sys.stdout.write({out!r})\nsys.exit({rc})\n")


def lane(ctx, d, files, sub="lane"):
    root = ctx.init(d / sub)
    for rel, text in files.items():
        ctx.write(root / rel, text)
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    return root


def run(lane_dir, *extra):
    return ["--lane", str(lane_dir), "--work", "{WORK}", *extra]


def b_no_evidence(ctx, d):
    return run(lane(ctx, d, {"README.md": "x\n"}))


def b_exit3(ctx, d):
    return run(lane(ctx, d, {EV: "X\n", "plans/foo_probe.py": probe("foo_probe", "X\n", 3)}))


def b_temp_paths(ctx, d):
    rel = "corpus/evidence/round36/regex-log-probe-first-run.txt"
    return run(lane(ctx, d, {rel: "path /tmp/tmpAAAAAA11/x\n",
                             "plans/regex_log_probe.py": probe("regex_log_probe", "path /tmp/tmpBBBBBB22/x\n")}))


def b_tamper_unknown(ctx, d):
    return run(lane(ctx, d, {EV: "X\n", "plans/foo_probe.py": probe("foo_probe", "X\n")}),
               "--tamper", "corpus/evidence/nope.txt")


def b_empty(ctx, d):
    return run(lane(ctx, d, {EV: "", "plans/foo_probe.py": probe("foo_probe", "")}))


def b_subdir(ctx, d):
    root = lane(ctx, d, {"sub/corpus/evidence/note.md": "x\n", "README.md": "x\n"}, sub="repo")
    return run(root / "sub")


def b_uv(ctx, d):
    return run(lane(ctx, d, {EV: "X\n", "plans/foo_probe.py": probe("foo_probe", "X\n",
                                                                   runas="uv run --no-project python3")}))


def b_two_scripts(ctx, d):
    return ["--lane", str(lane(ctx, d, {EV: "X\n", "plans/foo_probe.py": probe("foo_probe", "X\n"),
                                        "plans/fooprobe.py": probe("fooprobe", "X\n")})), "--list"]


def b_derived(ctx, d):
    return ["--lane", str(lane(ctx, d, {EV: "X\n", "plans/foo_probe.py": probe("foo_probe", "X\n")})), "--list"]


def b_table(ctx, d):
    rel = "corpus/evidence/round35/tb2-grader-probe.txt"
    return ["--lane", str(lane(ctx, d, {rel: "X\n", "plans/tb2_grader_probe.py": probe("tb2_grader_probe", "X\n")})),
            "--list"]


def b_log(ctx, d):
    return ["--lane", str(lane(ctx, d, {"corpus/evidence/r/foo-probe.log": "X\n"})), "--list"]


def b_control(ctx, d):
    return run(lane(ctx, d, {EV: "X\n", "plans/foo_probe.py": probe("foo_probe", "X\n")}))


FIXTURES = [
    {"fid": "w-t02-no-evidence", "tool": "receipts", "expect": "error", "defects": [], "build": b_no_evidence},
    {"fid": "w-t03-probe-exit-3", "tool": "receipts", "expect": "reject", "defects": [f"differ:{EV}"],
     "build": b_exit3},
    {"fid": "w-t04-temp-paths-masked", "tool": "receipts", "expect": "accept",
     "defects": ["skip:corpus/evidence/round36/regex-log-probe-first-run.txt:"
                 "declared-nonreproducible-absolute-scratch-paths"], "build": b_temp_paths},
    {"fid": "w-t05-tamper-unknown", "tool": "receipts", "expect": "error", "defects": [], "build": b_tamper_unknown},
    {"fid": "w-t06-empty-receipt-control", "tool": "receipts", "expect": "reject",
     "defects": [f"equal:{EV}", "control:unavailable"], "build": b_empty},
    {"fid": "w-t07-lane-is-subdir", "tool": "receipts", "expect": "error", "defects": [], "build": b_subdir},
    {"fid": "w-t08-uv-absent", "tool": "receipts", "expect": "accept", "defects": [f"skip:{EV}:dependency-missing"],
     "build": b_uv},
    {"fid": "w-t09-two-scripts-one-stem", "tool": "receipts", "expect": "accept",
     "defects": [f"skip:{EV}:no-committed-re-run-command"], "build": b_two_scripts},
    {"fid": "w-t10-derived-list", "tool": "receipts", "expect": "accept", "defects": [f"map:{EV}:derived"],
     "build": b_derived},
    {"fid": "w-t11-table-over-derived", "tool": "receipts", "expect": "accept",
     "defects": ["map:corpus/evidence/round35/tb2-grader-probe.txt:table"], "build": b_table},
    {"fid": "w-t12-log-receipt", "tool": "receipts", "expect": "accept",
     "defects": ["skip:corpus/evidence/r/foo-probe.log:no-committed-re-run-command"], "build": b_log},
    {"fid": "w-t13-control-differ", "tool": "receipts", "expect": "accept",
     "defects": [f"equal:{EV}", "control:differ"], "build": b_control},
]
