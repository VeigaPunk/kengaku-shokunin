# ClaimFalsify2 — round 68, attempt 2, wave w2: falsification of R68-C1, R68-C2 and the A2 report gate

Seat: `ClaimFalsify2` (leaf; no subagent). Lane root `L = /home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scratch `S = /fast/scratch/hyaku/kengaku-r68/ClaimFalsify2` (deleted before yield; all receipts quoted
here). No tool was installed. `cmark` 0.31.2 was already present at `/usr/bin/cmark` and was used
read-only as a CommonMark renderer. No clone, no fixture repo, no `git`/`jj` mutation anywhere.

**Verification tip.** The lane moved during this seat: `7803bdd4` (A2 freeze) → `27f649f8` (A3 freeze,
`git log` line 1). `git rev-parse HEAD origin/master` at verification → both
`27f649f874ae96d7cf7f4f3e6ea4d0810f0d2f91`. `git diff --stat 7803bdd4..27f649f8` over every
claim-relevant path shows **only** `plans/round-68-claims.md` (+27 lines, Amendment A3); the C1 probe,
C2 gate, A2 gate, receipt, captures, erratum, `SKILL.md`, `SHONEN.md` and round-67 probe are
byte-identical at both tips. All results below therefore apply to both. (The working tree at
verification carried another seat's in-flight A3 correction: ` M SCORECARD.md`,
`plans/round68_capability_table.py`, plus untracked w2 files. I touched none of them. Shortly after the
target re-derivation another seat added a `round66_c1_tensor_probe` row to `SKILL.md` (working-tree
modification, not mine); that row is not one E4 reads, the two E4-bound rows
(`round65-c1-sqlite-probe` with `--strict`, `round67_c1_pipeline_probe`) are unchanged, and both
predicates were re-run after the addition: `PREDICATE R68-C1 pass` rc 0 and `DEFECTS n=0` /
`PREDICATE R68-C2 pass` rc 0. `git diff` over the artifacts I hash-pinned above is still empty.)

Target hashes re-derived at the tip:

| artifact | sha256 |
|---|---|
| `plans/round68_c1_pypi_finish.py` | `4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc` |
| `plans/round63_c1_pypi_probe.py` (BASE-PROBE) | `2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929` |
| grader `pypi-server/tests/test_outputs.py` | `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` |
| `plans/round68_c2_correction_gate.py` | `1d9fd08f11a10b30f7b504d13b803c3fbd1136157559407d55177de16bed879d` |
| `plans/round68_report_contract.py` | `18fbfc2111d747ae9f40220333f0bbd56062c89e93bcd7c2477358228a0723f4` |
| `corpus/evidence/round68/pypi/receipt.txt` | `c6ed306e80bf01a36a35b8f0c38f0f9e13fdff276d53444ca03caecf20a665de` |
| `plans/round-67-claims.md` | `d465f601cc05cd4df777d1e7432d3327c517afbcf7436b6025538e61de4c9be4` |
| `plans/round67_c1_pipeline_probe.py` | `03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e` |

Fixtures were built in `S/forge/`, `S/roots/`, `S/a2/`; commands below run with cwd `L`.

---

## 0. Re-derivation of the frozen predicates (no attack)

| check | command | rc | observed |
|---|---|---|---|
| R68-C1 | `python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt` | 0 | `CHECK ok cases=4 vector=P/F/F/F wheel_sha256=6fad8ea86492...`; `CHECK stored-predicate=pass derived=pass`; `PREDICATE R68-C1 pass` |
| R68-C2 | `python3 plans/round68_c2_correction_gate.py` | 0 | `E1..E5 ok`; `DEFECTS n=0`; `PREDICATE R68-C2 pass` |
| A2 selftest | `python3 plans/round68_report_contract.py --selftest --work S/a2final` | 0 | `SELFTEST n=5 red-refused=4 green-ok=1`; r1 fails S1/S2/S3, r2 S2, r3 S3, r4 S5; r5 passes |
| A2 green control | `python3 plans/round68_report_contract.py S/a2/green-control.md --shonen SHONEN.md` | 0 | `DEFECTS n=0`; `PREDICATE R68-A2 pass` |
| C1 selftest | `python3 plans/round68_c1_pypi_finish.py --selftest --work S/c1-self --green-receipt corpus/evidence/round68/pypi/receipt.txt` | 0 | `RED r1-all-p..r5-stderr-sha rc=1 refused=True`; `GREEN receipt rc=0 accepted=True`; `SELFTEST red_refused=5/5 green_ok=1 ok=True` |
| C2 selftest | `python3 plans/round68_c2_correction_gate.py --selftest --work S/c2-self` | 0 | `DEFECTS n=5`; `SELFTEST defects-in-fake=5 want=5 all-fail=True` |
| C1 do-nothing control | `python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/controls/control-old-receipt.txt` | 1 | 22 refusal lines: `probe-sha (none)`, `base-probe-sha (none)`, `grader-sha/pin (none)`, all four `CASE` lines missing, no stderr/server-log/class/vector/exit lines; `PREDICATE R68-C1 fail` |

Counting anchors at the tip: base receipt absent `git cat-file -e d2ed4ca3:corpus/evidence/round68/pypi/receipt.txt` → rc 128;
`git show d2ed4ca3:SKILL.md | grep -c 'executed 1 of 8'` → 1; `grep -c 'executed 2 of 8' SKILL.md` → 1;
`grep -cE '^\|[[:space:]]*S240[[:space:]]*\|' corpus/SOURCES.md` → 1; `grep -c '^## Erratum (round 68)' plans/round-67-claims.md` → 1;
`grep -c 'ERRATUM-68' corpus/evidence/round67/pipe/a1-mutants.txt` → 1; `grep -c 'round67_c1_pipeline_probe' SKILL.md` → 2 (row exists);
`test -e corpus/evidence/round68/r67-probe-selftest.txt` → true; `grep -c 'recipe-unexecuted' plans/round-67-claims.md` → 2.

---

## 1. R68-C1 — required forgeries (f1–f4)

Command template (cwd `L`):
`python3 plans/round68_c1_pypi_finish.py --check-receipt S/forge/<fixture>`

| # | fixture (delta from the receipt of record) | rc | first refusal line | verdict |
|---|---|---|---|---|
| f1 | copy, CASE K1 `observed=P` → `observed=F` | **1** | `CHECK defect K1-observed F != P` | **refused** (then `exit-agreement CLASS-PROBE-EXIT=0 want 1`, `stored-predicate pass != derived`) |
| f2 | copy, K2 `stderr_sha256=` `dedbc20d…` → `9c7014b3…` (K3 capture sha) | **1** | `CHECK defect k2-stderr-sha receipt 9c7014b3b55bad773f6b5ac8bf950338e191a40f1ea7e002a25f7a9e1f2b4a58 != committed dedbc20d70cc292e39eec807222312473313ee274e3a8db8476e3e0d8565375d` | **refused** (twice: clause and per-case binding; then exit/predicate disagreement) |
| f3 | real head lines + all-P `CASE` lines with expected=P and zero shas | **1** | `CHECK defect K2-expected P != F` | **refused** (also K2/K3/K4 observed, all stderr shas against committed, server-log sha, exit/predicate) |
| f4 | byte copy of `corpus/evidence/round63/pypi-probe.txt` | **1** | `CHECK defect probe-sha (none) != 4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc` | **refused.** Measured precisely: it *does* carry a matching `GRADER sha256=… pin=…` (the grader is unchanged), so the seat brief's "lacks every new binding" is imprecise for `GRADER`. It lacks `PROBE`, `BASE-PROBE`, the new-format `CASE` lines with `stderr_sha256`, the server-log line/flags, the corrected K2 clause line, `CLASS network-service executed=2`, `PREDICTION-VECTOR`, and exit agreement; its old `K2 stderr_mentions_8080=True` line is ignored |

**Required-refusal result: 4/4 refused, rc 1 each. No claim-killing pass.**

---

## 2. R68-C1 — additional attacks (mine, not required)

| # | delta | rc | observed | verdict |
|---|---|---|---|---|
| f5 | real receipt + unknown `CASE K5 …` line | 1 | `CHECK defect case-unknown K5` (+ exit/predicate disagreement) | refused; the frozen duplicate/unknown-CASE strictness works |
| f6 | K3 `exception=AssertionError` → `exception=CalledProcessError` | **0** | `PREDICATE R68-C1 pass` | **PASS — attack succeeded** (see finding C1-1) |
| f7 | K1 ` exception=none` token removed entirely | **0** | `PREDICATE R68-C1 pass` | **PASS — attack succeeded**, same class as f6 |
| f8 | K1 observed→F **and** stored `PREDICATE … fail` / `CLASS-PROBE-EXIT=1` made self-consistent | 1 | `CHECK defect K1-observed F != P` | refused; agreement bookkeeping cannot launder a vector flip |
| f9 | K1 `index_pid=999999`, K1 wheel `a*64`; K3/K4 pid and wheel replaced (`f*64`, `e*64`) | **0** | `PREDICATE R68-C1 pass` | **PASS — attack succeeded**; provenance fields are format-only (declared limitation (i)) |
| f10 | the four `CASE` lines reversed (K4,K3,K2,K1) | **0** | `PREDICATE R68-C1 pass` | PASS; order is not part of the frozen predicate |
| f11 | duplicate `PROBE` line after the correct one, second with zeros | **0** | `PREDICATE R68-C1 pass` | PASS; only duplicate **CASE** lines are refused, as frozen |

---

## 3. R68-C2 — required false greens (g1–g4)

Command template (cwd `L`): `python3 plans/round68_c2_correction_gate.py --root S/roots/<root>`

| # | root | rc | result | verdict |
|---|---|---|---|---|
| g1 | pre-landing tree: `plans/round-67-claims.md`, `SKILL.md`, `plans/round67_c1_pipeline_probe.py` from `git show d2ed4ca3:…`; no tally | **1** | `E1 defect … section absent`; `E2 defect no erratum section`; `E3 defect … r67-probe-selftest.txt missing (probe re-hash ok)`; `E4 defect pipeline-row=False, sqlite-row-strict=False`; `E5 defect no erratum section`; **`DEFECTS n=5`**; `PREDICATE R68-C2 fail` | **refused, n=5 — exactly the frozen red-before shape** (the pre-landing bytes of both files are identical at `d2ed4ca3` and `a8883187`, so the fixture is faithful) |
| g2 | landed tree + appended exact `## Erratum (round 68)` section | **1** | `E1 defect ## Erratum (round 68) heading count 2 (want exactly 1)`; `DEFECTS n=1`; E2–E5 ok | **refused at E1 as specified** (A1 amendment 3 works for exact duplicates) |
| g3 | landed tree, wrong sha `32bacf1d…` removed from the erratum | **1** | `E1 defect section present, correct-sha=True, wrong-sha-named=False`; `DEFECTS n=1` | **refused at E1 as specified** |
| g4 | landed tree, `7 refused` → `seven refused` | **1** | `E2 defect 7-refused=False, 1-accepted-by-design=True`; `DEFECTS n=1` | **refused at E2 as specified** |

