#!/usr/bin/env python3
"""Round-44 C1 counter (calibration): five behaviours `plans/anchor_digest_check.py` and `plans/order_check.py`
advertise in their docstrings that no landed battery demonstrates — the `u = 18` unmutated advertised behaviours
(`.ufo/waves/round-43/build/R43CritEquiv.md` §3) priced in round 43 by `R43PlanNext` (§B.1-B.4): six of them carry
a single-replacement mutant with a witnessed direction; five of those six survive battery42 + battery43 run as one
battery (freeze control `claims/control-c1-standing-batteries.txt`; U3 is killed there by battery43
`a_alt-slug-deepest`, so it is already demonstrated and left out) — killed only by an
ATTRIBUTED kill in a declared direction, every fixture built and every tool run inside a read-only host sandbox.

Frozen predicate (same sentence in plans/round-44-claims.md and in the receipt label):
  C1 passes iff `python3 plans/round44_c1_verify.py --lane .` prints `PINS total=2 mismatched=0`, then
  `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, then
  `MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0`, then
  `MUTANTS-BY-TOOL anchor=4/4 order=1/1`, then `PINS-AFTER mismatched=0`, then `PREDICATE C1 pass`,
  exit 0, measured on a clean clone of the landing tip.

New in round 44 (round-43 wave-1 `R43SentinelCounter` F1-F6, `R43CritC1Counter` V2'; each with a hostile module
red under the round-43 counter's rule and refused here, `claims/control-c1-hostile-f*.txt`):
  F1   a `.git` FILE (gitdir redirect) is refused and `rev-parse --absolute-git-dir` must resolve inside the fixture;
  F2   the repo walk has no depth cap (a visited-entry bound refuses a pathological tree instead);
  F3   argv shape: an order argv is exactly `--lane V --claims V --receipt V`; an anchor argv uses only the exact
       options `--lane V`, `--evidence-ref V`, `--verbose` (no argparse abbreviation, no `--opt=value`);
  F4   every parent-side git call has a 30 s timeout and no stdin; a hang is a SETUP refusal, not a stall;
  F5   `core.worktree` is read `--local --no-includes`, a config carrying any include is refused, and
       `objects/info/alternates` is refused;
  F6   parent-side git discovery is bounded by `GIT_CEILING_DIRECTORIES` at the fixture directory's parent, and the
       repo the tool adopts from `--lane` (git's own discovery, no ceiling) must have toplevel and git dir in d.
Mutant list and literals: `TOTAL = 5`, `FLOORS = {anchor: 4, order: 1}` (U5 U6 U7 U9 U14c); battery = `plans/battery44/*.py`.
Everything below this paragraph is the round-43 counter's rule, carried unchanged except those names.

Non-vacuity (round-41 Q31): the predicate binds the mutant total and a per-tool count to literals (`TOTAL`,
`FLOORS`); a copy of this counter with an empty mutant list prints `PREDICATE C1 fail` (freeze control
`control-c1-no-mutants.txt`). The counter's digest is pinned in the round's `frozen-digests.txt`.

Carried from the round-42 counter (`plans/round42_c1_verify.py`, repairs a-f) through the round-42 wave-2 hardened
copy (`.ufo/waves/round-42/falsify/F42C1Hardened/round42_c1_verify.py`, R1-R4, each with a hostile module):
  a-e  variant bound by fd and the store hidden; `--unshare-ipc`; `--tmpfs /run`; relative argv tokens resolved
       against the fixture dir; streaming digests;
  f    SPAN attribution: a direction hit counts as a kill only when a traced re-run of the mutant on the killing
       fixture reproduces the same (exit, class set) and executes at least one line of the replaced span;
  R1   gpg.program=/bin/true, log.showSignature=false, core.fsmonitor=false, core.hooksPath=/dev/null pinned as
       GIT_CONFIG_KEY_n for the build child and every tool run (`R42SentinelCounter` V1);
  R2   no copy of this counter in the scratch root: the build child runs a generated minimal builder bound by fd
       (`R42SentinelCounter` V2);
  R3   hides are empty READ-ONLY binds, the lane hidden from tool runs too (`R42SentinelCounter` V3/V5);
  R4   a fixture repo whose `rev-parse --show-toplevel` or `core.worktree` leaves its directory is refused
       (`R42CritC1Counter` V1b).
New in round 43 (round-42 closure R4 and `F42CritPlanNext` D3):
  g    VALUE attribution (`R42CritAttribution` §2.2; method of `F42C1StrongAttrib`, made generic): the traced
       re-runs record, for every execution of a replaced-span line in the tool file, the next event of that frame
       — (next line number, digest of the frame's locals) or (return, digest of the returned value); memory
       addresses and per-run scratch names are normalised, `PYTHONHASHSEED=0`. A kill needs the mutant's record
       to DIFFER from the reference's record on the killing fixture (the reference traced over the same span
       lines; a mutant whose `old`/`new` differ in newline count is invalid). The reference is traced twice; a
       record that differs between those two runs is not evidence (`site-record-unstable`). A hit whose span
       ran but whose site record equals the reference's is `unattributed` (`site-record-equal`).
  h    SYMLINK escape (`R42CritC1Counter` V2b): a fixture is refused when any symlink under its directory
       resolves outside it.
  i    ORDER argv blobs (`R42CritC1Counter` §1 substitutes `b-xo1-receipt-is-directory`,
       `b-xo3-emptied-directory`): an order fixture is refused unless its `--claims` and `--receipt` each name a
       BLOB at HEAD of the `--lane` repo it names.
Each of R1-R4, h and i has a hostile module that turns it red at the freeze (`claims/control-c1-hostile-*.txt`);
g has a forced-equal copy (`claims/control-c1-value.txt`).

Self-assessment under test: each tool's own docstring. Each mutant is one byte-level `old -> new` replacement; its
`adv` cell quotes the advertising sentence with file:line (both tools unchanged since round 39: pins below equal
the round-42 counter's). `adv_kind` as in round 41 (`indirect`: the behaviour follows from the advertised
contract rather than being worded in it). A survivor is an advertised-but-undemonstrated behaviour.

Directions (QUALITY Q29/Q33), each RE-DERIVED before the freeze: the round-42 wave-2 seat's table is carried data,
so `.ufo/waves/round-43/claims/witness/w_near.py` (ported from that seat's `w2_probe.py`) is run through this
counter in development mode (`claims/witness-run.txt`) and every direction below is the one that run witnesses.
  silence     reference prints class C, the fixture declares C, the mutant does not print C (both exit 0/1)
  rc-silence  fixture `expect=reject`, reference exits 1, mutant exits 0
  rc-mirror   fixture `expect=accept`, reference exits 0, mutant exits 1
  error       fixture `expect=error`, reference exits 2, mutant exits 0 or 1
Classes: anchor — every `class=<C>` token of a `DEFECT ` line; order — none (exit-code directions only; an order
fixture declares `defects: []`).

Battery = `plans/battery44/*.py`, nothing else. Contract: `FIXTURES = [{"fid", "tool": anchor|order,
"expect": accept|reject|error, "defects": [...], "build": build}]`; `build(ctx, d)` fills the EMPTY directory d
and returns the tool argv tail as a list of str. An absolute or relative path in the argv must resolve inside d
(tokens `{WORK}`, `{WORK}/<rel>`, `{WORK:<name>}` as in round 41). `ctx` offers `ctx.init(dest)` (git init -b
master), `ctx.git(repo, *args)` (refuses unless repo is its own toplevel; commits as `fixture
<fixture@kengaku.invalid>` at a fixed date), `ctx.write(path, text|bytes)` and `ctx.sh(*argv, cwd=)`; every path
must lie inside d. No lane clone is offered. `defects` is the exact class set the reference must print; a fixture
whose reference result differs from its declaration is `wrong`. The battery may not import, copy or read the
witness modules.

Isolation as in round 42 plus R1-R4 (build child and every tool run in `bwrap --ro-bind / /`, lane hidden, fixed
system PATH, HOME read-only and empty, git config pinned, `GIT_CEILING_DIRECTORIES` at the scratch root,
fingerprints after the build and after the last run, pins hashed before and after, `sidechannel` token scan,
`null_detected` on a second unmodified run, `--work` inside the lane refused).

Limits named at the freeze: a kill records a result difference in the declared direction on a fixture that
executes the mutated line and changes its site record, not the fixture's intent; the value record sees locals and
control flow, not attribute state hidden inside an object whose repr does not show it (a mutant whose only effect
is such hidden state would read `unattributed`, a false negative, never a false kill); the token scan is a
heuristic, so non-author review of battery44 stays part of admission; a module can still read other copies of
the tools elsewhere on the read-only host; R1 pins four keys, not git's whole key space. NA12 (null, unreachable
line) and the 15 near-variants battery42 already kills are not in this list; neither is any
`state_check.py`/`round_close.py` survivor nor the `u = 18` unmutated advertised behaviours (`R42CritEquiv` §3).

  --battery-dir DIR   load battery modules from DIR instead of plans/battery44 (development; predicate n/a)
  --only U7,U14c      restrict mutants (development; predicate n/a)
  --work DIR          scratch parent, created if absent (default: $TMPDIR via tempfile)
  --jobs N            parallel tool runs (default 8)
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import itertools
import json
import os
import pathlib
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile

BATTERY_REL = "plans/battery44"
TOOLS = {
    "anchor": "plans/anchor_digest_check.py",
    "order": "plans/order_check.py",
}
PINS = {
    "plans/anchor_digest_check.py": "11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2",
    "plans/order_check.py": "948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc",
}
SIDECHANNEL = ("/proc", "ppid", "cmdline", "psutil", "environ", "fsmonitor", "hookspath", "filter.",
               "gitattributes", "core.", "alias.", "setsid", "daemon", "fork", "nohup", "socket",
               "/home/", ".local", "__file__", "inspect", "importlib", "sys.path", "ctypes", "chmod",
               "witness", "settrace", "/run")
SIMPLE_DIRECTIONS = ("silence", "rc-silence", "rc-mirror", "error")
PAIR = re.compile(r"^(\d)>(\d)$")
EXPECT_RC = {"accept": 0, "reject": 1, "error": 2}
WORK_TOKEN = re.compile(r"^\{WORK(?::([a-z]+))?\}(/[A-Za-z0-9._/-]+)?$")
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
BWRAP = "/usr/bin/bwrap"
PY = "/usr/bin/python3"
TRACER_SLOT = "/run/k44-tracer.py"
WR = ".ufo/waves/round-44/claims/witness-run.txt"
TOTAL = 5
FLOORS = {"anchor": 4, "order": 1}


def SITE_EQUAL(mut_sites, ref_sites):
    """Round-43 leg g: equal site records mean the replaced span ran without changing what followed it."""
    return tuple(mut_sites) == tuple(ref_sites)

# --- F42C1Hardened banner (round-42 wave 2, falsify), carried into round 43 unchanged except the k44 slot names.
#   R1  R42SentinelCounter V1: the run and build env pin gpg.program=/bin/true and log.showSignature=false,
#       so a fixture's `.git/config` cannot run a program through `git log --format=%H` (order_check.py:97).
#   R2  R42SentinelCounter V2: no copy of this counter is written into the scratch root. The build child runs
#       a generated minimal builder (Ctx/load/build_module_child only) bound by `--ro-bind-data`; the old
#       root/bin builder path is hidden instead of populated.
#   R3  R42SentinelCounter V3/V5: `hide` binds an empty read-only directory over the target (a `--tmpfs` hide
#       left a writable directory at the hidden name); the lane is hidden from tool runs too.
#   R4  R42CritC1Counter V1b: after a module builds, every fixture repo is refused when
#       `rev-parse --show-toplevel` or `core.worktree` resolves somewhere other than the repo directory.
GIT_PINS = {
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_COUNT": "4",
    "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
    "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null",
    "GIT_CONFIG_KEY_2": "gpg.program", "GIT_CONFIG_VALUE_2": "/bin/true",
    "GIT_CONFIG_KEY_3": "log.showSignature", "GIT_CONFIG_VALUE_3": "false",
}
PIN_CHECK_ENV = {"PATH": PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", **GIT_PINS}
COUNTER_DIR = pathlib.Path(__file__).resolve().parent
BUILDER_SLOT = "/run/k44-builder.py"
SLOT = "/run/k44-slot.py"

TRACER = r'''
import hashlib, os, re, runpy, sys
slot, out = sys.argv[1], os.path.join(os.environ["TMPDIR"], "k44-trace.txt")
span = frozenset(int(x) for x in os.environ.get("K44_SPAN", "").split(",") if x)
hit, sites, last = set(), [], {}
ADDR = re.compile(r"0x[0-9a-fA-F]+")
RUN = re.compile(r"/(?:rtmp/t|work/w)[0-9]{6}")
def digest(obj):
    try:
        if isinstance(obj, dict):
            obj = {k: v for k, v in obj.items() if not (isinstance(k, str) and k.startswith("__"))}
            text = repr(sorted(((repr(k), repr(v)) for k, v in obj.items())))
        else:
            text = repr(obj)
    except Exception as e:  # an unrepresentable value still yields a stable record
        text = "unrepr:" + type(e).__name__
    text = RUN.sub("/RUN", ADDR.sub("0x", text))
    return hashlib.sha256(text.encode()).hexdigest()[:16]
def note(frame, after):
    prev = last.get(id(frame))
    if prev in span and len(sites) < 2000:
        sites.append(f"{prev}>{after}:{digest(frame.f_locals)}")
def local(frame, event, arg):
    if event == "line":
        hit.add(frame.f_lineno)
        note(frame, frame.f_lineno)
        last[id(frame)] = frame.f_lineno
    elif event == "return":
        prev = last.pop(id(frame), None)
        if prev in span and len(sites) < 2000:
            sites.append(f"{prev}>ret:{digest(arg)}")
    return local
def glob(frame, event, arg):
    if frame.f_code.co_filename == slot:
        hit.add(frame.f_lineno)
        return local
    return None
sys.argv = sys.argv[1:]
code = 0
sys.settrace(glob)
try:
    runpy.run_path(slot, run_name="__main__")
except SystemExit as e:
    code = e.code
finally:
    sys.settrace(None)
    with open(out, "w") as fh:
        fh.write(" ".join(str(n) for n in sorted(hit)) + "\n" + " ".join(sites) + "\n")
sys.exit(code)
'''

# (id, tool, class, direction, adv_kind, adv [file:line 'quoted sentence'], witness [pre-freeze, committed],
#  old, new)
MUTANTS = [
    ('U5', 'anchor', 'digest-short', 'silence', 'direct',
     "plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex digits (`digest-short`, `digest-long`' (a short token labelled digest-long)",
     f"{WR} (MUTANT U5); round-43 wave-1 R43PlanNext B.1 row 5",
     'cls, why = ("digest-short" if len(tok) < 64 else "digest-long")',
     'cls, why = ("digest-long" if len(tok) < 64 else "digest-long")'),
    ('U6', 'anchor', 'digest-long', 'silence', 'direct',
     "plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex digits (`digest-short`, `digest-long`' (a long token labelled digest-short)",
     f"{WR} (MUTANT U6); round-43 wave-1 R43PlanNext B.1 row 6",
     'cls, why = ("digest-short" if len(tok) < 64 else "digest-long")',
     'cls, why = ("digest-short" if len(tok) < 64 else "digest-short")'),
    ('U7', 'anchor', '-', 'rc-mirror', 'direct',
     "plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures is not a defect' (only the first resolving capture is claimed)",
     f"{WR} (MUTANT U7); round-43 wave-1 R43PlanNext B.1 row 7",
     'hit = sorted(p for p, ent in per.items() if tok in ent["digests"])\n                claimed.update(hit)\n                if verbose:\n                    path, how',
     'hit = sorted(p for p, ent in per.items() if tok in ent["digests"])[:1]\n                claimed.update(hit)\n                if verbose:\n                    path, how'),
    ('U9', 'anchor', '-', 'rc-mirror', 'direct',
     "plans/anchor_digest_check.py:106-107 'lessons are read from the working tree for paths committed at HEAD, so a seat's erratum counts before it is committed' (lessons read from HEAD instead)",
     f"{WR} (MUTANT U9); round-43 wave-1 R43PlanNext B.1 row 9",
     'f.read_text(encoding="utf-8", errors="replace")',
     'git(lane, "show", "HEAD:" + p).decode("utf-8", "replace")'),
    ('U14c', 'order', '-', 'error', 'direct',
     "plans/order_check.py:26-27 'Exit: 0 order holds · 1 order broken · 2 setup error (... unparseable round number, bad arguments)' (the claims-name guard disabled)",
     f"{WR} (MUTANT U14c); round-43 wave-1 R43PlanNext B.1 row 14 (U14c)",
     '        if not m:\n            raise SetupError(f"claims file name',
     '        if False:\n            raise SetupError(f"claims file name'),
]


def sha256(p):
    try:
        return file_sha256(p)
    except OSError:
        return None


class Ctx:
    """What a battery build() may use. Runs only inside the build child."""

    ENV = {"PATH": PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
           "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
           "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
           "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00"}

    def __init__(self, fixture_root):
        self._root = pathlib.Path(fixture_root).resolve()
        # F42C1Hardened R1/R4: the build child gets the same executable-key pins as a tool run.
        self.ENV = dict(self.ENV, GIT_CEILING_DIRECTORIES=str(self._root.parent), **GIT_PINS)

    def _inside(self, p):
        p = pathlib.Path(p).resolve()
        if not p.is_relative_to(self._root):
            raise ValueError(f"path outside the fixture root: {p}")
        return p

    def sh(self, *argv, cwd=None, check=True):
        r = subprocess.run([str(a) for a in argv], cwd=str(self._inside(cwd)) if cwd else None,
                           env=self.ENV, capture_output=True, text=True)
        if check and r.returncode != 0:
            raise RuntimeError(f"{argv[:3]} rc={r.returncode}: {r.stderr.strip()[-200:]}")
        return r

    def write(self, path, text):
        p = self._inside(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(text, bytes):
            p.write_bytes(text)
        else:
            p.write_text(text)
        return p

    def init(self, dest):
        dest = self._inside(dest)
        dest.mkdir(parents=True, exist_ok=True)
        self.sh("git", "-C", str(dest), "init", "-q", "-b", "master")
        return dest

    def git(self, repo, *args, check=True):
        repo = self._inside(repo)
        top = self.sh("git", "-C", str(repo), "rev-parse", "--show-toplevel", check=False)
        if top.returncode != 0 or pathlib.Path(top.stdout.strip()).resolve() != repo:
            raise RuntimeError(f"refusing git in {repo}: not its own toplevel")
        return self.sh("git", "-C", str(repo), *args, check=check)


def load(path, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_module_child(module, dest):
    """Child entry (inside bwrap): build every fixture of one module into dest/fNNN, print JSON only."""
    mod = load(module, f"kengaku_b42_{module.stem}")
    ctx = Ctx(dest)
    out = []
    for k, fx in enumerate(getattr(mod, "FIXTURES", [])):
        d = dest / f"f{k:03d}"
        d.mkdir(parents=True)
        argv = fx["build"](ctx, d)
        if not isinstance(argv, list) or not all(type(t) is str for t in argv):
            raise TypeError(f"fixture {fx.get('fid')!r}: build() must return a list of str")
        out.append({"fid": fx["fid"], "tool": fx.get("tool"), "expect": fx.get("expect"),
                    "defects": fx.get("defects"), "argv": argv})
    sys.stdout.write("BUILT " + json.dumps(out) + "\n")
    return 0


def ro_sandbox(writable=(), ro_binds=(), hide=(), ro_data=(), empty=None):
    argv = [BWRAP, "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--unshare-pid", "--unshare-net",
            "--unshare-ipc", "--tmpfs", "/run",
            "--die-with-parent", "--new-session"]
    if hide and empty is None:
        raise ValueError("ro_sandbox: hide targets need an empty directory to bind over them")
    for h in hide:
        # F42C1Hardened R3: `--tmpfs <h>` left a *writable* empty directory at the hidden name (a build could
        # plant files there); an empty read-only bind keeps the contents empty and a write fails with EROFS.
        argv += ["--ro-bind", str(empty), str(h)]
    for w in writable:
        argv += ["--bind", str(w), str(w)]
    for src, dst in ro_binds:
        argv += ["--ro-bind", str(src), str(dst)]
    for fd, dst in ro_data:
        argv += ["--ro-bind-data", str(fd), str(dst)]
    return argv


def file_sha256(p):
    """Content digest of one file, streamed: no read of the whole file into memory."""
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while chunk := fh.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def fingerprint(d):
    h = hashlib.sha256()
    for top, dirs, files in os.walk(d):
        dirs[:] = sorted(x for x in dirs if x != "__pycache__")
        rel_top = os.path.relpath(top, d)
        for name in sorted(files) + [x for x in dirs if os.path.islink(os.path.join(top, x))]:
            rel = os.path.normpath(os.path.join(rel_top, name))
            if rel.endswith(".git/index") or rel.endswith(".lock"):
                continue
            p = os.path.join(top, name)
            st = os.lstat(p)
            link = os.readlink(p) if os.path.islink(p) else ""
            content = ""
            if not link and os.path.isfile(p):
                content = file_sha256(p)
            h.update(f"{rel}\0{st.st_mode}\0{st.st_size}\0{link}\0{content}\n".encode())
    return h.hexdigest()


def path_ok(tok, d):
    if WORK_TOKEN.match(tok):
        return ".." not in tok
    d = d.resolve()
    for cand in (tok, tok.split("=", 1)[1] if tok.startswith("--") and "=" in tok else ""):
        if not cand:
            continue
        base = pathlib.Path(cand) if cand.startswith("/") else d / cand
        if not base.resolve().is_relative_to(d):
            return False
    return True


def classes(tool, out):
    got = set()
    if tool != "anchor":
        return frozenset(got)
    for line in out.splitlines():
        if line.startswith("DEFECT "):
            got.update(re.findall(r"\bclass=(\S+)", line))
    return frozenset(got)


def hide_list(paths, existing=False):
    """F42C1Hardened R3: dedupe hide targets and drop any target nested inside another.

    A nested `--ro-bind` would need a mount destination inside a directory an earlier hide has already
    emptied, so only the outermost target of each chain is bound.
    """
    keep = []
    for p in paths:
        if p is None:
            continue
        p = pathlib.Path(p).resolve() if existing else pathlib.Path(p)
        if existing and not p.exists():
            continue
        if any(p == q or p.is_relative_to(q) for q in keep):
            continue
        keep = [q for q in keep if not q.is_relative_to(p)]
        keep.append(p)
    return keep


def builder_source():
    """F42C1Hardened R2 (R42SentinelCounter V2): the build child's entry point, without the mutant table.

    Built from this file's own definitions, so the sandboxed builder cannot drift from the parent's Ctx; it
    is delivered by `--ro-bind-data` at BUILDER_SLOT, so no copy of this counter (and therefore no
    `MUTANTS` table) is written into the scratch root where a battery module could read it.
    """
    import ast
    text = pathlib.Path(__file__).read_text()
    want = ("Ctx", "load", "build_module_child")
    picked = {node.name: ast.get_source_segment(text, node)
              for node in ast.parse(text).body
              if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name in want}
    missing = [n for n in want if not picked.get(n)]
    if missing:
        raise RuntimeError(f"builder_source: cannot slice {missing} out of {__file__}")
    head = ("import json, pathlib, subprocess, sys\nimport importlib.util\n\n"
            + "PATH = " + repr(PATH) + "\n"
            + "GIT_PINS = " + repr(GIT_PINS) + "\n\n")
    body = "\n\n".join(picked[n] for n in want)
    tail = ("\n\nif __name__ == \"__main__\":\n"
            "    sys.exit(build_module_child(pathlib.Path(sys.argv[1]).resolve(),\n"
            "                                pathlib.Path(sys.argv[2]).resolve()))\n")
    return head + body + tail


GIT_TIMEOUT = 30
ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True, "--verbose": False}
ORDER_SHAPE = ("--lane", "--claims", "--receipt")


def pin_git(repo, *args, ceiling):
    """Round-44 F4/F6 (`R43SentinelCounter`): every parent-side git call has a timeout, no stdin, and discovery
    stops at `ceiling` (the parent of the fixture directory, which holds no repo), so neither a FIFO include nor a repo above `d` decides it.
    Returns (rc, stdout) or None on a timeout."""
    env = {**PIN_CHECK_ENV, "GIT_CEILING_DIRECTORIES": str(ceiling)}
    try:
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=env,
                           stdin=subprocess.DEVNULL, timeout=GIT_TIMEOUT)
    except subprocess.TimeoutExpired:
        return None
    return r.returncode, r.stdout.strip()


def repo_breach(d):
    """F42C1Hardened R4 (R42CritC1Counter V1b) with the round-44 fence repairs (`R43SentinelCounter` F1, F2, F4,
    F5, F6): a fixture's repo must stay rooted at its own directory AND keep its git store inside `d`.

    Every directory under `d` is walked with no depth cap (F2; a visited-entry bound of 200000 refuses a
    pathological tree instead of skipping it). A `.git` that is a plain FILE is refused (F1: `gitdir:` redirect),
    `rev-parse --absolute-git-dir` must resolve inside `d` (F1), `objects/info/alternates` is refused (F5), and
    `core.worktree` is read with `--local --no-includes` (F5) — any include.path is refused outright, so no file
    outside `d` is parsed. A git call that hangs is a breach (F4)."""
    d = d.resolve()
    repos, seen_entries = [], 0
    for top, dirs, files in os.walk(d):
        seen_entries += len(dirs) + len(files)
        if seen_entries > 200000:
            return "fixture tree exceeds 200000 entries"
        if ".git" in files:
            return f"{os.path.relpath(top, d)}/.git is a file (gitdir redirect), not a directory"
        if ".git" in dirs:
            repos.append(pathlib.Path(top))
        dirs[:] = sorted(x for x in dirs if x != ".git")
    for repo in repos:
        repo = repo.resolve()
        gd = repo / ".git"
        if gd.is_symlink():
            return f"{repo.name}/.git is a symlink"
        if (gd / "objects" / "info" / "alternates").exists():
            return f"{repo.name}/.git/objects/info/alternates present"
        inc = pin_git(repo, "config", "--local", "--no-includes", "--get-regexp", r"^include(if)?\.", ceiling=d.parent)
        if inc is None:
            return f"{repo.name}/git hung"
        if inc[0] == 0 and inc[1]:
            return f"{repo.name}/.git/config carries an include"
        for args, what in ((("rev-parse", "--show-toplevel"), "rev-parse --show-toplevel"),
                           (("rev-parse", "--absolute-git-dir"), "rev-parse --absolute-git-dir")):
            got = pin_git(repo, *args, ceiling=d.parent)
            if got is None:
                return f"{repo.name}/git hung"
            if got[0] == 0:
                p = pathlib.Path(got[1]).resolve()
                ok = p == repo if what.endswith("toplevel") else p.is_relative_to(d)
                if not ok:
                    return f"{repo.name}/{what}={got[1]}"
        wt = pin_git(repo, "config", "--local", "--no-includes", "--get", "core.worktree", ceiling=d.parent)
        if wt is None:
            return f"{repo.name}/git hung"
        val = wt[1] if wt[0] == 0 else ""
        if val:
            p = pathlib.Path(val)
            if (p if p.is_absolute() else repo / p).resolve() != repo:
                return f"{repo.name}/core.worktree={val}"
    return None

def symlink_breach(d):
    """Round 43 leg h (R42CritC1Counter V2b): no symlink under a fixture may resolve outside it."""
    d = d.resolve()
    for top, dirs, files in os.walk(d):
        for name in dirs + files:
            p = pathlib.Path(top) / name
            if p.is_symlink() and not p.resolve().is_relative_to(d):
                return f"symlink {p.relative_to(d)} -> {os.readlink(p)}"
    return None


def argv_shape_breach(tool, argv):
    """Round-44 F3 (`R43SentinelCounter` F3, `R43CritC1Counter` V2'): the argv must use the tool's options exactly
    as the module contract writes them, so no argparse abbreviation or `--opt=value` form can bypass a leg. An
    order argv is exactly `["--lane", v, "--claims", v, "--receipt", v]`, an argv that leaves one flag out (or adds
    one) included; an anchor argv uses only `--lane V`, `--evidence-ref V`, `--verbose`."""
    if tool == "order":
        if len(argv) != 6 or tuple(argv[0::2]) != ORDER_SHAPE:
            return f"order argv is not the contract shape {list(ORDER_SHAPE)}: {argv}"
        return None
    k = 0
    while k < len(argv):
        t = argv[k]
        if t not in ANCHOR_OPTS:
            return f"anchor argv token {t!r} is not an exact option"
        k += 2 if ANCHOR_OPTS[t] else 1
    return None


def order_argv_breach(d, argv):
    """Round 43 leg i (R42CritC1Counter §1 substitutes): an order fixture's `--claims` and `--receipt` must each
    name a BLOB at HEAD of the `--lane` repo when that path exists at HEAD at all (a missing path stays the tool's
    own setup error, exit 2; a directory standing in for a file is refused here). Round 44: the argv is the exact
    contract shape (checked first, `argv_shape_breach`), and the git call is bounded (F4/F6)."""
    vals = dict(zip(argv[0::2], argv[1::2]))
    lane = pathlib.Path(vals.get("--lane", "."))
    lane = lane if lane.is_absolute() else d / lane
    for opt in ("--claims", "--receipt"):
        got = pin_git(lane, "cat-file", "-t", f"HEAD:{vals[opt]}", ceiling=d.resolve().parent)
        if got is None:
            return f"{opt} git hung"
        if got[0] == 0 and got[1] != "blob":
            return f"{opt} {vals[opt]} is a {got[1]} at HEAD, not a blob"
    return None


def lane_breach(d, argv):
    """Round-44 F2/F6 remediation (`R43SentinelCounter` F2 "derive the repos from the argv"): the repo the tool
    will adopt from `--lane` — found by git's own discovery, with no ceiling below the host root, exactly as the
    tool run discovers it up to its scratch-root ceiling — must have its toplevel and its git dir inside `d`. A
    `--lane` that is no repo at all stays the tool's own setup error."""
    vals = dict(zip(argv[0::2], argv[1::2]))
    if "--lane" not in vals:
        return None
    lane = pathlib.Path(vals["--lane"])
    lane = (lane if lane.is_absolute() else d / lane).resolve()
    if not lane.is_dir():
        return None
    d = d.resolve()
    for args in (("rev-parse", "--show-toplevel"), ("rev-parse", "--absolute-git-dir")):
        try:
            r = subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True, env=PIN_CHECK_ENV,
                               stdin=subprocess.DEVNULL, timeout=GIT_TIMEOUT)
        except subprocess.TimeoutExpired:
            return "--lane git hung"
        if r.returncode == 0 and not pathlib.Path(r.stdout.strip()).resolve().is_relative_to(d):
            return f"--lane {' '.join(args)}={r.stdout.strip()} is outside the fixture"
    return None



