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
      exits its pid namespace dies, so a process it started with `start_new_session` does not survive into the
      reference or mutant runs. That is all a pid namespace contains — it never contained the write surface
      (round-40 quantifier: a process handed to a service manager runs outside it), which is why the round-41
      sandbox ro-binds `/` and binds back only the counter's own run root. Each fixture tree is fingerprinted
      by CONTENT (path, mode, size, mtime, link target, digest; only `.git/index` and `__pycache__` excluded)
      after the build and again after the last run; a change is `tampered`.
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
the caller's HOME (the round-35 package re-run inside the ledger's R35-D1 check runs `uv` from `~/.local/bin`,
and uv needs a writable cache even on a hit — measured: `uv run --with biopython==1.85` fails with a read-only
cache, `Could not acquire lock … Read-only file system at …/.cache/uv/.tmp…`), so `TOOL_PATH` is the fixed
system order with `~/.local/bin` LAST and `~/.cache/uv` is the one writable path outside the run root. Residual:
a `uv` shim already sitting in `~/.local/bin` before the run is still consulted (no `git`/`python3`/`sha256sum`
shim can be — every system directory precedes it), and fixture code that the ledger imports can write in the
caller's uv cache. `R39PlanNext`'s O13 (`CASE_LINE.match` -> `.search`) is
EQUIVALENT, not reachable: the pattern starts with `^` and lines are matched one at a time, so the pre-freeze
witness `w-o13-quoted-case` could not tell them apart; it is listed as a limit and not frozen.

Round-41 repairs (each one is a wave-1 or wave-2 counterexample; see
`.ufo/waves/round-40/falsify/F40CritCounterLimits.md`):
  R1 A1  every copy of `plans/defect_ledger.py` / `plans/round36_c1_verify.py` under a fixture must be the
         pristine clone's bytes — the ledger imports those bodies, so a rewritten one is fixture code running
         inside the tool, free to answer by phase.
  R2 A2  tool runs get `TOOL_PATH`, not the caller's PATH, and the sandbox ro-binds `/`: a battery can neither
         plant a `git` shim where the tool looks nor write one during the run.
  R3 A3  every kill is re-checked: the reference is re-run on the killing fixture and a moved verdict makes the
         mutant `invalid`, so the mutant is credited only for a difference that is still there.
  R4 A4  `path_ok` resolves every non-`{WORK}` token against d and rejects relative paths, `..`, unresolved
         `{`/`}`, and a bare word that resolves outside d through a symlink.
  R5 A5  `fingerprint` hashes file content and no longer exempts `.lock` names.
  R6 S2  the counter's own source and every battery source are hashed before and after the run and reported as
         `sources_changed`; a change is `tampered`.
  R7 F2  `build()` must return a list (a bare string used to be char-split into a passing argv), and a fixture
         id must be non-empty.

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
import stat
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
# Round-41 repairs (F40CritCounterLimits). Every sandbox ro-binds / and makes only the counter's own run root
# writable; tool runs additionally get the caller's uv cache back read-write, because the ledger's R35-D1 check
# runs `uv run --with biopython==1.85` and uv needs a writable cache even on a hit. PATH is the fixed system
# order with the operator's ~/.local/bin LAST: `uv` lives there, `git` never should.
LOCAL_BIN = pathlib.Path.home() / ".local/bin"
UV_CACHE = pathlib.Path.home() / ".cache/uv"
TOOL_PATH = PATH + ((":" + str(LOCAL_BIN)) if LOCAL_BIN.is_dir() else "")
# The ledger imports these two bodies from the lane it audits, so a fixture that rewrites them runs its own
# code inside the tool (wave-1 A1). Every copy under a fixture must be the pristine clone's bytes.
LEDGER_BODIES = ("plans/defect_ledger.py", "plans/round36_c1_verify.py")
A = "plans/anchor_digest_check.py"
L = "plans/ledger_tip.py"
O = "plans/order_check.py"
P39 = ".ufo/waves/round-39/build/R39PlanNext"
W40 = ".ufo/waves/round-40/claims/witness-run.txt"

