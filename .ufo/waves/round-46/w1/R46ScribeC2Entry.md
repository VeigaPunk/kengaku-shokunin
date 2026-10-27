# R46ScribeC2Entry — repaired `password-recovery` entry (C2 wave-1 draft)

Seat: scribe, leaf. Round 46 / hyaku run 9, wave 1. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
base = tip `fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f` (stage-1 freeze; contains the round-45 closure tip
`64ba8385ea10af1b78d367dcb242b92d97062af7` in its history). No lane file, `git`/`jj` state or commit touched.
Draft delivered for the L1 to integrate.

## Behavior delivered

`corpus/knowledge/tb2-password-recovery-grader.md`, five surfaces repaired, nothing else changed
(`51 insertions(+), 11 deletions(-)` across one file):

1. **`## Predictor` block** — translates CRLF *and* lone CR to `\n` before `.strip().split("\n")`, matching
   `read_text()`'s universal-newline read. Lint-clean under `round45_c2_verify.PRED_LINT_TOKENS` (no `{`, `}`,
   `import`, `open`, `os.`, `sys.`, `states`, `__`, `print(`, …); only `str.replace/strip/split` and `in`.
2. **`## Predictor` prose** — now states the four conversions the code performs instead of asserting a read the
   old block did not implement.
3. **`source:` range cells** — S151 `1-43`, S152 `1-20`, S153 `1-29`, S154 `1-33`, S155 `1-68`. S150 `1-9`,
   S156 `1-41` and the S149 `:9-10` / `:14-18` ranges were already exact and are byte-identical.
4. **`empty-file` Mechanism row** — decisive line moved from `test_outputs.py:16` to `:18` with the `:18` quote;
   `:16` (`len(guesses) > 0`) cannot fire because `"".split("\n")` is `['']`.
5. **`## Errata (round 46)`** — new section (38 lines at the end of the entry) naming all five corrected
   statements with old text and evidence: the `lone-CR` predictor gap, the prose overclaim (base-revision
   `:150`, `:193-194`), `S152`/`S153`/`S154` wrong anchors superseded by S161/S162/S163, the `empty-file`
   Mechanism row, and the range cells.

Findings 3's CRLF sentence was *extended*, not deleted (`read_text()` universal-newline mode, "which turns a lone
`\r` into `\n` as well") — see Findings §1 below for why.

## Gates (all measured, envelope lines pasted)

### Line counts re-measured (requirement 2 — "re-count yourself")

`cd corpus/evidence/round45/tb2-password-recovery && for f in …; do wc -l; python3 -c "…splitlines()…"; done`

| capture | `wc -l` | `splitlines()` | range used |
|---|---|---|---|
| instruction.md | 9 | 9 | `1-9` (unchanged) |
| setup.sh | 42 | **43** | `1-43` |
| Dockerfile | 20 | **20** | `1-20` |
| test.sh | 29 | **29** | `1-29` |
| README.md | 32 | **33** | `1-33` |
| solve.sh | 68 | **68** | `1-68` |
| task.toml | 41 | 41 | `1-41` (unchanged) |
| test_outputs.py | 18 | 18 | `:9-10`, `:14-18` (unchanged) |

`wc -l` under-counts `setup.sh` (42) and `README.md` (32) because those files carry no trailing newline; leg C
counts `splitlines()`, which is the line count the requester and the claim state. This is a real trap for the next
auditor — see Findings §3.

### Clone and base assertion

```
mkdir -p $S; git clone -q --shared <lane> $S/lane
git -C $S/lane rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r46/R46ScribeC2Entry/lane
git -C $S/lane rev-parse HEAD              -> fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f
git -C $S/lane status --porcelain | wc -l  -> 0
```

### After — round-46 C2 counter (`receipts/c2-r46.txt`)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind …/R46ScribeC2Entry/env46 … --bind …/env46/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 …/lane/plans/round46_c2_verify.py --lane …/lane --work …/w46
ENVELOPE start 02:04:35 cwd=/home/vgpnk/Projects/shokunin
PINS total=3 mismatched=0
A anchorline live=8 repaired=0 base_rows=149 base_missing=0 base_changed=0 DEFECT
B predictor states=16 grader_pass=10 grader_fail=6 disagree=0 ok
C entry source_ranges=9 source_ranges_bad=0 errata_marks=5/5 ok
D selftest exit=0 ok
checks=4 defects=1
PREDICATE C2 fail
ENVELOPE end 02:04:39 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

