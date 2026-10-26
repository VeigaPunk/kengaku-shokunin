#!/usr/bin/env python3
"""Round-44 C2 counter (coverage): the pinned Terminal-Bench 2.0 `feal-linear-cryptanalysis` grader admitted as a
knowledge package with an executed offline probe (a tenth grader class, the round-43 class histogram's largest
uncovered one, F1 constant-compare: the graded artefact is an agent-written TEXT FILE that the grader checks with a
substring test of 100 expected constants embedded in the test file; the verdict is the pytest exit status
tests/test.sh rewards).

Frozen predicate (same sentence in plans/round-44-claims.md and in the receipt label):
  C2 passes iff `python3 plans/round44_c2_verify.py --lane .` prints `checks=11 defects=0`, then
  `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.

Every input this counter reads that exists at the freeze is pinned here by digest: the spec template, the gate,
the probe, the frozen dry table and the eleven captures. V1-V10 are the round-43 counter's
(`plans/round43_c2_verify.py`), re-pointed at the round-44 package; no V1-V10 check is relaxed. V11 is new
(round-43 closure R5 / SCORECARD `### Planned (round 44)` "C2 counter content leg": V10's DECISIVE map is readable
in the counter, so a copycat filler passes V10 — `R43CritClaims` §1).

  V1 capture manifest: corpus/evidence/round44/tb2-feal-linear-cryptanalysis/SHA256SUMS lists exactly the eleven
     captured files at their frozen digests and every file's bytes match.
  V2 package gate: plans/pkg-spec-r44.json and plans/pkg_gate.py at their freeze digests;
     `pkg_gate.py package --rerun --require-clean-tree` accepts the package (P10 = fresh probe run byte-compared).
  V3 anchor digests: each spec row has one 11-cell registry row whose anchor carries exactly its own `sha256` pin.
  V4 receipt: CASE ids equal the frozen case table in order; one consistent summary line; every `match=NO` case id
     named in the entry.
  V5 frozen probe: plans/feal_linear_probe.py at its freeze digest and its `--dry` output byte-equal to
     corpus/evidence/round44/feal-linear-dry-cases-freeze.txt (itself at its freeze digest).
  V6 census: `scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md` exits 0.
  V7 requirement map: one `## Requirement map` row per frozen tag, label DERIVED from the receipt.
  V8 order (QUALITY Q30): `plans/order_check.py --lane <lane> --claims plans/round-44-claims.md --receipt
     <spec receipt>` exits 0 and prints `ORDER RESULT PASS`.
  V9 content consistency: `## Case table` equal to the receipt; every spec row id outside the `source:` line;
     PROVINCE.md names `feal-linear-cryptanalysis` and the entry file on one line; README `## Frontier` names it.
  V10 mechanism: `## Mechanism` rows per receipt case citing a frozen DECISIVE line with a >=2-word verbatim quote.
  V11 held-out predictor (new; the key is not in this file): the entry's `## Predictor` section holds exactly one
     fenced ```python block defining `predict(text)` -> bool (`text` is the full content of /app/plaintexts.txt, or
     None when the file is absent; True = the grader passes that end state). The counter builds STATES (48 end
     states, `random.Random(44)`, from the 100 constants of the pinned capture plus decoys and format changes),
     runs the CAPTURED grader's `test_attack` on each inside a bubblewrap sandbox (no network, /app a scratch dir,
     only plaintexts.txt varies), runs `predict` on each in a second sandbox, and requires: 0 disagreements, and at
     least 8 grader passes and 8 grader fails among the states (non-vacuity). The verdicts are never stored here:
     they exist only by executing the grader, so a filler cannot copy them from the counter (it can only read the
     grader, which is the content asked for). Freeze controls `claims/control-c2-predictor.txt`: always-True ->
     V11 DEFECT; a whitespace-token-set reading -> V11 DEFECT; an exact-line reading -> V11 DEFECT; the substring
     reading -> V11 ok.

`--work DIR` is created if absent before the scratch directory is made inside it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import tempfile

CAP = "corpus/evidence/round44/tb2-feal-linear-cryptanalysis"
CAPTURES = {
    "Dockerfile": "ef521cded1b5e0e9a11a6aa9c758e4474f2160e641fb9a177a20cdc728bfff1d",
    "README.md": "a038645f908b4e011e9c5526b73aaa826057287a4cf3237b205f4e38f6d3dc33",
    "decrypt.c": "4c6864e0d3a76626f1a7af1383e6826a85bdd1e7e373215741ece4f50a94ebd2",
    "feal.c": "bbd38d19f976b27e5a5aff23e21ba5f0164335397928ca05220379552dea08da",
    "gen.py": "3a71f0b5d9095440bea31bced5ea4fc8dd4cff0ae4226ea0400a3bfa7c452c63",
    "gitignore": "9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953",
    "instruction.md": "a2f1669d4067af6c7b8ac05ff7d5849ca5df68397c94701645c4b9a3b6f71b03",
    "solve.sh": "be50ae01a3ea850a6dc4bc99dc130d0b7ad37963c85544a02b03a4f5da29cb77",
    "task.toml": "a39ec2c427af534c96c719dc87f70eb536956b487ce909d04b6365160e7c9fc4",
    "test.sh": "9431cbc2bad2b690001e096218ecd3f7f2f241b415062a2ea1ec7083d2e7c9e1",
    "test_outputs.py": "f59ebc7218a648582483cee02556c3bc1235e186301376bc3be066ed106ed9f9",
}
SPEC_REL = "plans/pkg-spec-r44.json"
SPEC_SHA256 = "1f31cf40a33325e02f986d709171ea48b2d131cf73641c0fd2e81b7709bbe4b8"
GATE_REL = "plans/pkg_gate.py"
GATE_SHA256 = "ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41"
PROBE_REL = "plans/feal_linear_probe.py"
PROBE_SHA256 = "0e7a59dab76266a167d9c3f51dd01817f7cec2f62896689bc488947dce545297"
DRY_REL = "corpus/evidence/round44/feal-linear-dry-cases-freeze.txt"
DRY_SHA256 = "07f1d0dfc10900c5a159e8c7b47688703d066a8641c5aed83fa266a1c1d2109a"
ORDER_REL = "plans/order_check.py"
CLAIMS_REL = "plans/round-44-claims.md"
TASK = "feal-linear-cryptanalysis"
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
SOURCE_ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SUMMARY = re.compile(r"^cases=(\d+) observed_pass=(\d+) observed_fail=(\d+) mismatches=(\d+)$")
MAP_ROW = re.compile(r"^\|\s*`instruction\.md:(\d+)`\s*\|\s*`([a-z0-9-]+)`\s*\|\s*(enforced|unenforced|partly)\s*\|(.*)\|\s*$")
CASE_ROW = re.compile(r"^\|\s*`([a-z0-9_-]+)`\s*\|\s*([PF])\s*\|\s*(pass|fail)\s*\|.*\|\s*$")
MECH_ROW = re.compile(r"^\|\s*`([a-z0-9_-]+)`\s*\|\s*`([A-Za-z0-9_.-]+):(\d+)`\s*\|\s*“(.+?)”\s*\|\s*$")


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def spec(lane):
    if sha256(lane / SPEC_REL) != SPEC_SHA256:
        raise ValueError("spec template not at its freeze digest")
    return json.loads((lane / SPEC_REL).read_text())


def dry(lane):
    if sha256(lane / DRY_REL) != DRY_SHA256:
        raise ValueError("dry table not at its freeze digest")
    text = (lane / DRY_REL).read_text()
    tags = {}
    cases = []
    for l in text.splitlines():
        p = l.split()
        if p and p[0] == "TAG":
            tags[p[1]] = p[2]
        elif p and p[0] == "CASE":
            cases.append(p[1])
    return tags, cases


def v1(lane):
    capdir = lane / CAP
    try:
        lines = [l for l in (capdir / "SHA256SUMS").read_text().splitlines() if l.strip()]
    except OSError:
        return False, "manifest absent"
    listed = {}
    for l in lines:
        m = re.match(r"^([0-9a-f]{64})\s+\*?(\S+)$", l.strip())
        if not m:
            return False, f"unparsed manifest line {l[:40]!r}"
        listed[m.group(2)] = m.group(1)
    bad = [n for n, d in CAPTURES.items() if listed.get(n) != d or sha256(capdir / n) != d]
    extra = sorted(set(listed) - set(CAPTURES))
    return not bad and not extra, f"listed={len(listed)} bad={bad or 0} extra={extra or 0}"


def v2(lane, work):
    s = spec(lane)
    if sha256(lane / GATE_REL) != GATE_SHA256:
        return False, "gate not at its freeze digest"
    s["receipt_sha256"] = sha256(lane / s["receipt"]) or "absent"
    sp = pathlib.Path(work) / "pkg-spec-r44-effective.json"
    sp.write_text(json.dumps(s))
    r = subprocess.run([sys.executable, str(lane / GATE_REL), "package", "--root", str(lane), "--spec", str(sp),
                        "--rerun", "--require-clean-tree"], capture_output=True, text=True, timeout=1800)
    for l in r.stdout.splitlines():
        print("    gate: " + l)
    return r.returncode == 0, f"spec=frozen gate=frozen gate_exit={r.returncode}"


def rows(lane):
    out = {}
    for line in (lane / "corpus/SOURCES.md").read_text().splitlines():
        m = SOURCE_ROW.match(line)
        if m:
            out.setdefault(m.group(1), []).append([c.strip() for c in line.strip().strip("|").split("|")])
    return out


def v3(lane):
    s = spec(lane)
    reg, bad = rows(lane), []
    for sid, row in s["rows"].items():
        found = reg.get(sid, [])
        if len(found) != 1 or len(found[0]) != 11:
            bad.append(f"{sid}:row")
            continue
        toks = re.findall(r"sha256\s+([0-9a-fA-F]+)", found[0][5])
        if toks != [row["sha256"]]:
            bad.append(f"{sid}:anchor_digest")
    return not bad, f"rows={len(s['rows'])} bad={bad or 0}"


def receipt_cases(text):
    out = {}
    for l in text.splitlines():
        m = re.match(r"^CASE (\S+) predicted=(pass|fail) observed=(pass|fail) .*?\bviolates=(\S*)", l)
        if m:
            out[m.group(1)] = (m.group(3), set(filter(None, m.group(4).split(","))))
    return out


def v4(lane):
    s = spec(lane)
    try:
        text = (lane / s["receipt"]).read_text()
        entry = (lane / s["entry"]).read_text()
    except OSError:
        return False, "receipt or entry absent"
    _tags, frozen_ids = dry(lane)
    cases = [l for l in text.splitlines() if l.startswith("CASE ")]
    ids = [l.split()[1] for l in cases]
    parsed = receipt_cases(text)
    no = [l.split()[1] for l in cases if " match=NO " in l]
    summ = [SUMMARY.match(l) for l in text.splitlines() if SUMMARY.match(l)]
    bad = []
    if ids != frozen_ids or len(parsed) != len(ids):
        bad.append("case ids differ from the frozen table")
    if len(summ) != 1:
        bad.append("summary line count != 1")
    else:
        n, p, f, m = map(int, summ[0].groups())
        cp = sum(1 for o, _v in parsed.values() if o == "pass")
        cf = sum(1 for o, _v in parsed.values() if o == "fail")
        if not (n == len(frozen_ids) and p + f == n and p == cp and f == cf and m == len(no)):
            bad.append("summary disagrees with the CASE lines")
    unnamed = [c for c in no if f"`{c}`" not in entry]
    if unnamed:
        bad.append(f"mismatch cases not named in the entry: {unnamed}")
    return not bad, f"cases={len(ids)} mismatches_named={len(no) - len(unnamed)}/{len(no)} bad={bad or 0}"


def v5(lane):
    if sha256(lane / PROBE_REL) != PROBE_SHA256 or sha256(lane / DRY_REL) != DRY_SHA256:
        return False, "probe or dry table not at freeze digest"
    r = subprocess.run([sys.executable, str(lane / PROBE_REL), "--lane", str(lane), "--dry"],
                       capture_output=True, text=True, timeout=120)
    same = r.returncode == 0 and r.stdout == (lane / DRY_REL).read_text()
    return same, f"probe=frozen dry_byte_equal={same}"


def v6(lane):
    r = subprocess.run([CENSUS, "validate", "--file", str(lane / "corpus/SOURCES.md")],
                       capture_output=True, text=True, timeout=300)
    return r.returncode == 0, f"census_exit={r.returncode}"


def derive(verdicts):
    if verdicts == {"fail"}:
        return "enforced"
    if verdicts == {"pass"}:
        return "unenforced"
    return "partly"


def v7(lane):
    s = spec(lane)
    tags, _ids = dry(lane)
    try:
        text = (lane / s["receipt"]).read_text()
        entry = (lane / s["entry"]).read_text()
    except OSError:
        return False, "receipt or entry absent"
    parsed = receipt_cases(text)
    sec = re.search(r"^## Requirement map\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
    if not sec:
        return False, "no '## Requirement map' section"
    seen, bad = {}, []
    for l in sec.group(1).splitlines():
        m = MAP_ROW.match(l)
        if not m:
            if l.startswith("|") and "instruction.md:" in l:
                bad.append(f"unparsed row {l[:50]!r}")
            continue
        line, tag, label, rest = m.group(1), m.group(2), m.group(3), m.group(4)
        seen[tag] = seen.get(tag, 0) + 1
        if tag not in tags:
            bad.append(f"{tag}: not a frozen tag")
            continue
        if tags[tag] != f"instruction.md:{line}":
            bad.append(f"{tag}: line {line} is not the frozen {tags[tag]}")
        violating = {cid: obs for cid, (obs, v) in parsed.items() if tag in v}
        if not violating:
            bad.append(f"{tag}: no receipt case violates it")
            continue
        want = derive(set(violating.values()))
        if label != want:
            bad.append(f"{tag}: labelled {label}, receipt derives {want}")
        cited = re.findall(r"`([a-z0-9_-]+)`", rest)
        if not cited or any(c not in violating for c in cited):
            bad.append(f"{tag}: cites no case or a case that does not violate it")
    missing = sorted(set(tags) - set(seen))
    dup = sorted(t for t, n in seen.items() if n > 1)
    if missing or dup:
        bad.append(f"tags missing={missing or 0} duplicated={dup or 0}")
    return not bad, f"rows={sum(seen.values())} tags={len(tags)} bad={bad or 0}"


def v8(lane):
    s = spec(lane)
    r = subprocess.run([sys.executable, str(lane / ORDER_REL), "--lane", str(lane), "--claims", CLAIMS_REL,
                        "--receipt", s["receipt"]], capture_output=True, text=True, timeout=300)
    passed = r.returncode == 0 and "ORDER RESULT PASS" in r.stdout.splitlines()
    return passed, f"order_exit={r.returncode} result={'PASS' if passed else 'not-PASS'}"


def v9(lane):
    s = spec(lane)
    try:
        text = (lane / s["receipt"]).read_text()
        entry = (lane / s["entry"]).read_text()
        province = (lane / "PROVINCE.md").read_text()
        readme = (lane / s["readme"]).read_text()
    except OSError:
        return False, "receipt, entry, PROVINCE.md or README absent"
    want = []
    for l in text.splitlines():
        m = re.match(r"^CASE (\S+) predicted=(?:pass|fail) observed=(pass|fail) tests=([PF]) ", l)
        if m:
            want.append((m.group(1), m.group(3), m.group(2)))
    bad = []
    sec = re.search(r"^## Case table\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
    got = [CASE_ROW.match(l).groups() for l in sec.group(1).splitlines() if CASE_ROW.match(l)] if sec else []
    if not sec:
        bad.append("no '## Case table' section")
    elif not want or got != want:
        bad.append(f"case table rows={len(got)} receipt cases={len(want)} equal={got == want}")
    body = "\n".join(l for l in entry.splitlines() if not l.startswith("source:"))
    missing = [sid for sid in s["rows"] if sid not in body]
    if missing:
        bad.append(f"row ids absent outside source lines: {missing}")
    name = pathlib.PurePosixPath(s["entry"]).name
    if not any(TASK in l and name in l for l in province.splitlines()):
        bad.append("PROVINCE.md names the task and the entry on no line")
    fr = re.search(r"^## Frontier\n(.*?)(?=^## |\Z)", readme, re.S | re.M)
    if not fr or TASK not in fr.group(1):
        bad.append("README ## Frontier does not name the task")
    return not bad, f"case_rows={len(got)}/{len(want)} bad={bad or 0}"


# V10: the source lines that decide each frozen case (capture name -> 1-based line numbers), read by the L1 at the
# freeze from the captures pinned above. Keys equal the frozen dry table's case ids.
DECISIVE = {
    "nop": {"test_outputs.py": (120,)},                                  # open("/app/plaintexts.txt")
    "oracle-solve-sh": {"solve.sh": (289, 304)},                        # ./decrypt with recovered keys > plaintexts
    "decrypt-public-keys": {"gen.py": (12,), "decrypt.c": (136,)},      # keys printed in gen.py; decimal printf
    "replay-public-gen": {"gen.py": (60, 61, 62)},                       # plaintext = sha256(seed + counter)[:8]
    "copy-public-constants": {"test_outputs.py": (4, 121)},              # soln constants; for c in soln.split()
    "oracle-concatenated": {"test_outputs.py": (122,)},                  # assert c in data (substring)
    "oracle-plus-decoys": {"test_outputs.py": (122,)},
    "oracle-reversed": {"test_outputs.py": (121, 122)},
    "oracle-zero-padded": {"test_outputs.py": (122,)},
    "one-missing": {"test_outputs.py": (122,)},
    "hex-output": {"test_outputs.py": (122,), "decrypt.c": (136,)},
    "wrong-key-decrypt": {"test_outputs.py": (122,)},
    "pairs-plaintexts": {"test_outputs.py": (122,)},
    "ciphertexts-copied": {"test_outputs.py": (122,)},
}


def norm(t):
    return " ".join(t.split())


def v10(lane):
    s = spec(lane)
    try:
        text = (lane / s["receipt"]).read_text()
        entry = (lane / s["entry"]).read_text()
    except OSError:
        return False, "receipt or entry absent"
    _tags, frozen_ids = dry(lane)
    if sorted(DECISIVE) != sorted(frozen_ids):
        return False, "DECISIVE keys differ from the frozen case ids"
    want = [l.split()[1] for l in text.splitlines() if l.startswith("CASE ")]
    sec = re.search(r"^## Mechanism\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
    if not sec:
        return False, "no '## Mechanism' section"
    got = [MECH_ROW.match(l).groups() for l in sec.group(1).splitlines() if MECH_ROW.match(l)]
    bad = []
    if [g[0] for g in got] != want or not want:
        bad.append(f"mechanism rows={len(got)} receipt cases={len(want)} ids_equal={[g[0] for g in got] == want}")
    capdir = lane / CAP
    for cid, cap, line, quote in got:
        allowed = DECISIVE.get(cid, {}).get(cap, ())
        if int(line) not in allowed:
            bad.append(f"{cid}:{cap}:{line} not decisive")
            continue
        if cap not in CAPTURES or sha256(capdir / cap) != CAPTURES[cap]:
            bad.append(f"{cid}:{cap} capture not pinned")
            continue
        lines = (capdir / cap).read_text().splitlines()
        q = norm(quote)
        if len(q.split()) < 2 or int(line) > len(lines) or q not in norm(lines[int(line) - 1]):
            bad.append(f"{cid}:{cap}:{line} quote not on the line")
    return not bad, f"mechanism_rows={len(got)}/{len(want)} bad={bad or 0}"


# V11: held-out predictor. STATES is a generator, not an answer key: no verdict is stored in this file.
STATE_KINDS = ("exact", "shuffled", "drop-one", "drop-three", "concat", "zero-pad", "hex", "decoys", "bump-one",
               "absent", "empty", "comma", "split-one", "duplicated", "half", "prefixed-digit")
PRED_SECTION = re.compile(r"^## Predictor\n(.*?)(?=^## |\Z)", re.S | re.M)
PRED_BLOCK = re.compile(r"^```python\n(.*?)^```\s*$", re.S | re.M)
BWRAP = "/usr/bin/bwrap"
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
SANDBOX_ENV = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1",
               "PYTHONDONTWRITEBYTECODE": "1"}


def constants(lane):
    src = (lane / CAP / "test_outputs.py").read_text()
    return re.search(r'soln = """(.*?)"""', src, re.S).group(1).split()


def states(consts):
    import random
    rng = random.Random(44)
    out = []
    for k in range(48):
        kind = STATE_KINDS[k % len(STATE_KINDS)]
        c = list(consts)
        if kind == "shuffled":
            rng.shuffle(c)
        elif kind == "drop-one":
            c.pop(rng.randrange(len(c)))
        elif kind == "drop-three":
            for _ in range(3):
                c.pop(rng.randrange(len(c)))
        elif kind == "bump-one":
            j = rng.randrange(len(c))
            c[j] = str(int(c[j]) + 1)
        elif kind == "half":
            c = c[: len(c) // 2]
        elif kind == "duplicated":
            c = c + c[: rng.randrange(1, 20)]
        decoys = [str(rng.getrandbits(64)) for _ in range(rng.randrange(0, 40))]
        if kind == "absent":
            text = None
        elif kind == "empty":
            text = ""
        elif kind == "concat":
            text = "".join(c)
        elif kind == "zero-pad":
            text = "\n".join("%022d" % int(x) for x in c) + "\n"
        elif kind == "hex":
            text = "\n".join(hex(int(x)) for x in c) + "\n"
        elif kind == "comma":
            text = ", ".join(c)
        elif kind == "split-one":
            j = rng.randrange(len(c))
            c[j] = c[j][:7] + "\n" + c[j][7:]
            text = "\n".join(c) + "\n"
        elif kind == "prefixed-digit":
            text = "\n".join(str(rng.randrange(1, 10)) + x for x in c) + "\n"
        elif kind == "decoys":
            mixed = c + decoys
            rng.shuffle(mixed)
            text = "\n".join(mixed) + "\n"
        else:
            text = "\n".join(c) + "\n"
        out.append((kind, text))
    return out


GRADE_PY = r'''
import contextlib, importlib.util, io, json, os, sys
states = json.load(open("/states.json"))
spec = importlib.util.spec_from_file_location("tb2_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
res = []
for text in states:
    p = "/app/plaintexts.txt"
    if os.path.exists(p):
        os.remove(p)
    if text is not None:
        open(p, "w").write(text)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            mod.test_attack()
        res.append(True)
    except BaseException:
        res.append(False)
print(json.dumps(res))
'''

PREDICT_PY = r'''
import json
states = json.load(open("/states.json"))
ns = {}
exec(compile(open("/predictor.py").read(), "predictor", "exec"), ns)
print(json.dumps([bool(ns["predict"](t)) for t in states]))
'''


def sandboxed(work, script, extra):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if pathlib.os.path.islink(link):
            argv += ["--symlink", pathlib.os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--ro-bind", str(work / "states.json"), "/states.json", "--ro-bind", str(work / script), "/run.py"]
    argv += extra + ["/usr/bin/python3", "/run.py"]
    r = subprocess.run(argv, env=SANDBOX_ENV, capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        raise RuntimeError(f"{script} exit={r.returncode}: {r.stderr.strip()[-200:]}")
    return json.loads(r.stdout.strip().splitlines()[-1])


def v11(lane, work):
    s = spec(lane)
    try:
        entry = (lane / s["entry"]).read_text()
    except OSError:
        return False, "entry absent"
    if sha256(lane / CAP / "test_outputs.py") != CAPTURES["test_outputs.py"]:
        return False, "grader capture not pinned"
    sec = PRED_SECTION.search(entry)
    blocks = PRED_BLOCK.findall(sec.group(1)) if sec else []
    if len(blocks) != 1:
        return False, f"'## Predictor' needs exactly one python block (found {len(blocks)})"
    work = pathlib.Path(work) / "v11"
    (work / "app").mkdir(parents=True)
    (work / "tests").mkdir()
    (work / "tests" / "test_outputs.py").write_bytes((lane / CAP / "test_outputs.py").read_bytes())
    st = states(constants(lane))
    (work / "states.json").write_text(json.dumps([t for _k, t in st]))
    (work / "grade.py").write_text(GRADE_PY)
    (work / "predict.py").write_text(PREDICT_PY)
    (work / "predictor.py").write_text(blocks[0])
    graded = sandboxed(work, "grade.py", ["--bind", str(work / "app"), "/app",
                                          "--ro-bind", str(work / "tests"), "/tests"])
    try:
        pred = sandboxed(work, "predict.py", ["--ro-bind", str(work / "predictor.py"), "/predictor.py"])
    except Exception as e:  # a predictor that crashes is a defect
        return False, f"predictor failed: {e}"
    if len(graded) != len(st) or len(pred) != len(st):
        return False, "result length mismatch"
    dis = [st[k][0] + f"#{k}" for k in range(len(st)) if graded[k] != pred[k]]
    npass, nfail = sum(graded), len(graded) - sum(graded)
    ok = not dis and npass >= 8 and nfail >= 8
    return ok, (f"states={len(st)} grader_pass={npass} grader_fail={nfail} disagree={len(dis)}"
                f"{' at=' + ','.join(dis[:6]) if dis else ''}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="k44-c2-", dir=a.work) as work:
        checks = [("V1", lambda: v1(lane)), ("V2", lambda: v2(lane, work)), ("V3", lambda: v3(lane)),
                  ("V4", lambda: v4(lane)), ("V5", lambda: v5(lane)), ("V6", lambda: v6(lane)),
                  ("V7", lambda: v7(lane)), ("V8", lambda: v8(lane)), ("V9", lambda: v9(lane)), ("V10", lambda: v10(lane)),
                  ("V11", lambda: v11(lane, work))]
        defects = 0
        for name, fn in checks:
            try:
                ok, note = fn()
            except Exception as e:  # a check that cannot run is a defect, never a pass
                ok, note = False, f"error {type(e).__name__}: {e}"
            defects += not ok
            print(f"{name} {'ok' if ok else 'DEFECT'} {note}")
    print(f"checks={len(checks)} defects={defects}")
    print(f"PREDICATE C2 {'pass' if defects == 0 else 'fail'}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
