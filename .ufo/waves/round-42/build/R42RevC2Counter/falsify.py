"""V9 falsifier: import plans/round42_c2_verify.py and call v9() against crafted lanes.
Each scenario builds a minimal lane (spec at pinned digest, receipt, entry, PROVINCE.md, corpus/README.md)
and reports v9's verdict. Ground truth: the lane's frozen receipt bytes."""
import importlib.util
import pathlib
import re
import shutil
import sys

CLONE = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/R42RevC2Counter/lane")
OUT = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/R42RevC2Counter/fals")

spec_src = CLONE / "plans/round42_c2_verify.py"
spec_mod = importlib.util.spec_from_file_location("c2r42", spec_src)
c2 = importlib.util.module_from_spec(spec_mod)
spec_mod.loader.exec_module(c2)

RECEIPT = (CLONE / "corpus/evidence/round42/fibsqrt-probe.txt").read_text()
SPEC_BYTES = (CLONE / "plans/pkg-spec-r42.json").read_bytes()

CASE_RE = re.compile(
    r"^CASE (\S+) predicted=(?:pass|fail) observed=(pass|fail) tests=([PF]{3}) (.*?)(?: -- (.*))?$"
)


def parse(text):
    out = []
    for l in text.splitlines():
        m = CASE_RE.match(l)
        if m:
            out.append({"cid": m.group(1), "obs": m.group(2), "tests": m.group(3), "text": m.group(5) or ""})
    return out


BASE_CASES = parse(RECEIPT)
assert len(BASE_CASES) == 16, len(BASE_CASES)


def table(cases):
    rows = "\n".join(f"| `{c['cid']}` | {c['tests']} | {c['obs']} | {c['text']} |" for c in cases)
    return (
        "## Case table\n\n"
        "| case | tests | observed | note |\n| --- | --- | --- | --- |\n" + rows + "\n"
    )


def build(tag, receipt_text, entry, province=None, frontier="the task `circuit-fibsqrt` is next door"):
    d = OUT / tag
    if d.exists():
        shutil.rmtree(d)
    (d / "plans").mkdir(parents=True)
    (d / "plans/pkg-spec-r42.json").write_bytes(SPEC_BYTES)
    (d / "corpus/evidence/round42").mkdir(parents=True)
    (d / "corpus/evidence/round42/fibsqrt-probe.txt").write_text(receipt_text)
    (d / "corpus/knowledge").mkdir(parents=True)
    (d / "corpus/knowledge/tb2-circuit-fibsqrt-grader.md").write_text(entry)
    (d / "PROVINCE.md").write_text(
        province or "round 42 adds `circuit-fibsqrt` as `corpus/knowledge/tb2-circuit-fibsqrt-grader.md`.\n"
    )
    (d / "corpus").mkdir(parents=True, exist_ok=True)
    (d / "corpus/README.md").write_text("# corpus\n\n## Frontier\n\n" + frontier + "\n")
    return d


PROSE = (
    "row ids outside the source line: S125, S126, S127 are pinned in SOURCES.\n\n"
)


def entry_with(case_section, prose=PROSE, extra=""):
    return (
        "source: S125 — https://example.com/test_outputs.py\n"
        "source: S126 — https://example.com/instruction.md\n"
        "source: S127 — https://example.com/sim.c\n\n"
        "# tb2 circuit-fibsqrt grader\n\n## Summary\n\n" + prose + extra + case_section
    )


results = []


def run(tag, d, expect):
    ok, note = c2.v9(d)
    verdict = "ok" if ok else "DEFECT"
    match = "MATCH" if verdict == expect else "SURPRISE"
    results.append((tag, expect, verdict, match, note))
    print(f"{tag:22s} expect={expect:6s} got={verdict:6s} {match}  {note}")


# A honest baseline
run("A-honest", build("A", RECEIPT, entry_with(table(BASE_CASES))), "ok")

# B text cell lies about what the case showed (receipt: nop observed=fail)
lie = [dict(c) for c in BASE_CASES]
lie[0]["text"] = "prints correct answers for every graded input"
run("B-textlie", build("B", RECEIPT, entry_with(table(lie))), "ok")

