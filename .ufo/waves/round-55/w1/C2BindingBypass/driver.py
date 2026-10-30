#!/usr/bin/env python3
"""Fixture driver for seat C2BindingBypass (kengaku r55 w1).

Builds five small git fixture lanes and runs the FROZEN r54 entry-truth counter
(plans/round54_c2_entrytruth.py, loaded read-only from the lane) over each, to
observe which laundering routes the r54 legs catch/miss and to reason precisely
about the frozen R55-C2 L1-L4 text. The r55 counter (plans/round55_c2_entryargv.py)
does not exist yet; the L1 replays these fixtures against it at integration.

Run:  python3 driver.py [--only NAME]
Env:  KENGAKU_POISON=1  -> poisons F1 (declared-green row only passes under poison)
      PATH=<shimdir>:$PATH  SHIM_LIB=<dir>  -> poisons F6 (interpreter + import shadow)
"""
from __future__ import annotations

import importlib.util
import json
import os
import py_compile
import re
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r55/C2BindingBypass")
FIX = S / "fixtures"
REC = S / "receipts"
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
R54 = LANE / "plans" / "round54_c2_entrytruth.py"

HEAD_ROW = ["## Gate/probe registry", "",
            "| name | kind | entry | verdict map | self-test | pinned | scope | owner |",
            "|---|---|---|---|---|---|---|---|"]


def load_counter():
    spec = importlib.util.spec_from_file_location("r54entry", R54)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def mkrepo(root: Path) -> Path:
    if root.exists():
        import shutil
        shutil.rmtree(root)
    (root / "plans").mkdir(parents=True)
    return root


def commit(root: Path):
    def git(*a):
        subprocess.run(["git", "-C", str(root), *a], check=True, capture_output=True)
    git("init", "-q")
    top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True)
    assert top.stdout.strip() == str(root), f"toplevel guard: {top.stdout.strip()} != {root}"
    git("add", "-A")
    git("-c", "user.name=f", "-c", "user.email=f@f", "commit", "-qm", "fixture")


def run_counter(mod, root: Path, tag: str, name: str, env=None):
    """Run the frozen r54 counter's evaluate() in-process under an optional caller env."""
    work = S / "work" / f"{name}-{tag}"
    if env is None:
        rc, lines = mod.evaluate(root, root, work, 1, 60, dry=False)
    else:
        saved = dict(os.environ)
        try:
            os.environ.clear(); os.environ.update(env)
            rc, lines = mod.evaluate(root, root, work, 1, 60, dry=False)
        finally:
            os.environ.clear(); os.environ.update(saved)
    out = [f"FIXTURE {name} run={tag}", f"COUNTER EXIT {rc}", *lines, ""]
    (REC / f"{name}.{tag}.txt").write_text("\n".join(out))
    return rc, lines


def truth(root: Path, argv, tag, name, env_extra=None):
    env = dict(os.environ)
    env.pop("KENGAKU_POISON", None)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(argv, cwd=root, capture_output=True, text=True, env=env)
    with open(REC / f"{name}.{tag}.txt", "a") as f:
        f.write(f"NEUTRAL-TRUTH {json.dumps(argv)} exit={p.returncode}\n")
        f.write((p.stdout or "") + (p.stderr or "") + "\n")
    return p.returncode


# --------------------------------------------------------------------------- F1 env poison
ENVGATE = """#!/usr/bin/env python3
import os, sys
if os.environ.get("KENGAKU_POISON") == "1":
    print("env-gate: poisoned path ran green")
    sys.exit(0)
print("entry failed: env-gate is red in a neutral environment")
sys.exit(7)
"""