class Runner:
    def __init__(self, root, jobs, lane=None):
        self.root, self.jobs, self.seq = root, jobs, itertools.count(1)
        self.lane = lane
        self.empty = root / "empty"
        self.empty.mkdir(exist_ok=True)
        (root / "home").mkdir()
        (root / "work").mkdir()
        (root / "rtmp").mkdir()
        (root / "tracer").mkdir()
        self.tracer = root / "tracer" / "k44-tracer.py"
        self.tracer.write_text(TRACER)

    def hidden(self):
        """F42C1Hardened R2/R3: store, builder dir, tracer dir, the lane and this counter's own directory."""
        return hide_list((self.root / "variants", self.root / "bin", self.root / "tracer",
                          self.lane, COUNTER_DIR), existing=True)

    def env(self, tmp, span=None):
        e = {"PATH": PATH, "HOME": str(self.root / "home"), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
             "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(tmp), "PYTHONHASHSEED": "0",
             "GIT_CEILING_DIRECTORIES": str(self.root), **GIT_PINS}
        if span is not None:
            e["K44_SPAN"] = ",".join(str(x) for x in sorted(span))
        return e

    def run(self, tool, variant, fx, trace=False, span=None):
        """One sandboxed tool run -> (exit, class set), or (exit, class set, executed line set, site records) when
        traced; `span` names the lines whose next event the tracer records (round-43 leg g)."""
        n = next(self.seq)
        work = self.root / "work" / f"w{n:06d}"
        tmp = self.root / "rtmp" / f"t{n:06d}"
        work.mkdir()
        tmp.mkdir()
        argv = []
        for t in fx["argv"]:
            m = WORK_TOKEN.match(t)
            if m:
                w = work / "run"
                if m.group(1):
                    (w / m.group(1)).mkdir(parents=True, exist_ok=True)
                if m.group(2):
                    w.mkdir(exist_ok=True)
                argv.append(str(w) + (m.group(2) or ""))
            else:
                argv.append(t)
        src = open(variant, "rb")
        tsrc = open(self.tracer, "rb")
        lines = None
        try:
            data = ((src.fileno(), SLOT), (tsrc.fileno(), TRACER_SLOT)) if trace else ((src.fileno(), SLOT),)
            head = [PY, TRACER_SLOT, SLOT] if trace else [PY, SLOT]
            cmd = ro_sandbox(writable=(work, tmp),
                             hide=[p for p in self.hidden() if p.exists()],
                             ro_data=data, empty=self.empty) + head + argv
            try:
                r = subprocess.run(cmd, cwd=str(fx["dir"]), env=self.env(tmp, span if trace else None),
                                   capture_output=True, text=True,
                                   timeout=600, pass_fds=tuple(fd for fd, _dst in data))
            except subprocess.TimeoutExpired:
                return ("timeout", frozenset(), frozenset(), ()) if trace else ("timeout", frozenset())
            if trace:
                try:
                    raw = (tmp / "k44-trace.txt").read_text().split("\n")
                    lines = frozenset(int(x) for x in raw[0].split())
                    sites = tuple(raw[1].split()) if len(raw) > 1 else ()
                except (OSError, ValueError):
                    lines, sites = frozenset(), ()
        finally:
            src.close()
            tsrc.close()
            shutil.rmtree(work, ignore_errors=True)
            shutil.rmtree(tmp, ignore_errors=True)
        if trace:
            return (r.returncode, classes(tool, r.stdout), lines, sites)
        return (r.returncode, classes(tool, r.stdout))

    def run_all(self, tool, variant, fixtures):
        with concurrent.futures.ThreadPoolExecutor(self.jobs) as ex:
            return list(ex.map(lambda fx: self.run(tool, variant, fx), fixtures))


