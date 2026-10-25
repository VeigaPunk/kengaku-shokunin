#!/usr/bin/env python3
"""Round-35 C1 counter (coverage): pinned Terminal-Bench 2.0 `protein-assembly` grader admitted.

Frozen predicate (same sentence in plans/round-35-claims.md and in the receipt label):
  C1 passes iff `python3 plans/round35_c1_verify.py --lane .` prints `checks=6 defects=0`
  and `PREDICATE C1 pass`, exit 0.
Checks (each prints `V<n> ok|DEFECT <reason>`):
  V1 capture   — corpus/evidence/round35/tb2-eval/SHA256SUMS lists test_outputs.py, test.sh and
                 instruction.md; every listed digest equals the file bytes; the three equal the
                 frozen pinned digests below.
  V2 rows      — corpus/SOURCES.md holds S105/S106/S107 exactly once each, 11 cells, tier A,
                 status mined, opened 2026-10-25, source URL = pinned raw URL of its file,
                 used-by = the entry path exactly.
  V3 entry     — corpus/knowledge/tb2-protein-assembly-grader.md opens with `source:` lines for
                 S105, S106, S107 (each carrying its pinned URL), then `verified-at: 2026-10-25`,
                 then `recheck:` with a date or cadence; has `## Negative space` containing
                 "falsif"; its `## Located quotes` table holds >=8 rows and every quote (<=25 words)
                 occurs verbatim on the cited line(s) of the cited round-35 capture file.
  V4 index     — corpus/README.md has an index row for the entry citing S105, S106, S107, a
                 coverage-map bullet naming it, and committed knowledge files == index rows == 42.
  V5 probe     — corpus/evidence/round35/tb2-grader-probe.txt equals a fresh run of
                 plans/tb2_grader_probe.py byte-for-byte; its summary line reports mismatches=0
                 and observed_pass>=1; the entry contains that summary line verbatim.
  V6 census    — scripts/sources-census.sh validate --root <fleet> kengaku exits 0.
"""
import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/protein-assembly/"
ENTRY = "corpus/knowledge/tb2-protein-assembly-grader.md"
CAP = "corpus/evidence/round35/tb2-eval/"
RECEIPT = "corpus/evidence/round35/tb2-grader-probe.txt"
FILES = {  # row id -> (capture name, upstream path, pinned sha256)
    "S105": ("test_outputs.py", "tests/test_outputs.py",
             "44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582"),
    "S106": ("test.sh", "tests/test.sh",
             "9ede46648fc67c9ce61975503de3e0fcff0b0fb110adc0f9e1d240a608c267b5"),
    "S107": ("instruction.md", "instruction.md",
             "1bb2af1d85e9a823a8ae7273a87df8a3f67e2c93b06cddf34f0051a8b003f7c5"),
}
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def section(text, heading):
    """Content of a `## <heading>` markdown section, or None."""
    return re.search(rf"^## {heading}\n(.*?)(?=^## |\Z)", text, re.S | re.M)


def v1(lane):
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
    for rid, (name, _up, pin) in FILES.items():
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


def v2(lane):
    r = rows(lane)
    for rid, (_name, up, _pin) in FILES.items():
        got = r.get(rid, [])
        if len(got) != 1:
            return f"{rid} present {len(got)} times"
        cells = [c.strip() for c in got[0].strip().strip("|").split("|")]
        if len(cells) != 11:
            return f"{rid} has {len(cells)} cells"
        _id, source, _kind, tier, _scope, _anchor, _teaches, status, opened, _recheck, used = cells
        urls = re.findall(r"https?://\S+", source)
        if urls != [RAW + up]:
            return f"{rid} source URL {urls} != {RAW + up}"
        if tier != "A" or status != "mined" or opened != "2026-10-25":
            return f"{rid} tier/status/opened = {tier}/{status}/{opened}"
        if used != ENTRY:
            return f"{rid} used-by {used!r}"
    return None


def v3(lane):
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
    neg = section(text, "Negative space")
    if not neg or "falsif" not in neg.group(1):
        return "negative space absent or has no falsifier"
    sec = section(text, "Located quotes")
    if not sec:
        return "located-quotes section absent"
    n = 0
    for line in sec.group(1).splitlines():
        m = re.match(r"^\|[^|]*\|\s*“(.+?)”\s*\|\s*`([^`:]+):(\d+)(?:-(\d+))?`\s*\|\s*$", line)
        if not m:
            continue
        quote, fname, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
        if len(quote.split()) > 25:
            return f"quote over 25 words: {quote[:40]}"
        f = lane / CAP / fname
        if not f.is_file():
            return f"quote cites missing capture {fname}"
        span = "\n".join(f.read_text().splitlines()[a - 1:b])
        if quote not in span:
            return f"quote not on {fname}:{a}-{b}: {quote[:40]}"
        n += 1
    if n < 8:
        return f"only {n} located quotes"
    return None


def v4(lane):
    readme = (lane / "corpus/README.md").read_text()
    rel = ENTRY.removeprefix("corpus/")
    idx = [l for l in readme.splitlines() if l.startswith(f"| `{rel}` |")]
    if len(idx) != 1 or not all(s in idx[0] for s in FILES):
        return "index row absent or missing S105/S106/S107"
    cov = re.search(r"^## Coverage map\n(.*?)(?=^## |\Z)", readme, re.S | re.M)
    if not cov or rel not in cov.group(1):
        return "coverage-map bullet absent"
    files = subprocess.run(["git", "-C", str(lane), "ls-files", "corpus/knowledge/*.md"],
                           capture_output=True, text=True).stdout.split()
    nidx = sum(1 for l in readme.splitlines() if l.startswith("| `knowledge/"))
    if not (len(files) == nidx == 42):
        return f"knowledge files={len(files)} index rows={nidx} (want 42/42)"
    return None


def v5(lane):
    rec = lane / RECEIPT
    if not rec.is_file():
        return "probe receipt absent"
    probe = ["plans/tb2_grader_probe.py", "--lane", "."]
    try:
        import Bio  # noqa: F401
        cmd = [sys.executable] + probe
    except ImportError:
        cmd = ["uv", "run", "--no-project", "--with", "biopython==1.85", "python3"] + probe
    run = subprocess.run(cmd, cwd=lane, capture_output=True, text=True)
    if run.stdout != rec.read_text():
        return f"fresh probe output differs from receipt (exit {run.returncode})"
    last = run.stdout.strip().splitlines()[-1]
    m = re.fullmatch(r"cases=(\d+) observed_pass=(\d+) observed_fail=(\d+) mismatches=(\d+)", last)
    if not m or m.group(4) != "0" or int(m.group(2)) < 1:
        return f"summary not green: {last}"
    entry = lane / ENTRY
    if not entry.is_file() or last not in entry.read_text():
        return "entry does not carry the receipt summary line verbatim"
    return None


def v6(lane, fleet):
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
    checks = [("V1", lambda: v1(lane)), ("V2", lambda: v2(lane)), ("V3", lambda: v3(lane)),
              ("V4", lambda: v4(lane)), ("V5", lambda: v5(lane)), ("V6", lambda: v6(lane, fleet))]
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
    print(f"PREDICATE C1 {'pass' if defects == 0 else 'fail'}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