def f1(mod, tag):
    root = mkrepo(FIX / "f1-envpoison")
    (root / "plans" / "envgate.py").write_text(ENVGATE)
    row = "| `env-gate` | gate | `python3 plans/envgate.py` | `0` ok · `1` bad | none | none | none | kengaku |"
    (root / "SKILL.md").write_text("\n".join(HEAD_ROW + [row]) + "\n")
    poisoned = os.environ.get("KENGAKU_POISON") == "1"
    # FIXED declaration (green/exit 0) in both runs: only the caller env changes.
    # neutral run  -> counter sees the truth (exit 7) and flags LAUNDERED (safe direction)
    # poisoned run -> counter sees exit 0, matches the declaration, PREDICATE pass,
    #                 while the neutral-truth entry is exit 7 (kill shape).
    decl_exit, decl_state = 0, "green"
    led = {"schema": "r54-entrytruth-v1", "rows": {"env-gate": {
        "entry_argv": ["python3", "plans/envgate.py"], "entry_exit": decl_exit,
        "entry_state": decl_state, "timeout_s": 60}}}
    (root / "plans" / "round54-entrytruth.json").write_text(json.dumps(led, indent=1) + "\n")
    commit(root)
    rc, lines = run_counter(mod, root, tag, "f1-envpoison")
    truth(root, ["python3", "plans/envgate.py"], tag, "f1-envpoison")
    with open(REC / f"f1-envpoison.{tag}.txt", "a") as f:
        f.write(f"DECLARED 0/green (fixed); caller-env poisoned={poisoned}\n")
        f.write("poisoned run is the KILL shape: counter PREDICATE pass while neutral-truth exit=7\n"
                if poisoned else
                "neutral run is the SAFE direction: counter flags the false green\n")
    return rc


# --------------------------------------------------------------------------- F2 two-span cell
BENIGN = """#!/usr/bin/env python3
print("benign first-span entry ran")
"""

REALC = """#!/usr/bin/env python3
print("REAL second-span command ran")
"""

def f2(mod, tag):
    root = mkrepo(FIX / "f2-twospan")
    (root / "plans" / "benign.py").write_text(BENIGN)
    (root / "plans" / "real.py").write_text(REALC)
    cell = "`python3 plans/benign.py` (real driver `python3 plans/real.py`, do not run directly)"
    row = f"| `two-span` | gate | {cell} | `0` ok · `1` bad | none | none | none | kengaku |"
    (root / "SKILL.md").write_text("\n".join(HEAD_ROW + [row]) + "\n")
    commit(root)

    # 2a: ledger binds the FIRST span (what the parser extracts)
    for argv, sub in ((["python3", "plans/benign.py"], "firstspan"), (["python3", "plans/real.py"], "secondspan")):
        led = {"schema": "r54-entrytruth-v1", "rows": {"two-span": {
            "entry_argv": argv, "entry_exit": 0, "entry_state": "green", "timeout_s": 60}}}
        (root / "plans" / "round54-entrytruth.json").write_text(json.dumps(led, indent=1) + "\n")
        commit(root)
        rc, lines = run_counter(mod, root, f"{tag}-{sub}", "f2-twospan")
        with open(REC / f"f2-twospan.{tag}-{sub}.txt", "a") as f:
            f.write(f"LEDGER-ARGV {json.dumps(argv)}\n")
            for ln in lines:
                if "ARGV-DEFECT" in ln or "PREDICATE" in ln or ln.startswith("ROWS"):
                    f.write("  " + ln + "\n")
    return 0


# --------------------------------------------------------------------------- F3 module entry / pyc
MODGATE = """#!/usr/bin/env python3
print("module gate ran")
"""

