# C2ExecSourceResolve — line-level source resolution, all 71 ledger rows

Seat: `C2ExecSourceResolve` (executor), kengaku round 51, hyaku run 11.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Read-only against the lane; this file is
the seat's only lane write. Scratch `/fast/scratch/hyaku/kengaku-r51/C2ExecSourceResolve` was
created, used as `TMPDIR`, and removed before yield (see §10).

## 1. Axes named

- **Adjacency (8 → 9) — the axis this seat feeds.** R51-C2's predicate has a `SOURCE` leg that
  must report `missing=0`. This seat measures the leg the counter *does not* have: whether each
  `path:line` pointer lands on text that carries the finding. Evidence here is the SOURCE leg's
  soundness evidence for the C2 after-measurement.
- **Freshness (8 → 9)** — not touched. This seat read no `PROVINCE.md` surface row and ran no
  C1 probe; no C1 claim depends on this report.

## 2. Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

`git rev-parse HEAD` at measurement. Stage-1 freeze `e07f131cf7037e58a21db6e1f3986cf401ad257c`;
`git diff --stat e07f131 4090c3d` touches only `.ufo/waves/round-51/{build_spec.py,w1-dispatch.json,w1-spec.json}`
(1743 insertions, 0 deletions), so no tracked source file moved between the freeze and this
measurement. `git status --porcelain` showed only untracked `.ufo/waves/round-5{0,1}/` wave files;
the working tree equals HEAD for every file this seat read (verified per row, §3.2).

## 3. Commands run and verbatim output

### 3.1 Frozen counter, for the record

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ TMPDIR=/fast/scratch/hyaku/kengaku-r51/C2ExecSourceResolve \
  python3 plans/round51_routing.py --lane . --run-checks
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
counter_exit=1
```

Identical to `.ufo/waves/round-51/claims/c2-before.txt` at the base tip, including
`SOURCES resolved=71 missing=0`. `VERIFIED ran=0` because no row carries a `disposition` yet, so
no ledger `check` command executed in this run.

### 3.2 Line resolution (the stricter leg)

Every one of the 71 `source` values has exactly one `:`, a numeric line, and a path that is a
file (no directory-only or bare-path pointers):

```
all sources single-colon
TOTAL 71
```

For each row the cited line was read from the **committed** blob (`git show HEAD:<path>`) and from
the worktree; both must agree and the line index must be `<= nlines`:

```
checked=71 committed_line_mismatch=0
```

So: **71/71 lines exist** — no out-of-range line, no blank line cited, no cited line that differs
between HEAD and the worktree.

### 3.3 What the counter would miss — four fixtures

The counter's leg is `src = source.split(":")[0]; if not src or not (lane/src).exists()`. It never
opens the file and never parses the line. Four fixtures, each a scratch copy of the real ledger
plus the 15 real source files under `<scratch>/fixture/lane/`, run through the same frozen counter:

```
### fixture: every cited line out of range (99999)
LEDGER corpus/routed-findings.jsonl rows=71
SOURCES resolved=71 missing=0
PREDICATE R51-C2 fail

### fixture: every cited line pinned to line 1 (unrelated text)
LEDGER corpus/routed-findings.jsonl rows=71
SOURCES resolved=71 missing=0
PREDICATE R51-C2 fail

### fixture: source is a DIRECTORY inside the lane
LEDGER corpus/routed-findings.jsonl rows=71
SOURCES resolved=71 missing=0
PREDICATE R51-C2 fail

### fixture: source escapes the lane (../escape.txt)
LEDGER corpus/routed-findings.jsonl rows=71
SOURCES resolved=71 missing=0
PREDICATE R51-C2 fail