**Required-false-green result: 4/4 refused; g1 prints `DEFECTS n=5`. No claim-killing pass.**

---

## 4. R68-C2 — additional false greens (mine)

| # | root | rc | observed | verdict |
|---|---|---|---|---|
| g5 | landed files, tally replaced by `this is not a selftest transcript` + correct `PROBE sha256=03793f4f…` + `SELFTEST` + `rc=1` | **0** | `E3 ok probe-line=True, selftest-line=True, rc-capture=True, probe-rehash=ok`; `DEFECTS n=0`; `PREDICATE R68-C2 pass` | **PASS — attack succeeded**; E3 cannot distinguish the committed tally from junk (finding C2-2) |
| g6 | landed `SKILL.md`, both `round67_c1_pipeline_probe` table rows replaced by the prose bullet `* note: the round67_c1_pipeline_probe gate is documented elsewhere *` | **0** | `E4 ok pipeline-row=True, sqlite-row-strict=True`; `DEFECTS n=0` | **PASS — attack succeeded**; E4 accepts a prose mention as a "row" (finding C2-3) |
| g7 | landed files + appended **`##  Erratum (round 68)`** (two spaces after `##`) section | **0** | `E1 ok section present, correct-sha=True, wrong-sha-named=True`; `DEFECTS n=0`; `PREDICATE R68-C2 pass` | **PASS — attack succeeded**; A1's exact-string heading count misses a whitespace variant (finding C2-1) |

