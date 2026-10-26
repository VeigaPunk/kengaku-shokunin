"""Critic attack R40CritC1Counter (NOT a candidate battery40; development battery for the C1 counter).

`plans/ledger_tip.py` imports the fixture's own `plans/defect_ledger.py` and calls its `CHECKS` entries, so a
fixture's check body runs inside the tool. It can therefore read its own program text (the counter invokes the
tool at ONE fixed variant path, `sys.argv[0]`) and answer differently for the reference and for a mutant, without
touching any input file. Two fixtures kill all seven ledger mutants; neither exhibits the advertised behaviour
of any of them. Source carries no SIDECHANNEL token.
"""
raise SystemExit("NEUTRALIZED by the round-40 L1 (orchestrator host-safety ruling 2026-10-26): this attack module "
                 "wrote a git shim into the shared host PATH dir ~/.local/bin; kept as evidence text only. Re-run only "
                 "inside a sandbox with a private ~/.local/bin (bwrap --tmpfs) and SHIM_DIR under the fixture root.")

ROWS = '{"id": "r1", "status": "closed", "check": "x"}\n'

BODY = '''import hashlib, pathlib, sys

REF = "%s"


def mutated():
    try:
        txt = pathlib.Path(sys.argv[0]).read_bytes()
    except OSError:
        return False
    return hashlib.sha256(txt).hexdigest() != REF


def note(lane):
    q = pathlib.Path(lane).parent.joinpath("state.lock")
    q.write_text("touched\\n")
    return len(q.read_text())


def honest(lane):
    n = note(lane)
    return mutated(), "wrote%%d-bytes" %% n


def trap(lane):
    note(lane)
    if not mutated():
        raise SystemExit(2)
    return True, "one-ledger-row"


CHECKS = {"x": %s}
'''

SECOND = "CHECKS = {}\n"


def _repo(ctx, d, which):
    import hashlib
    ref = hashlib.sha256((ctx.lane / "plans/ledger_tip.py").read_bytes()).hexdigest()
    r = ctx.init(d / "repo")
    (r / "corpus").mkdir()
    (r / "plans").mkdir()
    (r / "corpus/defects.jsonl").write_text(ROWS)
    (r / "corpus/defects-round35.jsonl").write_text("")
    (r / "plans/defect_ledger.py").write_text(BODY % (ref, which))
    (r / "plans/round36_c1_verify.py").write_text(SECOND)
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one closed row, one check body")
    return ["--lane", str(r)]


def reject(ctx, d):
    return _repo(ctx, d, "honest")


def error(ctx, d):
    return _repo(ctx, d, "trap")


FIXTURES = [
    {"fid": "crit-l-selfread-reject", "tool": "ledger", "expect": "reject", "defects": ["NO:r1"],
     "build": reject},
    {"fid": "crit-l-selfread-error", "tool": "ledger", "expect": "error", "defects": [], "build": error},
]
