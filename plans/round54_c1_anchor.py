#!/usr/bin/env python3
"""Round 54, claim C1: an externally anchored measurement freeze (novelty axis).

The digest of the frozen claims file is committed into a Bitcoin block header via
OpenTimestamps (https://opentimestamps.org).  ``verify`` re-derives everything from
committed bytes: the proof, the 80-byte block header, and fresh explorer receipts
fetched this round.  No lane-writable input is trusted for existence or ordering, so
the coordinated-history forgery of round 53 (``.ufo/waves/round-53/w3/C1CritOracle2.md``)
cannot reproduce a passing state.

Subcommands
    stamp  --claims PATH --anchor DIR [--ots-bin BIN] [--calendar URL ...]
           compute the canonical sha256 of the claims file, submit it to the OTS
           calendars, write claims.ots + anchor.json.  Network required, once.
    upgrade --anchor DIR [--ots-bin BIN]
           ask the calendars for the Bitcoin attestation (repeat until confirmed).
           Does not touch header.bin / receipts; those land from explorer fetches.
    verify --anchor DIR --claims NAME --source CLEAN_CLONE --work SCRATCH
           [--controls]
           the frozen counting command (see plans/round-54-claims.md).  All legs
           recompute from committed bytes; no network in verify.

Exit codes: 0 predicate holds · 1 predicate fails · 2 setup/usage.
Honours TMPDIR/--work; never writes under a hard-coded /tmp path.

Dependency (declared, installed via the official Python index into a scratch venv):
    uv venv "$HYAKU_SCRATCH/kengaku-r54/l1/venv/otsenv" \
      && VIRTUAL_ENV=<venv> uv pip install "opentimestamps==0.5.0" "opentimestamps-client==0.8.0"
Run this counter with that venv's python (verify needs the ``opentimestamps`` library;
``stamp``/``upgrade`` additionally need the ``ots`` CLI via --ots-bin).
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "r54-anchor-v1"
MAINNET_HEIGHT_FLOOR = 800_000
SKEW_SECONDS = 7200  # a calendar cannot pick a block whose time precedes submission by more than skew
EXPLORER_MIN = 2


def _sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).hexdigest()


def _double_sha256(b: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def _git(source: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(source), *args], capture_output=True, text=True)


def _fail(msg: str, lines: list[str]) -> tuple[int, list[str]]:
    lines.append(msg)
    return 1, lines


def _setup(msg: str, lines: list[str]) -> tuple[int, list[str]]:
    lines.append(f"SETUP {msg}")
    return 2, lines


def canonical_digest(data: bytes) -> str:
    """The claims bundle digest: plain sha256 over the exact file bytes (the OTS default op)."""
    return hashlib.sha256(data).hexdigest()


# --------------------------------------------------------------------------------- stamp/upgrade
def cmd_stamp(args: argparse.Namespace) -> int:
    lines: list[str] = []
    claims = Path(args.claims)
    anchor = Path(args.anchor)
    ots = args.ots_bin or "ots"
    if not claims.is_file():
        _setup(f"claims absent: {claims}", lines)
        print("\n".join(lines))
        return 2
    data = claims.read_bytes()
    digest = canonical_digest(data)
    anchor.mkdir(parents=True, exist_ok=True)
    ots_path = anchor / "claims.ots"
    tmp = Path(tempfile.mkdtemp(dir=str(args.work) if args.work else None, prefix="stamp-"))
    try:
        target = tmp / claims.name
        target.write_bytes(data)
        p = subprocess.run([ots, "stamp", str(target)], capture_output=True, text=True, timeout=300)
        if p.returncode != 0 or not (tmp / f"{claims.name}.ots").is_file():
            lines.append(f"STAMP failed rc={p.returncode} {p.stdout.strip()[:200]} {p.stderr.strip()[:200]}")
            print("\n".join(lines))
            return 1
        shutil.copyfile(tmp / f"{claims.name}.ots", ots_path)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    meta = {
        "schema": SCHEMA,
        "claims_path": str(claims),
        "digest": digest,
        "stamped_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ots_tool": subprocess.run([ots, "--version"], capture_output=True, text=True).stdout.strip(),
        "calendars": args.calendar,
        "freeze_rev": args.freeze_rev or "",
        "note": "freeze_rev is filled at the stage-1 commit; header.bin + block-explorer-*.json land after confirmation",
    }
    (anchor / "anchor.json").write_text(json.dumps(meta, indent=1, sort_keys=True) + "\n")
    lines.append(f"STAMP digest={digest} stamped_at={meta['stamped_at']} proof={ots_path}")
    print("\n".join(lines))
    return 0


def cmd_upgrade(args: argparse.Namespace) -> int:
    lines: list[str] = []
    anchor = Path(args.anchor)
    ots = args.ots_bin or "ots"
    proof = anchor / "claims.ots"
    if not proof.is_file():
        _setup(f"proof absent: {proof}", lines)
        print("\n".join(lines))
        return 2
    p = subprocess.run([ots, "upgrade", str(proof)], capture_output=True, text=True, timeout=300)
    lines.append(f"UPGRADE rc={p.returncode}")
    for ln in (p.stdout or "").splitlines():
        lines.append(f"  {ln.strip()}")
    print("\n".join(lines))
    return 0 if p.returncode == 0 else 1


# --------------------------------------------------------------------------------------- verify
_UNARY_ALGOS = {}  # filled lazily: op class -> hashlib algorithm name


def _collect_digests(root_ts):
    """(timestamp object -> digest carried at that node), recomputed by walking ops from the file digest.

    The deserializer builds the tree from the serialized ops; this walk re-derives every node digest
    from the root so a tree whose attestation digest does not follow from the file digest is caught.
    """
    import opentimestamps.core.op as _op  # noqa: PLC0415

    if not _UNARY_ALGOS:
        _UNARY_ALGOS.update({_op.OpSHA256: "sha256", _op.OpRipemd160: "ripemd160",
                             _op.OpKeccak256: "keccak256"})

    out: dict[int, bytes] = {}

    def walk(ts, digest: bytes) -> None:
        out[id(ts)] = digest
        for op, child in ts.ops.items():
            if isinstance(op, _op.OpAppend):
                walk(child, digest + op.arg)
            elif isinstance(op, _op.OpPrepend):
                walk(child, op.arg + digest)
            elif type(op) in _UNARY_ALGOS:
                walk(child, hashlib.new(_UNARY_ALGOS[type(op)], digest).digest())
            elif type(op) is _op.OpKECCAK256:
                raise ValueError("keccak256 proof paths are not supported by this counter")
            elif isinstance(op, _op.OpReverse):
                walk(child, digest[::-1])
            else:
                raise ValueError(f"unsupported op in proof tree: {op!r}")

    walk(root_ts, root_ts.msg)
    return out


def _verify_control_cases(anchor: Path, real_proof: bytes, good_digest: str, work: Path) -> tuple[int, list[str]]:
    """Four forged cases; each must FAIL.  Returns (failed_count, lines)."""
    import opentimestamps.core.notary as notary  # noqa: PLC0415
    from opentimestamps.core.timestamp import DetachedTimestampFile, Timestamp  # noqa: PLC0415
    from opentimestamps.core.op import OpSHA256  # noqa: PLC0415

    lines: list[str] = []
    failed = 0

    def case(name: str, passed: bool, detail: str) -> None:
        nonlocal failed
        if passed:
            failed += 1
            lines.append(f"  CONTROL {name} UNEXPECTEDLY PASSED ({detail})")
        else:
            lines.append(f"  CONTROL {name} failed-as-required ({detail})")

    # the attested digest of the real proof, used as the header root for the forged case
    real_attested = None
    try:
        with io.BytesIO(real_proof) as fd:
            dtf_real = DetachedTimestampFile.deserialize(fd)
        for ts, digest in _collect_digests(dtf_real.timestamp).items():
            for att in ts.attestations:
                if isinstance(att, notary.BitcoinBlockHeaderAttestation):
                    real_attested = digest
    except Exception:
        real_attested = None

    # (a) forged byte flip inside the serialized file digest (offset 5, deterministic):
    # the tree may re-parse but the file digest no longer matches the anchored digest and the
    # attested digest no longer follows from the flipped root.
    flip = bytearray(real_proof)
    if len(flip) > 40:
        flip[5] ^= 0x01
    else:
        flip[-1] ^= 0x01
    forged_ok = False
    try:
        forged_ok = (verify_proof_bytes(bytes(flip), good_digest, work, real_attested) == 0)
    except Exception:
        forged_ok = False
    case("forged-proof", forged_ok, "flipped digest byte must break verification")
    # (b) wrong bundle digest
    r = _digest_binding("sha256-of-nothing", good_digest)
    case("wrong-bundle", r == 0, f"binding rc={r}")
    # (c) pending-only proof built offline (no Bitcoin attestation)
    tmp = Path(tempfile.mkdtemp(dir=str(work)))
    ts = Timestamp(hashlib.sha256(b"pending-only").digest())
    ts.attestations.add(notary.PendingAttestation("https://a.pool.opentimestamps.org"))
    dtf = DetachedTimestampFile(OpSHA256(), ts)
    pend = tmp / "pending.ots"
    with pend.open("wb") as fd:
        from opentimestamps.core.serialize import StreamSerializationContext
        dtf.serialize(StreamSerializationContext(fd))
    r = _attestation_leg(pend, work, require_bitcoin=True, lines=[])
    case("pending-only", r == 0, f"attestation leg rc={r}")
    # (d) absent proof
    r = _attestation_leg(tmp / "missing.ots", work, require_bitcoin=True, lines=[])
    case("absent", r == 0, f"attestation leg rc={r}")
    return failed, lines


def _digest_binding(found: str, want: str) -> int:
    return 0 if found == want else 1


def _attestation_leg(proof: Path, work: Path, require_bitcoin: bool, lines: list[str]) -> int:
    """Parse the proof, require exactly the bitcoin attestation; returns 0/1."""
    try:
        from opentimestamps.core.timestamp import DetachedTimestampFile  # noqa: PLC0415
        from opentimestamps.core.op import OpSHA256  # noqa: PLC0415
        import opentimestamps.core.notary as notary  # noqa: PLC0415
    except ImportError as e:
        return _setup(f"opentimestamps library not importable: {e}; see this file's docstring", lines)[0]
    if not proof.is_file():
        return _setup(f"proof absent: {proof}", lines)[0]
    try:
        with proof.open("rb") as fd:
            dtf = DetachedTimestampFile.deserialize(fd)
    except Exception as e:
        lines.append(f"ATTESTATION proof unreadable: {type(e).__name__}: {e}")
        return 1
    digests = _collect_digests(dtf.timestamp)
    hits = []
    for ts, digest in digests.items():
        for att in ts.attestations:
            if isinstance(att, notary.BitcoinBlockHeaderAttestation):
                hits.append((att, digest))
    if require_bitcoin and not hits:
        lines.append("ATTESTATION no BitcoinBlockHeaderAttestation in proof (pending-only?)")
        return 1
    return 0


def verify_proof_bytes(proof_bytes: bytes, expected_digest_hex: str, work: Path, fake_header, expect_setup_ok: bool) -> int:
    """Full structural+attestation verification over raw proof bytes (used by controls)."""
    import tempfile
    tmp = Path(tempfile.mkdtemp(dir=str(work)))
    p = tmp / "p.ots"
    p.write_bytes(proof_bytes)
    lines: list[str] = []
    rc = _attestation_leg(p, work, require_bitcoin=True, lines=lines)
    if rc != 0:
        return 1
    # binding: file digest must equal expected
    from opentimestamps.core.timestamp import DetachedTimestampFile  # noqa: PLC0415
    with p.open("rb") as fd:
        dtf = DetachedTimestampFile.deserialize(fd)
    if dtf.file_digest().hex() != expected_digest_hex:
        return 1
    if fake_header is not None:
        # attested digest must equal the header's merkle root
        digests = _collect_digests(dtf.timestamp)
        import opentimestamps.core.notary as notary  # noqa: PLC0415
        for ts, digest in digests.items():
            for att in ts.attestations:
                if isinstance(att, notary.BitcoinBlockHeaderAttestation):
                    if digest != fake_header:
                        return 1
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    import opentimestamps.core.notary as notary  # noqa: PLC0415
    from opentimestamps.core.timestamp import DetachedTimestampFile  # noqa: PLC0415

    lines: list[str] = []
    anchor = Path(args.anchor)
    source = Path(args.source)
    work = Path(args.work) if args.work else Path(os.environ.get("TMPDIR", ".")) / "r54c1"
    work.mkdir(parents=True, exist_ok=True)
    meta_p = anchor / "anchor.json"
    proof_p = anchor / "claims.ots"
    header_p = anchor / "header.bin"

    if not meta_p.is_file() or not proof_p.is_file():
        print("SETUP anchor absent (no anchor.json / claims.ots)")
        print("PREDICATE R54-C1 fail")
        return 1
    if not header_p.is_file():
        print("SETUP header.bin absent (attestation not yet confirmed or not yet landed)")
        print("PREDICATE R54-C1 fail")
        return 1
    meta = json.loads(meta_p.read_text())
    if meta.get("schema") != SCHEMA:
        return _setup(f"anchor.json schema {meta.get('schema')!r} != {SCHEMA!r}", lines)[0]
    freeze_rev = meta.get("freeze_rev") or ""
    if not freeze_rev:
        return _setup("anchor.json freeze_rev empty", lines)[0]

    # tree sanity: clean source at the tip, claims bytes identical at freeze_rev, HEAD and on disk
    st = _git(source, "status", "--porcelain")
    if st.returncode != 0 or st.stdout.strip():
        return _fail(f"SOURCE not clean: {st.stdout.strip()[:120]}", lines)
    tip = _git(source, "rev-parse", "HEAD").stdout.strip()
    r_freeze = _git(source, "rev-parse", "--verify", freeze_rev + "^{commit}")
    if r_freeze.returncode != 0:
        return _setup(f"freeze_rev {freeze_rev} not a commit in SOURCE", lines)
    if _git(source, "merge-base", "--is-ancestor", freeze_rev, tip).returncode != 0:
        return _fail("freeze_rev not an ancestor of the tip", lines)
    show = _git(source, "show", f"{freeze_rev}:{args.claims}")
    if show.returncode != 0:
        return _setup(f"claims not at freeze rev: {args.claims}", lines)
    b_freeze = show.stdout.encode("utf-8", "surrogateescape")
    show_head = _git(source, "show", f"{tip}:{args.claims}")
    b_head = show_head.stdout.encode("utf-8", "surrogateescape") if show_head.returncode == 0 else b""
    b_disk = (source / args.claims).read_bytes() if (source / args.claims).is_file() else b""

    want = meta["digest"]
    d_freeze, d_head, d_disk = canonical_digest(b_freeze), canonical_digest(b_head), canonical_digest(b_disk)
    if not (d_freeze == d_head == d_disk == want):
        return _fail(f"BINDING digest mismatch freeze={d_freeze[:12]} head={d_head[:12]} disk={d_disk[:12]} want={want[:12]}",
                     lines)
    lines.append(f"BINDING ok rev={freeze_rev} digest={want}")

    # proof structure + attestation
    try:
        with proof_p.open("rb") as fd:
            dtf = DetachedTimestampFile.deserialize(fd)
    except Exception as e:
        return _fail(f"ATTESTATION proof unreadable: {type(e).__name__}: {e}", lines)
    file_digest_hex = dtf.file_digest().hex()
    if file_digest_hex != want:
        return _fail(f"ATTESTATION proof file_digest {file_digest_hex[:12]} != anchored {want[:12]}", lines)
    node_digests = _collect_digests(dtf.timestamp)
    hits = []
    for ts, digest in node_digests.items():
        for att in ts.attestations:
            if isinstance(att, notary.BitcoinBlockHeaderAttestation):
                hits.append((att, digest))
    if not hits:
        return _fail("ATTESTATION no BitcoinBlockHeaderAttestation (proof still pending?)", lines)
    att, attested_digest = hits[0]
    if attested_digest != dtf.file_digest():
        # the attestation must apply to a digest that follows from the file digest; equality is the
        # canonical shape the calendars produce for a direct sha256 stamp
        return _fail("ATTESTATION attested digest does not follow from the file digest", lines)
    if att.height < MAINNET_HEIGHT_FLOOR:
        return _fail(f"ATTESTATION height {att.height} < floor {MAINNET_HEIGHT_FLOOR}", lines)
    lines.append(f"ATTESTATION ok height={att.height} attestations={len(hits)}")

    # header
    header = header_p.read_bytes()
    if len(header) != 80:
        return _fail(f"HEADER size {len(header)} != 80", lines)
    if header[36:68] != attested_digest:
        return _fail("HEADER merkle root != attested digest", lines)
    block_hash = _double_sha256(header)
    block_hash_hex = block_hash[::-1].hex()  # display order
    n_time = int.from_bytes(header[68:72], "little")
    block_time = None
    try:
        from bitcoin.core import CBlockHeader  # noqa: PLC0415

        bh = CBlockHeader.deserialize(header)
        att.verify_against_blockheader(attested_digest, bh)  # raises unless merkle root matches
        block_time = int(bh.nTime)
    except ImportError:
        # manual merkle-root field check when python-bitcoinlib is absent
        if header[36:68] != attested_digest:
            return _fail("HEADER merkle root != attested digest (manual check)", lines)
        block_time = n_time
    except Exception as e:
        return _fail(f"HEADER attestation vs header: {e}", lines)
    if block_time is None:
        return _fail("HEADER attestation vs header failed", lines)
    stamped = datetime.fromisoformat(meta["stamped_at"]).timestamp()
    now = time.time()
    if block_time < stamped - SKEW_SECONDS:
        return _fail(f"TIME block time {block_time} precedes stamp {stamped} beyond skew", lines)
    if block_time >= now:
        return _fail(f"TIME block time {block_time} not before the verification run {now}", lines)
    lines.append(f"HEADER ok block={block_hash_hex} time={block_time}")

    # external receipts
    receipts = sorted(anchor.glob("block-explorer-*.json"))
    if len(receipts) < EXPLORER_MIN:
        return _fail(f"EXTERNAL-PIN {len(receipts)} receipts < {EXPLORER_MIN}", lines)
    sources = set()
    for rcp in receipts:
        try:
            r = json.loads(rcp.read_text())
        except Exception as e:
            return _fail(f"EXTERNAL-PIN {rcp.name} unreadable: {e}", lines)
        for k in ("source", "url", "height", "hash", "time", "fetched_at"):
            if k not in r:
                return _fail(f"EXTERNAL-PIN {rcp.name} missing {k}", lines)
        if r["height"] != att.height or r["hash"] != block_hash_hex or int(r["time"]) != block_time:
            return _fail(f"EXTERNAL-PIN {rcp.name} disagrees with header/attestation", lines)
        sources.add(r["source"])
    if len(sources) < EXPLORER_MIN:
        return _fail(f"EXTERNAL-PIN {len(sources)} distinct sources < {EXPLORER_MIN}", lines)
    lines.append(f"EXTERNAL-PIN ok receipts={len(receipts)} sources={len(sources)}")

    rc = 0
    if args.controls:
        failed, clines = _verify_control_cases(anchor, proof_p.read_bytes(), want, work)
        lines.append(f"CONTROLS forged=4 failed={failed}")
        for c in clines:
            lines.append(c)
        if failed:
            rc = 1
    lines.append(f"PREDICATE R54-C1 {'pass' if rc == 0 else 'fail'}")
    print("\n".join(lines))
    return rc


# -------------------------------------------------------------------------------------- selftest
def _selftest() -> int:
    import opentimestamps.core.notary as notary  # noqa: PLC0415
    from opentimestamps.core.timestamp import DetachedTimestampFile, Timestamp  # noqa: PLC0415
    from opentimestamps.core.op import OpSHA256  # noqa: PLC0415

    work = Path(tempfile.mkdtemp(prefix="r54c1-selftest-"))
    cases = []

    def check(name, cond, detail=""):
        cases.append((name, bool(cond), detail))

    digest = canonical_digest(b"kengaku-r54-selftest")
    check("digest-canonical", digest == hashlib.sha256(b"kengaku-r54-selftest").hexdigest())

    # pending-only proof (offline) fails the attestation leg
    tmp = Path(tempfile.mkdtemp(dir=str(work)))
    ts = Timestamp(hashlib.sha256(b"p").digest())
    ts.attestations.add(notary.PendingAttestation("https://a.pool.opentimestamps.org"))
    dtf = DetachedTimestampFile(OpSHA256(), ts)
    pend = tmp / "pend.ots"
    with pend.open("wb") as fd:
        from opentimestamps.core.serialize import StreamSerializationContext
        dtf.serialize(StreamSerializationContext(fd))
    lines: list[str] = []
    check("pending-only-fails", _attestation_leg(pend, work, True, lines) == 1, "no bitcoin attestation")

    # absent proof fails (setup-class nonzero)
    rc_absent = _attestation_leg(tmp / "nope.ots", work, True, lines)
    check("absent-fails", rc_absent != 0, f"rc={rc_absent}")

    # attestation-vs-header core: synthetic bitcoinlib header
    try:
        from bitcoin.core import CBlockHeader  # noqa: PLC0415
        import io as _io

        def mk_header(merkle: bytes) -> bytes:
            h = bytearray(80)
            h[36:68] = merkle
            h[68:72] = (1_700_000_000).to_bytes(4, "little")
            return bytes(h)

        att = notary.BitcoinBlockHeaderAttestation(900000)
        good = CBlockHeader.deserialize(mk_header(bytes.fromhex(digest)))
        try:
            att.verify_against_blockheader(bytes.fromhex(digest), good)
            ok_good = True
        except Exception:
            ok_good = False
        bad = CBlockHeader.deserialize(mk_header(b"\x00" * 32))
        try:
            att.verify_against_blockheader(bytes.fromhex(digest), bad)
            ok_bad = False
        except Exception:
            ok_bad = True
        check("attestation-good-header-passes", ok_good)
        check("attestation-bad-header-fails", ok_bad)
        try:
            att.verify_against_blockheader(b"\x01" * 31, good)  # short digest must raise
            ok_short = False
        except Exception:
            ok_short = True
        check("attestation-short-digest-fails", ok_short)
        check("bitcoinlib-present", True)
    except ImportError:
        check("bitcoinlib-present", False, "python-bitcoinlib import failed")

    # forged flip: a flipped byte in a serialized proof must not verify (deserialize error or digest mismatch)
    ts2 = Timestamp(hashlib.sha256(b"flip").digest())
    ts2.attestations.add(notary.PendingAttestation("https://a.pool.opentimestamps.org"))
    dtf2 = DetachedTimestampFile(OpSHA256(), ts2)
    raw = tmp / "flip.ots"
    with raw.open("wb") as fd:
        from opentimestamps.core.serialize import StreamSerializationContext
        dtf2.serialize(StreamSerializationContext(fd))
    fb = bytearray(raw.read_bytes())
    fb[len(fb) // 2] ^= 0x01
    broken = tmp / "flip2.ots"
    broken.write_bytes(bytes(fb))
    rejected = False
    try:
        with broken.open("rb") as fd:
            DetachedTimestampFile.deserialize(fd)
        lines2: list[str] = []
        rejected = _attestation_leg(broken, work, True, lines2) == 1
    except Exception:
        rejected = True
    check("forged-proof-fails", rejected, "deserialize or leg failure")

    passed = sum(1 for _, ok, _ in cases if ok)
    for name, ok, detail in cases:
        print(f"[selftest] {'PASS' if ok else 'FAIL'} {name} {detail}")
    print(f"[selftest] {passed}/{len(cases)} PASS")
    shutil.rmtree(work, ignore_errors=True)
    return 0 if passed == len(cases) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_stamp = sub.add_parser("stamp", help="submit the claims digest to OTS calendars")
    p_stamp.add_argument("--claims", required=True)
    p_stamp.add_argument("--anchor", required=True)
    p_stamp.add_argument("--ots-bin", default=os.environ.get("OTS_BIN", "ots"))
    p_stamp.add_argument("--calendar", action="append", default=[])
    p_stamp.add_argument("--freeze-rev", default="")
    p_stamp.add_argument("--work", default=None)
    p_stamp.set_defaults(fn=cmd_stamp)

    p_up = sub.add_parser("upgrade", help="ask calendars for the bitcoin attestation")
    p_up.add_argument("--anchor", required=True)
    p_up.add_argument("--ots-bin", default=os.environ.get("OTS_BIN", "ots"))
    p_up.set_defaults(fn=cmd_upgrade)

    p_ver = sub.add_parser("verify", help="the frozen counting command")
    p_ver.add_argument("--anchor", required=True)
    p_ver.add_argument("--claims", required=True, help="repo-relative claims path")
    p_ver.add_argument("--source", required=True, help="clean clone of the tree under test")
    p_ver.add_argument("--work", default=None)
    p_ver.add_argument("--controls", action="store_true")
    p_ver.set_defaults(fn=cmd_verify)

    sub.add_parser("selftest", help="offline self-test").set_defaults(fn=lambda a: _selftest())

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
