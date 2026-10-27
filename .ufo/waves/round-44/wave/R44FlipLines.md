# R44FlipLines — closure R1 drafts: corrected flip verdicts, and the differential entry re-sourced (append-only)

Seat `R44FlipLines`, kengaku round 44 (hyaku run 9, 2026-10-26), wave item = round-43 closure **R1**
(`corpus/lessons/round-43-verifier-spotcheck.md` §5 R1). Leaf seat: no subagents, no background jobs spawned by me, no
lane edit, no commit, no push. Nothing was written outside
`.ufo/waves/round-44/wave/R44FlipLines/` and `/fast/scratch/hyaku/kengaku-r44/R44FlipLines`. No tool was installed.

Deliverables are **drafts for the L1**: three files in `.ufo/waves/round-44/wave/R44FlipLines/` (two `Flip check (round
44)` lines for `corpus/lessons/round-43.md`; one `## Errata (round 44 …)` section for
`corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md`; two `corpus/SOURCES.md` rows). Nothing above either
append point was edited, and no frozen surface was touched.

## 0. The assignment, restated as the two things R1 asks

1. **A false `not fired` flip verdict.** The round-43 Gate refused `task.toml`, `setup.py`, `solve.sh`, `feal.h` and
   `SHA256SUMS` as one set with the flip "an entry sentence that rests on one of them alone"
   (`corpus/lessons/round-43.md:41`), then recorded `Flip check (round 43): task.toml — not fired — no entry sentence
   rests on task.toml, setup.py, solve.sh, feal.h or SHA256SUMS alone` (`:46`). The round-43 non-author spot-check
   disagreed on that verdict (`…spotcheck.md` §3, last-but-one row).
2. **The entry sentences that make the verdict false.** Finding 11's "only time bound" sentence and `:122` rest on
   `task.toml:22` alone; finding 2, finding 12 and the `oracle-solve-sh` Mechanism row rest on `solve.sh:90` alone; and
   the entry's own provenance paragraph (`:72-74`) says the opposite about `solve.sh` ("own reading, tier C — not a
   registry row … no finding rests on its internal logic"). R1 offers two routes: admit the two files as rows (with Gate
   quotes) or withdraw the claims. This seat chose **admit both**, per file, with the tier argued rather than assumed —
   §2 below is that argument.

## 1. Evidence base (read before drafting)

