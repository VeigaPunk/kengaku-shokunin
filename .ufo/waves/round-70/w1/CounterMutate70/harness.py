#!/usr/bin/env python3
"""R70-C1 mutation probe v2: prove each --check-receipt check is load-bearing.

Isolation rules:
  * every mutant is a byte copy of the frozen instrument with exactly one check
    neutralised, committed in its own throwaway git repo so `probe_blob_sha`
    returns a real blob sha instead of the "absent" escape hatch;
  * every receipt is regenerated against the lane under test, so PROBE and
    PROBE_BLOB always name that lane's own bytes (otherwise probe-sha fires
    first and every mutant looks "killed" for the wrong reason);
  * one targeted stimulus per check, and the pristine instrument must refuse it.

leg-coverage is measured in-process: through the CLI its stimulus is
unreachable (see report).
"""

import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import shutil
import subprocess
import sys
import traceback

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r70/CounterMutate70")
L = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE_REL = "plans/round70_c1_nginx_probe.py"
GRADER_REL = ("corpus/evidence/round52/graders/nginx-request-logging/"
              "tests/test_outputs.py")
ZERO = "0" * 64
TRANSCRIPT = []


def say(*parts):
    line = " ".join(str(p) for p in parts)
    print(line)
    TRANSCRIPT.append(line)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    return sha_bytes(pathlib.Path(p).read_bytes())


def run(argv, **kw):
    say("$", " ".join(str(a) for a in argv))
    r = subprocess.run([str(a) for a in argv], capture_output=True, text=True, **kw)
    say(f"  rc={r.returncode}")
    for ln in (r.stdout or "").splitlines():
        say("  |", ln)
    for ln in (r.stderr or "").splitlines():
        say("  !", ln)
    return r


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PRISTINE_BYTES = (L / PROBE_REL).read_bytes()
PRISTINE_SHA = sha_bytes(PRISTINE_BYTES)
FROZEN = load_module(L / PROBE_REL, "r70_c1_frozen")
CASES, CASE_SHA, LEGS = FROZEN.CASES, dict(FROZEN.CASE_SHA), FROZEN.LEGS
GRADER_BYTES = (L / GRADER_REL).read_bytes()


def make_lane(root, probe_bytes):
    root = pathlib.Path(root)
    if root.exists():
        shutil.rmtree(root)
    (root / "plans").mkdir(parents=True)
    (root / GRADER_REL).parent.mkdir(parents=True)
    (root / PROBE_REL).write_bytes(probe_bytes)
    (root / GRADER_REL).write_bytes(GRADER_BYTES)
    return root


def commit_lane(root):
    root = pathlib.Path(root)
    run(["git", "-C", root, "init", "-q", "-b", "master"])
    top = run(["git", "-C", root, "rev-parse", "--show-toplevel"])
    assert top.stdout.strip() == str(root), (top.stdout, root)
    ident = ["-c", "user.name=R70-CounterMutate70",
             "-c", "user.email=r70@countermutate.invalid", "-c", "commit.gpgsign=false"]
    run(["git", "-C", root] + ident + ["add", "-A"])
    run(["git", "-C", root] + ident + ["commit", "-q", "-m", "mutation probe fixture"])
    return root


def live_blob_for(root):
    r = subprocess.run(["git", "-C", str(root), "cat-file", "blob",
                        f"master:{PROBE_REL}"], capture_output=True)
    assert r.returncode == 0, "blob arm dead: probe not committed"
    return sha_bytes(r.stdout)


def base_lines(probe_sha, blob_sha):
    return [
        f"PROBE {PROBE_REL} sha256 {probe_sha}",
        f"PROBE_BLOB {PROBE_REL} sha256 {blob_sha}",
        f"PROBE_VERSION {FROZEN.PROBE_VERSION}",
        f"GRADER {GRADER_REL} sha256 {FROZEN.GRADER_SHA256} pin {FROZEN.TB2_PIN}",
        f"PORT {FROZEN.PORT} free-at-start=True",
    ]


