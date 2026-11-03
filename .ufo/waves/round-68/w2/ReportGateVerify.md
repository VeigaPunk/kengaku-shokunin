# ReportGateVerify — w2 seat report: A2 report-contract gate verification (round 68 attempt 2)

Date: 2026-11-03. Scope: verify `plans/round68_report_contract.py` against the frozen
predicate in `plans/round-68-claims.md` Amendment A2 item 3 (read-only on L; receipts in
`.ufo/waves/round-68/w2/ReportGateVerify/`; scratch `/fast/scratch/hyaku/kengaku-r68/ReportGateVerify/`,
deleted before this seat yielded). No edits to any lane file; no git/jj write commands; no tools
installed (none needed; pacman untouched per the host-wide pause).

## Provenance (receipt `provenance.txt`, captured 20:30:49-03:00)

- gate sha256 `18fbfc2111d747ae9f40220333f0bbd56062c89e93bcd7c2477358228a0723f4` (`plans/round68_report_contract.py`, 244 lines)
- red fixture sha256 `0399cd5376d27e1c006075929a9b3511c820fc326b4a3751a4cd9b78b8573839` (`.ufo/waves/round-68/w2/report-fixtures/attempt1-report.md`, 12415 bytes, pre-existing)
- `SHONEN.md` sha256 `e65634a0aa51362734c380db033a363535aa1f4433c5b3578269f00ac147d8a1` (4 box lines)
- lane HEAD moved during the seat: `7803bdd4` (first read, 20:29) → `27f649f874ae96d7cf7f4f3e6ea4d0810f0d2f91` == origin/master (20:30:49); the w2 landing was in flight. Both `git status --porcelain` snapshots show a clean tracked tree — only untracked `.ufo/waves/round-68/w2*` sibling files. All shas above were taken against `27f649f8`.
- Python 3.14.8 (`/usr/bin/python3`), as frozen.

## Runs (cwd = L for every gate invocation; `rc` captured in-runner as `echo "rc=$?"`)

| # | command (abbreviated path tail) | receipt | expected | measured | verdict |
|---|---|---|---|---|---|
| 1 | `python3 plans/round68_report_contract.py .ufo/waves/round-68/w2/report-fixtures/attempt1-report.md --shonen SHONEN.md` | `red-attempt1.txt` | `PREDICATE R68-A2 fail`, rc 1, S1+S2+S3 defects | identical | PASS |
| 2 | `python3 plans/round68_report_contract.py --selftest --work /fast/scratch/hyaku/kengaku-r68/ReportGateVerify/a2` | `selftest.txt` | `SELFTEST n=5 red-refused=4 green-ok=1`, rc 0 | identical | PASS |
| 3 | `python3 plans/round68_report_contract.py /fast/scratch/hyaku/kengaku-r68/ReportGateVerify/green/report.md --shonen SHONEN.md` | `green.txt` (+ `green-report-fixture.md`) | `PREDICATE R68-A2 pass`, rc 0 | identical (`DEFECTS n=0`) | PASS |
| 4a | variant a1: report argument omitted | `edge-a-missing-path.txt` | rc 2 | rc 2, `usage: …` on **stderr**, **no `SETUP` token** (gate main:222-224) | PASS with nuance (below) |
| 4b | variant a2: report path does not exist | `edge-a-missing-path.txt` | rc 2 with `SETUP` | `SETUP could-not-evaluate [Errno 2] …`, rc 2 (main:229-231) | PASS |
| 5 | duplicate `## SHONEN` section (green + appended second section) | `edge-b-dup-shonen.txt` (+ fixture receipt) | refused, rc 1 | rc 1, **S1** defect `dup=['## SHONEN x2']`, S2 ok | PASS with nuance (below) |
| 6 | six headings present but out of order (`## SHONEN` moved after `## Landed changes`) | `edge-c-out-of-order.txt` (+ fixture receipt) | S1 refuses, rc 1 | `S1 defect … ordered=False`, rc 1, only S1 defects | PASS |
| 7 | supplementary S4 probe: 1 evidence row, no backtick/hex | `probe-s4.txt` (+ fixture receipt) | S4 refuses | `S4 defect rows=1 pointed=0`, rc 1, isolated | PASS |
| 8 | supplementary S6 probe: 301-byte report | `probe-s6.txt` (+ fixture receipt) | S6 refuses | `S6 defect bytes=301 sections=6`, rc 1 (S2/S4 also defect by construction) | PASS |