| object | what I read it for | observed |
|---|---|---|
| `plans/round-44-claims.md` | round-44 frozen claims; confirms R1 is routed work, not a claim | read in full. R1 is listed under "Closure R1…", not under C1/C2 |
| `corpus/lessons/round-43.md` | the Gate record, the flip lines, the router's own wording | `## Gate` = `:21-53`; refused rows = 2; flip lines at `:44-47` |
| `corpus/lessons/round-43-verifier-spotcheck.md` §3, §5 | the disagreement and the routed fix | §5 R1: "Append a corrected `Flip check (round 44): task.toml — fired — …` and the same for `solve.sh`"; §3 reasons with `task.toml` alone |
| `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` (437 lines) | every citation of the two files | `task.toml` at `:41`, `:66`, `:122`, `:240`, `:300`, `:326`, `:332`, `:352`; `solve.sh` at `:52`, `:72`, `:210`, `:230`, `:251-252`, `:306`, `:350`, `:399` |
| the twelve captures, `corpus/evidence/round43/tb2-feal-differential-cryptanalysis/` | the two Gate quotes, line-for-line | `task.toml:22` = `timeout_sec = 1800.0`; `solve.sh:90` = `if (c1l ^ c2l) == 0x02000000:`; `test.sh:17-29` carries no `timeout` wrapper |
| `plans/pkg-spec-r43.json`, `plans/pkg_gate.py`, `plans/round43_c2_verify.py` | what a new row may and may not touch | `rows` = S129–S134 only; `SPEC_SHA256` pinned by V2; `c_sources`/`c_captures`/`c_provenance` iterate `spec["rows"]` only, so extra registry rows are legal and inert |
| `plans/anchor_digest_check.py` (docstring + binding rules) | whether the two digests can bind | binding rule 2 (upstream URL → task-component match against a committed `task.toml`'s `name`) binds both |
| `plans/gate_flip_check.py` (docstring, `collect_obligations`, `parse_resolution`, `resolve`) | what a corrected line can and cannot do | resolution = **first** matching line after the row; scanning is over **all** lines, not just `## Gate` |
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | row shape, enums, what the new rows must satisfy | 11 cells, kind enum includes `code`, tier enum A/B/C, E11 `used-by` path must exist |

## 2. The decision, per file — and why "admit" beats "withdraw" here

**`task.toml` → admit as S147, tier B.** Finding 11's sentence ("The only ceiling in the captured material is
`task.toml:22`'s `timeout_sec = 1800.0` for the verifier", `:299-300`; "it is the only time bound the grader's
environment actually carries", `:302`) and `:122` are claims about the graded environment. No other capture carries an
**enforced** process bound: `test.sh:17-22` runs `uvx … pytest …` with no `timeout` wrapper, and `README.md:35` only
asserts "Confirms the attack completes within the time limit" (`test.sh` full text read, 29 lines). Withdrawing the
sentence would delete a true, uniquely-sourced observation, so re-sourcing is the honest route, and the file is exactly
what S136/S137's own tier-B sentence covers (`:424-425`).

**`solve.sh` → admit as S148, tier B — and the tier-C label in `:72-74` had to be corrected anyway.** Three facts decide
this:

- The claim being re-sourced is false as written in the provenance paragraph. `:73-74` says "no finding rests on its
  internal logic"; findings 2 (`:251-252`) and 12 (`:306`) and the `oracle-solve-sh` Mechanism row (`:230`) all do.
- **Withdrawal is blocked by the frozen round-43 counter.** `plans/round43_c2_verify.py` V10 accepts only lines from its
  frozen `DECISIVE["oracle-solve-sh"]`, which is `solve.sh` lines `59, 63, 67, 68, 78, 90, 96` — not `test_outputs.py:30`.
  An erratum that withdrew the `solve.sh:90` reading while the Mechanism table keeps citing it (the append rule forbids
  editing the table) would leave the entry self-contradictory *and* the frozen predicate holding up a claim the entry no
  longer makes.
- **Tier C is unavailable, not merely undesirable.** `corpus/SOURCES.md:15`: C is "lead only, never sole support for an
  admitted entry"; `corpus/QUALITY.md` Q2 (`:25-27`): "a tier-C row never stands alone". S148 stands alone as the support
  of one Mechanism row's decisive line. So the choice is A or B. A is "primary or authoritative for the row's scope
  (spec, official docs, source code …)" (`SOURCES.md:12-13`) — but the tier is scoped (`:7-9`), and this row's scope is
  the oracle recipe the probe executes, not the graded rule (`test_outputs.py:30`, S129). B is what S136/S137 were given
  for the same role, and consistency with that sentence is the deciding argument.

Tier aside, the registry arithmetic is small and additive: two rows, both already in the committed capture manifest, no
spec change (the spec is digest-pinned and may not gain rows — the same constraint that put S136/S137 outside it).

## 3. Draft (a) — the two lesson lines

File: `.ufo/waves/round-44/wave/R44FlipLines/lesson-flip-lines.draft.txt`. Insertion point: `corpus/lessons/round-43.md`
**after line 47** (the `merge/kengaku/` flip line) and before the blank line preceding `Gate prose:` (`:49`) — inside the
`## Gate` section. The two lines, verbatim:

```
Flip check (round 44): task.toml — fired — the landed entry rests on `task.toml:22` alone (finding 11, `:299-302`, "it is the only time bound the grader's environment actually carries"; also `:41`, `:122`, Mechanism row `:240`); admitted as S147 (tier B), entry errata E3/E4
Flip check (round 44): solve.sh — fired — the landed entry rests on `solve.sh:90` alone (Mechanism row `:230` quotes "if (c1l ^ c2l) == 0x02000000:", finding 2 `:251-252`, finding 12 `:306`); admitted as S148 (tier B), entry errata E5/E6
```

Evidence lines are re-read and pasted in that draft file (the `grep -n` output for both files, as the assignment
requires). Each evidence fragment is ≤25 words and verbatim on the cited line.

## 4. Draft (b) — `## Errata (round 44, closure R1; nothing above edited)`

File: `.ufo/waves/round-44/wave/R44FlipLines/entry-errata-round44.draft.md` (80 lines, appended at EOF after the existing
`## Errata (round 43 …)` block). Shape: a preamble that states what fired and what was admitted (S147/S148, tier B,
outside the frozen spec, with re-measured provenance), then four items and two named limits.

| item | target of the correction | disposition |
|---|---|---|
| **E3** | finding 11 `:299-302`, plus `:40-41` and `:122` | re-sourced to S147, **not** withdrawn; scope narrowed to S147; `:66`'s "read only, never exercised" and `:326-332`'s "untested" both stand |
| **E4** | Mechanism row `slow-oracle-45s` → `task.toml:22` (`:240`) | re-sourced to S147; decisive line and quote unchanged |
| **E5** | Mechanism row `oracle-solve-sh` → `solve.sh:90` (`:230`), finding 2 (`:251-252`), finding 12 (`:306`) | re-sourced to S148; two bounds travel with it — see F4 below |
| **E6** | the provenance paragraph `:72-74` and `task.toml`'s parenthetical `:66` | three superseded statements named (`own reading, tier C`; `not a registry row`; `no finding rests on its internal logic…`), the surviving clauses preserved (`it runs as the oracle-solve-sh case's recipe inside the sandbox`; the receipt's tier A; `setup.py`/`feal.h`/`SHA256SUMS` remain captured, not rows) |

The two limits: (i) the round-43 Gate carried **no** quote for `solve.sh` (it quoted `task.toml:22` only), so S148's
anchor quote is supplied from the capture at its cited line — a thin Gate record, not a wrong one; (ii) the corrected
verdict is **not machine-visible**: `gate_flip_check.py` takes the first matching line, so the round-43 `not fired` line
stays the recorded resolution while the tool is green (measured, F2 below).

## 5. Draft (c) — the two `corpus/SOURCES.md` rows

File: `.ufo/waves/round-44/wave/R44FlipLines/sources-rows.draft.md`, to be inserted directly after the `S137` row. Both
11-cell rows are printed there in full; their anchors:

| id | source | kind | tier | anchor | sha256 |
|---|---|---|---|---|---|
| S147 | `task.toml` (`<base>task.toml`) | `code` | B | `task.toml:1-41, :22 "timeout_sec = 1800.0" (3 words)` | `dcb9f2f15047…e2383eecb` |
| S148 | `solution/solve.sh` (`<base>solution/solve.sh`) | `code` | B | `solution/solve.sh:1-102, :90 "if (c1l ^ c2l) == 0x02000000:" (6 words)` | `6846dd2877aa…4071a9620` |

Both `mined`, opened 2026-10-26, recheck `180d`, used-by
`corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md`. **Do not** add them to `plans/pkg-spec-r43.json`: that
spec is digest-pinned by `round43_c2_verify.py` V2, which is also why S136/S137 live outside it.

## 6. Measurements — before → after, commands and envelope lines

All runs inside the round-44 envelope (`claims/envelope.sh "$S" …`, `S=/fast/scratch/hyaku/kengaku-r44/R44FlipLines`),
in a `--shared` clone of the lane at `5e3d3aa06c6b7000929ac3e62563a39159c4501f` (tip at the time of the clone;
`git -C "$S/lane" rev-parse --show-toplevel` printed `$S/lane`). The clone was the fixture; the lane itself was never
written. "After" = the clone with the three drafts applied (`git -C "$S/lane" diff --numstat` → `2/0` SOURCES, `81/0`
entry, `2/0` lesson: **85 insertions, 0 deletions**, three files).

| # | check | before (clone at tip) | after (drafts applied) |
|---|---|---|---|
| 1 | `python3 plans/round43_c2_verify.py --lane . --work …` (round-43 C2 = the package gate the entry lives in) | `checks=10 defects=0`, `PREDICATE C2 pass`, exit 0 (`gate: defects=0`, V1–V10 all `ok`, wall 99.86 s) | `checks=10 defects=0`, `PREDICATE C2 pass`, exit 0 (wall 98.94 s, final draft bytes) — V3 `rows=6`, V4 `cases=12`, V9 `case_rows=12/12`, V10 `mechanism_rows=12/12` unchanged; `P4 ok checked=18 bad=0`, `P7 ok source_lines=6`, `P8 ok index_rows=50 knowledge_files=50`, `P10 ok probe_rerun=byte-equal bytes=3292` |
| 2 | `python3 plans/anchor_digest_check.py --lane . --evidence-ref index` | `rows=130 tokens=36 defects=0`, exit 0 | `rows=132 tokens=38 defects=0`, exit 0; `BIND S147 … by=url-task`, `BIND S148 … by=url-task`, both `RESOLVED` with the pinned digests |
| 3 | `sources-census.sh validate --file …/corpus/SOURCES.md` | `ok`, 15 `W04` (S040…S100, pre-existing), exit 0 | `ok`, 15 `W04`, exit 0 — no new E/W for S147/S148 |
| 4 | `python3 plans/gate_flip_check.py --lesson corpus/lessons/round-43.md` | `FLIPS total=2 unresolved=0`, `resolution=line:46:not fired:round=43`, exit 0 | identical (`resolution=line:46:not fired:round=43`), exit 0 — the corrected line does **not** displace the stale one (F2) |
| 5 | placement experiment (stale line deleted from a copy) | — | line inside `## Gate` → `resolution=line:47:fired:round=44`; same lines at EOF → `resolution=line:105:fired:round=44`; both exit 0, so placement affects readability, not the tool's verdict |

ENVELOPE receipts (Q32). Every run ended with the same content digest on both sides of the bracket, so no measurement is
`INVALID`. The `ENVELOPE end` lines below are verbatim as printed; start lines were printed only for the runs whose full
stdout I kept, and are given for those three only (I do not reconstruct the others):

```
ENVELOPE start 20:36:25 cwd=/fast/scratch/hyaku/kengaku-r44/R44FlipLines/lane        (anchor, before)
ENVELOPE end   20:36:27 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE end   20:36:30 exit=0 … unchanged                                            (census, before)
ENVELOPE start 20:36:31 cwd=…/lane                                                     (flip check, before)
ENVELOPE end   20:36:33 exit=0 … unchanged
ENVELOPE end   20:38:03 exit=0 … unchanged                                            (round-43 counter, before; 99.86 s)
ENVELOPE end   20:41:26 exit=0 … unchanged                                            (placement A)
ENVELOPE end   20:41:29 exit=0 … unchanged                                            (placement B)
ENVELOPE start 20:42:43 cwd=…/lane                                                     (anchor, after)
ENVELOPE end   20:42:45 exit=0 … unchanged
ENVELOPE end   20:42:51 exit=0 … unchanged                                            (census, after)
ENVELOPE end   20:42:54 exit=0 … unchanged                                            (flip check, after)
ENVELOPE end   20:44:21 exit=0 … unchanged                                            (round-43 counter, drafts applied)
ENVELOPE end   20:46:20 exit=0 … unchanged                                            (round-43 counter, final bytes; 98.94 s)
```

The sandbox shape, from one full `ENVELOPE` line (after the argv the command follows):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind $S $S --bind $S/home-cache /home/vgpnk/.cache
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- <command>
```

Provenance re-measured (not carried from round 43): both pinned URLs re-fetched 2026-10-26 20:38 -03 —

    $ curl -sS -o task.toml  -w '%{http_code}' …/feal-differential-cryptanalysis/task.toml          → 200, 928 bytes
    $ curl -sS -o solve.sh   -w '%{http_code}' …/feal-differential-cryptanalysis/solution/solve.sh   → 200, 2644 bytes
    $ cmp …  → identical, identical
    $ sha256sum → dcb9f2f15047…e2383eecb, 6846dd2877aa…4071a9620

Quote check on the drafts themselves (each fragment normalised-whitespace-matched against the entry or the capture at its
cited line): 15/15 `OK`, every fragment ≤25 words — including the two capture quotes `task.toml:22` (3 words) and
`solve.sh:90` (6 words).

## 7. Findings

- **F1 — the round-43 verdict was false for 2 of the 5 refused files, and the record was wrong about which.** `task.toml`
  (finding 11, `:299-302`, `:122`, `:40-41`; Mechanism row `:240`) and `solve.sh` (`:230`, `:251-252`, `:306`) each carry
  an entry sentence that rests on them alone. `setup.py`, `feal.h` and `SHA256SUMS` do not: no sentence rests on them
  alone, so the refused row is now 2/5 fired, 3/5 not.
- **F2 — `plans/gate_flip_check.py` cannot see the correction.** `resolve()` returns on the **first** matching
  `Flip check` line after the row, and it scans **all** lines (not the `## Gate` section), so appending the corrected line
  after the stale one changes nothing (`resolution=line:46:not fired:round=43` before and after); with the stale line
  removed, the same appended line resolves it (`resolution=line:47:fired:round=44`). This is the measured reason the Q35
  extension is still owed: the tool tests that a line exists, never that its verdict is true.
- **F3 — the round-43 Gate record was thin for `solve.sh`.** The refused row quoted `task.toml:22` but described
  `solve.sh` only as "the oracle end state (an input to the probe)" (`corpus/lessons/round-43.md:41`). The erratum
  supplies the missing quote from the capture rather than pretending the Gate had one.
- **F4 — finding 12's `solve.sh:90` claim is bounded by the code, and the bound is now named.** `solve.sh:59` is
  `candidates = list(range(0xFFFF))` → seeds 0–65534 (`len=65535, max=65534`, `65535 not in range`);
  `:95-96` index `candidates[0]`. A draw whose sixth key seed were `65535` (1 in 65536) lies outside the survivor set, so
  the oracle would index an empty list. That bounds the oracle, not the grader, and the entry's existing oracle-correctness
  limit (`:399`) still stands. Both bounds are in E5; neither is claimed as observed.
- **F5 — a tier-C label on `solve.sh` would have been a Q2 violation, not a modesty.** `corpus/SOURCES.md:15` and
  `corpus/QUALITY.md` Q2 (`:25-27`) forbid a tier-C row as sole support; S148 is sole support of one Mechanism row's
  decisive line. That is why E6 corrects the label rather than keeping the paragraph's own wording.
- **F6 — the frozen spec is not the place for these rows, and the drafts respect that.** `plans/pkg-spec-r43.json` is
  digest-pinned (`SPEC_SHA256`) by `round43_c2_verify.py` V2; adding a row there would turn the frozen predicate red.
  Registry-only rows keep `V3 rows=6` and `c_captures`' manifest completeness unchanged — measured (check 1 after).

## 8. Not done (out of scope for this seat, and why)

- **No lane edit.** The three blocks are drafts; the L1 integrates. Measured read-only at the end of the seat:
  `git -C <lane> status --porcelain -- corpus/lessons/round-43.md corpus/SOURCES.md
  corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` → empty (the three target files are untouched). The
  lane's other modified paths (`SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/routed-findings.jsonl`) are
  other seats' in-flight work, not mine.
- **No instrument change.** The Q35 / `gate_flip_check.py` extension (a `not fired` verdict naming a file is red when the
  entry carries a `<file>:<line>` citation of it) is the third leg of R1 and a wave item of its own; my erratum says so
  explicitly and does not claim the instrument was fixed.
- **`plans/round44_c2_verify.py` was not run here.** It reads its own entry
  (`corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md`), which does not exist at the clone tip I measured, so a run
  would report absence-of-surface, not my change. The only surface round 44's counter shares with this work is
  `corpus/SOURCES.md` through the census, and that leg is measured green (check 3). The round-43 counter was run instead,
  because that is the package this entry belongs to.
- **`corpus/README.md` was not drafted.** Its index row (line 76) and coverage bullet (line 273, "S129–S134") enumerate
  ids, but the `c_readme` clause iterates the frozen spec's rows only, so no check depends on S147/S148 appearing there.
  If the L1 wants the prose exact, append a round-44 line instead of editing line 76 — noted at the end of the SOURCES
  draft.

## 9. Limits

- Everything measured here is measured on **host** python and a `--shared` clone; no image was pulled and no network
  beyond the two `raw.githubusercontent.com` fetches.
- The erratum's claim that the two rows "stand alone" as sole support is a reading of the entry's current text: if the L1
  instead withdraws findings 2/12 at integration, S148's necessity changes (and the frozen V10 would then be the thing to
  argue with, not this seat).