# (id, tool, class, direction, adv [file:line 'quoted sentence'], witness [pre-freeze, committed], old, new)
MUTANTS = [
    ("A01", "anchor", "digest-uppercase", "silence",
     f"{A}:88-89 'any other anchor token must be exactly 64 lowercase hex digits (`digest-short`, `digest-long`, "
     "`digest-uppercase` otherwise)'",
     f"{P39}/out_anchor_r5.txt:15,41 (X01-upper: ref rc=1 class=digest-uppercase; A01 killers=[X01-upper:class])",
     'HEX64 = re.compile(r"[0-9a-f]{64}")', 'HEX64 = re.compile(r"[0-9a-fA-F]{64}")'),
    ("A02", "anchor", "-", "rc-silence",
     f"{A}:84-85 'a defect (`abbrev-unresolved`) unless its hex is 8-63 lowercase hex digits and a prefix of a "
     "digest of the capture this row names'",
     f"{P39}/out_anchor_r5.txt:17,42 (X03-abbrev-7hex: ref rc=1; A02 killers=[X03-abbrev-7hex:rc])",
     "if not (8 <= len(tok) <= 63 and tok == tok.lower()):",
     "if not (1 <= len(tok) <= 63 and tok == tok.lower()):"),
    ("A03", "anchor", "-", "rc-silence",
     f"{A}:84-85 (as A02: 'its hex is 8-63 lowercase hex digits')",
     f"{P39}/out_anchor_r5.txt:19,43 (X05-abbrev-64hex-ellipsis: ref rc=1; A03 killers=[X05:rc])",
     "if not (8 <= len(tok) <= 63 and tok == tok.lower()):",
     "if not (8 <= len(tok) <= 64 and tok == tok.lower()):"),
    ("A06", "anchor", "-", "rc-mirror",
     f"{A}:31 'Row set — the census shape (... `^ {{0,3}}\\\\|\\\\s*(S\\\\d{{3,}})\\\\s*\\\\|`), so this check and "
     "the census agree on what a row is' (a 4-space-indented line is not a row)",
     f"{P39}/out_anchor_r5.txt:23,45 (X09-indent4-wrong: ref rc=0; A06 killers=[X09-indent4-wrong:rc])",
     'ROW = re.compile(r"^ {0,3}\\|\\s*(S\\d{3,})\\s*\\|")', 'ROW = re.compile(r"^ {0,4}\\|\\s*(S\\d{3,})\\s*\\|")'),
    ("A08", "anchor", "-", "rc-silence",
     f"{A}:81 'a token outside the anchor cell is `token-outside-anchor` — always a defect, whatever its value'",
     f"{P39}/out_anchor_r5.txt:20,47 (X06-token-in-teaches: ref rc=1; A08 killers=[X06:rc])",
     "if cell_idx != ANCHOR_CELL:", "if False:"),
    ("A09", "anchor", "-", "rc-silence",
     f"{A}:34-35 'A row that matches the census regex but does not have 11 cells is a `row-malformed` defect'",
     f"{P39}/out_anchor_r5.txt:21,48 (X07-12-cells: ref rc=1; A09 killers=[X07-12-cells:rc])",
     'if len(r["cells"]) != NCELLS:', 'if len(r["cells"]) < NCELLS:'),
    ("A15", "anchor", "-", "rc-silence",
     f"{A}:55 'is matched **exactly** against the `name = \"<org>/<task>\"` a committed `task.toml` gives' "
     "(an ambiguous slug binds nothing)",
     f"{P39}/out_anchor_r5.txt:31,54 (X17-duplicate-task-slug: ref rc=1; A15 killers=[X17:rc])",
     "        if len(owners) != 1:\n            continue  # ambiguous",
     "        if len(owners) < 1:\n            continue  # ambiguous"),
    ("A17", "anchor", "-", "rc-mirror",
     f"{A}:74 '`--evidence-ref index` reads the index blobs (`git cat-file :<path>`)'",
     f"{P39}/out_anchor_r5.txt:29,56 (X15-index-staged-capture: ref rc=0; A17 killers=[X15:rc, ...])",
     'return (":" if ref == "index" else "HEAD:") + path', 'return (":" if ref == "head" else "HEAD:") + path'),
    ("A21", "anchor", "-", "rc-mirror",
     f"{A}:44-46 'the digest that entry lists, and the digest of the committed file bytes, are both accepted "
     "views of that one capture' (a manifest entry is read case-folded)",
     f"{P39}/out_anchor_r5.txt:35,60 (X21-uppercase-manifest-entry: ref rc=0; A21 killers=[X21:rc])",
     "dig = m.group(1).lower()", "dig = m.group(1)"),
    ("A22", "anchor", "-", "rc-mirror",
     f"{A}:44-46 (as A21: the manifest entry is an accepted view of the capture)",
     f"{P39}/out_anchor_r5.txt:34,61 (X20-stale-manifest-digest: ref rc=0; A22 killers=[X20:rc, X21:rc])",
     "if (d, base) in idx[\"dir_entries\"]:\n        got.setdefault(idx[\"dir_entries\"][(d, base)], "
     "f\"{d}/SHA256SUMS:{base}\")",
     "if False:\n        pass"),
    ("A27", "anchor", "capture-unanchored", "silence",
     f"{A}:96-98 'A capture none of the row's anchor tokens resolves is `capture-unanchored`'",
     f"{W40} (witness/w_anchor.py w-a27-second-url: ref class=capture-unanchored; mutant without it); "
     f"{P39}/out_anchor_r5.txt:24 (X10 ref rc=1 class=capture-unanchored)",
     '                    defects.append(f"DEFECT {sid} anchor token=- class=capture-unanchored "',
     '                    (f"DEFECT {sid} anchor token=- class=capture-unanchored "'),
    ("L01", "ledger", "-", "error",
     f"{L}:23-25 'Exit codes are the registry row's contract (SKILL.md:581): ... `2` usage/clone/setup refusal'",
     f"{P39}/out_ledger_r5.txt (T08-source-not-a-repo, T09-source-work-exists: ref rc=2; L01 killers=[T08:rc, "
     "T09:rc])",
     "    raise SystemExit(2)\n\n\ndef load_module", "    raise SystemExit(1)\n\n\ndef load_module"),
    ("L05", "ledger", "-", "rc-silence",
     f"{L}:20-21 'mismatches counts every closed row whose check fails plus every open row whose check passes "
     "(stale self-assessment)'",
     f"{P39}/out_ledger_r5.txt (T05-control-row-flipped-open: ref rc=1; L05 killers=[T05:rc])",
     'agree = (is_closed and ok) or (st == "open" and not ok)', 'agree = ok'),
    ("L06", "ledger", "-", "rc-silence",
     f"{L}:23-24 '`0` no mismatch · `1` a ledger row genuinely disagrees' (exit 0 needs rows: "
     f"`return 0 if (rows and mism == 0) else 1`)",
     f"{P39}/out_ledger_r5.txt (T06-control-empty-ledgers: ref rc=1; L06 killers=[T06:rc])",
     "return 0 if (rows and mism == 0) else 1", "return 0 if mism == 0 else 1"),
    ("L11", "ledger", "-", "error",
     f"{L}:58 'The clone is created at <work>/lane (must not exist)'",
     f"{P39}/out_ledger_r5.txt (T09-source-work-exists: ref rc=2; L11 killers=[T09:rc]); {W40} (w-l11-work-exists)",
     "    if dest.exists():\n        refuse", "    if False:\n        refuse"),
    ("L14", "ledger", "-", "rc-silence",
     f"{L}:228 '# a crash is an observed failure, never a pass'",
     f"{P39}/out_ledger_r5.txt (T10-control-check-crashes: ref rc=1; L14 killers=[T10:rc])",
     '                    ok, note = False, f"error {type(e).__name__}: {e}"',
     '                    ok, note = True, f"error {type(e).__name__}: {e}"'),
    ("L15", "ledger", "-", "rc-silence",
     f"{L}:20-21 (as L05: a closed row whose check fails is a mismatch; an unknown check is a failed check, "
     f"{L}:220)",
     f"{P39}/out_ledger_r5.txt (T07-control-unknown-check: ref rc=1; L15 killers=[T07:rc])",
     "                ok, note = False, f\"unknown check {r.get('check')!r}\"",
     "                ok, note = True, f\"unknown check {r.get('check')!r}\""),
    ("L21", "ledger", "-", "error",
     f"{L}:44-45 'REFUSE stale pin ref … (exit 2) the ref exists but resolves to a commit other than the one "
     "under audit'",
     f"{W40} (witness/w_ledger.py w-l21-control-stale-master: ref rc=2; mutant rc 0/1); "
     f"{P39}/R39PlanNext.md:110-111 (old tool rc=0 silent, new tool REFUSE rc=2)",
     '        if rev and rev != tip:\n            refuse(f"stale pin ref',
     '        if False:\n            refuse(f"stale pin ref'),
    ("O04", "order", "-", "rc-silence",
     f"{O}:15-16 'a gate `P10` line whose detail is anything other than `receipt unreadable`' (only a "
     "DEFECT line may carry the excuse)",
     f"{W40} (witness/w_order.py w-o04-p10-ok-excuse: ref rc=1; mutant rc=0); {P39}/R39PlanNext.md:126",
     'if not (m.group(1) == "DEFECT" and EXECUTED_EXCUSE.match(detail)):',
     'if not (EXECUTED_EXCUSE.match(detail)):'),
    ("O12", "order", "-", "rc-error",
     f"{O}:37 'it reads every blob under claims/' (non-blob tree entries are not blobs to read)",
     f"{W40} (witness/w_order.py w-o12-gitlink: ref rc=0; mutant rc=2); {P39}/R39PlanNext.md:126",
     'if len(parts) != 3 or parts[1] != "blob":', 'if len(parts) != 3:'),
    ("O14", "order", "-", "error",
     f"{O}:26-27 'Exit: ... 2 setup error (..., unparseable round number, bad arguments)' (the claims file "
     "name must be round-NN-claims.md)",
     f"{W40} (witness/w_order.py w-o14-claims-name-prefixed: ref rc=2; mutant rc 0/1); {P39}/R39PlanNext.md:126",
     'CLAIMS_NAME = re.compile(r"^round-(\\d+)-claims\\.md$")', 'CLAIMS_NAME = re.compile(r"round-(\\d+)-claims\\.md")'),
]
TOTAL = 21


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
        built = fx["build"](ctx, d)
        # Round-41 F2 (review): a bare string used to be char-split into one argv token per character and
        # every token passed the contract check, so a vacuous fixture could still be credited with a kill.
        if not isinstance(built, (list, tuple)):
            raise TypeError(f"battery40/{module.name} fixture {fx.get('fid')!r}: build() must return a list "
                            f"of argv strings, got {type(built).__name__}")
        argv = [str(t) for t in built]
        out.append({"fid": fx["fid"], "tool": fx.get("tool"), "expect": fx.get("expect"),
                    "defects": fx.get("defects"), "argv": argv})
    sys.stdout.write("BUILT " + json.dumps(out) + "\n")
    return 0