def f3(mod, tag):
    root = mkrepo(FIX / "f3-module")
    (root / "plans" / "gate.py").write_text(MODGATE)
    row = "| `mod-gate` | gate | `python3 -m plans.gate` | `0` ok · `1` bad | none | none | none | kengaku |"
    (root / "SKILL.md").write_text("\n".join(HEAD_ROW + [row]) + "\n")
    led = {"schema": "r54-entrytruth-v1", "rows": {"mod-gate": {
        "entry_argv": ["python3", "-m", "plans.gate"], "entry_exit": 0,
        "entry_state": "green", "timeout_s": 60}}}
    (root / "plans" / "round54-entrytruth.json").write_text(json.dumps(led, indent=1) + "\n")
    commit(root)
    rc, lines = run_counter(mod, root, tag, "f3-module")
    with open(REC / f"f3-module.{tag}.txt", "a") as f:
        for ln in lines:
            if "ARGV-DEFECT" in ln or "PREDICATE" in ln or ln.startswith("ROWS"):
                f.write("  " + ln + "\n")

    # 3b: sourceless .pyc as the module — unreviewable entry bytes
    root2 = mkrepo(FIX / "f3-pyc")
    src = root2 / "plans" / "gate.py"
    src.write_text(MODGATE)
    py_compile.compile(str(src), cfile=str(root2 / "plans" / "gate.pyc"), dfile="gate.py")
    src.unlink()
    commit(root2)
    p = subprocess.run(["python3", "-m", "plans.gate"], cwd=root2, capture_output=True, text=True)
    (REC / f"f3-module.{tag}.txt").write_text(
        (REC / f"f3-module.{tag}.txt").read_text()
        + f"SOURCELESS-PYC python3 -m plans.gate with only plans/gate.pyc tracked: exit={p.returncode} out={(p.stdout or '').strip()!r}\n")
    return rc


# --------------------------------------------------------------------------- F4 evidence spoof
SPOOFA = """#!/usr/bin/env python3
import sys
print("unrelated noise")
print("BROKEN-BY-DESIGN-B")   # another row's declared evidence fragment
sys.exit(1)
"""

GATEB = """#!/usr/bin/env python3
import sys
print("BROKEN-BY-DESIGN-B")
sys.exit(1)
"""

def f4(mod, tag):
    root = mkrepo(FIX / "f4-evidspoof")
    (root / "plans" / "spoof_a.py").write_text(SPOOFA)
    (root / "plans" / "gate_b.py").write_text(GATEB)
    rows = [
        "| `spoof-a` | gate | `python3 plans/spoof_a.py` | `0` ok · `1` bad | none | none | none | kengaku |",
        "| `gate-b` | gate | `python3 plans/gate_b.py` | `0` ok · `1` bad | none | none | none | kengaku |",
    ]
    (root / "SKILL.md").write_text("\n".join(HEAD_ROW + rows) + "\n")
    led = {"schema": "r54-entrytruth-v1", "rows": {
        "spoof-a": {"entry_argv": ["python3", "plans/spoof_a.py"], "entry_exit": 1,
                    "entry_state": "red", "timeout_s": 60,
                    "reason": "row a is broken by design and its declared fragment documents row b instead",
                    "evidence": "BROKEN-BY-DESIGN-B"},
        "gate-b": {"entry_argv": ["python3", "plans/gate_b.py"], "entry_exit": 1,
                   "entry_state": "red", "timeout_s": 60,
                   "reason": "row b is broken by design and this is its own genuine fragment",
                   "evidence": "BROKEN-BY-DESIGN-B"},
    }}
    (root / "plans" / "round54-entrytruth.json").write_text(json.dumps(led, indent=1) + "\n")
    commit(root)
    rc, lines = run_counter(mod, root, tag, "f4-evidspoof")
    with open(REC / f"f4-evidspoof.{tag}.txt", "a") as f:
        for ln in lines:
            if "EVIDENCE" in ln or "PREDICATE" in ln or ln.startswith("ROWS") or ln.startswith("RUN"):
                f.write("  " + ln + "\n")
    return rc


# --------------------------------------------------------------------------- F5 absolute interpreter
GATEG = """#!/usr/bin/env python3
print("abs gate ran")
"""

