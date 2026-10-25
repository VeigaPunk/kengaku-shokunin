#!/usr/bin/env python3
"""Independent record-by-record replay of the frozen round-27 extraction comparison."""
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path

# FEntryNumbers' independent witness; L1 changed only this relocated root binding.
ROOT = Path(__file__).resolve().parents[3]
FILES = OrderedDict([
    ("corpus/evidence/round8-horizon/results.jsonl", "bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204"),
    ("corpus/evidence/round9-replication/results-r9.jsonl", "c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb"),
    ("corpus/evidence/round11-power/results-r11.jsonl", "918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad"),
    ("corpus/evidence/round12-ladder/results-r12.jsonl", "ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1"),
])
POLICY_IDS = [f"E{i}" for i in range(9)]
NAMES = dict(zip(POLICY_IDS, ("lane", "first-fence", "bare-last", "bare-first", "strict-whole", "fence-only", "any-label-fence", "decode-first", "decode-last")))
FORMAT_CLASSES = ("FJ1", "FJM", "MULTI", "DANGLE", "BARE")
FENCE = re.compile(r"```(?:json)?\s*\n(.*?)```", re.S)
ANY_FENCE = re.compile(r"```[A-Za-z0-9_+-]*[ \t]*\r?\n(.*?)```", re.S)
BARE = re.compile(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]", re.S)
DECODER = json.JSONDecoder()


def parse(s):
    try:
        return True, json.loads(s)
    except Exception:
        return False, None


def bare(raw, first):
    candidates = BARE.findall(raw)
    for text in (candidates if first else reversed(candidates)):
        ok, value = parse(text)
        if ok:
            return True, value
    return False, None


def extract(pid, raw):
    if pid in ("E0", "E1", "E5"):
        matches = FENCE.findall(raw)
        if matches:
            ok, value = parse(matches[0] if pid == "E1" else matches[-1])
            if ok:
                return value
        return None if pid == "E5" else bare(raw, False)[1]
    if pid == "E2":
        return bare(raw, False)[1]
    if pid == "E3":
        return bare(raw, True)[1]
    if pid == "E4":
        return parse(raw.strip())[1]
    if pid == "E6":
        matches = ANY_FENCE.findall(raw)
        if matches:
            ok, value = parse(matches[-1])
            if ok:
                return value
        return bare(raw, False)[1]
    if pid == "E7":
        for i, ch in enumerate(raw):
            if ch in "{[":
                try:
                    return DECODER.raw_decode(raw, i)[0]
                except Exception:
                    pass
        return None
    if pid == "E8":
        last = None
        i = 0
        while i < len(raw):
            if raw[i] not in "{[":
                i += 1
                continue
            try:
                last, end = DECODER.raw_decode(raw, i)
            except Exception:
                i += 1
            else:
                i = end
        return last
    raise AssertionError(pid)


def state_apply(old, op):
    new = dict(old)
    kind = op[0]
    if kind == "SET":
        new[op[1]] = op[2]
    elif kind == "ADD":
        new[op[1]] += op[2]
    elif kind == "SUB":
        new[op[1]] -= op[2]
    elif kind == "MOV":
        new[op[2]] += new[op[1]]
        new[op[1]] = 0
    elif kind == "DEL":
        del new[op[1]]
    elif kind == "NEW":
        new[op[1]] = op[2]
    else:
        raise ValueError(f"unknown state operation {kind}")
    return new


def state_history(initial, operations):
    current, history = dict(initial), []
    for operation in operations:
        current = state_apply(current, operation)
        history.append(current)
    return history


def list_apply(old, op):
    new = list(old)
    kind = op[0]
    if kind == "APP":
        new.append(op[1])
    elif kind == "INS":
        new.insert(op[1], op[2])
    elif kind == "DEL":
        del new[op[1]]
    elif kind == "SET":
        new[op[1]] = op[2]
    elif kind == "MOV":
        item = new.pop(op[1])
        new.insert(op[2], item)
    elif kind == "SWP":
        new[op[1]], new[op[2]] = new[op[2]], new[op[1]]
    elif kind == "REV":
        left, right = op[1], op[2]
        new[left:right + 1] = reversed(new[left:right + 1])
    else:
        raise ValueError(f"unknown list operation {kind}")
    return new


