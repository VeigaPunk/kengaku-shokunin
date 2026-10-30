# SC3ArgvUniverse — independent entry-argv binding-leg scan (round 55, wave 1)

**Seat** `SC3ArgvUniverse` (scout) — an *independent* implementation of the frozen R55-C2
binding legs, written to cross-check `E13BindingScan`. No code was shared with that seat and
`plans/round55_c2_entryargv.py` did not exist in the lane when this scan ran (it is the round's
new counter, not yet landed).

**Lane** `/home/vgpnk/Projects/shokunin/kengaku-shokunin` @ `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`
(round-55 freeze commit, base tip `798f5e9e…`). **Date** 2026-10-30.

**Inputs** (sha256; identical at scan time and at write time — `git status --porcelain` on both
paths is empty):

| input | sha256 |
|---|---|
| `SKILL.md` | `31e6e69562ce409d5347182fe44c9ca5eb0735438884ab3933ea985cf1e47347` |
| `plans/round54-entrytruth.json` | `40a77a3baa10f8d96159b136083cc1de3f86c1b6515f318bb6fd6503216de5f7` |

**Scratch** `/fast/scratch/hyaku/kengaku-r55/SC3ArgvUniverse/` (deleted before yield).

## 1. Definition actually implemented

Taken from the frozen claim `plans/round-55-claims.md` (R55-C2, commit `80afa61`); this seat
implements the three *static* binding legs over the CURRENT pair, before the new counter exists.

- **Universe** — registry rows: `SKILL.md` §`## Gate/probe registry`, pipe table with 8 cells,
  parsed with the frozen grammar (backslash-escaped pipes split; separator row skipped; the
  `| name | kind | … |` header line is not a row). Parser cross-validated against the frozen r52
  counter, which prints `rows=79` = 78 registry rows + that header line. Ledger rows:
  `plans/round54-entrytruth.json` → `rows` (78). **Name sets are equal** — no missing row, no
  extra row, no duplicate name — so every registry row has exactly one ledger row and back.
- **L1 — ledger↔registry argv identity.** The first backtick span of the *entry* cell that
  carries a `python3` command is shlex-tokenised; its token list must equal the ledger row's
  `entry_argv` token list exactly. Mismatch → `ARGV-DEFECT`; no command span → `UNPARSED`; no
  ledger row → `LEDGER-MISSING`.
- **L2 — interpreter identity, no wrappers.** `argv[0]` must be a real interpreter
  (`python3` → `/usr/bin/python3`, `python` → `/usr/bin/python`, both resolved on this host);
  `uv`/`uvx`/`pipx`/`poetry`/`npx` as `argv[0]`, or any inline `-c…` program token, on either
  the registry side or the ledger side → `WRAPPER-DEFECT`.
- **L3 — no flag-prefix abbreviation.** A flag token (either side) that is **not a complete flag
  literal** in the entry script's own body but **is a proper prefix** of a longer flag literal
  in that body → `ABBREV-DEFECT` candidate. Static (script body read), no execution.

**Legs have teeth** — six positive controls (`--selftest`, 6/6 ok, exit 0): `ctl-equal`
(L1 equal), `ctl-abbrev` (`--selft` vs a body `--selftest` → L3 fires), `ctl-uv`
(`uv run …` → L2 fires), `ctl-inline-c` (`python3 -c "print(1)"` → L2 fires), `ctl-mismatch`
(L1 fires), `ctl-unparsable` (no span → UNPARSED).

## 2. Counts (today's freeze-state pair)

| measure | count |
|---|---:|
| registry rows | 78 |
| ledger rows | 78 |
| name-set mismatches (missing/extra/duplicate) | 0 |
| **L1** equal | 62 |
| **L1** ARGV-DEFECT | 16 |
| **L1** UNPARSED | 0 |
| **L1** LEDGER-MISSING | 0 |
| **L2** WRAPPER-DEFECT | 1 |
| **L3** ABBREV-DEFECT candidates | 0 |
| **rows flagged by ≥1 binding leg** | **17** |
| rows where registry and ledger name the same interpreter **and** the same script | 78 / 78 |

## 3. Full 78-row table

`ledger` = declared `entry_state`/`chosen` of the ledger row. `strict-r52-cmd` = whether the
entry cell's command also matches the r52 counter's frozen `CMD` shape
(`plans/<n>.py` | `corpus/evidence/<dir>/<n>.py` | `grader.py`; no hyphens in directory names).