def table_lines(cases, sha_map):
    out = []
    for case in cases:
        cid, vec = case["id"], case["expected"]
        out.append(f"CASE {cid} case_sha256={sha_map.get(cid, ZERO)} "
                   f"server_pid=4242 sandbox_rc=0")
        for i, name in enumerate(LEGS):
            out.append(f"TEST {cid} {name} {vec[i]}")
        out.append(f"VECTOR {cid} {vec} expected {vec} agree=True")
    out.append(f"SUMMARY cases={len(cases)} legs={len(cases) * len(LEGS)} "
               f"mismatches=0 setup=0")
    out.append("PREDICATE R70-C1 pass")
    return out


def good_receipt(probe_sha, blob_sha, cases=None, sha_map=None):
    cases = CASES if cases is None else cases
    sha_map = CASE_SHA if sha_map is None else sha_map
    return "\n".join(base_lines(probe_sha, blob_sha) + table_lines(cases, sha_map)) + "\n"


def apply_line(text, needle, replacement):
    lines = text.splitlines()
    hits = [i for i, ln in enumerate(lines) if needle in ln]
    assert len(hits) == 1, (needle, hits)
    lines[hits[0]] = replacement
    return "\n".join(lines) + "\n"


BAD_RECEIPT = {
    "case-sha": lambda t: apply_line(
        t, "CASE K1 case_sha256=",
        f"CASE K1 case_sha256={ZERO} server_pid=4242 sandbox_rc=0"),
    "probe-blob": lambda t: apply_line(
        t, "PROBE_BLOB ", f"PROBE_BLOB {PROBE_REL} sha256 {ZERO}"),
    "vector-agreement": lambda t: apply_line(
        t, "VECTOR K3 ", "VECTOR K3 PPPPPPFF expected PPPPPPFF agree=False"),
    "case-set": lambda t: t.replace(
        "SUMMARY cases=7", "VECTOR K8 FFFFFFFF expected FFFFFFFF agree=True\n"
                           "SUMMARY cases=7"),
}

MUTANTS = {
    "leg-coverage": (
        "    for name in LEGS:\n"
        "        if seen_p[name] == 0 or seen_f[name] == 0:\n"
        "            defect(\"leg-coverage\", f\"{name} p={seen_p[name]} f={seen_f[name]}\")\n",
        "    for name in LEGS:\n"
        "        if False:  # MUTANT leg-coverage neutralised\n"
        "            defect(\"leg-coverage\", f\"{name} p={seen_p[name]} f={seen_f[name]}\")\n",
    ),
    "case-sha": (
        "        elif got_sha != want_sha:\n"
        "            defect(\"case-sha\", f\"{cid} {got_sha} != {want_sha}\")\n",
        "        elif False:  # MUTANT case-sha comparison neutralised\n"
        "            pass\n",
    ),
    "probe-blob": (
        "            if got_blob != live_blob:\n"
        "                defect(\"probe-blob\", f\"{got_blob} != {live_blob}\")\n"
        "            if got_blob != own_sha256():\n"
        "                defect(\"probe-blob-working-tree\", f\"{got_blob} != {own_sha256()}\")\n",
        "            if False:  # MUTANT probe-blob binding neutralised\n"
        "                defect(\"probe-blob\", f\"{got_blob} != {live_blob}\")\n"
        "            if False:  # MUTANT probe-blob working-tree binding neutralised\n"
        "                defect(\"probe-blob-working-tree\", f\"{got_blob} != {own_sha256()}\")\n",
    ),
    "grader-file": (
        "    grader_file = lane_root() / GRADER_REL\n"
        "    if not grader_file.is_file():\n"
        "        defect(\"grader-file\", f\"{GRADER_REL} missing\")\n"
        "    else:\n"
        "        live = sha256_file(grader_file)\n"
        "        if live != GRADER_SHA256:\n"
        "            defect(\"grader-file-sha\", live)\n",
        "    if False:  # MUTANT grader-file rehash neutralised\n"
        "        pass\n",
    ),
    "vector-agreement": (
        "            if parts[4] != parts[2]:\n"
        "                defect(\"vector-expected-field\", ln)\n",
        "            if False:  # MUTANT vector/expected field agreement neutralised\n"
        "                defect(\"vector-expected-field\", ln)\n",
    ),
    "case-set": (
        "    if sorted(vectors) != sorted(expected_ids):\n"
        "        defect(\"case-set\", f\"got={sorted(vectors)} want={sorted(expected_ids)}\")\n",
        "    if False:  # MUTANT case-set comparison neutralised\n"
        "        defect(\"case-set\", f\"got={sorted(vectors)} want={sorted(expected_ids)}\")\n",
    ),
}

