# R43R42Defects — appended corrections for the round-42 wave-2 document defects (kengaku round 43, wave 1)

Seat: scribe (leaf), lane `kengaku-shokunin`, no subagents. Re-check tip `d33350f` (wave-2 reports and the SCORECARD
wave-2 outcome landed at `f9bbee6`; the m_flash lesson row landed at `3e8a2e5`). Basis read in full:
`.ufo/waves/round-42/falsify/F42RevLesson.md` (8 defects), `F42RevQuality.md` (6), `F42CritScorecard.md` (1 mismatch),
`F42CritAdv.md` (2 adv errata), `F42RevRiders.md` (5). Nothing in the lane was edited; no frozen file touched; every
number below is a command I ran at `d33350f` or is marked `[REPORTED]` with the report that measured it. Receipts and a
paste-ready JSONL fragment are in `.ufo/waves/round-43/build/R43R42Defects/`.

## 1. Disposition of the 22 defects at `d33350f`

| report | id | target doc | status now | correction |
|---|---|---|---|---|
| F42RevLesson | D1 | `corpus/lessons/round-42.md:98` | **stands** | A-E1 |
| F42RevLesson | D2 | `…:106-108` | **stands** | A-E2 |
| F42RevLesson | D3 | `…:151` | **stands**, and now worse: the L1 committed the same unpersisted ratios at `3e8a2e5` | A-E3 |
| F42RevLesson | D4 | `…:57` | **stands** | A-E4 |
| F42RevLesson | D5 | `…:96` | **REFUTED** — `plans/round42_c2_verify.py:327` *is* the `V9` tuple; `:328` is `defects = 0` | none (recorded in A) |
| F42RevLesson | D6 | `…:122` | **stands** | A-E5 |
| F42RevLesson | D7 | `…:43` | **REFUTED** — the capture's two `COPY` lines are `:9` and `:10`; the lesson's `Dockerfile:9-10` is exact | none (recorded in A) |
| F42RevLesson | D8 | `…:150` | **stands** | A-E6 |
| F42CritAdv | X3, X7 | frozen counter rows (display-only) | **stands** ×2 | A-E7 + C-S2 |
| F42RevQuality | D1 | `corpus/QUALITY.md:718-719,800-801` | **stands** — neither tool exists at `d33350f` or in any commit | B-C1 |
| F42RevQuality | D2 | `QUALITY.md:713,791` | **stands**, measured by me | B-C2 |
| F42RevQuality | D3 | `QUALITY.md:721-725` | **stands** | B-C3 |
| F42RevQuality | D4 | `QUALITY.md:809-811` | **stands**; conclusion true, cited evidence invalid | B-C4 |
| F42RevQuality | D5 | `QUALITY.md:767` | **stands** | B-C5 |
| F42RevQuality | D6 | `QUALITY.md:767` | **stands** | B-C6 |
| F42CritScorecard | M1 | `SCORECARD.md:1760` | **stands** (round 36 passed under v1) | C-S1 |
| F42RevRiders | D1 | `corpus/routed-findings.jsonl` R42-R4 | **stands**, live: `OBSERVE … mismatched=1` | D-1 |
| F42RevRiders | D2 | R42-R2 check | **PARTLY REFUTED** — the build copy is committed at `f9bbee6` and byte-identical to the landed tool (both `f0360e30…`), so "unpassable in a clean clone" and the "second mismatch" no longer hold; the surviving half (the check pins the build copy, never `plans/scratch_guard.py`, and its clause 1 pins a deleted scratch root) stands | D-2 |
| F42RevRiders | D3 | `plans/scratch_guard.py` docstring vs code | **stands**, re-measured | D-3 |
| F42RevRiders | D4 | the guard's 36-case selftest | **stands**, re-measured | D-3 (same row) |
| F42RevRiders | D5 | `SKILL.md` | **stands** — `grep -c 'scratch_guard\|scratch-root-guard' SKILL.md` → `0` | E-K1 |

Totals: 22 defects, 20 corrections drafted, 3 refuted-or-partly (2 outright: lesson D5, lesson D7 — plus riders D2's
two dead assertions).

