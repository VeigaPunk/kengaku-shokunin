# R44RoutedQuality — six routed QUALITY/SCORECARD rows re-checked, fixed at the source, checks re-pointed

Seat R44RoutedQuality (scribe, leaf). Round 44 v2 wave, routed-item burn-down. Lane tip measured: `5e3d3aa`
(`git -C <clone> rev-parse HEAD` → `5e3d3aa06c6b7000929ac3e62563a39159c4501f`). Working tree for every measurement:
`git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`, `git -C "$S/lane" rev-parse
--show-toplevel` → `/fast/scratch/hyaku/kengaku-r44/R44RoutedQuality/lane`. Nothing was written to the lane, its
index, its jj state, any `corpus/`/`plans/` file, or any PATH directory; the four criterion edits, the one lesson
edit and the two appended blocks exist **only in my scratch clone** and are handed over as drafts below.

Scope: routed rows `R42-R3-18/19/20/23` (`F42RevQuality.md` D1/D2/D3/D6), `R42-R3-31`
(`F42CritScorecard.md` M1), `R42-R3-32` (`F42ConnClaims.md` §2 Drift 1).

## Axes (Godspeed)

- **Quality** (the judged axis) — every one of the six rows is a defect in a *checkable* claim. Move kept: each row
  gets a `check` that exits 0 on corrected text and 1 on the tip, measured on two trees.
- **Operability** — each replacement check is one `sh -c` line `plans/routed_open.py --observe` can run from the lane
  root (Q32 envelope, ~2 s per full 60-row observe).
- **Auditability** — every edit is given as before/after text with the command that ran it; the two instrument runs
  (draft tools, re-pointed ledger) are bracketed by ENVELOPE lines with an unchanged PATH-dir content digest.

## 1. What each row claims, measured at `5e3d3aa`

| row | source | claim | measurement at the tip | verdict |
|---|---|---|---|---|
| R42-R3-18 | `F42RevQuality.md:13` | Q33/Q34 Checks name `plans/carried_direction_diff.py` / `plans/sources_appendonly.py`, which exist in no commit | `ls plans/carried_direction_diff.py plans/sources_appendonly.py` → `No such file or directory` (both); `git log --oneline --all -- plans/carried_direction_diff.py plans/sources_appendonly.py \| wc -l` → `0` | **held** |
| R42-R3-19 | `F42RevQuality.md:26` | the drafts take the lane positionally, the Check lines write `--lane .` | `corpus/QUALITY.md:713` and `:795` still carry the `--lane` form; the drafts are `LANE = sys.argv[1]` (`carried_vs_rederived.py:5`) and `sys.argv[1] if len(sys.argv) > 1 else "."` (`sources_appendonly.py:13`) | **held** |
| R42-R3-20 | `F42RevQuality.md:35` | (b) prescribes dev mode but cites `PREDICATE C1 fail`; dev mode prints `n/a` | `plans/round42_c1_verify.py:525` `dev = a.battery_dir is not None or a.only is not None`; `:657` `PREDICATE C1 n/a (non-default battery or mutant subset)`; `QUALITY.md:725` lists `PREDICATE C1 fail` (`:37`) in (b)'s line set | **held** |
| R42-R3-23 | `F42RevQuality.md:73` | `:767` "No lane tool reads it from committed history" needs creation-time scope | `QUALITY.md:767` reads `No lane tool reads it from committed history: of the tools` (unscoped) | **held** |
| R42-R3-31 | `F42CritScorecard.md:66` | `SCORECARD.md:1759-1760` says every C2-class counter went red on the uv lock; round 36 passed | `SCORECARD.md:1760` `every C2-class counter went red on \`uv\`'s cache lock`; `integrate/measure-baseline-v1.txt` → `PREDICATE C2 fail` at `:51,161,239,386,522,669`, `PREDICATE C2 pass` at `:679` | **held** |
| R42-R3-32 | `F42ConnClaims.md:34` | the landing measure's own envelope records CHANGED; the drift is not in the lesson | `measure-final.txt:938` `ENVELOPE end 17:52:40 exit=0 local_bin_listing_before=763032563d3739aa after=77408cab9a10361a CHANGED`; start `17:42:34` (`:2`); `measure-tip3.txt:938` `… before=77408cab9a10361a after=77408cab9a10361a unchanged`; `grep -cF 'measure-final.txt:938' corpus/lessons/round-42.md` → `0` (the record is at `round-42-verifier-spotcheck.md:46` only) | **held** |

