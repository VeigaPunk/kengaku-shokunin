# R42QualityDraft — two QUALITY criteria drafted (kengaku round 42, wave 1)

Scribe seat. Draft only: **nothing in `corpus/`, `plans/`, the lane's git index or any lane surface was written.**
The two blocks in §1/§2 are ready to append verbatim to `corpus/QUALITY.md` by the L1 (Q33, Q34 follow Q32; the
file's last content is the round-41 wave-2 errata block at `corpus/QUALITY.md:677-688`).

Baseline lane tip at read time: `fda71ae round-42: wave-1 spec and dispatch (39 seats, policy v1)`.

## 0. What this seat decides

- **Q33** is drafted from this round's mined mistake (`plans/round-42-claims.md:105-109`): a carried mutant table's
  direction cells must be **re-derived through the frozen counter before freeze**. I measured the size of the class
  rather than repeating the claims file: of the **14 carried direction cells, 2 differ** (`XO5`, `XO6`, both
  `rc-silence` in round 40 → `rc-mirror` re-derived, `CARRIED-DIRECTIONS total=14 differ=2`), and the discriminating
  control (`claims/control-c1-direction-mislabel.txt`) reddens the frozen predicate when the carried labels are
  restored (`MUTANTS total=14 killed=12 survived=2`, `MUTANTS-BY-TOOL anchor=9/9 order=3/5`, `PREDICATE C1 fail`).
- **Q34** is drafted from round-41 closure **R4** (`corpus/lessons/round-41-verifier-spotcheck.md:116`, defect D2 at
  `:30-36`): a `SOURCES` row's non-mutable cell is corrected only by a new row opening `supersedes S0NN —`. I built
  the missing executable check and measured it on committed history: **15 in-place non-mutable-cell edits in 8 commits,
  none with a superseding row**, plus a green/red fixture pair (2 commits → `violations=0`, exit 0; third commit an
  in-place `anchor` edit → `violations=1`, exit 1).

Both are drafted in the file's existing shape (`## RoundNN criterion — …`, then `- **Qnn — …**`, `Check (executable,
round-42 instance):`, `Shown able to fail:`, `Limits:`, `Lesson: … Supersedes: …`), matching Q29–Q32
(`corpus/QUALITY.md:501-688`).

## 1. Draft criterion Q33 — append after `corpus/QUALITY.md:688`

```markdown
## Round42 criterion — a carried direction cell is re-derived through the frozen counter before freeze