def list_history(initial, operations):
    current, history = list(initial), []
    for operation in operations:
        current = list_apply(current, operation)
        history.append(current)
    return history


def allowed(rel, cell):
    if rel.endswith("round8-horizon/results.jsonl"):
        return ((cell.startswith("A-") and not cell.endswith("-ack"))
                or cell.startswith("B-") or cell.startswith("C-"))
    if rel.endswith("round9-replication/results-r9.jsonl"):
        return cell.startswith("A-") and not cell.endswith("-ack")
    if rel.endswith("round11-power/results-r11.jsonl"):
        return cell in ("A-CKPT4710", "A-CKPT710")
    if rel.endswith("round12-ladder/results-r12.jsonl"):
        return cell in {"A-INC", "A-CKPT4710", "A-CKPT710", "A-CKPT10", "A-MONO", "T-DENSE", "T-SPARSE"}
    return False


def class_of(raw):
    matches = list(FENCE.finditer(raw))
    if len(matches) > 1:
        return "MULTI"
    if matches:
        body = matches[0].group(1).strip()
        return "FJM" if "\n" in body or "\r" in body else "FJ1"
    return "DANGLE" if "```" in raw else "BARE"


def want_for(rel, row, state, seq):
    cell, pid, turn = row.get("cell", ""), row.get("pid"), row.get("turn")
    if rel.endswith("round8-horizon/results.jsonl"):
        if cell.startswith("C-"):
            return None
        if cell.startswith("B-"):
            states = state[pid][1]
            return states[-1] if states else None
        if cell.startswith("A-"):
            init, states = state[pid]
            idx = len(states) - 1 if cell == "A-MONO" else turn - 1
            return states[idx] if isinstance(idx, int) and 0 <= idx < len(states) else None
        return None
    if rel.endswith("round12-ladder/results-r12.jsonl") and cell in ("T-DENSE", "T-SPARSE"):
        init, states = seq[pid]
        return states[turn - 1] if isinstance(turn, int) and 1 <= turn <= len(states) else None
    init, states = state[pid]
    idx = len(states) - 1 if cell == "A-MONO" else turn - 1
    return states[idx] if isinstance(idx, int) and 0 <= idx < len(states) else None


def latin(square):
    symbols = {"A", "B", "C", "D"}
    if not isinstance(square, list) or len(square) != 4:
        return False
    if not all(isinstance(row, list) and len(row) == 4 and set(row) == symbols for row in square):
        return False
    return all({square[r][c] for r in range(4)} == symbols for c in range(4))


def c_grade(value, cell):
    if cell == "C-MONO":
        return latin(value)
    if not isinstance(value, dict):
        return False
    violations, square = value.get("violations"), value.get("square")
    if not isinstance(violations, list) or not isinstance(square, list):
        return False
    conflict = [["A", "B", "C", "D"], ["B", "C", "D", "A"], ["A", "B", "D", "C"]]
    benign = [["A", "B", "C", "D"], ["B", "A", "D", "C"], ["C", "D", "A", "B"]]
    prior = conflict if cell == "C-conflict" else benign
    with_rule = cell != "C-norule"
    symbols = {"A", "B", "C", "D"}
    if with_rule:
        square_ok = latin(square)
    else:
        square_ok = len(square) == 4 and all(isinstance(row, list) and set(row) == symbols for row in square)
    changed = set(violations)
    preserved = all(square[i] == prior[i] for i in range(3) if (i + 1) not in changed)
    remaining = [prior[i] for i in range(3) if (i + 1) not in changed]
    feasible = all(len({row[col] for row in remaining}) == len(remaining) for col in range(4)) if with_rule else True
    return square_ok and feasible and preserved


def verdict(row, value, expected):
    if row["cell"].startswith("C-"):
        return c_grade(value, row["cell"])
    if row.get("cell") in ("T-DENSE", "T-SPARSE"):
        return isinstance(value, list) and value == expected
    return isinstance(value, dict) and value == expected


