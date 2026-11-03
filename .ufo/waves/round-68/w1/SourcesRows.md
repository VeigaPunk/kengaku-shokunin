# SourcesRows — round 68, wave 1 (scribe seat)

Seat scope: frontier drafts only (S240 registry row, round-68 lesson skeleton, considerthese
scan). No file under `corpus/`, `plans/`, or the lane root was edited; writes are confined to
`.ufo/waves/round-68/w1/SourcesRows.md`, `.ufo/waves/round-68/w1/SourcesRows/`, and the scratch
root `/fast/scratch/hyaku/kengaku-r68/SourcesRows` (deleted before yield). No installs (no
pacman, no uv/npx); the only network tool used was `curl`.

## 1. S240 row — status: the frozen spec is refuted by the opened bytes

The assignment's row (source = CPython `Lib/http/client.py` at `v3.14.8`, anchor = the
`HTTPConnection.__repr__` line) **cannot be written truthfully**: at that tag `class
HTTPConnection` (`:858`) defines no `__repr__`/`__str__`; the file's only `def __repr__` is
`:1559`, inside `class IncompleteRead` (`:1554`). `HTTPConnection` inherits `object.__repr__`
(`<http.client.HTTPConnection object at …>`). `plans/round-68-claims.md` §R68-C1's mechanism
sentence ("the rendering is the `repr()` of an `http.client.HTTPConnection`") is therefore
contradicted by the named source.

The actual renderer is urllib3 2.7.0 (the version pip 26.2.1 vendors,
`pip/_vendor/vendor.txt:11`), `src/urllib3/connection.py:163-164`:
`def __str__` → `return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"`;
`NewConnectionError.__init__` formats `f"{conn}: {message}"` (`exceptions.py:148`). My fetch and
the scout's capture are byte-identical (sha256 `668b37ab…`, 42786 bytes); the pip-vendored copy in
the round's scored venv has the same sha256. The full receipt, with commands and outputs, is
`w1/SourcesRows/S240-receipt.md`.

The frozen K2 clause itself is unaffected: its markers are read from the captured stderr, and the
capture carries `host='localhost'` ×5, `port=8080` ×5, literal `localhost:8080` ×0, `Errno 111`
×5 (`corpus/evidence/round68/pypi/stderr/K2.txt`, sha256 `dedbc20d…`). The predicate does not
depend on S240; the "Sourced:" attribution and the counting anchor do.

### Option A (recommended) — S240 is the urllib3 row (paste-ready, 11 columns, one line)

```
| S240 | urllib3 `src/urllib3/connection.py` at tag `2.7.0` — the endpoint renderer pip 26.2.1 embeds in connection-refused stderr — https://raw.githubusercontent.com/urllib3/urllib3/2.7.0/src/urllib3/connection.py | code | A | the endpoint rendering pip 26.2.1 embeds in connection-refused stderr (R68-C1 corrected clause): host and port as separate fields | :164 verbatim: return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})" — def __str__ at :163, class HTTPConnection at :82; NewConnectionError formats f"{conn}: {message}" at exceptions.py:148; sha256 668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532, 42786 bytes, byte-identical to pip 26.2.1's vendored urllib3==2.7.0 | the urllib3 connection's __str__ renders host and port as separate fields, so the literal localhost:8080 is not a form this renderer produces; the captured pip text carries host='localhost' and port=8080 | queued | 2026-11-03 | 180d | corpus/knowledge/tb2-network-service-offline-grader.md |
```

Consequences for the L1: `grep -cE '^\|[[:space:]]*S240[[:space:]]*\|' corpus/SOURCES.md` → 1 still
holds, but the row's source is urllib3, not CPython. The claims doc's S240 sentence needs a dated
amendment section (append-only; new section, never an edit) stating the corrected mechanism or
naming S240's source as urllib3. This seat does not edit it.

### Option B (literal spec preserved) — S240 is a rejected CPython row; urllib3 takes S241