### fixture: source has no line number at all
LEDGER corpus/routed-findings.jsonl rows=71
SOURCES resolved=71 missing=0
PREDICATE R51-C2 fail
```

(The predicate fails in each fixture only on the pre-existing `FIELDS`/`OWNER`/`DISPOSITION`
legs, which are untouched by the mutation; the `SOURCES` leg stays green in all five shapes.)
Concretely, the counter would accept, at `SOURCES missing=0`:

1. a line number past EOF (`:99999`),
2. a line number pointing at unrelated text (`:1`),
3. a pointer to a **directory** (`corpus`),
4. a pointer that **escapes the lane** (`../escape.txt`, resolved through `lane/src`),
5. a pointer with **no line at all** (no `path:line` shape required).

On this corpus none of those shapes occur (§4: 71/71 exact), so the counter's green SOURCE leg is
not *false* at this tip — it is *unfalsifiable* by construction. That is the gap this seat closes
with row-by-row evidence rather than a counter change: the C2 predicate as frozen cannot tell an
exact pointer from a drifted one.

### 3.4 Clean-clone safety of the pointers

The claims measure the after-predicate "at the landing tip in a clean clone". Every source file
must therefore be tracked. `git ls-files --error-unmatch` on each of the 15 distinct files:

```
TRACKED   .ufo/waves/round-42/falsify/F42ConnClaims.md
TRACKED   .ufo/waves/round-42/falsify/F42CritAdv.md
TRACKED   .ufo/waves/round-42/falsify/F42CritPlanNext.md
TRACKED   .ufo/waves/round-42/falsify/F42CritScorecard.md
TRACKED   .ufo/waves/round-42/falsify/F42EntryQuotes.md
TRACKED   .ufo/waves/round-42/falsify/F42RevC2Package.md
TRACKED   .ufo/waves/round-42/falsify/F42RevLesson.md
TRACKED   .ufo/waves/round-42/falsify/F42RevQuality.md
TRACKED   .ufo/waves/round-42/falsify/F42RevRiders.md
TRACKED   SKILL.md
TRACKED   corpus/lessons/round-39-verifier-spotcheck.md
TRACKED   corpus/lessons/round-40-verifier-spotcheck.md
TRACKED   corpus/lessons/round-41-verifier-spotcheck.md
TRACKED   corpus/lessons/round-45-verifier-spotcheck.md
TRACKED   plans/scratch_guard.py
```

15/15 tracked → a clean clone at the landing tip keeps all 71 pointers resolvable. Last-touch
commits (all ≤ 2026-10-27, none after this wave started):

```
f9bbee6:2026-10-26  .ufo/waves/round-42/falsify/*.md (9 files)
02287ee:2026-10-26  SKILL.md
d8fad16:2026-10-26  corpus/lessons/round-39-verifier-spotcheck.md
e50c134:2026-10-26  corpus/lessons/round-40-verifier-spotcheck.md
d69452c:2026-10-26  corpus/lessons/round-41-verifier-spotcheck.md
64ba838:2026-10-27  corpus/lessons/round-45-verifier-spotcheck.md
ff14d76:2026-10-26  plans/scratch_guard.py
```

## 4. Per-row classification — 71 rows

Method: open the cited file, read the cited line from the committed blob, quote it (≤25 words),
and judge whether that text plausibly carries the row's `class`/`note`. All rows resolve to a line
whose text names the row's own finding (the `D<n>`/`R<n>`/`S5-<n>` marker in the quote is the
finding's own label, and the class is the finding's own slug).

**Totals: `exact 71`, `drifted 0`, `missing 0`.** 67 distinct `path:line` pointers over 15 files.

| id | source | nlines | cited line (≤25 words) | verdict |
|---|---|---|---|---|
| R39-R1 | `corpus/lessons/round-39-verifier-spotcheck.md:132` | 147 | - R1 Register `plans/order_check.py` (gate) and `plans/round39_c1_audit.py` in `SKILL.md` §Gate/probe registry with verdict | exact |
| R39-R2 | `corpus/lessons/round-39-verifier-spotcheck.md:134` | 147 | - R2 `plans/git_leak_probe.py --work DIR`: create the dir or exit 2 with a setup message; declare it in the registry row (D3). | exact |
| R39-R3 | `corpus/lessons/round-39-verifier-spotcheck.md:135` | 147 | - R3 Write the order class to `corpus/defects.jsonl` with `recurrence=2` through a separately frozen `defect_ledger` check (D4). | exact |
| R39-R4 | `corpus/lessons/round-39-verifier-spotcheck.md:136` | 147 | - R4 Carried residuals the lane already routed: `order_check.py` 2/6 mutants and the fail-open mid-scan git error | exact |
| R39-R5 | `corpus/lessons/round-39-verifier-spotcheck.md:140` | 147 | - R5 Seat scratch hygiene: the two leftover seat dirs (D5). | exact |
| R40-R1 | `corpus/lessons/round-40-verifier-spotcheck.md:92` | 105 | - **R1** C1 counter soundness (frozen, gameable): `R40CritC1Counter` A1/A2, `R40SentinelCounter` (host fs writable), `R40RevCounters` | exact |
| R40-R2 | `corpus/lessons/round-40-verifier-spotcheck.md:95` | 105 | - **R2** Host-safety (D1): no seat may write outside the lane scope or scratch; keep the read-only `~/.local/bin` sandbox for | exact |
| R40-R3 | `corpus/lessons/round-40-verifier-spotcheck.md:97` | 105 | - **R3** Register `plans/round_close.py` as a gate row (verdict map, self-test, pinned values) and give the `tip_receipts.py` | exact |
| R40-R4 | `corpus/lessons/round-40-verifier-spotcheck.md:99` | 105 | - **R4** The "advertised behaviour" count: 4 of 21 frozen mutants are not advertised (`F40CritC1Count`); the round-41 freeze | exact |
| R40-R5 | `corpus/lessons/round-40-verifier-spotcheck.md:101` | 105 | - **R5** Carried: R3-from-r39 (order class into a separately frozen ledger), `F39LedgerTip` D1, `F39MutDirection`, | exact |
| R42-R1 | `corpus/lessons/round-41-verifier-spotcheck.md:105` | 123 | - **R1** C1 counter soundness residuals (`R41SentinelCounter` F1–F4: variant readable inside a tool run, AF_UNIX, SysV IPC, relative | exact |
| R42-R2 | `corpus/lessons/round-41-verifier-spotcheck.md:110` | 123 | - **R2** Scratch hygiene (D1): no seat may delete outside its own `$SCR/<SeatName>`; give the round root a guard the seats cannot | exact |
| R42-R3 | `corpus/lessons/round-41-verifier-spotcheck.md:114` | 123 | - **R3** C2 filler admission: the frozen V1–V8 pass a content-free package (`R41CritClaims` D2); the round-42 C2 counter needs a | exact |
| R42-R4 | `corpus/lessons/round-41-verifier-spotcheck.md:116` | 123 | - **R4** SOURCES rule 2 (D2): correct a non-mutable cell by a new row opening `supersedes S0NN —`, never in place. | exact |
| R42-R5 | `corpus/lessons/round-41-verifier-spotcheck.md:117` | 123 | - **R5** Carried: 14 `round_close.py`/`tip_receipts.py` residuals (`R41RoundCloseMut`), `F39LedgerTip` D1, `F39MutDirection`, | exact |
| R40-R1.1 | `corpus/lessons/round-40-verifier-spotcheck.md:92` | 105 | - **R1** C1 counter soundness (frozen, gameable): `R40CritC1Counter` A1/A2, `R40SentinelCounter` (host fs writable), `R40RevCounters` | exact (shared anchor with R40-R1) |
| R42-R2.1 | `corpus/lessons/round-41-verifier-spotcheck.md:110` | 123 | - **R2** Scratch hygiene (D1): no seat may delete outside its own `$SCR/<SeatName>`; give the round root a guard the seats cannot | exact (shared anchor with R42-R2) |
| R42-R2.2 | `SKILL.md:562` | 1338 | \| name \| kind \| entry \| verdict map \| self-test \| pinned values \| write scope \| owner \| | exact — **absence anchor**, see §5.1 |
| R42-R6 | `plans/scratch_guard.py:17` | 622 | Exit 1 when the sentinel is missing, unparseable, or names another round; exit 2 when | exact |
| R42-R3-01 | `.ufo/waves/round-42/falsify/F42RevC2Package.md:71` | 148 | **D1 (content — false arithmetic clause) — `corpus/knowledge/tb2-circuit-fibsqrt-grader.md:297`.** | exact |
| R42-R3-02 | `.ufo/waves/round-42/falsify/F42RevC2Package.md:80` | 148 | **D2 (SKILL row line reference wrong for V7) — `SKILL.md:600`.** | exact |
| R42-R3-03 | `.ufo/waves/round-42/falsify/F42RevC2Package.md:86` | 148 | **D3 (internal inconsistency) — entry:96.** | exact |
| R42-R3-04 | `.ufo/waves/round-42/falsify/F42RevC2Package.md:93` | 148 | **D4 (citation location) — entry:311.** | exact |
| R42-R3-05 | `.ufo/waves/round-42/falsify/F42RevC2Package.md:98` | 148 | **D5 (line-ref off-by-one) — entry:350.** | exact |
| R42-R3-06 | `.ufo/waves/round-42/falsify/F42RevC2Package.md:102` | 148 | **D6 (provenance label) — `corpus/README.md:75`.** | exact |
| R42-R3-07 | `.ufo/waves/round-42/falsify/F42RevC2Package.md:109` | 148 | **D7 (overstated check description) — `SKILL.md:684-685`.** | exact |
| R42-R3-08 | `.ufo/waves/round-42/falsify/F42RevC2Package.md:116` | 148 | **D8 (undeclared dependency in the frozen gate) — `plans/pkg_gate.py:273-276` + `SKILL.md:686-687`.** | exact |
| R42-R3-09 | `.ufo/waves/round-42/falsify/F42RevC2Package.md:124` | 148 | **D9 (nit) — entry:328.** | exact |
| R42-R3-10 | `.ufo/waves/round-42/falsify/F42RevLesson.md:102` | 180 | **D1 (moderate) — R4's measured claim is false at the docs tip.** Lesson R4: "`git diff bc856d8..HEAD -- corpus/SOURCES.md` | exact |
| R42-R3-11 | `.ufo/waves/round-42/falsify/F42RevLesson.md:109` | 180 | **D2 (moderate) — R5's "named carried again in the freeze (§Limits)" is not true for the F39 trio.** `plans/round-42-claims.md` | exact |
| R42-R3-12 | `.ufo/waves/round-42/falsify/F42RevLesson.md:118` | 180 | **D3 (moderate) — L1 row 4's decisive number is unpersisted, and its role list doesn't match wave 2.** The quoted | exact |
| R42-R3-13 | `.ufo/waves/round-42/falsify/F42RevLesson.md:128` | 180 | **D4 (minor) — `fibsqrt-probe.txt:6` cited twice for content that lives at `:23-24`.** The Gate prose and the | exact |
| R42-R3-14 | `.ufo/waves/round-42/falsify/F42RevLesson.md:134` | 180 | **D5 (minor) — `round42_c2_verify.py:327` off by one.** R3 cites ":327" for "V9 is the ninth check"; the checks-list | exact |
| R42-R3-15 | `.ufo/waves/round-42/falsify/F42RevLesson.md:137` | 180 | **D6 (minor) — the census command as printed does not produce the quoted numbers.** The lesson cites | exact |
| R42-R3-16 | `.ufo/waves/round-42/falsify/F42RevLesson.md:142` | 180 | **D7 (minor) — `Dockerfile:9-10` is one line off.** The README-reject row says "`Dockerfile:9-10` copies only | exact |
| R42-R3-17 | `.ufo/waves/round-42/falsify/F42RevLesson.md:146` | 180 | **D8 (low) — L1 row 3's fix has no failure receipt.** Every other Mistakes row names a persisted receipt that shows its | exact |
| R42-R3-18 | `.ufo/waves/round-42/falsify/F42RevQuality.md:13` | 160 | ### D1 — HIGH, both criteria: the executable checks point at tools that were never landed in any commit | exact |
| R42-R3-19 | `.ufo/waves/round-42/falsify/F42RevQuality.md:26` | 160 | ### D2 — HIGH, both criteria: the Check command lines do not match the tools' CLIs | exact |
| R42-R3-20 | `.ufo/waves/round-42/falsify/F42RevQuality.md:35` | 160 | ### D3 — MEDIUM, Q33: the red half's cited `PREDICATE C1 fail` line is not reachable under the check's own instruction | exact |
| R42-R3-21 | `.ufo/waves/round-42/falsify/F42RevQuality.md:50` | 160 | ### D4 — MEDIUM, Q34: the pipe-in-cell sentence is false as written, and its evidence is an invalid inference | exact |
| R42-R3-22 | `.ufo/waves/round-42/falsify/F42RevQuality.md:67` | 160 | ### D5 — LOW, Q34: wrong line pin for `registry_check.py` | exact |
| R42-R3-23 | `.ufo/waves/round-42/falsify/F42RevQuality.md:73` | 160 | ### D6 — LOW, Q34: "No lane tool reads it from committed history" is self-undermining as landed | exact |
| R42-R3-24 | `.ufo/waves/round-42/falsify/F42RevRiders.md:121` | 203 | **D1 (defect, ledger): R42-R4's check passes at the landing while the row says open — the ledger's | exact |
| R42-R3-25 | `.ufo/waves/round-42/falsify/F42RevRiders.md:133` | 203 | **D2 (defect, stale check): R42-R2's clause 3 pins the uncommitted build copy, not the landed | exact |
| R42-R3-26 | `.ufo/waves/round-42/falsify/F42RevRiders.md:74` | 203 | **D3 (defect, doc/behavior): `check` on a root whose sentinel is unreadable exits 1; the docstring | exact |
| R42-R3-27 | `.ufo/waves/round-42/falsify/F42RevRiders.md:85` | 203 | **D4 (defect, selftest coverage): the 36-case selftest has no unreadable-sentinel `check` case.** | exact |
| R42-R3-28 | `.ufo/waves/round-42/falsify/F42RevRiders.md:157` | 203 | **D5 (defect, integration): the landed guard has no SKILL.md registry row.** | exact |
| R42-R3-29 | `.ufo/waves/round-42/falsify/F42CritAdv.md:30` | 175 | ## 3. X3 — verbatim quote and cite check | exact |
| R42-R3-30 | `.ufo/waves/round-42/falsify/F42CritAdv.md:53` | 175 | ## 4. X7 — verbatim quote and cite check | exact |
| R42-R3-31 | `.ufo/waves/round-42/falsify/F42CritScorecard.md:66` | 93 | **M1 (minor, overstatement).** SCORECARD §Round42 “Envelope note: under the v1 envelope (home read-only) | exact |
| R42-R3-32 | `.ufo/waves/round-42/falsify/F42ConnClaims.md:34` | 48 | ## 2. Drift 1 — measure-final's own Q32 envelope records a CHANGED `~/.local/bin` listing | exact |
| R42-R3-33 | `.ufo/waves/round-42/falsify/F42CritPlanNext.md:56` | 139 | ### D1 — mutant-list numerator is unbound: "20 rc-witnessed survivors" vs 11 witnessed / 9 directional | exact |
| R42-R3-34 | `.ufo/waves/round-42/falsify/F42CritPlanNext.md:69` | 139 | ### D2 — Q33 carried-cell red control is not specified for the u=18 branch | exact |
| R42-R3-35 | `.ufo/waves/round-42/falsify/F42CritPlanNext.md:79` | 139 | ### D3 — the dishonest-green vectors of R42CritC1Counter (XO1/XO3/X13 substitutes; V2b symlink escape) are absent from the round-43 counter plan | exact |
| R42-R3-36 | `.ufo/waves/round-42/falsify/F42CritPlanNext.md:91` | 139 | ### D4 — coverage class sentence is asserted from a non-frozen host probe; prior-art hits exist for this exact task | exact |
| R42-R3-37 | `.ufo/waves/round-42/falsify/F42CritPlanNext.md:107` | 139 | ### D5 — `cheat-clock-seed` is glibc/platform-dependent; the "5/5" is a host result | exact |
| R42-R3-38 | `.ufo/waves/round-42/falsify/F42EntryQuotes.md:45` | 61 | 1. **entry:297 — wrong.** "maximum, 48401 = 220²+1, is the only reach above 2^15" (finding 7). Six of the 28 graded inputs lie above 2^15 | exact |
| R42-R3-39 | `.ufo/waves/round-42/falsify/F42EntryQuotes.md:46` | 61 | 2. **entry:311 — wrong (fact and locator).** "the probe runs every case with stdin on `/dev/null` (probe docstring — the oracle case's own `solve.sh` recipe | exact |
| R42-R3-40 | `.ufo/waves/round-42/falsify/F42EntryQuotes.md:47` | 61 | 3. **entry:431 — overclaim.** "`lookup-28-padded-31999` and `lookup-28-padded-32000` … so they too pass only because the print window is the 32 highest-indexed signals" (integration, D2 bullet). | exact |
| R42-R3-41 | `.ufo/waves/round-42/falsify/F42EntryQuotes.md:48` | 61 | 4. **entry:433-434 — wrong under the bullet's own counterfactual.** "they would carry `last-32-lines` and `line-form` as well … Neither changes a requirement-map label (`last-32-lines` and | exact |
| R45-S5-1 | `corpus/lessons/round-45-verifier-spotcheck.md:145` | 159 | 1. Supersede S152, S153, S154 under Q34 with correct anchor lines/ranges and a verbatim S154 `teaches`; add the | exact |
| R45-S5-2 | `corpus/lessons/round-45-verifier-spotcheck.md:147` | 159 | 2. Mark or supersede the entry's `## Predictor` (lone-CR divergence; prose at `:150,:194` overclaims universal newline) | exact |
| R45-S5-3 | `corpus/lessons/round-45-verifier-spotcheck.md:149` | 159 | 3. LOG.md: append a correction entry for the two in-place rewritten round-45 lines (D1); never rewrite committed LOG lines. | exact |
| R45-S5-4 | `corpus/lessons/round-45-verifier-spotcheck.md:150` | 159 | 4. Lesson Gate: record the ≤25-word quote + location per new row (D2). | exact |
| R45-S5-5 | `corpus/lessons/round-45-verifier-spotcheck.md:151` | 159 | 5. Receipts name the revision measured inside the receipt bytes (D3); run the frozen counters at the tip that ships the report. | exact |
| R45-S5-6 | `corpus/lessons/round-45-verifier-spotcheck.md:152` | 159 | 6. Name every post-freeze claims-file edit (`52d7486`) in the amendment paragraph (D4). | exact |
| R45-S5-7a | `corpus/lessons/round-45-verifier-spotcheck.md:153` | 159 | 7. Carried, lane-owned: re-freeze the C1 counter under Q39 with the held-out modules as frozen refusals; | exact |
| R45-S5-7b | `corpus/lessons/round-45-verifier-spotcheck.md:154` | 159 | `R45CritV11Bypass` lookup predictors; `R45SentC2Grader` F1 (P10 unpinned `uv` fetch) and F2/F3 (P9); `R45CritIntent` | exact (shared anchor with R45-S5-7c) |
| R45-S5-7c | `corpus/lessons/round-45-verifier-spotcheck.md:154` | 159 | `R45CritV11Bypass` lookup predictors; `R45SentC2Grader` F1 (P10 unpinned `uv` fetch) and F2/F3 (P9); `R45CritIntent` | exact (shared anchor with R45-S5-7b) |
| R45-S5-7d | `corpus/lessons/round-45-verifier-spotcheck.md:155` | 159 | brace-prefix bypass; re-attack the two unattacked mutation items (D5). | exact (shared anchor with R45-S5-7e) |
| R45-S5-7e | `corpus/lessons/round-45-verifier-spotcheck.md:155` | 159 | brace-prefix bypass; re-attack the two unattacked mutation items (D5). | exact (shared anchor with R45-S5-7d) |

Two-line context was checked for every lesson bullet (`round-39:129-142`, `round-40:89-102`,
`round-41:103-118`, `round-45:143-156`): each cited line is the bullet's own first line or the
continuation line carrying that finding's label, not a neighbouring bullet. The 14 `### D<n>` /
`## <n>. X<n>` cites in `.ufo/waves/round-42/falsify/` are section headings whose own text names
the finding — legitimate anchors, and the only heading-shaped cites in the ledger.

## 5. Findings the counter would miss, and two weak spots

### 5.1 The single "absence anchor" — R42-R2.2 (`SKILL.md:562`)

`SKILL.md:562` is the registry **table header**:

```
560: ## Gate/probe registry (PROTOCOL §Gate standard)
562: | name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
564: | `hermetic-grader` | gate | ...
```

The finding is "the landed guard has no SKILL.md registry row" — an absence in the table that
starts at `:562`, so the pointer names the right *site* but no text that carries the finding. A
quote-based resolution check finds nothing to quote here; the counter's file-existence leg cannot
tell the difference either way. **The registry row now exists at `SKILL.md:608`**
(`| `scratch-root-guard` | gate | ...`, `grep -c -E 'scratch[_-]guard' SKILL.md` → `1`), 46 lines
below the cited anchor — that is the nearest line carrying the row's resolution, and the line a
re-anchor should use if the L1 touches this row. Classified `exact` because the anchor is the
table the finding is about; it is `drifted` under a quote-required reading, so both readings are
recorded rather than hidden.

### 5.2 Duplicate line anchors (4 pairs, 71 rows → 67 distinct pointers)

```
2 corpus/lessons/round-40-verifier-spotcheck.md:92  ['R40-R1', 'R40-R1.1']
2 corpus/lessons/round-41-verifier-spotcheck.md:110 ['R42-R2', 'R42-R2.1']
2 corpus/lessons/round-45-verifier-spotcheck.md:154 ['R45-S5-7b', 'R45-S5-7c']
2 corpus/lessons/round-45-verifier-spotcheck.md:155 ['R45-S5-7d', 'R45-S5-7e']
```

Each pair is a status-change row (`.1` suffix) or a bundle item that genuinely lives on the same
lesson line, and each line carries both findings, so no row is mis-anchored. Recorded because
C1's manifest has an `ANCHOR-DUP` leg and C2 has no duplicate-pointer leg at all: a future row that
copies a neighbour's pointer verbatim would pass every current leg.

## 6. What this changes for the landing (C2 after-measurement)

- The SOURCE leg will be green at the landing tip for any ledger that keeps these 71 pointers
  intact: 71/71 resolve at file **and** line level at `4090c3d`, and all 15 files are tracked, so
  the clean-clone measurement cannot lose them.
- **Do not introduce a source pointing into `.ufo/waves/round-51/`** unless the file is committed
  in the landing commit: the counter resolves against the working tree, but the claims measure the
  after-predicate in a clean clone, where an untracked wave artifact is absent and `SOURCE missing`
  goes to 1. No such pointer exists today (all 15 source files are round-42-or-earlier).
- If the L1 re-anchors R42-R2.2 while adding `owner`/`disposition`, use `SKILL.md:608`.
- The frozen C2 predicate cannot detect a drifted pointer (§3.3). If the axis is to hold at 9
  rather than merely print `pass`, the wave evidence in §4 is the only thing standing behind
  "every `source` pointer resolves" — the counter alone is not evidence for it.

## 7. Limits

- Point-in-time: measured at `4090c3d` in the working tree, cross-checked against the committed
  blobs of the same revision. A later edit to any of the 15 files can move a line; nothing here
  predicts that.
- "Plausibly carries the finding" is a reading, not a proof. For 70 rows the cited line contains
  the finding's own label and the row's class names the same thing; for R42-R2.2 the reading rests
  on the table context (§5.1) and is disclosed.
- This seat did not judge `owner`, `disposition`, `status`, `check`, `close` or `next` — other
  seats own those legs. `CHECKS absent=10` is quoted only as context from the frozen run.
- Historical drift (did the pointer land on the same text at the row's `opened_round`?) was not
  re-measured row by row; last-touch dates per file are recorded in §3.4 and every cited line's
  text is unchanged between HEAD and the worktree.
- No C1 surface row, probe or manifest entry was read or measured by this seat.

## 8. Tooling

No tool installed or upgraded: the measurement used the lane's `python3` and read-only `git`
(`log`, `show`, `ls-files`, `rev-parse`, `diff`, `status`). No pacman transaction, no network.

## 9. Scratch

`/fast/scratch/hyaku/kengaku-r51/C2ExecSourceResolve` (NVMe, well under any `/tmp` size concern);
`TMPDIR` exported there for every run; `rm -rf` of that directory was performed before yield and
is confirmed in the closing line below. Every path cited in this report is a lane path; no `/tmp`
or scratch path is cited as evidence. All fixture git/file operations were inside that scratch
directory and the frozen counter's own `tempfile` work dir, which it removes itself.

## 10. Cleanup confirmation

```
$ rm -rf /fast/scratch/hyaku/kengaku-r51/C2ExecSourceResolve
$ test -e /fast/scratch/hyaku/kengaku-r51/C2ExecSourceResolve && echo PRESENT || echo REMOVED
REMOVED
```

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

VERDICT: 71/71 ledger `source` pointers resolve at file AND line level at `4090c3d` and the cited
line plausibly carries its row's finding (exact 71, drifted 0, missing 0; 67 distinct pointers,
15 tracked files) — so the frozen C2 SOURCE leg (`resolved=71 missing=0`) is true at this tip, not
merely unfalsifiable; but the leg is blind by construction to out-of-range lines, wrong-but-
existing lines, directory pointers, lane-escaping pointers and line-less pointers (five scratch
fixtures each keep `SOURCES resolved=71`), and one row (`R42-R2.2`) anchors an absence at a table
header whose satisfying row is now `SKILL.md:608`. No lane production file was edited; scratch
removed.
