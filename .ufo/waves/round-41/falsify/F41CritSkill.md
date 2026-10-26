# F41CritSkill — SKILL.md `## Scheduling-constraint TB2 grader — round 41` rows, and the four new registry rows

Seat: F41CritSkill (critic, wave 2 falsify). Scope: verify every decision-table row and the
"what a green means" paragraph against the receipt/capture lines they cite; run every command in
`SKILL.md:595-598` and the `Round-41 registry addendum` in a clean clone (C1 under the host-guard
bwrap envelope); report where each verdict map matches and where it does not. Leaf seat: no
subagents, no background jobs. Nothing frozen edited; nothing written outside this report dir and
`/fast/scratch/hyaku/kengaku-r41/F41CritSkill/`.

## 1. Setup and tip

Lane HEAD is **d7c7789**, not the dispatch's `3d0058f`. The extra commit is wave-2 dispatch only:

```
$ git diff --stat 3d0058f..d7c7789
 .ufo/waves/round-41/falsify-dispatch.json | 578 +++++
 .ufo/waves/round-41/falsify-spec.json     | 339 +++
 2 files changed, 917 insertions(+)
$ git diff --name-only 3d0058f..d7c7789 | grep -E '^(plans|corpus)/'   # (no output)
```

No `plans/` or `corpus/` byte changed, so the frozen surfaces are identical to `3d0058f`. All
measurements below are on a clean shared clone of `d7c7789`:

```
$ S=/fast/scratch/hyaku/kengaku-r41/F41CritSkill
$ git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
$ git -C "$S/lane" rev-parse --show-toplevel   ->  /fast/scratch/hyaku/kengaku-r41/F41CritSkill/lane
$ git -C "$S/lane" rev-parse --short HEAD      ->  d7c7789
```

Frozen digests hold (`claims/frozen-digests.txt`):

```
$ sha256sum -c .ufo/waves/round-41/claims/frozen-digests.txt
plans/round-41-claims.md: OK        plans/round41_c1_verify.py: OK   plans/round41_c2_verify.py: OK
plans/constraints_probe.py: OK      plans/pkg-spec-r41.json: OK      corpus/evidence/round41/constraints-dry-cases-freeze.txt: OK
corpus/evidence/round41/tb2-constraints-scheduling/SHA256SUMS: OK   plans/tip_receipts.py: OK
plans/sources_adopt.py: OK          plans/pkg_gate.py: OK           plans/order_check.py: OK
   (11/11 OK; $? = 0)
$ cd corpus/evidence/round41/tb2-constraints-scheduling && sha256sum -c SHA256SUMS
Dockerfile: OK … test_outputs.py: OK   (10/10 OK)
```