VECTOR_AGREE_EXTRA = (
    "        if stored_agree != \"True\":\n"
    "            defect(\"vector-agree\", f\"{cid} agree={stored_agree}\")\n",
    "        if False:  # MUTANT stored agree= flag neutralised\n"
    "            defect(\"vector-agree\", f\"{cid} agree={stored_agree}\")\n",
)


def mutate(src_bytes, name):
    text = src_bytes.decode()
    pats = [MUTANTS[name]]
    if name == "vector-agreement":
        pats.append(VECTOR_AGREE_EXTRA)
    for old, new in pats:
        n = text.count(old)
        assert n == 1, f"{name}: anchor count={n} for {old.splitlines()[0]!r}"
        text = text.replace(old, new)
    return text.encode()


def cli(lane, receipt):
    r = subprocess.run([sys.executable, str(lane / PROBE_REL),
                        "--check-receipt", str(receipt)],
                       capture_output=True, text=True)
    return r.returncode, [ln for ln in r.stdout.splitlines() if ln.startswith("DEFECT")]


def inproc(lane, receipt, cases, sha_map):
    mod = load_module(lane / PROBE_REL, "probe_" + sha_bytes(str(lane).encode())[:12])
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = mod.check_receipt(pathlib.Path(receipt), cases=cases, case_sha=sha_map)
    return rc, [ln for ln in buf.getvalue().splitlines() if ln.startswith("DEFECT")]