Rendered proof (`cmark 0.31.2 -t html`): the g7 claims doc renders **two** `<h2>Erratum (round 68)</h2>`
(lines 53 and 60 of the HTML); the landed claims doc renders **one**. So the g7 fixture really is a
document with two erratum sections, and the gate green-lights it.

Per-check negative controls on landed-like roots (each isolates one check; all refused rc 1, `DEFECTS n=1`):

| root | delta | failing line |
|---|---|---|
| g8 | erratum `executed 2 of 3` → `executed two of three` | `E5 defect recipe-unexecuted=True, executed-2-of-3=False` |
| g9 | tally file absent | `E3 defect corpus/evidence/round68/r67-probe-selftest.txt missing (probe re-hash ok)` |
| g10 | `round67_c1_pipeline_probe` row lines removed, sqlite row untouched | `E4 defect pipeline-row=False, sqlite-row-strict=True` |

Together with g2/g3 (E1), g4 (E2) and g1 (all five), every C2 check is shown failing on a fixture.

---

## 5. A2 gate — required forgeries (a1–a4)

Command template (cwd `L`):
`python3 plans/round68_report_contract.py S/a2/<fixture>.md --shonen SHONEN.md`
(`a4` uses the committed fixture `.ufo/waves/round-68/w2/report-fixtures/attempt1-report.md`.)