Every C1 / probe / counter run used the envelope
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`,
`TMPDIR` = my scratch dir, `--work` under it.

## 2. Decision table — 11/11 rows match the receipt/capture lines they cite

The frozen receipt is byte-reproducible, so citations can be checked against a fresh run as well as
the committed file. `diff` of the fresh probe stdout against the committed receipt is empty:

```
$ bwrap … python3 plans/constraints_probe.py --lane . --work "$S/work" > probe.out   # 16.6 s, exit 0
$ diff probe.out corpus/evidence/round41/constraints-probe.txt && echo RECEIPT-BYTE-EQUAL
RECEIPT-BYTE-EQUAL
probe.out:31  cases=25 observed_pass=6 observed_fail=19 mismatches=2
probe.out:32  regrade cases=25 differ=0
```

Scripted comparison of every case the table cites (`CASE <id> … tests=` parsed from the receipt),
21 checks, 0 disagreements — `cited-case checks=21 bad=0`:

| row | row's claim | cite | receipt line → `tests=` | holds |
|---|---|---|---|---|
| 1 | decoded-text integrity; CRLF rewrite passes, append/delete fail | `test_outputs.py:88-96` | 31 `PPP`, 21 `FPP`, 22 `FPP` | yes |
| 2 | structure block; first-VEVENT decoy passes, mirror `PFF` | `:97-103`, `:106-118` | 14 `PPP`, 28 `PFF` | yes |
| 3 | line-anchored ATTENDEE; extra attendee free, folded line fails | `:120-123` | 29 `PPP`, 25 `FPP` | yes |
| 4 | flat `DTSTART`/`DTEND`, 1 h, 15-19 Jan weekday | `:125-129` | 15 `FPP`, 20 `FFF`, 27 `FPP` (+16/17 `FPP`) | yes |
| 5 | tests 2-3 take the file's first `DTSTART` | `:135`, `:151` | 14 `PPP`, 28 `PFF` | yes |
| 6 | `_hard_ok` then `_overlap`; `seconds-30` `PFF` | `:58-83`, `:46-55`, `:137-143` | 18 `PFF`, 12 `PFF` | verdict yes; **explanation wrong — F1** |
| 7 | earliest scan raises on a valid earlier slot; two `PFP` | `:158-167` | 13 `PFP`, 23 `PFP` | yes |
| 8 | `9 <= hour < 12` unconditional; tie-break/buffer unwitnessed | `:188`, `:180-186`, `:190-208` | 11 `PPF` | yes (ground truth re-derived, §2.1) |
| 9 | calendars-as-events unread; RFC 5545 forms fail | — | 24 `PPP`, 25 `FPP`, 26 `FFF`, 30 `FPP` | yes |
| 10 | calendars themselves unread | — | 9 `PPP` | yes |
| 11 | oracle `PPP`, nop `FFF` with `FileNotFoundError` in each | — | 8 `PPP`, 7 `FFF` | yes |

Code citations spot-checked against the captured grader (line numbers exact):
`:40-43` `_dt`; `:46-55` `_overlap` zip of two `findall`s; `:58-83` `_hard_ok`; `:61` Alice end,
`:65-68` Bob Tue/Thu; `:88-96` integrity; `:97-103` structure; `:106-118` meeting block;
`:120-123` ATTENDEE; `:125-129` duration/window; `:135` and `:151` file-first `DTSTART`;
`:137-143` model+overlap call; `:158-167` earliest scan; `:180-186` tie-break; `:188` morning
assert; `:190-208` Carol buffer. Capture-metadata citations also exact: `instruction.md:1,10,12,15,17-18,21,23,25,27`;
`test.sh:18-22,25-29`; `task.toml:30,35`; `Dockerfile:3,14`.

### 2.1 Ground truth re-derived independently (row 8)

Replaying the captured `_hard_ok`/`_overlap` over the three captured calendars, every minute
Mon 09:00 → Fri 18:00:

```
valid starts: ['Wed 2024-01-17 11:00', 'Thu 2024-01-18 11:00']
```

So "on the pinned calendars the only valid starts are already morning" is true, and neither the
Monday tie-break nor the Carol buffer can be witnessed — the row's claim holds.

### 2.2 Tag paragraph re-derived from the receipt (11/11 counts, 7 singletons)

`CASE … violates=` parsed from the receipt, case count / observed passes per tag:

| tag | cases/pass | SKILL says |
|---|---|---|
| `window` | 1/0 | 1, 0 |
| `output-file` | 1/0 | 1, 0 |
| `meeting-title` | 1/0 | 1, 0 |
| `attendees` | 1/0 | 1, 0 |
| `one-hour` | 1/0 | 1, 0 |
| `hard-constraints` | 5/1 | 5, 1 (`decoy-first-vevent`) |
| `no-conflict` | 5/0 | 5, 0 |
| `inputs-readonly` | 3/1 | 3, 1 (`input-crlf-rewrite`) |
| `version-prodid` | 1/0 | 1, 0 |
| `utc-format` | 1/0 | 1, 0 |
| `earliest` | 10/1 | 10, 1 (`decoy-first-vevent`) |

`singletons= 7 tags= 11` — "seven of the eleven tags rest on a single witness" is exact. The
counter's own V7 re-derives the same eleven labels on the landed tree:

```
$ bwrap … python3 plans/round41_c2_verify.py --lane . --work "$S/w2"   # 12.1 s, exit 0
V7 ok rows=11 tags=11 bad=0
checks=8 defects=0
PREDICATE C2 pass
```

The entry's `## Requirement map` (line 146) is one row per tag in that shape, and its prose counts
(`earliest` 10, `hard-constraints` 5, `no-conflict` 5, seven singletons, `inputs-readonly` 3) equal
the receipt's, so the SKILL paragraph and the entry cannot drift silently.

### 2.3 "What a green means" paragraph — 7/7 clauses supported