def read_records():
    records, pins = [], {}
    for rel, expected_hash in FILES.items():
        path = ROOT / rel
        payload = path.read_bytes()
        actual_hash = hashlib.sha256(payload).hexdigest()
        if actual_hash != expected_hash:
            raise ValueError(f"pin mismatch {rel}: {actual_hash}")
        pins[rel] = {"actual": actual_hash, "expected": expected_hash, "match": True}
        rows = [json.loads(line) for line in payload.decode("utf-8").splitlines() if line.strip()]
        state_meta, seq_meta = {}, {}
        for row in rows:
            if row.get("cell") in ("meta", "meta2"):
                target = state_meta if row["cell"] == "meta" else seq_meta
                pid = row["pid"]
                if pid in target:
                    raise ValueError(f"duplicate metadata pid {rel} {row['cell']} {pid}")
                init, ops = row["init"], row["ops"]
                target[pid] = (init, state_history(init, ops) if row["cell"] == "meta" else list_history(init, ops))
        for lineno, row in enumerate(rows, 1):
            if "raw" not in row or "ok" not in row:
                continue
            if not isinstance(row["raw"], str) or type(row["ok"]) is not bool:
                raise ValueError(f"invalid raw/ok {rel}:{lineno}")
            if not allowed(rel, row.get("cell", "")):
                raise ValueError(f"ungraded raw/ok {rel}:{lineno} cell={row.get('cell')}")
            expected = want_for(rel, row, state_meta, seq_meta)
            if not row["cell"].startswith("C-"):
                if expected is None:
                    raise ValueError(f"missing rederived truth {rel}:{lineno}")
                if "want" in row and row["want"] != expected:
                    raise ValueError(f"want mismatch {rel}:{lineno}")
            records.append({"file": rel, "line": lineno, "row": row, "want": expected,
                            "format": class_of(row["raw"])})
    if len(records) != 1964:
        raise ValueError(f"population={len(records)} expected=1964")
    return records, pins


# Independent regularized incomplete beta and inverse, used for exact CP intervals.
def beta_fraction(a, b, x):
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-300:
        d = 1e-300
    d = 1.0 / d
    h = d
    for m in range(1, 1001):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-300:
            d = 1e-300
        c = 1.0 + aa / c
        if abs(c) < 1e-300:
            c = 1e-300
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-300:
            d = 1e-300
        c = 1.0 + aa / c
        if abs(c) < 1e-300:
            c = 1e-300
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-14:
            return h
    raise ArithmeticError("beta continued fraction did not converge")


def beta_cdf(x, a, b):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    factor = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                      + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return factor * beta_fraction(a, b, x) / a
    return 1.0 - factor * beta_fraction(b, a, 1.0 - x) / b


def beta_quantile(probability, a, b):
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2.0
        if beta_cdf(mid, a, b) < probability:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def cp95(successes, n):
    if successes == 0:
        lower = 0.0
    else:
        lower = beta_quantile(0.025, successes, n - successes + 1)
    if successes == n:
        upper = 1.0
    else:
        upper = beta_quantile(0.975, successes + 1, n - successes)
    return lower, upper


def rate(bucket):
    return bucket["pass"] / bucket["n"] if bucket["n"] else 0.0


