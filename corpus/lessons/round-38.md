# Round 38 — gate behaviours attributed (21/22, one frozen direction wrong), a fourth TB2 grader executed (2026-10-26, hyaku run 8)

Baseline as read at round start: `fc1174f52b150999bef91f2e81da78732ca0eb9f` (the round-37 non-author spot-check).
Erratum to that baseline: the round-37 L1 landed `21e6251bfebf87ecf09f7b0a6df98b5c6179d0e9` (round-37 wave-2 reports,
results and an appended outcome in `SCORECARD.md` / `corpus/lessons/round-37.md`) at 02:38:25, three seconds before the
round-38 freeze commit, so the freeze `e0a378539a45cc9388c66cfba22f44275131de23` is a child of `21e6251`, not of
`fc1174f5`. Neither frozen counter reads anything `21e6251` touched; `git diff --stat fc1174f5 21e6251 -- plans/ corpus/knowledge
corpus/SOURCES.md corpus/README.md` is empty. Frozen claims `plans/round-38-claims.md`; first recorded probe run
`e95cf5500b6c13305cc41b8532ae07fb2c9dcd7b`. Landing measurement: `.ufo/waves/round-38/integrate/measure-final.txt`
(clean `--no-local` clone of `d93b7d68`, `untracked_in_clone=0`).

