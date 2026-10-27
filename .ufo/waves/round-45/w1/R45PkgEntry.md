# R45PkgEntry — C2 knowledge entry draft (wave 1, round 45)

Seat: `R45PkgEntry` (scribe). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Lane tip read at
`05b02e2` ("round-45: first recorded probe run — password-recovery 16 cases, mismatches=0, regrade differ=0");
freeze commit of the claims is `b4fcd35141acda5fa0980a34dd29ab880b702ee6`. Two post-freeze commits
(`52d7486`, `05b02e2`) and one uncommitted worktree edit to the C2 counter were observed during the seat; both
are recorded below as provenance/conflicts, not acted on. I wrote nothing in the lane outside
`.ufo/waves/round-45/w1/R45PkgEntry/`, ran no git/jj mutation anywhere, and installed no tools.

## Deliverable

| Item | Path | State |
|---|---|---|
| Knowledge entry draft | `.ufo/waves/round-45/w1/R45PkgEntry/tb2-password-recovery-grader.md` | 24,160 bytes, sha256 `66810cf900830138c19dbcb9aebff9fcc458cb520c8f3155217d8c8e6af6fd72` |
| Copy target for the L1 | `corpus/knowledge/tb2-password-recovery-grader.md` | **not written by this seat** (lane is read-only for me) |

The draft carries the five required sections (`## Case table`, `## Mechanism`, `## Requirement map`,
`## Located quotes`, `## Predictor`) plus the provenance the package gate parses (`source:` lines for all eight
rows, `verified-at: 2026-10-26`, `recheck:`, `## Negative space` with a falsifier, `## Findings`,
`## What the probe does not show`). Row ids S149-S156 appear in body text outside the `source:` lines.

## What was verified, with the command and its output

Every counter/gate run below was executed inside the frozen envelope
(`.ufo/waves/round-45/claims/envelope.sh "$S/env" …`); the `ENVELOPE` lines are pasted with each result and the
`~/.local/bin` content digest was `c263b11afb1cccf6` before and after in every run (`unchanged`).

The staged fixture for all of it was a `git clone -q --shared` of the lane at `$S/lane` (rev-parse
`--show-toplevel` checked), with the draft copied to `corpus/knowledge/` and the lane worktree's uncommitted
`corpus/SOURCES.md` copied in for the V3/V6 legs. Receipts are in this seat's subdir.