- **Q33 — a kill-direction cell carried from another round's campaign into this round's mutant table is
  re-derived from that campaign's own recorded reference/mutant outcome before the table is frozen, and the
  re-derivation is priced by a control that restores the carried cell and reddens the predicate.** Q29 binds a
  *frozen* mutant's direction and cannot run before a battery exists — its own Check line says `UNWITNESSED`
  "is not a verdict, so the check cannot run before some battery exists" (`corpus/QUALITY.md:516-517`) — so a
  table inherited from a prior round is exactly the object that escapes it. Round 40 exhibits the gap: its
  near-variant table labelled `XO5` and `XO6` `rc-silence`
  (`.ufo/waves/round-40/falsify/F40XMutLedgerOrder.md:70-71`) while its own §2 witness text recorded the opposite
  pair for both — "the reference scans `commits=1` and PASSes; the mutant scans `commits=2` … → FAIL rc=1"
  (`:122-124`), and "a claims blob `P10 PASS receipt unreadable` is invisible to the reference and a HIT to the
  mutant" (`:127-128`). Under the round-42 counter's own vocabulary (`plans/round42_c1_verify.py:42-45`:
  `rc-silence` = fixture `expect=reject`, reference exits 1, mutant exits 0; `rc-mirror` = fixture `expect=accept`,
  reference exits 0, mutant exits 1) those recorded pairs are `rc-mirror`: reference 0 → mutant 1, the mutant
  STRICTER. The round-41 plan carried the list without re-deriving it (`plans/round-42-claims.md:105-109`), and
  round 42's freeze re-derives both to `rc-mirror` (`plans/round42_c1_verify.py:38-41`, table rows `:201`, `:206`).
  Measured at the criterion's creation (2026-10-26, this lane, tip `fda71ae`): `CARRIED-DIRECTIONS total=14
  differ=2 ids=XO5,XO6` — the other twelve carried cells (X1 X3 X6 X7 X9 X12 X13 X14 X15 XO1 XO3 XO7) re-derive
  unchanged at the head, and the three that carry a class keep it too (X6 `digest-wrong-capture`, X7
  `digest-unknown`, X14 `erratum-digest-unresolved`, read off `.ufo/waves/round-40/falsify/F40XMutAnchor.md:71-72,79`
  and `plans/round42_c1_verify.py:156,161,181`).
  Check (executable, round-42 instance), three commands, the first two red and the third the landed green:
  (a) `python3 plans/carried_direction_diff.py --lane .` prints one `CARRIED <id> round40=<cell> round42=<cell>
  same|DIFFERS fixture=<fid> attributed=<Lnnn>` line per carried mutant and `CARRIED-DIRECTIONS total=14
  differ=2 ids=XO5,XO6`, exit 0 — this is a derivation report, not the gate: it prints `differ=2` because the
  freeze corrected two cells, and a freeze that had copied the round-40 labels would print `differ=0` and look
  clean, which is why (b) is the discriminating half (tool draft at
  `.ufo/waves/round-42/build/R42QualityDraft/carried_vs_rederived.py`, sha256 `47151f23…`, to land as
  `plans/carried_direction_diff.py` for this line to run as written);
  (b) restore the carried cells — `git apply .ufo/waves/round-42/claims/control-c1-direction-mislabel.patch`
  (four lines: `XO5` and `XO6` back to `rc-silence`) on a scratch copy of `plans/round42_c1_verify.py`, run it in
  development mode with the witness fixtures — prints `MUTANT XO5 order rc-silence SURVIVED
  exhibits=0>1,rc-mirror` (`claims/control-c1-direction-mislabel.txt:29`), the same for `XO6` (`:30`),
  `MUTANTS total=14 killed=12 survived=2 invalid=0 null_detected=0 unattributed=0` (`:33`),
  `MUTANTS-BY-TOOL anchor=9/9 order=3/5` (`:34`), `PREDICATE C1 fail` (`:37`), `exit=1` (`:38`);
  (c) unpatched, the frozen labels — `MUTANT XO5 order rc-mirror killed by=w-xo5-post-receipt-blob attributed=L117`
  and `MUTANT XO6 order rc-mirror killed by=w-xo6-p10-pass-line attributed=L53`
  (`claims/witness-run.txt:29-30`), `MUTANTS total=14 killed=14 survived=0 … unattributed=0` (`:33`),
  `MUTANTS-BY-TOOL anchor=9/9 order=5/5` (`:34`).
  Shown able to fail: (b) is the red half and it fails on exactly the two restored cells — the receipt shows the
  declared cell and the exhibited set disagreeing on the same line (`declared=rc-silence … exhibits=…,rc-mirror`)
  and the predicate at `killed=12`; the round-40 record itself is the other red half, where a table cell contradicts
  the §2 paragraph three lines above it. The green half is not trivially green either: the same run reports
  `killed=14` only with the re-derived cells, so a round that copies a label without re-deriving it loses a kill
  it could have had.
  Limits: the cell vocabulary is the counter's four names (`silence`, `rc-silence`, `rc-mirror`, `error`, `:42-45`),
  so the re-derivation compares the *head* — X6/X7/X8/X10/X14's round-40 cells carried a class as
  `silence/<class>` (`.ufo/waves/round-40/falsify/F40XMutAnchor.md:71-73,75,79`) and the frozen table keeps it
  in a separate `class` column (`plans/round42_c1_verify.py:156,161,181`, e.g. `('X6', 'anchor',
  'digest-wrong-capture', 'silence', 'direct',`), so `carried_direction_diff.py` compares heads only and a wrong
  class under the right head passes both it and the counter's direction check (the counter still matches the
  fixture's printed classes, `FIXTURE … declared=digest-wrong-capture`); a mislabel's cost is a survivor, not a
  wrong green —
  (b) shows `killed=12` and `fail`, so the failure mode is an honest stop plus a wasted fixture, which is why the
  criterion prices the re-derivation at freeze instead of in the battery; the check reads a *recorded* run
  (`claims/witness-run.txt`), so a wrong label paired with a matching wrong witness would pass (a) and only (b)'s
  independent restore would catch it; twelve of fourteen cells already agreed, so this freeze's discrimination is
  two cells and a wholly copied-and-correct table demonstrates nothing; and Q29's instrument remains the
  post-battery one and defaults to a different counter (`plans/mutant_direction_check.py:92`
  `--counter plans/round38_c1_verify.py`), so it must be pointed at `plans/round42_c1_verify.py` to speak about
  this round at all.
  Lesson: `plans/round-42-claims.md:105-109` §Frontier step (mined mistake, captured-by Q29 "not applied because
  that table was never frozen"); carried-table provenance
  `.ufo/waves/round-40/falsify/F40XMutLedgerOrder.md:70-71` against its own §2 `:120-128`; the class lands in
  `corpus/lessons/round-42.md` §Mistakes when the round writes it (absent at this draft: `ls
  corpus/lessons/round-42.md` → `No such file or directory`). Supersedes: none; extends Q29's direction rule with
  the pre-battery leg Q29's own check cannot reach.
```

## 2. Draft criterion Q34 — append after Q33

```markdown
## Round42 criterion — a SOURCES row is corrected by a new superseding row, never in place

- **Q34 — every cell of a `corpus/SOURCES.md` registry row except `status`, `recheck` and `used-by` is immutable
  under its id: a correction lands as a NEW row whose `teaches` cell opens `supersedes S0NN —`, and an in-place
  change is a rule-2 defect even when the round wrote the row itself and the cell it corrects is its own anchor.**
  The rule is written twice and enforced nowhere: `SOURCES-CONTRACT-v1.md:49-51` "Only `status`, `recheck` and
  `used-by` change in place … A correction is a new row whose `teaches` opens `supersedes S0NN —`"
  (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`), restated at
  `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`. No lane tool reads it from committed history: of the tools
  naming `corpus/SOURCES.md`, none calls `rev-list`/`git show`/`git log` (`grep -ln 'corpus/SOURCES.md' plans/*.py`
  crossed with `grep -E 'rev-list|git\.show|git log'` → no file); `plans/registry_check.py` parses the working-tree
  registry only (`parse_registry(text, …)`, `:20`); `plans/state_check.py`'s supersede regexes match round-revision
  lines, not registry rows (`:206`); and `plans/round33_c1_verify.py:170,210` only *writes* the refused-duplicate
  rows (`"supersedes {sid} — duplicate staged row refused"`) without checking any row's immutability. Round 41
  measured one instance and
  routed the fix as prose (R4): in `53b9e4e5` the `S124` `anchor` cell changed in place —
  `git diff --numstat 74513c06 53b9e4e5 -- corpus/SOURCES.md` → `1	1`, old text "`PR body §Proposed PR
  description`", new text "`PR body preamble paragraph (pr245-body.md:11; …)`" — no `supersedes S124 —` row
  exists in the file (`corpus/lessons/round-41-verifier-spotcheck.md:30-36`, routed `:116`). Measured at the
  criterion's creation (2026-10-26, tip `fda71ae`, `python3 …/sources_appendonly.py <lane>` /
  `build/R42QualityDraft/receipt-lane.txt`): `SOURCES-COMMITS scanned=36 rows_at_tip=117`, `SOURCES-APPENDONLY
  violations=15 arity=0`, exit 1 — the class is older and wider than the routed item: `S081 scope`, `S082 anchor`
  (`706ed3f2`), `S086 tier` + `S086 scope` (`9af639c9`), `S092 anchor`, `S100 anchor` (`f6422263`), `S100 anchor`
  (`634ded8e`), `S103 source`, `S104 source`, `S104 teaches` (`6c20dd8d`), `S105 anchor`, `S107 anchor`
  (`1d4084fa`), `S046 anchor`, `S052 anchor` (`ec172168`), `S124 anchor` (`53b9e4e5`) — 15 cells in 8 commits
  across rounds 30, 31, 33, 35, 40 and 41, and none of the 15 was ever repaired by a superseding row for that id
  (`repair_row=none` on all 15; a second run also asked whether a `supersedes` row appeared in ANY later commit:
  `supersede_same_or_later=NO` for all 15). The mechanism is not invented here:
  `grep -c 'supersedes S0[0-9][0-9]' corpus/SOURCES.md` → `17`, of which 15 are correcting rows —
  `S026←S023 S036←S025 S039←S034 S040←S035 S042←S030 S047←S037 S048←S043 S058←S050 S064←S054 S066←S038
  S067←S066 S068←S061 S069←S062 S075←S071 S076←S075` — and two are refused-duplicate records that name
  themselves (`S094`, `S097`: "duplicate staged row refused after registry collision").
  Check (executable, round-42 instance): `python3 plans/sources_appendonly.py --lane .` prints one
  `CELL <sha8> <id> <cell> repair_row=same-commit|none` line per in-place non-mutable-cell change, then
  `SOURCES-COMMITS scanned=<n> rows_at_tip=<n>` and `SOURCES-APPENDONLY violations=<n> arity=<n>`, exit 1 iff
  `violations>0`; it reads commits only (`git log`/`git show` over `corpus/SOURCES.md`), so the working tree and
  index cannot satisfy it. On the lane tip it prints `violations=15`, exit 1 (red list above). The check is not
  always red: a two-commit fixture whose second commit only ADDS a row opening `supersedes S001 —` prints
  `SOURCES-COMMITS scanned=2 rows_at_tip=2`, `violations=0`, exit 0, and the same fixture plus a third commit that
  edits `S001`'s `anchor` in place prints `CELL 6888d84c S001 anchor repair_row=none`,
  `SOURCES-APPENDONLY violations=1`, exit 1 (`build/R42QualityDraft/receipt-{green,red}.txt`; the tool is a draft
  at `build/R42QualityDraft/sources_appendonly.py`, sha256 `f1b84d8a…`, and must land as
  `plans/sources_appendonly.py` for this line to run as written).
  Shown able to fail: the two fixtures above differ by one commit and one cell — the green one corrects by adding
  a row, the red one corrects by editing the row — and the tool separates them with exit 0 / exit 1; on the lane's
  own history the 15 `CELL` lines are the red half, the routed `S124` case among them.
  Limits: the check is act-level and red on history from round 30, so as a gate it binds from round 42 forward;
  this criterion names the 15 older cells and does **not** re-adjudicate them — at least one was a substantive
  tier change made in place on purpose (`9af639c9` "S086 is not peer-reviewed (society stamp) — relabel and tier
  to B", `tier` A→B plus a `scope` change), which rule 2 forbids and which the round-30 lesson's old→new logging
  does not cure, since the three mutable cells are the only ones logging covers; a row carrying a literal `|`
  inside a cell would parse as an arity mismatch and is reported (`arity=<n>`, exit 1) rather than silently
  misread — `arity=0` over 117 rows × 36 commits says no such row exists today; an in-place edit that was never
  committed is invisible (the same blind spot Q30's gate names); `status`, `recheck` and `used-by` changes are
  deliberately not flagged and their required old→new logging is not checked, because the log lives in the lesson
  and this tool reads `corpus/SOURCES.md` only; a commit that edits a cell and adds the superseding row in the same
  commit is still reported (rule 2 is act-level: the old row is never rewritten), and the column is printed as
  `repair_row=same-commit` so a reader can see the shape; a squash-merge that folds an edit and its revert into
  one tree hides both; and the check says nothing about whether the correcting row's new content is true — that is
  Q1/Q3/Q26's work — nor whether the id a `supersedes` cell names exists: two registry rows name themselves
  (`S094`, `S097`, both refused-duplicate records), which this tool reports as context and does not adjudicate.
  Lesson: routed item R4 and closure defect D2, `corpus/lessons/round-41-verifier-spotcheck.md:30-36` and `:116`;
  rule text `SOURCES-CONTRACT-v1.md:49-51` and `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`. Supersedes: none;
  it is the first executable leg of rule 2 and supersedes no criterion.
```