| # | fixture | rc | result | verdict |
|---|---|---|---|---|
| a1 | gate skeleton with the `## SHONEN` section emptied | **1** | `S2 defect box-lines=0 want=4 matched=0`; `DEFECTS n=1` | **refused at S2 as specified** |
| a2 | skeleton + appended exact `## SHONEN` section | **1** | `S1 defect headings=6/6 missing=[] dup=['## SHONEN x2'] ordered=True`; **`S2 ok box-lines=4 want=4 matched=4`**; `DEFECTS n=1` | **refused overall, but NOT by S2** — the assigned "must fail S2" expectation is not met; S1 catches the duplicate (finding A2-1) |
| a3 | skeleton with `TODO` in the measurements row | **1** | `S5 defect placeholders=['TODO']`; `DEFECTS n=1` | **refused at S5 as specified** |
| a4 | committed attempt-1 report bytes | **1** | `S1 defect … missing=['## Trend verdicts', '## SHONEN'] ordered=False`; `S2 defect no ## SHONEN section (boxes=4)`; `S3 defect expansion=None quality=None discernment=None`; `DEFECTS n=3` | **refused at S1/S2/S3 as specified** (A2 kill rule (a) not triggered: the gate does not pass the attempt-1 report) |

---

## 6. A2 gate — additional attacks (mine)

| # | fixture | rc | observed | verdict |
|---|---|---|---|---|
| a5 | `discernment: unimproved` | 1 | `S3 defect … discernment=None` | refused; no prefix-bypass in the other direction |
| a5b | `discernment: improved-ish` | **0** | `S3 ok expansion=improved quality=improved discernment=improved`; `PREDICATE R68-A2 pass` | **PASS — attack succeeded**; the verdict regex prefix-matches `improved` (finding A2-2) |
| a6 | both measurement rows replaced by bare hex `deadbeef/1234567`, `abcdef0/89abcde` (no backticks) | **0** | `S4 ok rows=2 pointed=2`; `PREDICATE R68-A2 pass` | **PASS — attack succeeded**; `git -C L cat-file -e <tok>^{commit}` → rc 128 for all four tokens, i.e. no cited hash is a commit (finding A2-3) |
| a8 | skeleton + appended **`##  SHONEN`** (two spaces after `##`) | **0** | `S1 ok headings=6/6 dup=[] ordered=True`; `S2 ok box-lines=4 want=4 matched=4`; `DEFECTS n=0`; `PREDICATE R68-A2 pass` | **PASS — attack succeeded**; cmark renders **two** `<h2>SHONEN</h2>` (HTML lines 21, 28); the gate passes a report with a second SHONEN section (finding A2-1) |
| a9 | skeleton with the two measurement rows removed (header only) | 1 | `S4 defect rows=0 pointed=0` | refused; S4 *can* fail (but has no selftest red fixture) |
| a10 | 368-byte minimal report: six headings, two tiny pointed rows, four box lines | 1 | `S6 defect bytes=368 sections=6` | refused; S6 *can* fail (but has no selftest red fixture) |

