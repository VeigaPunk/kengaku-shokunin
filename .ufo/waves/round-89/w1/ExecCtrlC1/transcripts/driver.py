#!/usr/bin/env python3
"""ExecCtrlC1 — R89-C1 control battery, scratch clones only (round 89 w1).

Controls:
  1 positive         counter at measured tip a9b8a1a -> expect rc 0, PREDICATE R89-C1 pass
  2 do-nothing       counter at base 192e809d       -> expect rc 1, PREDICATE R89-C1 fail (list DEFECTs)
  3 ledger-only      receipt removed, committed     -> expect DEFECT L1-receipt, rc 1
  4 forged-receipt   orphan empty commit HF; receipt LANE_TIP := HF; commit -> expect DEFECT L3-tip, rc 1
  4b (info)          claims-file variant: LANE_TIP := HF (non-ancestor) committed on the TIP lineage
  5 forged-probe     echo probe + receipt TOOL_SHA := sha(forged bytes), commit -> expect DEFECT L9-tool, rc 1
  5b (info)          same state, counter copy with the L9 mismatch branch disabled -> is L6 alone enough?

All fixture commits happen in scratch clones after asserting `git rev-parse --show-toplevel` equals
the clone. The production lane repo is never mutated; the lane's counter file is never edited (5b uses
a scratch copy).
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

SRC = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
S = Path("/fast/scratch/hyaku/kengaku-r89/ExecCtrlC1")
T = S / "transcripts"
T.mkdir(parents=True, exist_ok=True)
LANE, LANE2, LANE3 = S / "lane", S / "lane2", S / "lane3"
TIP = "a9b8a1a00b6a5ab5206be4d377dba439e02f8244"
BASE = "192e809d582ecbd544798cbc03da1666a0de23f7"
FREEZE = "d1c4f1b04bb39d18967075974b5984238b7c97f7"
PINNED_TOOL_SHA = "03c202f5072e8aa55636592fed9c2fb64b6a7684ec853f8968428e73d50df898"
COUNTER = "plans/round89_c1_replay.py"
RECEIPT = "corpus/evidence/round89/polyglot-rust-c-probe.txt"
PROBE = "plans/round89_polyglot_probe.py"
IDENT = ["-c", "user.name=seat", "-c", "user.email=seat@scratch"]


def sh(*args, cwd=None, timeout=300):
    return subprocess.run(list(args), cwd=cwd, capture_output=True, text=True, timeout=timeout)


def git(lane, *args, timeout=300):
    return sh("git", "-C", str(lane), *args, cwd=None, timeout=timeout)


def log(name, text):
    (T / name).write_text(text if text.endswith("\n") else text + "\n")
    print(f"[log] {name} written", flush=True)


def require_toplevel(lane):
    p = git(lane, "rev-parse", "--show-toplevel")
    ok = p.returncode == 0 and Path(p.stdout.strip()).resolve() == Path(lane).resolve()
    assert ok, f"toplevel guard failed for {lane}: rc={p.returncode} out={p.stdout!r} err={p.stderr!r}"
    return p.stdout.strip()


def commit(lane, message, paths=()):
    require_toplevel(lane)
    if paths:
        p = git(lane, "add", "-A", "--", *paths)
        assert p.returncode == 0, f"git add failed: {p.stderr}"
    p = git(lane, *IDENT, "commit", "-q", "--allow-empty" if not paths else "--allow-empty",
            "-m", message)
    assert p.returncode == 0, f"git commit failed in {lane}: {p.stdout} {p.stderr}"
    return git(lane, "rev-parse", "HEAD").stdout.strip()


def run_counter(name, counter_path, lane, rev, work):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(counter_path), "--lane", str(lane), "--rev", rev, "--work", str(work)]
    header = f"$ " + " ".join(cmd) + "\n"
    try:
        p = sh(*cmd, timeout=1500)
        body = header + "--- stdout ---\n" + p.stdout
        if p.stderr:
            body += "--- stderr ---\n" + p.stderr
        body += f"--- rc ---\n{p.returncode}\n"
    except subprocess.TimeoutExpired as e:
        body = header + f"TIMEOUT after 1500s: {e}\n--- rc ---\nN/A\n"
        p = None
    log(name, body)
    return p


def blob_sha(lane, rev, path):
    p = git(lane, "show", f"{rev}:{path}")
    return hashlib.sha256(p.stdout.encode("utf-8", errors="surrogateescape")).hexdigest() if p.returncode == 0 else None


def main():
    # ---------- 00 environment ----------
    env = []
    env.append(f"lane clone HEAD: {git(LANE, 'rev-parse', 'HEAD').stdout.strip()}")
    env.append(f"clone status --porcelain lines: {len(git(LANE, 'status', '--porcelain').stdout.splitlines())}")
    for label, h, d in [("FREEZE", FREEZE, TIP), ("TIP", TIP, None), ("BASE", BASE, None),
                        ("instruments 0e6bb05", "0e6bb05f3a6c2d9a96bb26db31a4fd39f58c2619", None),
                        ("fixes 000b7d1", "000b7d1cdbbadb8086f6bb41149c3d32744105ad", None)]:
        t = git(LANE, "cat-file", "-t", h)
        env.append(f"{label} {h[:12]} type={t.stdout.strip() or t.stderr.strip()}")
    for q, a in [("FREEZE ancestor of TIP", (FREEZE, TIP)), ("TIP ancestor of clone HEAD", (TIP, "HEAD"))]:
        r = git(LANE, "merge-base", "--is-ancestor", q.split()[0] == "FREEZE" and FREEZE or TIP, a[1])
        env.append(f"{q}: rc={r.returncode} (0=yes)")
    for path in (COUNTER, PROBE, RECEIPT, "plans/round89-cases.json",
                 "corpus/evidence/round52/graders/polyglot-rust-c/tests/test_outputs.py"):
        env.append(f"sha256@TIP {path} = {blob_sha(LANE, TIP, path)}")
    d = git(LANE, "diff", "--stat", f"{TIP}..HEAD", "--", COUNTER, PROBE, RECEIPT,
            "plans/round89-cases.json", "plans/grader-population-ledger.json")
    env.append("diff TIP..cloneHEAD on involved paths:\n" + (d.stdout or "(empty)"))
    for c in (["python3", "-V"], ["rustc", "-V"], ["g++", "-dumpfullversion", "-dumpversion"],
              ["bwrap", "--version"]):
        r = sh(*c)
        env.append(f"{c[0]}: {r.stdout.strip() or r.stderr.strip()}")
    log("00-env.txt", "\n".join(env) + "\n")

    # point the primary clone at the measured tip (scratch clone, detached checkout)
    p = git(LANE, "checkout", "-q", TIP)
    assert p.returncode == 0, f"checkout TIP failed: {p.stderr}"
    head = git(LANE, "rev-parse", "HEAD").stdout.strip()
    assert head == TIP, f"HEAD {head} != TIP"
    counter_bytes = (LANE / COUNTER).read_bytes()
    log("00b-counter-bytes.txt",
        f"counter bytes used for every invocation: {COUNTER} @ {TIP}\n"
        f"sha256 = {hashlib.sha256(counter_bytes).hexdigest()}\n"
        f"TRUSTED_TOOL_SHA constant in counter = {PINNED_TOOL_SHA}\n")

    # ---------- control 1: positive at measured tip ----------
    run_counter("01-control1-positive.txt", LANE / COUNTER, LANE, TIP, S / "w0")

    # ---------- control 2: do-nothing at BASE ----------
    run_counter("02-control2-donothing.txt", LANE / COUNTER, LANE, BASE, S / "w1")

    # ---------- control 3: ledger-only (receipt removed) in lane ----------
    require_toplevel(LANE)
    (LANE / RECEIPT).unlink()
    h3 = commit(LANE, "control 3: remove probe receipt (ledger row left intact)", [RECEIPT])
    parents = git(LANE, "log", "--format=%H %P", "-3").stdout
    log("03-control3-ledger-only.git.txt",
        f"base: {TIP}\nH3 (receipt removed): {h3}\nlast 3 commits (hash parents):\n{parents}")
    run_counter("03-control3-ledger-only.txt", LANE / COUNTER, LANE, h3, S / "w2")

    # ---------- control 4: forged-receipt (seat recipe: orphan empty commit, LANE_TIP := HF) ----------
    p = sh("git", "clone", "--no-hardlinks", SRC, str(LANE2))
    assert p.returncode == 0, f"clone lane2 failed: {p.stderr}"
    assert git(LANE2, "checkout", "-q", TIP).returncode == 0
    require_toplevel(LANE2)
    assert git(LANE2, "checkout", "-q", "--orphan", "forge").returncode == 0
    hf = commit(LANE2, "control 4: empty orphan root commit (forge)")
    receipt_text = (LANE2 / RECEIPT).read_text()
    assert f"LANE_TIP {FREEZE}" in receipt_text
    (LANE2 / RECEIPT).write_text(re.sub(r"^LANE_TIP .*$", f"LANE_TIP {hf}", receipt_text, flags=re.M))
    h4 = commit(LANE2, "control 4: receipt LANE_TIP replaced by the empty orphan commit", [RECEIPT])
    h4_parents = git(LANE2, "log", "--format=%H %P", "-2").stdout
    anc = git(LANE2, "merge-base", "--is-ancestor", hf, h4)
    log("04-control4-forged-receipt.git.txt",
        f"HF (empty orphan root): {hf}\nH4 (receipt LANE_TIP:=HF): {h4}\n"
        f"last 2 commits:\n{h4_parents}"
        f"is-ancestor HF of H4: rc={anc.returncode} (0=yes)\n"
        "receipt diff:\n" + git(LANE2, "diff", f"{hf}..{h4}", "--", RECEIPT).stdout)
    run_counter("04-control4-forged-receipt.txt", LANE2 / COUNTER, LANE2, h4, S / "w3")

    # ---------- control 4b (info): claims-file variant — LANE_TIP := commit NOT an ancestor ----------
    # same forged receipt content, but committed on the TIP lineage so HF stays unrelated
    assert git(LANE2, "checkout", "-q", "-B", "orig", TIP).returncode == 0
    (LANE2 / RECEIPT).write_text(re.sub(r"^LANE_TIP .*$", f"LANE_TIP {hf}", (LANE2 / RECEIPT).read_text(), flags=re.M))
    h4b = commit(LANE2, "control 4b: receipt LANE_TIP:=HF committed on the TIP lineage (HF not an ancestor)", [RECEIPT])
    anc_b = git(LANE2, "merge-base", "--is-ancestor", hf, h4b)
    log("04b-control4b-forged-receipt.git.txt",
        f"H4b (parent = {TIP[:12]}): {h4b}\nLANE_TIP forged to: {hf}\n"
        f"is-ancestor HF of H4b: rc={anc_b.returncode} (0=no, expected for claims-file variant)\n"
        "last 2 commits:\n" + git(LANE2, "log", "--format=%H %P", "-2").stdout)
    run_counter("04b-control4b-forged-receipt.txt", LANE2 / COUNTER, LANE2, h4b, S / "w3b")

    # ---------- control 5: forged-probe (Sentinel F1 echo probe + regenerated TOOL_SHA) ----------
    p = sh("git", "clone", "--no-hardlinks", SRC, str(LANE3))
    assert p.returncode == 0, f"clone lane3 failed: {p.stderr}"
    assert git(LANE3, "checkout", "-q", TIP).returncode == 0
    require_toplevel(LANE3)
    receipt_lines = (LANE3 / RECEIPT).read_text().splitlines()
    b, e = receipt_lines.index("OBSERVATIONS_BEGIN"), receipt_lines.index("OBSERVATIONS_END")
    forged_block = []
    for ln in receipt_lines[b + 1:e]:
        m = re.match(r"^CASE (\S+) predicted=(\S+) observed=(\S+)$", ln)
        forged_block.append(f"CASE {m.group(1)} predicted={m.group(2)} observed={m.group(2)}" if m else ln)
    body = "".join(f"    {ln!r},\n" for ln in forged_block)
    forged_probe = (
        "#!/usr/bin/env python3\n"
        '"""FORGED probe (ExecCtrlC1 control 5 fixture): echoes the receipt observation block with\n'
        "observed == predicted. No grader call, no lane read. Round-88 Sentinel F1 shape.\"\"\"\n"
        "BLOCK = [\n" + body + "]\n"
        'print("OBSERVATIONS_BEGIN")\n'
        "for line in BLOCK:\n"
        "    print(line)\n"
        'print("OBSERVATIONS_END")\n'
    )
    (LANE3 / PROBE).write_bytes(forged_probe.encode())
    forged_sha = hashlib.sha256(forged_probe.encode()).hexdigest()
    assert forged_sha != PINNED_TOOL_SHA
    new_receipt = re.sub(r"^TOOL_SHA .*$", f"TOOL_SHA {forged_sha}", "\n".join(receipt_lines), flags=re.M) + "\n"
    (LANE3 / RECEIPT).write_text(new_receipt)
    h5 = commit(LANE3, "control 5: forged echo probe + receipt TOOL_SHA regenerated from forged bytes",
                [PROBE, RECEIPT])
    shutil_sha_probe_at_tip = blob_sha(LANE3, TIP, PROBE)
    log("05-control5-forged-probe.git.txt",
        f"H5 (forged probe + receipt): {h5}\n"
        f"last 2 commits:\n" + git(LANE3, "log", "--format=%H %P", "-2").stdout +
        f"probe sha256 @TIP (trusted) = {shutil_sha_probe_at_tip}\n"
        f"probe sha256 forged        = {forged_sha}\n"
        f"TRUSTED_TOOL_SHA (counter constant) = {PINNED_TOOL_SHA}\n"
        "receipt stamp diff (TIP -> H5):\n" +
        git(LANE3, "diff", f"{TIP}..{h5}", "--", RECEIPT).stdout +
        "--- forged probe bytes ---\n" + forged_probe)
    # keep a copy of the forged probe as evidence
    (T / "05-forged-probe.py").write_text(forged_probe)
    run_counter("05-control5-forged-probe.txt", LANE3 / COUNTER, LANE3, h5, S / "w4")

    # ---------- control 5b (info): same forged state, L9 mismatch branch disabled in a scratch copy ----------
    counter_text = counter_bytes.decode()
    target = "elif sha256(tool) != TRUSTED_TOOL_SHA:"
    assert counter_text.count(target) == 1, f"L9 elif occurrences = {counter_text.count(target)}"
    nol9_text = counter_text.replace(target, "elif False:  # ExecCtrlC1 control 5b: L9 mismatch branch disabled")
    nol9_path = S / "c1_replay_noL9.py"
    nol9_path.write_text(nol9_text)
    log("06-control5b-nol9.copy.txt",
        f"scratch counter copy: {nol9_path}\n"
        f"sha256 = {hashlib.sha256(nol9_path.read_bytes()).hexdigest()}\n"
        f"edit: replaced 1 occurrence of: {target}\n"
        "lane counter NOT modified (production file untouched; copy lives in scratch only)\n")
    run_counter("06-control5b-nol9.txt", nol9_path, LANE3, h5, S / "w5b")

    print("DRIVER DONE", flush=True)


if __name__ == "__main__":
    main()