### Verbatim key outputs

Run 1 (red): `S1 defect headings=4/6 missing=['## Trend verdicts', '## SHONEN'] dup=[] ordered=False` / `S2 defect no ## SHONEN section (boxes=4)` / `S3 defect expansion=None quality=None discernment=None` / `S4 ok rows=2 pointed=2` / `S5 ok placeholders=[]` / `S6 ok bytes=12415 sections=7` / `DEFECTS n=3` / `PREDICATE R68-A2 fail` / `rc=1` — exactly the frozen r1 expectation (S1/S2/S3).

Run 2 (selftest): r1-attempt1 fail(S1,S2,S3); r5-green pass; r2-three-boxes fail(S2 `box-lines=3 want=4 matched=3`); r3-no-discernment fail(S3 `discernment=None`); r4-placeholder fail(S5 `placeholders=['TODO']`); summary `SELFTEST n=5 red-refused=4 green-ok=1`, rc 0.

Run 3 (green): `S1 ok headings=6/6 … ordered=True` / `S2 ok box-lines=4 want=4 matched=4` / `S3 ok expansion=improved quality=improved discernment=unchanged` / `S4 ok rows=3 pointed=3` / `S5 ok` / `S6 ok bytes=2683 sections=6` / `DEFECTS n=0` / `PREDICATE R68-A2 pass` / `rc=0`. Green skeleton written by this seat into scratch (adapted structure, own prose, evidence pointers: `0e52fb5d`, `a8883187`, `d2ed4ca3`, receipt/gate paths); copy of record `green-report-fixture.md`.

## Frozen sentence vs implementation, S1–S6 (file `plans/round68_report_contract.py`; line numbers at sha `18fbfc21…`)