def exhibits(cls, direction, fx, ref, mut):
    want = EXPECT_RC.get(fx["expect"])
    m = PAIR.match(direction)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return want == a and ref[0] == a and mut[0] == b
    if direction == "rc-silence":
        return fx["expect"] == "reject" and ref[0] == 1 and mut[0] == 0
    if direction == "rc-mirror":
        return fx["expect"] == "accept" and ref[0] == 0 and mut[0] == 1
    if direction == "error":
        return fx["expect"] == "error" and ref[0] == 2 and mut[0] in (0, 1)
    if ref[0] not in (0, 1) or mut[0] not in (0, 1) or cls == "-":
        return False
    return cls in ref[1] and cls in set(fx["defects"]) and cls not in mut[1]  # silence


def seen_directions(cls, direction, fx, ref, mut):
    out = {x for x in SIMPLE_DIRECTIONS if x != direction and exhibits(cls, x, fx, ref, mut)}
    if isinstance(ref[0], int) and isinstance(mut[0], int) and ref[0] != mut[0] and 0 <= ref[0] <= 9 \
            and 0 <= mut[0] <= 9:
        pair = f"{ref[0]}>{mut[0]}"
        if pair != direction:
            out.add(pair)
    return out


def build_battery(bdir, root, lane):
    fixtures, side = [], 0
    if not bdir.is_dir():
        return fixtures, side
    mods = root / "mods"
    mods.mkdir(exist_ok=True)
    empty = root / "empty"
    empty.mkdir(exist_ok=True)
    builder_src = builder_source()
    for f in sorted(bdir.glob("*.py")):
        text = f.read_text().lower()
        hits = [t for t in SIDECHANNEL if t in text]
        if hits:
            side += 1
            print(f"SIDECHANNEL {bdir.name}/{f.name} tokens={','.join(hits)}")
        mod_copy = mods / f"mod_{f.name}"
        mod_copy.write_text(f.read_text())
        dest = root / "fx" / f.stem
        dest.mkdir(parents=True)
        tmp = root / "btmp" / f.stem
        tmp.mkdir(parents=True)
        bfd = os.memfd_create("k44-builder", 0)
        try:
            os.write(bfd, builder_src.encode())
            os.lseek(bfd, 0, os.SEEK_SET)
            # F42C1Hardened R2/R3: the builder arrives on an fd at BUILDER_SLOT and no copy of this file exists
            # in the scratch root; `hide` is an empty read-only bind, so the lane's name is not a writable tmpfs.
            cmd = ro_sandbox(writable=(dest, tmp),
                             hide=[p for p in hide_list((lane, COUNTER_DIR, root / "bin"), existing=True)],
                             ro_data=((bfd, BUILDER_SLOT),), empty=empty) \
                + [PY, BUILDER_SLOT, str(mod_copy), str(dest)]
            r = subprocess.run(cmd, cwd=str(dest), capture_output=True, text=True, timeout=1800,
                               env={"PATH": PATH, "HOME": "/nonexistent", "TMPDIR": str(tmp), "LANG": "C.UTF-8",
                                    "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"},
                               pass_fds=(bfd,))
        finally:
            os.close(bfd)
        built = [l for l in r.stdout.splitlines() if l.startswith("BUILT ")]
        if r.returncode != 0 or len(built) != 1:
            raise RuntimeError(f"module {bdir.name}/{f.name} failed to build (rc={r.returncode}): "
                               f"{r.stderr.strip()[-300:]}")
        for k, fx in enumerate(json.loads(built[0][6:])):
            d = dest / f"f{k:03d}"
            argv = fx.get("argv")
            ok = (isinstance(fx.get("fid"), str) and fx.get("tool") in TOOLS and fx.get("expect") in EXPECT_RC
                  and isinstance(fx.get("defects"), list) and all(isinstance(x, str) for x in fx["defects"])
                  and (fx.get("tool") == "anchor" or not fx["defects"])
                  and isinstance(argv, list) and all(isinstance(t, str) and path_ok(t, d) for t in argv)
                  and d.is_dir())
            if not ok:
                raise ValueError(f"fixture {fx.get('fid')!r} of {bdir.name}/{f.name} breaks the contract")
            breach = argv_shape_breach(fx["tool"], argv) or lane_breach(d, argv) or repo_breach(d) or symlink_breach(d) \
                or (order_argv_breach(d, argv) if fx.get("tool") == "order" else None)
            if breach:
                raise ValueError(f"fixture {fx.get('fid')!r} of {bdir.name}/{f.name}"
                                 f" escapes its directory: {breach}")
            fixtures.append({**fx, "dir": d, "module": f.name})
    return fixtures, side


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--battery-dir", default=None)
    ap.add_argument("--only", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--build-module", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--dest", default=None, help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.build_module:
        return build_module_child(pathlib.Path(a.build_module).resolve(), pathlib.Path(a.dest).resolve())
    lane = pathlib.Path(a.lane).resolve()
    dev = a.battery_dir is not None or a.only is not None
    mism = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
    print(f"PINS total={len(PINS)} mismatched={len(mism)}" + (f" first={mism[0]}" if mism else ""))
    for exe in (BWRAP, PY):
        if not os.access(exe, os.X_OK):
            print(f"SETUP {exe} is required", file=sys.stderr)
            return 2
    if a.work:
        if pathlib.Path(a.work).resolve().is_relative_to(lane):
            print("SETUP --work must not lie inside the lane (the build sandbox hides the lane)", file=sys.stderr)
            return 2
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k44-c1-", dir=a.work)).resolve()
    if root.is_relative_to(lane):
        print("SETUP scratch root lies inside the lane; pass --work", file=sys.stderr)
        shutil.rmtree(root, ignore_errors=True)
        return 2
    try:
        runner = Runner(root, a.jobs, lane)
        srcs = {tool: (lane / rel).read_text() if (lane / rel).is_file() else "" for tool, rel in TOOLS.items()}
        bdir = pathlib.Path(a.battery_dir).resolve() if a.battery_dir else lane / BATTERY_REL
        try:
            fixtures, side = build_battery(bdir, root, lane)
        except (RuntimeError, ValueError, KeyError, TypeError, json.JSONDecodeError,
                subprocess.TimeoutExpired) as e:
            print(f"SETUP {e}", file=sys.stderr)
            return 2
        ids = [fx["fid"] for fx in fixtures]
        if len(set(ids)) != len(ids):
            print("SETUP duplicate fixture id", file=sys.stderr)
            return 2
        prints = [fingerprint(fx["dir"]) for fx in fixtures]
        vdir = root / "variants"
        vdir.mkdir()
        refs = {}
        for tool in TOOLS:
            p = vdir / f"ref-{tool}.py"
            p.write_text(srcs[tool])
            refs[tool] = (p, sha256(p))
        by_tool = {tool: [fx for fx in fixtures if fx["tool"] == tool] for tool in TOOLS}
        ref = {}
        for tool, fxs in by_tool.items():
            for fx, res in zip(fxs, runner.run_all(tool, refs[tool][0], fxs)):
                ref[fx["fid"]] = res
        wrong = 0
        for fx in fixtures:
            res = ref[fx["fid"]]
            ok = res[0] == EXPECT_RC[fx["expect"]] and res[1] == frozenset(fx["defects"])
            wrong += not ok
            print(f"FIXTURE {fx['fid']} tool={fx['tool']} expect={fx['expect']}"
                  f" declared={','.join(sorted(fx['defects'])) or '-'} observed_rc={res[0]}"
                  f" observed={','.join(sorted(res[1])) or '-'} {'ok' if ok else 'WRONG'}")
        null_detected = 0
        for tool, fxs in by_tool.items():
            nv = vdir / f"null-{tool}.py"
            nv.write_text(srcs[tool])
            for fx, res in zip(fxs, runner.run_all(tool, nv, fxs)):
                if res != ref[fx["fid"]]:
                    null_detected += 1
                    print(f"NULL {fx['fid']} differs on a second unmodified run")
        only = set(a.only.split(",")) if a.only else None
        killed = survived = invalid = unattributed = 0
        per_tool = {tool: [0, 0] for tool in TOOLS}  # [frozen, killed]
        adv = {"direct": 0, "indirect": 0, "none": 0}
        for mid, tool, cls, direction, adv_kind, label, _witness, old, new in MUTANTS:
            if only and mid not in only:
                continue
            per_tool.setdefault(tool, [0, 0])[0] += 1
            adv[adv_kind] = adv.get(adv_kind, 0) + 1
            src = srcs.get(tool, "")
            valid_dir = direction in SIMPLE_DIRECTIONS or PAIR.match(direction)
            if tool not in TOOLS or TOOLS[tool] in mism or src.count(old) != 1 or not valid_dir \
                    or old.count("\n") != new.count("\n") \
                    or (direction == "silence") == (cls == "-") or adv_kind not in ("direct", "indirect", "none"):
                invalid += 1
                print(f"MUTANT {mid} {tool} {direction} invalid -- {label[:90]}")
                continue
            mv = vdir / f"{mid}.py"
            mv.write_text(src.replace(old, new, 1))
            try:
                py_compile.compile(str(mv), doraise=True, cfile=str(vdir / f"{mid}.pyc"))
            except py_compile.PyCompileError:
                invalid += 1
                print(f"MUTANT {mid} {tool} {direction} invalid(compile) -- {label[:90]}")
                continue
            digest = sha256(mv)
            start = src[:src.index(old)].count("\n") + 1
            span = set(range(start, start + new.count("\n") + 1))
            fxs = by_tool[tool]
            hits, seen = [], set()
            for fx, res in zip(fxs, runner.run_all(tool, mv, fxs)):
                if exhibits(cls, direction, fx, ref[fx["fid"]], res):
                    hits.append((fx, res))
                else:
                    seen.update(seen_directions(cls, direction, fx, ref[fx["fid"]], res))
            by = None
            why = "span-not-run"
            for fx, res in hits:
                t_rc, t_cls, t_lines, t_sites = runner.run(tool, mv, fx, trace=True, span=span)
                if (t_rc, t_cls) != res or not span & t_lines:
                    continue
                # round-43 leg g: the site record must differ from the reference's over the same span lines
                _r_rc, _r_cls, _r_lines, r_sites = runner.run(tool, refs[tool][0], fx, trace=True, span=span)
                _r_rc, _r_cls, _r_lines, r_sites2 = runner.run(tool, refs[tool][0], fx, trace=True, span=span)
                if tuple(r_sites) != tuple(r_sites2):
                    why = "site-record-unstable"
                    continue
                if SITE_EQUAL(t_sites, r_sites):
                    why = "site-record-equal"
                    continue
                by = fx["fid"]
                break
            if sha256(mv) != digest or sha256(refs[tool][0]) != refs[tool][1]:
                invalid += 1
                print(f"MUTANT {mid} {tool} {direction} invalid(variant changed during the run) -- {label[:90]}")
                continue
            if by:
                killed += 1
                per_tool[tool][1] += 1
                print(f"MUTANT {mid} {tool} {direction} killed by={by} attributed=L{min(span)} value=differs"
                      f" hits={len(hits)} -- {label[:90]}")
            elif hits:
                unattributed += 1
                print(f"MUTANT {mid} {tool} {direction} UNATTRIBUTED hits={len(hits)} last={why}"
                      f" first={hits[0][0]['fid']} span=L{min(span)}-L{max(span)} -- {label[:90]}")
            else:
                survived += 1
                print(f"MUTANT {mid} {tool} {direction} SURVIVED exhibits={','.join(sorted(seen)) or 'none'}"
                      f" -- {label[:90]}")
        tampered = 0
        for fx, before in zip(fixtures, prints):
            if fingerprint(fx["dir"]) != before:
                tampered += 1
                print(f"TAMPERED {fx['fid']} fixture tree changed during the run")
        print(f"BATTERY fixtures={len(fixtures)} wrong={wrong} tampered={tampered} sidechannel={side}")
        total = len(MUTANTS) if not only else len([m for m in MUTANTS if m[0] in only])
        print(f"MUTANTS total={total} killed={killed} survived={survived} invalid={invalid}"
              f" null_detected={null_detected} unattributed={unattributed}")
        print("MUTANTS-BY-TOOL " + " ".join(f"{t}={per_tool.get(t, [0, 0])[1]}/{per_tool.get(t, [0, 0])[0]}"
                                            for t in TOOLS))
        print(f"ADVERTISED direct={adv['direct']} indirect={adv['indirect']} none={adv['none']}")
        after = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
        print(f"PINS-AFTER mismatched={len(after)}")
        if dev:
            print("PREDICATE C1 n/a (non-default battery or mutant subset)")
            return 0 if (wrong == 0 and tampered == 0 and side == 0 and survived == 0 and invalid == 0
                         and unattributed == 0 and null_detected == 0 and not after) else 1
        floors_ok = (TOTAL >= 1 and all(FLOORS.get(t, 0) >= 1 for t in TOOLS) and sum(FLOORS.values()) == TOTAL
                     and all(per_tool.get(t, [0, 0]) == [FLOORS[t], FLOORS[t]] for t in TOOLS))
        good = (not mism and not after and len(MUTANTS) == TOTAL and floors_ok and wrong == 0 and tampered == 0
                and side == 0 and killed == TOTAL and survived == 0 and invalid == 0 and unattributed == 0
                and null_detected == 0)
        print(f"PREDICATE C1 {'pass' if good else 'fail'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