Substantive verification that the two row-31 evidence legs still hold:

- `integrate/measure-baseline-v1.txt` at the tip: the six fails and the one pass above.
- The `uv` leg it names: `plans/pkg_gate.py:276` `["uv", "run", "--no-project", "--with", "biopython==1.85", "python3"]`.
- The firefox symlink named by the drift row: `stat -c '%y %N' /home/vgpnk/.local/bin/firefox` →
  `2026-10-26 17:48:46.564447073 -0300 '/home/vgpnk/.local/bin/firefox' -> '/home/vgpnk/.local/opt/firefox-158.0.1/firefox'`
  — inside the `17:42:34`–`17:52:40` window.
- `measure-tip3` verdict equality (the claim the lesson append rests on): `diff <(grep -E '^(PREDICATE|MUTANTS|CHECKS|CHECK |BATTERY)' measure-final.txt) <(… measure-tip3.txt) | wc -l` → `0`.

**Refuted: 0 of 6.** Three rows carry a *stale leg* in their `note`, which is not a refutation of the finding:

1. `R42-R3-18`'s aggravating leg — "even the fallback paths do not resolve at the pinned commit" — is now false:
   `.ufo/waves/round-42/build/R42QualityDraft/` is tracked (`git log --oneline -1 -- <dir>` → `445e81f`), both
   drafts are present, and their digests equal the ones C1 pins
   (`sha256sum` → `47151f23c16bca596cdb2ad302ec0b9b7e9991a4f02c35f948a771f159f89def` and
   `f1b84d8a136ae917bc7201931bb10fa92e62eecf9293651a5741d47095b06544`). Only "land both tools" remains in the
   row's check, while C1 accepts two legs.
2. `R42-R3-19`'s note pins `sources_appendonly.py:14`; the definition is `:13` (C2 records the off-by-one already).
3. `R42-R3-32`'s note is fully confirmed at the tip (firefox mtime, both digests, verdict equality above).

## 2. What is wrong with the six checks themselves

All six exit 1 and `plans/routed_open.py --observe` reports them `observed=fail self=open` at the tip
(`OBSERVE rows=60 mismatched=0`, `ROWS total=60 open=38 blocked=1 closed=21`, `routed_open=39 oldest_round=39`). The
round-43 corrections block (`QUALITY.md:829-873`, `SCORECARD.md:1828-1844`) records C1–C6 and S1 for D1–D6, i.e. for
five of these six rows, **but closed none of them and left checks that cannot pass**:

- **Q1 — `R42-R3-31`'s check is unsatisfiable as filed.** It greps `counter that invokes`; S1's corrected wording is
  "that drives the gate's `uv` leg". `grep -qF 'counter that invokes' SCORECARD.md` → rc 1 at the tip, and no edit
  that fixes the defect can make it pass. Same class as the literal it complains about: a check coupled to wording
  nobody wrote.
- **Q2 — `R42-R3-23`'s check is unsatisfiable as filed.** It demands the exact string
  `No lane tool reads it from committed history at this criterion`; C6's own recorded correction uses
  `no lane tool read it from committed history at this criterion's creation` (lower case, past tense, and split
  across `QUALITY.md:867-868`). Applying C6 verbatim leaves the check red.