## 3. Evidence — commands and observed output

All counter/fixture work ran inside the Q32 envelope (see §6); every quote is ≤25 words.

| # | claim | command | observed |
|---|---|---|---|
| E1 | round-40 order table labelled XO5/XO6 `rc-silence` | `sed -n '66,72p' .ufo/waves/round-40/falsify/F40XMutLedgerOrder.md` | `:70` `\| XO5 \| … rev-list … "HEAD" … \| rc-silence \| **SURVIVED** \|`; `:71` `\| XO6 \| … verdict set … \| rc-silence \| **SURVIVED** \|` |
| E2 | its own witness text recorded the rc pair | `grep -n 'the mutant scans\|invisible to the' …F40XMutLedgerOrder.md` | `:123` "the mutant scans `commits=2` and prints"; `:124` "`ORDER HIT …` → FAIL rc=1 … the mutant is *stricter*"; `:127-128` XO6 "invisible to the reference and a HIT to the mutant" |
| E3 | the frozen counter re-derives both to `rc-mirror` | `grep -n "'XO5'\|'XO6'" plans/round42_c1_verify.py` | `:201` `('XO5', 'order', '-', 'rc-mirror', 'direct',`; `:206` `('XO6', 'order', '-', 'rc-mirror', 'indirect',`; docstring `:38-41` names the round-40 label as wrong |
| E4 | 14 carried cells, 2 differ | `python3 build/R42QualityDraft/carried_vs_rederived.py <lane>` (envelope) | 14 `CARRIED …` lines, all `same` except `XO5` and `XO6`; `CARRIED-DIRECTIONS total=14 differ=2 ids=XO5,XO6` |
| E5 | restoring the carried labels reddens the predicate | `grep -n 'MUTANT XO5\|MUTANT XO6\|MUTANTS total\|MUTANTS-BY-TOOL\|PREDICATE' .ufo/waves/round-42/claims/control-c1-direction-mislabel.txt` | `:29` `MUTANT XO5 order rc-silence SURVIVED exhibits=0>1,rc-mirror`; `:30` XO6 same; `:33` `killed=12 survived=2`; `:34` `anchor=9/9 order=3/5`; `:37` `PREDICATE C1 fail`; `:38` `exit=1` |
| E6 | with the re-derived labels all 14 die, attributed | `grep -n 'MUTANT XO5\|MUTANT XO6\|MUTANTS total\|MUTANTS-BY-TOOL' .ufo/waves/round-42/claims/witness-run.txt` | `:29` `rc-mirror killed by=w-xo5-post-receipt-blob attributed=L117`; `:30` `attributed=L53`; `:33` `killed=14 … unattributed=0`; `:34` `anchor=9/9 order=5/5` |
| E7 | the mislabel patch is four lines | `cat .ufo/waves/round-42/claims/control-c1-direction-mislabel.patch` | one hunk, `- XO5 … rc-mirror` / `+ XO5 … rc-silence`, same for XO6; no other line touched |
| E8 | rule 2 text | `sed -n '108,130p' /home/vgpnk/Projects/shokunin/CORPUS.md` | `:116` "Only `status`, `recheck` and `used-by` change in place"; `:118` "A correction is a new row whose `teaches` opens `supersedes S0NN —`" |
| E9 | contract v1 states the same | `grep -n 'Append-only\|supersedes' .ufo/waves/kaika/SOURCES-CONTRACT-v1.md` (fleet root) | `:49` `2. **Append-only.** Only status, recheck and used-by change in place`; `:51` `supersedes S0NN —` |
| E10 | the routed in-place edit | `git diff --numstat 74513c06 53b9e4e5 -- corpus/SOURCES.md` | `1	1	corpus/SOURCES.md`; the hunk rewrites S124's `anchor` (`PR body §Proposed PR description` → `PR body preamble paragraph (pr245-body.md:11; …)`) |
| E11 | 15 in-place non-mutable-cell edits, 8 commits, none repaired | `python3 …/sources_appendonly.py <lane>` (envelope; `receipt-lane.txt`) | `SOURCES-COMMITS scanned=36 rows_at_tip=117`; 15 `CELL …` lines all `repair_row=none`; `SOURCES-APPENDONLY violations=15 arity=0`; `exit=1` |
| E12 | no later superseding row anywhere | `python3 …/supersede_later.py <lane>` (scratch, same envelope rules) | 15 `EDIT … supersede_same_or_later=NO` lines, `exit=0` |
| E13 | check is not always red | `python3 …/sources_appendonly.py fx-green` (`receipt-green.txt`) | `scanned=2 rows_at_tip=2`, `violations=0 arity=0`, `exit=0` |
| E14 | check red on a one-cell in-place edit | `python3 …/sources_appendonly.py fx-red` (`receipt-red.txt`) | `scanned=3`, `CELL 6888d84c S001 anchor repair_row=none`, `violations=1`, `exit=1` |
| E15 | no lane tool enforces rule 2 from history | `grep -ln 'corpus/SOURCES.md' plans/*.py` piped through `grep -lE 'rev-list\|git\.show\|git log'`; `grep -n 'supersedes' plans/{state_check,round33_c1_verify,round32_defects,round33_defects}.py` | no file with git history; `state_check.py:206` regex matches `- **R2[5-9]-E<n> …**` revision lines; `round33_c1_verify.py:170,210` writes refused-duplicate rows only; `registry_check.py` `parse_registry(text, source_ids)` at `:20`, no git |
| E16 | the mechanism is already in use | `grep -c 'supersedes S0[0-9][0-9]' corpus/SOURCES.md`; `grep -oE '^\| S[0-9]+ .*\| supersedes S0[0-9]+' corpus/SOURCES.md` | `17`; 15 correcting rows (`S026←S023 S036←S025 S039←S034 S040←S035 S042←S030 S047←S037 S048←S043 S058←S050 S064←S054 S066←S038 S067←S066 S068←S061 S069←S062 S075←S071 S076←S075`) and 2 self-naming refusals (`S094`, `S097`) |
| E17 | Q29's check cannot reach a pre-battery table | `sed -n '31,35p' plans/mutant_direction_check.py` | "A mutant with no observed direction is `UNWITNESSED`"; `--counter` default `plans/round38_c1_verify.py` (`:92`) |
| E18 | no round-42 lesson yet | `ls corpus/lessons/round-42.md` | `No such file or directory` |

