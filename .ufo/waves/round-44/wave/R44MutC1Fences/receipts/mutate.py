#!/usr/bin/env python3
"""R44MutC1Fences: generate single-edit mutants of the round-44 C1 counter's NEW guard code.

Base: $S/base/round44_c1_verify.py (byte-identical to the frozen plans/round44_c1_verify.py).
Each mutant: exactly one replacement, asserted to occur exactly once, written to $S/mut/<ID>.py.
The frozen lane file is never touched."""
import hashlib
import pathlib
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r44/R44MutC1Fences")
BASE = (S / "base" / "round44_c1_verify.py").read_text()

MUTANTS = [
    # pin_git (F4/F6 wrapper)
    ("PG1", "capture_output=True, text=True, env=env,\n                           stdin=subprocess.DEVNULL, timeout=GIT_TIMEOUT)",
     "capture_output=True, text=True, env=env,\n                           stdin=subprocess.DEVNULL)",
     "pin_git: drop the 30 s timeout"),
    ("PG2", 'env = {**PIN_CHECK_ENV, "GIT_CEILING_DIRECTORIES": str(ceiling)}', "env = dict(PIN_CHECK_ENV)",
     "pin_git: drop GIT_CEILING_DIRECTORIES"),
    ("PG3", "env=env,\n                           stdin=subprocess.DEVNULL, timeout=GIT_TIMEOUT)",
     "env=env,\n                           stdin=None, timeout=GIT_TIMEOUT)",
     "pin_git: stdin=None (inherit) instead of DEVNULL"),
    # constants of the new block
    ("GT1", "GIT_TIMEOUT = 30", "GIT_TIMEOUT = 0", "GIT_TIMEOUT 30 -> 0 (every pin_git call times out)"),
    ("OS1", 'ORDER_SHAPE = ("--lane", "--claims", "--receipt")', 'ORDER_SHAPE = ("--lane", "--receipt", "--claims")',
     "ORDER_SHAPE pair order swapped"),
    ("AO1", 'ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True, "--verbose": False}',
     'ANCHOR_OPTS = {"--evidence-ref": True, "--verbose": False}', "ANCHOR_OPTS drops --lane"),
    # repo_breach
    ("RB1", '        if ".git" in files:', "        if False:",
     "repo_breach: .git FILE (gitdir redirect) check disabled"),
    ("RB2", "if seen_entries > 200000:", "if False:",
     "repo_breach: F2 visited-entry bound disabled"),
    ("RB3", 'if (gd / "objects" / "info" / "alternates").exists():', "if False:",
     "repo_breach: alternates refusal disabled"),
    ("RB4", "if inc[0] == 0 and inc[1]:", "if inc[0] == 0 and False:",
     "repo_breach: config include refusal disabled"),
    ("RB5", 'ok = p == repo if what.endswith("toplevel") else p.is_relative_to(d)', "ok = True",
     "repo_breach: rev-parse containment (toplevel==repo, gitdir in d) disabled"),
    ("RB6", "        if val:\n", "        if False and val:\n",
     "repo_breach: core.worktree value check disabled"),
    # argv_shape_breach
    ("AS1", "if len(argv) != 6 or tuple(argv[0::2]) != ORDER_SHAPE:", "if False:",
     "argv_shape: order contract shape check disabled"),
    ("AS2", "if t not in ANCHOR_OPTS:", "if False:",
     "argv_shape: anchor exact-option token check disabled"),
    ("AS3", "k += 2 if ANCHOR_OPTS[t] else 1", "k += 1",
     "argv_shape: value-taking option consumes 1 token instead of 2"),
    # lane_breach
    ("LB1", "if r.returncode == 0 and not pathlib.Path(r.stdout.strip()).resolve().is_relative_to(d):", "if False:",
     "lane_breach: --lane repo containment check disabled"),
    ("LB2", "env=PIN_CHECK_ENV,\n                               stdin=subprocess.DEVNULL, timeout=GIT_TIMEOUT)",
     "env=PIN_CHECK_ENV,\n                               stdin=subprocess.DEVNULL)",
     "lane_breach: drop the 30 s timeout"),
    # order_argv_breach
    ("OA1", 'if got[0] == 0 and got[1] != "blob":', 'if False and got[0] == 0 and got[1] != "blob":',
     "order_argv: HEAD blob check disabled"),
]


def main() -> int:
    ok = True
    for mid, old, new, why in MUTANTS:
        n = BASE.count(old)
        if n != 1:
            print(f"{mid}: OLD occurs {n}x, expected 1 -- SKIP")
            ok = False
            continue
        out = S / "mut" / f"{mid}.py"
        text = BASE.replace(old, new, 1)
        out.write_text(text)
        digest = hashlib.sha256(out.read_bytes()).hexdigest()
        print(f"{mid}: written sha256={digest[:16]}  ({why})")
    ref = S / "mut" / "REF.py"
    ref.write_text(BASE)
    print(f"REF: pristine copy sha256={hashlib.sha256(BASE.encode()).hexdigest()[:16]}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
