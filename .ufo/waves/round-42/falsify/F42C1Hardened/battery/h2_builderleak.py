"""F42C1Hardened hostile module `h2_builderleak` — repair R2 (R42SentinelCounter V2).

Vector: the frozen `build_battery` writes the whole counter to `<scratch root>/bin/builder.py`
(round42_c1_verify.py:475-476) and the build sandbox hides only the lane (:489), so a battery module can
read the 14 `old -> new` pairs, the `SIDECHANNEL` list and the pin table at build time, from inside the
sandbox, and author itself against them.

Observable: the build child reads its own entry point (`sys.argv[0]`, i.e. the builder), every other `.py`
beside it, and every `.py` under the scratch root it can reach, then puts the finding in the fixture id,
which the counter prints:

  frozen counter  FIXTURE h2-builder-LEAK-35983b-builder.py:35972 …  (counter source readable: vector green)
  hardened copy   FIXTURE h2-builder-CLEAN-3908b …                   (minimal builder, no table: vector red)

`35983b` is the builder file's byte size — the frozen counter itself, written whole. The `builder.py:35972`
suffix is the decoded character length of that source (the docstring carries six non-ASCII characters). `3908b`
is the generated Ctx/load/build_module_child builder, which carries no `MUTANTS` table, no `SIDECHANNEL` list
and no pins.
"""

import pathlib
import sys

M42 = ".ufo/waves/round-42/claims"
CLAIMS = "plans/round-42-claims.md"
PROBE = "corpus/evidence/round42/fibsqrt-probe.txt"
RECEIPT_BODY = "cases=16 observed_pass=7 observed_fail=9 mismatches=0\nregrade cases=16 differ=0\n"


def commit(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


def clean_history(ctx, d):
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS, "# round 42 - frozen claims\n\nThe run is recorded after the freeze.\n")
    ctx.write(repo / M42 / "control.txt", "P10 DEFECT receipt unreadable\n")
    commit(ctx, repo, "freeze")
    ctx.write(repo / PROBE, RECEIPT_BODY)
    commit(ctx, repo, "first recorded run")
    return repo


def scan(paths):
    hits = []
    for p in paths:
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        if "MUTANTS = [" in text or "SIDECHANNEL = (" in text:
            hits.append(f"{p.name}:{len(text)}")
    return hits


def build(ctx, d):
    here = pathlib.Path(sys.argv[0])
    try:
        size = len(here.read_bytes())
    except OSError:
        size = -1
    candidates = [here]
    try:
        candidates += sorted(p for p in here.parent.glob("*.py") if p != here)
    except OSError:
        pass
    if len(here.parents) >= 3:      # a builder staged on the runtime tmpfs has only one parent above it
        root = here.parents[1]
        if root.is_dir() and len(list(root.iterdir())) < 64:
            found = sorted(root.rglob("*.py"))
            if len(found) < 256:
                candidates += found
    hits = scan(dict.fromkeys(candidates))
    FIXTURES[0]["fid"] = ("h2-builder-" + ("LEAK" if hits else "CLEAN") + f"-{size}b"
                          + (("-" + hits[0]) if hits else ""))
    repo = clean_history(ctx, d)
    return ["--lane", str(repo), "--claims", CLAIMS, "--receipt", PROBE]


FIXTURES = [
    {"fid": "h2-builder-placeholder", "tool": "order", "expect": "accept", "defects": [], "build": build},
]
