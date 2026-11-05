# Kengaku round 88 — a sixth executed Terminal-Bench 2.0 member, and the Q66 counter-side check made executable (and found weaker than its predicate)

Round 88 (hyaku run 15, attempt 1), 2026-11-05. L1 `KengakuR88`. Lane `kengaku-shokunin`, branch `master`.
Frozen claims: commit `0220c2f9f356bf032bd58b4ed39e32f6e26fa440` (`plans/round-88-claims.md`,
`plans/round88-cases.json`), frozen before any instrument existed. Base `801b903af6412cb424209a60b3a52e56c3532866`.
Instruments: `1f267d4b6f60f1137ebf8b905d318bd2d9894e99`. Measured tip `7fcc680b86599eedd63e862a061848298428b3cc`.

Two claims on two distinct surfaces:

- `R88-C1` coverage: one more located offline replay, `fix-git`, by `plans/round88_c1_replay.py`. It moves the
  `crypto-credential` class 2 → 3 of 12; the previous executed member of that class is `openssl-selfsigned-cert` (round 80).
- `R88-C2` capability acquisition (no axis-score move, round-82-C3 framing): `plans/round88_claim_figures.py`,
  the executable half of QUALITY.md Q66 routed to this round by the round-87 verifier spot-check.

Dated pointer (round-87 spot-check routed defect V3): the non-author spot-check of this lane's round-87 work is
`corpus/lessons/round-87-verifier-spotcheck.md` (committed `801b903a`, 2026-11-05, written by the hyaku closure
session, not by the round-87 author).

## Gate

### Source admitted (S277)

The L1 opened the source below on 2026-11-05 (`curl`, HTTP 200, 1194 bytes) and byte-compared it with the
round-52 capture (`sha256 a8a6f51eb0d7c4ebdf0813c8f0b645edf29c995f1f9faf2aca3886a6713043f3` on both, `cmp` silent).
One new row was appended to `corpus/SOURCES.md`; no existing row's status, recheck or used-by cell changed.
ScribeR88 re-opened the same URL independently (HTTP 200, 1194 B, same sha256) and checked the row and the Gate line.

| id and decision | URL | access date | located quote (5 words, ≤25) | reason / flip |
|---|---|---|---|---|
| S277 admit, A for pinned grader acceptance semantics (member replay only) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/fix-git/tests/test_outputs.py | 2026-11-05 | `assert hash_file(path_a) == hash_file(path_b), (` at line 19 | the grader's md5-pair predicates over `/app` file pairs are the replay's acceptance surface; `hash_file` strips bytes before hashing at :6-9, which the trailing-whitespace case exercises; scope is member replay only, not a git-semantics or solved-task claim |

### Quarantine slice (shokuknow absent-defect register, kengaku rows)