## 4. Integration notes for the L1

1. Append §1 then §2 at the end of `corpus/QUALITY.md` (after the round-41 errata block, `:677-688`). Numbering Q33,
   Q34 is free; no `supersedes` is claimed, so no existing row changes.
2. Two Check lines name tools that do not exist in `plans/` yet. Both drafts and their receipts are in
   `.ufo/waves/round-42/build/R42QualityDraft/`; landing them as `plans/carried_direction_diff.py` and
   `plans/sources_appendonly.py` (byte-identical, sha256 below) makes the Check lines run as written. If the L1 does
   not land them, the criteria must be edited to say "draft tool at build/R42QualityDraft/" — do not leave a Check
   line pointing at a missing path.
3. Q34's Check is **red on the lane's current history (15 cells)**. Either state that in the round lesson's `## Gate`
   and keep the gate forward-binding from round 42, or narrow the check with a `--since <round-42 freeze sha>`
   floor — both are defensible; silently landing a red gate without naming the 15 is not.
4. Q33 asks for a re-derivation **per carried table**, not a new instrument: the round-42 instance is already green
   (`witness-run.txt` 14/14 attributed) and the red is the frozen control. Nothing needs to be rebuilt for it.
5. Both criteria are evidence-verified against committed and frozen artefacts only; I ran no counter and no battery
   (see §5).