| # | row | kind | ledger | strict-r52-cmd | L1 | L2 | L3 | note |
|---:|---|---|---|---|---|---|---|---|
| 1 | `hermetic-grader` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 2 | `coverage-census` | probe | green/r53-entry | NO | ARGV-DEFECT | ok | ok | flag-structure |
| 3 | `interval-reverdict` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 4 | `state-assertion-check` | gate | red/r53-entry | yes | equal | ok | ok |  |
| 5 | `grader-perturb` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 6 | `gate-timing` | gate | green/r53-entry | yes | ARGV-DEFECT | ok | ok | instantiation; cell-has-placeholder |
| 7 | `benchmark-spec-audit` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 8 | `registry-reference-check` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 9 | `config-projection` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 10 | `sources-adopt` | gate | red/bare | yes | ARGV-DEFECT | ok | ok | flag-structure |
| 11 | `package-gate` | gate | green/r53-entry | yes | ARGV-DEFECT | ok | ok | flag-structure; cell-has-placeholder |
| 12 | `round36-c1-battery` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 13 | `regex-log-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 14 | `git-webserver-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 15 | `round37-c1-mutants` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 16 | `round37-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 17 | `anchor-digest-check` | gate | red/r53-entry | yes | ARGV-DEFECT | ok | ok | flag-structure; cell-has-placeholder |
| 18 | `ledger-tip` | gate | green/r53-entry | yes | ARGV-DEFECT | ok | ok | flag-structure; cell-has-placeholder |
| 19 | `build-pmars-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 20 | `round38-c1-mutants` | gate | red/r53-entry | yes | equal | ok | ok |  |
| 21 | `round38-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 22 | `mutant-direction-check` | gate | red/r53-entry | yes | ARGV-DEFECT | ok | ok | flag-structure |
| 23 | `tip-receipts` | gate | green/r53-entry | yes | ARGV-DEFECT | ok | ok | flag-structure; cell-has-placeholder |
| 24 | `git-leak-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 25 | `round39-c1-mutants` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 26 | `round39-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 27 | `order-check` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 28 | `round39-c1-audit` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 29 | `round40-c1-mutants` | gate | red/r53-entry | yes | equal | ok | ok |  |
| 30 | `round40-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 31 | `db-wal-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 32 | `round41-c1-mutants` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 33 | `round41-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 34 | `constraints-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 35 | `round-close-check` | gate | green/r53-entry | yes | ARGV-DEFECT | ok | ok | flag-structure |
| 36 | `round42-c1-mutants` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 37 | `round42-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 38 | `fibsqrt-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 39 | `round43-c1-mutants` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 40 | `round43-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 41 | `feal-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 42 | `round44-c1-mutants` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 43 | `round44-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 44 | `feal-linear-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 45 | `scratch-root-guard` | gate | red/hand-contract | yes | ARGV-DEFECT | ok | ok | instantiation; cell-has-placeholder |
| 46 | `adoption-check` | gate | red/r53-entry | yes | ARGV-DEFECT | ok | ok | instantiation; cell-has-placeholder |
| 47 | `attrib-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 48 | `catalog-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 49 | `defect-ledger` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 50 | `gate-flip-check` | gate | red/r53-entry | yes | ARGV-DEFECT | ok | ok | instantiation; cell-has-placeholder |
| 51 | `extraction-policy-compare` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 52 | `password-recovery-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 53 | `polyglot-c-py-probe` | probe | green/r53-entry | yes | equal | ok | ok |  |
| 54 | `round28-census` | gate | red/r53-entry | yes | ARGV-DEFECT | ok | ok | instantiation; cell-has-placeholder |
| 55 | `round30-defects` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 56 | `round31-c1-literals` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 57 | `round31-defects` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 58 | `round33-c1-literals` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 59 | `round33-defects` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 60 | `round35-c1-coverage` | gate | red/r53-entry | yes | equal | ok | ok |  |
| 61 | `round35-hardening` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 62 | `round36-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 63 | `round45-c1` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 64 | `round45-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 65 | `round46-c1` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 66 | `round46-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 67 | `round46-c3` | gate | red/r53-entry | yes | equal | ok | ok |  |
| 68 | `round50-c1` | gate | green/r53-entry | yes | ARGV-DEFECT | ok | ok | flag-structure; cell-has-placeholder |
| 69 | `round50-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 70 | `round51-routing` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 71 | `round51-surfaces` | gate | red/r53-entry | yes | equal | ok | ok |  |
| 72 | `round52-c1` | gate | red/r53-entry | yes | equal | ok | ok |  |
| 73 | `round52-c2` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 74 | `routed-findings` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 75 | `tb2-grader-probe` | probe | green/r53-entry | yes | equal | WRAPPER-DEFECT | ok | reg:argv0=uv,led:argv0=uv |
| 76 | `round53-c1` | gate | green/r53-entry | yes | equal | ok | ok |  |
| 77 | `round53-c2` | gate | red/bare | yes | ARGV-DEFECT | ok | ok | flag-structure; cell-has-placeholder |
| 78 | `stage-scan` | gate | red/bare | yes | ARGV-DEFECT | ok | ok | flag-structure |

