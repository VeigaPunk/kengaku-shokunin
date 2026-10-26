#!/usr/bin/env python3
"""Round-36 C2 counter (coverage): pinned Terminal-Bench 2.0 `regex-log` grader admitted.

Frozen predicate (same sentence in plans/round-36-claims.md and in the receipt label):
  C2 passes iff `python3 plans/round36_c2_verify.py --lane .` prints `checks=6 defects=0`
  and `PREDICATE C2 pass`, exit 0.
Checks (each prints `W<n> ok|DEFECT <reason>`):
  W1 capture   — corpus/evidence/round36/tb2-regex-log/SHA256SUMS lists test_outputs.py, test.sh and
                 instruction.md; every listed digest equals the file bytes; the three equal the
                 frozen pinned digests below.
  W2 rows      — corpus/SOURCES.md holds S108/S109/S110 exactly once each, 11 cells, tier A, status
                 mined, opened 2026-10-25, source URL = pinned raw URL of its file, used-by = the
                 entry path exactly, teaches >= 8 words and pairwise distinct.
  W3 entry     — corpus/knowledge/tb2-regex-log-grader.md opens with `source:` lines for S108, S109,
                 S110 (each carrying its pinned URL), then `verified-at: 2026-10-25`, then `recheck:`
                 with a date or cadence; has `## Negative space` containing "falsif"; every row of
                 its `## Located quotes` table parses (an unparsed row is a defect), with >= 8 rows,
                 >= 8 distinct quotes of 3..25 words, >= 8 distinct (file, line) locations, each
                 quote verbatim on the cited line(s) of the cited round-36 capture file.
  W4 index     — corpus/README.md has one index row for the entry citing S108, S109, S110, a
                 coverage-map bullet naming it, and knowledge files on disk == index rows >= 43.
  W5 probe     — plans/regex_log_probe.py equals its frozen digest; corpus/evidence/round36/
                 regex-log-probe.txt equals a fresh run byte-for-byte; its summary line reads
                 cases=24; the entry carries that summary line verbatim and names every case whose
                 line says `match=NO`.
  W6 census    — scripts/sources-census.sh validate --root <fleet> kengaku exits 0.
"""
import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/regex-log/"
ENTRY = "corpus/knowledge/tb2-regex-log-grader.md"
CAP = "corpus/evidence/round36/tb2-regex-log/"
RECEIPT = "corpus/evidence/round36/regex-log-probe.txt"
PROBE = "plans/regex_log_probe.py"
PROBE_SHA256 = "d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc"  # Amendment 1 (claims file)
FILES = {  # row id -> (capture name, upstream path, pinned sha256)
    "S108": ("test_outputs.py", "tests/test_outputs.py",
             "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"),
    "S109": ("test.sh", "tests/test.sh",
             "4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334"),
    "S110": ("instruction.md", "instruction.md",
             "4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c"),
}
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
QUOTE_RE = re.compile(r"^\|[^|]*\|\s*“(.+?)”\s*\|\s*`([^`:]+):(\d+)(?:-(\d+))?`\s*\|\s*$")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def w1(lane):
    d = lane / CAP
    sums = d / "SHA256SUMS"
    if not sums.is_file():
        return "SHA256SUMS absent"
    listed = {}
    for line in sums.read_text().splitlines():
        m = re.fullmatch(r"([0-9a-f]{64})\s+\*?(\S+)", line.strip())
        if m:
            listed[m.group(2)] = m.group(1)
    for name, dig in listed.items():
        f = d / name
        if not f.is_file() or sha(f) != dig:
            return f"listed digest mismatch or missing file: {name}"
    for _rid, (name, _up, pin) in FILES.items():
        if listed.get(name) != pin:
            return f"{name} not listed at pinned digest"
    return None


def rows(lane):
    out = {}
    for line in (lane / "corpus/SOURCES.md").read_text().splitlines():
        m = ROW_RE.match(line)
        if m:
            out.setdefault(m.group(1), []).append(line)
    return out


def w2(lane):
    r = rows(lane)
    teaches_seen = set()
    for rid, (_name, up, _pin) in FILES.items():
        got = r.get(rid, [])
        if len(got) != 1:
            return f"{rid} present {len(got)} times"
        cells = [c.strip() for c in got[0].strip().strip("|").split("|")]
        if len(cells) != 11:
            return f"{rid} has {len(cells)} cells"
        _id, source, _kind, tier, _scope, _anchor, teaches, status, opened, _recheck, used = cells
        urls = re.findall(r"https?://\S+", source)
        if urls != [RAW + up]:
            return f"{rid} source URL {urls} != {RAW + up}"
        if tier != "A" or status != "mined" or opened != "2026-10-25":
            return f"{rid} tier/status/opened = {tier}/{status}/{opened}"
        if used != ENTRY:
            return f"{rid} used-by {used!r}"
        if len(teaches.split()) < 8:
            return f"{rid} teaches has {len(teaches.split())} words"
        if teaches in teaches_seen:
            return f"{rid} teaches duplicates another row"
        teaches_seen.add(teaches)
    return None


