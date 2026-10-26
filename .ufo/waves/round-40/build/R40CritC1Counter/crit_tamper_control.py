"""Critic control for the fingerprint hole: the same mid-run write, under a name the fingerprint hashes."""
import hashlib
import pathlib

BODY = '''import hashlib, pathlib, sys

REF = "%s"


def mutated():
    try:
        txt = pathlib.Path(sys.argv[0]).read_bytes()
    except OSError:
        return False
    return hashlib.sha256(txt).hexdigest() != REF


def chk(lane):
    pathlib.Path(lane).parent.joinpath("state.log").write_text("touched\\n")
    return False, "wrote-under-a-hashed-name"


CHECKS = {"x": chk}
'''


def build(ctx, d):
    ref = hashlib.sha256((ctx.lane / "plans/ledger_tip.py").read_bytes()).hexdigest()
    r = ctx.init(d / "repo")
    (r / "corpus").mkdir()
    (r / "plans").mkdir()
    (r / "corpus/defects.jsonl").write_text('{"id": "r1", "status": "closed", "check": "x"}\n')
    (r / "corpus/defects-round35.jsonl").write_text("")
    (r / "plans/defect_ledger.py").write_text(BODY % ref)
    (r / "plans/round36_c1_verify.py").write_text("CHECKS = {}\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "control")
    return ["--lane", str(r)]


FIXTURES = [{"fid": "crit-tamper-log", "tool": "ledger", "expect": "reject", "defects": ["NO:r1"],
             "build": build}]