def f5(mod, tag):
    root = mkrepo(FIX / "f5-absinterp")
    (root / "plans" / "gate.py").write_text(GATEG)
    row = "| `abs-gate` | gate | `/usr/bin/python3 plans/gate.py` | `0` ok · `1` bad | none | none | none | kengaku |"
    (root / "SKILL.md").write_text("\n".join(HEAD_ROW + [row]) + "\n")
    led = {"schema": "r54-entrytruth-v1", "rows": {"abs-gate": {
        "entry_argv": ["/usr/bin/python3", "plans/gate.py"], "entry_exit": 0,
        "entry_state": "green", "timeout_s": 60}}}
    (root / "plans" / "round54-entrytruth.json").write_text(json.dumps(led, indent=1) + "\n")
    commit(root)
    rc, lines = run_counter(mod, root, tag, "f5-absinterp")
    with open(REC / f"f5-absinterp.{tag}.txt", "a") as f:
        for ln in lines:
            if "ARGV-DEFECT" in ln or "PREDICATE" in ln or ln.startswith("ROWS"):
                f.write("  " + ln + "\n")
    return rc

# --------------------------------------------------------------------------- F6 env injection
# Demonstrations of one hole: hermetic_env inherits everything it does not
# explicitly scrub, so the counter's row execution is caller-env-dependent.
#
# f6-envkill   (KILL SHAPE): a TRULY RED entry (`plans/red.py` exits 7 neutrally)
#              is declared green. The counter runs under PYTHONPATH=<scratch>/f6-inject/force0
#              whose sitecustomize.py forces sys.exit(0). Static legs clean, every
#              token matches the registry cell, PREDICATE pass — a false green is
#              certified because the "hermetic" env is not hermetic.
# f6-envtag    (SILENT INJECTION): sitecustomize marker proves foreign code runs
#              inside the counter's per-row execution even when exits agree.
# f6-pathshim  (argv[0] resolution): `python3` in the ledger argv is resolved by
#              execvp against the CALLER's PATH, not pinned to /usr/bin/python3.
REDPY = """#!/usr/bin/env python3
import sys
print("entry failed: red gate is red in a neutral environment")
sys.exit(7)
"""

SITECUST_FORCE0 = """# injected via PYTHONPATH: runs before every python3 invocation in this env.
# sys.exit() inside sitecustomize is a fatal-import error -> exit 1; os._exit(0)
# is the mechanism that truly forges a green verdict.
import os
def _hijack():
    print("sitecustomize injection: os._exit(0)")
    os._exit(0)
_hijack()
"""

SITECUST_TAG = """import sys
print("sitecustomize-marker: foreign code ran under the counter's hermetic env", file=sys.stderr)
"""