One correction to a reviewer's own fix suggestion: **appending a closed `R42-R4.1` row does not clear the mismatch.**
`observe()` (`plans/routed_open.py:139-160`) compares each row's own status with its own check, so R42-R4 stays
`open` + `rc=0` however many rows are appended. Measured: original ledger + my three appended rows only →
`OBSERVE R42-R4 rc=0 observed=pass self=open MISMATCH`, `OBSERVE rows=19 mismatched=1`, exit 1. The leg that clears it
is the row's own `status: closed` (D-1). Candidate ledger with the flip plus the three appends →
`OBSERVE rows=19 mismatched=0`, exit 0.

## 2. Paste blocks (append only; nothing above any block is edited)

### A. `corpus/lessons/round-42.md` — append after the last line (`:151`)

````markdown
## Errata (appended in round 43 from the wave-2 review; nothing above is edited)

`F42RevLesson` (`.ufo/waves/round-42/falsify/F42RevLesson.md`) routed eight defects; six are corrected here, two were
re-checked against this file at `d33350f` and are not defects (last paragraph). Line numbers are this file's.

- **E1 — R4's measurement (`:98`).** `git diff bc856d8..HEAD -- corpus/SOURCES.md` is not empty:
  `git diff --numstat bc856d8..HEAD -- corpus/SOURCES.md` → `4	0	corpus/SOURCES.md` — the four added rows `S125`–`S128`,
  zero removals. The substance holds (no in-place edit), but the honest wording is "the diff shows only additions, no
  in-place edits"; as written the sentence is true only against the freeze commit itself (`bc856d8..bc856d8`).
- **E2 — R5's freeze pointer (`:106-108`).** The 14 `round_close.py`/`tip_receipts.py` residual mutants and
  `F39LedgerTip` D1 / `F39MutDirection` / `F39OrderGateMut` fail-open are **not** "named carried again in the freeze":
  `plans/round-42-claims.md` has no `§Limits` section (headers at `:1,23,65,96,102`) and
  `grep -nE 'LedgerTip|MutDirection|OrderGateMut|fail-open|s_usage' plans/round-42-claims.md` → no output (rc=1). The
  freeze's "Limits named now" bullet (`:60-63`) names XL1–XL6, `state_check.py`/`round_close.py` survivors and the 34
  unpriced advertised rows — so `:111` is right and `:106-108` is not: the F39 trio and the residual mutants were
  carried by this lesson alone.
- **E3 — the route-mix ratios are quoted stdout, not persisted data (`:151`).** `flash=14/33` and `attack=22/33` appear
  nowhere under `.ufo/waves/round-42/` except the review that quotes them; `falsify-spec.json`'s 33 items carry only
  `axes, milestone, name, prompt, role` (reviewer 10, critic 9, executor 5, mutation-tester 3, scout 3, connector 3), and
  `falsify-dispatch.json` carries `counts {spawn 33, resume 0, total 33}` with no model or route field. The row's role
  list "(executor/scribe/critic/sentinel)" also names two roles wave 2 did not have. The class and the fix stand; the two
  ratios are one generator run's stdout, and the persisted facts are the role mix above and `counts.spawn=33`.
- **E4 — receipt pointer (`:57`).** `grep -n 'fibsqrt-probe.txt:6'` finds one citation, not the review's two. `:6` is
  the `# capture test_outputs.py sha256=` header. The summary
  is `:23` (`regrade cases=16 differ=0`) and `:24` (`cases=16 observed_pass=7 observed_fail=9 mismatches=0`); the
  `lookup-28` case is `:11`.