The register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` has three
`kengaku` rows; two are data rows with an S-id and class `payload-absent` (`.ufo/waves/round-88/assimilation/quarantine-slice`).
Each was hand-checked this round as the register requires: fetch the cited source, locate the quote.

| row | cited source | fetch this round (2026-11-05) | quote located | verdict |
|---|---|---|---|---|
| S091 (round2) | https://jpn.nec.com/techrep/journal/g23/n02/230212.html | HTTP 403, 418 B, an edge "Access Denied" page | not located (no page body to search) | **unverifiable — unreachable**, not fabrication: the source could not be read, so neither admission nor refusal is grounded. Stays unadopted. |
| S105 (round3) | http://web.archive.org/web/20251118034714/https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html | HTTP 200 (Wayback wrapper, 13 KB; raw `id_` form 10 KB) — the archived body is the live GENIAC 第1期 性能評価結果公開 results page | `指定されたページまたはファイルは存在しません` ("the specified page or file does not exist") **absent** from both captures | **refused — absent**: the quote is not in the cited capture; refused in the fabrication class. Stays unadopted. |

Adoption: none. The register slice is quarantined; no package from it is admitted this round.

### Census

`sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`: exit 0 after (269 rows).
Before, from a full `git archive 801b903a` tree, `validate --file corpus/SOURCES.md`: exit 0, 268 rows (a partial
corpus-only archive gives E11 path errors; the full tree does not). After, `--file` on the tip tree: exit 0.
Rows added by tier: A 1 (S277 admitted). Status: mined 243 → 244, rejected 17, queued 8. The 30 W04 duplicate-URL
warnings are the standing cross-scope duplicates of earlier rounds (identical count before and after).

### Considerthese

`considerthese/2026-10-26.md` carries three items under "proposals only; not acted on". Round 88 takes none.
Proposal 1 (routed-findings burn-down, with a freeze refusal) is still unimplemented; the Q66 instrument discharges
two routed round-87 defects (V2, V4) but is not that burn-down. Proposal 1 is the named candidate for round 89.

Assimilation: none. `merge/kengaku/` remains blocked by L0 `kengaku | round-54`.

## Claims and their measurements

- **R88-C1 (coverage).** Before (BASE `801b903a`): `TARGET executed_rows=31 member=fix-git located=0 executed=0 cases=0 legs=0 mismatches=0 defects=3`, `PREDICATE R88-C1 fail`, exit 1. Three defects: `L4-table` (table absent at base), `L1-receipt` (receipt absent), `L7-ledger` (row unexecuted). After (measured tip `7fcc680b`): `TARGET executed_rows=32 member=fix-git located=1 executed=1 cases=8 legs=16 mismatches=0 defects=0`, `PREDICATE R88-C1 pass`, exit 0. Ledger: executed 31 → 32; `crypto-credential` 2 of 12 → 3 of 12; `file-artifact` 23 of 76 → 24 of 76. Predicate status: met as frozen; see the soundness findings below before reading the pass as authentication.
- **R88-C2 (capability acquisition).** Before (BASE): the instrument does not exist (`git cat-file -e 801b903a:plans/round88_claim_figures.py` fails). After (measured tip `7fcc680b`): `RECORDS claims=17 files=8 records=56 checked=56 matched=55 mismatches=1 prose=0`, one `MISMATCH KNOWN R87-C1 kv:defects claimed==7 measured 3`, `DEFECTS n=0`, `PREDICATE R88-C2 pass`, exit 0. `--selftest` prints five `SELFTEST … pass` lines and `PREDICATE R88-C2-SELFTEST pass`, exit 0 (the frozen text says four; reported, not repaired). Predicate status: met as frozen; see the soundness findings below.

## Controls and battery

Committed before the measured tip is scored (see `.ufo/waves/round-88/L1/`):

- do-nothing at BASE: R88-C1 `defects=3`, rc 1; R88-C2 instrument absent at BASE (`base-runs.txt`);
- the ledger-only control (receipt removed in a committed fixture) → `DEFECT L1-receipt`, `defects=1`, rc 1;
- the forged `LANE_TIP` control (receipt stamp names an orphan commit, not an ancestor) → `DEFECT L3-tip`, `defects=1`, rc 1 (`controls.txt`);
- the R88-C2 able-to-fail battery: `--selftest` T1 feeds a doctored claims copy (`defects=7`→`defects=9`) through the same extract+check pipeline and observes `verdict=mismatch`; T2 pins marker negatives; T3 pins the backward `at BASE` direction; T4 pins dedupe (T4 is vacuous in practice, see below);
- the separation transcript (`separation.txt`): the C2 counter at the ledger-only fixture still reports `PREDICATE R88-C2 pass`, so C2 does not read C1's receipt.

## Wave 1 (12 seats; attack share 6 of 12; one connector seat)

Dispatch `.ufo/waves/round-88/w1-dispatch.json`, handoff `w1.ready` → `w1.ready.dispatched`
2026-11-05T02:37. Seats: ScoutR88, ScribeR88, ExecBaseR88, ExecCtrlR88, ExecCensusR88, ReviewerR88a/b/c, CriticR88,
MutTesterR88, SentinelR88, ConnectorR88. Evidence under `.ufo/waves/round-88/w1/<seat>/`. Results (verbatim verdicts):
ScribeR88 `FINDINGS findings=1` (cosmetic); CriticR88 `FINDINGS findings=15` (six MAJOR); SentinelR88 `FINDINGS 8` (2 High, 4 Medium, 2 Low);
ReviewerR88c `SPOTCHECK admit=agree q66=agree`; ReviewerR88a 2 MINOR; ReviewerR88b 5 (1 frozen-text, 1 wording, 3 engine);
MutTesterR88 C1 13 mutants (9 killed, 4 survived: three redundant with L6, one output-only) and Q66 10 mutants (6 killed, 4 survived).
No seat died; the dispatcher reused `SentinelR88-2` and `ConnectorR88-2` as spawn names, outputs remain under the plain seat names.

**Disposition rule.** Every finding below is reported, not repaired in this round. The frozen kill rules name "any edit to a
frozen claims file, case table, counter or this instrument after commit A" as making the claim unmet, so an in-round fix
would void both claims. Each is routed to round 89 as a counter amendment with its own frozen predicate and controls.

### Findings that bear on what this round's green can mean

1. **C1 accepts a forged probe (Sentinel F1 High; Critic F1 MAJOR).** L6 re-runs `plans/round88_fixgit_probe.py` from the
   measured tree, unsandboxed, and compares against the receipt. A probe whose grader call is replaced by an echo of the
   predicted vector reproduces its own receipt and passes (Critic: `TARGET … defects=0`, `PREDICATE R88-C1 pass`, rc 0;
   Sentinel variant A). No frozen element pins the probe bytes. The tip's receipt is real (the L1 and Scout reruns
   reproduced it); what the counter cannot establish is that the receipt came from the grader rather than from a forged probe.
2. **C2 passes when a frozen before-figure's claimed value changes (ExecCtrlR88 control B, predicted UNEXPECTED, got PASS; Critic F4; MutTester O1).**
   The KNOWN check compares `(claim, key)` only. A doctored `defects=9` for R87-C1 yields `MISMATCH KNOWN` and `PREDICATE R88-C2 pass`.
   This contradicts the frozen wording "exactly" and is the most consequential defect this wave found.
3. **C2 passes when before-figures are deleted (ExecCtrlR88 control C; Critic F5; Sentinel F3).** Deleting R85-C1's Before sentence
   drops 56 → 49 records and still passes. `F6-norecords` fires only for a zero-record claim whose counter passes at BASE; a claim
   that loses its figure while its counter still fails is silent. Records and checked counts are printed, never gated (MutTester O3).
4. **C2 extraction net is convention-dependent (Reviewer B finding 3; MutTester O4; Critic F3).** R83-C2's before-state
   ("before eight unregistered ids plus missing index, fail") carries no counter vocabulary and contributes zero records.
   Colon-delimited, post-`PREDICATE` and prose-number figures escape. A dropped backward-direction selftest (m08) removes five
   records and still passes the predicate at tip.
5. **C2 has no freeze anchor (Critic F5/F6; Sentinel F3).** Claims-file bytes are not pinned to commit A's blob ids; the kill rule
   "edit … makes the claim unmet" is not implemented; the selftest is named in the predicate but `run_check` does not invoke it (MutTester O2).
6. **C2 self-tests are partly vacuous (MutTester O5, m06, m07; Critic F11).** T4 (dedupe) passes with dedupe disabled because the
   duplicate fixture yields one span; FAIL_RE can be dropped with no selftest or tip change.
7. **Frozen-text wording (Reviewer B 1–2; Critic F13–F14).** The R88-C2 After bullet says four selftest lines, the instrument prints five;
   the predicate sentence differs across its three homes; `legs` in C1 is arithmetic, not a measurement (O6 notes `executed_rows` is printed but not a leg).

### Lower-severity findings, routed

- Sentinel F2 Medium: C1 anchors (`FREEZE_REV`, `SUBJECT_SHA`, `FROZEN`) are constants inside the file under test; repointing `FREEZE_REV` passes.
- Reviewer A F1 MINOR: L3 accepts any resolvable ancestor, not only the measured tip; the honest-limit prose understates this (demonstrated with BASE `801b903a` as the stamp).
- Reviewer A F2 MINOR: `stage()` with `rel=""` raises an uncaught `IsADirectoryError` outside the documented exit contract (unreachable at the frozen table).
- MutTester m06/m11/m13: C1 L5 and L8 are redundant with L6 on every reachable fixture, so one change yields two defect lines.
- Critic F2 MAJOR: C1 is a count move (one more member of an existing class) not a new surface; the frontier moved by arithmetic.
- Critic F7: real before-figures are unchecked for the prose path; the prose path contradicts the docstring.
- Critic F15: the SKILL.md `file-artifact` cell read 22 of 76 at BASE while the ledger counted 23 (the round-87 movement was not
  reflected). This round sets it to 24 of 76 (round 88 adds `fix-git`) and discloses the earlier drift here.
- Scribe F1 (cosmetic): "Considerthese" label spacing in this lesson — fixed in the commit that carries this text.
- ExecBaseR88: one first-pass quoting defect in its own capture harness (`"|"` passed as a git argument); corrected in the same transcript; no value changed.
- ExecCensusR88: `validate --file` returns rc 1 on partial trees (E11 path resolution, documented); `--root` rc 0 is the contract and holds.

### Connector overlap (ConnectorR88)

Fleet-first: the located replay of `fix-git` (a) and the L6 probe re-run (b-L6) have no sibling mechanism. The receipt-ancestor
leg (L3) has DUPLICATE relatives in kama (`tools/round72-receipt-tip-binding.py`) and tameshi (`tools/receipt-revision-gate.py`),
neither of which re-runs a probe. Re-derivation of frozen before-figures by re-running historical counters (c) has no sibling
equivalent; the nearest is chousa's claims-file audit, which reads blobs and does not re-run counters.

## Mistakes

1. **Class `figure-not-measured`** (routed defects R87-V2/V4, QUALITY.md Q66). Evidence: `plans/round-87-claims.md`
   asserts R87-C1's BASE figure as `defects=7`; the counter's own BASE output measures `defects=3` (table, receipt,
   ledger — the `7` was carried over from the round-86 shape and never measured for this member). Captured-by: none
   until this round. Fix attempted: `plans/round88_claim_figures.py` re-derives every frozen before-figure record and
   reports the KNOWN mispredict. Status: the executable check exists and the known mispredict is on the record, but the
   wave (findings 2–4 above) shows it is not yet a sound guard. It must not be read as proof that before-figures are measured.
2. **Instrument-side bugs found during development** (fixed before the instrument was committed): mis-ordered regex groups
   (`ValueError` on `stamps`); a bare `BASE` opening spans; `at BASE` inside an after-target sentence read as a before-marker;
   `q1=1` parsed as absent (the key regex excluded digits); binary `git archive` decoded as text.
3. **Overclaim in the first draft of this lesson and of QUALITY Q66.** Both described the Q66 check as complete. The wave
   shows it is not. Both are corrected in this commit.

## Frontier

One source admitted (S277); two quarantined rows adjudicated (S091 unverifiable, S105 refused); no new candidate opened.
The round-87 lesson's "next candidate" (`fix-git`) is now executed.

## Routed to round 89

Named as findings for the next round's frozen claims (not repaired here): pin probe bytes to the instrument commit and
run the frozen probe from there (finding 1); compare `(claim, key, claimed, measured)` in the KNOWN check and gate record
counts per claim against claims blobs at commit A (findings 2, 3, 5); widen the extraction net or make an unextractable
before-figure a defect (finding 4); invoke the selftest from the predicate path (finding 5); fix T4 and the FAIL_RE gap (finding 6);
drop or pin the frozen "four" text and predicate homes (finding 7). Proposal 1 of `considerthese/2026-10-26.md` remains the
round-89 candidate.