`--selftest` fixture coverage measured: four red fixtures for six checks. S1←r1, S2←r2, S3←r3, S5←r4;
**S4 and S6 have no red fixture**, although a9/a10 show they can fail. The frozen A2 text simultaneously
says "Every check must fail on its own red fixture" and fixes the tally at `n=5 red-refused=4 green-ok=1`
(finding A2-4).

---

## 7. Findings — counterexample, evidence, impacted axes, smallest safe correction

I edited no predicate, counter, case table, kill rule, target, or lane file. These are reports only.

### C1-1 (C1 receipt field unbound — **attack succeeded, not claim-killing under the frozen sentence**)
- **Counterexample:** f6 (K3 `exception=AssertionError` → `CalledProcessError`) and f7 (K1 `exception=none` removed) both pass `--check-receipt` rc 0.
- **Evidence:** quoted outputs in §2; the frozen predicate sentence (claims doc, R68-C1) binds only
  `observed`/`expected`/leg, PROBE, BASE-PROBE, GRADER, stderr shas, K1 pid/wheel, server log, K2
  clause, CLASS, PREDICTION-VECTOR, exit. The `exception=` token shown in the receipt template is never
  read. The sha-bound K3 capture does carry the failure mode independently
  (`grep -c AssertionError corpus/evidence/round68/pypi/stderr/K3.txt` → 1; K4 `CalledProcessError` → 2;
  K1 `AssertionError` → 0), so the vector's discrimination is still evidenced by committed bytes.
- **Impacted axes:** coverage (C1, held at 7) — receipt self-consistency, not vector semantics. The
  receipt of record states the correct exceptions, so the landed claim is unchanged.
- **Smallest safe correction (next re-freeze, not this seat):** bind a per-case expected exception map
  (`K1 none`, `K2 CalledProcessError`, `K3 AssertionError`, `K4 CalledProcessError`) and/or require the
  named exception to occur in the sha-bound per-case stderr capture.

### C1-2 (C1 provenance fields format-only — **attack succeeded; declared limitation (i) substantiated**)
- **Counterexample:** f9 (K1 pid `999999`, wheel `a*64`; K3/K4 pid+wheel replaced) passes rc 0.
- **Evidence:** §2 f9. The checker requires only "pid not `none`" and "64 hex" for K1; it never binds a
  wheel artifact and never checks K3/K4 pid/wheel at all. `battery-run.txt` (the named live witness) is
  not named by any receipt line and is not sha-bound by the counter.
- **Impacted axes:** coverage (C1, held at 7) — provenance strength; the frozen predicate's named
  limitation (i) already says `--check-receipt` cannot prove a run. This attack only quantifies it.
- **Smallest safe correction:** state explicitly in the receipt/limitation that pid/wheel are
  format-only, or add a `BATTERY sha256=` line binding `battery-run.txt` and a committed wheel artifact.

### C1-3 (minor) duplicate non-CASE lines and CASE order are free
- f10 (reversed CASE lines) and f11 (duplicate `PROBE`, second wrong) pass. The frozen strictness only
  names duplicate/unknown **CASE** lines, so this is a literal-tradeoff, not a defect against the frozen
  text. Correction if desired: singleton-line duplicate check. Impact: negligible.

### C2-1 (C2 E1 whitespace-variant duplicate erratum — **attack succeeded; instrument bypass**)
- **Counterexample:** g7 — a landed-tree copy with an appended `##  Erratum (round 68)` (two spaces) →
  `E1 ok`, `DEFECTS n=0`, `PREDICATE R68-C2 pass`.
- **Evidence:** cmark 0.31.2 renders **two** `<h2>Erratum (round 68)</h2>`; the exact-string counter
  (`ln.strip() == "## Erratum (round 68)"`) counts one. The landed document has exactly one heading in
  any spelling (`grep -nE '^#+[[:space:]]+Erratum'` → one line; cmark → one H2), so the landed C2 verdict
  is unaffected; the counter's A1-amendment-3 purpose ("count the heading lines, require exactly one") is
  only partly met.
