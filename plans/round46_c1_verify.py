#!/usr/bin/env python3
"""Round-46 C1 counter (calibration): does the lane's fixture fence do what the lane says it does?

Self-assessment under test. SCORECARD capability `fenced-fixture-discovery` (round 44) and the
`plans/fixture_fence.py` docstring: "admit only a fixture whose git store, discovered repos and argv stay inside
`d`", deciding without reading outside `d`. Observed at base (`64ba8385`): the round-45 counter is passed by a
fence that keys on the counter's own fixture names (QUALITY Q39), and 9 of 14 held-out hostile modules written
against the landed fence are admitted. The calibration count is the number of frozen hostile modules on which
the fence's observed behaviour contradicts that advertisement: a module is CLEAN only if every fixture it builds
is refused AND the fence's whole process tree touches no path outside the fixture directory while deciding.

Subject (not pinned, it is the work): `plans/fixture_fence.py`, a module exposing

    breach(d: pathlib.Path, argv: list[str], tool: str) -> str | None

`d` is the fixture directory (absolute, resolved), `argv` the module's argv (tokens relative to `d` or absolute
inside it), `tool` is `anchor` or `order`. A non-empty string refuses the fixture (the reason); None admits it.
It runs with cwd `d`, in a read-only sandbox (nothing it does can write; `/run` and `/dev` are its own), under
`strace -f -y` started OUTSIDE the sandbox, so the log lives in a mount the fence cannot write, rename or unlink,
and the harness closes every fd above 2 before `breach` is called.

Legs, every input pinned below by digest (PINS):
  REFUSALS  `plans/refusals46/`: f1-f10 byte-copied from `plans/refusals45/` (checked as byte copies, `COPY`
            rows) plus every round-45 held-out module that the landed fence admits or reads, converted to the
            module contract and kept only while it is LEAKED or READ under the base fence. Built in the
            round-44 build sandbox (the round-44 counter's own `Ctx`/builder, imported unchanged); every fixture
            is handed to the fence. Per module: `clean` | `LEAKED` (a fixture admitted) | `READ` (refused, but
            the fence touched a path outside d) | `HUNG` (no answer in 120 s).
  SEALED    `plans/sealed46/`: hostile modules authored in wave 1 by critic seats that no fence-writing seat
            reads, kept only while LEAKED or READ under the base fence. Same build and same verdicts; a sealed
            module is never edited to make the counter pass, it is dropped and the drop is reported.
  HONEST    the 22 modules of the standing batteries `plans/battery42`, `plans/battery43`, `plans/battery44`
            (104 fixtures the round-44 counter admits) must all be ADMITTED with no outside touch: a fence that
            refuses everything, or anything with a git repo, fails here.

Rules this counter adds to the round-45 one (round-45 wave-1 `R45CriticPredicate.md` B1-B6, QUALITY Q39):
  (a) the round-44 counter's legs, builder and HONEST leg are imported unchanged (digest-pinned); the build
      child is the round-44 counter's `builder_source()` delivered by `--ro-bind-data`, so no copy of this file
      exists inside the scratch root.
  (b) Q39 NAME HIDING: fixture dirs, build dirs, fixture parents and module copies are named by a per-run
      `secrets` token, never derived from a module or group name; every fixture parent is padded to `PAD`
      children with empty decoy dirs, so the child count (and `st_nlink`) carries no module signal; the fence
      jobs run in a shuffled order.
  (c) REFUSALS as above, with the byte-copy check of f1-f10 reported per file.
  (d) SEALED as above, from a directory this seat never writes.
  (e) B1 LOG INTEGRITY: `strace` runs on the host, outside the sandbox, and its log is under the scratch root
      where the sandbox is read-only (no writable bind exists), so the fence cannot truncate, rewrite or unlink
      it; the harness closes every fd above 2 before calling `breach`; a missing, empty, NUL-holed or
      execve-less log counts as READ, never as zero.
  (f) B3 WHOLE SCRATCH ROOT: a touch is any path under the scratch root that is neither `d` nor under the
      harness directory (`<root>/ctl`, which holds only the harness and the fence copy). Module-source copies,
      sibling fixtures, logs and `d`'s own parent are all in scope.
  (g) B5 STAT CHANNEL: `stat`, `lstat`, `newfstatat`, `statx`, `access`, `faccessat(2)`, `readlink(at)`,
      `getxattr`/`lgetxattr`/`listxattr`, `inotify_add_watch`, `name_to_handle_at`, `execve(at)` and the
      write-side calls (`unlink(at)`, `rename(at2)`, `truncate`, `mkdir(at)`, `rmdir`, `symlink(at)`,
      `link(at)`) are traced and count like opens. A stat-family call counts for a NON-directory path only
      (git's bounded discovery stats every ancestor directory of `d` successfully; a directory stat's only
      content channel is `st_nlink`, which rule (b)'s padding nulls). `access`/`faccessat` returning EACCES
      count: existence was revealed.
  (h) B6 BLOCKED CALLS: a `<unfinished ...>` line is stored and decoded with its `<... resumed>` tail; a call
      that never returns (killed, blocked on a FIFO) is counted from its stored text. Dirfd-relative paths are
      resolved against the `fd<dir>` annotation strace `-y` prints, falling back to cwd `d`.
  (i) B4 VERDICT CHANNEL: the harness carries the decision in its exit status — 10 BREACH, 11 ADMIT, anything
      else (exception, fence `SystemExit`, strace failure) ERROR; stdout is never parsed.

A touch is "outside d": its normalized path lies under the scratch root, and is not `d`, not under `d`, not under
`<root>/ctl`. Success rule: an open counts when it succeeds or fails with an errno other than ENOENT (an
existing path was aimed at); a stat-family call counts on success (or EACCES for access); a never-returned call
counts as attempted.

Frozen predicate (same lines as `plans/round-46-claims.md` §C1; the L1 fills `<P>`, `<R>`, `<S>` at the stage-2
amendment, together with the pins of `plans/refusals46/` and `plans/sealed46/`):
  C1 passes iff `python3 plans/round46_c1_verify.py --lane .` prints `PINS total=65 mismatched=0`, then
  `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`, then
  `SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0`, then
  `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, then
  `CALIBRATION advertised=32 contradicted=0`, then `PREDICATE C1 pass`, exit 0, on a clean clone of the
  landing tip.

Non-vacuity: `REFUSAL_FLOOR` and `SEALED_FLOOR` bind the two hostile legs to a minimum module count, and
`HONEST_TOTAL` binds the honest leg, so an empty hostile directory cannot print a passing predicate.

Limits named now: io_uring SQE opens/reads emit no traced syscall (B7, not exploited here; the counter does not
block `io_uring_*`); host paths outside the scratch root are not counted, so a fence may still read `/etc`,
`/proc` and `/sys` while deciding — the advertisement says "without reading outside d" and this counter measures
the scratch root only; a directory stat's `st_nlink` channel is nulled by padding, not measured; the round-44
counter's `SIDECHANNEL` token scan is not repeated over the hostile modules; `--refusals`, `--sealed`, `--fence`
and `--seed` are testing overrides, and the predicate they print is the predicate of the inputs they name (never
a receipt for the frozen run).

  --work DIR     scratch parent (must lie outside the lane; default $TMPDIR)
  --jobs N       parallel fence runs (default 8)
  --refusals DIR testing only: read the refusal modules from DIR
  --sealed DIR   testing only: read the sealed modules from DIR
  --fence PATH   testing only: run the fence at PATH instead of plans/fixture_fence.py
  --seed HEX     testing only: fix the per-run token seed (names stay opaque; receipts reproduce)

Exit 0 pass, 1 fail, 2 setup error.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import pathlib
import random
import re
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile

K44_REL = "plans/round44_c1_verify.py"
FENCE_REL = "plans/fixture_fence.py"
REFUSAL_REL = "plans/refusals46"
SEALED_REL = "plans/sealed46"
REFUSAL_SOURCE_REL = "plans/refusals45"
HONEST_RELS = ("plans/battery42", "plans/battery43", "plans/battery44")
PINS = {
    "plans/round44_c1_verify.py": "6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad",
    "plans/refusals45/f1_gitfile.py": "bac0df8aa55e35de2964f0e98a8c461aa6eeeba9daa2f18ca113a383f24a4c8d",
    "plans/refusals45/f2_deep.py": "027972c63696dd16e147b70002a532bf754ef5bd4f31956ae4510efd8ddcb734",
    "plans/refusals45/f3_abbrev.py": "05a43c051053d131fc11a0f7625c0b28fc0ca1a8c5d9c5302fca5f21062ead48",
    "plans/refusals45/f4_fifo.py": "6ba6a730192d056f60e1accfb1a31f30e2133296b56537ff6047d0da6817d043",
    "plans/refusals45/f5_alternates.py": "8d56f2f7d4c1e8dd5951d87e1d5e5443fa45721fc1da1a61abcd11320061eab4",
    "plans/refusals45/f6_above.py": "e9a599e400952eb203123205754f7993a37c83de9ddc881521bbcaa4df4608df",
    "plans/refusals45/f7_commondir.py": "c828c1010e38e17812374e8d5383d4fb04e8e37d0ad38915f46723b726eaa0f3",
    "plans/refusals45/f8_worktreecfg.py": "e9483e36db55a98abdc3f9b93964fe96d4cda4e714d2be831696db6a245af364",
    "plans/refusals45/f9_nodescribe.py": "b85ca5c6f95ac535ee762323cf0461a27e15820fd93c994d58df5ccb2ca557d2",
    "plans/refusals45/f10_laneinclude.py": "58ab580f84f84b4bd5e536418e7580874ae7ecf1717585628712e800feaf5111",
    "plans/battery42/a_class.py": "eef02b5df0a8b5e7e558956eaf3d5fca6fa5701872f11632d5327717def8f1bb",
    "plans/battery42/a_route.py": "d6dad7cd1458838dcd546f2176ff5b2217faab78cc68b92c86ad94b688adf81f",
    "plans/battery42/a_row.py": "947194e4517fb94b8d3529e6c4d5118585697497103784655ddd736635b48df8",
    "plans/battery42/o_clause.py": "badc9e3d3807e22c99161ae3c991db1e0ed840dd8c76542dbf9643c210af163b",
    "plans/battery42/o_scan.py": "4a9ef972806481eaa07349f109a843fa0a3e091057d3f6c33b13bfbec4b5279c",
    "plans/battery43/a_alt.py": "31ddcc0cb9a475dd3d7e3a41b90daa949a2b84fec827cf490333cd0620c5dc01",
    "plans/battery43/a_err.py": "2c41e02a38fcdb115890be9d8db83e72f20171a2a1111999c6b1a936e9772b6e",
    "plans/battery43/a_row.py": "b140efcf3f9088b471453cf731be0d4e57c12207efc42d2c510a998c3e8c421b",
    "plans/battery43/a_url.py": "6a3d4732162c46a4eeabf8f5274860cab5373ffa6eabfa16a5c259524697e5fd",
    "plans/battery43/o_alt.py": "8555d3a663d9e58b6a7dcf6c7919dc91a7408deb5195ca41d550ce245e2d6e97",
    "plans/battery43/o_excuse.py": "9f741fdc126d6f0f3e126aee22b45a66816c9d46141714cd8c0f7f1ed5631c96",
    "plans/battery43/o_scan.py": "6ddcdbb8ca3075f119bf8a3fe662a67b22637be243645bc145e7439a0314f38c",
    "plans/battery44/u14c_name_a.py": "6e8dc5d0db31416ab21b7278e2b3dd70c4265c36f212708d03f998f13cd9bcf9",
    "plans/battery44/u14c_name_b.py": "7ac8f05ebf07d78087cdf3239dccb4d4c550b9bc154c1f0ce89c156deef62620",
    "plans/battery44/u5_short_a.py": "fdd4048af41530e9e09821d724fae83962a811053bd32c44ad18b74f2451ef09",
    "plans/battery44/u5_short_b.py": "eff6edf8b407753c19dd70a825eaeb5889244cc308af70019fa17a4addeec86d",
    "plans/battery44/u6_long_a.py": "5dceb2b274cdbe753ebfa7d37f02ea0b53ff31652acab020b0d8911c6b3fa778",
    "plans/battery44/u6_long_b.py": "52f50a2fecd053eb15346964702900859b4e474b06dfcf5fe5207f6b496d773a",
    "plans/battery44/u7_twin_a.py": "8c322cf38293f34b82669734e793e75f8cb6d82071bdb7ac854e34bf387e66e5",
    "plans/battery44/u7_twin_b.py": "6bee837959584e12577647fb280d1ea50228edf03106868ec2c4cb11087f4d89",
    "plans/battery44/u9_worktree_a.py": "20f3d3da28f138c32d9f1cc99240308112567334b3c149f10f3f20c9074e92bd",
    "plans/battery44/u9_worktree_b.py": "f1a14b5f0a8e24c512f645cfc3e6d5bd325e75efc9adf19a9c40db95e78aed6c",
    "plans/refusals46/f10_laneinclude.py": "58ab580f84f84b4bd5e536418e7580874ae7ecf1717585628712e800feaf5111",
    "plans/refusals46/f11_cr_include.py": "33f11fd88ba912f2df864abbb6a6bdfe61d5923940da11dd6687c5fb210c9176",
    "plans/refusals46/f12_includeif_cond.py": "b9ad463fa1fc1705ffe568d288b26dbfc5db35583f9f1a10f774f509ae584d66",
    "plans/refusals46/f13_bom_include.py": "9d423838705f9a7377c82fa0ce36df1cfcef27fd8289532559dbb563f02a9c79",
    "plans/refusals46/f14_gitdir_include_symlink.py": "f9bec1897917d3a2c262f66c361cc8be0d30b0025ca1d7dce857c6bd76070e27",
    "plans/refusals46/f15_objects_symlink_out.py": "d60ec7567888a58c0ee23b28cf554bdc3c82362091fdfdf4a18436654d8021f4",
    "plans/refusals46/f16_objects_hardlink_out.py": "bfebf9cef085990d2e0fd7097b3b80026639feedb05309ae74340f93075ab97f",
    "plans/refusals46/f17_argv_nul.py": "89585960748982b6725dd81fe7c6a38ebba18f2cf879708ff0e43751120d53db",
    "plans/refusals46/f18_wtmeta_out.py": "1f8a60048a5f3ecc84bd64030e0def80cc9009a6821e80f23e3bb7c9ecceb369",
    "plans/refusals46/f19_commondir_hidden.py": "6e15f399ced91faf552a6cf76bc3134f0a8de502e6006a2f854387be9d76d3c4",
    "plans/refusals46/f1_gitfile.py": "bac0df8aa55e35de2964f0e98a8c461aa6eeeba9daa2f18ca113a383f24a4c8d",
    "plans/refusals46/f20_attributes_file.py": "911edab27d8387a994696d9c28755a1b37db636757ff68f7837aa17cf4c4e954",
    "plans/refusals46/f2_deep.py": "027972c63696dd16e147b70002a532bf754ef5bd4f31956ae4510efd8ddcb734",
    "plans/refusals46/f3_abbrev.py": "05a43c051053d131fc11a0f7625c0b28fc0ca1a8c5d9c5302fca5f21062ead48",
    "plans/refusals46/f4_fifo.py": "6ba6a730192d056f60e1accfb1a31f30e2133296b56537ff6047d0da6817d043",
    "plans/refusals46/f5_alternates.py": "8d56f2f7d4c1e8dd5951d87e1d5e5443fa45721fc1da1a61abcd11320061eab4",
    "plans/refusals46/f6_above.py": "e9a599e400952eb203123205754f7993a37c83de9ddc881521bbcaa4df4608df",
    "plans/refusals46/f7_commondir.py": "c828c1010e38e17812374e8d5383d4fb04e8e37d0ad38915f46723b726eaa0f3",
    "plans/refusals46/f8_worktreecfg.py": "e9483e36db55a98abdc3f9b93964fe96d4cda4e714d2be831696db6a245af364",
    "plans/refusals46/f9_nodescribe.py": "b85ca5c6f95ac535ee762323cf0461a27e15820fd93c994d58df5ccb2ca557d2",
    "plans/sealed46/a_newline_anchor.py": "4542b9099f7f56528344f59dda9fa47f1fefaca30a6d3ca9bd8209f897ce849c",
    "plans/sealed46/a_phantom_anchor.py": "2291451aa94ccc6e12353f1c940f974b48c421a39cf5aee8d0072a77a3f90bae",
    "plans/sealed46/a_phantom_order.py": "debf651d002e7c7b8c8f9c6430fe662d0851cd1e2d72994b9523122ee9bd25c5",
    "plans/sealed46/c_core_attributes_path.py": "2a8218c123fced0917d6dcd27ffdaae60b1c0d92a1d05f71ec914693218f293f",
    "plans/sealed46/c_excludes_file.py": "3ce40827cab1bfd4d25a1d812873a24ea97b7ac673022ed6ba0cb5052bd9a5da",
    "plans/sealed46/c_url_rewrite.py": "3de8d61fb7288309eca8dc2defd90933a1b406b0c7ff5fbf14bb3615442013d8",
    "plans/sealed46/p_info_redirect.py": "675945e9556c88dae8d811c7f1182bb6c855d3c932bc73b3469dc497fe225938",
    "plans/sealed46/p_pack_redirect.py": "78246f4aeeda91e3ff2af6e74948a7fdb59f60c4d370e3da29bc15d032be5c1e",
    "plans/sealed46/p_refs_redirect.py": "932d62819a05f0bc3a752d13a7167f064a5ab2cbcfa2594bb0ff1eae2e26e9e8",
    "plans/sealed46/s_objects_link.py": "b9bc8b665d6dde269ef1418fc47b35924e3d2ecdf6a517ae55bb7cd8b19c3d2e",
    "plans/sealed46/s_packed_refs.py": "3f7d4e08bc7c2c5ba4a42b6ac376344942cc70d2b23ef6873f4f1dafccc08fda",
    "plans/sealed46/s_refs_link.py": "b25d66ea8fb8a595c8b339d6741e14b72f26040e4e16388c2662b0c76d779084",
}
REFUSAL_FLOOR = 20  # stage-2 literal <R> (round-46 amendment): exact, not a floor
SEALED_FLOOR = 12  # stage-2 literal <S> (round-46 amendment): exact, not a floor
HONEST_TOTAL = 104
PAD = 24
STRACE = "/usr/bin/strace"
FENCE_TIMEOUT = 120
TRACE_SET = ",".join((
    "open", "openat", "openat2", "creat",
    "stat", "lstat", "newfstatat", "statx", "statfs", "statfs64",
    "access", "faccessat", "faccessat2",
    "readlink", "readlinkat", "getxattr", "lgetxattr", "listxattr", "llistxattr",
    "inotify_add_watch", "name_to_handle_at", "open_by_handle_at",
    "execve", "execveat",
    "unlink", "unlinkat", "rename", "renameat", "renameat2", "truncate",
    "mkdir", "mkdirat", "rmdir", "symlink", "symlinkat", "link", "linkat",
))
OPEN_FAMILY = frozenset(("open", "openat", "openat2", "creat", "open_by_handle_at"))
STAT_FAMILY = frozenset(("stat", "lstat", "newfstatat", "statx", "statfs", "statfs64", "readlink", "readlinkat",
                         "getxattr", "lgetxattr", "listxattr", "llistxattr", "inotify_add_watch",
                         "name_to_handle_at"))
ACCESS_FAMILY = frozenset(("access", "faccessat", "faccessat2"))
WRITE_FAMILY = frozenset(("unlink", "unlinkat", "rename", "renameat", "renameat2", "truncate", "mkdir",
                          "mkdirat", "rmdir", "symlink", "symlinkat", "link", "linkat"))
EXEC_FAMILY = frozenset(("execve", "execveat"))
TRACED = OPEN_FAMILY | STAT_FAMILY | ACCESS_FAMILY | WRITE_FAMILY | EXEC_FAMILY
HARNESS = r'''
import importlib.util, json, os, pathlib, sys
spec = importlib.util.spec_from_file_location("fixture_fence_under_test", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
os.closerange(3, 1024)          # rule (e): the fence never holds the log fd or any other inherited fd
try:
    r = m.breach(pathlib.Path(sys.argv[2]), json.loads(sys.argv[4]), sys.argv[3])
except Exception as e:          # a raising fence is an ERROR, never an admission
    sys.stderr.write(f"HARNESS-ERROR {type(e).__name__}: {e}\n")
    sys.exit(12)
sys.stderr.write(("BREACH " + " ".join(str(r).split()))[:300] + "\n" if r else "ADMIT\n")
sys.exit(10 if r else 11)
'''
QUOTED = re.compile(r'"((?:[^"\\]|\\.)*)"')
DIRFD = re.compile(r"(?:AT_FDCWD|-?\d+)<([^<>]*)>,\s*$")
RESUME = re.compile(r"^\s*(\d+)\s+<\.\.\.\s+([a-z_0-9]+)\s+resumed>(.*)$")
PIDLINE = re.compile(r"^\s*(\d+)\s+(.*)$")
CALLNAME = re.compile(r"^([a-z_0-9]+)\(")
ERRNO = re.compile(r"\bE([A-Z0-9]+)\b")


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def load(path, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def token(rng):
    """Rule (b): one per-run opaque name, never derived from a module, group or fixture name."""
    return format(rng.getrandbits(64), "016x")


def split_call(text):
    """(name, args, result-or-None) from one strace call body; result keeps its errno/fd token only."""
    m = CALLNAME.match(text)
    if not m:
        return None
    k = text.rfind(") = ")
    if k < 0:
        return m.group(1), text[m.end():], None
    res = text[k + 4:].split("<", 1)[0].strip()
    return m.group(1), text[m.end():k], res


def _paths(name, args, cwd):
    """Every path argument of one traced call; a dirfd-relative path is resolved against the `fd<dir>`
    annotation (rule h), otherwise against cwd `d`. For execve only the program path is a path."""
    out = []
    for m in QUOTED.finditer(args):
        s = m.group(1)
        if "\\" in s:
            try:
                s = s.encode().decode("unicode_escape")
            except UnicodeDecodeError:
                pass
        if s.startswith("/"):
            p = s
        else:
            fd = DIRFD.search(args[:m.start()])
            base = fd.group(1) if (fd and fd.group(1)) else str(cwd)
            p = os.path.join(base, s)
        out.append(os.path.normpath(p))
        if name in EXEC_FAMILY:
            break
    return out


def _outside(p, d, root, ctl):
    if p == d or p.startswith(d + os.sep):
        return False
    if p == ctl or p.startswith(ctl + os.sep):
        return False
    return p == root or p.startswith(root + os.sep)


def analyse(raw, d, root, ctl):
    """Returns (hits, calls): hits is a list of (syscall, path) touches outside d under the scratch root."""
    hits, calls = [], 0
    pending = {}
    d, root, ctl = str(d), str(root), str(ctl)

    def consider(name, args, res):
        nonlocal calls
        if name not in TRACED:
            return
        calls += 1
        if res is None:                                   # never returned: the path was touched
            ok = True
        elif res.startswith("?"):
            ok = True                                     # never returned (killed, blocked, interrupted)
        elif res.startswith("-") or res.startswith("E"):
            err = ERRNO.search(res)
            code = f"E{err.group(1)}" if err else ""
            ok = (name in ACCESS_FAMILY and code == "EACCES") or (name in OPEN_FAMILY and code not in ("", "ENOENT"))
        else:
            ok = True
        if not ok:
            return
        for p in _paths(name, args, d):
            if not _outside(p, d, root, ctl):
                continue
            if name in STAT_FAMILY and res is not None:
                try:
                    if os.path.isdir(p) and not os.path.islink(p):
                        continue                          # rule (g): a directory stat carries no name
                except OSError:
                    pass
            hits.append((name, p))

    for line in raw:
        m = RESUME.match(line)
        if m:
            pid, _name, tail = m.groups()
            head = pending.pop(pid, None)
            if head is not None:
                call = split_call(head + tail)
                if call:
                    consider(*call)
            continue
        pm = PIDLINE.match(line)
        if not pm:
            continue
        pid, body = pm.groups()
        if "<unfinished ...>" in body:
            pending[pid] = body.split("<unfinished ...>")[0]
            continue
        call = split_call(body)
        if call:
            consider(*call)
    for head in pending.values():                        # blocked and never resumed: rule (h)
        call = split_call(head)
        if call:
            consider(call[0], call[1], None)
    return hits, calls


def run_fence(k44, lane, root, ctl, empty, fence_copy, fx, n):
    """One fence decision in a read-only sandbox under a host `strace -f -y` -> (verdict, reason, hits, calls)."""
    logdir = root / "strace" / secrets.token_hex(8)
    logdir.mkdir(parents=True)
    log = logdir / "log"
    d = fx["dir"]
    cmd = [STRACE, "-f", "-qq", "-y", "-s", "256", "-e", "trace=" + TRACE_SET, "-o", str(log)] \
        + k44.ro_sandbox(hide=k44.hide_list((lane,), existing=True), empty=empty) \
        + [k44.PY, "-I", str(ctl / "harness.py"), str(fence_copy), str(d), fx["tool"], json.dumps(fx["argv"])]
    p = subprocess.Popen(cmd, cwd=str(d), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, start_new_session=True,
                         env={"PATH": k44.PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8",
                              "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"})
    try:
        _out, err = p.communicate(timeout=FENCE_TIMEOUT)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except OSError:
            pass
        p.communicate()
        shutil.rmtree(logdir, ignore_errors=True)
        return "HUNG", "", [], 0
    try:
        raw = log.read_text(errors="replace").splitlines()
        size = log.stat().st_size
    except OSError:
        raw, size = [], 0
    keep = os.environ.get("K46_KEEP_STRACE")
    if keep:
        shutil.copy(log, pathlib.Path(keep) / f"f{n:05d}.txt")
    shutil.rmtree(logdir, ignore_errors=True)
    rc = p.returncode
    verdict = "BREACH" if rc == 10 else ("ADMIT" if rc == 11 else "ERROR")
    why = (err.strip().splitlines() or [""])[-1][:160]
    if size == 0 or not raw or any("\x00" in line for line in raw) or not any("execve(" in line for line in raw):
        return verdict, "LOG-TAMPER " + why, [("log", "<untrusted>")], 0     # rule (e)
    hits, calls = analyse(raw, d, root, ctl)
    return verdict, why, hits, calls


def build_module(k44, lane, root, empty, f, rng, ctl):
    """Build one module in the round-44 build sandbox (that counter's own builder, unchanged) and return its
    fixtures; no fence is consulted here. Rule (b): the build dir, the module copy and the fixture parent carry
    per-run tokens, and the parent is padded to PAD children."""
    dest = root / "fx" / token(rng)
    dest.mkdir(parents=True)
    tmp = root / "btmp" / token(rng)
    tmp.mkdir(parents=True)
    mods = root / "mods"
    mods.mkdir(exist_ok=True)
    mod_copy = mods / f"{token(rng)}.py"
    mod_copy.write_text(f.read_text())
    bfd = os.memfd_create("k46-builder", 0)
    try:
        os.write(bfd, k44.builder_source().encode())
        os.lseek(bfd, 0, os.SEEK_SET)
        cmd = k44.ro_sandbox(writable=(dest, tmp),
                             hide=k44.hide_list((lane, ctl), existing=True),
                             ro_data=((bfd, k44.BUILDER_SLOT),), empty=empty) \
            + [k44.PY, k44.BUILDER_SLOT, str(mod_copy), str(dest)]
        r = subprocess.run(cmd, cwd=str(dest), capture_output=True, text=True, timeout=1800,
                           env={"PATH": k44.PATH, "HOME": "/nonexistent", "TMPDIR": str(tmp), "LANG": "C.UTF-8",
                                "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"},
                           pass_fds=(bfd,))
    finally:
        os.close(bfd)
    built = [l for l in r.stdout.splitlines() if l.startswith("BUILT ")]
    if r.returncode != 0 or len(built) != 1:
        raise RuntimeError(f"{f.parent.name}/{f.name} failed to build (rc={r.returncode}): {r.stderr.strip()[-200:]}")
    out = []
    for k, fx in enumerate(json.loads(built[0][6:])):
        d = dest / f"f{k:03d}"
        argv = fx.get("argv")
        if not (isinstance(fx.get("fid"), str) and fx.get("tool") in k44.TOOLS and isinstance(argv, list)
                and all(isinstance(t, str) for t in argv) and d.is_dir()):
            raise ValueError(f"fixture {fx.get('fid')!r} of {f.parent.name}/{f.name} breaks the module contract")
        out.append({"fid": fx["fid"], "tool": fx["tool"], "argv": argv, "dir": d.resolve(),
                    "module": f"{f.parent.name}/{f.name}"})
    n_children = len(list(dest.iterdir()))
    if n_children > PAD:
        print(f"PAD-OVERFLOW parent={dest.name} children={n_children} (child count survives for this module)")
    for _ in range(PAD - n_children):
        (dest / token(rng)).mkdir()
    return out


def copy_rows(refdir, lane):
    """f1-f10 must be byte copies of `plans/refusals45/`; returns the copies that differ or are absent."""
    bad = []
    for f in sorted((lane / REFUSAL_SOURCE_REL).glob("*.py")):
        got = refdir / f.name
        if not got.is_file():
            bad.append(str(got))
            print(f"COPY {f.name} ABSENT")
        elif sha256(got) != sha256(f):
            bad.append(str(got))
            print(f"COPY {f.name} DIFFERS")
        else:
            print(f"COPY {f.name} ok")
    return bad


def pin_issues(lane, refdir, sealdir, default_mode):
    issues = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
    if default_mode:
        for f in sorted(refdir.glob("*.py")) + sorted(sealdir.glob("*.py")):
            rel = f.relative_to(lane).as_posix()
            if rel not in PINS:
                issues.append(rel + ":unpinned")           # stage 2 pins every hostile input
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--refusals", default=None, help="testing only: refusal module dir")
    ap.add_argument("--sealed", default=None, help="testing only: sealed module dir")
    ap.add_argument("--fence", default=None, help="testing only: fence file under test")
    ap.add_argument("--seed", default=None, help="testing only: fixed token seed")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    rng = secrets.SystemRandom() if a.seed is None else random.Random(int(a.seed, 16))
    default_mode = a.refusals is None and a.sealed is None and a.fence is None and a.seed is None
    refdir = pathlib.Path(a.refusals).resolve() if a.refusals else lane / REFUSAL_REL
    sealdir = pathlib.Path(a.sealed).resolve() if a.sealed else lane / SEALED_REL
    fence_src = pathlib.Path(a.fence).resolve() if a.fence else lane / FENCE_REL

    issues = pin_issues(lane, refdir, sealdir, default_mode)
    print(f"PINS total={len(PINS)} mismatched={len(issues)}" + (f" first={issues[0]}" if issues else ""))
    for rel in issues[1:]:
        print(f"PIN-MISMATCH {rel}")
    for exe in ("/usr/bin/bwrap", "/usr/bin/python3", STRACE):
        if not os.access(exe, os.X_OK):
            print(f"SETUP {exe} is required", file=sys.stderr)
            return 2
    if K44_REL in issues:
        print("SETUP the round-44 counter (builder) is not at its pinned digest", file=sys.stderr)
        return 2
    if a.work:
        if pathlib.Path(a.work).resolve().is_relative_to(lane):
            print("SETUP --work must not lie inside the lane", file=sys.stderr)
            return 2
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k46-c1-", dir=a.work)).resolve()
    if root.is_relative_to(lane):
        print("SETUP scratch root lies inside the lane; pass --work", file=sys.stderr)
        shutil.rmtree(root, ignore_errors=True)
        return 2
    # bwrap is itself traced (rule e): every bind source must live OUTSIDE the counted scratch root, so its
    # mount-time opens cannot look like fence touches.
    empty = pathlib.Path(tempfile.mkdtemp(prefix=root.name + "-empty-", dir=root.parent))
    try:
        k44 = load(lane / K44_REL, "kengaku_r44_counter")
        ctl = root / "ctl"
        ctl.mkdir()
        (ctl / "harness.py").write_text(HARNESS)
        fence_copy = ctl / "fence.py"
        if not fence_src.is_file():
            print(f"FENCE {fence_src} absent")
            fence_copy.write_text("def breach(d, argv, tool):\n    raise RuntimeError('fence absent')\n")
        else:
            fence_copy.write_bytes(fence_src.read_bytes())
            print(f"FENCE source={fence_src} sha256={sha256(fence_copy)}")
        print(f"LAYOUT refusals={refdir} sealed={sealdir} pad={PAD} jobs={a.jobs}")
        if default_mode:
            cp_bad = copy_rows(refdir, lane) if refdir.is_dir() else []
        else:
            cp_bad = []
            print("COPY-CHECK skipped (refusals dir overridden for testing)")
        groups = {
            "refusal": sorted(refdir.glob("*.py")),
            "sealed": sorted(sealdir.glob("*.py")),
            "honest": [f for rel in HONEST_RELS for f in sorted((lane / rel).glob("*.py"))],
        }
        for g in ("refusal", "sealed", "honest"):
            print(f"MODULES {g} total={len(groups[g])}"
                  + ("" if groups[g] else " (directory absent or empty)"))
        built = {g: [] for g in groups}
        build_errors = {g: 0 for g in groups}
        order = [(g, f) for g in groups for f in groups[g]]
        rng.shuffle(order)                                # rule (b): build order carries no signal
        for g, f in order:
            try:
                built[g].append((f, build_module(k44, lane, root, empty, f, rng, ctl)))
            except (RuntimeError, ValueError, KeyError, TypeError, json.JSONDecodeError,
                    subprocess.TimeoutExpired) as e:
                build_errors[g] += 1
                print(f"BUILD-ERROR {g} {f.parent.name}/{f.name} {str(e)[:160]}")
        jobs = [(g, f, fx) for g in built for f, fxs in built[g] for fx in fxs]
        rng.shuffle(jobs)                                 # rule (b): run order carries no signal
        with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as ex:
            res = list(ex.map(lambda t: run_fence(k44, lane, root, ctl, empty, fence_copy, t[1][2], t[0]),
                              enumerate(jobs)))
        per = {}
        for (g, f, fx), (verdict, why, hits, calls) in zip(jobs, res):
            per.setdefault((g, f), []).append((fx, verdict, why, hits, calls))
            head = f"{hits[0][0]}:{hits[0][1]}" if hits else ""
            print(f"FENCE-RUN {g} {fx['module']} {fx['fid']} {verdict} touches={len(hits)} calls={calls}"
                  + (f" first={head}" if head else "") + (f" -- {why}" if why else ""))

        def rollup(g):
            clean = leaked = read = hung = 0
            for f, fxs in built[g]:
                rows = per.get((g, f), [])
                n_admit = sum(v in ("ADMIT", "ERROR") for _fx, v, _w, _o, _c in rows)
                n_hung = sum(v == "HUNG" for _fx, v, _w, _o, _c in rows)
                n_hit = sum(len(o) for _fx, _v, _w, o, _c in rows)
                if not rows or n_admit:
                    verdict = "LEAKED"
                    leaked += 1
                elif n_hung:
                    verdict = "HUNG"
                    hung += 1
                elif n_hit:
                    verdict = "READ"
                    read += 1
                else:
                    verdict = "clean"
                    clean += 1
                print(f"{g.upper()} {f.name} {verdict} fixtures={len(rows)} admitted={n_admit} hung={n_hung}"
                      f" touches={n_hit}")
            return clean, leaked, read, hung

        rclean, rleaked, rread, rhung = rollup("refusal")
        rtotal = len(groups["refusal"])
        rbuild = build_errors["refusal"] + len(cp_bad)
        print(f"REFUSALS total={rtotal} clean={rclean} leaked={rleaked} read={rread} hung={rhung}"
              f" build_errors={rbuild}")
        sclean, sleaked, sread, shung = rollup("sealed")
        stotal = len(groups["sealed"])
        sbuild = build_errors["sealed"]
        print(f"SEALED total={stotal} clean={sclean} leaked={sleaked} read={sread} hung={shung}"
              f" build_errors={sbuild}")
        hrows = [row for (g, _f), rows in per.items() if g == "honest" for row in rows]
        h_adm = sum(_v == "ADMIT" and not _o for _fx, _v, _w, _o, _c in hrows)
        h_ref = sum(_v in ("BREACH", "ERROR") for _fx, _v, _w, _o, _c in hrows)
        h_read = sum(bool(_o) for _fx, _v, _w, _o, _c in hrows)
        h_hung = sum(_v == "HUNG" for _fx, _v, _w, _o, _c in hrows)
        hbuild = build_errors["honest"]
        print(f"HONEST fixtures={len(hrows)} admitted={h_adm} refused={h_ref} read={h_read} hung={h_hung}"
              f" build_errors={hbuild}")
        contradicted = rleaked + rread + rhung + rbuild + sleaked + sread + shung + sbuild
        print(f"CALIBRATION advertised={rtotal + stotal} contradicted={contradicted}")
        after = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
        fails = []
        if issues:
            fails.append(f"pins={len(issues)}")
        if after:
            fails.append(f"pins-after={len(after)}")
        if rtotal != REFUSAL_FLOOR or rtotal != len(groups["refusal"]):
            fails.append(f"refusals-total={rtotal}!={REFUSAL_FLOOR}")
        if rclean != rtotal or rleaked or rread or rhung or rbuild:
            fails.append("refusals-not-clean")
        if stotal != SEALED_FLOOR:
            fails.append(f"sealed-total={stotal}!={SEALED_FLOOR}")
        if sclean != stotal or sleaked or sread or shung or sbuild:
            fails.append("sealed-not-clean")
        if len(hrows) != HONEST_TOTAL or h_adm != HONEST_TOTAL or h_ref or h_read or h_hung or hbuild:
            fails.append("honest-not-admitted")
        if contradicted:
            fails.append(f"contradicted={contradicted}")
        good = not fails
        print("REASON " + (",".join(fails) if fails else "-"))
        print(f"PREDICATE C1 {'pass' if good else 'fail'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(empty, ignore_errors=True)
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