## 5. Limits of this seat

- I did **not** run `plans/round42_c1_verify.py` or `plans/round42_c2_verify.py`, the probe, or any battery. Every
  number in §1/§2 is either read from a frozen receipt (`E1–E7`) or produced by my own read-only checkers
  (`E4`, `E11–E14`).
- Q34's 15 historical cells are **named, not adjudicated**. I did not open each round's lesson to decide whether the
  edit was disclosed or defensible; the criterion says the act is a rule-2 defect, and the draft carries that
  reading rather than a per-cell verdict.
- The Q34 checker's parsing assumption is `11` cells per row (`arity=0` over `117 × 36`); a future row with a literal
  `|` in a cell would surface as `ARITY`, not as a silent misread, but that path is untested here.
- My `carried_vs_rederived.py` matches the round-40 tables by their **first** row per id and takes the
  second-to-last cell as the direction (the round-40 rows embed a literal `|` in two replacements, which is why the
  first attempt mis-indexed XO6/XO7 — the corrected run is `E4`, and the wrong intermediate run is not evidence).
- No `corpus/lessons/round-42.md` exists, so both Lesson lines point at `plans/round-42-claims.md` and the round-40
  artefacts; the L1 should repoint them at the round-42 lesson when it is written.
- Out of scope and untouched: QUALITY Q29–Q32 text, the frozen tools/counters/probe/spec/gate/dry table/captures/
  receipt/freeze modules, the C1/C2 claims, and every lane file.