- **Impacted axes:** calibration (C2, held at 10) — instrument discrimination.
- **Smallest safe correction:** count ATX heading lines after normalizing the heading text, e.g. match
  `^#{2}\s+Erratum\s+\(round 68\)\s*$` (or strip the leading `#`s and collapse internal whitespace)
  instead of exact string equality.

### C2-2 (C2 E3 presence-only — **attack succeeded; frozen E3 text permits it**)
- **Counterexample:** g5 — tally replaced by junk + the correct `PROBE` line + literal `SELFTEST` + `rc=1`
  → `E3 ok`, `DEFECTS n=0`.
- **Evidence:** §4 g5. Frozen E3 only asks for the three substrings plus the probe re-hash, so a failed
  or fabricated transcript passes. The landed tally is genuine (`rc=0`, `SELFTEST green_rc=0 red_rc=1 ok`,
  line count 14) and the gate's re-hash matches; the claim stands on the frozen predicate.
- **Impacted axes:** calibration (C2, held at 10) — "re-deriving receipts" is weaker than narrated for
  the tally.
- **Smallest safe correction:** require `rc=0` and the exact `SELFTEST green_rc=0 red_rc=1 ok` line, and
  reject `rc=` values other than 0; optionally bind the tally sha in a C2 receipt.

### C2-3 (C2 E4 prose-as-row — **attack succeeded; instrument bypass**)
- **Counterexample:** g6 — the two `round67_c1_pipeline_probe` table rows replaced by a prose bullet
  containing the token → `E4 ok`, `DEFECTS n=0`.
- **Evidence:** §4 g6. The landed `SKILL.md` rows are genuine table rows (`SKILL.md:686-687` inside the
  registry section), so the landed verdict stands.
- **Impacted axes:** calibration (C2, held at 10).
- **Smallest safe correction:** require the token on a line whose first non-space character is `|` inside
  the registry section.

### A2-1 (A2 S2 uniqueness not enforced — **attack succeeded; counterexample to the frozen S2 sentence**)
- **Counterexamples:** (i) a2, exact second `## SHONEN`: refused by **S1**, while `S2 ok`;
  (ii) a8, second `##  SHONEN`: **full `PREDICATE R68-A2 pass`** with `S1 ok`, `S2 ok`.
- **Evidence:** §5 a2 / §6 a8; cmark renders a8 with **two** `<h2>SHONEN</h2>` (HTML lines 21, 28).
  Frozen S2 says "`## SHONEN` occurs once and the section carries exactly one line per box"; the gate's
  S2 only inspects the first exact-string section and never counts occurrences. Under the semantic
  (CommonMark) reading of the heading, a8 violates the frozen S2 conjunct and the gate still prints pass.
  The only defense is a literal-exact-byte reading of the backticked heading, which the g7 evidence
  contradicts as an intended reading.
- **Impacted axes:** the new A2 report-contract gate (report contract); if the judge accepts the semantic
  reading, this is a **claim-killing false green for S2** — the gate does not enforce its frozen "iff".
  The attempt-1 mistake class (missing headings) is still refused (a4; kill rule (a) not triggered).
- **Smallest safe correction:** normalize and count ATX heading occurrences in **S2 itself** (not via
  S1): match `^#{2}\s+SHONEN\s*$` with whitespace normalization, require count 1, then inspect that
  section; apply the same normalization to S1.

### A2-2 (A2 S3 suffix acceptance)
- **Counterexample:** a5b `discernment: improved-ish` → `S3 ok`, pass. Frozen S3 allows only the four
  exact verdict words; the regex prefix-matches `improved`.
- **Impacted axes:** report contract (S3).
- **Smallest safe correction:** append a negative lookahead `(?![-\w])` to the verdict alternation (a
  `\b` is insufficient before `-`), or compare the captured token exactly against `VERDICTS`.

### A2-3 (A2 S4 non-commit hex)
- **Counterexample:** a6 — rows pointing only at `deadbeef` / `1234567` etc. pass `S4 ok rows=2 pointed=2`,
  yet none is a commit (`git -C L cat-file -e <tok>^{commit}` → rc 128 for all four).