- **E5 — the census command (`:122`).** Run as printed (BRE) the `\|` is alternation and the `^ {0,3}` branch matches
  every line, so it yields 171/175 — `wc -l` at `bc856d8`/`508434a` — not 117/121. The quoted numbers come from the `-E`
  form: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`.
- **E6 — row 3's fix has no failing receipt (`:150`).** The syntax warning was ephemeral and nothing under
  `.ufo/waves/round-42/` stores it; `frozen-digests.txt:4` (`fc58bf3f…`) only proves the frozen probe is the corrected
  file (`sha256sum plans/fibsqrt_probe.py` matches). Every other Mistakes row names a persisted failing receipt; this
  one's falsifier exists only in its own sentence.
- **E7 — two C1 `adv` cites (from `F42CritAdv`).** The frozen `MUTANTS` rows X3 and X7 quote `plans/anchor_digest_check.py`
  verbatim but cite the wrong lines: X3 `:57-58` for a sentence at `:59-61`, X7 `:92-93` for a sentence at `:91-92`; both
  carried from `F40XMutAnchor.md` §5. Display-only — the counter echoes `label[:90]` and never parses it — so no
  admission claim moves; correct the cites when the counter is next editable.

Re-checked and **not** defects (at `d33350f`): `plans/round42_c2_verify.py:327` is the `("V7" …), ("V8" …), ("V9",
lambda: v9(lane))]` line and `:328` is `defects = 0`, so the R3 citation `:327` is exact (the review's D5 moved it one
line early); and `corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile` carries `COPY tests/sim.c /app` at `:9` and
`COPY gates.txt /app` at `:10` with the comment at `:8`, so `Dockerfile:9-10` is right (the review's D7 moved both pins
one line late).
````

### B. `corpus/QUALITY.md` — append at end of file (after `:822`)

````markdown
## Round42 criteria — corrections appended in round 43 (Q33, Q34)

`F42RevQuality` (`.ufo/waves/round-42/falsify/F42RevQuality.md`) routed six defects; all six re-held at `d33350f` and
all six are recorded here. The criteria stay as written; these are the corrections a reader needs and the fixes owed.
Line numbers are this file's.

- **C1 (D1) — the tools the Check lines name exist in no commit.** Q33 (`:718-719`) and Q34 (`:800-801`) say the drafts
  "to land as" `plans/carried_direction_diff.py` and "must land as" `plans/sources_appendonly.py`. Neither exists at
  `d33350f` and neither appears in any commit (`git log --oneline --all -- plans/carried_direction_diff.py
  plans/sources_appendonly.py` → empty). Both Check lines were dead text as landed. Owed: land the two drafts from
  `.ufo/waves/round-42/build/R42QualityDraft/` (`carried_vs_rederived.py` `47151f23…`, `sources_appendonly.py`
  `f1b84d8a…`) under those names, or rewrite each Check line to name the draft path — the fallback now resolves,
  because the draft directory is committed since `f9bbee6`.
- **C2 (D2) — the Check lines do not match the drafts' CLI.** Both drafts take the lane positionally
  (`build/R42QualityDraft/carried_vs_rederived.py:5` `LANE = sys.argv[1]`; `sources_appendonly.py:13` `LANE = sys.argv[1]
  if len(sys.argv) > 1 else "."` — the review said `:14`, one line late), so `--lane .` is consumed as the path `--lane`.
  Measured 2026-10-26 at `d33350f`:
  `carried_vs_rederived.py --lane .` → `FileNotFoundError: … '--lane/.ufo/waves/round-40/falsify/F40XMutAnchor.md'`,
  exit 1; `sources_appendonly.py --lane .` → `SETUP git log failed: fatal: cannot change to '--lane': No such file or
  directory`, exit 2. The form that runs is `python3 <tool> <lane>` (positional run: `CARRIED-DIRECTIONS total=14
  differ=2 ids=XO5,XO6`; `SOURCES-COMMITS scanned=37 rows_at_tip=121`, `SOURCES-APPENDONLY violations=15 arity=0`,
  exit 1). A byte-identical landing alone would not make either Check runnable.
- **C3 (D3) — Q33 (b) cites a predicate line its own instruction cannot print.** Development mode
  (`plans/round42_c1_verify.py:525` `dev = a.battery_dir is not None or a.only is not None`) prints `PREDICATE C1 n/a
  (non-default battery or mutant subset)` (`:657`), so the `PREDICATE C1 fail` at
  `claims/control-c1-direction-mislabel.txt:37` belongs to the default battery run (29 fixtures), not to (b)'s
  "development mode with the witness fixtures". Correction: (b) keeps its discriminating lines — XO5/XO6 `rc-silence
  `SURVIVED exhibits=0>1,rc-mirror`, `MUTANTS total=14 killed=12 survived=2 …`, `MUTANTS-BY-TOOL order=3/5`, `exit=1`
  (`:38`) — and names the default battery as the mode that additionally prints the predicate, or drops the `:37`
  citation.