## 6. Host-safety and scratch receipt (Q32)

Scratch `S=/fast/scratch/hyaku/kengaku-r42/R42QualityDraft`; round-root sentinel present
(`ls -d /fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL` → the path); all fixture repos under `$S`
(`git -C <dir> rev-parse --show-toplevel` → the same dir, checked at creation). Deletes stayed inside `$S`
(`rm -rf -- "$S/fx-good"`, `"$S/fx-green"`, `"$S/fx-red"` — each literal starts with `$S/`).

Envelope used for every check that reads a repo (three runs, plus the first 17:27 tuning run):

```
/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 <checker> <repo>
```

| run | start | end | `ls -A ~/.local/bin \| sha256sum` before | after |
|---|---|---|---|---|
| tuning (lane) 17:27 | 17:27:18 | 17:27:18 | `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` | same |
| lane (`receipt-lane.txt`) | 17:29:34 | 17:29:34 | `436b361f…d63fc18` | `436b361f…d63fc18` |
| fx-green (`receipt-green.txt`) | 17:29:29 | 17:29:29 | `436b361f…d63fc18` | `436b361f…d63fc18` |
| fx-red (`receipt-red.txt`) | 17:29:42 | 17:29:42 | `436b361f…d63fc18` | `436b361f…d63fc18` |