Controls, all red at the freeze (`.ufo/waves/round-38/claims/`): `control-c1-nothing.txt` (`PINS total=14 mismatched=0`,
`BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=0 survived=22`, exit 1),
`control-c1-gate-edited.txt` (`invalid=22`), `control-c2-nothing.txt` (`checks=7 defects=4`), `control-c2-skip.txt`
(`checks=7 defects=2`, V2 and V6 red, V7 green — disclosed at freeze), `census-before.txt` (exit 0, 15 W04).

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `knowledge/tb2-build-pmars-grader.md` (C2) | **Admitted** | Drafted by wave-1 seat `R38PkgEntry` (its own clone: `checks=7 defects=0`), integrated by the L1 with the prior-art section rewritten from `R38ScoutPriorArt`/`R38ScoutUpstream`, "14-line" corrected to the probe's 21-line `C_SRC` (`R38CritProbe` §5), and a contestable-tags subsection (`R38CritProbe` §3; the frozen tags are not edited). Rests on the 22-case receipt (`cases=22 observed_pass=7 observed_fail=15 mismatches=0`, predictions frozen before the first recorded run, second run byte-equal) and on the frozen C2 counter at the landing tip (`checks=7 defects=0`, `PREDICATE C2 pass`). Independent agreement: `R38CritPytest` real pytest 8.4.1 `22/22`; `R38CritIndep` re-derivation `22/22` plus `3/3` extra cases; `R38MutProbe` `5/5` probe mutants change the receipt. The counter alone does not prove admission: `R38CritC2Counter` §1 builds an informed filler package that reaches `checks=7 defects=0`. Flip: a wave-2 or closure re-read falsifies an entry finding against the receipt. |
| S115 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined)** | Opened 2026-10-26 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars/tests/test_outputs.py`; quote, line 46: “assert re.match(r"Results: \d+ \d+ \d+", battle_result), (”; capture `corpus/evidence/round38/tb2-build-pmars/test_outputs.py`, sha256 `d9d2796d…f4e85`; upstream `main` byte-equal (`R38ScoutUpstream`), and TB2.1 `tasks/build-pmars/tests/test_outputs.py` byte-equal too (`R38ScoutPriorArt` row 4). Flip: the capture's digest leaves the pin. |
| S116 `instruction.md` @ `2fd12b88` | **Admitted (mined)** | Opened 2026-10-26 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars/instruction.md`; quote, line 9: “We'll verify the binary has no X11 dependencies, uses Debian sources, and that the debugger works properly.”; capture sha256 `1606850…3b82`. TB2.1 revised this file (`R38ScoutUpstream`); the row pins TB2 `2fd12b88`. Flip: the capture's digest leaves the pin. |
| `tests/test.sh`, `task.toml`, `solution/solve.sh` @ `2fd12b88` (captured) | **Captured, not rows** | `test.sh` is the pytest-exit → reward mechanism the registry holds as S109; `task.toml` is read only for declared limits; `solve.sh` is the oracle, never executed. `environment/Dockerfile:9` (`COPY warriors/flashpaper.red warriors/rave.red /app/`) opened by the L1 and cited in the entry, not captured. Flip: a claim that needs one of them as its source. |
| TB2 issue #59 (`build-pmars` failing with oracle solution) | **Refused as a row** | Re-opened 2026-10-26 (`R38ScoutPriorArt` row 1; body captured by `R38LessonDraft` at `.ufo/waves/round-38/build/R38LessonDraft/tb2-issue-59-body.md`): `E: Version '1.22.21' for 'dpkg-dev' was not found` — the oracle's apt pin, not the grader; no entry statement rests on it. Flip: an entry statement about the oracle path. |
| `JonathanGabor/terminal-bench-2-audit` audit.txt:211-259 | **Refused as a row; cited as nearest prior statement** | Static LLM audit naming the provenance gap (l.249) and calling the `ldd` check "reliable" (l.255) — partly contradicted by `canned-x11-dlopen`; no executed case. Flip: a claim that rests on what the audit asserts. |
| Assimilation: `considerthese/2026-10-25.md` proposal 2(c) (read 2026-10-26) | **Mined; landed as `plans/tip_receipts.py`** | Drafted by `R38TipReceipts`; at the landing tip `receipts=24 byte_equal=4 differ=0 skipped=20` (19 round-19 logs have no committed re-run command; one round-36 first-run receipt is declared non-reproducible), tamper control `differ` (`R38TipReceipts/tip-receipts-tamper-control.txt`). 2(b) (block pre-registration on a recurring class) stays unbuilt — this round's order-of-operations recurrence (Mistakes row 2) is exactly its case. |
| Assimilation: `merge/kengaku/` card family (`benchmark-card-field-schema-2026-10-23.md`, `benchmark-card-adoption.md`) | **Admit-candidate, deferred** | `R38MergeRescreen` rows 1–2: in PROVINCE scope (Frontier "contamination transparency cards"), public sources; not adopted because no round-38 claim names it and adoption needs in-round re-grounding of S122–S124/S135–S139. Package unchanged since `ba6779f0` (2026-10-24). Flip: a round that freezes an assimilation claim on it. |
| Assimilation: `merge/kengaku/` rows 8–12 (`R38MergeRescreen`) | **Refused** | Own-work locators or duplicate ground, as recorded per row there. Id check: `.ufo/waves/round-38/assimilation/collisions` holds 31 ids (lane S077–S114 occupy the staged range); moot, nothing appended. Quarantine slice: 2 rows (`assimilation/quarantine-slice`), not hand-checked because nothing from the package is adopted. |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **freeze defect — a frozen mutant's kill direction was unreachable** (new this round) | `plans/round38_c1_verify.py` MUTANTS row N21 (`"silence"`, `sums.splitlines()` → `sums.splitlines()[:1]`): restricting an `any(...)` manifest lookup to its first row makes D5 stricter on every input, so the mutant's DEFECT set always contains the reference's and the silence rule can never hold — the frozen `killed=22` was unreachable by any battery. Found by wave-1 seat `R38BatD5` (`.ufo/waves/round-38/build/R38BatD5.md` §BLOCKER: 8 manifest shapes, no `ref DEFECT ∧ mutant ok`); landing `MUTANTS total=22 killed=21 survived=1`, `PREDICATE C1 fail` | none at freeze — the L1 wrote each direction from the replacement text and ran only the do-nothing control, which is silent on direction (every mutant survives it) | `plans/mutant_direction_check.py` + QUALITY Q29: per frozen mutant it records which attributed directions the battery exhibits and fails on `declared ∉ observed ≠ ∅`. Shown able to fail at the landing tip: `DIR N21 D5 declared=silence observed=mirror MISLABELLED`, `DIRECTIONS total=22 mislabelled=1`, exit 1 (`.ufo/waves/round-38/integrate/direction-check.txt`); the other 21 print `ok`. Not applied to N21 after scoring: C1 is an honest stop. |
| order-of-operations — **recurrence** of `corpus/lessons/round-37.md:42` (the C2 skip-control executed the frozen probe before the first recorded run) | `plans/round-38-claims.md:8-15` disclosure; `control-c2-skip.txt` keeps only `P10 DEFECT fresh probe output is not byte-equal to the receipt`; at the freeze commit no receipt exists (`git cat-file -e e0a37853:corpus/evidence/round38/build-pmars-probe.txt` → rc 128) while a committed control proves the probe ran (`R38LessonDraft` drafting) | the claims header itself (self-disclosed before the freeze commit); round 37's fix (re-pin and re-run every counter run) does not prevent the ordering, it only makes the discarded run harmless | ordering rule for round 39: a skip-control that runs the gate with `--rerun` is built only after the first recorded run lands, or with `--rerun` off. Lint, shown red on this freeze: any committed control under `.ufo/waves/round-38/claims/` whose text contains `fresh probe` requires the receipt to exist at that commit — `grep -l "fresh probe" .ufo/waves/round-38/claims/*.txt` → `control-c2-skip.txt`, receipt absent at `e0a37853` → RED. A write-up, not yet a gate: considerthese 2(b) is where it would become one. |
| witness-picked label — a requirement-map label chosen from one convenient case (round-37 closure D2) | `corpus/knowledge/tb2-git-webserver-grader.md:107` labels `instruction.md:9` `enforced` beside `CASE token-in-body … observed=pass`; the round-37 counter printed `V7 ok rows=4 bad=0` (`.ufo/waves/round-37/falsify/F37CritC2Map.md`) | `F37CritC2Map` and `F37CritC2Overclaim` (round-37 wave 2); no round-37 counter | forward: `plans/round38_c2_verify.py` V7 derives every label from all violating cases (QUALITY Q28); shown able to fail by `R38MapErratum/controls.txt` Control B (`results-format: labelled enforced, receipt derives partly`) and Control C; retro: `R38MapRetro` applies the derived rule to the round-37 map with a justified violates mapping and finds 2 disagreeing rows; the round-37 entry carries an appended `## Errata (round 38)` (rows 7–9). |
| count — a calibration claim's source arithmetic does not reach its own total | `plans/round-38-claims.md` §C1 and the counter docstring say "13 non-equivalent survivors … one diagnostic … B1, B2, B5, B6, B7, B8" (13+1+6 = 20 ≠ 22); the frozen MUTANTS cite 16 distinct extra-mutant survivors + 1 diagnostic + 6 shapes − 1 overlap (N15 = L2 = B5) = 22 (`R38CritClaims.md` §1 D4) | `R38CritClaims` (wave-1 critic) | erratum here; the list itself (N01–N22) is what the counter scores and is unchanged. Also from the same seat: 3 of the 22 `adv` cells name no advertising sentence in the claim's declared surface (N01's branch is listed as unclaimed at `corpus/QUALITY.md:435-437`), so the advertised-class mismatch count is 19→1, not 22→1. |

Note on the C1 counter (not a mistake of this round's battery): `R38CritClaims` §2 shows a two-fixture junk module that
patches the counter's in-process `run_gate` reaches `killed=20` with `wrong=0 sidechannel=0` — battery38 modules
are imported into the counter's own process, and the token scan does not see a monkeypatch. The landed battery's
code is reviewed by wave-2 seats; the counter's predicate alone is not evidence that a kill is honest
(round-37 lesson row 7's limit, reached by a new door).

## Round-37 closure routed items (`corpus/lessons/round-37-verifier-spotcheck.md` §5)

| item | disposition | measurement |
|---|---|---|
| D1 wave-2 outputs uncommitted | **Closed by the round-37 L1** in `21e6251` (37/37 reports, results, outcome sections); `R38R37Integrate` maps all 37 reports to dispositions (`.ufo/waves/round-38/build/R38R37Integrate.md`) | `git ls-files .ufo/waves/round-37/falsify \| wc -l` → 380 |
| D2 entry map overstates enforcement | **Closed** — errata appended, Q28, V7 forward rule | Mistakes row 3 |
| D3 anchor check binds to any committed digest | **Closed** — `plans/anchor_digest_check.py` binds each token to the capture its own row names (`R38AnchorBind`) | tip `rows=109 tokens=17 defects=0`; M4b/M5/M6/M7 cross-capture fixtures → `digest-wrong-capture` (old tool: `defects=0`) |
| D4 `ledger-tip` red in detached clones | **Closed** — the driver binds an absent `BRANCH` ref to the commit under audit; a `CalledProcessError` is an exit-2 refusal (`R38LedgerTip`); the pinned check bodies are not edited | tip `rows=9 closed=9 observed_pass=9 mismatches=0`; detached-clone before/after in `R38LedgerTip.md` §4 |
| D5 C1 freeze limits (survivors, attribution) | **Taken up as C1** — honest stop 21/22 | `measure-final.txt` |
| D6 sibling prior art uncited | **Closed (report-out)** — PROVINCE `Reported out (round 38)` block, 16 sibling surfaces with file:line (`R38SiblingCite`) | `PROVINCE.md` tail |
| D7 carried (C2 counter pin; F3–F5 wording) | **Partly** — the round-38 counter pins spec, dry table, probe, gate, captures; R36CritScope F3–F5 wording stays open | `plans/round38_c2_verify.py` constants |

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before (freeze): exit 0, `kengaku ok`, 15 W04 (`claims/census-before.txt`). After (landing, `--file` form on the clean
clone, `measure-final.txt`): exit 0. Counts at landing: registry rows 107 → 109 (S115, S116, tier A, `mined`),
knowledge files 44 → 45, README index rows 44 → 45.

## Spot-check

Pending — the non-author closure follows the report. Cheapest failing check first:

1. `python3 plans/round38_c1_verify.py --lane .` on a clean clone of the landing tip: expect `MUTANTS total=22
   killed=21 survived=1`, `PREDICATE C1 fail` (N21 the survivor) — the round reports C1 as an honest stop.
2. `python3 plans/mutant_direction_check.py --lane .`: expect `N21 … MISLABELLED`, every other mutant `ok`.
3. Hand-run N21 outside the counter on `d5m-n21-manifest-row-2` (the battery's only accept fixture whose matching
   manifest row is not the first): reference `D5 ok`, mutant `D5 DEFECT` — the mirror direction.
4. `python3 plans/round38_c2_verify.py --lane .` → `checks=7 defects=0`, `PREDICATE C2 pass`.
5. Relabel one `partly` row of the new entry's map to `enforced` in a scratch clone → V7 red.
6. Re-open S115/S116 live at the pin (digest + quote line).
7. `python3 plans/round37_c1_verify.py --lane .` → still `killed=55` (no harm).
