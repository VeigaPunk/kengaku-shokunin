#!/usr/bin/env python3
"""scratch_guard.py -- sentinel-bound guard for a hyaku shared scratch root.

Round-41 closure R2 (defect D1): a wave-1 seat ran ``rm -rf`` on the shared round root and
destroyed other seats' work. The L1 already greps the sentinel before each measurement
(``.ufo/waves/round-42/integrate/measure.sh:9``); this tool gives every seat the same two
operations as one stdlib command, so nothing in the envelope needs shell ``rm``.

Commands
--------
``check <root> [--round N] [--json]``
    Exit 0 iff ``<root>/.ROUND-ROOT-SENTINEL`` exists and its content names the round
    (``kengaku r<NN> round root``, the round-42 wording at
    ``/fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL``). When ``--round N`` is given
    the named round must equal N. Every direct subdirectory (a seat; the L1 included) is
    printed with its apparent size; symlinked seats are marked and never walked.
    Exit 1 when the sentinel is missing, unparseable, or names another round; exit 2 when
    the root is not a directory or the sentinel cannot be read (cannot evaluate).
    Read-only: nothing under <root> is created, touched or written.

``safe-rm <root> <seat> <path> [--dry-run]``
    Delete ``<path>`` only when it resolves inside ``<root>/<seat>``; otherwise exit 2 and
    delete nothing. Refused, always:

    * the root itself, and any ancestor of it (``target-is-root``);
    * ``<root>/.ROUND-ROOT-SENTINEL`` (``target-is-sentinel``);
    * another seat's directory or anything under it
      (``target-resolves-outside-seat`` / ``target-outside-seat``);
    * any path containing a ``..`` component, before resolution (``target-dotdot``);
    * a target that is, or is reached through, a symlink resolving outside the seat
      (``target-resolves-outside-seat``) -- ``rm -rf`` would follow the parent link while
      walking, so the resolved path, not the literal one, decides;
    * ``<root>/<seat>`` that is itself a symlink (``seat-is-symlink``): a link named after
      seat A must never delete seat B's bytes;
    * a seat name that is not one path component (``seat-invalid``) and a root whose
      sentinel is absent or unreadable (``root-untrusted`` / ``root-not-a-directory``).

    Allowed: any path at or below ``<root>/<seat>``, including the seat directory itself (a
    seat's cleanup trap deletes its own ``$S``). A relative ``<path>`` is relative to
    ``<root>/<seat>`` -- never to the caller's cwd -- so ``cd`` cannot move the anchor.
    A missing target prints ``ABSENT`` and exits 0 (traps re-run); a refused delete exits 2.

``--selftest``
    Builds a throwaway root under ``TMPDIR`` with seats, a symlinked seat, an outside tree
    and a sentinel, then drives every refusal and every allow through the same dispatch as
    the CLI. Each refusal case also proves it is able to fail: the refused target still
    exists, is writable, and the same naive operation succeeds on a twin at a legal path.
    Exit 0 iff every case passes; prints ``SELFTEST ok=<k>/<n>``.

Exit codes: ``0`` ok / deleted / absent; ``1`` check red (sentinel missing, unparseable,
round mismatch) or a failing selftest case; ``2`` usage, cannot evaluate, or a refused
delete. Stdlib only; no subprocess, no network, no shell.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import shutil
import stat
import sys
import tempfile

SENTINEL = ".ROUND-ROOT-SENTINEL"
SENTINEL_RE = re.compile(r"kengaku\s+r(\d+)\s+round\s+root", re.IGNORECASE)
SENTINEL_MAX = 4096


# ---------------------------------------------------------------- sentinel / sizes

def sentinel_state(root):
    """Return (text, None) or (None, reason). Never writes."""
    path = os.path.join(root, SENTINEL)
    if not os.path.isfile(path):
        return None, "sentinel-missing"
    try:
        with open(path, "rb") as fh:
            raw = fh.read(SENTINEL_MAX)
    except OSError as exc:
        return None, "sentinel-unreadable:%s" % (exc.strerror or exc)
    return raw.decode("utf-8", "replace"), None


def round_named(text):
    """The round number the sentinel names, or None."""
    if not text:
        return None
    m = SENTINEL_RE.search(text)
    return int(m.group(1)) if m else None


def tree_size(path):
    """Apparent size of a path, walking directories without following symlinks."""
    try:
        st = os.lstat(path)
    except OSError:
        return 0
    if not stat.S_ISDIR(st.st_mode):
        return st.st_size
    total = 0
    stack = [path]
    while stack:
        cur = stack.pop()
        try:
            entries = list(os.scandir(cur))
        except OSError:
            continue
        for entry in entries:
            try:
                est = entry.stat(follow_symlinks=False)
            except OSError:
                continue
            total += est.st_size
            if stat.S_ISDIR(est.st_mode):
                stack.append(entry.path)
    return total


def human(n):
    value = float(n)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024.0 or unit == "TiB":
            return ("%d%s" % (n, unit)) if unit == "B" else ("%.1f%s" % (value, unit))
        value /= 1024.0
    return "%dB" % n


def seat_rows(root):
    """(seats, rootfiles, error); a seat is every direct child that is a directory or a link."""
    seats, rootfiles = [], []
    try:
        entries = sorted(os.scandir(root), key=lambda e: e.name)
    except OSError as exc:
        return None, None, exc
    for entry in entries:
        try:
            is_link = entry.is_symlink()
        except OSError:
            is_link = False
        if is_link or entry.is_dir(follow_symlinks=False):
            seats.append((entry.name, tree_size(entry.path), is_link))
        else:
            rootfiles.append(entry.name)
    return seats, rootfiles, None


# ---------------------------------------------------------------- check

def cmd_check(rootarg, want_round=None, as_json=False):
    root = os.path.realpath(rootarg)
    if not os.path.isdir(root):
        if as_json:
            print(json.dumps({"ok": False, "root": root, "reason": "root-not-a-directory"},
                             sort_keys=True))
        else:
            print("SETUP root-not-a-directory root=%s" % root)
        return 2

    text, why = sentinel_state(root)
    if text is None:
        reason = why
        named = None
    else:
        named = round_named(text)
        if named is None:
            reason = "sentinel-no-round"
        elif want_round is not None and named != want_round:
            reason = "round-mismatch"
        else:
            reason = None

    seats, rootfiles, walk_err = seat_rows(root)
    if walk_err is not None:
        if as_json:
            print(json.dumps({"ok": False, "root": root, "reason": "root-unreadable:%s"
                              % (walk_err.strerror or walk_err)}, sort_keys=True))
        else:
            print("SETUP root-unreadable root=%s error=%s" % (root, walk_err.strerror or walk_err))
        return 2

    total = sum(size for _, size, _ in seats)
    ok = reason is None

    if as_json:
        print(json.dumps({
            "ok": ok,
            "root": root,
            "reason": reason,
            "sentinel": {
                "name": SENTINEL,
                "present": text is not None,
                "round": named,
                "bytes": len(text.encode("utf-8")) if text is not None else 0,
                "text": (text.strip() if text is not None else ""),
            },
            "want_round": want_round,
            "seats": [{"name": name, "bytes": size, "symlink": link}
                      for name, size, link in seats],
            "rootfiles": rootfiles,
            "seat_count": len(seats),
            "total_bytes": total,
        }, indent=2, sort_keys=True))
        return 0 if ok else 1

    print("ROOT %s" % root)
    if text is not None:
        print("SENTINEL %s round=%s bytes=%d text=%s"
              % (SENTINEL, named if named is not None else "?", len(text.encode("utf-8")),
                 json.dumps(text.strip())))
    else:
        print("SENTINEL %s present=no reason=%s" % (SENTINEL, why))
    for name, size, link in seats:
        print("SEAT %s bytes=%d size=%s%s"
              % (name, size, human(size), " symlink(not-walked)" if link else ""))
    print("ROOTFILES n=%d names=%s" % (len(rootfiles), " ".join(rootfiles)))
    print("TOTAL seats=%d bytes=%d size=%s" % (len(seats), total, human(total)))
    if ok:
        print("CHECK ok round=%s want=%s seats=%d"
              % (named, want_round if want_round is not None else "*", len(seats)))
        return 0
    print("CHECK red reason=%s round=%s want=%s seats=%d"
          % (reason, named, want_round if want_round is not None else "*", len(seats)))
    return 1


# ---------------------------------------------------------------- safe-rm

def _refuse(reason, **fields):
    extra = "".join(" %s=%s" % (k, fields[k]) for k in sorted(fields))
    print("REFUSE reason=%s%s" % (reason, extra))
    return 2


def _seat_valid(seat):
    return (bool(seat) and seat not in (".", "..") and seat != SENTINEL
            and "\0" not in seat and "/" not in seat and os.sep not in seat)


def cmd_safe_rm(rootarg, seat, target, dry_run=False):
    root = os.path.realpath(rootarg)
    if not os.path.isdir(root):
        return _refuse("root-not-a-directory", root=root)
    text, why = sentinel_state(root)
    if text is None:
        return _refuse("root-untrusted", root=root, sentinel=why)
    if not _seat_valid(seat):
        return _refuse("seat-invalid", seat=json.dumps(seat))
    if target == "":
        return _refuse("empty-target", seat=seat)
    if "\0" in target:
        return _refuse("target-nul", seat=seat)

    seat_lex = os.path.join(root, seat)
    if os.path.islink(seat_lex):
        return _refuse("seat-is-symlink", seat=seat,
                       resolves=os.path.realpath(seat_lex))
    if not os.path.isdir(seat_lex):
        return _refuse("seat-missing", seat=seat)
    seat_real = os.path.realpath(seat_lex)
    if seat_real == root:
        return _refuse("seat-is-root", seat=seat)
    if not seat_real.startswith(root + os.sep):
        return _refuse("seat-escapes-root", seat=seat, resolves=seat_real)

    raw_parts = target.replace(os.sep, "/").split("/")
    if ".." in raw_parts:
        return _refuse("target-dotdot", target=json.dumps(target))

    if os.path.isabs(target):
        cand = os.path.normpath(target)
        if cand != seat_lex and not cand.startswith(seat_lex + os.sep):
            return _refuse("target-outside-seat", seat=seat, target=cand,
                           seat_dir=seat_lex)
    else:
        cand = os.path.normpath(os.path.join(seat_lex, target))

    real = os.path.realpath(cand)
    sentinel_path = os.path.join(root, SENTINEL)
    if real == root:
        return _refuse("target-is-root", target=cand)
    if real == sentinel_path or cand == sentinel_path:
        return _refuse("target-is-sentinel", target=cand)
    if not (real == seat_real or real.startswith(seat_real + os.sep)):
        return _refuse("target-resolves-outside-seat", seat=seat, target=cand,
                       resolves=real, seat_dir=seat_real)

    size = tree_size(cand)
    if not os.path.lexists(cand):
        print("ABSENT path=%s seat_dir=%s anchor=seat" % (cand, seat_lex))
        return 0
    if dry_run:
        print("WOULD-DELETE path=%s resolved=%s bytes=%d size=%s"
              % (cand, real, size, human(size)))
        return 0
    try:
        if os.path.islink(cand):
            os.unlink(cand)
        elif os.path.isdir(cand):
            shutil.rmtree(cand)
        else:
            os.unlink(cand)
    except OSError as exc:
        return _refuse("delete-failed", path=cand, error=json.dumps(str(exc)))
    print("DELETE path=%s resolved=%s bytes=%d size=%s" % (cand, real, size, human(size)))
    return 0


# ---------------------------------------------------------------- dispatch

def dispatch(argv):
    parser = argparse.ArgumentParser(
        prog="scratch_guard.py",
        description="Sentinel-bound guard for a shared hyaku scratch root.")
    parser.add_argument("--selftest", action="store_true",
                        help="build a throwaway root and drive every refusal and allow")
    sub = parser.add_subparsers(dest="command")

    p_check = sub.add_parser("check", help="verify the round sentinel and list seats")
    p_check.add_argument("root")
    p_check.add_argument("--round", dest="want_round", type=int, default=None)
    p_check.add_argument("--json", dest="as_json", action="store_true")

    p_rm = sub.add_parser("safe-rm", aliases=["safe_rm"],
                          help="delete a path only inside your own seat directory")
    p_rm.add_argument("root")
    p_rm.add_argument("seat")
    p_rm.add_argument("path")
    p_rm.add_argument("--dry-run", dest="dry_run", action="store_true")

    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.command == "check":
        return cmd_check(args.root, args.want_round, args.as_json)
    if args.command in ("safe-rm", "safe_rm"):
        return cmd_safe_rm(args.root, args.seat, args.path, args.dry_run)
    parser.print_usage()
    return 2


def main(argv=None):
    return dispatch(sys.argv[1:] if argv is None else argv)


# ---------------------------------------------------------------- selftest

def _run(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = dispatch(argv)
    return code, buf.getvalue()


def _reason(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    if not lines:
        return "none"
    tokens = lines[-1].split()
    for tok in tokens:
        if tok.startswith("reason="):
            return tok.split("=", 1)[1]
    return tokens[0].lower()


def _writable(path):
    try:
        return os.access(os.path.realpath(path), os.W_OK)
    except OSError:
        return False


class Harness:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = []

    def case(self, name, ok, detail):
        self.total += 1
        if ok:
            self.passed += 1
            print("case %-34s PASS %s" % (name, detail))
        else:
            self.failed.append(name)
            print("case %-34s FAIL %s" % (name, detail))
        return ok


def selftest():
    base = tempfile.mkdtemp(prefix="scratch-guard-selftest-")
    try:
        return _selftest_in(base)
    finally:
        shutil.rmtree(base, ignore_errors=True)


def _selftest_in(base):
    h = Harness()
    root = os.path.join(base, "root")
    outside = os.path.join(base, "outside")
    bare = os.path.join(base, "bare")
    probe = os.path.join(base, "no-such-dir")

    os.makedirs(os.path.join(root, "L1"))
    os.makedirs(os.path.join(root, "SeatA", "sub"))
    os.makedirs(os.path.join(root, "SeatB"))
    os.makedirs(outside)
    os.makedirs(os.path.join(bare, "SeatA"))
    with open(os.path.join(root, SENTINEL), "w") as fh:
        fh.write("kengaku r42 round root; L1 selftest; seats delete only $S/<SeatName>\n")
    for path, data in (
        (os.path.join(root, "L1", "note.txt"), "l1\n"),
        (os.path.join(root, "SeatA", "keep.txt"), "keep-a\n"),
        (os.path.join(root, "SeatA", "other.txt"), "other-a\n"),
        (os.path.join(root, "SeatA", "sub", "deep.bin"), "x" * 4096),
        (os.path.join(root, "SeatB", "keep.txt"), "keep-b\n"),
        (os.path.join(outside, "precious.txt"), "precious\n"),
        (os.path.join(bare, "SeatA", "keep.txt"), "bare\n"),
    ):
        with open(path, "w") as fh:
            fh.write(data)
    os.symlink(os.path.join(outside, "precious.txt"),
               os.path.join(root, "SeatA", "escape"))
    os.symlink(outside, os.path.join(root, "SeatA", "escapedir"))
    os.symlink(os.path.join("..", SENTINEL),
               os.path.join(root, "SeatA", "sentinel_link"))
    os.symlink("..", os.path.join(root, "SeatA", "rootlink"))
    os.symlink("SeatA", os.path.join(root, "SeatC"))
    os.symlink(".", os.path.join(root, "SeatLink"))

    twin_n = [0]

    def twin(kind):
        """Same naive operation, at a path the guard allows: proves the op itself works."""
        twin_n[0] += 1
        path = os.path.join(root, "SeatB", ".twin%d" % twin_n[0])
        try:
            if kind == "file":
                with open(path, "w") as fh:
                    fh.write("twin\n")
                os.unlink(path)
            elif kind == "dir":
                os.makedirs(os.path.join(path, "d"))
                with open(os.path.join(path, "d", "x"), "w") as fh:
                    fh.write("x\n")
                shutil.rmtree(path)
            else:
                os.symlink(os.path.join(outside, "precious.txt"), path)
                os.unlink(path)
            return True
        except OSError as exc:
            print("  twin-error %s" % exc)
            return False

    sentinel_path = os.path.join(root, SENTINEL)
    seatb_keep = os.path.join(root, "SeatB", "keep.txt")
    precious = os.path.join(outside, "precious.txt")

    # ---- check -------------------------------------------------------------
    code, out = _run(["check", root])
    seats_ok = ("seats=5" in out and "round=42" in out
                and "SEAT SeatC" in out and "symlink(not-walked)" in out
                and "SEAT SeatB bytes=" in out and "SEAT L1 bytes=" in out)
    h.case("check-green", code == 0 and seats_ok,
           "exit=%d expected=0 seats5+round42+symlink-seat=%s" % (code, seats_ok))

    code, out = _run(["check", root, "--round", "41"])
    h.case("check-round-mismatch", code == 1 and _reason(out) == "round-mismatch",
           "exit=%d expected=1 reason=%s" % (code, _reason(out)))

    code, out = _run(["check", bare])
    h.case("check-sentinel-missing", code == 1 and _reason(out) == "sentinel-missing",
           "exit=%d expected=1 reason=%s" % (code, _reason(out)))

    bad = os.path.join(bare, ".ROUND-ROOT-SENTINEL")
    with open(bad, "w") as fh:
        fh.write("kengaku r4x round root; not a round\n")
    code, out = _run(["check", bare])
    h.case("check-sentinel-unparseable", code == 1 and _reason(out) == "sentinel-no-round",
           "exit=%d expected=1 reason=%s" % (code, _reason(out)))
    os.unlink(bad)

    code, out = _run(["check", probe])
    h.case("check-non-directory",
           code == 2 and "SETUP root-not-a-directory" in out,
           "exit=%d expected=2 setup=%s" % (code, "SETUP root-not-a-directory" in out))
    h.case("check-wrote-nothing", not os.path.lexists(probe),
           "probe-absent=%s" % (not os.path.lexists(probe)))

    code, out = _run(["check", root, "--json"])
    try:
        doc = json.loads(out)
        json_ok = (code == 0 and doc["ok"] is True and doc["seat_count"] == 5
                   and doc["sentinel"]["round"] == 42
                   and any(s["symlink"] for s in doc["seats"]))
    except (ValueError, KeyError):
        json_ok = False
    h.case("check-json", json_ok,
           "exit=%d expected=0 parses=%s" % (code, json_ok))

    # ---- allowed deletes ---------------------------------------------------
    code, out = _run(["safe-rm", root, "SeatA", "keep.txt"])
    gone = not os.path.lexists(os.path.join(root, "SeatA", "keep.txt"))
    h.case("allow-delete-file", code == 0 and gone and _reason(out) == "delete",
           "exit=%d expected=0 deleted=%s" % (code, gone))

    code, out = _run(["safe-rm", root, "SeatA", "sub"])
    gone = not os.path.lexists(os.path.join(root, "SeatA", "sub"))
    kept = os.path.lexists(os.path.join(root, "SeatA", "escape"))
    h.case("allow-delete-dir", code == 0 and gone and kept,
           "exit=%d expected=0 deleted=%s sibling-kept=%s" % (code, gone, kept))

    code, out = _run(["safe-rm", root, "SeatA", "ghost.txt"])
    h.case("allow-absent", code == 0 and _reason(out) == "absent"
           and not os.path.lexists(os.path.join(root, "SeatA", "ghost.txt")),
           "exit=%d expected=0 reason=%s no-create=%s"
           % (code, _reason(out), not os.path.lexists(os.path.join(root, "SeatA", "ghost.txt"))))

    code, out = _run(["safe-rm", root, "SeatB", "keep.txt", "--dry-run"])
    h.case("allow-dry-run-keeps", code == 0 and os.path.lexists(seatb_keep)
           and _reason(out) == "would-delete",
           "exit=%d expected=0 kept=%s reason=%s"
           % (code, os.path.lexists(seatb_keep), _reason(out)))

    # ---- refusals: each proves it can fail ---------------------------------
    def refuse(name, argv, target, kind, want_reason, expect_writable=True):
        code, out = _run(argv)
        kept = os.path.lexists(target)
        writ = _writable(target)
        t_ok = twin(kind)
        reason = _reason(out)
        ok = (code == 2 and kept and t_ok and reason == want_reason
              and (writ or not expect_writable))
        h.case(name, ok,
               "exit=%d expected=2 reason=%s want=%s kept=%s writable=%s naive_twin=%s"
               % (code, reason, want_reason, kept, writ, t_ok))
        return out

    refuse("refuse-root", ["safe-rm", root, "SeatA", root], root, "dir",
           "target-outside-seat")
    refuse("refuse-root-dot", ["safe-rm", root, "SeatA", ".."], root, "dir",
           "target-dotdot")
    refuse("refuse-sentinel", ["safe-rm", root, "SeatA", sentinel_path], sentinel_path,
           "file", "target-outside-seat")
    refuse("refuse-other-seat", ["safe-rm", root, "SeatA", seatb_keep], seatb_keep,
           "file", "target-outside-seat")
    refuse("refuse-dotdot-relative", ["safe-rm", root, "SeatA", "../SeatB/keep.txt"],
           seatb_keep, "file", "target-dotdot")
    refuse("refuse-dotdot-absolute",
           ["safe-rm", root, "SeatA", os.path.join(root, "SeatA", "..", "SeatB", "keep.txt")],
           seatb_keep, "file", "target-dotdot")
    refuse("refuse-symlink-file-escape",
           ["safe-rm", root, "SeatA", "escape"], precious, "link",
           "target-resolves-outside-seat")
    refuse("refuse-symlink-dir-escape",
           ["safe-rm", root, "SeatA", "escapedir/precious.txt"], precious, "dir",
           "target-resolves-outside-seat")
    refuse("refuse-symlink-dir-rmtree",
           ["safe-rm", root, "SeatA", "escapedir"], outside, "dir",
           "target-resolves-outside-seat")
    refuse("refuse-symlink-to-sentinel",
           ["safe-rm", root, "SeatA", "sentinel_link"], sentinel_path, "link",
           "target-is-sentinel")
    refuse("refuse-symlink-to-root",
           ["safe-rm", root, "SeatA", "rootlink"], root, "dir", "target-is-root")
    refuse("refuse-seat-traversal", ["safe-rm", root, "../outside", "precious.txt"],
           precious, "file", "seat-invalid")
    refuse("refuse-seat-dot", ["safe-rm", root, ".", "precious.txt"], root, "dir",
           "seat-invalid")
    refuse("refuse-seat-empty", ["safe-rm", root, "", "precious.txt"], root, "dir",
           "seat-invalid")
    refuse("refuse-seat-symlink-root",
           ["safe-rm", root, "SeatLink", "."], root, "dir", "seat-is-symlink")
    refuse("refuse-seat-symlink-other",
           ["safe-rm", root, "SeatC", "other.txt"],
           os.path.join(root, "SeatA", "other.txt"), "file", "seat-is-symlink")
    refuse("refuse-empty-target", ["safe-rm", root, "SeatA", ""], root, "dir",
           "empty-target")
    refuse("refuse-nul-target", ["safe-rm", root, "SeatA", "x\0y"], root, "dir",
           "target-nul")
    refuse("refuse-fs-root", ["safe-rm", root, "SeatA", "/"], os.sep, "dir",
           "target-outside-seat", expect_writable=False)
    refuse("refuse-bare-root", ["safe-rm", bare, "SeatA", "keep.txt"],
           os.path.join(bare, "SeatA", "keep.txt"), "file", "root-untrusted")

    # a symlink inside the seat pointing inside the seat: unlink the link only
    os.symlink("other.txt", os.path.join(root, "SeatA", "inlink"))
    code, out = _run(["safe-rm", root, "SeatA", "inlink"])
    link_gone = not os.path.lexists(os.path.join(root, "SeatA", "inlink"))
    target_kept = os.path.lexists(os.path.join(root, "SeatA", "other.txt"))
    h.case("allow-unlink-inside-symlink", code == 0 and link_gone and target_kept,
           "exit=%d expected=0 link-gone=%s target-kept=%s"
           % (code, link_gone, target_kept))

    # ---- own seat dir is allowed, and only that ----------------------------
    code, out = _run(["safe-rm", root, "SeatA", "."])
    gone = not os.path.lexists(os.path.join(root, "SeatA"))
    kept = os.path.lexists(seatb_keep) and os.path.lexists(sentinel_path)
    h.case("allow-delete-own-seat", code == 0 and gone and kept,
           "exit=%d expected=0 seat-gone=%s siblings-kept=%s" % (code, gone, kept))
    code, out = _run(["check", root])
    h.case("check-after-seat-gone", code == 0 and "seats=4" in out,
           "exit=%d expected=0 seats4=%s" % (code, "seats=4" in out))
    code, out = _run(["safe-rm", root, "SeatA", "keep.txt"])
    h.case("refuse-missing-seat", code == 2 and _reason(out) == "seat-missing",
           "exit=%d expected=2 reason=%s" % (code, _reason(out)))
    code, out = _run(["safe-rm", root, "SeatB", "keep.txt"])
    h.case("allow-after-refusals", code == 0 and not os.path.lexists(seatb_keep),
           "exit=%d expected=0 deleted=%s" % (code, not os.path.lexists(seatb_keep)))

    print("SELFTEST ok=%d/%d" % (h.passed, h.total))
    if h.failed:
        print("SELFTEST failed=%s" % ",".join(h.failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
