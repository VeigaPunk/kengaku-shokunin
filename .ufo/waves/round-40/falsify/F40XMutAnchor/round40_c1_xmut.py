#!/usr/bin/env python3
"""Round-40 C1 counter (calibration): the behaviours the lane's three tripwire tools advertise that no committed
fixture demonstrates — `plans/anchor_digest_check.py`, `plans/ledger_tip.py`, `plans/order_check.py` — killed
only by an ATTRIBUTED kill in a declared direction, with every fixture built in a pid-namespaced child and every
tool run sandboxed at one fixed path.

Frozen predicate (same sentence in plans/round-40-claims.md and in the receipt label):
  C1 passes iff `python3 plans/round40_c1_verify.py --lane .` prints `PINS total=3 mismatched=0`, then
  `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, then
  `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`, then `PINS-AFTER mismatched=0`, then
  `PREDICATE C1 pass`, exit 0, measured on a clean clone of the landing tip.

Self-assessment under test: each tool's own docstring, which is the contract the lane cites for it
(`SKILL.md` gate/probe registry rows, `corpus/QUALITY.md` Q27/Q30). Each mutant is one byte-level `old -> new`
replacement of one pinned tool; its `adv` cell quotes the advertising sentence with file:line at the freeze. A
survivor is an advertised-but-undemonstrated behaviour: the calibration count.

Directions (QUALITY Q29). Every mutant declares one, and every one has a pre-freeze witness on record (the
`witness` cell; the counter never reads it). `C` is the mutant's class (anchor tool: the `class=` token of a
`DEFECT` line; ledger and order mutants use exit-code directions only).
  silence     reference prints class C, the fixture declares C, the mutant does not print C (both exit 0/1)
  rc-silence  fixture `expect=reject`, reference exits 1, mutant exits 0
  rc-mirror   fixture `expect=accept`, reference exits 0, mutant exits 1
  error       fixture `expect=error`, reference exits 2, mutant exits 0 or 1
  rc-error    fixture `expect=accept`, reference exits 0, mutant exits 2
Kill rule: mutant M is killed by fixture f iff f's `tool` is M's tool and (reference result, mutant result) on f
satisfies M's declared direction. A survivor prints the other directions it exhibited on any fixture
(`exhibits=`), so a mislabelled direction is visible in the receipt.

Battery = `plans/battery40/*.py`, nothing else. Contract: `FIXTURES = [{"fid", "tool": anchor|ledger|order,
"expect": accept|reject|error, "defects": [...], "build": build}]`; `build(ctx, d)` fills the EMPTY directory
d and returns the tool argv tail (everything after the tool path). An absolute path in the argv must lie inside
d, except the literal token `{WORK}`, which the counter replaces per run with a fresh, absent scratch path
outside d (ledger `--work`), and `{WORK:<name>}` (name = lowercase letters), replaced by a fresh scratch path
outside d that already holds an empty directory `<name>` (the ledger's existing-clone-dir refusal). `ctx` offers `ctx.lane` (a read-only shared clone of the lane at HEAD),
`ctx.clone(dest)` (`git clone --shared` of it), `ctx.init(dest)`, `ctx.git(repo, *args)` (refuses unless
`rev-parse --show-toplevel` of repo is repo itself; commits as `fixture <fixture@kengaku.invalid>`) and
`ctx.sh(*argv, cwd=)`. `defects` is the exact class set the reference must print: anchor `class=` tokens;
ledger `NO:<row id>` for each row line with `agree=NO`; order `hit:<kind>` for each `ORDER HIT` kind and
`fail:<name>` for each named `ORDER FAIL` line. A fixture whose reference result differs from its
declaration (exit code or class set) is `wrong`.

Soundness repairs over the round-39 counter (`.ufo/waves/round-39/build/R39CritC1Counter.md` §2-§5, routed as
round-39 closure R4):
  A1  every module is built by a child running inside `bwrap --unshare-pid --die-with-parent`: when the child
      exits its pid namespace dies, so no process a fixture started survives into the reference or mutant
      runs. Each fixture tree is fingerprinted (path, mode, size, mtime, link target; `.git/index` and
      `__pycache__` excluded) after the build and again after the last run; a change is `tampered`.
  A3  no battery file is ever imported in-process: only `plans/battery40/*.py`, each in its own child.
  A4  the three tool pins are hashed before AND after the run (`PINS-AFTER`), and every tool variant file is
      digest-checked after its runs.
  A5  the counter owns every fixture directory (dest/fNNN by fixture index); the child reports only fid,
      tool, expect, defects and argv, never a directory.
Every tool run (reference, null, mutants) is itself sandboxed (`bwrap --unshare-pid --die-with-parent`) with
the variant bound read-only at ONE fixed path, so a fixture cannot tell reference from mutant by path; git
runs with `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `core.fsmonitor=false`,
`core.hooksPath=/dev/null`. `sidechannel` counts battery40 sources carrying any of SIDECHANNEL (a token
heuristic for process-table, environment and git-execution hooks); non-author code review stays in admission.
`null_detected` counts fixtures whose second run of the unmodified tool differs from the first.

Limits named at the freeze: a kill records a result difference in the declared direction, not the fixture's
intent; git filter/attribute execution beyond the two disabled hooks is caught only by the token scan; text-only
mutants (summary-line counts, labels) are not in the list because no direction here reads them. Tool runs keep
the caller's PATH and HOME (the round-35 package re-run inside the ledger's R35-D1 check runs `uv` from
`~/.local/bin`; with a bare PATH it exits 1 — measured at the freeze, `w-ledger-tip-source`). `R39PlanNext`'s O13 (`CASE_LINE.match` -> `.search`) is
EQUIVALENT, not reachable: the pattern starts with `^` and lines are matched one at a time, so the pre-freeze
witness `w-o13-quoted-case` could not tell them apart; it is listed as a limit and not frozen.

  --battery-dir DIR   load battery modules from DIR instead of plans/battery40 (development; predicate n/a)
  --only A01,L05      restrict mutants (development; predicate n/a)
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

BATTERY_REL = "plans/battery40"
TOOLS = {
    "anchor": "plans/anchor_digest_check.py",
    "ledger": "plans/ledger_tip.py",
    "order": "plans/order_check.py",
}
PINS = {
    "plans/anchor_digest_check.py": "11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2",
    "plans/ledger_tip.py": "853bcb2a5052b3c2319d3006459bb5012ba72dfc1e5f22874f7334b62eb77ad4",
    "plans/order_check.py": "948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc",
}
SIDECHANNEL = ("/proc", "ppid", "cmdline", "psutil", "environ", "fsmonitor", "hookspath", "filter.",
               "gitattributes", "core.", "alias.", "setsid", "daemon", "fork", "nohup", "socket")
DIRECTIONS = ("silence", "rc-silence", "rc-mirror", "error", "rc-error")
EXPECT_RC = {"accept": 0, "reject": 1, "error": 2}
WORK_TOKEN = re.compile(r"^\{WORK(?::([a-z]+))?\}$")
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
BWRAP = "/usr/bin/bwrap"
A = "plans/anchor_digest_check.py"
L = "plans/ledger_tip.py"
O = "plans/order_check.py"
P39 = ".ufo/waves/round-39/build/R39PlanNext"
W40 = ".ufo/waves/round-40/claims/witness-run.txt"

# (id, tool, class, direction, adv [file:line 'quoted sentence'], witness [pre-freeze, committed], old, new)
MUTANTS = [
    ('X1', 'anchor', '-', 'rc-mirror', "plans/anchor_digest_check.py:50-52 'Provenance row — a committed markdown under corpus/evidence/ whose table line carries this row's id'", 'witness built post-hoc by this seat (report W1): PROVENANCE.md table line with no pinned URL', '    got = [(cap, "provenance-row") for cap, _ in idx["prov_sid"].get(sid, [])]', '    got = []'),
    ('X2', 'anchor', '-', 'rc-mirror', "plans/anchor_digest_check.py:62-64 'Explicit lane path — a corpus/evidence/… path written in the row ... binds that committed file only'", 'witness built post-hoc (report W2); also a_man rows bind by row-path', '            got.append((p, "row-path"))', '            pass  # row-path route removed'),
    ('X3', 'anchor', '-', 'rc-mirror', "plans/anchor_digest_check.py:57-58 'A provenance URL (an evidence markdown naming the same <repo>/<subpath>) is consulted when the task.toml route finds nothing'", 'witness built post-hoc (report W3): PROVENANCE.md URL, row URL, no task.toml slug', '            if (repo, subpath) in idx["prov_url"]:', '            if False:'),
    ('X4', 'anchor', '-', 'rc-mirror', "plans/anchor_digest_check.py:106-112 'An erratum for S<id> exempts that row's anchor token ... when it carries the row's exact wrong token'", "witness = lane's own live S110 erratum (corpus/lessons/round-37.md:32), load-bearing at tip", '        elif cited_wrong:', '        elif False:'),
    ('X5', 'anchor', '-', 'rc-mirror', "plans/anchor_digest_check.py:106 'A line in a committed corpus/lessons/*.md beginning Erratum (round 37): S<id> anchor sha256 is read'", "witness = lane's own live S110 erratum (corpus/lessons/round-37.md:32)", 'ERRATUM = re.compile(r"^ {0,3}Erratum \\(round 37\\): (S\\d{3,}) anchor sha256\\b")', 'ERRATUM = re.compile(r"^ {0,3}Erratum \\(round 38\\): (S\\d{3,}) anchor sha256\\b")'),
    ('X6', 'anchor', 'digest-wrong-capture', 'silence', "plans/anchor_digest_check.py:89-92 'A 64-hex token that is a committed capture but not this row's is digest-wrong-capture'", "witness built post-hoc (report W6): row anchored on a sibling capture's committed digest", '            elif tok not in row_scope:\n                if tok in allowed:', '            elif tok not in row_scope:\n                if False:'),
    ('X7', 'anchor', 'digest-unknown', 'silence', "plans/anchor_digest_check.py:92-93 'a token that is no committed capture at all is digest-unknown'", 'witness built post-hoc (report W7): row anchored on a made-up 64-hex digest', '                    defects.append(f"DEFECT {sid} anchor token={tok} class=digest-unknown "', '                    defects.append(f"DEFECT {sid} anchor token={tok} class=digest-wrong-capture "'),
    ('X8', 'anchor', 'token-outside-anchor', 'silence', "plans/anchor_digest_check.py:81 'a token outside the anchor cell is token-outside-anchor — always a defect, whatever its value'", "witness = a_row-token-in-teaches (S111's own committed digest moved to the teaches cell)", '            if cell_idx != ANCHOR_CELL:', '            if cell_idx != ANCHOR_CELL and tok not in allowed:'),
    ('X9', 'anchor', '-', 'rc-silence', "plans/anchor_digest_check.py:34-35 'A row that matches the census regex but does not have 11 cells is a row-malformed defect'", 'witness = a_row-12-cells (S111 with a twelfth cell)', '        if len(r["cells"]) != NCELLS:', '        if len(r["cells"]) > NCELLS:'),
    ('X10', 'anchor', 'digest-uppercase', 'silence', "plans/anchor_digest_check.py:37-39 'sha256 plus whitespace plus a hex run, optionally backtick-quoted and optionally followed by … or ...'", 'witness = a_tok-upper-anchor (plain uppercase token must still be collected)', 'TOKEN = re.compile(r"sha256[ \\t]+`?([0-9A-Fa-f]+)`?([ \\t]*(?:…|\\.\\.\\.))?")', 'TOKEN = re.compile(r"sha256[ \\t]+`?([0-9A-Fa-f]+)`?([ \\t]*(?:…|\\.\\.\\.))")'),
    ('X11', 'anchor', '-', 'rc-mirror', "plans/anchor_digest_check.py:44-46 'the digest that entry lists, and the digest of the committed file bytes, are both accepted views of that one capture'", 'witness built post-hoc (report W11): anchor = blob digest while the manifest entry is stale', '    if path in idx["file_digest"]:', '    if False:'),
    ('X12', 'anchor', '-', 'rc-mirror', 'plans/anchor_digest_check.py:55-56 \'matched **exactly** against the name = "<org>/<task>" a committed task.toml gives\' (slash-less name fallback dropped)', 'witness built post-hoc (report W12): task.toml with name = "plain-slug"', '            pick = next((n for n in names if "/" in n), names[0] if names else None)', '            pick = next((n for n in names if "/" in n), None)'),
    ('X13', 'anchor', '-', 'rc-silence', "plans/anchor_digest_check.py:73 '`--evidence-ref head` (default) reads HEAD blobs, so an unpromoted capture never counts'", 'witness built post-hoc (report W13): capture staged beyond HEAD, row claims staged digest, default ref', '    ap.add_argument("--evidence-ref", choices=("head", "index"), default="head")', '    ap.add_argument("--evidence-ref", choices=("head", "index"), default="index")'),
    ('X14', 'anchor', 'erratum-digest-unresolved', 'silence', "plans/anchor_digest_check.py:111-113 'no 64-hex token on it may be outside A unless it is the cited wrong token of the row it names (erratum-digest-unresolved)'", 'witness built post-hoc (report W14): erratum line carrying an uppercase non-committed 64-hex token', '            if HEX64_ANY.fullmatch(t) and t not in allowed and t not in cited_wrong:', '            if HEX64.fullmatch(t) and t not in allowed and t not in cited_wrong:'),
    ('X15', 'anchor', '-', 'rc-silence', "plans/anchor_digest_check.py:108-110 'at least one other token that is 64 lowercase hex and a digest **of the capture that row names**'", "witness built post-hoc (report W15): erratum correction citing a sibling row's committed digest", '                     and (t in row_scope if row_scope is not None else t in allowed)]', '                     and t in allowed]'),
    ('X16', 'anchor', 'digest-uppercase', 'silence', "plans/anchor_digest_check.py:88-89 '(`digest-short`, `digest-long`, `digest-uppercase` otherwise)' (the class emitted for a 64-hex uppercase token)", 'witness = a_tok-upper-anchor (the fixture declares class digest-uppercase)', '                    cls, why = "digest-uppercase", "64-hex-but-not-lowercase"', '                    cls, why = "digest-short", "64-hex-but-not-lowercase"'),
]
TOTAL = 16
# SWAPPED by seat F40XMutAnchor (round-40 wave 2): 16 near-variant anchor mutants, not the frozen 21.


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


class Ctx:
    """What a battery build() may use. Runs only inside the build child."""

    ENV = {"PATH": PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
           "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
           "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
           "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00"}

    def __init__(self, lane, fixture_root):
        self.lane = pathlib.Path(lane)
        self._root = pathlib.Path(fixture_root).resolve()

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

    def clone(self, dest):
        dest = self._inside(dest)
        self.sh("git", "clone", "-q", "--shared", str(self.lane), str(dest))
        return dest

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


def build_module_child(module, dest, pristine):
    """Child entry (inside bwrap): build every fixture of one module into dest/fNNN, print JSON only."""
    mod = load(module, f"kengaku_b40_{module.stem}")
    ctx = Ctx(pristine, dest)
    out = []
    for k, fx in enumerate(getattr(mod, "FIXTURES", [])):
        d = dest / f"f{k:03d}"
        d.mkdir(parents=True)
        argv = [str(t) for t in fx["build"](ctx, d)]
        out.append({"fid": fx["fid"], "tool": fx.get("tool"), "expect": fx.get("expect"),
                    "defects": fx.get("defects"), "argv": argv})
    sys.stdout.write("BUILT " + json.dumps(out) + "\n")
    return 0


def sandbox(extra_binds=()):
    argv = [BWRAP, "--dev-bind", "/", "/", "--proc", "/proc", "--unshare-pid", "--die-with-parent", "--new-session"]
    for src, dst in extra_binds:
        argv += ["--ro-bind", str(src), str(dst)]
    return argv


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
            h.update(f"{rel}\0{st.st_mode}\0{st.st_size}\0{st.st_mtime_ns}\0{link}\n".encode())
    return h.hexdigest()


def path_ok(tok, d):
    for cand in (tok, tok.split("=", 1)[1] if tok.startswith("--") and "=" in tok else ""):
        if cand.startswith("/") and not pathlib.Path(cand).resolve().is_relative_to(d.resolve()):
            return False
    return True


def classes(tool, out):
    got = set()
    for line in out.splitlines():
        if tool == "anchor" and line.startswith("DEFECT "):
            got.update(re.findall(r"\bclass=(\S+)", line))
        elif tool == "ledger":
            m = re.match(r"^(\S+) status=\S+ observed=\S+ agree=NO\b", line)
            if m:
                got.add(f"NO:{m.group(1)}")
        elif tool == "order":
            m = re.match(r"^ORDER HIT \S+ kind=(\S+)", line)
            if m:
                got.add(f"hit:{m.group(1)}")
            m = re.match(r"^ORDER FAIL (\S+) ", line)
            if m and " hits=" not in line:
                got.add(f"fail:{m.group(1)}")
    return frozenset(got)


class Runner:
    def __init__(self, root, jobs):
        self.root, self.jobs, self.seq = root, jobs, itertools.count(1)
        self.slots = root / "slots"
        self.slots.mkdir()
        (root / "home").mkdir()
        (root / "tmp").mkdir()
        for tool in TOOLS:
            (self.slots / f"{tool}.py").write_text("# slot\n")

    def env(self):
        return {"PATH": os.environ.get("PATH") or PATH, "HOME": os.environ.get("HOME") or str(self.root / "home"), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
                "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(self.root / "tmp"),
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_COUNT": "2",
                "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
                "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null"}

    def run(self, tool, variant, fx):
        work = self.root / "work" / f"w{next(self.seq):06d}"
        argv = []
        for t in fx["argv"]:
            m = WORK_TOKEN.match(t)
            if m and m.group(1):
                (work / m.group(1)).mkdir(parents=True, exist_ok=True)
            argv.append(str(work) if m else t)
        slot = self.slots / f"{tool}.py"
        cmd = sandbox([(variant, slot)]) + [sys.executable, str(slot), *argv]
        try:
            r = subprocess.run(cmd, cwd=str(fx["dir"]), env=self.env(), capture_output=True, text=True,
                               timeout=900)
        except subprocess.TimeoutExpired:
            return ("timeout", frozenset())
        finally:
            shutil.rmtree(work, ignore_errors=True)
        return (r.returncode, classes(tool, r.stdout))

    def run_all(self, tool, variant, fixtures):
        with concurrent.futures.ThreadPoolExecutor(self.jobs) as ex:
            return list(ex.map(lambda fx: self.run(tool, variant, fx), fixtures))


def exhibits(cls, direction, fx, ref, mut):
    if direction == "rc-silence":
        return fx["expect"] == "reject" and ref[0] == 1 and mut[0] == 0
    if direction == "rc-mirror":
        return fx["expect"] == "accept" and ref[0] == 0 and mut[0] == 1
    if direction == "error":
        return fx["expect"] == "error" and ref[0] == 2 and mut[0] in (0, 1)
    if direction == "rc-error":
        return fx["expect"] == "accept" and ref[0] == 0 and mut[0] == 2
    if ref[0] not in (0, 1) or mut[0] not in (0, 1) or cls == "-":
        return False
    return cls in ref[1] and cls in set(fx["defects"]) and cls not in mut[1]  # silence


def build_battery(bdir, root, lane_clone):
    fixtures, side = [], 0
    if not bdir.is_dir():
        return fixtures, side
    for f in sorted(bdir.glob("*.py")):
        text = f.read_text().lower()
        hits = [t for t in SIDECHANNEL if t in text]
        if hits:
            side += 1
            print(f"SIDECHANNEL battery40/{f.name} tokens={','.join(hits)}")
        dest = root / "fx" / f.stem
        dest.mkdir(parents=True)
        r = subprocess.run(sandbox() + [sys.executable, str(pathlib.Path(__file__).resolve()), "--build-module",
                                        str(f), "--dest", str(dest), "--pristine", str(lane_clone)],
                           cwd=str(dest), capture_output=True, text=True, timeout=1800,
                           env={"PATH": PATH, "HOME": str(root / "home"), "TMPDIR": str(root / "tmp"),
                                "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"})
        built = [l for l in r.stdout.splitlines() if l.startswith("BUILT ")]
        if r.returncode != 0 or len(built) != 1:
            raise RuntimeError(f"module battery40/{f.name} failed to build (rc={r.returncode}): "
                               f"{r.stderr.strip()[-300:]}")
        for k, fx in enumerate(json.loads(built[0][6:])):
            d = dest / f"f{k:03d}"
            argv = fx.get("argv")
            ok = (isinstance(fx.get("fid"), str) and fx.get("tool") in TOOLS and fx.get("expect") in EXPECT_RC
                  and isinstance(fx.get("defects"), list) and all(isinstance(x, str) for x in fx["defects"])
                  and isinstance(argv, list) and all(isinstance(t, str) and path_ok(t, d) for t in argv)
                  and d.is_dir())
            if not ok:
                raise ValueError(f"fixture {fx.get('fid')!r} of battery40/{f.name} breaks the contract")
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
    ap.add_argument("--pristine", default=None, help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.build_module:
        return build_module_child(pathlib.Path(a.build_module).resolve(), pathlib.Path(a.dest).resolve(),
                                  pathlib.Path(a.pristine).resolve())
    lane = pathlib.Path(a.lane).resolve()
    dev = a.battery_dir is not None or a.only is not None
    mism = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
    print(f"PINS total={len(PINS)} mismatched={len(mism)}" + (f" first={mism[0]}" if mism else ""))
    if not os.access(BWRAP, os.X_OK):
        print(f"SETUP {BWRAP} is required", file=sys.stderr)
        return 2
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k40-c1-", dir=a.work))
    try:
        runner = Runner(root, a.jobs)
        lane_clone = root / "lane"
        r = subprocess.run(["git", "clone", "-q", "--shared", str(lane), str(lane_clone)], capture_output=True,
                           text=True, env=runner.env())
        if r.returncode != 0:
            print(f"SETUP cannot clone {lane}: {r.stderr.strip()[-200:]}", file=sys.stderr)
            return 2
        srcs = {tool: (lane / rel).read_text() if (lane / rel).is_file() else "" for tool, rel in TOOLS.items()}
        bdir = pathlib.Path(a.battery_dir).resolve() if a.battery_dir else lane / BATTERY_REL
        try:
            fixtures, side = build_battery(bdir, root, lane_clone)
        except (RuntimeError, ValueError, KeyError, json.JSONDecodeError, subprocess.TimeoutExpired) as e:
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
        for mid, tool, cls, direction, label, _witness, old, new in MUTANTS:
            if only and mid not in only:
                continue
            src = srcs[tool]
            if TOOLS[tool] in mism or src.count(old) != 1 or direction not in DIRECTIONS \
                    or (direction == "silence") == (cls == "-"):
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
                    seen.update(x for x in DIRECTIONS if x != direction
                                and exhibits(cls, x, fx, ref[fx["fid"]], res))
            if sha256(mv) != digest or sha256(refs[tool][0]) != refs[tool][1]:
                invalid += 1
                print(f"MUTANT {mid} {tool} {direction} invalid(variant changed during the run) -- {label[:90]}")
                continue
            if by:
                killed += 1
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
        after = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
        print(f"PINS-AFTER mismatched={len(after)}")
        if dev:
            print("PREDICATE C1 n/a (non-default battery or mutant subset)")
            return 0 if (wrong == 0 and tampered == 0 and side == 0 and survived == 0 and invalid == 0
                         and null_detected == 0 and not after) else 1
        good = (not mism and not after and len(MUTANTS) == TOTAL and wrong == 0 and tampered == 0 and side == 0
                and killed == TOTAL and survived == 0 and invalid == 0 and null_detected == 0)
        print(f"PREDICATE C1 {'pass' if good else 'fail'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