| check | frozen sentence (A2 item 3) | implementation | implemented as frozen? |
|---|---|---|---|
| S1 | each of the six headings appears exactly once, in that order | `check()`:80-94 — per-heading `line.strip() == heading` hit counts (exact match after strip); `missing`/`dup` at 85-89; `ordered = positions == sorted(positions) and len(positions) == len(HEADINGS)` at 92; ok at 93 | YES — order, uniqueness and presence all enforced |
| S2 | `## SHONEN` occurs once AND exactly one checklist line per SHONEN.md box (4), matched by first five whitespace-normalized words | `check()`:96-105 + `box_keys()`:52-59 + `section()`:62-73 — keys = first five normalized words; `got` = CHECK_RE lines of the **first** `## SHONEN` section only; ok = `len(got)==len(keys) and matched==len(keys)` via `startswith`. The "occurs once" conjunct is enforced at **S1:89** (`dup.append`), not inside the S2 block | YES net (refusal guaranteed; measured edge-b: rc 1 via S1 dup while S2 stays ok on the first section) — enforcement site differs from the sentence's letter |
| S3 | `expansion:` / `quality:` / `discernment:` each with one of improved\|harmed\|unchanged\|unprovable-but-better | `check()`:107-114 — per-trend regex inside the `## Trend verdicts` section only; optional `**` bold tolerated between colon and word (VERDICTS:41) | YES (bold tolerance is a harmless superset) |
| S4 | measurements section: ≥2 table rows; every claim row carries a backticked token or 7+-hex commit hash | `check()`:116-131 — table lines minus separator rows and `claim`-prefixed header (case-insensitive); HEX_RE:44 `\b[0-9a-f]{7,}\b`; ok = `rows>=2 and pointed==len(rows)` | YES; two implementation choices inside the letter: HEX_RE is lowercase-only (uppercase hashes wouldn't count), header exclusion keyed on first-cell prefix `claim` |
| S5 | no TODO / TBD / FIXME / lorem ipsum / \<placeholder\> in the report | `check()`:133-136 — case-insensitive substring scan over the WHOLE report (PLACEHOLDERS:45) | YES ("in the report" = whole report); substring+case-insensitive is stricter than a token read, e.g. prose containing `tbd` refuses |
| S6 | report ≥ 400 bytes and ≥ 3 `##` sections | `check()`:138-143 — `len(report.encode("utf-8")) >= 400 and` count of lines `startswith("## ")` `>= 3` | YES (counts any `##`-prefixed line, a superset of "sections") |

Exit surfaces: no report argument → usage on stderr, rc 2, **no `SETUP`** (main:222-224); provided-but-unreadable path → `SETUP could-not-evaluate …`, rc 2 (main:229-231); defects → rc 1, `PREDICATE R68-A2 fail` (main:238-240); selftest missing r1 fixture → rc 2 (selftest:172-174). Docstring contract (lines 4-12) matches all of these.

## Findings (reported, not edited — no seat edits a frozen rule)

1. **F1 (wording tension inside A2 item 3, no gate defect).** The frozen sentence "Every check must fail on its own red fixture" is not satisfiable by the frozen enumerated fixture set: r1 covers S1+S2+S3, r2→S2, r3→S3, r4→S5, r5 green — **S4 and S6 have no frozen red fixture**, yet the frozen summary line fixes `n=5`. The gate implements exactly the enumerated list and prints the frozen summary. To close the vacuousness question (kill rule b) I probed S4 and S6 myself (runs 7-8): both refuse on their defect condition. Conclusion: no check is vacuous; the tension is in the frozen text, not the code.
2. **F2 (edge-b site nuance).** A second `## SHONEN` section is refused by **S1**'s duplicate detection (measured `dup=['## SHONEN x2']`), while S2's own block passes because `section()` extracts the first occurrence. The frozen S2 sentence's "occurs once" conjunct is therefore enforced conjunctively at S1:89 — net behavior (refusal, rc 1) matches the contract; the defect label differs from the seat spec's shorthand "S2 refuses".
3. **F3 (edge-a variant).** "Missing report path" has two readings: argument omitted → rc 2 with a usage line and **no `SETUP` token**; path given but unreadable → rc 2 with `SETUP could-not-evaluate`. Only the second carries `SETUP`. Both captured in `edge-a-missing-path.txt`.
4. **F4 (lane state).** HEAD advanced `7803bdd4` → `27f649f8` == origin/master while this seat ran (w2 landing in flight); tracked tree clean at both snapshots; all shas pinned against `27f649f8`. No effect on the gate outputs above.

## A2 gate kill rules, checked

- (a) gate passes the attempt-1 report → vacuous: **NOT observed** — refused rc 1 with S1/S2/S3 (run 1).
- (b) a check cannot fail on its own red fixture → vacuous: **NOT observed** — S1/S2/S3/S5 fail in the frozen selftest (run 2); S4/S6 demonstrated failing by runs 7-8 (see F1 for the fixture-set wording tension).
- (c) gate fails the landed attempt-2 report for an unfixable reason: not exercisable by this seat (the landed fleet report is the L1's to score); the green run proves a compliant report passes with `DEFECTS n=0`.

## Verdict

`plans/round68_report_contract.py` at sha `18fbfc21…` implements the frozen A2 item 3 predicate as written on every exercised path: red refused (rc 1, S1/S2/S3), selftest `n=5 red-refused=4 green-ok=1` (rc 0), green passes (rc 0), and all three specified edge cases behave as specified (with F2/F3 nuances recorded). Findings F1-F4 are reported for the L1; nothing was edited in L.

## Hygiene

Scratch `/fast/scratch/hyaku/kengaku-r68/ReportGateVerify/` deleted before yield; all receipts and fixture copies preserved in this directory (`red-attempt1.txt`, `selftest.txt`, `green.txt`, `green-report-fixture.md`, `edge-a-missing-path.txt`, `edge-b-dup-shonen.txt` + `-fixture.md`, `edge-c-out-of-order.txt` + `-fixture.md`, `probe-s4.txt` + `-fixture.md`, `probe-s6.txt` + `-fixture.md`, `provenance.txt`). Only wave-dir writes made; no tracked lane file touched; no git/jj write command run; no subagent and no labrat spawned (leaf seat; no falsifiable-hypothesis probe needed).