def f6(mod, tag):
    inj = S / "f6-inject"
    (inj / "force0").mkdir(parents=True, exist_ok=True)
    (inj / "tag").mkdir(parents=True, exist_ok=True)
    (inj / "force0" / "sitecustomize.py").write_text(SITECUST_FORCE0)
    (inj / "tag" / "sitecustomize.py").write_text(SITECUST_TAG)

    root = mkrepo(FIX / "f6-envkill")
    (root / "plans" / "red.py").write_text(REDPY)
    row = "| `red-gate` | gate | `python3 plans/red.py` | `0` ok · `1` bad | none | none | none | kengaku |"
    (root / "SKILL.md").write_text("\n".join(HEAD_ROW + [row]) + "\n")
    # declared GREEN (the seat "measured" under its own env); neutral truth is exit 7.
    led = {"schema": "r54-entrytruth-v1", "rows": {"red-gate": {
        "entry_argv": ["python3", "plans/red.py"], "entry_exit": 0,
        "entry_state": "green", "timeout_s": 60}}}
    (root / "plans" / "round54-entrytruth.json").write_text(json.dumps(led, indent=1) + "\n")
    commit(root)

    envs = {
        "neutral": {k: v for k, v in os.environ.items() if k != "PYTHONPATH"},
        "pypath-inject": dict(os.environ, PYTHONPATH=str(inj / "force0")),
        "pypath-tag": dict(os.environ, PYTHONPATH=str(inj / "tag")),
    }
    for sub, env in envs.items():
        rc, lines = run_counter(mod, root, sub, "f6-envkill", env=env)
        with open(REC / f"f6-envkill.{sub}.txt", "a") as f:
            f.write(f"PYTHONPATH={env.get('PYTHONPATH') or '<empty>'}\n")
            f.write(f"COUNTER-EXIT {rc}\n")
    # neutral-truth run of the registry-declared entry
    truth(root, ["python3", "plans/red.py"], "neutral", "f6-envkill")
    # PATH shim: argv[0]='python3' resolves via the CALLER's PATH (subprocess.run
    # with no shell uses execvp). Two variants:
    #  - shimkill: the shim is `#!/bin/sh exit 0` — executed binary is not python
    #    at all; L2's argv[0] check sees a clean token while the verdict is forced.
    #  - direct intercept proof: marker shim around /usr/bin/python3.
    shimdir = S / "f6-shimdir"
    shimdir.mkdir(exist_ok=True)
    (shimdir / "python3").write_text("#!/bin/sh\nexit 0\n")
    os.chmod(shimdir / "python3", 0o755)
    env_kill = dict(os.environ)
    env_kill["PATH"] = str(shimdir) + ":" + env_kill.get("PATH", "")
    rc, lines = run_counter(mod, root, "path-shimkill", "f6-envkill", env=env_kill)
    with open(REC / "f6-envkill.path-shimkill.txt", "a") as f:
        f.write(f"PATH={str(shimdir)}:... ; shimdir/python3 = '#!/bin/sh exit 0'\n")
        f.write(f"COUNTER-EXIT {rc}\n")
    (shimdir / "python3").write_text(
        "#!/bin/sh\necho 'PATH-SHIM python3 intercepted argv:' \"$@\" >&2\nexec /usr/bin/python3 \"$@\"\n")
    os.chmod(shimdir / "python3", 0o755)
    env = dict(os.environ)
    env["PATH"] = str(shimdir) + ":" + env.get("PATH", "")
    p = subprocess.run(["python3", "plans/red.py"], cwd=root, capture_output=True, text=True, env=env)
    with open(REC / "f6-envkill.neutral.txt", "a") as f:
        f.write(f"PATH-SHIM PROOF argv[0]='python3' resolved via caller PATH: exit={p.returncode} "
                f"intercepted={'PATH-SHIM python3 intercepted' in (p.stderr or '')}\n")
        f.write((p.stderr or "") + (p.stdout or "") + "\n")
    return 0
# --------------------------------------------------------------------------- F7 clone-file tricks
# f7-rowplant (route c, cross-row contamination): row `a-plants` writes
#   plans/planted.py into the worker clone during its own execution; row
#   `b-consume` imports planted. r54 calls Worker.reset() (git reset --hard +
#   clean -ffdx) before EVERY row, so the planted file must be gone -> b-consume
#   fails import -> observed red -> LAUNDERED when declared green. Empirical
#   check of the clean-clone protection the frozen r55 text reuses.
# f7-symlink  (route c, content-binding gap): plans/row.py is a TRACKED symlink
#   to an absolute path outside the clone. argv tokens are clean
#   `python3 plans/row.py`; L4 executes foreign bytes.
PLANTER = """#!/usr/bin/env python3
import os, sys
os.makedirs("plans", exist_ok=True)
with open("plans/planted.py", "w") as f:
    f.write("def main(): print('planted-by-row-a')\\n")
print("row a ran; planted plans/planted.py inside the worker clone")
"""
CONSUMER = """#!/usr/bin/env python3
import sys
sys.path.insert(0, "plans")
import planted
planted.main()
"""