# D extra bogus row appended
extra_row = BASE_CASES + [{"cid": "z-invented", "tests": "PPP", "obs": "pass", "text": "invented"}]
run("D-extrarow", build("D", RECEIPT, entry_with(table(extra_row))), "DEFECT")

# E permuted row order
perm = [BASE_CASES[i] for i in [1, 0] + list(range(2, 16))]
run("E-permuted", build("E", RECEIPT, entry_with(table(perm))), "DEFECT")

# F tests letters flipped
flip_t = [dict(c) for c in BASE_CASES]
flip_t[2]["tests"] = "PPP"
run("F-letters", build("F", RECEIPT, entry_with(table(flip_t))), "DEFECT")

# G observed verdict flipped
flip_o = [dict(c) for c in BASE_CASES]
flip_o[1]["obs"] = "fail"
run("G-observed", build("G", RECEIPT, entry_with(table(flip_o))), "DEFECT")

# H ids only inside a blockquote line (not a source: line)
run("H-quote-id", build("H", RECEIPT, entry_with(table(BASE_CASES), prose="> quoted: S125 S126 S127\n")), "ok")

# I ids only as substrings of longer tokens
run("I-substring", build("I", RECEIPT, entry_with(table(BASE_CASES), prose="see S1250 and S1260 and S1270.\n")), "ok")

# J second divergent Case table section (first wins)
second = table([dict(c) for c in BASE_CASES[:3]] + [{"cid": "x", "tests": "FFF", "obs": "fail", "text": "bogus"}])
run("J-second-table", build("J", RECEIPT, entry_with(table(BASE_CASES), extra="\n" + second)), "ok")

# K PROVINCE line names only the entry file name (which embeds the task name)
run("K-province-file", build("K", RECEIPT, entry_with(table(BASE_CASES)),
                             province="see corpus/knowledge/tb2-circuit-fibsqrt-grader.md for details.\n"), "ok")

# P fabricated receipt + agreeing entry (observed flipped for two cases, entry mirrors it)
fabricated = RECEIPT.replace(
    "CASE nop predicted=fail observed=fail tests=PPF",
    "CASE nop predicted=fail observed=pass tests=PPP",
).replace(
    "CASE oracle-solve-sh predicted=pass observed=pass tests=PPP",
    "CASE oracle-solve-sh predicted=pass observed=fail tests=PPF",
)
fab_cases = parse(fabricated)
assert len(fab_cases) == 16
run("P-fabricated", build("P", fabricated, entry_with(table(fab_cases))), "ok")

# N CRLF entry (heading `## Case table\r\n`)
crlf = entry_with(table(BASE_CASES)).replace("## Case table\n", "## Case table\r\n")
run("N-crlf", build("N", RECEIPT, crlf), "DEFECT")

# O uppercase case id in one entry row
up = [dict(c) for c in BASE_CASES]
up[0]["cid"] = "NOP"
run("O-uppercase", build("O", RECEIPT, entry_with(table(up))), "DEFECT")

# Q ids only on `source-note:` lines (startswith('source:') does not exclude them)
run("Q-source-note", build("Q", RECEIPT, entry_with(table(BASE_CASES),
    prose="source-note: S125 S126 S127 pinned in SOURCES.\n")), "ok")

# R heading spelled `## case table` (lowercase)
low = entry_with(table(BASE_CASES)).replace("## Case table", "## case table")
run("R-lowercase", build("R", RECEIPT, low), "DEFECT")

# T rows missing the trailing pipe (not matched, count drops)
notrail = table(BASE_CASES).replace(" | nop".join([""] * 1), " nop", 1)
notrail_cases = [dict(c) for c in BASE_CASES]
rows_nt = "\n".join(
    (f"| `{c['cid']}` | {c['tests']} | {c['obs']} | {c['text']} |" if c["cid"] != "nop"
     else f"| `{c['cid']}` | {c['tests']} | {c['obs']} | {c['text']}") for c in notrail_cases
)
nt = "## Case table\n\n| case | tests | observed | note |\n| --- | --- | --- | --- |\n" + rows_nt + "\n"
run("T-notrail", build("T", RECEIPT, entry_with(nt)), "DEFECT")

print()
surprises = [r for r in results if r[3] == "SURPRISE"]
print(f"scenarios={len(results)} surprises={len(surprises)}")
sys.exit(0)