def compute(records, pins):
    results = {pid: [] for pid in POLICY_IDS}
    tallies = {}
    for pid in POLICY_IDS:
        tallies[pid] = {"n": 0, "pass": 0, "agree": 0, "flip_pf": 0, "flip_fp": 0, "none": 0,
                        "strata": {fmt: {"n": 0, "agree": 0, "pass": 0} for fmt in FORMAT_CLASSES},
                        "files": {}, "cells": {}}
    for rec in records:
        row, raw, stored = rec["row"], rec["row"]["raw"], rec["row"]["ok"]
        for pid in POLICY_IDS:
            value = extract(pid, raw)
            ok = verdict(row, value, rec["want"])
            results[pid].append((value, ok))
            t = tallies[pid]
            t["n"] += 1
            t["pass"] += int(ok)
            t["agree"] += int(ok == stored)
            t["none"] += int(value is None)
            if ok != stored:
                t["flip_pf" if stored else "flip_fp"] += 1
            stratum = t["strata"][rec["format"]]
            stratum["n"] += 1
            stratum["agree"] += int(ok == stored)
            stratum["pass"] += int(ok)
            short = f"{Path(rec['file']).parent.name}/{Path(rec['file']).name}"
            file_bucket = t["files"].setdefault(rec["file"], {"n": 0, "pass": 0})
            cell_bucket = t["cells"].setdefault((short, row["cell"]), {"n": 0, "pass": 0})
            for bucket in (file_bucket, cell_bucket):
                bucket["n"] += 1
                bucket["pass"] += int(ok)
    base = tallies["E0"]
    if (base["n"], base["agree"]) != (1964, 1964):
        raise ValueError(f"E0 baseline {base['agree']}/{base['n']}")
    policies, strata, files, cells = [], {}, {}, {}
    for pid in POLICY_IDS:
        t = tallies[pid]
        lo, hi = cp95(t["agree"], t["n"])
        policies.append({"id": pid, "name": NAMES[pid], "n": t["n"], "agree": t["agree"],
                         "flip_pf": t["flip_pf"], "flip_fp": t["flip_fp"], "none": t["none"],
                         "pass": t["pass"], "pass_rate": rate(t),
                         "delta_pp": (rate(t) - rate(base)) * 100.0, "cp95_lo": lo, "cp95_hi": hi})
        strata[pid] = {fmt: dict(v, pass_rate=rate(v)) for fmt, v in t["strata"].items()}
        files[pid] = {key: dict(v, pass_rate=rate(v)) for key, v in t["files"].items()}
        cells[pid] = {f"{short}:{cell}": dict(v, pass_rate=rate(v))
                      for (short, cell), v in t["cells"].items()}
    order = sorted(tallies["E0"]["cells"], key=lambda k: (list(FILES).index(next(f for f in FILES if f.endswith(k[0].split("/", 1)[1]))), k[1]))
    cellshift = {}
    for pid in POLICY_IDS[1:]:
        best, bestkey = -1.0, None
        for key in order:
            yours = tallies[pid]["cells"].get(key)
            if yours is None:
                continue
            shift = abs(rate(yours) - rate(tallies["E0"]["cells"][key])) * 100.0
            if shift > best:
                best, bestkey = shift, key
        cellshift[pid] = {"max_abs_pp": max(best, 0.0), "cell": f"{bestkey[0]}:{bestkey[1]}" if bestkey else None}
    matrix = [[0] * len(POLICY_IDS) for _ in POLICY_IDS]
    for idx in range(len(records)):
        for i in range(len(POLICY_IDS)):
            for j in range(i + 1, len(POLICY_IDS)):
                if results[POLICY_IDS[i]][idx][1] != results[POLICY_IDS[j]][idx][1]:
                    matrix[i][j] += 1
                    matrix[j][i] += 1
    alternatives = POLICY_IDS[1:]
    total = {"population": len(records), "policies": len(alternatives),
             "compared_verdicts": sum(tallies[pid]["n"] for pid in alternatives),
             "disagreements": sum(tallies[pid]["flip_pf"] + tallies[pid]["flip_fp"] for pid in alternatives),
             "policies_with_flips": sum(bool(tallies[pid]["flip_pf"] + tallies[pid]["flip_fp"]) for pid in alternatives)}
    return {"root": str(ROOT), "population": len(records), "pins": pins, "defects": [],
            "policies": policies, "strata": strata, "files": files, "cells": cells,
            "cellshift": cellshift, "matrix": {"ids": POLICY_IDS, "rows": matrix},
            "total": total, "exit": 0}, results


