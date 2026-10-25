# Round 31 — verifier execution model, round-30 routed-defect closure, citation-bound adoption gate (2026-10-25)

Lane: kengaku (LLM/model research & evaluation). Round shape: two v1 waves — 36 build + 36 falsify =
**72 seats** (band 32–64 per wave, ≤128 per round; policy `scripts/hyaku/ufo-wave-policy.json`).
Frozen claims: `plans/round-31-claims.md`. Baseline lane tip `0883e72`; landed round work `dbb07364`.
Access date for every source opened this round: **2026-10-25**.

## Gate

One theme — *how a benchmark's verifier actually runs* — and one admitted entry, re-grounded on three
pinned revisions opened this round. Every quote below was located in this round's own fetch; the captures
are committed with their digests at `.ufo/waves/round-31/assimilation/captures/` (`SHA256SUMS.txt`).

|candidate|decision|reason|read|
|---|---|---|---|
|`benchmark-verifier-execution-model.md` (staged package) | **admit, re-grounded** | the staged bytes fail the bar as written (Q1 `verified-at: 2026-10-23`, Q3 a 28-word block quote, Q4 no falsifier, Q5 no source-label paragraph, Q6 an unnamed "round-1 checklist", Q7 a premise — "partly observable" — that exists only in the staged copy); the *finding* survives re-grounding on the three pins, and the entry lands with the two qualifications the staged text missed (`skip_tests_upload`, SWE-bench Pro's own reset and its `DATA_DIRS` hole) | `plans/round31_*`, `.ufo/waves/round-31/build/R31DraftEntry.md`, `R31EntryScope.md` |
|`judge-calibration-thresholds.md` (package) | reject (carried from round 30) | not this round's theme, and its kappa figures still appear in none of its three anchor cells (Q3) | `corpus/lessons/round-30.md` §Gate |
|`card-publication-contracts.md` (package) | reject (carried) | a load-bearing claim rests on a tier-C machine rendering of a document the campaign holds at tier B (Q2 floor) | round-30 §Gate; round-30 spot-check §3 |
|`terminal-bench-release-identity.md` (package) | reject this round | a second theme (release identity rather than verifier execution) whose `used-by` would dangle at an entry this round does not admit; its S100/S092 citations are the ones this round's entry uses, so nothing is lost by waiting | `.ufo/waves/round-31/build/R31ReconPackage.md` |
|`benchmark-grader-semantics.md` (package) | reject this round | third theme, and its S094/S097 rows were not opened this round — CORPUS rule 4 forbids appending a row no admitted entry cites | `R31ReconPackage.md` §a |

Flip conditions are recorded on each rejected row's `teaches` cell or here: a later round that takes the
theme and opens the rows.

### Id collision check (scratch, before any append)

```
reg-ids   = 88 ids from corpus/SOURCES.md   (0–3 leading-space anchor, the census parser's own)
staged-ids= 175 ids from merge/kengaku/SOURCES.append.md
collisions= 12  (S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S090 S091)
adopted   = S092 S093 S100 — none of them in the collision set, so no renumbering was needed
```
Guard proved once before the append, on a scratch registry holding an *indented* row (`  | S002 |`): the
column-zero pattern returns **0** collisions, the 0–3-space pattern returns **1** (`S002`). Artifacts:
`.ufo/waves/round-31/assimilation/{reg-ids,staged-ids,collisions,guard/}`.

### Staged-row normalization (no staged row was appended as-is)

- **S093 carried an escaped pipe** inside a quoted span (`fail_to_pass \| pass_to_pass`), which splits the
  row into 12 cells; the anchor was rewritten around pipe-free spans of the same file, and the dropped span
  is named in the row's own `anchor` (it is described in words, not quoted).
- **All three `recheck` cells were prose** (`2026-10-23 — re-verify at the next upstream release (Gate S09x
  below)`); normalized to `180d`, and the stripped prose is recorded here: *re-verify at the next upstream
  release*. The package contains **0** `## Gate` blocks, so those pointers resolved nowhere.
- **`opened` was 2026-10-23** on all three; re-dated to 2026-10-25 only because every source was re-opened
  this round (`--attest-opened` semantics).
- **`used-by` dangled** at `terminal-bench-release-identity.md` and `benchmark-grader-semantics.md`, neither
  of which exists in this lane; projected to the one admitted entry.
- **S092's quote was not a byte substring** as staged (the description is four implicit string literals);
  the landed row quotes two spans that are.

### Sources opened this round (per-row fetch, quote and location)

| row | URL opened | located quotes (words / location) | fetch identity |
|---|---|---|---|
| S092 | https://raw.githubusercontent.com/laude-institute/harbor/6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5/src/harbor/models/task/config.py | "Whether the verifier runs in the agent's environment ('shared')" (9, `config.py:590`); "to 'separate' if a verifier 'environment' is set, otherwise" (9, `:591-592`) | 39 055 B, sha256 `ac9f5d19…bf2163` |
| S092 | …/src/harbor/models/task/verifier_mode.py | "or VerifierEnvironmentMode.SHARED" (2, `:31`); precedence docstring (`:35-38`) | 5 142 B, sha256 `e5893be9…8a6f2d` |
| S092 | …/src/harbor/verifier/verifier.py | "Discard stale rewards without removing other verifier inputs or logs." (10, `:168`); `verify()` awaits it at `:207`; `if not self._skip_tests_upload:` at `:209` | 11 910 B, sha256 `fc5d9fc6…30da34` |
| S093 | https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/v2/tasks/instance_internetarchive__openlibrary-00bec1e7…/tests/test.sh | "Resetting test-space to base state (full test-code surface)..." (8, `:33`); `T) git checkout HEAD -- "$path"` (`:71`); "success = all_required <= passed_tests" (5, `:214`) | 7 864 B, sha256 `b6f26eec…60976d0` |
| S093 | …/tests/parser.py | pattern at `:68`, `re.match` at `:71` and `:90`, dedupe at `:121` | 4 229 B, sha256 `303ceda2…0770b66` |
| S100 | https://raw.githubusercontent.com/laude-institute/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md | "uv run harbor run --dataset terminal-bench@2.0" (6, line 46) | 4 574 B, sha256 `7dfa9992…972364` |
| S100 | contents API for the same ref | 92 top-level entries — 89 dirs, 3 files (`.gitignore`, `LICENSE`, `README.md`); 301 → `harbor-framework/terminal-bench-2`, whose root tree sha equals the pin's tree | 96 537 B after redirect; `truncated` absent |

Quote mode over the landed rows: `python3 plans/sources_adopt.py --quote-file
.ufo/waves/round-31/assimilation/adopted-rows.txt --artifact .ufo/waves/round-31/assimilation/captures` →
`QUOTE rows=3 spans=7 located=7 found=7 overlong=0 absent=0 malformed=0`, exit 0
(`corpus/evidence/round31/quote-mode-adopted-rows.txt`), and the same run under `--url-map` →
`mismatch=0 unmapped=0 urlmap=capture-url-map.json entries=6`, exit 0 (`quote-mode-bound.txt`).

### Per-criterion record for the admitted entry (QUALITY Q1–Q19)

Q1 pass (triad at lines 1-6: three `source:` lines naming the row id **and** the pinned URL, `verified-at:
2026-10-25`, `recheck:` with an action, `writer: KengakuR31`); Q2 **pass with a stated bound** — S092/S093
are the code being described, S100 is the tree the count comes from, and the one sentence the entry carries
from a seat rather than from its own fetch (the 731-manifest sweep, the 88-of-89 script count) names that
seat and its report; Q3 pass (every quoted span ≤22 words with a location; the S092 description is quoted as
two spans because the file concatenates four literals); Q4 pass (§What this does not establish, six bullets,
plus a falsifier naming the unit and the observation); Q5 pass (S092/S093/S100 are primary code and tree
artefacts, not self-reports, and the entry says so); Q6 pass (§Extends names the checklist's axis E, its
`:71-74` rule and its `:94-95` gap, and states that it does not revise the SWE-bench Pro row); Q7 pass (entry
+ index row + coverage row + frontier sub-bullet in one commit); Q8 pass (this Gate: one admit, four rejects,
each with a flip); Q9 pass (each rejection's reason addresses the property it rejects — Q3, Q2, theme, theme);
Q10–Q15 by the falsify reports cited in `.ufo/waves/round-31/falsify/`; Q16–Q19 by the wave evidence and the
seat ledger below. **The bar row that fails is Q2's stronger reading**: the 731-manifest sweep is a seat's
measurement, not mine, and the entry says so instead of presenting it as its own.

### Non-author spot-check

Pending: the round's closure is a non-author pass and will re-open a sample of this Gate (one admit, one
reject). This lane's own seats cannot satisfy it. Recorded here so the closure has the pointer.

## Assimilation record (contract §10)

- **Theme**: how a benchmark's verifier runs and what it restores — one entry, three rows.
- **Collision guard**: proved on a scratch indented-row fixture (above), and the adopted ids were disjoint
  from the 12 collisions.
- **Scratch validation before append**: the three rows were checked with the gate's scoped mode and with
  quote mode before they landed; the census was run on the appended tree before commit.
- **Quarantine slice** (`absent-defect-register.md`, read-only, lane slice re-derived with the §10 awk):
  **2 data rows** — `S091` and `S105`, both `payload-absent`. Verdicts: **neither is appendable and neither
  is used this round** — no admitted entry cites them, and their payload-absent class means the register
  records a row whose source could not be fetched. `unreachable` is not fabrication; both stay unadopted and
  the flip is "a round that fetches the payload and locates a quote".
- **considerthese**: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/considerthese/2026-10-24.md` proposal 2
  ("put an as-of date and a live/dead status on every knowledge entry") is the one proposal this round
  grounds, as `QUALITY.md` **Q21** — measured absence: 5 of 40 knowledge entries name a pinned revision in a
  `source:` line and 5 of 40 name one in `recheck:` (`grep -lE '^source:.*[0-9a-f]{40}' corpus/knowledge/*.md
  | wc -l` → 5; `grep -lE '^recheck:.*(commit|pinned|pin)' corpus/knowledge/*.md | wc -l` → 5, both
  2026-10-25). The round's own entry is one of the five.
- **Source repo**: `/home/vgpnk/Projects/shokuknow` was read only; no campaign tool was run there.

## Census

- before: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0, 14 `W04`,
  88 rows, 39 knowledge files, 39 index rows (`.ufo/waves/round-31/claims/census-before.txt`).
- after: same command → exit 0, **15** `W04`, 91 rows, 40 knowledge files, 40 index rows
  (`corpus/evidence/round31/census-after.txt`). The 15th warning is `S100 duplicate url
  github.com/laude-institute/terminal-bench-2 across scopes` — the same repository S079 already carries,
  read for a different scope (task-package schema vs release identity and verifier execution). It is a
  warning under the census contract, not an `E` finding, and it is disclosed in the row's own `scope` cell
  and in the round report.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| `vacuous` — the C1 counter prints its pass line for a 63-byte stub | `.ufo/waves/round-31/build/R31CritC1.md` (fixtures V1/V2b/V3/V4b), reproduced by `R31RevClaims.md` | none: the frozen predicate names `adoption_check.py`, which reads the entry only twice | second receipt `plans/round31_c1_verify.py` (frozen path, access-date literal, per-row citation identity, pinned revisions, index-title substance, control digest) → `checks=6 defects=0`; the frozen counter stays the claim's line, the second receipt is the content check |
| `survivor` — the C2 counter greened its own repair | `R31DefR6.md` (substring trap), `R31DefR7.md` (two-string guard), `R31CritC2.md` (ten survivors) | none: the counter had only red-on-empty selftest cases | R6 parses the counted form and re-derives the number; R7 tests three substantive conditions; R1/R2/R3/R10 add an append-only `git diff --numstat` test; R4/R5 strip zero-width characters; R8 reads registry **cells**; R9 refuses a blob shorter than the baseline's. The remaining survivor class (m3/m4/m5 of `R31MutCounter.md`) is disclosed debt: the selftest still feeds no non-empty violating tree |
| `number-drift` — a counter demanded 3 where the registry gives 2 | `R31DefR6.md` §c: S001 carries `…/2026.gem-main.50/` while the staged row cites `…/2026.gem-main.50.pdf` | the entry's own `:160` already said "two of its three" | `document_key()` compares documents, not byte URLs — a `.pdf` locator and its landing page are one document |
| `landing` — the C3 landing made quote mode unreachable while the selftest stayed green | `R31GateDesign.md` (md5 `fcd357da`), `R31SimplGate.md`, `R31GateFixture.md` | none: `--selftest` never drove `main`, so the tally could not see a dead CLI | the `elif` was removed, the guard moved after the quote-mode body, and a selftest case now drives `main` and asserts its exit 2 (with stderr redirected, so the receipt stays 2>&1-clean) |
| `reference-drift` — a landed row's quote was not a byte substring | `R31DraftGate.md` §gates: S092 `7` findings, because the config description is four implicit literals | Q3's "a quote names its location" did not say *substring* | the row quotes two spans that are substrings; quote mode over the landed rows now reads `spans=7 located=7 absent=0` |
| `scope` — the round named its surface as "runtime task validity", which `PROVINCE.md` refuses | `R31EntryScope.md` §a: the ground actually moved is the frontier's "their scoring code was not read and stays open" | none: the claims file was written before the scope seat reported | the entry and the README frontier sub-bullet name the scoring-code clause and say "not runtime task validity"; the claims file is frozen and is not rewritten, so the report carries the correction |
| `landing` — five round-30 seat reports sat uncommitted through that round's closure | `R31DefR9.md` (numstat), `R31Revenger.md` (the wave validator renders one fixed report path and never seals it) | round 30's own D4 check tested one wave path, not the round's tree | committed as authored under this round's entry (R9's counter check), and the structural fix is routed: a wave-evidence freeze (write-once report path, post-return revisions at `<name>.r2.md`) plus `reportSha256` in the registry — operator-side, named in the report |
| `provider` — `/tmp` was full at round start (128 G tmpfs at 100 %) | `df -h /tmp` → 356 K available; `du -sh /tmp/r30fx-kengakuPred` → 36 G from a round-30 seat | none | kengaku's own round-30 scratch was deleted (≈47 G freed, `df` → 6.6 G); every wave `context` now forbids `git clone` and caps scratch at 60 MB. The remaining pressure is other lanes' live scratch, which this lane must not delete |
| `number-drift` — round 30's falsify receipt prints a tier histogram that is stale | `R31ReconCensus.md`: `R30FxRowsCensus.md:107` and `R30FxEvidence.md:108` say `A 79 / B 7 / C 2`; the registry and three independent readings say `A 78 / B 8 / C 2` | nothing re-ran those receipts after `9af639c` relabelled S086 A→B | recorded here and routed; the round-30 seat reports are committed as authored (rewriting another seat's verdict is not this round's repair) |

## Seat ledger

| wave | seats | roles | attack share | dead seats |
|---|---|---|---|---|
| build | 36 | scout 12, reviewer 10, critic 4, scribe 3, executor 2, mutation-tester 2, connector 1, revenger 1, simplifier 1 | 16/36 (reviewer+critic+mutation-tester) = 44 % | none |
| falsify | 36 | reviewer 13, critic 11, scout 7, mutation-tester 4, revenger 1 | 28/36 (reviewer+critic+mutation-tester) = 78 % | none |

Registries: `.ufo/waves/round-31/build/swarm-registry.json`, `.ufo/waves/round-31/falsify/swarm-registry.json`
(36 + 36 members, every one with its agent id recorded). The planner seat is the L1's (the validator rejects
`planner`); the bounded planning data-walk rode the scout item `R31PlanWalk`.

## Falsify-wave findings that changed landed bytes (appended after the wave returned)

- **The entry's `DATA_DIRS` sentence was half false.** `R31FxQuoteS093.md` found the third pass at
  `test.sh:97-104` (a `*fixtures/*` case whose `git checkout HEAD -- "$p"` restores *edited* tracked
  fixtures) and executed the replay; the entry now says the hole is **additions**, not edits, and cites the
  pass. Class `survivor` — the sentence was written from a partial read of the same file the entry quotes.
- **The general "shared mode is leaky" fact was already in-lane.** `R31FxPriorArt.md` found S077
  (`TASK_REVIEW_AUTOMATION.md:183`) stating it verbatim before this round; the entry now cites S077 for the
  general fact and claims only the per-benchmark application and the restore facts. Class `attribution`.
- **"Unless a task opts in" is per verify pass, not per task** (`R31FxSharedMode.md`): a multi-step task mixes
  modes per step, and regrade refuses shared-mode tasks; both are now in the entry.
- **The freeze was not committed before the data** (`R31FxClaimsOrder.md`): the claims text existed on disk at
  05:45:26, before every seat report and its own control receipts, but first entered git at 06:01:13 in the
  landing commit. The claim "frozen BEFORE any wave seat ran" is true of the file's birth time and false of
  the commit history. Class `landing`; the fix for the next round is a freeze commit of its own before the
  first dispatch — recorded here rather than silently relied on.
- **"91 rows" overstates the registry's distinct sources** (`R31FxS100Dupe.md`): the 15 `W04` are occurrences,
  not defects, and the effective distinct-URL count is ≈73 (≈71 with the own-work aliases). The census also
  cannot see the S078↔S093 same-repo-same-pin pair because the hosts differ. Disclosed in the report.
- **A fourth wrong cell in round 30's lesson is left standing** (`R31FxLessonDraft.md`):
  `corpus/lessons/round-30.md:66` still calls S083/S086 "peer-reviewed" while the registry row records that the
  society publishes without peer review. It is outside the frozen R-list, so it is recorded as debt here and
  not silently corrected — an erratum is owed by the next round that touches that lesson.
- **The C2 counter's R6 and R8 checks were a false positive and a false green** (`R31FxC2R6R8.md`):
  R6 required the byte-exact landed sentence, so an honest paraphrase of the entry's own §Extends sentence
  (`:163`) reddened it; R8 scanned every cell of every row, so a scope cell mentioning CC0 greened an
  ungrounded entry. R6 now tests only the *bare* assertion ("its three source rows are not in this lane's
  registry"), and R8 grounds a licence token only in a row's `source` or `anchor` cell. Both receipts were
  regenerated from the tightened bytes: before `defects=10` exit 1, after `defects=0` exit 0.
- **R9's line-count test is a stub heuristic, not an integrity invariant** (`R31FxC2R9.md`): a 120-line stub
  is caught, but a revert, a one-line append and an identical delete/re-add survive. Named debt.

## Final instrument verdict on C2 (appended after the last falsify seat returned)

`R31FxC2Survivors.md` re-ran the ten fakeability routes against the **final** counter bytes and every one of
R1–R10 still has a route that prints `defects=0` without the underlying mismatch being repaired — appending
the right wording beside the unrepaired sentence, a reworded copy, a row-cell licence injection, and R9 by the
very revert the kill rule forbids. Three of the earlier routes are now killed (the in-place rewrite, the
zero-width-character copy, the stub blob), so the counter is strictly stronger than at the freeze, and it is
still **not** an instrument that proves its own closure: `defects=0` is necessary evidence, and the closure's
proof is the byte-level review the seats did (`R31DefR1.md`, `R31DefR2R3.md`, `R31DefR4R5.md`, `R31DefR6.md`,
`R31DefR7.md`, `R31DefR8.md`, `R31DefR9.md`, `R31DefR10.md`), each of which re-derived its item from committed
bytes and re-printed the quoted window. C2's verdict is therefore carried by that review plus the counter, and
the counter's inadequacy is stated here rather than implied by a green line.


## Corrections (round 33, appended — the filed bytes above stand as written)

- **verifier_mode.py precedence locator (routed defect N5).** The Gate row at `:57` cites the
  precedence docstring at `:35-38`; after the entry's locator repair (`ae95fe0`) the verifier_mode.py
  precedence docstring is at `:39-40` (verifier_mode.py ... :39-40, this correction) — this
  correction supersedes the `:35-38` citation while the
  stale line is kept verbatim per append-only. Evidence: `git show ae95fe0 --stat`.
