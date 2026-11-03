#!/usr/bin/env python3
"""Build R67-C1 receipt mutants from the committed receipt copy, one change each.

Every mutant dir holds receipt.txt (mutated) + receipt.junit/ (byte copy of base,
minus one file for the junit-deletion mutant). The script asserts that a text
mutant differs from base on exactly one line, and records sha256s + diffs.
"""
import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "base"
MUT = ROOT / "mut"
ZERO = "0" * 64


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


base_lines = (BASE / "receipt.txt").read_text().splitlines()


def idx_of(prefix: str) -> int:
    hits = [i for i, l in enumerate(base_lines) if l.startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f"prefix {prefix!r} matched {len(hits)} lines")
    return hits[0]


def set_field(line: str, field: str, value: str) -> str:
    parts = line.split(" ")
    out = []
    seen = 0
    for p in parts:
        if p.startswith(field + "="):
            out.append(f"{field}={value}")
            seen += 1
        else:
            out.append(p)
    if seen != 1:
        raise SystemExit(f"field {field} appears {seen}x in {line!r}")
    return " ".join(out)


def m_flip_vector(lines):
    i = idx_of("VECTOR q1-ref ")
    lines[i] = lines[i].replace("exists=P", "exists=F", 1)
    return lines


def m_drop_vector(lines):
    i = idx_of("VECTOR q3-stub ")
    del lines[i]
    return lines


def m_drop_case(lines):
    i = idx_of("CASE q4-hooks-noop ")
    del lines[i]
    return lines


def m_case_sha(lines):
    i = idx_of("CASE q1-ref ")
    lines[i] = set_field(lines[i], "case_sha256", ZERO)
    return lines


def m_junit_sha(lines):
    i = idx_of("CASE q6-unscaled-loss ")
    lines[i] = set_field(lines[i], "junit_sha256", ZERO)
    return lines


def m_probe_sha(lines):
    i = idx_of("PROBE ")
    lines[i] = set_field(lines[i], "sha256", ZERO)
    return lines


def m_probe_version(lines):
    i = idx_of("PROBE ")
    lines[i] = set_field(lines[i], "version", "r67-c1/9")
    return lines


def m_grader_sha(lines):
    i = idx_of("GRADER ")
    lines[i] = set_field(lines[i], "sha256", ZERO)
    return lines


def m_q5_pppp(lines):
    i = idx_of("VECTOR q5-full-model ")
    lines[i] = lines[i].replace("ws2=F", "ws2=P", 1)
    return lines


def m_rc_tamper(lines):
    i = idx_of("CASE q4-hooks-noop ")
    lines[i] = set_field(lines[i], "rc", "7")
    return lines


def m_frozen_flag(lines):
    i = idx_of("VECTOR q4-hooks-noop ")
    lines[i] = lines[i].replace("frozen=match", "frozen=mismatch", 1)
    return lines


MUTANTS = [
    ("m01-flip-vector-q1-exists", "VECTOR q1-ref exists P->F", m_flip_vector, None),
    ("m02-drop-vector-q3-stub", "delete the VECTOR line for q3-stub", m_drop_vector, None),
    ("m03-drop-case-q4-hooks-noop", "delete the CASE line for q4-hooks-noop", m_drop_case, None),
    ("m04-case-sha-q1-zeroed", "CASE q1-ref case_sha256 -> 64 zeros", m_case_sha, None),
    ("m05-junit-sha-q6-zeroed", "CASE q6-unscaled-loss junit_sha256 -> 64 zeros", m_junit_sha, None),
    ("m06-probe-sha-zeroed", "PROBE sha256 -> 64 zeros", m_probe_sha, None),
    ("m07-probe-version-token", "PROBE version r67-c1/1 -> r67-c1/9", m_probe_version, None),
    ("m08-grader-sha-zeroed", "GRADER sha256 -> 64 zeros", m_grader_sha, None),
    ("m09-q5-vector-pppp", "VECTOR q5-full-model ws2 F->P (row PPPP)", m_q5_pppp, None),
    ("m10-drop-junit-q3-stub", "delete receipt.junit/q3-stub.xml", None, "q3-stub.xml"),
    ("m11-rc-tamper-q4", "CASE q4-hooks-noop rc=1 -> rc=7 (extra)", m_rc_tamper, None),
    ("m12-frozen-flag-q4", "VECTOR q4-hooks-noop frozen=match -> frozen=mismatch (extra)", m_frozen_flag, None),
]

shutil.rmtree(MUT, ignore_errors=True)
MUT.mkdir(parents=True)

manifest = []
for name, desc, fn, drop_junit in MUTANTS:
    d = MUT / name
    d.mkdir()
    if fn is not None:
        lines = fn(list(base_lines))
        (d / "receipt.txt").write_text("\n".join(lines) + "\n")
        diff = f"--- base/receipt.txt\n+++ {name}/receipt.txt\n"
        if len(lines) == len(base_lines) - 1:
            removed = list(base_lines)
            for l in lines:
                removed.remove(l)
            if len(removed) != 1:
                raise SystemExit(f"{name}: removal ambiguous {removed}")
            if [l for l in base_lines if l != removed[0]] != lines:
                raise SystemExit(f"{name}: more than one line removed")
            diff += f"- {removed[0]}\n"
        else:
            changed = [i for i, (a, b) in enumerate(zip(base_lines, lines)) if a != b]
            if len(lines) != len(base_lines) or len(changed) != 1:
                raise SystemExit(f"{name}: {len(changed)} lines changed, len {len(lines)}")
            i = changed[0]
            diff += f"- {base_lines[i]}\n+ {lines[i]}\n"
    else:
        shutil.copyfile(BASE / "receipt.txt", d / "receipt.txt")
        diff = f"--- base/receipt.txt\n+++ {name}/receipt.txt\n (receipt bytes identical)\n"
    shutil.copytree(BASE / "receipt.junit", d / "receipt.junit")
    if drop_junit:
        (d / "receipt.junit" / drop_junit).unlink()
        diff += f"- receipt.junit/{drop_junit}\n"
    (d / "diff.txt").write_text(diff)
    manifest.append(
        f"{name}\t{d}/receipt.txt\tsha256={(sha(d / 'receipt.txt'))}\tdesc={desc}"
    )

(ROOT / "manifest.tsv").write_text("\n".join(manifest) + "\n")
print("\n".join(manifest))
print(f"mutants={len(MUTANTS)}")