- **C4 (D4) — Q34's pipe sentence is false where it matters, and its inference is invalid.** `:809-811` says a cell
  carrying a literal `|` "would parse as an arity mismatch and is reported … rather than silently misread — `arity=0`
  over 117 rows × 36 commits says no such row exists today". The tool skips every row it has not seen before
  (`build/R42QualityDraft/sources_appendonly.py:58-60` `if rid not in prev: continue`), so a row *born* with a pipe can
  never produce an `ARITY` line, and its later in-place edits are attributed to the cell the pipe shifted into —
  `F42RevQuality`'s `fx-pipe3` fixture reported `violations=0 arity=0`, exit 0. `arity=0` therefore cannot establish the
  conclusion. The conclusion is nevertheless true: `awk -F'|' '/^\| S[0-9]+/ && NF!=13' corpus/SOURCES.md | wc -l` → `0`
  over 121 rows at `d33350f`. Correction: keep the conclusion, cite that scan, and state the limit — arity is a length
  guard for ids already present, nothing else.
- **C5 (D5) — wrong pin.** `:767` cites `parse_registry(text, …)` at `plans/registry_check.py:20`; `:20` is
  `def safe_path(value):`, `parse_registry` is defined at `:25`, and the working-tree call is `:55`.
- **C6 (D6) — the last sentence of `:767` needs the creation-time scope.** "No lane tool reads it from committed history"
  is true at `d33350f` only because C1 left the instrument unlanded; landing `sources_appendonly.py` — C1's own fix —
  would falsify it with the criterion's instrument. Correction: "no lane tool read it from committed history at this
  criterion's creation", the scope the neighbouring measured sentences already carry.
````

### C. `SCORECARD.md` — append after the last line (`:1825`, end of the round-42 wave-2 outcome)

````markdown
### Round-42 corrections appended in round 43