```
| S240 | CPython Lib/http/client.py at tag v3.14.8 — https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/http/client.py | code | A | the endpoint rendering pip embeds in connection-refused stderr (R68-C1 corrected clause) — rejected as the mechanism source | the file's only def __repr__ is at :1559 (class IncompleteRead, :1554); class HTTPConnection (:858) defines no __repr__ or __str__, and a sweep over :858–:1531 finds 0 | REJECTED: HTTPConnection has no __repr__ at v3.14.8 (object.__repr__ renders <http.client.HTTPConnection object at …>), so this source cannot produce HTTPConnection(host='localhost', port=8080); flip: a CPython release adding HTTPConnection.__repr__ with host and port as separate fields | rejected | 2026-11-03 | 180d | — |
| S241 | urllib3 `src/urllib3/connection.py` at tag `2.7.0` — https://raw.githubusercontent.com/urllib3/urllib3/2.7.0/src/urllib3/connection.py | code | A | the endpoint rendering pip 26.2.1 embeds in connection-refused stderr (R68-C1 corrected clause): host and port as separate fields | :164 verbatim: return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})" — def __str__ at :163, class HTTPConnection at :82; NewConnectionError formats f"{conn}: {message}" at exceptions.py:148; sha256 668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532, 42786 bytes | the urllib3 connection's __str__ renders host and port as separate fields, so the literal localhost:8080 is not a form this renderer produces | queued | 2026-11-03 | 180d | corpus/knowledge/tb2-network-service-offline-grader.md |
```

Option B keeps the frozen prose literally (S240 = the CPython source) at the cost of the
mechanism row carrying a new id (S241), which the claim's counting command does not name. Option A
is recommended: S240 was never written, so the id is unused and may carry the row that actually
grounds the clause; the refusal is recorded in the lesson Gate.

## 2. Lesson skeleton

Draft: `.ufo/waves/round-68/w1/SourcesRows/lesson-round-68.md` (author header: "kengaku L1 round
68 attempt 1"). It contains the `## Gate` block with both S240 bullets (URL, access date, located
≤25-word quotes, admit/reject result), L1 placeholders for admitted/rejected/assimilation, the
`## Mistakes` table with the two round-67 closure rows pre-filled (reference-drift / wrong-sha
citation; number-drift / count drift, both citing `corpus/lessons/round-67-verifier-spotcheck.md`
§5 items 1–2 with `captured-by: none` and the R68-C2 fixes), and one candidate `attribution` row
outside the table for this wave's S240 finding (L1 decides whether it becomes a row).

## 3. considerthese scan — one line per proposal (27 total; 8 files)

2026-10-19 (4)
- #1 bidirectional `corpus/README.md` ↔ disk index gate — implemented by round 24 (`plans/round24_census.sh`: `C1.knowledge_unindexed 0`, `dead_index_rows 0`) and made re-derivable by round 25 (`plans/state_check.py` P2e/P3e check README index rows both directions; not inside `grader.py` as proposed).
- #2 TTL + quarantine for unadmitted WIP — still open (no `wip/round` prefix, no machine-readable `status: unadmitted` header; `grep -rn "wip/round" plans corpus/QUALITY.md` → none).
- #3 SCORECARD self-consistency pass — implemented by round 24 (`scorecard_state_defects_open 6/6 → 0/6` per the 10-20 status; `plans/state_check.py` re-derives the frozen P2/P3/P4 assertions).
- #4 per-trial `gt_predicate` field on attribution receipts — still open (`grep -rln gt_predicate` over `*.py`/`*.md` hits only considerthese copies and one r32 report; the attribution program it measured is retired).

2026-10-20 (4)
- #1 executable R1–R10 round-close gate + mutation-tested census — partly implemented (r26 `plans/gate_timing_check.py`, r39 `plans/order_check.py`, and `plans/round_close.py` which runs order+census), but the R1–R10-verbatim `--round-close` leg and its per-row seeded mutants are still open.
- #2 archived source text + quote locator — implemented by round 29 attempt 2 (`plans/sources_adopt.py` capability 5 measures the ≤25-word cap and locates the quote in `--artifact`; `plans/adoption_check.py` re-derives from committed bytes); the universal per-source normalized-extract archive is still open.
- #3 opencode-go stop-loss + coverage-cap petition — still open (no stop-loss rule: `grep -niE 'stop-loss|unreachable-via' corpus/QUALITY.md plans/round-*-claims.md` → 0; the coverage-cap L0 stays open and the decision packet survives only as L0 `kengaku | round-33`).
- #4 self-vs-outside verdict agreement ledger — still open (`corpus/evidence/verdict-agreement.tsv` absent; agreement is prose in each spot-check lesson).

