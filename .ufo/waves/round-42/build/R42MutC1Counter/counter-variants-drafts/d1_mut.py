#!/usr/bin/env python3
"""Round-42 C1 counter (calibration): the behaviours `plans/anchor_digest_check.py` and `plans/order_check.py`
advertise that battery40 does not demonstrate — the 14 directional round-40 wave-2 near-variants that survived
battery40 (`F40XMutAnchor`, `F40XMutLedgerOrder`; re-measured at round-41 wave 1 by `R41PlanNext` §2.2:
`MUTANTS total=20 killed=0 survived=20` for the 20 survivors, 14 of them directional) — killed only by an
ATTRIBUTED kill in a declared direction, every fixture built and every tool run inside a read-only host sandbox.

Frozen predicate (same sentence in plans/round-42-claims.md and in the receipt label):
  C1 passes iff `python3 plans/round42_c1_verify.py --lane .` prints `PINS total=2 mismatched=0`, then
  `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, then
  `MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0`, then
  `MUTANTS-BY-TOOL anchor=9/9 order=5/5`, then `PINS-AFTER mismatched=0`, then `PREDICATE C1 pass`,
  exit 0, measured on a clean clone of the landing tip.

Non-vacuity (round-41 Q31): the predicate binds the mutant total and a per-tool count to literals (`TOTAL`,
`FLOORS`); a copy of this counter with an empty mutant list prints `PREDICATE C1 fail` (freeze control
`control-c1-no-mutants.txt`). The counter's digest is pinned in the round's `frozen-digests.txt`.

New over the round-41 counter (round-41 closure R1; `.ufo/waves/round-41/falsify/F41C1Hardened.md` repairs a-e,
`F41C1Attribution.md` method):
  a  the variant is bound into each tool run by `--ro-bind-data` from an fd, and the counter's variant store,
     slots and builder dir are hidden behind tmpfs, so nothing inside a run can read which variant it is;
  b  `--unshare-ipc`; c  `--tmpfs /run` (host sockets under /run unreachable);
  d  `path_ok` resolves relative argv tokens against the fixture dir (a `../` escape is a contract breach);
  e  streaming content digests in `fingerprint` and the pins;
  f  ATTRIBUTION: a direction hit counts as a kill only when a traced re-run of the mutant on the killing
     fixture (1) reproduces the same (exit, class set) and (2) executes at least one line of the replaced
     span (`sys.settrace` restricted to the tool file, the tracer bound read-only like the variant). A hit
     that fails either is `unattributed` and the mutant does not count as killed.
Both tools execute no fixture code (git plumbing only, hooks and fsmonitor disabled), so repairs a-c close
vectors these two tools do not open; they are carried so the counter stays sound for any later tool list.

Self-assessment under test: each tool's own docstring, the contract the lane cites for it (`SKILL.md` gate
registry rows, `corpus/QUALITY.md` Q27/Q30). Each mutant is one byte-level `old -> new` replacement; its `adv`
cell quotes the advertising sentence with file:line (both tools unchanged since round 39: pins below equal the
round-40 counter's). `adv_kind` as in round 41. A survivor is an advertised-but-undemonstrated behaviour.

Directions (QUALITY Q29), each witnessed before the freeze by `.ufo/waves/round-42/claims/witness/` run through
this counter in development mode (`claims/witness-run.txt`). XO5 and XO6 are `rc-mirror` (the mutant is
STRICTER: reference exits 0, mutant 1), although the round-40 table labelled them `rc-silence`; the round-40
witness text itself records `reference ORDER ok rc=0, mutant ORDER HIT rc=1` for both.
  silence     reference prints class C, the fixture declares C, the mutant does not print C (both exit 0/1)
  rc-silence  fixture `expect=reject`, reference exits 1, mutant exits 0
  rc-mirror   fixture `expect=accept`, reference exits 0, mutant exits 1
  error       fixture `expect=error`, reference exits 2, mutant exits 0 or 1
Classes: anchor — every `class=<C>` token of a `DEFECT ` line; order — none (exit-code directions only; an
order fixture declares `defects: []`).

Battery = `plans/battery42/*.py`, nothing else. Contract: `FIXTURES = [{"fid", "tool": anchor|order,
"expect": accept|reject|error, "defects": [...], "build": build}]`; `build(ctx, d)` fills the EMPTY directory d
and returns the tool argv tail as a list of str. An absolute or relative path in the argv must resolve inside d
(tokens `{WORK}`, `{WORK}/<rel>`, `{WORK:<name>}` as in round 41). `ctx` offers `ctx.init(dest)` (git init -b
master), `ctx.git(repo, *args)` (refuses unless repo is its own toplevel; commits as `fixture
<fixture@kengaku.invalid>` at a fixed date), `ctx.write(path, text|bytes)` and `ctx.sh(*argv, cwd=)`; every path
must lie inside d. No lane clone is offered. `defects` is the exact class set the reference must print; a
fixture whose reference result differs from its declaration is `wrong`. The battery may not import, copy or read
the witness modules.

Isolation as in round 41 (build child and every tool run in `bwrap --ro-bind / /`, lane hidden from builds,
fixed system PATH, HOME read-only and empty, git config pinned, `GIT_CEILING_DIRECTORIES` at the scratch
root, fingerprints after the build and after the last run, pins hashed before and after, `sidechannel` token
scan, `null_detected` on a second unmodified run, `--work` inside the lane refused).

Limits named at the freeze: a kill records a result difference in the declared direction on a fixture that
executes the mutated line, not the fixture's intent; the token scan is a heuristic, so non-author review of
battery42 stays part of admission; a module can still read other copies of the tools elsewhere on the
read-only host. The six text-only ledger variants (XL1-XL6) and the round-40 order rows battery40 already
kills (XO2, XO4) are not in this list; neither is any `state_check.py`/`round_close.py` survivor.

  --battery-dir DIR   load battery modules from DIR instead of plans/battery42 (development; predicate n/a)
  --only X1,XO5       restrict mutants (development; predicate n/a)
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

BATTERY_REL = "plans/battery42"
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
TRACER_SLOT = "/run/k42-tracer.py"
WR = ".ufo/waves/round-42/claims/witness-run.txt"
TOTAL = 14
FLOORS = {"anchor": 9, "order": 5}

TRACER = r'''
import os, runpy, sys
slot, out = sys.argv[1], os.path.join(os.environ["TMPDIR"], "k42-trace.txt")
hit = set()
def local(frame, event, arg):
    if event == "line":
        hit.add(frame.f_lineno)
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
        fh.write(" ".join(str(n) for n in sorted(hit)))
sys.exit(code)
'''

# (id, tool, class, direction, adv_kind, adv [file:line 'quoted sentence'], witness [pre-freeze, committed],
#  old, new)
MUTANTS = [
    ('X1', 'anchor', '-', 'rc-mirror', 'direct',
     "plans/anchor_digest_check.py:50-52 'Provenance row — a committed markdown under corpus/evidence/ whose table line carries this row's id'",
     f"{WR} (MUTANT X1); round-40 source: F40XMutAnchor W1, PROVENANCE.md table line with no pinned URL",
     '    got = [(cap, "provenance-row") for cap, _ in idx["prov_sid"].get(sid, [])]',
     '    got = []'),
    ('X3', 'anchor', '-', 'rc-mirror', 'direct',
     "plans/anchor_digest_check.py:57-58 'A provenance URL (an evidence markdown naming the same <repo>/<subpath>) is consulted when the task.toml route finds nothing'",
     f"{WR} (MUTANT X3); round-40 source: F40XMutAnchor W3, PROVENANCE.md URL, row URL, no task.toml slug",
     '            if (repo, subpath) in idx["prov_url"]:',
     '            if False:'),
    ('X6', 'anchor', 'digest-wrong-capture', 'silence', 'direct',
     "plans/anchor_digest_check.py:89-92 'A 64-hex token that is a committed capture but not this row's is digest-wrong-capture'",
     f"{WR} (MUTANT X6); round-40 source: F40XMutAnchor W6, row anchored on a sibling capture's digest",
     '            elif tok not in row_scope:\n                if tok in allowed:',
     '            elif tok not in row_scope:\n                if False:'),
    ('X7', 'anchor', 'digest-unknown', 'silence', 'direct',
     "plans/anchor_digest_check.py:92-93 'a token that is no committed capture at all is digest-unknown'",
     f"{WR} (MUTANT X7); round-40 source: F40XMutAnchor W7, row anchored on a made-up 64-hex digest",
     '                    defects.append(f"DEFECT {sid} anchor token={tok} class=digest-unknown "',
     '                    defects.append(f"DEFECT {sid} anchor token={tok} class=digest-wrong-capture "'),
    ('X9', 'anchor', '-', 'rc-silence', 'direct',
     "plans/anchor_digest_check.py:34-35 'A row that matches the census regex but does not have 11 cells is a row-malformed defect'",
     f"{WR} (MUTANT X9); round-40 source: F40XMutAnchor W9, a 10-cell row",
     '        if len(r["cells"]) != NCELLS:',
     '        if len(r["cells"]) > NCELLS:'),
    ('X12', 'anchor', '-', 'rc-mirror', 'direct',
     'plans/anchor_digest_check.py:55-56 \'matched **exactly** against the name = "<org>/<task>" a committed task.toml gives\' (slash-less name fallback dropped)',
     f"{WR} (MUTANT X12); round-40 source: F40XMutAnchor W12, task.toml with a slash-less name",
     '            pick = next((n for n in names if "/" in n), names[0] if names else None)',
     '            pick = next((n for n in names if "/" in n), None)'),
    ('X13', 'anchor', '-', 'rc-silence', 'direct',
     "plans/anchor_digest_check.py:73 '`--evidence-ref head` (default) reads HEAD blobs, so an unpromoted capture never counts'",
     f"{WR} (MUTANT X13); round-40 source: F40XMutAnchor W13, capture staged beyond HEAD, default ref",
     '    ap.add_argument("--evidence-ref", choices=("head", "index"), default="head")',
     '    ap.add_argument("--evidence-ref", choices=("head", "index"), default="index")'),
    ('X14', 'anchor', 'erratum-digest-unresolved', 'silence', 'direct',
     "plans/anchor_digest_check.py:111-113 'no 64-hex token on it may be outside A unless it is the cited wrong token of the row it names (erratum-digest-unresolved)'",
     f"{WR} (MUTANT X14); round-40 source: F40XMutAnchor W14, erratum line with an uppercase uncommitted token",
     '            if HEX64_ANY.fullmatch(t) and t not in allowed and t not in cited_wrong:',
     '            if HEX64.fullmatch(t) and t not in allowed and t not in cited_wrong:'),
    ('X15', 'anchor', '-', 'rc-silence', 'direct',
     "plans/anchor_digest_check.py:108-110 'at least one other token that is 64 lowercase hex and a digest **of the capture that row names**'",
     f"{WR} (MUTANT X15); round-40 source: F40XMutAnchor W15, erratum correction citing a sibling row's digest",
     '                     and (t in row_scope if row_scope is not None else t in allowed)]',
     '                     and t in allowed]'),
    ('XO1', 'order', '-', 'rc-silence', 'direct',
     "plans/order_check.py:17,183 'FAIL when the freeze commit (the first commit adding <claims>) already contains <receipt>' (clause skipped)",
     f"{WR} (MUTANT XO1); round-40 source: F40XMutLedgerOrder wit-xo1, freeze commit already carries the receipt",
     '        if git.rc("cat-file", "-e", f"{freeze}:{receipt}") == 0:',
     '        if False and git.rc("cat-file", "-e", f"{freeze}:{receipt}") == 0:'),
    ('XO3', 'order', '-', 'rc-silence', 'direct',
     "plans/order_check.py:18,188 'FAIL when <receipt> was committed before <claims> (pre-registration inverted ...)' (clause skipped)",
     f"{WR} (MUTANT XO3); round-40 source: F40XMutLedgerOrder wit-xo3b, receipt commit an ancestor of the freeze",
     '        if freeze != receipt_commit and git.rc("merge-base", "--is-ancestor", receipt_commit, freeze) == 0:',
     '        if False and freeze != receipt_commit and git.rc("merge-base", "--is-ancestor", receipt_commit, freeze) == 0:'),
    ('XO5', 'order', '-', '0>1', 'direct',
     "plans/order_check.py:116-117 'Every blob ever committed under claims_dir up to and including `upto`' (upto replaced by HEAD: blobs committed AFTER the receipt are scanned too)",
     f"{WR} (MUTANT XO5); round-40 source: F40XMutLedgerOrder wit-xo5, P10-ok claims blob committed after the receipt",
     '    commits = git.out("rev-list", "--reverse", upto, "--", claims_dir).split()',
     '    commits = git.out("rev-list", "--reverse", "HEAD", "--", claims_dir).split()'),
    ('XO6', 'order', '-', 'rc-mirror', 'indirect',
     "plans/order_check.py:52-53 'a gate output line, with or without the C2 counter's `gate: ` echo prefix' (verdict alternation widened with PASS: a `P10 PASS` line, which the gate never prints, becomes a hit)",
     f"{WR} (MUTANT XO6); round-40 source: F40XMutLedgerOrder wit-xo6, claims blob 'P10 PASS receipt unreadable'",
     'GATE_P10 = re.compile(r"^\\s*(?:gate:\\s*)?P10\\s+(DEFECT|ok)\\b[ \\t]*(.*)$")',
     'GATE_P10 = re.compile(r"^\\s*(?:gate:\\s*)?P10\\s+(DEFECT|ok|PASS)\\b[ \\t]*(.*)$")'),
    ('XO7', 'order', '-', 'rc-silence', 'direct',
     "plans/order_check.py:54-55 'a probe receipt line (the probe's per-case verdict record)' (observed value narrowed to pass|fail, so observed=timeout/other verdicts are missed)",
     f"{WR} (MUTANT XO7); round-40 source: F40XMutLedgerOrder wit-xo7, claims blob 'CASE c1 observed=timeout'",
     'CASE_LINE = re.compile(r"^\\s*CASE\\s+\\S+.*\\bobserved=[^\\s]*")',
     'CASE_LINE = re.compile(r"^\\s*CASE\\s+\\S+.*\\bobserved=(?:pass|fail)")'),
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
        self.ENV = dict(self.ENV, GIT_CEILING_DIRECTORIES=str(self._root.parent))

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


def ro_sandbox(writable=(), ro_binds=(), hide=(), ro_data=()):
    argv = [BWRAP, "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--unshare-pid", "--unshare-net",
            "--unshare-ipc", "--tmpfs", "/run",
            "--die-with-parent", "--new-session"]
    for h in hide:
        argv += ["--tmpfs", str(h)]
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


class Runner:
    def __init__(self, root, jobs):
        self.root, self.jobs, self.seq = root, jobs, itertools.count(1)
        self.slots = root / "slots"
        self.slots.mkdir()
        (root / "home").mkdir()
        (root / "work").mkdir()
        (root / "rtmp").mkdir()
        (root / "tracer").mkdir()
        self.tracer = root / "tracer" / "k42-tracer.py"
        self.tracer.write_text(TRACER)
        for tool in TOOLS:
            (self.slots / f"{tool}.py").write_text("# slot\n")

    def env(self, tmp):
        return {"PATH": PATH, "HOME": str(self.root / "home"), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
                "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(tmp),
                "GIT_CEILING_DIRECTORIES": str(self.root),
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_COUNT": "2",
                "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
                "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null"}

    def run(self, tool, variant, fx, trace=False):
        """One sandboxed tool run -> (exit, class set), or (exit, class set, executed line set) when traced."""
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
        slot = self.slots / f"{tool}.py"
        src = open(variant, "rb")
        tsrc = open(self.tracer, "rb")
        lines = None
        try:
            data = ((src.fileno(), slot), (tsrc.fileno(), TRACER_SLOT)) if trace else ((src.fileno(), slot),)
            head = [PY, TRACER_SLOT, str(slot)] if trace else [PY, str(slot)]
            cmd = ro_sandbox(writable=(work, tmp),
                             hide=[p for p in (self.root / "variants", self.root / "slots", self.root / "bin",
                                               self.root / "tracer") if p.exists()],
                             ro_data=data) + head + argv
            try:
                r = subprocess.run(cmd, cwd=str(fx["dir"]), env=self.env(tmp), capture_output=True, text=True,
                                   timeout=600, pass_fds=tuple(fd for fd, _dst in data))
            except subprocess.TimeoutExpired:
                return ("timeout", frozenset(), frozenset()) if trace else ("timeout", frozenset())
            if trace:
                try:
                    lines = frozenset(int(x) for x in (tmp / "k42-trace.txt").read_text().split())
                except (OSError, ValueError):
                    lines = frozenset()
        finally:
            src.close()
            tsrc.close()
            shutil.rmtree(work, ignore_errors=True)
            shutil.rmtree(tmp, ignore_errors=True)
        if trace:
            return (r.returncode, classes(tool, r.stdout), lines)
        return (r.returncode, classes(tool, r.stdout))

    def run_all(self, tool, variant, fixtures):
        with concurrent.futures.ThreadPoolExecutor(self.jobs) as ex:
            return list(ex.map(lambda fx: self.run(tool, variant, fx), fixtures))


def exhibits(cls, direction, fx, ref, mut):
    want = EXPECT_RC.get(fx["expect"])
    m = PAIR.match(direction)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return ref[0] == a and mut[0] == b
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
    bin_dir = root / "bin"
    bin_dir.mkdir(exist_ok=True)
    builder = bin_dir / "builder.py"
    builder.write_text(pathlib.Path(__file__).read_text())
    for f in sorted(bdir.glob("*.py")):
        text = f.read_text().lower()
        hits = [t for t in SIDECHANNEL if t in text]
        if hits:
            side += 1
            print(f"SIDECHANNEL {bdir.name}/{f.name} tokens={','.join(hits)}")
        mod_copy = bin_dir / f"mod_{f.name}"
        mod_copy.write_text(f.read_text())
        dest = root / "fx" / f.stem
        dest.mkdir(parents=True)
        tmp = root / "btmp" / f.stem
        tmp.mkdir(parents=True)
        cmd = ro_sandbox(writable=(dest, tmp), hide=(lane,)) + [PY, str(builder), "--build-module", str(mod_copy),
                                                             "--dest", str(dest)]
        r = subprocess.run(cmd, cwd=str(dest), capture_output=True, text=True, timeout=1800,
                           env={"PATH": PATH, "HOME": "/nonexistent", "TMPDIR": str(tmp), "LANG": "C.UTF-8",
                                "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"})
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
    root = pathlib.Path(tempfile.mkdtemp(prefix="k42-c1-", dir=a.work)).resolve()
    if root.is_relative_to(lane):
        print("SETUP scratch root lies inside the lane; pass --work", file=sys.stderr)
        shutil.rmtree(root, ignore_errors=True)
        return 2
    try:
        runner = Runner(root, a.jobs)
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
            for fx, res in hits:
                t_rc, t_cls, t_lines = runner.run(tool, mv, fx, trace=True)
                if (t_rc, t_cls) == res and span & t_lines:
                    by = fx["fid"]
                    break
            if sha256(mv) != digest or sha256(refs[tool][0]) != refs[tool][1]:
                invalid += 1
                print(f"MUTANT {mid} {tool} {direction} invalid(variant changed during the run) -- {label[:90]}")
                continue
            if by:
                killed += 1
                per_tool[tool][1] += 1
                print(f"MUTANT {mid} {tool} {direction} killed by={by} attributed=L{min(span)} hits={len(hits)}"
                      f" -- {label[:90]}")
            elif hits:
                unattributed += 1
                print(f"MUTANT {mid} {tool} {direction} UNATTRIBUTED hits={len(hits)}"
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