- **S1 — the envelope note is one counter too wide (`:1760`, from `F42CritScorecard` M1).** "under the v1 envelope
  (home read-only) every C2-class counter went red on `uv`'s cache lock" — `integrate/measure-baseline-v1.txt` shows
  `PREDICATE C2 fail` six times (`:51,161,239,386,522,669`) and `PREDICATE C2 pass` once (`:679`), for round 36.
  Corrected: every C2-class counter that drives the gate's `uv` leg (`plans/pkg_gate.py:276` `["uv", "run",
  "--no-project", "--with", "biopython==1.85", "python3"]`, which is the `P10` line those six report as DEFECT) went
  red; `plans/round36_c2_verify.py`'s six checks (`W1`–`W6`, `:215-216`) drive no `uv`-backed tool and stayed green.
- **S2 — two frozen C1 `adv` cells carry wrong line pins (`F42CritAdv`).** X3 cites
  `plans/anchor_digest_check.py:57-58` for a sentence that sits at `:59-61`; X7 cites `:92-93` for one at `:91-92`; both
  are carried from `F40XMutAnchor.md` §5. Display-only (`label[:90]` is echoed and never parsed, so no admission claim
  moves); the erratum is `corpus/lessons/round-42.md` E7 and the cites are to be corrected when
  `plans/round42_c1_verify.py` is next editable.
- **S3 — where the wave-2 routed defects are carried.** The lesson, QUALITY and SCORECARD corrections above live in the
  documents themselves; the ledger/rider defects live in `corpus/routed-findings.jsonl` as `R42-R2.1`, `R42-R2.2` and
  `R42-R6`, with `R42-R4` closed and `R42-R2`'s stale check cleared (drafts:
  `.ufo/waves/round-43/build/R43R42Defects.md` §2 D–E).
````

### D. `corpus/routed-findings.jsonl` — three appended rows, plus two field changes the observe leg requires

Append these three lines (byte-exact, one JSON object per line) after `R40-R1.1`; they validate
(`routed_open.py --lane . --file <candidate> --list` → no `DEFECT line=`):

```
{"id": "R42-R2.1", "class": "scratch-root-guard", "source": "corpus/lessons/round-41-verifier-spotcheck.md:110", "opened_round": 42, "status": "closed", "close": "plans/scratch_guard.py (sha256 f0360e30…, `--selftest` ok=36/36 exit 0, `check /fast/scratch/hyaku/kengaku-r43` rc=0); LOG.md:1299 records the landing", "blocker": null, "check": "test -f plans/scratch_guard.py && grep -qs 'safe-rm' plans/scratch_guard.py && python3 plans/scratch_guard.py --selftest >/dev/null 2>&1", "note": "Closes R42-R2's substantive half (the guard landed). The check pins the landed tool, not the wave-1 build copy: deleting plans/scratch_guard.py flips it red. Registry visibility is carried by R42-R2.2."}
{"id": "R42-R2.2", "class": "scratch-root-guard-registry", "source": "SKILL.md:562", "opened_round": 42, "status": "open", "close": null, "blocker": null, "check": "grep -qs 'scratch-root-guard' SKILL.md", "note": "The landed guard has no SKILL.md registry row (grep -c 'scratch_guard|scratch-root-guard' SKILL.md -> 0 at d33350f; LOG.md:1299 mentions the landing once). The row is drafted at .ufo/waves/round-43/build/R43R42Defects.md §2 E."}
{"id": "R42-R6", "class": "scratch-guard-exit-contract", "source": "plans/scratch_guard.py:17", "opened_round": 42, "status": "open", "close": null, "blocker": null, "check": "o=$(python3 plans/scratch_guard.py --selftest 2>&1) && printf '%s\\n' \"$o\" | grep -qE '^case +check-sentinel-unreadable +PASS exit=2'", "note": "`check` on a root whose sentinel is unreadable prints CHECK red reason=sentinel-unreadable:Permission denied and exits 1, while the docstring (plans/scratch_guard.py:17-18) promises exit 2; the 36-case selftest has no such case (measured 2026-10-26 19:12, exit=1). One case expecting exit 2 closes both."}
```

Two existing lines change, and only these fields (the rest of each line stays byte-identical):

1. **`R42-R4`** — `"status": "open"` → `"status": "closed"`, `"close": null` → `"close": "corpus/QUALITY.md:759 (Q34
   states rule 2 in-lane) + 0 removed lines in `git diff d69452cf..HEAD -- corpus/SOURCES.md`; `routed_open.py
   --observe` rc=0"`, and append to the end of `note`: `" Closed 2026-10-26 (round 43, R43R42Defects): the rule landed
   as Q34 (corpus/QUALITY.md:759) and the invariant still holds (removed_lines=0, 121 rows)."` This is the leg that
   clears `mismatched=1`; appending a new row cannot (see §1).
2. **`R42-R2`** — `"check"` (the five-clause string) → `null`, and append to the end of `note`: `" Stale-check
   correction 2026-10-26 (round 43, R43R42Defects): clause 1 pins
   /fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL, deleted with the round-42 scratch root; clause 3 now resolves
   (the build copy is committed at f9bbee6, byte-identical to the landed tool, sha256 f0360e30). The landed work is
   closed in R42-R2.1."` With the check cleared the row reports `observed=n/a` while open — the shape `R40-R1` already
   uses.

Measured effect of D in full: `OBSERVE rows=19 mismatched=0`, `ROWS total=19 open=10 blocked=1 closed=8 refused=0`,
`routed_open=11 oldest_round=39`, exit 0.

### E. `SKILL.md` — one registry row, appended as the last row of the table (after `fibsqrt-probe`, `:601`)

Column order is the table's (`:562`): name | kind | entry | verdict map | self-test | pinned values | write scope |
owner.

```
| `scratch-root-guard` | gate | `python3 plans/scratch_guard.py check <root>` and `python3 plans/scratch_guard.py safe-rm <root> <seat> <path>` (`--dry-run` prints `WOULD-DELETE`; `--json`; `--selftest` runs the temp-root cases) | `0` check green, or the delete performed · `1` check red (sentinel missing / unparseable / another round, or a failing selftest case) — and **`check` on an unreadable sentinel exits 1 today although `plans/scratch_guard.py:17-18` promises 2** (measured 2026-10-26, routed `R42-R6`) · `2` usage, an untrusted root, or a refused delete (`root-untrusted`, `target-outside-seat`, …) | `python3 plans/scratch_guard.py --selftest` (`SELFTEST ok=36/36`, measured; no unreadable-sentinel `check` case yet) | round-42 sentinel `/fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL` (present when the criterion was written, since deleted with that scratch root) | writes and deletes only inside `<root>/<seat>`; the root's sentinel is read, never written | kengaku |
```

