#!/usr/bin/env python3
"""R98-C2 counter — nested replay captures the frozen anchor-digest gate cannot bind (round 98).

Population (claim-local, derived at BASE by one rule and frozen below as POP): a SOURCES row whose
ONLY `anchor-digest-check` defect is `anchor-unbound` with detail
`no-capture-for-upstream-<task>/<sub>/<file>-task=<sub>`, and for which a committed file
`corpus/evidence/round<N>/graders/<task>/<sub>/<file>` exists at BASE whose sha256 equals the
row's 64-hex token. The expected capture is the matching file from the highest round. The gate
cannot bind these because it looks for `<task dir>/<basename>` (flat), while rounds 52 and 92-97
captured nested task trees (round-97 routed defect 1).

The gate is never edited. Each revision is checked out in a `git clone --shared` fixture under
--work (the gate reads SOURCES.md from the work tree and evidence from HEAD) and the BASE bytes of
`plans/anchor_digest_check.py` are run there with --verbose.

Legs (every input read at the revision):
  K1 `plans/anchor_digest_check.py` at --rev hashes to its BASE sha (gate unchanged)
  K2 the population re-derived at BASE equals POP (ids, tokens, expected capture paths)
  K3 at --rev the gate prints no DEFECT line for any POP row
  K4 at --rev every POP row is `BIND <sid> capture=<expected path> by=provenance-row` and `RESOLVED
     <sid> digest=<token>` — bound to the replay's own committed capture, not to a copy
  K5 every POP row's SOURCES.md line at --rev is byte-identical to BASE (no token edited away)
  K6 every expected capture blob at --rev is byte-identical to BASE
  K7 for every row id present at BASE, the (sid, class) DEFECT pairs at --rev are a subset of
     BASE's — rows added after BASE (other claims) are outside this claim's population

Usage:  python3 plans/round98_c2_nested_bind.py --lane <repo> --rev <rev> --work <dir>
Exit:   0 predicate pass, 1 a leg failed, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

BASE = "49a1c4f1097db7c923da56d4213cad75772ed1c0"
GATE = "plans/anchor_digest_check.py"
GATE_SHA = "11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2"
SOURCES = "corpus/SOURCES.md"
DEFECT = re.compile(r"^DEFECT (S\d{3,}) \S+ token=(\S+) class=(\S+) detail=(\S+)")
BIND = re.compile(r"^BIND (S\d{3,}) capture=(\S+) by=(\S+)")
RESOLVED = re.compile(r"^RESOLVED (S\d{3,}) digest=([0-9a-f]+) via=(\S+)")
NESTED = re.compile(r"^no-capture-for-upstream-(.+)-task=(tests|solution|environment)$")
ROWID = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
# sid -> (token, expected capture path); frozen from the BASE derivation (P1 receipt c2-pop.txt)
POP: dict[str, tuple[str, str]] = {
    "S181": ("364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b", "corpus/evidence/round52/graders/bn-fit-modify/tests/test_outputs.py"),
    "S182": ("5d4d57c43e6913bf3d0081da764ad36d1b7275e3bb114a05abda529afe563905", "corpus/evidence/round52/graders/pytorch-model-recovery/tests/test_outputs.py"),
    "S183": ("4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290", "corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py"),
    "S201": ("a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286", "corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py"),
    "S224": ("d6f510b51fafc81b4e9b5cc95535aa13491c8753e0e4171db42c45f4de460ee7", "corpus/evidence/round52/graders/cancel-async-tasks/tests/test_outputs.py"),
    "S234": ("115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e", "corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py"),
    "S241": ("045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0", "corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py"),
    "S243": ("045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0", "corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py"),
    "S273": ("8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881", "corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py"),
    "S274": ("171fae772ccf262aec8ddac5bd2c6c731eed842421f5d8439a330b158c9f8c13", "corpus/evidence/round52/graders/raman-fitting/tests/test_outputs.py"),
    "S275": ("e4e6b21fed6662adb4a42aba23d35609450392839a2282f3ba77c70c8d907c0b", "corpus/evidence/round52/graders/mteb-retrieve/tests/test_outputs.py"),
    "S276": ("b28f8fc8b7614801305813c402be52f4be1e75de6658ecdfdf9383aa793892cf", "corpus/evidence/round52/graders/mteb-leaderboard/tests/test_outputs.py"),
    "S277": ("a8a6f51eb0d7c4ebdf0813c8f0b645edf29c995f1f9faf2aca3886a6713043f3", "corpus/evidence/round52/graders/fix-git/tests/test_outputs.py"),
    "S278": ("baed5e4d0cc0e5809ff41a7df1815d18c65c708a3a3f264428e1cda11ce692f9", "corpus/evidence/round52/graders/polyglot-rust-c/tests/test_outputs.py"),
    "S280": ("c9052954cd6ce25c4a375a2fb48e765b1efa5b39f7991b93993cc793af8ab9d2", "corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test.sh"),
    "S282": ("e868c85466ebf4815e2e4efbd252bf50ad979bceb14325a9377b1bbf852f0281", "corpus/evidence/round52/graders/modernize-scientific-stack/tests/test.sh"),
    "S283": ("80b06b7c4ba0db28832b767d48be74bb462d7f5df5798d9cb58c4f1160d96ffa", "corpus/evidence/round92/graders/llm-inference-batching-scheduler/tests/test_outputs.py"),
    "S284": ("d3e810a99d40327fb8317f6512d879c52c6aeebdf5dcdc0c5e117c7df61c9ab9", "corpus/evidence/round92/graders/llm-inference-batching-scheduler/tests/cost_model_for_tests.py"),
    "S290": ("fbb84e3c0c2f72ed7de90f54380f860052c16155e7d0c9076cd57c966e9be7ed", "corpus/evidence/round93/graders/schemelike-metacircular-eval/tests/test_outputs.py"),
    "S291": ("efb8b5cdcf78b73afcf39d59600a1f355ca89b7bac9854bb01f110cc77bea2c1", "corpus/evidence/round93/graders/schemelike-metacircular-eval/tests/interp.py"),
    "S292": ("e2c5b0ac2bef4801a1891e13c108813381877426c1a7f01bab86b4fc1f712510", "corpus/evidence/round93/graders/schemelike-metacircular-eval/solution/solve.sh"),
    "S297": ("809f486053e3ffbce852111dee1f63d80ab31297bd33172389e50278bed384e2", "corpus/evidence/round94/graders/write-compressor/tests/test_outputs.py"),
    "S299": ("0fc483d0fb31128dfa41ed11adca56c88688888189826ef9daeafd7559b4fa4e", "corpus/evidence/round94/graders/write-compressor/tests/original-data.txt"),
    "S301": ("4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334", "corpus/evidence/round94/graders/write-compressor/tests/test.sh"),
    "S302": ("9a583d29d46818f6ff2be7c6a0879d03343106e5376fd5a48eb5926b402bb93b", "corpus/evidence/round94/graders/write-compressor/environment/Dockerfile"),
    "S303": ("c006a5de95b69bd78055aa26cc055734dbd50718ede25d331f767bfee4ef7f26", "corpus/evidence/round95/graders/fix-code-vulnerability/tests/test_outputs.py"),
    "S304": ("7a0131b369d83ae8546ecc3f9b4e23d38240f1bd1f0941e4430fa85b5182ee03", "corpus/evidence/round95/graders/fix-code-vulnerability/solution/solve.sh"),
    "S305": ("0917470986224df4daf4854a71302ae81c73ba5dd6e25be1232d29b758a5b3ab", "corpus/evidence/round95/graders/fix-code-vulnerability/environment/Dockerfile"),
    "S308": ("f1611da693cb4cfc5e8482698c6a1858a5c67220ae9db89b50aed66584e9b17f", "corpus/evidence/round95/graders/fix-code-vulnerability/tests/test.sh"),
    "S310": ("a070888930cf829aeca039771260b1386bda990ea805f313468d381ba3608ca5", "corpus/evidence/round96/graders/multi-source-data-merger/tests/test_outputs.py"),
    "S311": ("1b3d0d50e31930d042495d48f4c8e95f1a9c1a979c803b7f7cec651322537e1e", "corpus/evidence/round96/graders/multi-source-data-merger/solution/solve.sh"),
    "S312": ("c95a40d3d35b473dc15ae1e8784ba7fb1725805c0583fc574dd2764325d75e4f", "corpus/evidence/round96/graders/multi-source-data-merger/environment/Dockerfile"),
    "S313": ("d5a00e64413c0e1ae452f38a1aa1a47c3ed7b4416bbfccae1a4c053025a336d1", "corpus/evidence/round96/graders/multi-source-data-merger/tests/test.sh"),
    "S317": ("ecf15840fc14f1eeff2f3b6317d7f0febc8fa81f688d24e3054205ba13207b39", "corpus/evidence/round97/graders/sparql-university/tests/test_outputs.py"),
    "S318": ("368ce01d32513ee04dfe592784b0c976086e514c1eab9b3165a016ca7b0192cb", "corpus/evidence/round97/graders/sparql-university/tests/university_graph_test.ttl"),
    "S319": ("d17995a8f29c6d656c749271fd28e10d31afee6aa75f40ad28fea1c907f2a791", "corpus/evidence/round97/graders/sparql-university/solution/solve.sh"),
    "S320": ("45902b57bd0f1dd6959216bc9943ab27bb349edc7ff557035a1ecc8732e4cc6b", "corpus/evidence/round97/graders/sparql-university/tests/test.sh"),
    "S322": ("0b0b1f2c0ee7ea7ddc9382f94ff8181996ffa7be60a1651111c1f57b49e09a85", "corpus/evidence/round97/graders/sparql-university/environment/university_graph.ttl"),
    "S323": ("dd0abcd64e90ab16141169bcbf88a8e5f52732f207cb37765d351cc7a48916a9", "corpus/evidence/round97/graders/sparql-university/environment/Dockerfile"),
}


class CouldNotEvaluate(Exception):
    pass


def git(root: Path, *args: str, timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=timeout)


def blob(root: Path, rev: str, path: str) -> bytes | None:
    proc = git(root, "show", f"{rev}:{path}")
    return proc.stdout if proc.returncode == 0 else None


def sha(data: bytes | None) -> str:
    return hashlib.sha256(data).hexdigest() if data is not None else "absent"


def checkout(lane: Path, rev: str, dest: Path) -> Path:
    if dest.exists():
        shutil.rmtree(dest)
    proc = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", str(lane), str(dest)],
                          capture_output=True, timeout=300)
    if proc.returncode != 0:
        raise CouldNotEvaluate(f"clone failed {proc.stderr.decode(errors='replace')[-200:]}")
    proc = git(dest, "-c", "advice.detachedHead=false", "checkout", "-q", rev)
    if proc.returncode != 0:
        raise CouldNotEvaluate(f"checkout {rev} failed")
    if git(dest, "rev-parse", "--show-toplevel").stdout.decode().strip() != str(dest):
        raise CouldNotEvaluate(f"fixture toplevel is not {dest}")
    return dest


def run_gate(gate: Path, tree: Path) -> list[str]:
    proc = subprocess.run([sys.executable, "-I", "-B", str(gate), "--lane", str(tree), "--verbose"],
                          capture_output=True, text=True, timeout=1200, cwd=str(tree))
    if proc.returncode not in (0, 1):
        raise CouldNotEvaluate(f"gate rc={proc.returncode} {proc.stdout.strip()[-200:]} {proc.stderr.strip()[-200:]}")
    return proc.stdout.splitlines()


def parse(lines: list[str]) -> dict:
    defects: dict[str, list[tuple[str, str, str]]] = {}
    binds: dict[str, list[tuple[str, str]]] = {}
    resolved: dict[str, list[tuple[str, str]]] = {}
    for line in lines:
        m = DEFECT.match(line)
        if m:
            defects.setdefault(m.group(1), []).append((m.group(2), m.group(3), m.group(4)))
            continue
        m = BIND.match(line)
        if m:
            binds.setdefault(m.group(1), []).append((m.group(2), m.group(3)))
            continue
        m = RESOLVED.match(line)
        if m:
            resolved.setdefault(m.group(1), []).append((m.group(2), m.group(3)))
    return {"defects": defects, "binds": binds, "resolved": resolved}


def rows(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        m = ROWID.match(line)
        if m:
            out.setdefault(m.group(1), line)
    return out


def derive(lane: Path, parsed: dict) -> dict[str, tuple[str, str]]:
    files = git(lane, "ls-tree", "-r", "--name-only", BASE, "corpus/evidence").stdout.decode().splitlines()
    pop: dict[str, tuple[str, str]] = {}
    for sid, ds in parsed["defects"].items():
        if len(ds) != 1:
            continue
        token, cls, detail = ds[0]
        m = NESTED.match(detail)
        if cls != "anchor-unbound" or not m or not re.fullmatch(r"[0-9a-f]{64}", token):
            continue
        tail = "/graders/" + m.group(1)
        hits = []
        for p in files:
            rm = re.match(r"^corpus/evidence/round(\d+)/graders/", p)
            if rm and p.endswith(tail) and p == f"corpus/evidence/round{rm.group(1)}{tail}":
                if sha(blob(lane, BASE, p)) == token:
                    hits.append((int(rm.group(1)), p))
        if hits:
            pop[sid] = (token, max(hits)[1])
    return pop


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--work", required=True)
    ap.add_argument("--derive", action="store_true", help="print the BASE population and exit (P1 only)")
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    work = Path(a.work).resolve()
    if work == lane or lane in work.parents:
        raise CouldNotEvaluate(f"--work inside the lane {work}")
    work.mkdir(parents=True, exist_ok=True)
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{a.rev}^{{commit}}")
    if proc.returncode != 0:
        raise CouldNotEvaluate(f"unresolved-revision {a.rev}")
    rev = proc.stdout.decode().strip()
    gate_base = blob(lane, BASE, GATE)
    if gate_base is None:
        raise CouldNotEvaluate("gate absent at BASE")
    gate = work / "gate-base.py"
    gate.write_bytes(gate_base)
    try:
        base_tree = checkout(lane, BASE, work / "base")
        base = parse(run_gate(gate, base_tree))
        derived = derive(lane, base)
        if a.derive:
            for sid in sorted(derived, key=lambda s: int(s[1:])):
                print(f'    "{sid}": ("{derived[sid][0]}", "{derived[sid][1]}"),')
            print(f"# GATE_SHA {sha(gate_base)} n={len(derived)}")
            return 0
        rev_tree = checkout(lane, rev, work / "rev")
        at = parse(run_gate(gate, rev_tree))
    finally:
        shutil.rmtree(work / "base", ignore_errors=True)
        shutil.rmtree(work / "rev", ignore_errors=True)

    defects: list[str] = []
    k1 = sha(gate_base) == GATE_SHA and sha(blob(lane, rev, GATE)) == GATE_SHA
    if not k1:
        defects.append(f"K1 gate base={sha(gate_base)[:12]} rev={sha(blob(lane, rev, GATE))[:12]} frozen={GATE_SHA[:12]}")
    k2 = derived == POP and len(POP) > 0
    if not k2:
        defects.append(f"K2 population derived={len(derived)} frozen={len(POP)} "
                       f"extra={sorted(set(derived) - set(POP))} missing={sorted(set(POP) - set(derived))}")
    still = sorted((s for s in POP if s in at["defects"]), key=lambda s: int(s[1:]))
    k3 = not still
    if not k3:
        defects.append(f"K3 POP rows still defective n={len(still)} {','.join(still)}")
    unbound = []
    for sid, (token, path) in POP.items():
        if at["binds"].get(sid) != [(path, "provenance-row")] or (token, path) not in at["resolved"].get(sid, []):
            unbound.append(sid)
    unbound.sort(key=lambda s: int(s[1:]))
    k4 = not unbound
    if not k4:
        defects.append(f"K4 not bound to the expected capture by provenance-row n={len(unbound)} {','.join(unbound)}")
    base_rows = rows((blob(lane, BASE, SOURCES) or b"").decode(errors="replace"))
    rev_rows = rows((blob(lane, rev, SOURCES) or b"").decode(errors="replace"))
    changed = sorted((s for s in POP if base_rows.get(s) is None or rev_rows.get(s) != base_rows.get(s)),
                     key=lambda s: int(s[1:]))
    k5 = not changed
    k5 = True  # MUTANT L5: leg disabled
    if not k5:
        defects.append(f"K5 POP SOURCES rows changed n={len(changed)} {','.join(changed)}")
    caps = sorted({p for _, p in POP.values() if blob(lane, rev, p) != blob(lane, BASE, p)})
    k6 = not caps
    if not k6:
        defects.append(f"K6 expected captures changed n={len(caps)} {','.join(caps)}")
    new_old = []
    for sid in base_rows:
        before = {(c) for _, c, _ in base["defects"].get(sid, [])}
        after = {(c) for _, c, _ in at["defects"].get(sid, [])}
        if after - before:
            new_old.append(f"{sid}:{'+'.join(sorted(after - before))}")
    k7 = not new_old
    if not k7:
        defects.append(f"K7 new defect classes on BASE rows n={len(new_old)} {','.join(new_old)}")

    legs = [k1, k2, k3, k4, k5, k6, k7]
    ok = all(legs)
    base_total = sum(len(v) for v in base["defects"].values())
    rev_total = sum(len(v) for v in at["defects"].values())
    print("LEGS " + " ".join(f"K{i + 1}={'pass' if v else 'fail'}" for i, v in enumerate(legs)))
    print(f"GATE defects base={base_total} rev={rev_total}")
    print(f"TARGET pop={len(POP)} cleared={len(POP) - len(still)} still={len(still)} unbound={len(unbound)} "
          f"rows_changed={len(changed)} captures_changed={len(caps)} new_old_row_defects={len(new_old)}")
    for d in defects:
        print("DEFECT " + d)
    print("PREDICATE R98-C2 " + ("pass" if ok else "fail"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R98-C2 could-not-evaluate")
        sys.exit(2)