- **Q3 — `R42-R3-18`/`19` encode only the landing leg.** C1 owes "land the two drafts **or** rewrite each Check
  line"; the row's check demands `test -f` both `plans/` names, so the rewrite leg can never close it. And a
  byte-identical landing would still leave `19` red: measured, `sources_appendonly.py --lane .` → `SETUP git log
  failed: fatal: cannot change to '--lane'`, **exit 2**, and `carried_vs_rederived.py --lane .` → `FileNotFoundError
  … '--lane/.ufo/waves/round-40/falsify/F40XMutAnchor.md'`, **exit 1** — the row's own `[ rc = 0 ] || [ rc = 1 ]`
  would then accept the carried tool's crash as "it ran".
- **Q4 — `R42-R3-20`'s check is a line-range proxy.** `! sed -n '690,758p' … | grep -qF 'development mode'` would go
  green on any unrelated edit that moves or deletes that phrase, and it tests the wrong thing: the defect is that
  (b) *lists* `PREDICATE C1 fail` among the lines its dev-mode run prints.
- **Q5 — `R42-R3-32` targets the wrong reader-facing file for closure.** The row is right that the lesson is
  uncorrected; its check is fine (`grep -F 'measure-final.txt:938' corpus/lessons/round-42.md`), it simply has nothing
  to pass on yet.
- **Q6 — the ledger could not burn down.** Five corrections were recorded in round 43 and zero rows of these six
  closed, because their checks test the *pre-correction* text or a landing that never happened. This is the
  burn-down defect the six rows now close.

## 3. Drafted corrections (ready to apply; measured red → green)

All six checks below exit **1** on the tip tree and **0** on my edited clone; the two appends were then added and the
six still exit 0 (append-safety). Receipts: `R44RoutedQuality/replacement-checks2.txt` (sha256 `05e13ec7…`) and
`replacement-checks3-append.txt` (byte-identical, sha256 `05e13ec7…`).

### 3.1 `corpus/QUALITY.md` — Q33 (a), Q33 (b), Q34 Check, `:767` (the "fixes owed" C1/C3/C6 name)

```diff
-  (a) `python3 plans/carried_direction_diff.py --lane .` prints one `CARRIED <id> round40=<cell> round42=<cell>
+  (a) `python3 .ufo/waves/round-42/build/R42QualityDraft/carried_vs_rederived.py .` prints one
+  `CARRIED <id> round40=<cell> round42=<cell>
   …
-  `.ufo/waves/round-42/build/R42QualityDraft/carried_vs_rederived.py`, sha256 `47151f23…`, to land as
-  `plans/carried_direction_diff.py` for this line to run as written);
+  `.ufo/waves/round-42/build/R42QualityDraft/carried_vs_rederived.py`, sha256 `47151f23…`, run positionally — its
+  CLI is `LANE = sys.argv[1]`, so `--lane .` is read as the path `--lane` (routed `R42-R3-18/19`);
   (b) … `MUTANTS total=14 killed=12 survived=2 invalid=0 null_detected=0 unattributed=0` (`:33`),
-  `MUTANTS-BY-TOOL anchor=9/9 order=3/5` (`:34`), `PREDICATE C1 fail` (`:37`), `exit=1` (`:38`);
+  `MUTANTS-BY-TOOL anchor=9/9 order=3/5` (`:34`), `exit=1` (`:38`); development mode prints `PREDICATE C1 n/a
+  (non-default battery or mutant subset)`, so the receipt's `PREDICATE C1 fail` (`:37`) is the default battery's
+  line (29 fixtures), not this run's;
   (c) …
-  `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`. No lane tool reads it from committed history: of the tools
+  `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`. No lane tool read it from committed history at this
+  criterion's creation: of the tools
   …
-  Check (executable, round-42 instance): `python3 plans/sources_appendonly.py --lane .` prints one
+  Check (executable, round-42 instance):
+  `python3 .ufo/waves/round-42/build/R42QualityDraft/sources_appendonly.py .` prints one
   … (`build/R42QualityDraft/receipt-{green,red}.txt`; the tool is a draft
-  at `build/R42QualityDraft/sources_appendonly.py`, sha256 `f1b84d8a…`, and must land as
-  `plans/sources_appendonly.py` for this line to run as written).
+  at `build/R42QualityDraft/sources_appendonly.py`, sha256 `f1b84d8a…`, run positionally (`sys.argv[1]`,
+  default `.`); the `plans/` landing named here was never made (routed `R42-R3-18/19`).
```