def sandbox(extra_binds=(), write_root=None, uv_cache=False):
    # Round-41 F1/S1: the whole filesystem is read-only inside the sandbox; only the counter's own run root
    # (and, for tool runs, the caller's uv cache) is writable, and network/ipc are unshared. The pid
    # namespace alone never contained the write surface, and `--dev-bind / /` left the host wide open.
    argv = [BWRAP, "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
            "--unshare-pid", "--unshare-ipc", "--unshare-net", "--die-with-parent", "--new-session"]
    if write_root is None or not str(write_root).startswith("/tmp/"):
        argv += ["--tmpfs", "/tmp"]
    if write_root is not None:
        argv += ["--bind", str(write_root), str(write_root)]
    if uv_cache and UV_CACHE.is_dir():
        argv += ["--bind", str(UV_CACHE), str(UV_CACHE)]
    for src, dst in extra_binds:
        argv += ["--ro-bind", str(src), str(dst)]
    return argv


def fingerprint(d):
    # Round-41 F3/A5: content, not metadata. A same-size write with the mtime restored used to be invisible,
    # and the `.lock` suffix exemption let a fixture write a file on every run and still read `tampered=0`.
    h = hashlib.sha256()
    for top, dirs, files in os.walk(d):
        dirs[:] = sorted(x for x in dirs if x != "__pycache__")
        rel_top = os.path.relpath(top, d)
        for name in sorted(files) + [x for x in dirs if os.path.islink(os.path.join(top, x))]:
            rel = os.path.normpath(os.path.join(rel_top, name))
            if rel.endswith(".git/index"):
                continue
            p = os.path.join(top, name)
            st = os.lstat(p)
            if stat.S_ISLNK(st.st_mode):
                body = b"link\0" + os.readlink(p).encode("utf-8", "surrogateescape")
            elif stat.S_ISREG(st.st_mode):
                try:
                    with open(p, "rb") as fh:
                        body = b"file\0" + hashlib.file_digest(fh, "sha256").hexdigest().encode()
                except OSError:
                    body = b"unreadable"
            else:
                body = b"other"
            h.update(f"{rel}\0{st.st_mode}\0{st.st_size}\0{st.st_mtime_ns}\0".encode("utf-8", "surrogateescape"))
            h.update(body + b"\n")
    return h.hexdigest()