2026-10-21 (4)
- #1 re-score historical verdicts under a hardened extractor — implemented by round 27 (`plans/parser_policy_compare.py`: 15712 paired comparisons, 1089 disagreement events, 1964/1964 baseline reproduced); the per-round list of stored conclusions that flip is still open.
- #2 prior-art preflight block before the freeze — still open (no `## Prior-art preflight` or `## Prior art` heading in any `plans/round-*-claims.md`).
- #3 seat-yield ledger and wave budget — implemented by round 29 (`.ufo/waves/yield.tsv` header `round seat role_family report caused_change commit`, first rows round 29); the cut-zero-yield-family rule is still open.
- #4 blind forecasters — still open (`blind` appears only in `plans/round-26-claims.md`; no hash-pinned forecaster seat or instrument in rounds 4x–6x).

2026-10-22 (3)
- #1 scratch as untracked cache + carrier-aware archive scan — still open (`.gitignore` has no `scratch` entry; no containment/archive scanner in `plans/`; post-r52 waves keep scratch outside the repo by wave bounds, which removes the bloat but is not the proposed gate).
- #2 WebArena evaluator-error measurement (false-pass/false-fail per stratum) — still open (no such instrument; `false-pass` occurs only in r24 claims and r25 fixtures).
- #3 crash-resumable waves (journal + `resume_wave`) — still open (no `resume_wave`/journal in `plans/`; dead seats are recorded, never redispatched by a lane step).

2026-10-23 (3)
- #1 closure-debt cap (block pre-registration while >1 admitted round lacks a non-author verdict) — still open (no `closure lag` field or rule; the debt itself was paid by r29a2–r31 but no blocking rule was written).
- #2 audit gate yield (replay every Q-gate per landing commit) — still open (`grep -rlniE 'gate-yield|gate yield' plans corpus SKILL.md SCORECARD.md PROVINCE.md` → 0).
- #3 root `STATUS.json` — still open (`STATUS.json` absent at the lane root).

2026-10-24 (3)
- #1 CI workflow running the gates on every push — still open (no `.github/` directory).
- #2 `as_of`/`source_status`/`revalidate_by` per knowledge entry — still open as proposed (no `source_status`/`as_of` front matter; the standing partial is the kaika contract's `source:/verified-at:/recheck:` trio).
- #3 demand-side question set (answerable/correct/cited/stale) — still open (no demand-side instrument; `grep -rln "demand-side"` → 0).

2026-10-25 (3)
- #1 model-diverse verification — still open (all roles route to `@m_flash`; no second-model seeded sample recorded; `grep -rniE 'second (different )?model'` → 0).
- #2 persistent routed-defect ledger + tip-receipt validator — implemented by rounds 34–39 (`corpus/defects.jsonl` opened r34 with `recurrence_of`; `plans/defect_ledger.py`, `plans/ledger_tip.py` r37, `plans/tip_receipts.py` r38, `plans/order_check.py` r39, wired by `plans/round_close.py`); the 10-26 lesson's weakness findings are quality caveats, not unimplemented scope.
- #3 coverage-cap decision packet — still open (the L0 question `kengaku | round-33` is cited in `plans/round-61-claims.md:32`; no memo exists in the repo).

2026-10-26 (3)
- #1 routed-findings burn-down — implemented by round 41 (`plans/routed_open.py` header names this proposal; `corpus/routed-findings.jsonl` exists, 74975 bytes).
- #2 one standing TB2 admission counter with a built-in filler control — partly implemented (`plans/pkg_gate.py` r36+ is spec-driven and `plans/filler46/` is the committed filler control), but per-round `roundNN_c*_verify.py` copies remain and the every-tip re-run for all admitted packages is still open.
- #3 batch TB2 grader sweep by class histogram, pick next graders by uncovered class — **implemented by rounds 62–67 (verified)**: `plans/round62_c1_class_survey.py` produces `corpus/evidence/round62/class-survey.txt` (14 classes; `EXECUTED-COVERAGE executed=17 classified=17 classes-covered=12 classes-uncovered=network-service,process-environment,db-state,container-image`), and rounds 64 (`kv-store-grpc`, network-service), 65 (`sqlite-with-gcov`, db-state), 66 (`torch-tensor-parallelism`, process-environment), 67 (`torch-pipeline-parallelism`, second process-environment member) each executed a member of an uncovered class; the remaining `container-image count=0` has no member to pick, and the attached per-task flake-rate rider is still open (`grep -rlni 'flake rate'` → only `corpus/lessons/round-40.md`).