| clause | cite | evidence |
|---|---|---|
| any calendar was read | receipt:9 | `literal-correct-slot` `PPP` with a hand-typed file |
| graded slot belongs to the meeting VEVENT | receipt:14 | `decoy-first-vevent` `PPP`, meeting at Fri 15:00 |
| inputs byte-identical to repo copies | receipt:31 | `input-crlf-rewrite` `PPP` (bytes differ, text equal) |
| invalid slot caught when no valid slot precedes | receipt:13,23 | `bob-start-0900-wed`, `wed-1059-overlaps-alice` `PFP` |
| a 90-minute meeting caught by any test but the first | receipt:15 | `duration-90min` `FPP` |
| tie-break / Carol-buffer branches work | no case | §2.1: only two valid starts, both morning |
| output is valid iCalendar | receipt:25,26,30 | `FPP`, `FFF`, `FPP` |

The paragraph's "on states the probe built, not states an agent built" is also accurate: the probe
stages `/app` itself, and `nop` fails all three tests with `error=FileNotFoundError` (receipt:7).

## 3. Registry rows `SKILL.md:595-598` — 4/4 command sets match their verdict maps

### 3.1 `round41-c1-mutants` (595) — exit 0 map reproduced verbatim

```
$ bwrap … python3 plans/round41_c1_verify.py --lane . --work "$S/w1"   # 5.4 s, exit 0
PINS total=2 mismatched=0
BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=13/13 sources=10/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 pass
```

Every token in the row's exit-0 cell is present and equal (`PINS total=2 mismatched=0`,
`fixtures=48`, `killed=23 …`, `13/13 sources=10/10`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`).

Other documented behaviours, all measured:

| row claim | command | observed |
|---|---|---|
| dev selectors print `PREDICATE C1 n/a` | `… --only T01,S02 --work "$S/w1b"` | `MUTANTS total=2 killed=2 …`, `PREDICATE C1 n/a (non-default battery or mutant subset)`, exit 0; `--work` dir created |
| `--work` refused inside the lane | `… --work "$S/lane/tmpw"` | `SETUP --work must not lie inside the lane …`, exit 2 |
| `--work` created if absent | first run above (dir absent) | `$S/w1` exists, empty after run (scratch removed) |
| `--jobs N …, default 8` | `grep -n add_argument plans/round41_c1_verify.py` | `511: ap.add_argument("--jobs", type=int, default=8)` |
| `len(MUTANTS)!=23` / per-tool floor → exit 1 | code `:640-642`; control files | `floors_ok` requires `len(MUTANTS)==TOTAL`, `killed==TOTAL` and `per_tool==[13,13]/[10,10]` |

Controls in the row's self-test cell, reproduced (each in a clone, under the envelope):

```
control-c1-nothing  (plans/battery41 emptied, no flag)
  BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0
  MUTANTS total=23 killed=0 survived=23 invalid=0 null_detected=0
  PREDICATE C1 fail                                  exit=1        [matches row]
control-c1-no-mutants (MUTANTS=[] inserted at :234, witness modules as plans/battery41)
  BATTERY fixtures=22 wrong=0 tampered=0 sidechannel=0
  MUTANTS total=0 killed=0 survived=0 invalid=0 null_detected=0
  PREDICATE C1 fail                                  exit=1        [matches row]