### Counter legs (frozen `plans/round45_c2_verify.py`, sections in situ against the draft)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind …/R45PkgEntry/env …/R45PkgEntry/env --bind …/R45PkgEntry/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 …/run_sections.py
ENVELOPE start 23:31:28 cwd=/home/vgpnk/Projects/shokunin
V1 ok listed=9 bad=0 extra=0
V3 DEFECT rows=8 bad=['S149:row', 'S150:row', 'S151:row', 'S152:row', 'S153:row', 'S154:row', 'S155:row', 'S156:row']
V4 ok cases=16 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V7 ok rows=9 tags=9 bad=0
V9 DEFECT case_rows=16/16 bad=['PROVINCE.md names the task and the entry on no line', 'README ## Frontier does not name the task']
V10 ok mechanism_rows=16/16 bad=0
V11 DEFECT raised FileExistsError: [Errno 17] File exists: '…/v11work/v11/app'
ENVELOPE end 23:31:30 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```
(`sections-run.txt`.) The V3 line is a staging artifact: the clone is at HEAD, whose `corpus/SOURCES.md` lacks
the S149-S156 rows that exist only in the worktree; re-run with the worktree file:

```
ENVELOPE start 23:33:58 cwd=/home/vgpnk/Projects/shokunin
V3 ok rows=8 bad=0
V6 ok census_exit=0
ENVELOPE end 23:34:01 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```
(`v36-run.txt`.) The V11 `FileExistsError` is the counter's own `v11()` calling `mkdir` on a work dir left by my
first run, not a content signal; with a fresh work dir:

```
ENVELOPE start 23:33:19 cwd=/home/vgpnk/Projects/shokunin
V11 (True, 'states=48 grader_pass=18 grader_fail=30 disagree=0')
ENVELOPE end 23:33:21 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```
(`v11-run.txt`.) So, against the draft: **V4, V5, V7, V10, V11 ok**. At 23:31 V9's only defects were the two
integration lines (PROVINCE, README §Frontier); those landed in the worktree minutes later, and the final draft
bytes were re-measured at 23:38 against a symlink root built from the current lane (every top-level lane entry
and `corpus/*` symlinked, `corpus/knowledge/` holding all 51 lane files plus my draft as the 52nd):

```
ENVELOPE start 23:37:28 cwd=…/R45PkgEntry/root2   (gate, no clean-tree/rerun)
P1 ok pinned=2 mismatched=0
P2 DEFECT receipt_sha256=587c8b345f8b0341e90640f83b78eafa7c5d5c996cac5e2d0a52a1131a8df23e
P3 ok rows=20 distinct_quotes=20 distinct_lines=20 out_of_word_range=0
P4 ok checked=20 bad=0 first=0
P5 DEFECT manifest_entries=9 bad=5 first=S149: capture test_outputs.py is not pinned in the manifest
P6 ok rows=8 bad=0 first=0
P7 ok source_lines=8 bad=0 first=0
P8 ok index_rows=52 knowledge_files=52 bad=0 first=0
defects=2
ENVELOPE end 23:37:30 exit=1 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

and the counter legs on the same root (V11 on the same bytes at 23:33, above):

```
V1 ok listed=9 bad=0 extra=0
V3 ok rows=8 bad=0
V4 ok cases=16 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=9 tags=9 bad=0
V9 ok case_rows=16/16 bad=0
V10 ok mechanism_rows=16/16 bad=0
```
(V1/V3/V4/V5/V7/V9/V10 from the 23:38 run; V6 from 23:37:40.) **Every counter leg the entry controls is green
on the final bytes**, `V9` included — the earlier PROVINCE/README defect is gone because the L1 landed those
lines. `V8` (order) run from the lane root as the predicate invokes it:

```
ORDER claims=plans/round-45-claims.md round=45 freeze=b4fcd35141acda5fa0980a34dd29ab880b702ee6
ORDER receipt=corpus/evidence/round45/password-recovery-probe.txt receipt_commit=05b02e2b7894a9c83219685f2374905e11c1beda claims_dir=.ufo/waves/round-45/claims/
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
```
(`v8-run.txt`.) `V2` is red only through the gate clauses below.

### Package gate (frozen `plans/pkg_gate.py` + `plans/pkg-spec-r45.json`, draft installed)

```
ENVELOPE start 23:31:55 cwd=…/R45PkgEntry/lane
P1 ok pinned=2 mismatched=0
P2 DEFECT receipt_sha256=587c8b345f8b0341e90640f83b78eafa7c5d5c996cac5e2d0a52a1131a8df23e
P3 ok rows=20 distinct_quotes=20 distinct_lines=20 out_of_word_range=0
P4 ok checked=20 bad=0 first=0
P5 DEFECT manifest_entries=9 bad=5 first=S149: capture test_outputs.py is not pinned in the manifest
P6 ok rows=8 bad=0 first=0
P7 ok source_lines=8 bad=0 first=0
P8 DEFECT index_rows=51 knowledge_files=52 bad=3 first=index rows for knowledge/tb2-password-recovery-grader.md=0
defects=3
ENVELOPE end 23:31:57 exit=1 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```
(`gate-run.txt`; `--require-clean-tree`/`--rerun` omitted, so P9/P10 were not exercised in this run — see Not
done.) The entry-side clauses are clean: **P3 (20 quotes, 20 distinct quotes, 20 distinct lines, 0 out of 3-25
words), P4 (20/20 verbatim), P6 (SOURCES rows 8/8), P7 (8 source lines, verified-at, recheck, negative space)**.
At 23:31 the three remaining defects were **not entry defects**: P2 and P5 are frozen-instrument conflicts, and
P8 was the README index row, which the L1 landed by 23:37 (`P8 ok index_rows=52 knowledge_files=52` in the
current-state run above). P2 and P5 are spelled out under Conflicts.

### Quotes re-opened line by line

`open-lines.txt` (45 lines) lists, for every cited line in `## Mechanism` and `## Located quotes`, the capture
name, the 1-based line, the recomputed sha256 of the capture and the verbatim test: 16 mechanism rows and 20
located-quote rows, `verbatim=True` on all 36, 22 distinct `capture:line` locations. Capture digests recomputed
at draft time and equal to `SHA256SUMS` and to the counter's `CAPTURES`:

| Capture | sha256 |
|---|---|
| `tests/test_outputs.py` | `2dc14fc180734b6fbb0ee00f27c4f866071247b57a2217f579465ff8ed3bfc9e` |
| `instruction.md` | `bc4f501148805bbccdb94a5c5b745f1ce9564f04ef0fe36bc37c3ca20b7810a5` |
| `solution/solve.sh` | `c5f9fc70b6bae40befdd0088dde1a3bc6e909852c9fbb36a617c627b7b8d804f` |
| `environment/setup.sh` | `9fdde5d9cd74ae0d633bdd59e7249cc6d7385d27a98b1e2dbbeb11b05a6f2af8` |
| `environment/Dockerfile` | `6fabcb9e1fcb7155bf8cfe106c17f2dfa3344103e97960dab580c2444b6c9fe0` |
| `tests/test.sh` | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` |
| `README.md` | `122bf15ef4a6ede562f21453f9f1c452fc10a3048bac7d46a013adbac6a13add` |
| `task.toml` | `cfd0362d201b957796f9bf1c02cc75646250cb2bd107ec88c768bfcfd091b24b` |

No capture bytes were written or re-fetched; the eight above are the nine-file freeze minus `gitignore` (which
the spec's 8 rows reject).

## The draft's content, section by section

**Case table (16 rows, receipt order, frozen predictions).** `nop F- fail`, `oracle-solve-sh PP pass`,
`constant PP pass`, `constant-crlf PP pass`, `constant-joined PF fail`, `dir-state PF fail`, `empty-file PF
fail`, `wrong-23 PF fail`, `prefix-decoy PF fail`, `sub-first PF fail`, `sub-last PF fail`, `lower23 PF fail`,
`decoys-1000 PP pass`, `password-eq PF fail`, `crlf-line PP pass`, `under-varsea F- fail`. The receipt now
exists (`corpus/evidence/round45/password-recovery-probe.txt`, sha256 `587c8b34…`) and records
`cases=16 observed_pass=5 observed_fail=11 mismatches=0` and `regrade cases=16 differ=0`, i.e. every observed
verdict equals the frozen prediction, so the third column is simultaneously `predicted=` and `observed=`.

**Mechanism (16 rows).** One row per case citing a `DECISIVE` line with a verbatim quote: `:10` for `nop`,
`solve.sh:11` for the oracle, `:18` for the six constant-comparison cases, `:14` for the four
read/strip/split cases, `:16` for the dead guard, `instruction.md:4` for `password-eq`, `:9` for
`under-varsea`. Two mechanism notes are stated as findings, not assumptions: `dir-state` dies inside
`read_text()` (the receipt's `error=IsADirectoryError`), and `empty-file`'s `len > 0` guard (`:16`) cannot fire
because `''.strip().split("\n") == ['']`.

**Requirement map (9 rows, labels derived by the counter's own rule).** `forensic` → `partly` (violated by
`constant`, `constant-crlf`, `decoys-1000`, `crlf-line`, all observed `pass`); `recover`, `len23`, `prefix`,
`suffix`, `charset`, `write-file`, `one-per-line`, `one-guess` → `enforced` (every violating case observed
`fail`). Each row cites only cases whose frozen `violates=` set carries the tag; `V7 ok rows=9 tags=9 bad=0`.

**Located quotes (20 rows).** 3-25 words each, spread over all eight captures and 20 distinct lines
(`tests/test_outputs.py:10,14,16,18`; `instruction.md:1,4,5,6,7,9`; `solution/solve.sh:63`;
`environment/setup.sh:25,36`; `tests/test.sh:22,26`; `environment/Dockerfile:16`; `README.md:31`;
`task.toml:5,29,34`). Three of them carry the leak: the answer constant in the grader (`:18`), in the setup
script (`setup.sh:25`) and in the authors' README (`:31`).

**Predictor (one ```python block, 170 bytes, lint-clean).**

```python
def predict(text):
    if text is None:
        return False
    guesses = text.replace("\r\n", "\n").strip().split("\n")
    return "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses
```

`V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0` — the counter's own bubblewrap run of the captured
grader's two functions against `random.Random(45)` states, with the counter's `PRED_LINT_TOKENS` scan clean
(`{`, `}`, `import`, `open`, `hash`, `states`, `__`, `print(`, … all absent) and 170 bytes against the 4000-byte
ceiling. A pure-python restatement of the same 48 states agreed independently (`disagree=0`, `grader_pass=18`).

**Findings (10, each tied to receipt cases).** 1 do-nothing 0/2 (`nop`); 2 copying the published answer passes
(`constant`, `constant-crlf`, `crlf-line`); 3 1001 guesses pass (`decoys-1000`); 4 whole-line, byte-exact
membership (`constant-joined`, `lower23`, `password-eq`); 5 format conformance buys nothing (`wrong-23`,
`prefix-decoy`); 6 truncation fails both ways (`sub-first`, `sub-last`) and the oracle hedges with
combinatorics (`solve.sh:55-66`); 7 a directory dies on `IsADirectoryError` (`dir-state`); 8 the emptiness guard
is dead (`empty-file`); 9 one directory too deep scores 0/2 (`under-varsea`); 10 the oracle appends rather than
selects (`solve.sh:63`).

## Conflicts for the canonical judge (verbatim; I changed nothing)

1. **The committed C2 counter cannot parse its own mechanism rows.** At HEAD `05b02e2`, `MECH_ROW`'s capture
   class is `[A-Za-z0-9_.-]`, which matches no `/`:
   `MECH_ROW = re.compile(r"^\|\s*`([a-z0-9_-]+)`\s*\|\s*`([A-Za-z0-9_.-]+):(\d+)`\s*\|\s*“(.+?)”\s*\|\s*$")`
   (`plans/round45_c2_verify.py:102` at HEAD). Seven of the eight captures are nested (`tests/test_outputs.py`,
   `environment/setup.sh`, `solution/solve.sh`, …) and 15 of the 16 `DECISIVE` maps point into them, so **a
   correct entry parses only 1 of 16 mechanism rows at the committed tip** and `V10` fails on `ids_equal=False`.
   Measured deterministically from HEAD's own source (`narrow-head.txt`):
   `HEAD-regex matches 1/16 mechanism rows`, with 15 `NOMATCH` lines listing `tests/test_outputs.py:*` and
   `solution/solve.sh:11`. My first in-situ V10 read (23:26) saw exactly this: `V10 mech rows parsed=1/17`.
   The current **worktree** carries an uncommitted two-line change to that frozen counter —
   `[A-Za-z0-9_.-]` → `[A-Za-z0-9_./-]`, and `"under-varsea": {"tests/test_outputs.py": (9,)}` →
   `(9, 10)` — file mtime `2026-10-26 23:29:43.273334828 -0300`, `git status` ` M plans/round45_c2_verify.py`
   (`counter-dirty.txt`). With that edit in place V10 is green (`mechanism_rows=16/16 bad=0`); with the committed
   version it cannot be. The claims say "Nothing frozen may change … not the counters", and the counter is not
   self-pinned in the spec's `frozen_instruments` (only `pkg_gate.py` and `password_recovery_probe.py`), so this
   edit is invisible to `P1`. **Judge decision needed:** admit the widening, or accept a red V10.
2. **The spec's `capture` names are flat, the frozen captures are nested → `P5` is red for any entry.**
   `P5 DEFECT manifest_entries=9 bad=5 first=S149: capture test_outputs.py is not pinned in the manifest`; the
   five mismatches are `test_outputs.py` vs `tests/test_outputs.py`, `setup.sh` vs `environment/setup.sh`,
   `Dockerfile` vs `environment/Dockerfile`, `test.sh` vs `tests/test.sh`, `solve.sh` vs `solution/solve.sh`
   (spec `rows[*].capture` vs `SHA256SUMS`). `pkg_gate.py` `c_captures` compares the spec's flat name to the
   manifest, so no edit to the entry can clear this.
3. **The spec has `"receipt_sha256": null`** while the receipt now exists at
   `587c8b345f8b0341e90640f83b78eafa7c5d5c996cac5e2d0a52a1131a8df23e` → `P2 DEFECT`. Together with (2) this
   makes `V2` red regardless of the entry, and `V2` is one of the eleven checks of the C2 predicate.
4. **The integration lines were landed during the seat, and they now pass.** At 23:31 `V9` failed on PROVINCE
   (`names the task and the entry on no line`) and README (`## Frontier does not name the task`), and `P8` failed
   on the missing README index row (51 index rows vs 52 knowledge files). By 23:37 the worktree carried
   `M PROVINCE.md`, `M corpus/README.md`, `M corpus/SOURCES.md`, and the same checks read `V9 ok case_rows=16/16`
   and `P8 ok index_rows=52 knowledge_files=52`. Nothing here is left for the entry.
5. **Post-freeze commits changed frozen-adjacent inputs (disclosed, not mine).** `git log --oneline
   b4fcd35..HEAD` → `05b02e2`, `52d7486`; the diff removes the spec's `S157` (`gitignore` → `.gitignore`) row,
   changes the claims' row list `S149–S157` → `S149–S156`, and re-pins `SPEC_SHA256` to
   `3eb696b4…` (the current spec digest). The dry table is still at its freeze digest
   `46036abe542aa8e50a59080bda82c154ae4735de25ac64416906de263f71aabb`, and `plans/password_recovery_probe.py`
   still hashes `f87a9eeb…`, matching `PROBE_SHA256`. The claims file now hashes
   `1e63c4ba57db9f79e142dfc60a4a5ab97c2cd22e34fec0f4338e1776393cba38` (freeze commit version:
   `79ede48a…`).
6. **`P10`'s byte-equality cannot hold for an envelope-recorded receipt.** The frozen receipt
   (`corpus/evidence/round45/password-recovery-probe.txt`, 26 lines) is the probe's stdout wrapped in the three
   mandated `ENVELOPE` lines — the command line, `ENVELOPE start …`, `ENVELOPE end …` — while `c_rerun` demands
   `r.stdout == want` against the whole file. Measured: a fresh `plans/password_recovery_probe.py --lane .
   --work …` run under the envelope produced 26 lines whose non-`ENVELOPE` lines are **`cmp`-identical** to the
   receipt's 23 (`probe-vs-receipt.txt`), and the gate prints
   `P10 DEFECT fresh probe output is not byte-equal to the receipt`. The host-safety rule (Q32: paste the
   ENVELOPE lines with every result) and this clause are in direct conflict; if the receipt stays enveloped, no
   package can pass `P10`, hence not `V2`.
7. **A PATH-directory content change was observed between my runs, not caused by me.** The envelope's
   `~/.local/bin` content digest was `c263b11afb1cccf6` at 23:29-23:34 and `e396f23e40a69201` at 23:37-23:38
   (before = after inside every run, so each measurement is valid). Some other process rewrote the directory in
   between; I installed nothing.

## A second entry candidate exists in the lane, and it is not this seat's

During the seat, another writer produced `corpus/knowledge/tb2-password-recovery-grader.md` in the lane itself
(untracked, 16,088 bytes, sha256 `657a16ca6eeef5538329fb56c761d150ba69dec77c15e933161ad41853ad5e8d`, mtime
`2026-10-26 23:29:43`). My draft is a separate file with different content (24,160 bytes, sha256 `66810cf9…`) and
cites only nested capture names. I checked the lane copy read-only; it is materially defective
(`lane-entry-check.txt`):

- counter `V4 ok cases=16`, `V7 ok rows=9` — its case table and requirement map are sound;
- `V9 DEFECT … row ids absent outside source lines: ['S149', …, 'S156']` — S149-S156 appear only on its `source:`
  lines, so the body never cites the registry rows;
- `V10 DEFECT mechanism_rows=16/16 bad=['constant-crlf:tests/test_outputs.py:14 quote not on the line',
  'dir-state:…:14 …', 'crlf-line:…:14 …', 'under-varsea:…:10 …']` — four mechanism quotes sit on the wrong
  line (all four of mine at `:14` are on a `guesses = Path(…)` prefix that is byte-verbatim there);
- **10 of its 19 `## Located quotes` rows are unreadable to the gate**: 17 rows cite flat capture names
  (`test_outputs.py`, `test.sh`, `setup.sh`, `solve.sh`, `Dockerfile`) and `capture_dir / test_outputs.py` does not
  exist, so `c_quote_verbatim` reports "unreadable capture" before any line comparison;
- with the flat names remapped to their nested captures, **6 of 19 rows are on the wrong line** —
  `test_outputs.py:8`→`:9`, `test.sh:26`→`:25`, `test.sh:28`→`:26`, `Dockerfile:15`→`:17`, `README.md:44`→`:31`,
  `task.toml:24`→`:22` (`:24` is blank; the quote also occurs on `:25`);
- five of its eight `source:` line ranges end past EOF. Physical line counts measured here:
  `setup.sh 43`, `Dockerfile 20`, `test.sh 29`, `README.md 33`, `solve.sh 68`, `test_outputs.py 18`,
  `instruction.md 9`, `task.toml 41`. My draft's ranges are `1-18`, `1-9`, `1-43`, `1-20`, `1-29`, `1-33`,
  `1-68`, `1-41` — all inside those counts.

Peer `R45Lesson` reported the same six line mismatches independently (message received during the seat); I
confirmed all six and sent the flat-capture finding back. Nothing in the lane file was edited by me: which
candidate lands is the L1's and the judge's decision, and if the lane copy is preferred it needs the nested
renames, the six line fixes, and S149-S156 in body text.

## Not done, and why

- **The entry was not installed in the lane** (`corpus/knowledge/…`): lane `corpus/` is read-only for this seat.
  The integration lines the entry needs are already in the worktree, uncommitted (`M PROVINCE.md`,
  `M corpus/README.md`, `M corpus/SOURCES.md`, and the README index row at `corpus/README.md:78`); V9 and P8 read
  green against them. What remains is copying this draft over `corpus/knowledge/tb2-password-recovery-grader.md`
  (where the *other* candidate sits today), then committing.
- **P9/P10.** P9 (`--require-clean-tree`) was not exercised: the symlink root is not a git worktree, and a clone
  with the draft copied in would flag that copy as untracked — P9 is a landing-time property, not an entry
  property. P10 was measured and fails on the envelope conflict (conflict 6), not on the entry.
- **The frozen probe was re-run once** (23:38, enveloped, `--lane . --work $S/pw`) only to isolate the P10
  difference: its stdout minus the three `ENVELOPE` lines is `cmp`-identical to the receipt (`probe-vs-receipt.txt`).
  The case verdicts themselves are the recorded receipt's, which I cross-checked against the dry table for
  `(id, tests, predicted)` equality (V4 ok) — I claim no new grading run of my own.
- **No claim about `pytest`, the docker image or the setup build.** The draft says so in
  `## What the probe does not show`: host `python3` stands in for `uvx -p 3.13` + `pytest==8.4.1`,
  `tests/test.sh` is read not run, the 4 MB image is not rebuilt, and the entropy of `setup.sh`
  (`/dev/urandom`, timestamps) is not reproduced.
- **`P2`/`P5` cannot be fixed from the entry.** If the judge admits a spec edit, the minimal form is
  `rows[*].capture` → the nested capture path and `receipt_sha256` → `587c8b34…`; if the spec stays frozen, V2
  cannot pass.

## Host safety

- Every counter/gate/probe execution went through
  `.ufo/waves/round-45/claims/envelope.sh "$S/env" <cmd>` with `S=/fast/scratch/hyaku/kengaku-r45/R45PkgEntry`
  (also `export TMPDIR=$S`). Five envelope runs, each printing
  `local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged`: 23:31:28 (sections), 23:31:55
  (gate), 23:33:19 (V11), 23:33:58 (V3/V6), plus the first gate run at 23:29:19 (same digest, superseded).
  No run reported `INVALID`.
- Writes: only `.ufo/waves/round-45/w1/R45PkgEntry/` (this report and its subdir) and `$S`. Nothing in the
  lane's `corpus/`, `plans/`, `README.md`, `PROVINCE.md`, `SCORECARD.md` or Git index; nothing in the fleet root,
  a sibling lane, `~/.local/bin` or any other PATH directory. The lane was read through `git -C
  /home/vgpnk/Projects/shokunin/kengaku-shokunin show/diff/log/status` (read-only) and cloned read-through into
  `$S/lane` (rev-parse verified). The fixture clone received copies of my draft and of the worktree
  `corpus/SOURCES.md`; no `git add`/`commit` was run in any repository.
- No tools installed or upgraded (`/home/vgpnk/.omp/agent/RULES.md` read; nothing needed).
- Scratch removed: `python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r45 R45PkgEntry
  /fast/scratch/hyaku/kengaku-r45/R45PkgEntry` → `DELETE path=… resolved=… bytes=542945487 size=517.8MiB`; the
  round root, its `.ROUND-ROOT-SENTINEL` and the other seats' dirs are untouched.

## Artifacts (all in `.ufo/waves/round-45/w1/R45PkgEntry/`, none over 1 MiB)

| File | Bytes | sha256 |
|---|---|---|
| `tb2-password-recovery-grader.md` | 24,160 | `66810cf900830138c19dbcb9aebff9fcc458cb520c8f3155217d8c8e6af6fd72` |
| `open-lines.txt` | — | `4a128e4df4c32d1e824724046efe1a2464a0ecbac5380aa2f2a6c2decc530665` |
| `gate-run.txt` | 1,141 | `130678665739c1bd429494cb7eb7c1b4708878986abbfc21d722186790c0a621` |
| `sections-run.txt` | 1,102 | `1ce42a867b0349ceedbcdfb6ec13b7722f75becca9305eac66beecce85e7aa51` |
| `v11-run.txt` | — | (envelope + the one V11 line, quoted above) |
| `v36-run.txt` | — | (envelope + V3/V6, quoted above) |
| `narrow-head.txt` | — | (HEAD `MECH_ROW` vs the 16 drafted rows, `1/16`) |
| `counter-dirty.txt` | — | (uncommitted counter diff + mtime) |
| `lane-entry-check.txt` | — | `5c7068b27800320c902e009f8bfcf8e8a663931f77ae043a8825e4259ea5b91d` |
| `probe-vs-receipt.txt` | — | `6f4b146aed8ede60e541d009a5f1bed3f4fb1ae9eb75823af2f15d275bc73f9d` |
| `probe-rerun-raw.txt` | — | `92f77cc99c5f751d6a039c747f620b2b0448a1ca4b739f381d908da969ef87fc` |
| `v8-run.txt` | — | `155479474b9d5adcbe6fb46f9aee1b81df89cc9e21ee8b7b51aa5d2132a45baa` |
| `check_entry.py` | 5,638 | `abb1cc8da215b14ad0f5f78638aba04a9b4211ae7ea8f7e5ef3404d2a7c07f77` |
| `run_sections.py` | 1,168 | `bad5fc9f0e8e83736a41013034a2083d7d7f4172e4c2bae7f6552b1f6d22870f` |
| `run_v11b.py` | 590 | `2b8046cb0c4f7124eed621cc4d5cbe3bd7c3698e6fed6e27b827b079e1a0bf6b` |
| `run_v36.py` | 890 | `a2086769b4a383325bbbb27b1f846ff2cf0d6902c446aa0f27abff6f14ddf0f4` |

The three `run_*.py` drivers take `<lane draft> <clone> <work>` from their own constants; `check_entry.py`
re-derives V7/V9/V10/V11 from the frozen module without writing to the lane.

VERDICT: entry-draft-sections-5-quotes-20
