#!/usr/bin/env python3
"""F35MutLedgerD3 — mutation-test r34_d3 at round-35 tip (wave 2, falsify).

Each scenario gets a fresh fixture clone at TIP with sparse checkout of the
tb2-eval captures + ledger checker + defects.jsonl. The cloned (landed)
SHA256SUMS lists all six files including test_outputs.py and test.sh.
Mutations run on the working tree (the checker reads bytes); no commits.
"""
import hashlib
import pathlib
import shutil
import subprocess
import tempfile

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
TIP = "dfee6fff631ebc5f623ba4506e5c7992a215401c"
CAP = ".ufo/waves/round-34/assimilation/captures/tb2-eval"
PATTERNS = [CAP + "/*", "plans/defect_ledger.py", "corpus/defects.jsonl"]
EVAL = ["test_outputs.py", "test.sh"]


def make_clone(tag):
    D = pathlib.Path(tempfile.mkdtemp(prefix=f"k35F-D3-{tag}-"))
    lane = D / "lane"
    subprocess.run(["git", "clone", "-q", "--no-checkout", "--shared", str(LANE), str(lane)], check=True)
    subprocess.run(["git", "-C", str(lane), "sparse-checkout", "set", "--no-cone", *PATTERNS], check=True)
    subprocess.run(["git", "-C", str(lane), "checkout", "-q", TIP], check=True)
    top = subprocess.run(["git", "-C", str(lane), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert top == str(lane), (top, lane)
    head = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    assert head == TIP, (head, TIP)
    return D, lane


def run_check(lane):
    p = subprocess.run(["python3", "plans/defect_ledger.py", "--lane", "."],
                       cwd=lane, capture_output=True, text=True)
    d3 = [l for l in p.stdout.splitlines() if l.startswith("R34-D3")]
    return p.returncode, p.stdout.rstrip(), (d3[0] if d3 else "(no D3 row)")


def main():
    cap0 = LANE / CAP
    h = {n: hashlib.sha256((cap0 / n).read_bytes()).hexdigest() for n in EVAL}
    print("== landed tip state (read-only lane) ==")
    p = subprocess.run(["sha256sum", "-c", str(cap0 / "SHA256SUMS")], capture_output=True, text=True)
    print(f"sha256sum -c exit={p.returncode}")
    print(p.stdout.rstrip())
    if p.stderr.strip():
        print("stderr:", p.stderr.rstrip())
    print("\n== C2 counter at tip (lane-only) ==")
    p2 = subprocess.run(["python3", "plans/defect_ledger.py", "--lane", "."],
                        cwd=LANE, capture_output=True, text=True)
    print(f"exit={p2.returncode}")
    print(p2.stdout.rstrip())

    results = []

    def scenario(tag, label, mutate):
        D, lane = make_clone(tag)
        try:
            cap = lane / CAP
            mutate(cap)
            rc, full, d3 = run_check(lane)
            results.append((label, d3, rc))
            print(f"\n=== {label} (clone {D.name}) rc={rc}")
            print(d3)
        finally:
            shutil.rmtree(D, ignore_errors=True)

    # baseline: landed 6-line manifest, untouched
    def base(cap):
        pass
    scenario("base", "baseline landed manifest (6 files)", base)

    # M1: flip one hex digit of the test.sh line
    def m1(cap):
        lines = (cap / "SHA256SUMS").read_text().splitlines()
        new = []
        for ln in lines:
            if ln.rstrip().endswith("  test.sh"):
                digest = ln.split()[0]
                flipped = ("0" if digest[0] != "0" else "1") + digest[1:]
                new.append(ln.replace(digest, flipped, 1))
            else:
                new.append(ln)
        (cap / "SHA256SUMS").write_text("\n".join(new) + "\n")
    scenario("m1", "M1 test.sh digest hex digit flipped", m1)

    # M2: delete the test_outputs.py line
    def m2(cap):
        lines = [ln for ln in (cap / "SHA256SUMS").read_text().splitlines()
                 if not ln.rstrip().endswith("  test_outputs.py")]
        (cap / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    scenario("m2", "M2 test_outputs.py line deleted", m2)

    # M3: append a line for a missing file
    def m3(cap):
        dummy = "0" * 64
        with (cap / "SHA256SUMS").open("a") as f:
            f.write(f"{dummy}  missing-probe.txt\n")
    scenario("m3", "M3 line appended for missing file", m3)

    print("\n\nSUMMARY")
    for label, d3, rc in results:
        print(f"{label:44s} rc={rc}  {d3}")


if __name__ == "__main__":
    main()