def path_ok(tok, d):
    # Round-41 A4/F4: the escape was a token that does not start with "/" — the tools run with cwd=d, so a
    # relative token resolves out of d. Relative tokens are legitimate (the order gate reads `--claims`
    # relative to `--lane`), so the rule is: an absolute token must lie inside d, and a relative token that
    # resolves against d to something that exists must still lead inside d (no `..`, no symlinked escape).
    root = d.resolve()
    cands = [tok]
    if tok.startswith("--") and "=" in tok:
        cands.append(tok.split("=", 1)[1])
    for cand in cands:
        if WORK_TOKEN.match(cand):
            continue
        if "{" in cand or "}" in cand:
            return False
        p = pathlib.Path(cand)
        if p.is_absolute():
            if not p.resolve().is_relative_to(root):
                return False
            continue
        try:
            target = root / cand
            real = target.resolve()
        except OSError:
            return False
        if target.exists() and not real.is_relative_to(root):
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
        # Round-41 A2: the fixed PATH, not the caller's. `git` resolves to /usr/bin/git even when a directory
        # earlier on the caller's PATH holds a shim; the ledger's `uv` still resolves from ~/.local/bin last.
        return {"PATH": TOOL_PATH, "HOME": os.environ.get("HOME") or str(self.root / "home"), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
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
        cmd = sandbox([(variant, slot)], write_root=self.root, uv_cache=True) + [sys.executable, str(slot), *argv]
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


def bodies_ok(d, lane):
    """Round-41 A1: every copy of a ledger check body under a fixture is the pristine clone's bytes.

    `ledger_tip.py:205` imports the audited lane's `plans/defect_ledger.py` / `plans/round36_c1_verify.py`,
    so a fixture that rewrites either one runs its own code inside the tool and can answer by phase. The
    three pinned tools cannot be rewritten the same way (PINS), which is why this is the only body set.
    """
    for rel in LEDGER_BODIES:
        src = lane / rel
        want = src.read_bytes() if src.is_file() else None
        for p in d.glob("**/" + rel):
            try:
                if want is None or p.read_bytes() != want:
                    return False
            except OSError:
                return False
    return True


def sources_digest(bdir, own):
    """Round-41 S2: the counter and the battery sources, hashed before and after the run."""
    h = hashlib.sha256((sha256(own) or "missing").encode())
    for f in (sorted(bdir.glob("*.py")) if bdir.is_dir() else []):
        h.update(f.name.encode() + b"\0" + (sha256(f) or "missing").encode() + b"\n")
    return h.hexdigest()


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
        r = subprocess.run(sandbox(write_root=root) + [sys.executable, str(pathlib.Path(__file__).resolve()),
                                                       "--build-module", str(f), "--dest", str(dest),
                                                       "--pristine", str(lane_clone)],
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
            ok = (isinstance(fx.get("fid"), str) and fx["fid"].strip() != "" and fx.get("tool") in TOOLS
                  and fx.get("expect") in EXPECT_RC
                  and isinstance(fx.get("defects"), list) and all(isinstance(x, str) for x in fx["defects"])
                  and isinstance(argv, list) and all(isinstance(t, str) and path_ok(t, d) for t in argv)
                  and d.is_dir())
            if not ok:
                raise ValueError(f"fixture {fx.get('fid')!r} of battery40/{f.name} breaks the contract")
            if fx["tool"] == "ledger" and not bodies_ok(d, lane_clone):
                raise ValueError(f"fixture {fx.get('fid')!r} of battery40/{f.name} rewrites a ledger check "
                                 f"body; the tool would import fixture code")
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
        sdig0 = sources_digest(bdir, pathlib.Path(__file__).resolve())
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
            if by:
                # Round-41 correction 2: attribute the kill to the mutant, not to the phase. Re-run the
                # reference on the killing fixture now; a fixture whose reference verdict moves is invalid, so
                # an input swapped between the two phases (wave-1 A3) cannot buy a kill.
                fx_by = next(fx for fx in fxs if fx["fid"] == by)
                if runner.run_all(tool, refs[tool][0], [fx_by])[0] != ref[by]:
                    invalid += 1
                    print(f"MUTANT {mid} {tool} {direction} invalid(reference verdict moved during the run)"
                          f" -- {label[:90]}")
                    continue
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
        src_changed = int(sdig0 != sources_digest(bdir, pathlib.Path(__file__).resolve()))
        tampered += src_changed
        if src_changed:
            print("TAMPERED the counter or a battery source changed during the run")
        print(f"BATTERY fixtures={len(fixtures)} wrong={wrong} tampered={tampered} sidechannel={side}"
              f" sources_changed={src_changed}")
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
