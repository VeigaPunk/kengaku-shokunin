#!/usr/bin/env python3
"""Round-43 C1 counter (calibration): nine behaviours `plans/anchor_digest_check.py` and `plans/order_check.py`
advertise that no landed battery demonstrates — the behaviour-bearing near-variants that survived battery42 in
round-42 wave 2 (`.ufo/waves/round-42/falsify/F42XMutNear.md` §3-§4: 25 near-variants, 15 killed, 10 survived, of
which NA12 is a null mutant) — killed only by an ATTRIBUTED kill in a declared direction, every fixture built and
every tool run inside a read-only host sandbox.

Frozen predicate (same sentence in plans/round-43-claims.md and in the receipt label):
  C1 passes iff `python3 plans/round43_c1_verify.py --lane .` prints `PINS total=2 mismatched=0`, then
  `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, then
  `MUTANTS total=9 killed=9 survived=0 invalid=0 null_detected=0 unattributed=0`, then
  `MUTANTS-BY-TOOL anchor=6/6 order=3/3`, then `PINS-AFTER mismatched=0`, then `PREDICATE C1 pass`,
  exit 0, measured on a clean clone of the landing tip.

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

Battery = `plans/battery43/*.py`, nothing else. Contract: `FIXTURES = [{"fid", "tool": anchor|order,
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
heuristic, so non-author review of battery43 stays part of admission; a module can still read other copies of
the tools elsewhere on the read-only host; R1 pins four keys, not git's whole key space. NA12 (null, unreachable
line) and the 15 near-variants battery42 already kills are not in this list; neither is any
`state_check.py`/`round_close.py` survivor nor the `u = 18` unmutated advertised behaviours (`R42CritEquiv` §3).

  --battery-dir DIR   load battery modules from DIR instead of plans/battery43 (development; predicate n/a)
  --only NA1,NO5      restrict mutants (development; predicate n/a)
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

BATTERY_REL = "plans/battery43"
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
TRACER_SLOT = "/run/k43-tracer.py"
WR = ".ufo/waves/round-43/claims/witness-run.txt"
TOTAL = 9
FLOORS = {"anchor": 6, "order": 3}


def SITE_EQUAL(mut_sites, ref_sites):
    """Round-43 leg g: equal site records mean the replaced span ran without changing what followed it."""
    return tuple(mut_sites) == tuple(ref_sites)

# --- F42C1Hardened banner (round-42 wave 2, falsify), carried into round 43 unchanged except the k43 slot names.
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
BUILDER_SLOT = "/run/k43-builder.py"
SLOT = "/run/k43-slot.py"

TRACER = r'''
import hashlib, os, re, runpy, sys
slot, out = sys.argv[1], os.path.join(os.environ["TMPDIR"], "k43-trace.txt")
span = frozenset(int(x) for x in os.environ.get("K43_SPAN", "").split(",") if x)
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
    ('NA1', 'anchor', 'row-malformed', 'silence', 'direct',
     "plans/anchor_digest_check.py:34-35 'A row that matches the census regex but does not have 11 cells is a `row-malformed` defect' (`!=` -> `<`: an over-long row is no longer malformed)",
     f"{WR} (MUTANT NA1); round-42 wave-2 F42XMutNear NA1, a 12-cell row",
     '        if len(r["cells"]) != NCELLS:',
     '        if len(r["cells"]) < NCELLS:'),
    ('NA5', 'anchor', '-', 'rc-mirror', 'direct',
     'plans/anchor_digest_check.py:54-56 \'The task component of `<subpath>` is matched **exactly** against the `name = "<org>/<task>"` a committed `task.toml` gives\' (slug keeps the `<org>/` prefix, so a slashed name never binds)',
     f"{WR} (MUTANT NA5); round-42 wave-2 F42XMutNear NA5, task.toml name with a slash",
     '                slugs[d] = pick.rsplit("/", 1)[-1]',
     '                slugs[d] = pick'),
    ('NA7', 'anchor', '-', 'rc-mirror', 'direct',
     "plans/anchor_digest_check.py:112-113 'no 64-hex token on it may be outside A unless it is the cited wrong token of the row it names' (a committed token in A is flagged too)",
     f"{WR} (MUTANT NA7); round-42 wave-2 F42XMutNear NA7, a valid erratum on a green lane",
     '            if HEX64_ANY.fullmatch(t) and t not in allowed and t not in cited_wrong:',
     '            if HEX64_ANY.fullmatch(t) and t not in cited_wrong:'),
    ('NA18', 'anchor', '-', 'rc-mirror', 'indirect',
     "plans/anchor_digest_check.py:53-54 'a `raw.githubusercontent.com/<owner>/<repo>/<commit>/<subpath>` ... URL anywhere in the row' (commit segment widened from 7-40 to 4-40 hex: a 4-6 hex segment now binds)",
     f"{WR} (MUTANT NA18); round-42 wave-2 F42XMutNear NA18, a URL with a short commit segment",
     'URL_RAW = re.compile(r"https?://raw\\.githubusercontent\\.com/([^/\\s|`)\\]]+)/([^/\\s|`)\\]]+)"\n                      r"/([0-9A-Fa-f]{7,40})/([^\\s|`)\\]]+)")',
     'URL_RAW = re.compile(r"https?://raw\\.githubusercontent\\.com/([^/\\s|`)\\]]+)/([^/\\s|`)\\]]+)"\n                      r"/([0-9A-Fa-f]{4,40})/([^\\s|`)\\]]+)")'),
    ('NA20', 'anchor', '-', 'rc-mirror', 'direct',
     "plans/anchor_digest_check.py:108-110 'An erratum for S<id> exempts that row's anchor token from *every* anchor class above when it carries the row's exact wrong token' (exemption never granted)",
     f"{WR} (MUTANT NA20); round-42 wave-2 F42XMutNear NA20, a lane kept green by a valid erratum",
     '            exempt.setdefault(sid, (path, lineno, cited_wrong[0], supported[0]))',
     '            pass'),
    ('NA21', 'anchor', '-', 'rc-mirror', 'direct',
     "plans/anchor_digest_check.py:108-109 'An erratum for S<id> exempts that row's anchor token ... when it carries the row's exact wrong token' (wrong-token membership keyed on the row ids, not the row's tokens)",
     f"{WR} (MUTANT NA21); round-42 wave-2 F42XMutNear NA21, a lane kept green by a valid erratum",
     '        cited_wrong = [t for t, _ in toks if t in anchor_tokens.get(sid, ())]',
     '        cited_wrong = [t for t, _ in toks if t in anchor_tokens]'),
    ('NO5', 'order', '-', 'rc-silence', 'direct',
     "plans/order_check.py:14-16 'FAIL when any file committed under `.ufo/waves/round-NN/claims/` at or before the first commit that adds <receipt> proves the probe executed' (only the oldest claims commit scanned)",
     f"{WR} (MUTANT NO5); round-42 wave-2 F42XMutNear NO5, a forbidden line added in a later claims commit",
     '    for commit in commits:',
     '    for commit in commits[:1]:'),
    ('NO7', 'order', '-', 'rc-mirror', 'direct',
     "plans/order_check.py:56-57 'The one P10 detail the gate prints before executing anything, optionally echoing the receipt path (`receipt unreadable: <path>` is the shape P2 uses' (the echoed shape no longer excused)",
     f"{WR} (MUTANT NO7); round-42 wave-2 F42XMutNear NO7, a P2-shaped excuse line",
     'EXECUTED_EXCUSE = re.compile(r"^receipt unreadable(?:: \\S+)?$")',
     'EXECUTED_EXCUSE = re.compile(r"^receipt unreadable$")'),
    ('NO22', 'order', '-', 'rc-silence', 'direct',
     "plans/order_check.py:15-16 'a gate `P10` line whose detail is anything other than `receipt unreadable`' (the gate-line branch disabled; CASE lines only)",
     f"{WR} (MUTANT NO22); round-42 wave-2 F42XMutNear NO22, a gate-P10-only claims blob",
     '        if m:\n            detail = m.group(2).strip()',
     '        if False:\n            detail = m.group(2).strip()'),
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


def repo_breach(d):
    """F42C1Hardened R4 (R42CritC1Counter V1b): a fixture's repo must stay rooted at its own directory.

    `path_ok` only validates the argv tokens; a repo whose `.git/config` carries `core.worktree` makes
    `git rev-parse --show-toplevel` (order_check.py:152) adopt a root outside the fixture, so the measured
    scenario would live outside `d` while the counter printed `wrong=0`.
    """
    repos = []
    for top, dirs, files in os.walk(d):
        rel = os.path.relpath(top, d)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        if ".git" in dirs or ".git" in files:
            repos.append(pathlib.Path(top))
        dirs[:] = sorted(x for x in dirs if x != ".git")
        if depth >= 3:
            dirs[:] = []
    for repo in repos:
        repo = repo.resolve()
        top = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, env=PIN_CHECK_ENV)
        if top.returncode == 0:
            seen = top.stdout.strip()
            if pathlib.Path(seen).resolve() != repo:
                return f"{repo.name}/rev-parse --show-toplevel={seen}"
        wt = subprocess.run(["git", "-C", str(repo), "config", "--get", "core.worktree"],
                            capture_output=True, text=True, env=PIN_CHECK_ENV)
        val = wt.stdout.strip() if wt.returncode == 0 else ""
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


def order_argv_breach(d, argv):
    """Round 43 leg i (R42CritC1Counter §1 substitutes): an order fixture's `--claims` and `--receipt` must each
    name a BLOB at HEAD of the `--lane` repo when that path exists at HEAD at all (a missing path stays the tool's
    own setup error, exit 2; a directory standing in for a file is refused here)."""
    vals, k = {}, 0
    while k < len(argv):
        t = argv[k]
        if t in ("--lane", "--claims", "--receipt") and k + 1 < len(argv):
            vals[t], k = argv[k + 1], k + 2
            continue
        if "=" in t and t.split("=", 1)[0] in ("--lane", "--claims", "--receipt"):
            vals[t.split("=", 1)[0]] = t.split("=", 1)[1]
        k += 1
    lane = pathlib.Path(vals.get("--lane", "."))
    lane = lane if lane.is_absolute() else d / lane
    for opt in ("--claims", "--receipt"):
        if opt not in vals:
            continue
        r = subprocess.run(["git", "-C", str(lane), "cat-file", "-t", f"HEAD:{vals[opt]}"],
                           capture_output=True, text=True, env=PIN_CHECK_ENV)
        if r.returncode == 0 and r.stdout.strip() != "blob":
            return f"{opt} {vals[opt]} is a {r.stdout.strip()} at HEAD, not a blob"
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
        self.tracer = root / "tracer" / "k43-tracer.py"
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
            e["K43_SPAN"] = ",".join(str(x) for x in sorted(span))
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
                    raw = (tmp / "k43-trace.txt").read_text().split("\n")
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
        bfd = os.memfd_create("k43-builder", 0)
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
            breach = repo_breach(d) or symlink_breach(d) \
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
    root = pathlib.Path(tempfile.mkdtemp(prefix="k43-c1-", dir=a.work)).resolve()
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