The corrected Check lines run as written (positional, lane root, inside the envelope):

```
CARRIED-DIRECTIONS total=14 differ=2 ids=XO5,XO6                 # rc 0
SOURCES-COMMITS scanned=38 rows_at_tip=130                       # rc 0 (Q34's exit is 1 iff violations>0)
SOURCES-APPENDONLY violations=15 arity=0                          # rc 1
```

(`Q34`'s Check already says "On the lane tip it prints `violations=15`, exit 1"; the row count moved `121 → 130`
with round 43's rows, which the placeholder `rows_at_tip=<n>` absorbs.)

### 3.2 `SCORECARD.md:1760` — S1 applied at the source

```diff
-envelope (home read-only) every C2-class counter went red on `uv`'s cache lock (`integrate/measure-baseline-v1.txt`); v2
+envelope (home read-only) every C2-class counter that drives the gate's `uv` leg went red on `uv`'s cache lock
+(`integrate/measure-baseline-v1.txt`); v2
```

### 3.3 `corpus/lessons/round-42.md:95` — the drift record (row 32)

```diff
-  digest list. So the forward leg Q32 asks for is met for the C1 counter runs and red for one C2 control.
+  digest list. So the forward leg Q32 asks for is met for the C1 counter runs and red for one C2 control. It is
+  unproven for the landing run itself: `integrate/measure-final.txt:938` records
+  `local_bin_listing_before=763032563d3739aa after=77408cab9a10361a CHANGED` (the `~/.local/bin/firefox`
+  symlink, mtime 17:48:46, inside the 17:42:34–17:52:40 window), while `measure-tip3.txt:938` records
+  `unchanged` and its verdict lines equal the landing ones (routed `R42-R3-32`).
```

### 3.4 Appended blocks (audit trail; the lane's "criteria stay as written" convention)

Insert **after** the round-43 corrections block in `corpus/QUALITY.md` (after `:873`, before
`## Round43 criterion — a conditional Gate refusal is resolved by a recorded flip check`) and **after** S3 in
`SCORECARD.md` (`:1844`, before `## Round 43 (hyaku run 9 …)`):

```markdown
## Round42 criteria — corrections appended in round 44 (Q33, Q34; SCORECARD S1)

The six defects `F42RevQuality` routed are recorded in the round-43 block above; round 44 pays the four fixes it
named as owed, at the source, and re-points each routed check (`R42-R3-18/19/20/23`). Measured at tip `5e3d3aa`;
each check exits 1 on the pre-edit text and 0 on the edited text
(`.ufo/waves/round-44/wave/R44RoutedQuality/receipts/replacement-checks2.txt`).

- **E1 (R42-R3-18, C1's second leg).** Q33 (a) (`:713`) and Q34's Check (`:795-796`) run the committed drafts
  positionally: `python3 .ufo/waves/round-42/build/R42QualityDraft/carried_vs_rederived.py .` and
  `python3 .ufo/waves/round-42/build/R42QualityDraft/sources_appendonly.py .`. Neither `plans/` name exists in any
  commit (`git log --oneline --all -- plans/carried_direction_diff.py plans/sources_appendonly.py` → 0 lines).
  Outputs at `5e3d3aa`: `CARRIED-DIRECTIONS total=14 differ=2 ids=XO5,XO6` (exit 0); `SOURCES-COMMITS scanned=38
  rows_at_tip=130`, `SOURCES-APPENDONLY violations=15 arity=0` (exit 1).
- **E2 (R42-R3-19, C2).** Both Check lines use the drafts' real CLI (`carried_vs_rederived.py:5` `LANE =
  sys.argv[1]`; `sources_appendonly.py:13`). Measured with the flag: `carried_vs_rederived.py --lane .` →
  `FileNotFoundError … '--lane/.ufo/waves/round-40/falsify/F40XMutAnchor.md'`, exit 1; `sources_appendonly.py
  --lane .` → `SETUP git log failed: fatal: cannot change to '--lane'`, exit 2.
- **E3 (R42-R3-20, C3).** (b) no longer lists `PREDICATE C1 fail` (`:37`) among the lines its development-mode run
  prints; it states that development mode prints `PREDICATE C1 n/a (non-default battery or mutant subset)`
  (`plans/round42_c1_verify.py:525,657`) and attributes `:37` to the default battery (29 fixtures).
- **E4 (R42-R3-23, C6).** `:769-770` carries the creation-time scope: "No lane tool read it from committed history at
  this criterion's creation".

- **S4 (round 44) — S1 applied at the source.** `:1760` now reads "every C2-class counter that drives the gate's `uv`
  leg went red on `uv`'s cache lock"; routed `R42-R3-31` closes on this text (its check exits 1 on the pre-edit text
  and 0 here, `.ufo/waves/round-44/wave/R44RoutedQuality/receipts/replacement-checks2.txt`).
```

(The S4 bullet goes into the `SCORECARD.md` block `### Round-42 corrections appended in round 43`; the E1–E4 bullets
go into the QUALITY block — they are shown together here only to keep the hand-off in one place.)

## 4. Replacement `check` commands (one line each, run from the lane root)

Measured with `bash receipts/checks2.sh` (definitions in `R44RoutedQuality/checks2.sh`, sha256 `bf98e0a5…`):

| row | pristine tip | edited clone |
|---|---|---|
| R42-R3-18 | rc 1 | rc 0 |
| R42-R3-19 | rc 1 | rc 0 |
| R42-R3-20 | rc 1 | rc 0 |
| R42-R3-23 | rc 1 | rc 0 |
| R42-R3-31 | rc 1 | rc 0 |
| R42-R3-32 | rc 1 | rc 0 |

```
# R42-R3-18 (named path exists, or the Check line runs the committed draft)
for pair in "carried_direction_diff:carried_vs_rederived" "sources_appendonly:sources_appendonly"; do p=${pair%%:*}; d=${pair##*:}; { test -f "plans/$p.py" && grep -qF "python3 plans/$p.py" corpus/QUALITY.md; } || grep -qF "python3 .ufo/waves/round-42/build/R42QualityDraft/$d.py ." corpus/QUALITY.md || exit 1; done; exit 0

# R42-R3-19 (the prescribed invocation is a form the tool actually runs: header line, not a usage crash)
for pair in "carried_direction_diff:carried_vs_rederived" "sources_appendonly:sources_appendonly"; do p=${pair%%:*}; d=${pair##*:}; if test -f "plans/$p.py" && grep -qF "python3 plans/$p.py" corpus/QUALITY.md; then python3 "plans/$p.py" --lane . 2>&1 | grep -qE "^(CARRIED-DIRECTIONS total=|SOURCES-COMMITS scanned=)" || exit 1; else grep -qF "python3 .ufo/waves/round-42/build/R42QualityDraft/$d.py ." corpus/QUALITY.md || exit 1; fi; done; exit 0

# R42-R3-20 ((b)'s own block states what development mode prints)
sed -n "/(b) restore the carried cells/,/(c) unpatched/p" corpus/QUALITY.md | grep -qF "development mode prints"

# R42-R3-23 (the sentence itself carries the scope; tr joins the wrapped line)
tr -s " \n" " " < corpus/QUALITY.md | grep -qF "No lane tool read it from committed history at this criterion's creation"

# R42-R3-31 (the Envelope-note sentence itself, not the quoted original in the corrections block)
sed -n "/Envelope note: under the v1/,/^$/p" SCORECARD.md | grep -qF "counter that drives the gate"

# R42-R3-32 (unchanged from the row; green once the lesson carries the record)
grep -qF "measure-final.txt:938" corpus/lessons/round-42.md
```

They are deliberately *positive* matches on the corrected text (or on a targeted range), so an appended erratum that
quotes the old wording cannot flip them red — the trap rows 23 and 31 fell into. The general invariant behind row 18
also caught the only other `python3 <path>` in `QUALITY.md` that does not exist — `/tmp/pre_probe.py` — which is a
shell example (`QUALITY.md:355` `git show 3241b86:plans/regex_log_probe.py >/tmp/pre_probe.py && …`), not a dead
tool path, hence the `plans/` restriction.

Adjacent, **out of scope, not counted**: `QUALITY.md:771` still pins `plans/registry_check.py` `parse_registry` at
`:20`; the definition is `:25` (routed row `R42-R3-22` closed on C5 for exactly this, and the pin is still wrong at
the source — fix it in the same edit if desired).

## 5. Ledger rows (replace in place; `routed_open.py` forbids a second row per id)

Full draft file built and observed: `60 rows`, `OBSERVE rows=60 mismatched=0`, all six `rc=0 observed=pass
self=closed`, `ROWS total=60 open=32 blocked=1 closed=27 refused=0`, `routed_open=33 oldest_round=39` (from `39`).
`close` strings carry the landing commit slot `<landing>` for the L1 to fill at integration; `id`, `class`, `source`,
`opened_round` unchanged.

```json
{"id": "R42-R3-18", "status": "closed", "close": "<landing>: corpus/QUALITY.md:713 + :795-796 run the committed drafts (C1's second leg) — routed_open.py --observe rc=0", "check": "<the R42-R3-18 line above>", "note": "was: neither plans/ tool exists in any commit (verified 0 commits at 5e3d3aa). The fallback leg is now resolvable: drafts tracked, shas 47151f23…/f1b84d8a… match C1's pins."}
{"id": "R42-R3-19", "status": "closed", "close": "<landing>: corpus/QUALITY.md:713, :795-796 use the drafts' positional CLI — routed_open.py --observe rc=0", "check": "<the R42-R3-19 line above>", "note": "note pin corrected: sources_appendonly.py:13, not :14. Landing the drafts alone would not close this row: --lane exits 1 (carried) / 2 (sources)."}
{"id": "R42-R3-20", "status": "closed", "close": "<landing>: corpus/QUALITY.md:725-727 names the dev-mode predicate n/a and attributes :37 to the default battery — routed_open.py --observe rc=0", "check": "<the R42-R3-20 line above>", "note": "C3 recorded the reading; the criterion line itself still listed PREDICATE C1 fail. Now paid."}
{"id": "R42-R3-23", "status": "closed", "close": "<landing>: corpus/QUALITY.md:769-770 carries the creation-time scope — routed_open.py --observe rc=0", "check": "<the R42-R3-23 line above>", "note": "old check demanded 'No lane tool reads it … at this criterion' — a literal C6 never wrote; re-pointed at the applied sentence."}
{"id": "R42-R3-31", "status": "closed", "close": "<landing>: SCORECARD.md:1760 applies S1's scope (measure-baseline-v1: 6 fail / 1 pass at :679) — routed_open.py --observe rc=0", "check": "<the R42-R3-31 line above>", "note": "old check demanded 'counter that invokes', which no correction used; it could never pass. Re-pointed at the Envelope-note sentence."}
{"id": "R42-R3-32", "status": "closed", "close": "<landing>: corpus/lessons/round-42.md:95-99 records measure-final.txt:938 CHANGED and measure-tip3.txt:938 unchanged — routed_open.py --observe rc=0", "check": "grep -qF \"measure-final.txt:938\" corpus/lessons/round-42.md", "note": "drift confirmed at the tip: firefox symlink mtime 17:48:46 inside 17:42:34–17:52:40; verdict lines equal between measure-final and measure-tip3 (diff 0)."}
```

## 6. Evidence and envelope

Receipts (all under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44RoutedQuality/`,
9.0 kB total):

| file | what | sha256 |
|---|---|---|
| `replacement-checks2.txt` | six checks on pristine + edited trees (240 B) | `05e13ec7941540acb95844527cbcbd9144f38e0e663a76093c07920af550bccf` |
| `replacement-checks3-append.txt` | same six after the erratum appends — byte-identical | `05e13ec7941540acb95844527cbcbd9144f38e0e663a76093c07920af550bccf` |
| `observe-draft.txt` | `routed_open.py --observe` on the re-pointed ledger | `2f668e62db44b1895f2c565f47ded07a3ff9003e20dac5bcf78bfa2fb7bda379` |
| `drafts-rc.txt` | the two drafts, positional and `--lane`, with exit codes | `0a39181f7e4b987912fa7c2b81f53d7e1b4fc20911ed78c43fb5589cecb0668b` |
| `edited-check-lines.txt` | the corrected Check lines run as written | `509b4f96878a3b87a9ac49a41361ee6adc6217c5cfa0c6bdc6993818ea46e1be` |
| `checks2.sh` | the six check definitions as measured | `bf98e0a503042ab51fdfca175e096d68bcf29d456e106b6eda55d2789e67d078` |

ENVELOPE lines, verbatim (Q32; all three measurements, PATH-dir content digest unchanged):

```
ENVELOPE start 20:37:27 cwd=/fast/scratch/hyaku/kengaku-r44/R44RoutedQuality/lane
ENVELOPE end 20:37:29 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 20:39:59 cwd=/fast/scratch/hyaku/kengaku-r44/R44RoutedQuality/lane
ENVELOPE end 20:40:00 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 20:42:43 cwd=/fast/scratch/hyaku/kengaku-r44/R44RoutedQuality/lane
ENVELOPE end 20:42:45 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

(Note the round-43 envelope's digest is a *content* digest, not round 42's names-only listing — the reason row 32
is worded "names-only listing would pass a content rewrite unseen" in `F42NoHarm` §3. No PATH-dir write happened
in any of the three runs.)

Scratch: `/fast/scratch/hyaku/kengaku-r44/R44RoutedQuality` (clone, pristine export via `git archive HEAD`, draft
ledger) — deleted at the end of this seat with `plans/scratch_guard.py safe-rm`.

## 7. Limits, and what is *not* claimed

- These are **drafts**. The lane's `corpus/QUALITY.md`, `SCORECARD.md`, `corpus/lessons/round-42.md` and
  `corpus/routed-findings.jsonl` are untouched; the L1 integrates. The red→green measurements come from my
  `--shared` clone (edited) against `git archive HEAD` of the same clone (pristine).
- The replacement checks are literal/range-keyed on the drafted wording (the lane's own closed-row convention,
  e.g. `R42-R3-41`). They are positive matches, so appended quotes of the old text cannot break them; they will
  still need re-pointing if the L1 rewords the edits.
- `R42-R3-18/19`: if the L1 instead lands the two drafts under `plans/`, both checks accept that leg **only if the
  landed tools honour `--lane`** (measured: as drafted, they exit 1 / 2 on it).
- I did not re-run the round-42 counters or the landing measurement. `measure-baseline-v1.txt`, `measure-final.txt`,
  `measure-tip3.txt` and the C1 receipts are read from the lane's committed `.ufo/` history; the counter line pins
  (`plans/round42_c1_verify.py:525,657`) were read, not executed.
- `F42RevQuality`'s own probe of the `fx-pipe*` fixtures and `F42CritScorecard`'s counter runs were not repeated;
  the two claims I rely on there (`PREDICATE C2 pass` at `:679`, `PREDICATE C2 fail` ×6) are re-read from the
  receipt, not re-executed.
- No `bc`/round-44 C1/C2 instrument was touched or run by this seat; nothing outside my report subdir and scratch
  was written.

VERDICT: quality-scorecard-defects-fixed-6-of-6