## 3. Evidence runs (commands, output, ENVELOPE lines)

All counter/tool/fixture runs below went through
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims/envelope.sh /fast/scratch/hyaku/kengaku-r43/R43R42Defects/env …`;
the lane clone is `/fast/scratch/hyaku/kengaku-r43/R43R42Defects/lane` (`git rev-parse --show-toplevel` = that path).
Read-only greps and `git diff`/`awk` runs against the lane were not enveloped (they write nothing).

1. **R42-R4 / R42-R2 live** — `cd <clone> && python3 plans/routed_open.py --observe`:
   `OBSERVE R42-R2 rc=1 observed=fail self=open` · `OBSERVE R42-R4 rc=0 observed=pass self=open MISMATCH` ·
   `OBSERVE rows=16 mismatched=1` · `ROWS total=16 open=9 blocked=1 closed=6 refused=0` · `routed_open=10 oldest_round=39`,
   exit 1.
   `ENVELOPE start 19:12:01 cwd=/home/vgpnk/Projects/shokunin/kengaku-shokunin`
   `ENVELOPE end 19:12:03 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`
2. **Candidate ledger (D applied)** — `python3 plans/routed_open.py --lane . --file …/candidate-routed.jsonl --observe`:
   `OBSERVE R42-R4 rc=0 observed=pass self=closed` · `OBSERVE R42-R2 self=open observed=n/a` ·
   `OBSERVE R42-R2.1 rc=0 observed=pass self=closed` · `OBSERVE R42-R2.2 rc=1 observed=fail self=open` ·
   `OBSERVE R42-R6 rc=1 observed=fail self=open` · `OBSERVE rows=19 mismatched=0`, exit 0.
   `ENVELOPE start 19:14:05 … / ENVELOPE end 19:14:07 exit=0 … unchanged`
3. **Append-only control** — original ledger + the three rows, no field changes:
   `OBSERVE R42-R4 rc=0 observed=pass self=open MISMATCH`, `OBSERVE rows=19 mismatched=1`, exit 1.
   `ENVELOPE start 19:15:22 … / ENVELOPE end 19:15:24 exit=1 … unchanged`
4. **Q33/Q34 drafts' CLI (B-C2)** — in the clone, each with its own rc:
   `carried_vs_rederived.py --lane .` → `FileNotFoundError: … '--lane/.ufo/waves/round-40/falsify/F40XMutAnchor.md'`, rc=1;
   `sources_appendonly.py --lane .` → `SETUP git log failed: fatal: cannot change to '--lane': No such file or
   directory`, rc=2; positional: `SOURCES-COMMITS scanned=37 rows_at_tip=121`, `SOURCES-APPENDONLY violations=15
   arity=0`, rc=1; `carried_vs_rederived.py .` → `CARRIED-DIRECTIONS total=14 differ=2 ids=XO5,XO6`.
   `ENVELOPE start 19:14:54 … / ENVELOPE end 19:14:56 exit=0 … unchanged`
5. **Guard exit contract (riders D3/D4)** — `plans/scratch_guard.py check` on a root whose sentinel is `chmod 000`:
   `SENTINEL .ROUND-ROOT-SENTINEL present=no reason=sentinel-unreadable:Permission denied` … `CHECK red
   reason=sentinel-unreadable:Permission denied round=None want=* seats=0`, exit **1**, while the docstring at `:17-18`
   says exit 2. Plus `--selftest` → `SELFTEST ok=36/36`, exit 0, and `grep -c 'check-sentinel-unreadable'` over its
   output → `0`.
   `ENVELOPE start 19:12:10 … / ENVELOPE end 19:12:12 exit=1 … unchanged` (check)
   `ENVELOPE end 19:12:22 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` (selftest;
   its start line was cut by `tail -4`, so only the end time is recorded)
6. **Read-only verifications at `d33350f`** (no envelope, no writes): the lesson's R4 diff (`4 0`), the freeze's five
   headers and the F39 grep (rc=1), the `flash=14/33` grep (only the two review echoes), the receipt lines `:6/:11/:23/:24`,
   the V9 tuple at `:327`, the census grep (171/175 vs `-E` 117/121), the Dockerfile lines `:8-10` with `sha256sum` =
   `780c2398…d3d4` = the capture `SHA256SUMS` row, `plans/registry_check.py:20/25/55`, the F42RevQuality/Q33 text,
   `base-v1` `PREDICATE C2` lines, the pipe scan (`0` over 121 rows), the appendonly skip at `:58-60`, the SKILL.md
   registry header (`:562`) and its zero guard mentions, and `sha256sum plans/scratch_guard.py` =
   `.ufo/waves/round-42/build/R42ScratchGuard/scratch_guard.py` = `f0360e30…`.

## 4. Limits and what I did not do

- I did not re-run the C1/C2 counters, the fibsqrt probe, or the pipe fixtures: their numbers are `[REPORTED]` from
  `F42RevQuality` and `F42CritScorecard`, and re-running would decorate, not test. The one thing I re-derived from code
  is the crux of each defect (dev-mode `n/a` at `:657`/`:525`; the first-appearance skip at `:58-60`; the V9 tuple line;
  the Dockerfile pins; the CLI form, which I did run).
- `R42-R6`'s green state is unverified: no tool yet prints `check-sentinel-unreadable … PASS exit=2`, so the check's only
  measured state is red (`rc=1`, 19:14:05 run). Its non-vacuity is by construction (suite green **and** the named case
  present), not by a passing run.
- `R42-R2.1`'s check passes today because `plans/scratch_guard.py` exists and its selftest is green; I did not mutate a
  clone to show it flipping red (that would require deleting a committed tool in a clone — cheap but out of scope here).
- The lesson's and QUALITY's erratum counts are as of `d33350f`; the round-43 landing will move registry rows (121 →
  more) and any figure the blocks quote would need the same treatment then.
- **Concurrent change, not mine:** at 19:17:03 (after my measurements, while this report was being written) the lane
  working tree gained 7 lines in `corpus/SOURCES.md` and a new `corpus/knowledge/tb2-circuit-fibsqrt-grader.md`
  (88 insertions, 0 deletions) — another seat's round-43 C2 landing, so `HEAD` is still `d33350f` and every figure here
  is a `d33350f` figure. Re-measured afterwards: `awk -F'|' '/^\| S[0-9]+/' corpus/SOURCES.md | wc -l` → 128 rows and the
  C4 pipe scan → `0`, so the effect of the new rows is none; but a paste block that quotes "121 rows" will need
  re-reading once the round lands.
- Out of scope by assignment: the other wave-2 routed reports (entry quotes, C2 package, cross-doc drift, plan-43,
  overclaim) and the round-42 wave-1 defects. No frozen file, counter, battery, probe, spec, gate or capture was read as
  writable; nothing was committed or pushed.

## 5. Findings worth the L1's attention

1. **Two of the eight lesson defects are the reviewer's own off-by-ones** (D5, D7). Both were asserted against the
   frozen counter and against a committed capture whose digest I re-computed; the lesson's cites are right. Expect this
   class elsewhere: a reviewer's `:N`/`:N+1` can be wrong in the same way it accuses the target of being.
2. **The reviewer's R42-R4 fix does not work as proposed** (§1, §3 run 3). This is the one place where a correction
   improves on the routed recommendation rather than restating it.
3. **The `m_flash` ratio is now load-bearing in a committed table row** (`corpus/lessons/round-42.md:151`, added at
   `3e8a2e5`) while remaining unpersisted. Either persist the generator's output next round or state the ratios as
   "printed at dispatch, not stored".
4. **`F42RevRiders`' Q32 digest recommendation is already superseded**: round-43's `envelope.sh` hashes names, types,
   targets and content bytes (`bindigest()`), which is why every run above reports a stable 16-hex digest; the plain
   `ls -A | sha256sum` volatility it warned about no longer applies to this round's receipts.
5. **Q34's `arity=0` stays a tempting false comfort** even after B-C4: the replacement scan (`awk … NF!=13`) is the
   evidence that cannot be fooled by a row born with a pipe, and it is one line a future criterion can reuse.

VERDICT: r42-defects-corrections-20-of-22-refuted-3