control-c1-tool-edited (one comment line added to plans/tip_receipts.py)
  PINS total=2 mismatched=1 first=plans/tip_receipts.py
  MUTANTS total=23 killed=10 survived=0 invalid=13 null_detected=0
  PINS-AFTER mismatched=1                            exit=1        [matches row's 13 invalid receipts mutants]
control-c1-hostile (--battery-dir …/claims/hostile)
  SIDECHANNEL hostile/h_host_writes.py tokens=/home/
  BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=1
  PREDICATE C1 n/a (non-default battery or mutant subset)          exit=1   [matches row]
control-c1-witness-as-battery (--battery-dir …/claims/witness)
  all FIXTURE w-* lines ok; PREDICATE C1 n/a                        exit=0   [see F4]
```

### 3.2 `round41-c2` (596) — green map, red path, and freeze control all match

```
$ bwrap … python3 plans/round41_c2_verify.py --lane . --work "$S/w2"
V1 ok … V8 ok order_exit=0 result=PASS
checks=8 defects=0
PREDICATE C2 pass          exit=0
```

* exit 1 path (live): deleting the entry in a clone gives `V2 DEFECT gate_exit=1`,
  `V4 DEFECT`, `V6 DEFECT census_exit=1`, `V7 DEFECT`, `checks=8 defects=4`, `PREDICATE C2 fail`, exit 1.
  A raising check is a defect (`:300` `ok, note = False, f"error {type(e).__name__}: {e}"`).
* exit 2 (argparse only): `--bogus` → `error: unrecognized arguments: --bogus`, exit 2.
* `--work DIR … created if absent`: `$S/w2b` absent before, created, run exit 0.
* freeze control reproduced **byte-for-byte on the V-lines** at the freeze commit 8ef8b4f with the
  frozen counter (`cf1632b5`):

```
V2 DEFECT … V3 DEFECT rows=2 bad=['S122:row','S123:row'] V4 DEFECT … V8 DEFECT order_exit=2 result=not-PASS
checks=8 defects=5
PREDICATE C2 fail          exit=1
$ diff <V-lines> claims/control-c2-nothing.txt  ->  CONTROL-MATCHES
```

Note for re-runners (F3): at `f774a87` (the receipt commit) the same run is `defects=4`, `V8 ok`,
because the receipt exists there; the recorded control is a property of `8ef8b4f`, where the
receipt is absent.

### 3.3 `constraints-probe` (597) — data line, dry table, stage check, setup

```
$ python3 plans/constraints_probe.py --lane . --dry > dry.out ; cmp dry.out corpus/evidence/round41/constraints-dry-cases-freeze.txt
DRY-BYTE-EQUAL ; dry.out:37 cases=25 predicted_pass=6 predicted_fail=19 ; exit 0
$ bwrap … python3 plans/constraints_probe.py --lane . --work "$S/work"        # full run
cases=25 observed_pass=6 observed_fail=19 mismatches=2                        exit 0   (mismatches never in $?)
$ bwrap … python3 plans/constraints_probe.py --lane . --stage-check --work "$S/w3b"
stagecheck cases=25 failed=0                                                  exit 0   (row maps 1 only when a stage fails)
$ bwrap … python3 plans/constraints_probe.py --lane "$S/empty" --work "$S/w3c"
SETUP capture alice_calendar.ics missing or not at its pinned digest          exit 2
```

`--dry` runs with no sandbox and `--work` is created when absent. Exit 1 was **not exercised**: it
needs a non-zero recipe stage, and every frozen recipe exits 0 (`stagecheck … failed=0`), so the
only frozen red can be a setup refusal (exit 2).

### 3.4 `round-close-check` (598) — both legs, the red round, the selftest, setup

```
$ python3 plans/round_close.py --lane . --round 41 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
ROUND-CLOSE receipts=1
ROUND-CLOSE order receipt=corpus/evidence/round41/constraints-probe.txt exit=0 verdict=PASS
ROUND-CLOSE census exit=0 warnings=15 verdict=PASS
ROUND-CLOSE RESULT PASS exit=0                                   exit=0
$ … --round 38   -> order receipt=corpus/evidence/round38/build-pmars-probe.txt exit=1 verdict=FAIL
                    ROUND-CLOSE RESULT FAIL exit=1               exit=1
$ … --round 39   -> RESULT PASS exit=0 ;   … --round 40 -> RESULT PASS exit=0
$ … --selftest --census … --work "$S/w5c"
SELFTEST checks=5 ok=5 failed=0  (A 0, B 1, C 1, D 2, E 2)        exit=0
$ … --lane .                 -> round_close.py: error: --round is required unless --selftest   exit=2
$ … --lane corpus --round 41 -> ROUND-CLOSE ERROR --lane must be the work-tree top: …          exit=2
$ … --lane . --round 41      -> ROUND-CLOSE ERROR no census script (scripts/sources-census.sh) exit=2
```

`warnings` do not fail the leg (15 W-lines, verdict PASS), matching the addendum. `find_census`
starts at `plans/round_close.py:138`; the ERROR mapping is at `:201-207` and `:210-213` (row cites
`:200-213`).

## 4. Round-41 registry addendum — every command matches, one coverage gap

| addendum claim | measurement |
|---|---|
| C1 23 mutants, 21 `direct` + 2 `indirect` | `ADVERTISED direct=21 indirect=2 none=0` (§3.1) |
| predicate binds total and per-tool floor | code `:640-642`; no-mutants control `MUTANTS total=0 … exit=1` |
| freeze was the do-nothing control (`fixtures=0`, `survived=23`) | reproduced (§3.1, `PREDICATE C1 fail`, exit 1) |
| run with `--lane` on a disposable clone, inside the envelope | every C1 run above |
| C2 = round-40 V1-V7 plus V8 (order gate) | `V1 … V8` present; `V8 ok order_exit=0 result=PASS` |
| C2 gate leg re-runs the probe | `gate: P10 ok probe_rerun=byte-equal bytes=5775`; C2 wall 12.1 s (probe alone 16.6 s) |
| needs the entry and **the two index rows** | **gap — F2**: three rows landed (S122, S123, S124) |
| probe row of the round-37 shape, mismatches are data | §3.3 (exit 0 with `mismatches=2`) |
| round-close census needs `--census PATH` outside the fleet; W-codes do not fail | §3.4 (exit 2 without it; `warnings=15 … PASS`) |
| tip-receipts derived mapping | below |

tip-receipts addendum paragraph, reproduced on the clone (`~53.5 s`, exit 0):

```
$ python3 plans/tip_receipts.py --lane . --list
receipt corpus/evidence/round39/git-leak-probe.txt kind=byte script=plans/git_leak_probe.py origin=derived …
receipt corpus/evidence/round40/db-wal-probe.txt   kind=byte script=plans/db_wal_probe.py   origin=derived …
receipt corpus/evidence/round41/constraints-probe.txt kind=byte script=plans/constraints_probe.py origin=derived …
$ bwrap … python3 plans/tip_receipts.py --lane . --work "$S/wtr"
receipt corpus/evidence/round41/constraints-probe.txt equal bytes=5775 exit=0 doc=SKILL.md:596+SKILL.md:667
control receipt=…/round35/tb2-grader-probe.txt flip=byte 1699 0x27->0x26 verdict=differ
note compared=7 declared_bounded=1 no_command=19
receipts=27 byte_equal=7 differ=0 skipped=20
```

Three derived receipts, `compared=7 declared_bounded=1 no_command=19`, `byte_equal=7 differ=0`,
`equal bytes=5775`, "≈54 s": all four numbers equal the addendum. The ambiguity claim also holds —
fixture repo with `plans/foo_probe.py` beside `plans/foo-probe.py`:

```
receipt corpus/evidence/round99/bar-probe.txt kind=byte script=plans/bar_probe.py origin=derived provenance=command=plans/bar_probe.py:4,receipt=undocumented
receipt corpus/evidence/round99/foo-probe.txt skip reason=no-committed-re-run-command
```

## 5. Findings

### F1 (defect, decision table row 6) — the `seconds-30` explanation names the wrong mechanism

Row 6 says: "`seconds-30` is `PFF` — test 1 accepts a `:30` start, test 2 fails because the end
crosses into Carol's 12:00-12:30 lunch". The verdict `PFF` is right (receipt:18), but test 2 fails
through `_overlap`, not through `_hard_ok`'s lunch window; that window is skipped for a `:30` start
because `lunch0/lunch1` are built from `t0` and inherit its seconds (`test_outputs.py:72-73`):

```
seconds-30: start=Wed 11:00:30 end=Wed 12:00:30 _hard_ok=True
lunch0 = 2024-01-17 12:00:30 lunch1 = 2024-01-17 12:30:30
test2 overlap alice,bob,carol = [False, True, True]
  overlap bob   20240117T120000Z 20240117T130000Z   ("Lunch Meeting")
  overlap carol 20240117T120000Z 20240117T130000Z   ("Team 1:1s", not a lunch block)
alice-end-14:00:30: start=Wed 13:00:30 end=Wed 14:00:30 _hard_ok=True
```

Two consequences a reviewer is taught by this row incorrectly: (a) a `:30` start does not trip the
model's own 12:00-12:30 lunch rule — only the pinned calendars catch it; (b) the Alice-end check
(`t1.hour < 14 or (t1.hour == 14 and t1.minute <= 0)`, `:61`) admits an end at 14:00:30, so
"absolutely no meetings after 2 PM" is second-blind too. Impact: a probe case with a second-offset
start and no 12:00 calendar event would pass test 2; the frozen case set has no such case, so no
receipt line changes. Smallest safe correction (row 6, prose only; nothing frozen): replace the
parenthetical with "test 2 fails only through `_overlap` against Bob's and Carol's 12:00-13:00
events; `_hard_ok`'s lunch window and `(14,0)` end check inherit the start's seconds, so a `:30`
start slips both rules".

### F2 (coverage gap, Round-41 addendum + row 596) — S124 is outside the counter's guarded rows

The addendum says `round41-c2` "needs the entry … and the two index rows as well as the receipt".
The round landed **three** rows; the addendum and the spec bind two:

```
$ grep -n '^| S12' corpus/SOURCES.md
137:| S122 | … constraints-scheduling task grader …   138:| S123 | … instruction.md …
139:| S124 | … TB2.1 pull request #245 "Bind constraints-scheduling checks to the requested event" …
$ python3 -c "import json;print(json.load(open('plans/pkg-spec-r41.json'))['rows'])"  -> ['S122', 'S123']
```

S124 is not decorative: `grep -c S124 corpus/knowledge/tb2-constraints-scheduling-grader.md` = 9
citations (source-note at `:366`, "published (S124 …)" at `:34`), and `plans/round-41-claims.md:117`
says "S124 to be opened in wave 1". Measured consequence — deleting the S124 row in a clone leaves
C2 fully green:

```
$ (delete the `| S124 |` line) ; python3 plans/round41_c2_verify.py --lane . --work "$S/w2e"
gate: P6 ok rows=2 bad=0 … P8 ok index_rows=48 knowledge_files=48 bad=0
V2 ok … V3 ok rows=2 bad=0 … V7 ok rows=11 tags=11 bad=0
checks=8 defects=0
PREDICATE C2 pass          exit=0
```

So the row's "two index rows" is accurate about what V3 guards but does not disclose that the
package's third source row is unguarded; a future edit could drop or corrupt S124 with no red.
Smallest safe correction: state in row 596 / the addendum that S124 is outside V3's guarded
population (the spec is frozen at `8e96421d…`, so do not edit it now; bind it in the round-42 spec,
or have `round41-c2`'s V3 assert the landed `S12x` set).

### F3 (clarification) — the round-41 C2 freeze control is a property of `8ef8b4f`, not of `f774a87`

Running the frozen counter at `f774a87` (first recorded probe run) gives `checks=8 defects=4`
(`V8 ok order_exit=0`), because the receipt exists there; at `8ef8b4f` (freeze, receipt absent) it
gives the recorded `defects=5` with `V8 DEFECT order_exit=2`. Re-runners should name the freeze
commit, not the receipt commit, or they will read a one-defect difference as a control failure.
No verdict-map change.

### F4 (disclosed, but worth restating) — `PREDICATE C1 pass` is reachable with a 22-fixture witness battery

`control-c1-witness-as-battery.txt` records `BATTERY fixtures=22 … MUTANTS total=23 killed=23 …
PREDICATE C1 pass exit=0`; my `--battery-dir …/witness` run instead prints
`PREDICATE C1 n/a (non-default battery or mutant subset)` (exit 0). Both are correct: the recorded
control swapped `plans/battery41` for the witness modules, so the default-battery path printed
`pass`. The row discloses "pass reachable by witnessed work", and its exit-0 map writes
`BATTERY fixtures=<n>` (n open), so this is not a false claim — but the only guard between a 22-
fixture witness battery and a printed `pass` is a human reading `fixtures=<n>`. If the L1 wants the
48-fixture wave-1 battery to be the sole path to `pass`, that needs a code pin (e.g. `fixtures==48`
or a battery digest), not a prose note.

## 6. What I did not verify

* No Terminal-Bench harness, task image or network run: the probe reads captures only, as designed;
  `uvx -p 3.13`/pytest and `/logs/verifier/reward.txt` are read, not executed (`test.sh:18-22,25-29`).
* `round41-c1-mutants` exit 2 paths other than `--work`-inside-lane (missing `bwrap`, duplicate
  fixture id, a `build()` contract breach) were not exercised; the row's exit-1/0 paths and all five
  controls were.
* `constraints-probe` exit 1 is unreachable with the frozen recipes (`stagecheck … failed=0`).
* Battery-module admission (does any wave-1 module use the known stub/dead-site/argv/socket/AF_UNIX
  vectors) is the battery reviewers' assignment, not re-run here; I only reproduced the counter's
  sidechannel token scan (`SIDECHANNEL` tuple at `plans/round41_c1_verify.py:109`, hit path `:472-475`).
* TB2.1 PR #245's content was checked by web read only: it exists in
  `harbor-framework/terminal-bench-2-1`, describes the decoy/event-binding flaw the entry cites, and
  is **closed unmerged**; "published" in row 5 is therefore true, "merged" would not be.

Every write I made is under `.ufo/waves/round-41/falsify/F41CritSkill/` (17 run receipts) or
`/fast/scratch/hyaku/kengaku-r41/F41CritSkill/` (deleted at exit). No lane file was touched; the
frozen control modules `crit_git_shim.py` / `crit_ledger_selfread.py` were neither used nor moved.

VERDICT: skill-rows-verified-11/11-registry-4/4