Two earlier fixture runs (a first `fx-good` pass and a first `fx-red` attempt, ~17:27–17:29) printed the same
verdicts but were not receipted; the receipted green/red pair above is the one §1/§2 cites, and the red fixture was
rebuilt from `git init` for it (`FIXTURE … commits: 6888d84 inplace;a9473eb supersede;ead310a base`).

No host write outside this report, my subdir and `$S`. No `pacman`, no package or tool installed, no `sudo`, no
network fetch, no lane git/jj mutation (all git calls were read-only `-C <repo> log|show|diff|rev-parse`; the
fixture repos were `git init`-ed inside `$S` and committed with a fixed `fixture` identity and fixed dates).
Tooling note: nothing installed this seat (no version/channel/reason row needed).

## 7. Artifacts

`.ufo/waves/round-42/build/R42QualityDraft/`:

| file | sha256 | what it is |
|---|---|---|
| `sources_appendonly.py` | `f1b84d8a136ae917bc7201931bb10fa92e62eecf9293651a5741d47095b06544` | Q34 draft check (commits only; strict act-level) |
| `carried_vs_rederived.py` | `47151f23c16bca596cdb2ad302ec0b9b7e9991a4f02c35f948a771f159f89def` | Q33 draft check (round-40 cells vs re-derived) |
| `receipt-lane.txt` | `4db25114d22750af7e2c27d4d49ff414767f55f0de56ff4a5fd47a1f900b4573` | Q34 red on the lane, envelope + timestamps |
| `receipt-green.txt` | `b5b48961ec804376a73b5fe71bd700451231c13861fe726c4af3caa0748fb496` | Q34 green fixture (2 commits) |
| `receipt-red.txt` | `0c82c5dec77aaf19d9de7763f9fbe83803365802fdc49de31443cd066af3ee09` | Q34 red fixture (3rd commit in place) |
| `supersede_later.py` | `dbd20c1d2473d2005bcc900199379e5e939d3be7c6e210f60ee17501e001c619` | Q34 corroboration (E12): was any `supersedes` row added later?) |

VERDICT: quality-criteria-drafted-2