## 4. The rows a binding counter would flag TODAY (17 of 78)

| row | ledger state/chosen | registry cell tokens (shlex) | ledger `entry_argv` | L1 class |
|---|---|---|---|---|
| `adoption-check` | red/r53-entry | `python3` `plans/adoption_check.py` `--lane` `.` `--expect` `<expect.json>` `--census` | `python3` `plans/adoption_check.py` `--lane` `.` `--expect` `.ufo/waves/round-33/claims/adoption-expect.json` `--census` | ARGV-DEFECT |
| `anchor-digest-check` | red/r53-entry | `python3` `plans/anchor_digest_check.py` `--lane` `DIR` `[--evidence-ref` `head` `or` `index]` `[--verbose]` | `python3` `plans/anchor_digest_check.py` `--lane` `.` | ARGV-DEFECT |
| `coverage-census` | green/r53-entry | `python3` `corpus/evidence/round13-coverage/coverage_census.py` `[--revision` `REV]` | `python3` `corpus/evidence/round13-coverage/coverage_census.py` | ARGV-DEFECT |
| `gate-flip-check` | red/r53-entry | `python3` `plans/gate_flip_check.py` `--lesson` `<lesson.md>` | `python3` `plans/gate_flip_check.py` `--lesson` `corpus/lessons/round-52.md` | ARGV-DEFECT |
| `gate-timing` | green/r53-entry | `python3` `plans/gate_timing_check.py` `--lesson` `corpus/lessons/round-26.md` `--commit` `REV` | `python3` `plans/gate_timing_check.py` `--lesson` `corpus/lessons/round-26.md` `--commit` `536925b5320fa64298030b4ee76a58fc4b82723f` | ARGV-DEFECT |
| `ledger-tip` | green/r53-entry | `python3` `plans/ledger_tip.py` `--source` `<lane>` `--work` `<scratch>` | `python3` `plans/ledger_tip.py` `--lane` `.` | ARGV-DEFECT |
| `mutant-direction-check` | red/r53-entry | `python3` `plans/mutant_direction_check.py` `--lane` `.` `[--counter` `plans/round38_c1_verify.py]` `[--work` `DIR]` | `python3` `plans/mutant_direction_check.py` `--lane` `.` | ARGV-DEFECT |
| `package-gate` | green/r53-entry | `python3` `plans/pkg_gate.py` `package` `--root` `DIR` `--spec` `plans/pkg-spec-r35.json` `[--rerun]` `[--require-clean-tree]` | `python3` `plans/pkg_gate.py` `package` `--root` `.` `--spec` `plans/pkg-spec-r35.json` `--require-clean-tree` | ARGV-DEFECT |
| `round-close-check` | green/r53-entry | `python3` `plans/round_close.py` `--lane` `.` `--round` `N` `[--census` `PATH]` | `python3` `plans/round_close.py` `--lane` `.` `--round` `44` `--census` `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | ARGV-DEFECT |
| `round28-census` | red/r53-entry | `python3` `plans/round28_census.py` `--root` `.` `--revision` `REV` | `python3` `plans/round28_census.py` `--root` `.` `--revision` `536925b5320fa64298030b4ee76a58fc4b82723f` | ARGV-DEFECT |
| `round50-c1` | green/r53-entry | `python3` `plans/round50_c1_verify.py` `--lane` `.` `--work` `DIR` | `python3` `plans/round50_c1_verify.py` `--lane` `.` | ARGV-DEFECT |
| `round53-c2` | red/bare | `python3` `plans/round53_c2_tipstate.py` `--lane` `.` `--source` `<clean` `git` `clone` `of` `the` `landing` `tip>` `--work` `<scratch>` | `python3` `plans/round53_c2_tipstate.py` `--lane` `.` | ARGV-DEFECT |
| `scratch-root-guard` | red/hand-contract | `python3` `plans/scratch_guard.py` `check` `<root>` | `python3` `plans/scratch_guard.py` `check` `.` | ARGV-DEFECT |
| `sources-adopt` | red/bare | `python3` `plans/sources_adopt.py` | `python3` `plans/sources_adopt.py` `--lane` `.` | ARGV-DEFECT |
| `stage-scan` | red/bare | `python3` `plans/stage_scan.py` `PATH...` | `python3` `plans/stage_scan.py` `--lane` `.` | ARGV-DEFECT |
| `tb2-grader-probe` | green/r53-entry | `uv` `run` `--no-project` `--with` `biopython==1.85` `python3` `plans/tb2_grader_probe.py` `--lane` `.` | `uv` `run` `--no-project` `--with` `biopython==1.85` `python3` `plans/tb2_grader_probe.py` `--lane` `.` | WRAPPER-DEFECT |
| `tip-receipts` | green/r53-entry | `python3` `plans/tip_receipts.py` `--lane` `DIR` `[--work` `DIR]` `[--list]` `[--tamper` `REL]` `[--only` `SUBSTR]` | `python3` `plans/tip_receipts.py` `--lane` `.` | ARGV-DEFECT |

## 5. What the 16 L1 defects actually are

- **0** wrong-instrument defects: on all 78 rows the registry cell and the ledger argv name the
  same interpreter *and* the same script. Every L1 defect is an argument-shape defect.
- **5 instantiation-only** — the cell holds a metavariable, the ledger holds a
  concrete value: `adoption-check`, `gate-flip-check`, `gate-timing`, `round28-census`, `scratch-root-guard`.
- **11 flag-structure** — the cell declares optional/bracketed flags the ledger
  argv omits, or a different flag shape entirely: `anchor-digest-check`, `coverage-census`, `ledger-tip`, `mutant-direction-check`, `package-gate`, `round-close-check`, `round50-c1`, `round53-c2`, `sources-adopt`, `stage-scan`, `tip-receipts`.
- **Binding defects are orthogonal to the declared colour.** 7 of the
  16 defect rows are declared **green** (`coverage-census`, `gate-timing`, `ledger-tip`, `package-gate`, `round-close-check`, `round50-c1`, `tip-receipts`) —
  a green row can still carry an unbound cell — while 7 declared-red rows bind
  cleanly (`round35-c1-coverage`, `round38-c1-mutants`, `round40-c1-mutants`, `round46-c3`, `round51-surfaces`, `round52-c1`, `state-assertion-check`).
- **4 rows are deliberately not entry-mode** (`chosen`: `bare` ×3 — `sources-adopt`,
  `round53-c2`, `stage-scan`; `hand-contract` ×1 — `scratch-root-guard`): their ledger argv is a
  *failing exercise*, not the registry's declared entry. Under the frozen L1 wording
  ("`entry_argv` must token-equal the SKILL registry row's declared entry command") these are
  `ARGV-DEFECT`s **by construction**; the correction is data, not a rule change — either the
  cell declares the exercising invocation, or the ledger row keeps the registry entry and the
  exercise moves into the row's `reason`/`evidence` fields.

## 6. The two r54 laundering routes against today's real data

- **uv-wrapper route — PRESENT in the lane's own data.** `tb2-grader-probe`: registry cell
  `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .`, and
  the ledger `entry_argv` is that same uv command (`argv[0]=uv`, ledger `chosen: r53-entry`,
  `entry_state: green`). L2 fires on **both** sides. This is a live row, not a fixture.
- **argparse-prefix-abbreviation route — ABSENT from the lane's own data.** L3 yields **0**
  candidates: no flag in any registry cell or ledger argv is a prefix of a longer flag in its
  script. The route exists only in the frozen fixture
  `plans/round55_c2_controls.py` case `abbreviated-selftest`
  (`python3 plans/fixture_gate.py --selft`, controls line 58). So L3 is defense in depth with
  zero live hits — a counter run over the real lane data would flag no abbreviation today.
- **Side finding for R55-C1 (registry closure).** Exactly one registry row's entry cell does
  **not** match the r52 counter's frozen `CMD` shape: `coverage-census`
  (`corpus/evidence/round13-coverage/coverage_census.py` — the hyphen in `round13-coverage` is
  outside that shape's `[A-Za-z0-9_]+`). 78 − 1 = 77 equals the `REGISTERED total=77` the r52
  counter prints at this tip, so the r52 registry closure cannot see that row's script at all.

## 7. Discrepancies vs `E13BindingScan`

E13's table existed when this scan finished:
`.ufo/waves/round-55/w1/E13BindingScan/binding-scan.tsv` (4038 bytes, written 12:40).

- **Row set**: 78 rows in both; identical names, no missing/extra row.
- **Verdict classes agree on 77 of 78 rows.**
  - **L1**: E13's `DIFF` set is exactly my `ARGV-DEFECT` set — the same 16 names, no more, no
    fewer.
  - **L2**: E13 flags exactly one row, `tb2-grader-probe` — the same row I flag.
  - **L3**: neither scan flags any row (0 candidates on both sides).
- **One disagreement — `tb2-grader-probe` (L1 label only).** E13 records `l1=NO-PY3-SPAN`
  ("registry entry cell has no backtick python3 span") plus `l2=L2`; I record `l1=equal` plus
  `l2=WRAPPER-DEFECT`. Cause: the span-acceptance rule. E13 requires the first backtick span
  to *start with* `python3`; this cell's only command span starts with `uv run …`, so E13 reads
  the cell as having no python3 span. I accept the first span that *contains* a `python3`
  command, so I tokenise the whole `uv run …` span and compare it with the ledger argv — which
  are identical — making L1 equal and pushing the defect into L2, which is where the frozen
  claim puts it ("`uv`/`pipx`/`poetry`-style wrappers as `argv[0]` … are `WRAPPER-DEFECT`s").
  **Both scans flag the row, and the flagged-row set is identical**; only the L1 label differs.
  A counter that stopped at E13's `NO-PY3-SPAN` would report an L1 defect and could stop there;
  under the frozen claim the attributable defect for this row is `WRAPPER-DEFECT`.
- **Coverage gain on my side (not a conflict):** the `strict-r52-cmd` column (section 3) has no
  counterpart in E13's table; it is what surfaces the `coverage-census` row that the r52
  registry-closure counter cannot resolve (section 6).
- **Vocabulary**: I use the frozen claim's names (`ARGV-DEFECT` / `WRAPPER-DEFECT` /
  `ABBREV-DEFECT`); E13 uses `DIFF` / `L2` / `OK` / `NO-PY3-SPAN`. E13's note categories
  (`placeholder-instantiated`, `optional-brackets-omitted`, `control-mode-instead-of-primary-entry`,
  `declared-red-unaccepted-flag`, `declared-red-rejected-flag`, `placeholder-plus-fleet-root-path`,
  `wrapper-cell-sanctioned-uv`) are finer than my two-way `why` (`instantiation` /
  `flag-structure`); the two agree row-for-row on *which* rows differ, and E13's categories are
  the more actionable form for the data corrections E4/L1 must make.

## 8. Bounds, dead ends, and what I did not do

- **No lane writes** beyond my three named outputs; no git/jj mutation of any kind (read-only
  `git rev-parse` / `git status` only); no clone was needed (the scan is static over the lane's
  committed files, pinned by the digests above).
- **I did not execute any entry argv** — that is the claim's L4 leg and belongs to the new
  counter; this seat is the static binding scan. No L4 claim is made or implied here.
- **Dead ends hit and fixed while building the scan** (each one changed a result, so they are
  recorded rather than hidden):
  1. *Substring test for "flag verbatim in the body" is wrong* — `--selft` is a substring of
     `--selftest`, so the substring test would never flag an abbreviation. Fixed to membership
     in the set of **complete** flag literals; the `--selft` control now fires.
  2. *The r52 `CMD` shape rejects the hyphenated `corpus/evidence/round13-coverage/` directory*,
     which initially made `coverage-census` look `UNPARSED` (0 command span). Fixed by
     broadening the span matcher to any `python3 <path>.py` (or `python3 -c`) and reporting the
     strict r52 shape in its own column instead of letting it hide the row.
  3. *An inline `-c` span carries no `.py` path*, so my first span matcher skipped it and the
     wrapper leg could not fire on it. Fixed by accepting `python3 -c` spans.
- **Not found / unknown:** whether the L1 integrator intends the strict full-span token equality
  or a contract-aware comparison is not settled in the frozen claim text; the counts above use
  the strict reading (which is what the claim's wording says) and the per-class breakdown in
  section 5 gives the softer reading's inputs, so both readings are derivable from this table.

## 9. Reproduce

```
python3 /fast/scratch/hyaku/kengaku-r55/SC3ArgvUniverse/universe_scan.py --selftest   # exit 0
python3 /fast/scratch/hyaku/kengaku-r55/SC3ArgvUniverse/universe_scan.py             # exit 0
python3 plans/round52_c2_registry.py --lane .                                        # exit 1 (frozen R55-C1 before-state)
```

The scanner is seat-local scratch (deleted on yield); its logic is fully described in section 1
and re-derivable from the two pinned inputs.
