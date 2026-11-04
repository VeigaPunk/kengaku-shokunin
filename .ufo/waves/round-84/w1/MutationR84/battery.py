#!/usr/bin/env python3
"""Run the Q1/Q21 mutation battery and write runs.txt and mutants.md.

Phases
  A  mkfixtures.py            build fixtures from the BASE entry bytes
  B  rules.py --selftest      instrument selftest (primitives)
  C  rules.py BASE            BASE must be red on q1 and q21 (sensitivity)
  D  rules.py <fixture>       one plain run and one --json run per fixture
  E  instrument mutant m8     rules_m8_always_true.py on BASE and on every
                              mutant: an always-true detector must be killed by
                              the BASE-sensitivity gate, not by a fixture.

Kill criterion (written down once, applied mechanically below)
  entry mutant is KILLED iff  observed failing set == expected failing set
                              and the exit code is 1 (0 for the green fixtures)
                              and the fixture bytes differ from `repaired`
  it SURVIVED iff            an expected rule did not fire
  it OVERFIRED iff           KILLED plus an unexpected rule also fired
  m8 (instrument mutant) is KILLED iff  it reports BASE green, i.e. the
                              BASE-sensitivity gate sees it (C2's kill rule:
                              "a base-insensitive check" fails the claim)
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import platform
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
RULES = HERE / "rules.py"
RULES_M8 = HERE / "rules_m8_always_true.py"
MK = HERE / "mkfixtures.py"
BASE = HERE / "entry-base.md"
FIXTURES = HERE / "fixtures"
PREAMBLE = HERE / "mutants-preamble.md"
RUNS = HERE / "runs.txt"
MUTANTS_MD = HERE / "mutants.md"

RULES_IDS = ("q1", "q21")
ORDER = ("q1", "q21")


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        argv,
        cwd=str(HERE),
        capture_output=True,
        text=True,
        env=None,
    )
    text = proc.stdout
    if proc.stderr:
        text += ("\n" if text and not text.endswith("\n") else "") + proc.stderr
    return proc.returncode, text.rstrip("\n")


def show(argv: list[str]) -> str:
    """argv as a reader can retype it from this directory."""
    parts = []
    for item in argv:
        path = pathlib.Path(item)
        try:
            parts.append(str(path.resolve().relative_to(HERE)))
        except ValueError:
            parts.append(item)
    return " ".join(parts)


class Transcript:
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.entries: list[dict[str, object]] = []

    def section(self, number: str, title: str, argv: list[str], code: int, out: str) -> None:
        self.lines.append(f"=== [{number}] {title}")
        self.lines.append(f"$ {show(argv)}")
        if out:
            self.lines.extend(out.splitlines())
        self.lines.append(f"EXIT={code}")
        self.lines.append("")
        self.entries.append({"section": number, "title": title, "argv": show(argv), "exit": code})


def observed_label(result: dict[str, object]) -> str:
    bits = []
    for rule in ORDER:
        block = result[rule]
        if block["pass"]:
            bits.append(f"{rule}=pass")
        else:
            if rule == "q1":
                spans = [s for s in ("order", "timing", "action") if not block[s]]
                bits.append(f"q1=fail[{'|'.join(spans)}]")
            else:
                bits.append("q21=fail")
    return " ".join(bits)


def observed_set(result: dict[str, object]) -> set[str]:
    return {rule for rule in ORDER if not result[rule]["pass"]}


def main() -> int:
    tx = Transcript()

    # phase A: fixtures ---------------------------------------------------
    code, out = run([sys.executable, str(MK)])
    tx.section("A", "build fixtures from BASE bytes", [sys.executable, str(MK)], code, out)
    if code != 0:
        RUNS.write_text("\n".join(tx.lines), encoding="utf-8")
        print("mkfixtures failed; see runs.txt", file=sys.stderr)
        return 2
    manifest = json.loads((FIXTURES / "fixtures.json").read_text(encoding="utf-8"))

    # phase B: instrument selftest ---------------------------------------
    code, out = run([sys.executable, str(RULES), "--selftest"])
    tx.section("B", "instrument selftest", [sys.executable, str(RULES), "--selftest"], code, out)
    selftest_exit = code
    selftest_out = out

    # phase C: BASE sensitivity ------------------------------------------
    code, out = run([sys.executable, str(RULES), str(BASE)])
    tx.section("C", "BASE bytes (must be red on q1 and q21)", [sys.executable, str(RULES), str(BASE)], code, out)
    base_plain = (code, out)
    code, out = run([sys.executable, str(RULES), "--json", str(BASE)])
    tx.section("C2", "BASE bytes, machine view", [sys.executable, str(RULES), "--json", str(BASE)], code, out)
    base = json.loads(out)
    base_exit = code

    # phase D: fixtures --------------------------------------------------
    results: dict[str, dict[str, object]] = {}
    exits: dict[str, int] = {}
    json_exits: dict[str, int] = {}
    for index, fixture_id in enumerate(manifest["fixtures"], start=1):
        path = FIXTURES / f"{fixture_id}.md"
        label = f"D{index:02d}"
        code, out = run([sys.executable, str(RULES), str(path)])
        tx.section(label, f"fixture {fixture_id}", [sys.executable, str(RULES), str(path)], code, out)
        exits[fixture_id] = code
        code, out = run([sys.executable, str(RULES), "--json", str(path)])
        tx.section(label + "j", f"fixture {fixture_id}, machine view", [sys.executable, str(RULES), "--json", str(path)], code, out)
        json_exits[fixture_id] = code
        parsed = json.loads(out)
        if parsed["sha256"] != manifest["fixtures"][fixture_id]["sha256"]:
            print(f"fixture hash mismatch for {fixture_id}", file=sys.stderr)
            return 2
        results[fixture_id] = parsed

    # phase E: instrument mutant m8 --------------------------------------
    code, out = run([sys.executable, str(RULES_M8), str(BASE)])
    tx.section("E1", "instrument mutant m8 (always-true) on BASE", [sys.executable, str(RULES_M8), str(BASE)], code, out)
    m8_base_exit = code
    m8_base_green = code == 0
    code, out = run([sys.executable, str(RULES_M8), "--json", str(BASE)])
    tx.section("E2", "instrument mutant m8 on BASE, machine view", [sys.executable, str(RULES_M8), "--json", str(BASE)], code, out)
    m8_base = json.loads(out)

    m8_survivors: list[str] = []
    m8_rows: list[tuple[str, str]] = []
    for index, fixture_id in enumerate(manifest["fixtures"], start=1):
        path = FIXTURES / f"{fixture_id}.md"
        code, out = run([sys.executable, str(RULES_M8), "--json", str(path)])
        tx.section(
            f"E3-{index:02d}",
            f"instrument mutant m8 on {fixture_id}",
            [sys.executable, str(RULES_M8), "--json", str(path)],
            code,
            out,
        )
        parsed = json.loads(out)
        observed = observed_set(parsed)
        m8_rows.append(
            (
                fixture_id,
                "green (no defect detected)" if not observed else f"detected {sorted(observed)}",
            )
        )
        if fixture_id.startswith("m") and not observed:
            m8_survivors.append(fixture_id)
    tx.section(
        "E4",
        "instrument mutant m8 summary: fixtures it fails to flag",
        [sys.executable, str(RULES_M8), "--json", "fixtures/<id>.md (one run per fixture, above)"],
        0,
        "\n".join(f"{fid:9s} {verdict}" for fid, verdict in m8_rows),
    )

    # phase F: the mutation is local ------------------------------------
    base_lines = BASE.read_text(encoding="utf-8").splitlines()
    body_rows: list[str] = []
    body_ok = True
    for fixture_id in manifest["fixtures"]:
        lines = (FIXTURES / f"{fixture_id}.md").read_text(encoding="utf-8").splitlines()
        start = 4 if fixture_id == "m4" else 3
        same = lines[start:] == base_lines[3:]
        body_ok = body_ok and same
        body_rows.append(
            f"{fixture_id:9s} body_lines_from={start} identical_to_BASE={same}"
        )
    tx.section(
        "F",
        "body invariant: every fixture differs from BASE only in its header lines",
        [sys.executable, "battery.py"],
        0 if body_ok else 1,
        "\n".join(body_rows),
    )

    # verdicts -----------------------------------------------------------
    verdicts: dict[str, dict[str, object]] = {}
    for fixture_id, meta in manifest["fixtures"].items():
        result = results[fixture_id]
        expected = set(meta["expected_failing_rules"])
        observed = observed_set(result)
        missed = sorted(expected - observed)
        extra = sorted(observed - expected)
        want_exit = 0 if not expected else 1
        same_bytes_as_repaired = (
            result["sha256"] == manifest["fixtures"]["repaired"]["sha256"]
            and fixture_id != "repaired"
        )
        if missed:
            verdict = "SURVIVED"
        elif extra:
            verdict = "KILLED + OVERFIRE"
        else:
            verdict = "KILLED" if expected else "GREEN AS REQUIRED"
        if not expected and observed:
            verdict = "WRONGLY RED"
        note = ""
        if exits[fixture_id] != want_exit or json_exits[fixture_id] != want_exit:
            note = f"exit {exits[fixture_id]}/{json_exits[fixture_id]} want {want_exit}"
            verdict = "EXIT MISMATCH"
        if same_bytes_as_repaired:
            note = (note + "; " if note else "") + "bytes identical to repaired (no mutation applied)"
            verdict = "NO-OP MUTANT"
        verdicts[fixture_id] = {
            "expected": sorted(expected),
            "observed": sorted(observed),
            "label": observed_label(result),
            "verdict": verdict,
            "note": note,
            "exit": exits[fixture_id],
        }

    mutants = [fid for fid in manifest["fixtures"] if fid.startswith("m")]
    mutants.sort(key=lambda fid: int(fid[1:]))
    controls = [
        fid for fid in manifest["fixtures"] if fid not in mutants and fid != "repaired"
    ]
    killed = [fid for fid in mutants if verdicts[fid]["verdict"].startswith("KILLED")]
    survived = [fid for fid in mutants if not verdicts[fid]["verdict"].startswith("KILLED")]
    # m8 is an always-true detector: it reports BASE green (m8_base_green) and
    # flags none of the mutant fixtures.  Killed iff the BASE-sensitivity gate,
    # i.e. C2's "base-insensitive check" kill rule, detects it.
    m8_killed = bool(m8_base_green) and bool(m8_survivors)
    killed_total = len(killed) + (1 if m8_killed else 0)

    total = len(mutants) + 1

    # runs.txt -----------------------------------------------------------
    header = [
        "# R84 w1 seat MutationR84 — Q1/Q21 admission-rule mutation battery, raw transcripts",
        "# host: " + platform.platform(),
        "# python: " + sys.version.replace("\n", " "),
        "# cwd for every run: " + str(HERE),
        "# input entry: entry-base.md sha256 " + sha256(BASE),
        "#   extracted from rev 4087b2f8369fb0c317a8460725a607681ff2fd7f "
        "corpus/knowledge/tb2-code-from-image-offline.md",
        "# instrument: rules.py sha256 " + sha256(RULES),
        "# instrument mutant: rules_m8_always_true.py sha256 " + sha256(RULES_M8),
        "# fixture builder: mkfixtures.py sha256 " + sha256(MK),
        "# exit-code convention: 0 no defect, 1 defect(s), 2 could-not-evaluate",
        "",
        "# Identities:",
        "#   BASE          entry-base.md (frozen BASE bytes)",
        "#   repaired      green baseline fixture (date + command + pin)",
        "#   m1..m7        entry mutants",
        "#   P1,N1..N5     controls (one positive branch probe, five negatives)",
        "#   m8            instrument mutant: rules_m8_always_true.py",
        "",
    ]
    summary = ["# KILL SUMMARY (mechanically derived from the runs above)", ""]
    summary.append(f"{'id':10s} {'expected':12s} {'observed':22s} {'exit':4s} verdict")
    for fixture_id in ["repaired"] + mutants + controls:
        v = verdicts[fixture_id]
        summary.append(
            f"{fixture_id:10s} {str(v['expected']):12s} {str(v['observed']):22s} "
            f"{v['exit']:<4d} {v['verdict']}"
            + (f" ({v['note']})" if v["note"] else "")
        )
    summary.append(
        f"{'m8':10s} {'BASE green?':12s} {'yes' if m8_base_green else 'no':22s} "
        f"{m8_base_exit:<4d} {'KILLED (base-insensitive instrument)' if m8_killed else 'SURVIVED'}"
    )
    summary.append("")
    summary.append(f"killed={killed_total} of {total}")
    summary.append(f"body invariant (mutation confined to header lines): {'ok' if body_ok else 'VIOLATED'}")
    summary.append(f"entry mutants killed: {len(killed)}/{len(mutants)} {killed}")
    summary.append(
        "controls as required: "
        + f"{sum(1 for c in controls if verdicts[c]['verdict'] in ('KILLED', 'GREEN AS REQUIRED'))}/{len(controls)}"
    )
    summary.append(f"m8 survivors (mutant fixtures it fails to flag): {len(m8_survivors)} {m8_survivors}")
    summary.append(f"selftest: {selftest_out.splitlines()[-2] if selftest_out else 'absent'}, exit {selftest_exit}")
    summary.append(f"BASE: {observed_label(base)} exit {base_exit}")
    summary.append(
        "BASE signature vs frozen C2: q1="
        + str(0 if base["q1"]["pass"] else 1)
        + " q21="
        + str(0 if base["q21"]["pass"] else 1)
        + " (frozen target before-values: q1=1 q21=1; q13 is the L1 counter's third rule, out of this seat)"
    )
    RUNS.write_text("\n".join(header + tx.lines + summary) + "\n", encoding="utf-8")

    # mutants.md ---------------------------------------------------------
    preamble = PREAMBLE.read_text(encoding="utf-8").rstrip("\n")
    doc = [preamble, "", "## Measured kill table", ""]
    doc.append("| id | mutation of the entry bytes | rule(s) that should fire | rules.py reports | exit | verdict |")
    doc.append("|---|---|---|---|---|---|")
    order = ["repaired"] + mutants + controls
    for fixture_id in order:
        meta = manifest["fixtures"][fixture_id]
        v = verdicts[fixture_id]
        expected = ", ".join(f"`{r}`" for r in v["expected"]) or "none"
        doc.append(
            f"| `{fixture_id}` | {meta['purpose']} | {expected} | `{v['label']}` | {v['exit']} | **{v['verdict']}**"
            + (f" — {v['note']}" if v["note"] else "")
            + " |"
        )
    doc.append(
        f"| `m8` | instrument mutant: every Q1/Q21 predicate replaced by always-true "
        f"(`rules_m8_always_true.py`) | BASE must stay red | BASE reported `{observed_label(m8_base)}`, "
        f"pristine `{observed_label(base)}` | "
        f"{m8_base_exit} | **{'KILLED (base-sensitivity gate)' if m8_killed else 'SURVIVED'}** |"
    )
    doc.append("")
    doc.append(f"`killed={killed_total} of {total}` (entry mutants {len(killed)}/{len(mutants)}, instrument mutant included).")
    doc.append("")
    doc.append(
        "Body invariant: every fixture's lines after its header are byte-identical to BASE "
        f"({'ok' if body_ok else 'VIOLATED'}), so each row prices one header edit and nothing else."
    )
    doc.append("")
    doc.append("## Full rule reasons per fixture")
    doc.append("")
    doc.append("| id | Q1 (`why`) | Q1 spans | Q21 (`why`) |")
    doc.append("|---|---|---|---|")
    for fixture_id in order:
        result = results[fixture_id]
        q1 = result["q1"]
        q21 = result["q21"]
        spans = " ".join(
            f"{span}={'ok' if q1[span] else 'bad'}" for span in ("order", "timing", "action")
        )
        doc.append(f"| `{fixture_id}` | {q1['why']} | {spans} | {q21['why']} |")
    doc.append("")
    doc.append("BASE under the instrument:")
    doc.append("")
    doc.append("```")
    doc.append(base_plain[1])
    doc.append("```")
    doc.append("")
    doc.append("## Exact mutant header bytes")
    doc.append("")
    doc.append("Lines 1-4 of each fixture as generated (body lines 5+ are byte-identical to BASE).")
    doc.append("")
    for fixture_id in order:
        header_lines = manifest["fixtures"][fixture_id]["header"]
        doc.append(f"`{fixture_id}` — sha256 `{manifest['fixtures'][fixture_id]['sha256']}`")
        doc.append("")
        doc.append("```")
        for index, line in enumerate(header_lines, start=1):
            doc.append(f"{index}| {line}" if line else f"{index}|")
        doc.append("```")
        doc.append("")
    doc.append("## Survivors and rule gaps")
    doc.append("")
    if survived:
        doc.append("Entry mutants that survived (a rule did not fire when it should):")
        doc.append("")
        for fixture_id in survived:
            v = verdicts[fixture_id]
            doc.append(
                f"- `{fixture_id}` — expected `{v['expected']}`, observed `{v['observed']}`; "
                f"minimal example: `{manifest['fixtures'][fixture_id]['header'][2]}`"
            )
        doc.append("")
    else:
        doc.append(
            f"No entry mutant survived: {len(killed)}/{len(mutants)} killed, and the instrument "
            "mutant m8 is killed by the BASE-sensitivity gate."
        )
        doc.append("")
    doc.append(
        f"The always-true instrument (m8) flags none of the {len(m8_survivors)} mutant fixtures green, "
        f"i.e. it lets every entry mutant through: {', '.join('`' + s + '`' for s in m8_survivors)}."
    )
    doc.append("")
    doc.append(
        "That is why the kill rule is anchored to BASE being red: without the sensitivity gate, "
        "m8 would be an unkillable detector that reports a clean admission bar for every entry."
    )
    doc.append("")
    doc.append("## Transcripts")
    doc.append("")
    doc.append(
        "`runs.txt` holds every command, its full output and its exit code "
        f"({len(tx.entries)} invocations), plus the mechanically derived kill summary. "
        "Fixture construction is scripted in `mkfixtures.py`; `fixtures/fixtures.json` "
        "pins every fixture sha256 and its expected failing rules."
    )
    MUTANTS_MD.write_text("\n".join(doc) + "\n", encoding="utf-8")

    print(f"runs.txt: {RUNS}")
    print(f"mutants.md: {MUTANTS_MD}")
    print(f"killed={killed_total} of {total}; entry mutants {len(killed)}/{len(mutants)}; survived={survived}")
    print(f"m8 killed={m8_killed} (base green under mutant={m8_base_green}, survivors={len(m8_survivors)})")
    print(f"selftest exit={selftest_exit}; base exit={base_exit} {observed_label(base)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