**Leg B ok, leg C ok, leg D ok.** Leg A is `live=8` and is **not this item's surface**: the eight live rows are
S108 and S149–S155 (the base receipt names them), repaired by the S157–S165 superseding rows other wave-1 seats
write in `corpus/SOURCES.md`. My item edits the knowledge entry only; `base_missing=0 base_changed=0` confirms I
left the registry untouched. `PREDICATE C2 fail` here is therefore leg A alone, not a C2-entry defect —
`checks=4 defects=1` with the only defect named on the A line.

### No-harm — frozen round-45 C2 counter (`receipts/c2-r45.txt`)

```
ENVELOPE start 02:04:41 cwd=/home/vgpnk/Projects/shokunin
V1 ok listed=9 bad=0 extra=0      (gate: P1–P10 ok, P10 probe_rerun=byte-equal, defects=0)
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=8 bad=0
V4 ok cases=16 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=9 tags=9 bad=0
V8 ok order_exit=0 result=PASS
V9 ok case_rows=16/16 bad=0
V10 ok mechanism_rows=16/16 bad=0
V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0
checks=11 defects=0
PREDICATE C2 pass
ENVELOPE end 02:04:52 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

`checks=11 defects=0` — no V leg turned red. Both envelope lines report the same PATH-dir content digest
(`ff187bb5c98aa6b5`) and no exit 4; neither measurement is `INVALID`.

### Before — control on an untouched second clone (`receipts/control-before.txt`)

Same counter, base entry, `git clone -q --shared` → `…/ctl` (`rev-parse --show-toplevel` = `…/ctl`):

```
PINS total=3 mismatched=0
A anchorline live=8 repaired=0 base_rows=149 base_missing=0 base_changed=0 DEFECT
B predictor states=16 grader_pass=10 grader_fail=6 disagree=6 DEFECT
C entry source_ranges=9 source_ranges_bad=4 errata_marks=0/5 DEFECT
D selftest exit=0 ok
checks=4 defects=3
PREDICATE C2 fail
ENVELOPE end 02:03:11 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

This reproduces the frozen before-values exactly (`B disagree=6`, `C … source_ranges_bad=4 errata_marks=0/5`) and
shows the two legs I was judged on are sensitive to the exact repair, not to a counter that always prints `ok`.

### Independent reproduction of the 6 disagreements

In-memory emulation (`io.TextIOWrapper(newline=None).read()` for the grader read, the two predictor bodies) over the
counter's 16 literal states, run outside the sandbox:

```
old disagree 6 new disagree 0
'C\rD' True/False/True   'D\rC' True/False/True   'D\n\rC' True/False/True
'C\r\r\nD' True/False/True   'D\r\rC' True/False/True   'D\r\nC\rD' True/False/True
'C\r' and '\rC' True/True/True (strip already removed the lone CR); 2 CRLF controls and 4 non-newline separators agree
```

The six names (grader / old / new) match the bwrap grader's count of 6 exactly.

## Touched surfaces

- Written (allowed): `.ufo/waves/round-46/w1/R46ScribeC2Entry.md`,
  `.ufo/waves/round-46/w1/R46ScribeC2Entry/{tb2-password-recovery-grader.md,entry.diff,c2-r46.txt,c2-r45.txt,control-before.txt}`.
- Scratch: `$S = /fast/scratch/hyaku/kengaku-r46/R46ScribeC2Entry` (two `--shared` clones `lane/`, `ctl/`, work
  dirs `w46/`, `w45/`, `wctl/`, envelope dirs `env46/`, `env45/`, `envctl/`), deleted:
  `python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r46 R46ScribeC2Entry "$S"` →
  `DELETE path=… bytes=1241050005 size=1.2GiB rc=0`; round root and `.ROUND-ROOT-SENTINEL` still present.
- Not touched: the lane tree (zero writes), `corpus/SOURCES.md`, any `plans/` file, `SCORECARD.md`, `LOG.md`,
  `README.md`, `PROVINCE.md`, the jj/Git state; no commit, push or fetch anywhere. Source repo not opened.
- Nothing installed (no `uv tool`, `npx`, `pacman`); no package manager called.

## Out of scope (not done here, owned elsewhere)