def compare(a, b, path="root"):
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            return [f"{path}: keys {sorted(a)} != {sorted(b)}"]
        errors = []
        for key in a:
            errors.extend(compare(a[key], b[key], f"{path}.{key}"))
        return errors
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [f"{path}: length {len(a)} != {len(b)}"]
        return [e for i, (x, y) in enumerate(zip(a, b)) for e in compare(x, y, f"{path}[{i}]")]
    if type(a) in (int, float) and type(b) in (int, float):
        return [] if math.isclose(a, b, rel_tol=0.0, abs_tol=2e-10) else [f"{path}: {a!r} != {b!r}"]
    return [] if a == b else [f"{path}: {a!r} != {b!r}"]


def main():
    records, pins = read_records()
    independent, results = compute(records, pins)
    production_run = subprocess.run([sys.executable, str(ROOT / "plans/parser_policy_compare.py"),
                                     "--root", str(ROOT), "--json"], cwd=ROOT, text=True,
                                    capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    if production_run.returncode != 0:
        raise RuntimeError(f"production comparator exit={production_run.returncode}: {production_run.stderr}")
    production = json.loads(production_run.stdout)
    diffs = compare(independent, production, "result")
    if diffs:
        raise AssertionError("production JSON differs: " + "; ".join(diffs[:20]))
    oracle_run = subprocess.run([sys.executable, str(ROOT / "plans/fixtures/r27/policy_oracle.py"),
                                 "--root", str(ROOT)], cwd=ROOT, text=True, capture_output=True,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    if oracle_run.returncode != 0:
        raise RuntimeError(f"oracle exit={oracle_run.returncode}: {oracle_run.stderr}")
    oracle = {}
    for line in oracle_run.stdout.splitlines():
        match = re.fullmatch(r"POLICY (E\d) agree=(\d+) flip_pf=(\d+) flip_fp=(\d+) none=(\d+)", line)
        if match:
            oracle[match[1]] = {"agree": int(match[2]), "flip_pf": int(match[3]),
                                "flip_fp": int(match[4]), "none": int(match[5])}
    for policy in independent["policies"]:
        pid = policy["id"]
        wanted = {key: policy[key] for key in ("agree", "flip_pf", "flip_fp", "none")}
        if oracle.get(pid) != wanted:
            raise AssertionError(f"oracle mismatch {pid}: {oracle.get(pid)} != {wanted}")
    if set(oracle) != set(POLICY_IDS):
        raise AssertionError(f"oracle policy set mismatch {sorted(oracle)}")
    t = independent["total"]
    if any(p["flip_fp"] for p in independent["policies"]):
        raise AssertionError("found a FAIL-to-PASS flip")
    print(f"INDEPENDENT PASS population={len(records)} pins=4 E0={independent['policies'][0]['agree']}/1964 "
          f"compared={t['compared_verdicts']} disagreements={t['disagreements']} "
          f"policies_with_flips={t['policies_with_flips']} production_json=exact oracle=exact "
          f"strata={sum(len(v) for v in independent['strata'].values())} "
          f"files={sum(len(v) for v in independent['files'].values())} "
          f"cells={sum(len(v) for v in independent['cells'].values())} matrix=9x9 no_FP=9/9")
    for p in independent["policies"]:
        print(f"NUM {p['id']} {p['agree']}/{p['n']} PF={p['flip_pf']} FP={p['flip_fp']} none={p['none']} "
              f"pass={p['pass']} delta_pp={p['delta_pp']:+.2f} "
              f"CP95=[{p['cp95_lo']:.6f},{p['cp95_hi']:.6f}]")
    for pid in ("E1", "E3", "E7"):
        s = independent["strata"][pid]["MULTI"]
        print(f"MULTI {pid} {s['agree']}/{s['n']} pass={s['pass']}")
    print("E5_DROPS DANGLE=17 BARE=9 total=26; E5_none=145")
    for pid in ("E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"):
        s = independent["cellshift"][pid]
        print(f"CELL {pid} {s['max_abs_pp']:.2f}pp {s['cell']}")
    for pid in ("E0", "E1", "E4", "E5"):
        f = independent["files"][pid]
        print("FILES " + pid + " " + " ".join(
            f"{Path(k).parent.name}={v['pass']}/{v['n']}" for k, v in f.items()))


if __name__ == "__main__":
    main()