def w3(lane):
    p = lane / ENTRY
    if not p.is_file():
        return "entry absent"
    text = p.read_text()
    head = text.splitlines()[:5]
    for i, rid in enumerate(FILES):
        if not (len(head) > i and head[i].startswith(f"source: {rid} ") and RAW + FILES[rid][1] in head[i]):
            return f"line {i + 1} is not the {rid} source line with its pinned URL"
    if len(head) < 5 or head[3] != "verified-at: 2026-10-25":
        return "line 4 is not verified-at: 2026-10-25"
    if not re.match(r"recheck: (\d{4}-\d{2}-\d{2}|\d+d|on-release)\b", head[4]):
        return "line 5 recheck lacks date/cadence"
    neg = re.search(r"^## Negative space\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not neg or "falsif" not in neg.group(1):
        return "negative space absent or has no falsifier"
    sec = re.search(r"^## Located quotes\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not sec:
        return "located-quotes section absent"
    body = [l for l in sec.group(1).splitlines() if l.startswith("|") and not re.match(r"^\|[\s|:-]+\|$", l)][1:]
    quotes, locs = set(), set()
    for line in body:
        m = QUOTE_RE.match(line)
        if not m:
            return f"unparsed quote row: {line[:60]}"
        quote, fname, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
        n = len(quote.split())
        if n > 25 or n < 3:
            return f"quote of {n} words: {quote[:40]}"
        f = lane / CAP / fname
        if not f.is_file():
            return f"quote cites missing capture {fname}"
        span = "\n".join(f.read_text().splitlines()[a - 1:b])
        if quote not in span:
            return f"quote not on {fname}:{a}-{b}: {quote[:40]}"
        quotes.add(quote)
        locs.add((fname, a, b))
    if len(body) < 8 or len(quotes) < 8 or len(locs) < 8:
        return f"rows={len(body)} distinct_quotes={len(quotes)} distinct_locations={len(locs)} (want >=8 each)"
    return None


def w4(lane):
    readme = (lane / "corpus/README.md").read_text()
    rel = ENTRY.removeprefix("corpus/")
    idx = [l for l in readme.splitlines() if l.startswith(f"| `{rel}` |")]
    if len(idx) != 1 or not all(s in idx[0] for s in FILES):
        return "index row absent or missing S108/S109/S110"
    cov = re.search(r"^## Coverage map\n(.*?)(?=^## |\Z)", readme, re.S | re.M)
    if not cov or rel not in cov.group(1):
        return "coverage-map bullet absent"
    files = [p for p in (lane / "corpus/knowledge").glob("*.md")]
    nidx = sum(1 for l in readme.splitlines() if l.startswith("| `knowledge/"))
    if not (len(files) == nidx >= 43):
        return f"knowledge files={len(files)} index rows={nidx} (want equal and >=43)"
    return None


def w5(lane):
    probe = lane / PROBE
    if not probe.is_file() or sha(probe) != PROBE_SHA256:
        return "probe file absent or digest differs from the frozen digest"
    rec = lane / RECEIPT
    if not rec.is_file():
        return "probe receipt absent"
    run = subprocess.run([sys.executable, PROBE, "--lane", "."], cwd=lane, capture_output=True, text=True)
    if run.stdout != rec.read_text():
        return f"fresh probe output differs from receipt (exit {run.returncode})"
    lines = run.stdout.strip().splitlines()
    last = lines[-1]
    m = re.fullmatch(r"cases=(\d+) observed_pass=(\d+) observed_fail=(\d+) mismatches=(\d+)", last)
    if not m or m.group(1) != "24":
        return f"summary not the 24-case line: {last}"
    entry = lane / ENTRY
    if not entry.is_file():
        return "entry absent"
    et = entry.read_text()
    if last not in et:
        return "entry does not carry the receipt summary line verbatim"
    for l in lines:
        mm = re.match(r"case=(\S+) .* match=NO ", l)
        if mm and mm.group(1) not in et:
            return f"entry does not name mismatching case {mm.group(1)}"
    return None


def w6(lane, fleet):
    script = str(fleet / "scripts/sources-census.sh")
    if lane == (fleet / "kengaku-shokunin").resolve():
        cmd = [script, "validate", "--root", str(fleet), "kengaku"]
    else:  # a fixture/clone lane: validate its own registry, never the live lane's
        cmd = [script, "validate", "--file", str(lane / "corpus/SOURCES.md")]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return None if r.returncode == 0 else f"census exit {r.returncode}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--fleet", default="/home/vgpnk/Projects/shokunin")
    a = ap.parse_args()
    lane, fleet = pathlib.Path(a.lane).resolve(), pathlib.Path(a.fleet)
    checks = [("W1", lambda: w1(lane)), ("W2", lambda: w2(lane)), ("W3", lambda: w3(lane)),
              ("W4", lambda: w4(lane)), ("W5", lambda: w5(lane)), ("W6", lambda: w6(lane, fleet))]
    defects = 0
    for name, fn in checks:
        try:
            err = fn()
        except Exception as e:  # a crash is a defect, never a pass
            err = f"error {type(e).__name__}: {e}"
        if err:
            defects += 1
            print(f"{name} DEFECT {err}")
        else:
            print(f"{name} ok")
    print(f"checks={len(checks)} defects={defects}")
    print(f"PREDICATE C2 {'pass' if defects == 0 else 'fail'}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