- SOURCES rows S157–S165, S154 `teaches` (closure D6), S156 `code`→`docs`, S108/S149/S150/S151/S155 anchor cells →
  the SOURCES drafting seats. Their absence is what keeps leg A at `live=8`.
- `plans/anchor_line_check.py`, `plans/round46_c2_verify.py`, `plans/round45_c2_verify.py`, `plans/pkg_gate.py`,
  `plans/pkg-spec-r45.json`, the claims file: frozen, read only, PINS `mismatched=0`.
- C1 and C3 surfaces (fence, sealed modules, `polyglot-c-py` package).
- `LOG.md` correction entry for closure D1; lesson `## Gate` quotes for closure D2.

## Findings

1. **Closure §2 groups `:150` with `:194` as an overclaim; measured, `:150` was true.** `:150` said "`read_text()`
   runs universal-newline mode (`:14`)" — a statement about the captured grader, and correct: the capture's `:14`
   is `read_text().strip().split("\n")`, and my emulation of `newline=None` read reproduces the bwrap grader's
   verdicts on all 16 states, lone-CR ones included. Only the block, and the `:193-194` prose describing the block,
   were false. The errata records it that way (item 2) and `:150` now names lone `\r` explicitly, rather than
   deleting a true sentence to match the closure's wording. If the L1 prefers the closure's framing, item 2 is the
   single place to edit.
2. **Leg C cannot see a short range.** Its check is `int(b) > nl or int(a) > int(b)`, so S152's `1-16` for a
   20-line Dockerfile passed at base and was repaired only because this item names the counts. Round 46's leg C
   would stay green on any `1-16`-style understatement. A stage-2 note could ask for `b == nl` or at least an
   "understates" counter; I did not propose a counter edit (frozen file).
3. **`wc -l` vs line count is a live trap.** `setup.sh` (43 lines, `wc -l` 42) and `README.md` (33, `wc -l` 32) have
   no trailing newline. Any later seat that "re-counts" with `wc -l` will read `1-33` as off-by-one and may
   "repair" a correct cell. The errata states the measurement recipe (`bytes.decode(); .splitlines()`) for that
   reason.
4. **The frozen round-45 counter cannot see the `empty-file` Mechanism row defect.** `DECISIVE["empty-file"]` allows
   both `(16, 18)`, so the base row citing `:16` — the assert that cannot fire — scored `V10 ok` in the round-45
   receipt and scores `V10 ok` after my change to `:18`. The repair is invisible to that counter, which is exactly
   the kind of false detail a non-author read has to catch; it is named in errata item 4 so the correction is
   auditable without a counter.
5. **The before-control is the strongest evidence the repair is load-bearing:** identical counter, identical input
   states, `disagree=6` → `disagree=0`, `source_ranges_bad=4` → `0`, `errata_marks=0/5` → `5/5`, with leg D and
   leg A unchanged in both runs.

## Artifacts

| artifact | sha256 |
|---|---|
| `.ufo/waves/round-46/w1/R46ScribeC2Entry/tb2-password-recovery-grader.md` (final draft, 251 lines) | `037653dc5db497d4a396bb3b5e56d5bdda2396f417cb0fd8f284e1c83c37d9e4` |
| `.ufo/waves/round-46/w1/R46ScribeC2Entry/entry.diff` (unified diff vs base entry, 103 lines) | `87018de468b5198e30d3c99da9146a731b99e9c1ae9d6cafa753a07a724defb6` |
| `.ufo/waves/round-46/w1/R46ScribeC2Entry/c2-r46.txt` | `ab028adc1a7fdd0adf3748ff7265ab4686b858cd74bdc6afd738949a5717bf6e` |
| `.ufo/waves/round-46/w1/R46ScribeC2Entry/c2-r45.txt` | `c625f0841386763dddc8b63e4014b92189d454d67e3a4c4d470758fbc23f9b59` |
| `.ufo/waves/round-46/w1/R46ScribeC2Entry/control-before.txt` | `f2d0bfdcf14bc62feada45e338d2af3d10c15671ce877c99c04dcee1b1bead95` |

The draft is the byte-identical file copied into the clone for both counter runs; the diff is
`git -C $S/lane diff -U3 -- corpus/knowledge/tb2-password-recovery-grader.md`.

VERDICT: c2-entry-legB-ok-legC-ok-r45-counter-pass