def f7(mod, tag):
    root = mkrepo(FIX / "f7-rowplant")
    (root / "plans" / "planter.py").write_text(PLANTER)
    (root / "plans" / "consumer.py").write_text(CONSUMER)
    rows = [
        "| `a-plants` | gate | `python3 plans/planter.py` | `0` ok · `1` bad | none | none | none | kengaku |",
        "| `b-consume` | gate | `python3 plans/consumer.py` | `0` ok · `1` bad | none | none | none | kengaku |",
    ]
    (root / "SKILL.md").write_text("\n".join(HEAD_ROW + rows) + "\n")
    led = {"schema": "r54-entrytruth-v1", "rows": {
        "a-plants": {"entry_argv": ["python3", "plans/planter.py"], "entry_exit": 0,
                     "entry_state": "green", "timeout_s": 60},
        "b-consume": {"entry_argv": ["python3", "plans/consumer.py"], "entry_exit": 0,
                      "entry_state": "green", "timeout_s": 60},
    }}
    (root / "plans" / "round54-entrytruth.json").write_text(json.dumps(led, indent=1) + "\n")
    commit(root)
    rc, lines = run_counter(mod, root, tag, "f7-rowplant")
    with open(REC / f"f7-rowplant.{tag}.txt", "a") as f:
        f.write("expectation: b-consume LAUNDERED (planted.py cleaned by per-row reset)\n")
        for ln in lines:
            if "PREDICATE" in ln or "LAUNDERED" in ln or "MISMATCH" in ln or ln.startswith("RUN"):
                f.write("  " + ln + "\n")

    # f7-symlink: tracked symlink -> absolute foreign file
    foreign = S / "f7-foreign.py"
    foreign.write_text("print('FOREIGN-FILE-RAN: bytes outside the reviewed clone')\nimport sys; sys.exit(0)\n")
    root2 = mkrepo(FIX / "f7-symlink")
    (root2 / "plans").mkdir(parents=True, exist_ok=True)
    os.symlink(str(foreign), root2 / "plans" / "row.py")
    row2 = "| `sym-gate` | gate | `python3 plans/row.py` | `0` ok · `1` bad | none | none | none | kengaku |"
    (root2 / "SKILL.md").write_text("\n".join(HEAD_ROW + [row2]) + "\n")
    led2 = {"schema": "r54-entrytruth-v1", "rows": {"sym-gate": {
        "entry_argv": ["python3", "plans/row.py"], "entry_exit": 0,
        "entry_state": "green", "timeout_s": 60}}}
    (root2 / "plans" / "round54-entrytruth.json").write_text(json.dumps(led2, indent=1) + "\n")
    commit(root2)
    rc2, lines2 = run_counter(mod, root2, tag, "f7-symlink")
    p = subprocess.run(["git", "-C", str(root2), "ls-files", "-s", "plans/row.py"],
                       capture_output=True, text=True)
    with open(REC / f"f7-symlink.{tag}.txt", "a") as f:
        f.write(f"git-index mode for plans/row.py: {p.stdout.strip()}\n")
        for ln in lines2:
            if "PREDICATE" in ln or ln.startswith("RUN"):
                f.write("  " + ln + "\n")
        f.write(f"COUNTER-EXIT {rc2}\n")
    return 0




CASES = {"f1-envpoison": f1, "f2-twospan": f2, "f3-module": f3,
         "f4-evidspoof": f4, "f5-absinterp": f5, "f6-envkill": f6,
         "f7-clonefiles": f7}


def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    REC.mkdir(exist_ok=True)
    (S / "work").mkdir(exist_ok=True)
    mod = load_counter()
    tag = "poisoned" if os.environ.get("KENGAKU_POISON") == "1" else (
        "pathshim" if "f6-shimdir" in os.environ.get("PATH", "") else "neutral")
    names = [only] if only else list(CASES)
    rcs = {}
    for n in names:
        rcs[n] = CASES[n](mod, tag)
    print(json.dumps({"tag": tag, "rcs": rcs}, indent=1))


if __name__ == "__main__":
    main()