def main():
    say("== R70-C1 check mutation probe (v2) ==")
    say("pristine probe", PROBE_REL, "sha256", PRISTINE_SHA)
    say("frozen CASES", "/".join(c["expected"] for c in CASES))
    say("frozen CASE_SHA distinct", len(set(CASE_SHA.values())), "of", len(CASE_SHA))

    base = commit_lane(make_lane(S / "lane-baseline", PRISTINE_BYTES))
    say("baseline lane", base, "probe sha", sha_file(base / PROBE_REL),
        "blob", live_blob_for(base))
    good_text = good_receipt(sha_file(base / PROBE_REL), live_blob_for(base))
    gp = S / "receipts" / "baseline.txt"
    gp.parent.mkdir(parents=True, exist_ok=True)
    gp.write_text(good_text, encoding="utf-8")
    say("wrote", gp, "sha256", sha_file(gp))
    r = run([sys.executable, base / PROBE_REL, "--check-receipt", gp])
    if r.returncode != 0:
        say("!! baseline refuse: instrument cannot accept its own frozen table")
        return 2
    say("BASELINE accept rc=0 accepted=True")

    (S / "selftest-work").mkdir(parents=True, exist_ok=True)
    st = run([sys.executable, base / PROBE_REL, "--selftest", "--work",
              S / "selftest-work"])
    say(f"SELFTEST rc={st.returncode}")

    # ---- targeted stimuli, measured on the pristine instrument first
    grader_bad = bytearray(GRADER_BYTES)
    grader_bad[-2] ^= 0x01
    grader_bad = bytes(grader_bad)
    say("bad grader sha256", sha_bytes(grader_bad), "(frozen", FROZEN.GRADER_SHA256 + ")")

    synth = ({"id": "S1", "expected": "P" * 8}, {"id": "S2", "expected": "P" * 8})
    synth_sha = {"S1": "1" * 64, "S2": "2" * 64}

    pristine_bad = {}
    for name, fn in BAD_RECEIPT.items():
        p = S / "receipts" / f"pristine-bad-{name}.txt"
        p.write_text(fn(good_text), encoding="utf-8")
        pristine_bad[name] = cli(base, p)
    # leg-coverage: custom table, in-process (CLI cannot carry a foreign table)
    sp = S / "receipts" / "pristine-bad-leg-coverage.txt"
    sp.write_text(good_receipt(sha_file(base / PROBE_REL), live_blob_for(base),
                               cases=synth, sha_map=synth_sha), encoding="utf-8")
    pristine_bad["leg-coverage"] = inproc(base, sp, synth, synth_sha)
    # grader-file: environment stimulus, restore after
    gpath = base / GRADER_REL
    keep = gpath.read_bytes()
    gpath.write_bytes(grader_bad)
    pristine_bad["grader-file"] = cli(base, gp)
    gpath.write_bytes(keep)
    assert sha_file(gpath) == FROZEN.GRADER_SHA256, "grader not restored"
    say("pristine grader restored:", sha_file(gpath))

    for name, (rc, defs) in pristine_bad.items():
        say(f"PRISTINE-BAD {name} rc={rc} defects={len(defs)}",
            *[f"[{d}]" for d in defs[:2]])

    say("== mutant matrix ==")
    results = []
    for name in MUTANTS:
        root = commit_lane(make_lane(S / "mut" / name, mutate(PRISTINE_BYTES, name)))
        msha, mblob = sha_file(root / PROBE_REL), live_blob_for(root)
        say(f"-- mutant {name}: probe sha {msha} blob {mblob}")
        assert msha == mblob, "mutant working tree != its blob"
        mg = S / "receipts" / f"good-{name}.txt"
        mg_text = good_receipt(msha, mblob)
        mg.write_text(mg_text, encoding="utf-8")
        rc_good, defs_good = cli(root, mg)
        say(f"MUTANT {name} good rc={rc_good} defects={len(defs_good)}")
        for d in defs_good:
            say("   ", d)

        if name == "leg-coverage":
            mp = S / "receipts" / f"mutant-bad-{name}.txt"
            mp.write_text(good_receipt(msha, mblob, cases=synth, sha_map=synth_sha),
                          encoding="utf-8")
            rc_bad, defs_bad = inproc(root, mp, synth, synth_sha)
        elif name == "grader-file":
            g2 = root / GRADER_REL
            gkeep = g2.read_bytes()
            g2.write_bytes(grader_bad)
            rc_bad, defs_bad = cli(root, mg)
            g2.write_bytes(gkeep)
            assert sha_file(g2) == FROZEN.GRADER_SHA256
        else:
            bp = S / "receipts" / f"mutant-bad-{name}.txt"
            bp.write_text(BAD_RECEIPT[name](mg_text), encoding="utf-8")
            rc_bad, defs_bad = cli(root, bp)
        say(f"MUTANT {name} bad rc={rc_bad} defects={len(defs_bad)}")
        for d in defs_bad[:5]:
            say("   ", d)

        prc, pdefs = pristine_bad[name]
        killed = (rc_good == 0 and prc != 0 and rc_bad == 0)
        results.append({
            "check": name, "killed": killed, "rc_good": rc_good, "rc_bad": rc_bad,
            "pristine_bad_rc": prc, "defects_good": defs_good,
            "defects_bad": defs_bad, "pristine_defects": pdefs,
            "probe_sha": msha,
        })
        say(f"MUTANT {name} killed={killed} rc_good={rc_good} rc_bad={rc_bad} "
            f"pristine_bad_rc={prc}")

    say("== summary ==")
    for r in results:
        say(f"RESULT {r['check']:<18} killed={str(r['killed']):<5} "
            f"rc_good={r['rc_good']} rc_bad={r['rc_bad']} "
            f"pristine_bad_rc={r['pristine_bad_rc']}")

    after = sha_file(L / PROBE_REL)
    say("L probe sha256 after:", after, "unchanged=", after == PRISTINE_SHA)
    say("L probe git status:", subprocess.run(
        ["git", "-C", str(L), "status", "--porcelain", PROBE_REL],
        capture_output=True, text=True).stdout.strip() or "(clean)")

    (S / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    (S / "transcript.txt").write_text("\n".join(TRANSCRIPT) + "\n", encoding="utf-8")
    return 0 if all(r["killed"] for r in results) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        (S / "transcript.txt").write_text("\n".join(TRANSCRIPT) + "\n", encoding="utf-8")
        raise
