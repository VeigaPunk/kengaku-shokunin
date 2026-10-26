#!/usr/bin/env python3
"""Round-41 C1 counter (calibration): the behaviours `plans/tip_receipts.py` (round 38, derived mapping round
40) and the CLI half of `plans/sources_adopt.py` advertise that no committed fixture demonstrates — killed only
by an ATTRIBUTED kill in a declared direction, every fixture built and every tool run inside a read-only host
sandbox.

Frozen predicate (same sentence in plans/round-41-claims.md and in the receipt label):
  C1 passes iff `python3 plans/round41_c1_verify.py --lane .` prints `PINS total=2 mismatched=0`, then
  `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, then
  `MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0`, then
  `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`, then `PINS-AFTER mismatched=0`, then `PREDICATE C1 pass`,
  exit 0, measured on a clean clone of the landing tip.

Non-vacuity (round-40 wave-2 `F40CritPlanNext` D1/D2): the predicate binds the mutant total and a per-tool
count to literals (`TOTAL`, `FLOORS`), and the counter refuses a pass when `len(MUTANTS)`, the per-tool counts
or the kill counts differ from them; a copy of this counter with an empty mutant list prints `PREDICATE C1
fail` (freeze control `control-c1-no-mutants.txt`). The counter's own digest is pinned in the round's
`frozen-digests.txt`, so editing the list and the literals together is visible to the closure.

Self-assessment under test: each tool's own contract — `tip_receipts.py`'s docstring and the `sources-adopt`
registry row (`SKILL.md:573`, the eight exit codes) with the parser messages in `main()`. Each mutant is one
byte-level `old -> new` replacement of one pinned tool. `adv_kind` is `direct` when a quoted sentence states
the behaviour, `indirect` when it follows from a quoted sentence plus the code, `none` when nothing advertises it
(round-40 closure R4: an `adv` cell is quoted only for mutants that carry one; the rest are counted apart on the
`ADVERTISED` line). A survivor is an advertised-but-undemonstrated behaviour: the calibration count.

Directions (QUALITY Q29). Every mutant declares one and every one has a pre-freeze witness on record (the
`witness` cell; the counter never reads it).
  silence     reference prints class C, the fixture declares C, the mutant does not print C (both exit 0/1)
  rc-silence  fixture `expect=reject`, reference exits 1, mutant exits 0
  rc-mirror   fixture `expect=accept`, reference exits 0, mutant exits 1
  error       fixture `expect=error`, reference exits 2, mutant exits 0 or 1
  A>B         (digits) fixture expects exit A, reference exits A, mutant exits exactly B — the sources tool's
              eight advertised exit codes need exact pairs
Kill rule: mutant M is killed by fixture f iff f's `tool` is M's tool and (reference result, mutant result) on
f satisfies M's declared direction. A survivor prints the other directions it exhibited on any fixture.

Classes (`silence` only; the tip-receipts tool): `map:<rel>:<origin>` for a `--list` line `receipt <rel>
kind=... origin=<origin>`; `skip:<rel>:<reason>` for `receipt <rel> skip reason=<reason>` (reason up to the
first character outside [A-Za-z0-9-]); `equal:<rel>`, `differ:<rel>`; `control:<verdict>`. The sources tool
uses exit-code directions only (its class set is always empty).

Battery = `plans/battery41/*.py`, nothing else. Contract: `FIXTURES = [{"fid", "tool": receipts|sources,
"expect": accept|reject|error|exit-3..exit-9, "defects": [...], "build": build}]`; `build(ctx, d)` fills the
EMPTY directory d and returns the tool argv tail as a list of str (anything else is a contract breach — round-40
`R40RevCounters`). An absolute path in the argv must lie inside d, except a token `{WORK}` or `{WORK}/<rel>`,
which the counter replaces per run with a fresh scratch path outside d: `{WORK}` alone is absent, `{WORK}/<rel>`
sits in an existing empty directory, and `{WORK:<name>}` pre-creates directory `<name>` there. `ctx` offers `ctx.init(dest)` (git init -b master), `ctx.git(repo, *args)`
(refuses unless `rev-parse --show-toplevel` of repo is repo itself; commits as `fixture
<fixture@kengaku.invalid>`), `ctx.write(path, text)` and `ctx.sh(*argv, cwd=)`; every path must lie inside d.
There is no lane clone this round: no fixture needs one, and none can read a tool's program text through it.
`defects` is the exact class set the reference must print; a fixture whose reference result differs from its
declaration (exit code or class set) is `wrong`.

Isolation (round-40 closure R1/R2; `R40CritC1Counter` A1/A2, `R40SentinelCounter`, `R40RevCounters`):
  * every module is built by a child in `bwrap --ro-bind / / --unshare-pid --unshare-net --die-with-parent`
    with the lane hidden (`--tmpfs <lane>`), its own fixture directory and a private tmp dir the only
    writable paths; the child runs a copy of this counter and a copy of the module, never the lane's files;
    `HOME=/nonexistent`, PATH = the fixed system PATH below.
  * every tool run (reference, null, mutants) runs in `bwrap --ro-bind / /` with only its per-run work dir
    and private tmp dir writable, `--unshare-pid --unshare-net --die-with-parent`, the variant bound
    read-only at ONE fixed slot path, PATH = the fixed system PATH (so no shared PATH directory such as
    `~/.local/bin` can shadow `git` or `python3`, and nothing a run does can write one), HOME a read-only
    empty dir, git with `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `core.fsmonitor=false`,
    `core.hooksPath=/dev/null`, `GIT_CEILING_DIRECTORIES` at the counter's scratch root.
  * fixture trees are fingerprinted by path, mode, size, link target AND content digest (`.git/index`,
    `*.lock`, `__pycache__` excluded) after the build and after the last run; a change is `tampered`.
  * the two tool pins are hashed before AND after the run (`PINS-AFTER`), every variant re-hashed after its
    runs; `sidechannel` counts battery41 sources carrying a SIDECHANNEL token; `null_detected` counts fixtures
    whose second unmodified run differs from the first.
  * `--work` inside the lane is refused (the build sandbox hides the lane).

Limits named at the freeze: a kill records a result difference in the declared direction, not the fixture's
intent; the token scan is a heuristic, so non-author code review of battery41 stays part of admission; a
module can still read other copies of the tools elsewhere on the read-only host (no network, no write). S10
(`check()`'s requested-id refusal) is NOT frozen: its witness showed it rc-equivalent (main's `build_block`
missing-id refusal returns exit 5 as well), recorded in `claims/witness-run.txt`.

  --battery-dir DIR   load battery modules from DIR instead of plans/battery41 (development; predicate n/a)
  --only T01,S02      restrict mutants (development; predicate n/a)
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

BATTERY_REL = "plans/battery41"
TOOLS = {
    "receipts": "plans/tip_receipts.py",
    "sources": "plans/sources_adopt.py",
}
PINS = {
    "plans/tip_receipts.py": "e4f49714299ca1f2a93303c59ac07e691cc45d6126ccf24e5eecab93733f88f3",
    "plans/sources_adopt.py": "38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0",
}
SIDECHANNEL = ("/proc", "ppid", "cmdline", "psutil", "environ", "fsmonitor", "hookspath", "filter.",
               "gitattributes", "core.", "alias.", "setsid", "daemon", "fork", "nohup", "socket",
               "/home/", ".local", "__file__", "inspect", "importlib", "sys.path", "ctypes", "chmod")
SIMPLE_DIRECTIONS = ("silence", "rc-silence", "rc-mirror", "error")
PAIR = re.compile(r"^(\d)>(\d)$")
EXPECT_RC = {"accept": 0, "reject": 1, "error": 2, **{f"exit-{n}": n for n in range(3, 10)}}
WORK_TOKEN = re.compile(r"^\{WORK(?::([a-z]+))?\}(/[A-Za-z0-9._/-]+)?$")
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
BWRAP = "/usr/bin/bwrap"
PY = "/usr/bin/python3"
TR = "plans/tip_receipts.py"
SA = "plans/sources_adopt.py"
SK = "SKILL.md:573"
WR = ".ufo/waves/round-41/claims/witness-run.txt"
TOTAL = 23
FLOORS = {"receipts": 13, "sources": 10}

# (id, tool, class, direction, adv_kind, adv [file:line 'quoted sentence'], witness [pre-freeze, committed],
#  old, new)
MUTANTS = [
    ("T01", "receipts", "-", "error", "direct",
     f"{TR}:30-32 '2 usage/setup (lane not a git work-tree root, no `corpus/evidence/`, absent git, clone or "
     "cleanup failure, unknown `--tamper` id)'",
     f"{WR} (MUTANT T01: killed in its declared direction by a witness fixture)",
     "    raise SystemExit(2)", "    raise SystemExit(0)"),
    ("T02", "receipts", "-", "error", "direct",
     f"{TR}:30-31 '2 usage/setup (..., no `corpus/evidence/`, ...)'",
     f"{WR} (MUTANT T02: killed in its declared direction by a witness fixture)",
     "    if not (lane / EVIDENCE).is_dir():", "    if False:"),
    ("T03", "receipts", "-", "rc-silence", "direct",
     f"{TR}:30 '1 a `differ`, a failed control, or a probe that did not complete (exit != 0)'",
     f"{WR} (MUTANT T03: killed in its declared direction by a witness fixture)",
     '            if run["exit"] != 0:', "            if False:"),
    ("T04", "receipts", "-", "rc-mirror", "direct",
     f"{TR}:21-23 'absolute mkdtemp paths are masked on both sides, so equality after masking is a "
     "reproducibility claim up to those paths'",
     f"{WR} (MUTANT T04: killed in its declared direction by a witness fixture)",
     "                if mask(fresh) == mask(blob):", "                if mask(fresh) != mask(blob):"),
    ("T05", "receipts", "-", "error", "direct",
     f"{TR}:31-32 '2 usage/setup (..., unknown `--tamper` id)'",
     f"{WR} (MUTANT T05: killed in its declared direction by a witness fixture)",
     "            if unknown:", "            if False:"),
    ("T06", "receipts", "-", "rc-silence", "indirect",
     f"{TR}:29-30 '0 every mapped receipt reproduces ... and the control reports `differ`; 1 ... a failed "
     "control' (an unavailable control on an empty receipt is a failed control)",
     f"{WR} (MUTANT T06: killed in its declared direction by a witness fixture)",
     "    return 0 if d == 0 and control_ok else 1", "    return 0 if d == 0 or control_ok else 1"),
    ("T07", "receipts", "-", "error", "direct",
     f"{TR}:30-31 '2 usage/setup (lane not a git work-tree root, ...)'",
     f"{WR} (MUTANT T07: killed in its declared direction by a witness fixture)",
     "    if not top or pathlib.Path(top).resolve() != lane.resolve():", "    if False:"),
    ("T08", "receipts", "-", "rc-mirror", "direct",
     f"{TR}:19-21 'A mapped receipt whose script is gone, whose dependency is absent, ... is printed as `skip` "
     "with the reason.'",
     f"{WR} (MUTANT T08: killed in its declared direction by a witness fixture)",
     "            elif shutil.which(argv[0]) is None:", "            elif False:"),
    ("T09", "receipts", "skip:corpus/evidence/r/foo-probe.txt:no-committed-re-run-command", "silence", "direct",
     f"{TR}:13-14 'if its own basename resolves to exactly one committed `plans/*.py` probe'",
     f"{WR} (MUTANT T09: killed in its declared direction by a witness fixture)",
     "        if len(hit) == 1:", "        if len(hit) >= 1:"),
    ("T10", "receipts", "map:corpus/evidence/r/foo-probe.txt:derived", "silence", "direct",
     f"{TR}:15-16 'with non-alphanumerics dropped and case folded, the receipt stem `git-leak-probe` and the "
     "script stem `git_leak_probe` are the same token'",
     f"{WR} (MUTANT T10: killed in its declared direction by a witness fixture)",
     'STEM_RE = re.compile(r"[^a-z0-9]+")', 'STEM_RE = re.compile(r"[^a-z0-9_]+")'),
    ("T11", "receipts", "map:corpus/evidence/round35/tb2-grader-probe.txt:table", "silence", "direct",
     f"{TR}:13-14 'A file enters the byte-comparison if the RECEIPTS table maps it ... or — the table being an "
     "override list, not a census — if its own basename resolves'",
     f"{WR} (MUTANT T11: killed in its declared direction by a witness fixture)",
     "        if rel in RECEIPTS:\n            continue", "        if False:\n            continue"),
    ("T12", "receipts", "skip:corpus/evidence/r/foo-probe.log:no-committed-re-run-command", "silence", "direct",
     f"{TR}:12 'Population, stated mechanically: committed files `corpus/evidence/**/*probe*.{{txt,log}}`.'",
     f"{WR} (MUTANT T12: killed in its declared direction by a witness fixture)",
     'CANDIDATE_RE = re.compile(r"probe.*\\.(?:txt|log)$", re.IGNORECASE)',
     'CANDIDATE_RE = re.compile(r"probe.*\\.(?:txt)$", re.IGNORECASE)'),
    ("T13", "receipts", "-", "rc-mirror", "direct",
     f"{TR}:26-27 'the comparator must answer `differ`. ... A control that answers `equal` exits 1.'",
     f"{WR} (MUTANT T13: killed in its declared direction by a witness fixture)",
     "            control_ok = control_ok and not same", "            control_ok = control_ok and same"),
    ("S01", "sources", "-", "2>0", "direct",
     f"{SK} '`2` usage error'; {SA}:1020-1021 '# Exclusive: before this guard, a combined invocation silently "
     "ignored the registry'",
     f"{WR} (MUTANT S01: killed in its declared direction by a witness fixture)",
     "        if args.registry or args.package:", "        if False:"),
    ("S02", "sources", "-", "2>1", "direct",
     f"{SK} '`2` usage error'; {SA}:1042 '--registry and --package are required unless --selftest'",
     f"{WR} (MUTANT S02: killed in its declared direction by a witness fixture)",
     "    if not args.registry or not args.package:", "    if False:"),
    ("S03", "sources", "-", "2>5", "direct",
     f"{SK} '`2` usage error'; {SA}:1053 '--access-date must be an ISO date (YYYY-MM-DD)'",
     f"{WR} (MUTANT S03: killed in its declared direction by a witness fixture)",
     "    if not ISO_DATE_RE.match(args.access_date):", "    if False:"),
    ("S04", "sources", "-", "2>0", "direct",
     f"{SK} '`2` usage error'; {SA}:1035-1036 '`--url-map` alone reached neither mode before this guard: given "
     "with --registry it was accepted and silently ignored'",
     f"{WR} (MUTANT S04: killed in its declared direction by a witness fixture)",
     '    if args.url_map:\n        parser.error("--url-map needs', '    if False:\n        parser.error("--url-map needs'),
    ("S05", "sources", "-", "2>0", "direct",
     f"{SK} '`2` usage error'; {SA}:1051 '--entries is required when --admit-ids is given (used-by has no "
     "fallback)'",
     f"{WR} (MUTANT S05: killed in its declared direction by a witness fixture)",
     "    if not args.entries:", "    if False:"),
    ("S06", "sources", "-", "2>0", "direct",
     f"{SK} '`2` usage error'; {SA}:1059 '--recheck must be an ISO date, <N>d, or a known symbolic cadence'",
     f"{WR} (MUTANT S06: killed in its declared direction by a witness fixture)",
     "    if not (\n        ISO_DATE_RE.match(args.recheck)", "    if False and (\n        ISO_DATE_RE.match(args.recheck)"),
    ("S07", "sources", "-", "3>0", "direct",
     f"{SK} '`3` staged/registry id collision'",
     f"{WR} (MUTANT S07: killed in its declared direction by a witness fixture)",
     "    if code != EXIT_OK or not want:", "    if code != EXIT_OK and not want:"),
    ("S08", "sources", "-", "2>1", "direct",
     f"{SK} '`2` usage error'; {SA}:1019 '--quote-file and --artifact must be given together'",
     f"{WR} (MUTANT S08: killed in its declared direction by a witness fixture)",
     "        if not (args.quote_file and args.artifact):", "        if False:"),
    ("S09", "sources", "-", "2>9", "direct",
     f"{SK} '`2` usage error or unreadable quote artifact'; {SA}:1028 'QUOTE problem=' (an unreadable --url-map)",
     f"{WR} (MUTANT S09: killed in its declared direction by a witness fixture)",
     '            if problem:\n                print(f"QUOTE problem={problem}")',
     '            if False:\n                print(f"QUOTE problem={problem}")'),
    ("S11", "sources", "-", "5>0", "indirect",
     f"{SK} '`5` requested id absent' (main() also refuses a requested row that is not `mined` or not opened "
     "on --access-date with exit 5)",
     f"{WR} (MUTANT S11: killed in its declared direction by a witness fixture)",
     '    if missing:\n        print(f"  missing:', '    if False:\n        print(f"  missing:'),
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
    mod = load(module, f"kengaku_b41_{module.stem}")
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
    if tool != "receipts":
        return frozenset(got)
    for line in out.splitlines():
        m = re.match(r"^receipt (\S+) kind=\S+ script=\S+ origin=(\S+)", line)
        if m:
            got.add(f"map:{m.group(1)}:{m.group(2)}")
            continue
        m = re.match(r"^receipt (\S+) skip reason=([A-Za-z0-9-]+)", line)
        if m:
            got.add(f"skip:{m.group(1)}:{m.group(2)}")
            continue
        m = re.match(r"^receipt (\S+) (equal|differ)\b", line)
        if m:
            got.add(f"{m.group(2)}:{m.group(1)}")
            continue
        m = re.match(r"^control receipt=\S+ .*verdict=(\S+)", line)
        if m:
            got.add(f"control:{m.group(1)}")
    return frozenset(got)


class Runner:
    def __init__(self, root, jobs):
        self.root, self.jobs, self.seq = root, jobs, itertools.count(1)
        self.slots = root / "slots"
        self.slots.mkdir()
        (root / "home").mkdir()
        (root / "work").mkdir()
        (root / "rtmp").mkdir()
        for tool in TOOLS:
            (self.slots / f"{tool}.py").write_text("# slot\n")

    def env(self, tmp):
        return {"PATH": PATH, "HOME": str(self.root / "home"), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
                "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(tmp),
                "GIT_CEILING_DIRECTORIES": str(self.root),
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_COUNT": "2",
                "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
                "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null"}

    def run(self, tool, variant, fx):
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
        try:
            cmd = ro_sandbox(writable=(work, tmp),
                             hide=[p for p in (self.root / "variants", self.root / "slots", self.root / "bin")
                                   if p.exists()],
                             ro_data=((src.fileno(), slot),)) + [PY, str(slot), *argv]
            try:
                r = subprocess.run(cmd, cwd=str(fx["dir"]), env=self.env(tmp), capture_output=True, text=True,
                                   timeout=600, pass_fds=(src.fileno(),))
            except subprocess.TimeoutExpired:
                return ("timeout", frozenset())
        finally:
            src.close()
            shutil.rmtree(work, ignore_errors=True)
            shutil.rmtree(tmp, ignore_errors=True)
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
                  and (fx.get("tool") == "receipts" or not fx["defects"])
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
    root = pathlib.Path(tempfile.mkdtemp(prefix="k41-c1-", dir=a.work)).resolve()
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
        killed = survived = invalid = 0
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
            fxs = by_tool[tool]
            by, seen = None, set()
            for fx, res in zip(fxs, runner.run_all(tool, mv, fxs)):
                if exhibits(cls, direction, fx, ref[fx["fid"]], res):
                    by = by or fx["fid"]
                else:
                    seen.update(seen_directions(cls, direction, fx, ref[fx["fid"]], res))
            if sha256(mv) != digest or sha256(refs[tool][0]) != refs[tool][1]:
                invalid += 1
                print(f"MUTANT {mid} {tool} {direction} invalid(variant changed during the run) -- {label[:90]}")
                continue
            if by:
                killed += 1
                per_tool[tool][1] += 1
                print(f"MUTANT {mid} {tool} {direction} killed by={by} -- {label[:90]}")
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
              f" null_detected={null_detected}")
        print("MUTANTS-BY-TOOL " + " ".join(f"{t}={per_tool.get(t, [0, 0])[1]}/{per_tool.get(t, [0, 0])[0]}"
                                            for t in TOOLS))
        print(f"ADVERTISED direct={adv['direct']} indirect={adv['indirect']} none={adv['none']}")
        after = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
        print(f"PINS-AFTER mismatched={len(after)}")
        if dev:
            print("PREDICATE C1 n/a (non-default battery or mutant subset)")
            return 0 if (wrong == 0 and tampered == 0 and side == 0 and survived == 0 and invalid == 0
                         and null_detected == 0 and not after) else 1
        floors_ok = (TOTAL >= 1 and all(FLOORS.get(t, 0) >= 1 for t in TOOLS) and sum(FLOORS.values()) == TOTAL
                     and all(per_tool.get(t, [0, 0]) == [FLOORS[t], FLOORS[t]] for t in TOOLS))
        good = (not mism and not after and len(MUTANTS) == TOTAL and floors_ok and wrong == 0 and tampered == 0
                and side == 0 and killed == TOTAL and survived == 0 and invalid == 0 and null_detected == 0)
        print(f"PREDICATE C1 {'pass' if good else 'fail'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