- **Impacted axes:** report contract (S4).
- **Smallest safe correction:** require backticked evidence tokens (the skeleton already uses them), or
  verify bare hex tokens as commits with `git -C <lane> cat-file -e <tok>^{commit}`.

### A2-4 (A2 selftest fixture coverage — **frozen spec inconsistency**)
- **Counterexample:** the selftest has red fixtures only for S1 (r1), S2 (r2), S3 (r3), S5 (r4); S4 and S6
  are never exercised, while the frozen text says "Every check must fail on its own red fixture" and fixes
  the count at four red fixtures. a9 and a10 show S4/S6 do fail when exercised, so they are not vacuous in
  fact — but the frozen selftest claim is not demonstrated for them.
- **Impacted axes:** report contract (selftest / calibration).
- **Smallest safe correction (requires an amendment, since it changes the frozen n=5):** add r6 (rows
  removed → S4) and r7 (368-byte minimal → S6), expected `SELFTEST n=7 red-refused=6 green-ok=1`.

### A2-5 (A2 attempt-1 fixture passes S4/S6, by design)
- a4 fails S1/S2/S3 and passes S4 (`rows=2 pointed=2`) and S6 (`bytes=12415 sections=7`); this is harmless
  (the report is refused), noted for completeness.

---

## 8. Verdict summary

- **R68-C1:** the four required forgeries are all refused (rc 1); the receipt of record re-derives
  `PREDICATE R68-C1 pass`, rc 0 at the tip; the base control and the round-63 receipt both fail; the
  frozen vector P/F/F/F and all bindings hold. Two narrow unbound fields (`exception=`, provenance
  pid/wheel) let a *self-inconsistent* receipt pass, and CASE order/non-CASE duplicates are free; none
  flips the vector or the frozen predicate. **No claim-killing finding against R68-C1 as frozen.**
- **R68-C2:** g1 refuses with `DEFECTS n=5`; g2/g3 fail E1, g4 fails E2. Three instrument gaps let a
  *fake root* pass (g5 E3, g6 E4, g7 E1-whitespace). The landed bytes are unaffected: one erratum heading
  in any spelling, genuine registry rows, a real `rc=0` tally. **No claim-killing finding against the
  landed R68-C2 corrections; the E1 strengthening is incomplete and should be re-normalized.**
- **A2 gate:** a1/a3/a4 are refused at the specified checks; a2 is refused but by S1, not S2. a8 is a
  full false green on a report with a second SHONEN H2, a5b bypasses S3, a6 bypasses S4, and the selftest
  does not exercise S4/S6. **The strongest attack (a8) succeeded and is a claim-killing finding for the
  frozen S2 clause under the semantic heading reading; S3/S4 are strictness gaps; S4/S6 are unproven by
  the frozen selftest.** I made no edit; the corrections above are recommendations for an amendment.
- **Kill rules:** C1 (a)–(e) none fired (no vector miss, checker refuses cleanly, no hang, K2 stays F, no
  foreign 8080 service observed). C2 (a)–(c) none fired (pre-landing tree refused n=5; landed tree passes;
  each of E1–E5 fails on at least one fixture: E1 g2/g3, E2 g4, E3 g9, E4 g10, E5 g8, and g1 fails all
  five together). A2 (a) not fired (attempt-1
  refused), (b) not fired for S1–S3/S5 (r1–r4 fail), **not demonstrated for S4/S6** (no red fixture;
  a9/a10 demonstrate failure manually), (c) the attempt-2 report was not yet filed at verification.
- **Impacted axes:** coverage 7 (unchanged), calibration 10 (unchanged on landed bytes), report-contract
  gate (A2) as in A2-1..A2-4.
- **No edits:** no predicate, counter, case table, kill rule or target was edited; no lane file written
  by me except this report; all git calls read-only (`log`, `show`, `diff`, `status`, `rev-parse`, `cat-file`).

Scratch `S = /fast/scratch/hyaku/kengaku-r68/ClaimFalsify2` was deleted before yield (no clone, no
fixture repo, I started no listener on 8080). Tooling: nothing installed; `cmark 0.31.2` preinstalled and used
read-only for heading rendering.