- `S147`/`S148` are the next free ids **at my read** (registry 130 rows, max `S137`; round 44 takes `S138`–`S146`). If the
  L1 lands a different row set first, renumber; nothing else in the drafts is id-sensitive except the two `Flip check`
  lines and E3–E6's cross-references.
- The `anchor_digest_check` binding is by upstream URL through the committed `task.toml`'s `name` field —
  `by=url-task` in the verbose output. A later change to that field would unbind both rows without touching their
  digests.

## 10. Artifacts

| path (under `.ufo/waves/round-44/wave/R44FlipLines/`) | what it is | sha256 |
|---|---|---|
| `lesson-flip-lines.draft.txt` (3711 B) | the two `Flip check (round 44)` lines + insertion point + the `grep -n` evidence | `59d3e6c8d80f08071f7b256b83b92219dd1d432c81bec90c86537326f73ebbe5` |
| `entry-errata-round44.draft.md` (8284 B) | the `## Errata (round 44 …)` section (E3–E6 + two named limits) | `6b10e4cf7be1d3593e481bbb0beaf441df5bae05ec674bed6315a55636e09bda` |
| `sources-rows.draft.md` (5857 B) | the two 11-cell `corpus/SOURCES.md` rows + the tier argument + re-fetch receipt | `2c138feb594854fee30a5590199d676c8181e625f9a36bb5a342d8d7c89ecdee` |

The same three lines are in the subdir file `SHA256SUMS`. Scratch (`/fast/scratch/hyaku/kengaku-r44/R44FlipLines`,
containing the `--shared` clone the measurements ran in) is removed with `plans/scratch_guard.py safe-rm` at the end of
this seat; no receipt lives there.

The verdict count `3` is the three draft artifacts above: (a) the two lesson lines, (b) the entry erratum, (c) the two
SOURCES rows. Inside them: 2 flip lines, 4 erratum items (E3–E6), 2 registry rows.

VERDICT: r1-drafts-3