Tally: 27 proposals scanned — 7 implemented (10-19 #1 r24–25; 10-19 #3 r24; 10-20 #2 r29a2; 10-21 #3 r29; 10-25 #2 r34–39; 10-26 #1 r41; 10-26 #3 r62–67), 3 partly implemented (10-20 #1, 10-21 #1, 10-26 #2), 17 still open. (Counts: 7 + 3 + 17 = 27.)

## 4. Findings the L1 must integrate

1. **Frozen-mechanism defect (pre-data).** `plans/round-68-claims.md` §R68-C1 attributes the
   rendering to `http.client.HTTPConnection.__repr__` and anchors S240 on that method; v3.14.8
   has no such method (`HTTPConnection` at `:858`; sole `def __repr__` at `:1559`,
   `IncompleteRead`). The predicate and its stderr clause are unaffected; the `Sourced:` sentence,
   the S240 row spec, and any prose resting on the CPython mechanism are not supported. Required:
   a dated amendment section in the claims doc (append-only) plus option A or B above.
2. **Scout capture version.** `recon/S241-urllib3-connection.py` (sha256 `88fe2981…`, 42613 B) is
   urllib3 2.5.0 and has no renderer; the correct 2.7.0 capture landed at
   `recon/S241-urllib3-2.7.0-connection.py` (sha256 `668b37ab…`, 42786 B) at 20:04. Adopt the
   2.7.0 bytes only.
3. **Scout receipts (landed 20:05, reconciled).** `recon/S240-receipt.md` and
   `recon/S241-receipt.md` now exist and agree with my independent open: same `client.py` sha256
   (`016aa766…`), the same `:1559` quote (`S240 opened=True sha=016aa766…`), the same urllib3
   2.7.0 sha (`668b37ab…`) and `:164` quote. The claim's gate condition ("live capture and located
   quote are in the wave dir") is met. Two nuances for the L1: (a) the S240 receipt's
   host/port-separation quote is `:921` (`(self.host, self.port) = self._get_hostport(host,
   port)`), which supports separate *attributes*, not the claim's sentence that the `repr()`
   renders them as separate fields; (b) the S241 receipt labels urllib3 2.5.0 "primary (as
   specified in seat prompt)" and 2.7.0 "secondary" — the row must use 2.7.0, the version pip
   26.2.1 vendors; 2.5.0 has no `__str__`/`__repr__` renderer.
4. **Counting anchors touched.** `grep -cE '^\|[[:space:]]*S240[[:space:]]*\|' corpus/SOURCES.md`
   → 1 is satisfiable (option A or B); the malformed-row census (`NF!=13`) holds for both drafts
   (11 cells = 13 `|`-split fields); no cell contains a literal `|`.
5. **No rule was edited.** This seat reports the mismatch; it does not change predicates,
   counters, kill rules, case tables, or any protected file.

## 5. Artifacts

- `.ufo/waves/round-68/w1/SourcesRows.md` (this report)
- `.ufo/waves/round-68/w1/SourcesRows/S240-receipt.md` (opens, sweeps, quotes, discrepancy)
- `.ufo/waves/round-68/w1/SourcesRows/sources/client-py-v3.14.8.txt` (sha256 `016aa766…`)
- `.ufo/waves/round-68/w1/SourcesRows/sources/urllib3-2.7.0-connection.py` (sha256 `668b37ab…`)
- `.ufo/waves/round-68/w1/SourcesRows/sources/urllib3-2.7.0-exceptions.py` (sha256 `8503c7a2…`)
- `.ufo/waves/round-68/w1/SourcesRows/lesson-round-68.md` (lesson skeleton)
- scout bytes (read-only, cited): `.ufo/waves/round-68/w1/recon/S240-client-py.txt`,
  `recon/S241-urllib3-2.7.0-connection.py`, `recon/S241-urllib3-connection.py`

DRAFTS ready=3 (S240 row set — option A paste-ready plus option B companion; lesson skeleton;
considerthese scan with 27 verdicts)
