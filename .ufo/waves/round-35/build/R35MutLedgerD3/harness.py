#!/usr/bin/env python3
"""R35MutLedgerD3 — attack check r34_d3 in fixture clones.

Each scenario gets a fresh fixture clone (commit-state only, sparse checkout of the
tb2-eval captures + the ledger checker + defects.jsonl). The baseline committed
SHA256SUMS lists only antibody.fasta/pdb_ids.txt/task.toml/instruction.md.
"""
import hashlib
import pathlib
import shutil
import subprocess
import tempfile

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CAP = ".ufo/waves/round-34/assimilation/captures/tb2-eval"
PATTERNS = [CAP + "/*", "plans/defect_ledger.py", "corpus/defects.jsonl"]
FOUR = ["antibody.fasta", "pdb_ids.txt", "task.toml", "instruction.md"]


def make_clone(tag):
    D = pathlib.Path(tempfile.mkdtemp(prefix=f"k35-D3-{tag}-"))
    lane = D / "lane"
    subprocess.run(["git", "clone", "-q", "--no-checkout", "--shared", str(LANE), str(lane)], check=True)
    subprocess.run(["git", "-C", str(lane), "sparse-checkout", "set", "--no-cone", *PATTERNS], check=True)
    subprocess.run(["git", "-C", str(lane), "checkout", "-q", "master"], check=True)
    top = subprocess.run(["git", "-C", str(lane), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert top == str(lane), (top, lane)
    return D, lane


def run_check(lane):
    p = subprocess.run(["python3", "plans/defect_ledger.py", "--lane", "."],
                       cwd=lane, capture_output=True, text=True)
    d3 = [l for l in p.stdout.splitlines() if l.startswith("R34-D3")]
    return p.returncode, p.stdout.rstrip(), (d3[0] if d3 else "(no D3 row)")


def sha(names, cap):
    return {n: hashlib.sha256((cap / n).read_bytes()).hexdigest() for n in names}


def manifest(cap, entries):
    # entries: list of (name, digest) OR raw line strings
    lines = []
    for e in entries:
        if isinstance(e, tuple):
            n, h = e
            lines.append(f"{h}  {n}")
        else:
            lines.append(e)
    return "\n".join(lines) + "\n"


def main():
    cap0 = LANE / CAP
    h = sha(FOUR + ["test_outputs.py", "test.sh"], cap0)
    good_out = h["test_outputs.py"]
    good_sh = h["test.sh"]
    print("computed digests from source working tree:")
    print(f"  test_outputs.py {good_out}")
    print(f"  test.sh {good_sh}")

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

    # baseline: committed 4-file manifest (leave as committed)
    def base(cap):
        pass
    scenario("base", "baseline committed manifest (4 files)", base)

    def base4(cap):
        # the clone's committed 4-line manifest, verbatim
        return (cap / "SHA256SUMS").read_text().rstrip("\n")

    # (a) append correct sha256 lines for test_outputs.py and test.sh
    def a(cap):
        lines = [base4(cap), f"{good_out}  test_outputs.py", f"{good_sh}  test.sh"]
        (cap / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    scenario("a", "(a) correct lines appended", a)

    # (b) wrong digest for test.sh
    def b(cap):
        bad_sh = ("0" if good_sh[0] != "0" else "1") + good_sh[1:]
        lines = [base4(cap), f"{good_out}  test_outputs.py", f"{bad_sh}  test.sh"]
        (cap / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    scenario("b", "(b) wrong digest for test.sh", b)

    # (c) listed file deleted (test.sh physically removed)
    def c(cap):
        lines = [base4(cap), f"{good_out}  test_outputs.py", f"{good_sh}  test.sh"]
        (cap / "SHA256SUMS").write_text("\n".join(lines) + "\n")
        (cap / "test.sh").unlink()
    scenario("c", "(c) listed test.sh deleted", c)

    # (d) only test_outputs.py listed
    def d(cap):
        lines = [base4(cap), f"{good_out}  test_outputs.py"]
        (cap / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    scenario("d", "(d) only test_outputs.py listed", d)

    # (e1) path written as ./test.sh
    def e1(cap):
        lines = [base4(cap), f"{good_out}  ./test_outputs.py", f"{good_sh}  ./test.sh"]
        (cap / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    scenario("e1", "(e1) path written as ./test.sh", e1)

    # (e2) sha256sum -b style `*` binary markers
    def e2(cap):
        lines = [base4(cap), f"{good_out} *test_outputs.py", f"{good_sh} *test.sh"]
        (cap / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    scenario("e2", "(e2) `*` binary marker lines", e2)

    # bonus: unlisted file deleted is invisible to the check
    def f(cap):
        lines = [base4(cap), f"{good_out}  test_outputs.py", f"{good_sh}  test.sh"]
        (cap / "SHA256SUMS").write_text("\n".join(lines) + "\n")
        (cap / "task.toml").unlink()
    scenario("f", "(f) unlisted task.toml deleted (bonus)", f)

    print("\n\nSUMMARY")
    for label, d3, rc in results:
        print(f"{label:44s} rc={rc}  {d3}")


if __name__ == "__main__":
    main()
