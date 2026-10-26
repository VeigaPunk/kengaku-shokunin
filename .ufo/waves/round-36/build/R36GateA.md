# R36GateA — C1 gate candidate (`plans/pkg_gate.py`), wave 1

Seat: R36GateA (executor, leaf). Target: kengaku round 36, C1 calibration, wave-1 item.
Frozen inputs read first, in full: `plans/round-36-claims.md` (freeze `3241b86c`, Amendment 1
`acbda2f3`), `plans/round36_c1_verify.py`, `plans/pkg-spec-r35.json`,
`corpus/defects-round35.jsonl`, `plans/round35_hardening.py` H1–H6,
`corpus/lessons/round-35-verifier-spotcheck.md` §5.

## What was built

| | |
|---|---|
| candidate | `.ufo/waves/round-36/build/R36GateA/pkg_gate.py` (L1 copies it to `plans/pkg_gate.py`; I did not touch lane files) |
| sha256 | `cd4206a0022468fbc891af89b081da4ee3b3a4f0c7a56c9dd0cb14345b59c319` |
| lines | 397 (`wc -l`), Python 3 stdlib only, no sockets/urllib/requests, no network |
| subcommands | `package --root DIR [--require-clean-tree] [--rerun] --spec SPEC`; `d4-line --file F --spec SPEC`; `d5-line --file F --capture-dir D --spec SPEC` |
| output | one `P<n> ok\|DEFECT <reason>` per package clause, `D4`/`D5` for line clauses, then `defects=<n>` |
| exit | 0 accept, 1 reject, 2 usage/setup (verified: missing spec / missing file / non-dir root / bad subcommand all exit 2) |
| fixture recognition | none: `grep -nE "P0\|P[1-9] \|fixture\|k36\|socket\|urllib\|requests\|http" pkg_gate.py` returns only the docstring sentence and the URL-matching regex that reads the spec's `raw_base` |

One function per clause, a table-driven `CLAUSES` list; every rule is derived from the spec, never
from a fixture id, path suffix or marker string. Two deliberate contract details:

- `P9` / `P10` print `P9 skipped (--require-clean-tree absent)` / `P10 skipped (--rerun absent)` when
  their flag is off instead of a false `ok`. The frozen battery always passes `--require-clean-tree`,
  so `P9` is always evaluated there; `P10` is evaluated on the real-lane run.
- `P10` honours the dependency the receipt pins on its first line (`biopython=1.85`): if the gate's
  interpreter cannot `import Bio` and `uv` exists, it runs
  `uv run --no-project --with biopython==1.85 python3 <probe> ...` (mirrors round-35 `v5`). The
  receipt digest is pinned by `P2`, so this adds no new trust.

Clause semantics (all spec-driven):

| clause | rule | spec key |
|---|---|---|
| P1 | every frozen instrument's sha256 == pin (a stub probe dies here) | `frozen_instruments` |
| P2 | receipt sha256 == pin | `receipt`, `receipt_sha256` |
| P3 | `## Located quotes`: every row parses, quote 3..25 words, ≥8 distinct quotes at ≥8 distinct `file:a-b` lines, each verbatim on the cited capture lines | `entry`, `capture_dir`, `entry_rules` |
| P4 | `capture_dir/SHA256SUMS` parses, every listed file hashes to it, every row's `capture` is listed at the row's pinned sha256 and the file matches | `capture_dir`, `rows` |
| P5 | one SOURCES row per id, 11 cells, tier A, status mined, `opened` == entry rule, source URL == `raw_base`+`upstream`, `used-by` == entry, anchor cites the row digest, teaches ≥8 words and pairwise distinct | `sources`, `rows`, `entry_rules` |
| P6 | entry head: one `source: <id>` line per row with its pinned URL, then `verified-at:` and a `recheck:` cadence | `entry`, `rows`, `entry_rules` |
| P7 | `## Negative space` non-empty and carries a falsifier statement (lexeme `falsif*` + a condition cue `if/when/differ/change/fail/refut` within 200 chars) | `entry` |
| P8 | exactly one README index row for the entry naming every row id, a coverage bullet, and knowledge files == index rows | `readme`, `knowledge_glob`, `entry` |
| P9 | `git -C ROOT ls-files --others --exclude-standard` empty | flag |
| P10 | probe command reproduces the receipt byte for byte | `probe_cmd`, `receipt` |
| D4 | one labelled line; all spec patterns hit: `R34C2CounterDraft.md:8 ... records ... SELFTEST cases=10 failed=0`, `R34MutC2Harness.md:12 ... SELFTEST green failed`, `counter draft's selftest was green` (both citations directional) | `d4` |
| D5 | one labelled line, `is present` required and `not present` forbidden, the capture cited, the capture's sha256 == its `quarantine-SHA256SUMS` entry, and the spec quote present after tag-strip | `d5` |

Manifest names in `.ufo/waves/round-34/assimilation/captures/quarantine-SHA256SUMS` are lane-relative
paths, so `manifest()` keys by basename; a duplicate basename with two digests returns `None`
(unparsed) rather than picking one.

## Fixture → clause map (measured, not reasoned)

`python3 .ufo/waves/round-36/build/R36GateA/clause_map.py` imports the frozen counter's own fixture
builders and runs the gate on each fixture; every `DEFECT` line it prints is listed:

```
P0 rc=0 fires=none
P1 rc=1 fires=['P3']            # 8 one-word quotes
P2 rc=1 fires=['P3']            # 8 copies of one quote
P3 rc=1 fires=['P3']            # unparsed quote row
P4 rc=1 fires=['P5']            # junk teaches cells
P5 rc=1 fires=['P1']            # stub probe (frozen-instrument digest)
P6 rc=1 fires=['P9']            # untracked leftover file
P7 rc=1 fires=['P1','P3','P5','P9']  # cheapest all-junk package
L1 rc=0 fires=none              # D4 genuine
L2 rc=1 fires=['D4']            # citations swapped
L3 rc=1 fires=['D4']            # harness token removed
L4 rc=0 fires=none              # D5 genuine
L5 rc=1 fires=['D5']            # "is not present"
L6 rc=1 fires=['D5']            # quote-injected capture (manifest digest mismatch)
```

The frozen battery does not exercise P2, P4, P6, P7, P8 or P10; each was isolated with a mutant
below, so no clause is dead code.

## Battery proof (fixture clone, per the fixture rule)

```
D=$(mktemp -d /tmp/k36-XXXX)
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone /corpus /plans /SCORECARD.md \
    /.ufo/waves/round-34/assimilation /.ufo/waves/round-34/build
git -C "$D/lane" checkout -q master        # toplevel-ok: rev-parse --show-toplevel == $D/lane
cp <lane>/plans/{regex_log_probe.py,round36_c1_verify.py,round36_c2_verify.py,pkg-spec-r35.json} "$D/lane/plans/"
cp <lane>/corpus/defects-round35.jsonl "$D/lane/corpus/"; cp -r <lane>/corpus/evidence/round36 "$D/lane/corpus/evidence/"
cp <lane>/.ufo/waves/round-36/build/R36GateA/pkg_gate.py "$D/lane/plans/pkg_gate.py"
git -C "$D/lane" add plans/pkg_gate.py     # index-only: the gate is committed at landing, untracked in wave 1
cd "$D/lane" && python3 plans/round36_c1_verify.py --lane "$D/lane"
```

The clone's gate hashed `cd4206a0…59c319`, identical to the build file. Full output:

```
FIXTURE P0 expect=accept observed=accept ok -- genuine round-35 package
FIXTURE P1 expect=reject observed=reject ok -- 8 one-word quotes
FIXTURE P2 expect=reject observed=reject ok -- 8 copies of one quote
FIXTURE P3 expect=reject observed=reject ok -- an unparsed quote row beside the genuine rows
FIXTURE P4 expect=reject observed=reject ok -- junk teaches cells
FIXTURE P5 expect=reject observed=reject ok -- stub probe printing the receipt
FIXTURE P6 expect=reject observed=reject ok -- untracked leftover file
FIXTURE P7 expect=reject observed=reject ok -- cheapest package: one-word quotes + junk teaches + stub probe + stray file
FIXTURE L1 expect=accept observed=accept ok -- D4 genuine correction line
FIXTURE L2 expect=reject observed=reject ok -- D4 line with the two file:line citations swapped
FIXTURE L3 expect=reject observed=reject ok -- D4 line without the harness token
FIXTURE L4 expect=accept observed=accept ok -- D5 genuine erratum line
FIXTURE L5 expect=reject observed=reject ok -- D5 erratum saying the quote is not present
FIXTURE L6 expect=reject observed=reject ok -- D5 genuine line over an altered (quote-injected) capture
FIXTURES total=14 false_green=0 false_red=0 unevaluated=0
R35-D1 status=open observed=pass agree=NO fixtures=14 false_green=0 false_red=0 unevaluated=0 tip_package_rc=0
R35-D2 status=open observed=pass agree=NO untracked_anywhere=0 line_fixtures_wrong=0/6
R35-D3 status=open observed=fail agree=yes committed_nested_wave_paths=21
R35-D4 status=open observed=fail agree=yes round-36 lesson absent; recount 13 + 23 + 1 = 37 vs stated denominator 38
rows=4 closed=0 observed_pass=2 mismatches=2
PREDICATE C1 fail
C1_RC=1
```

`FIXTURES` line is at target. `PREDICATE C1 fail` is now **only** the ledger state, not the gate:

- `R35-D1` and `R35-D2` observe **pass** while their rows are still `status=open` → `mismatches=2`.
  L1 closes them (`status: closed`, `closed_round: 36`) after the predicate run; the checks
  themselves are green, including the tip re-run in the clean clone (`tip_package_rc=0`,
  `untracked_anywhere=0`, `line_fixtures_wrong=0/6`).
- `R35-D3` is red at 21 committed nested paths under `.ufo/waves/round-34/build/R34ReviewCounterC1Attacks/`
  (`committed_nested_wave_paths=21`) — lane-tree work, outside this gate.
- `R35-D4` is red because `corpus/lessons/round-36.md` does not exist yet; the recount it wants is
  `13 + 23 + 1 = 37` against stated `denominator 38` — lesson work, outside this gate.

## Real-lane run (requested command)

```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-36/build/R36GateA/pkg_gate.py \
  package --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --rerun \
  --spec /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/pkg-spec-r35.json
```

```
P1 ok pinned=3 all-match
P2 ok receipt=match
P3 ok rows=22 distinct_quotes=22 distinct_locations=22
P4 ok manifest_entries=6 all-pinned
P5 ok rows=3 distinct_teaches=3 all-match
P6 ok sources=3 trio+verified-at+recheck
P7 ok chars=977 falsifier=yes
P8 ok knowledge_files=42 index_rows=42 parity
P9 skipped (--require-clean-tree absent)
P10 ok byte-equal (3399B, rc=0, runner=uv)
defects=0
REAL_RC=0
```

**Exit code 0** (as required, `--require-clean-tree` omitted because the lane holds untracked wave
files). The probe re-run inside `P10` used the receipt's own `biopython=1.85` pin under
`uv run --no-project` and reproduced `corpus/evidence/round35/tb2-grader-probe.txt` byte for byte.

Line checks on the real lane (same gate):

```
python3 …/pkg_gate.py d4-line --file SCORECARD.md --spec plans/pkg-spec-r35.json
D4 ok patterns=3/3 directional-ok
defects=0                                   # rc=0

python3 …/pkg_gate.py d5-line --file corpus/lessons/round-34.md \
  --capture-dir .ufo/waves/round-34/assimilation/captures --spec plans/pkg-spec-r35.json
D5 ok label+direction+manifest-pin+quote
defects=0                                   # rc=0
```

## Clause isolation mutants (each clause can fail)

`python3 .ufo/waves/round-36/build/R36GateA/mutants.py` (each mutant is a fresh mktemp git repo built
from the genuine package, run with `--require-clean-tree`):

```
M0-genuine: rc=0 accepted
M1-receipt-tampered: rc=1 P2 DEFECT receipt=9f80b2060ec7!=2359d9067906
M2-capture-byte: rc=1 P4 DEFECT manifest_entries=6 test.sh=changed,S106=digest
M3-source-head-missing: rc=1 P6 DEFECT sources=3 line3!=S107,verified-at,recheck
M4a-falsifier-label-renamed: rc=0 accepted          # label is not a magic string; the sentence still falsifies
M4b-falsifier-removed: rc=1 P7 DEFECT chars=628 falsifier=no
M5-index-row-missing: rc=1 P8 DEFECT knowledge_files=42 index_rows=41 index_rows=0,knowledge_files=42!=41_index_rows
M6-sources-row-duplicated: rc=1 P5 DEFECT rows=3 distinct_teaches=2 S106:count=2
M7-quote-not-verbatim: rc=1 P3 DEFECT not verbatim on test_outputs.py:23-23: assert len(gblock) <= 3001, "gBlock must
M9-rerun-receipt-differs: rc=1 P10 DEFECT receipt differs (probe=3399B receipt=3399B rc=0)
```

`M9` uses a spec copy that re-pins the tampered receipt so `P2` passes and `P10` alone fires; the
probe's 3399 fresh bytes differ from the tampered receipt at equal length, so the comparison is a
byte compare, not a length compare. `M4a` is a deliberate accepted mutant: renaming the
`**Falsifier:**` label while keeping the falsifying sentence does not remove the falsifier, so the
gate must not key on the label — it does not.

## Limits and risks (named, not repaired)

1. **`P10` depends on the host's `uv` cache.** On this host biopython 1.85 resolves from uv's cache
   (no network). On a cold or offline host the clause reports `DEFECT receipt differs ... rc=2`
   (a rejection, never `unevaluated`), because uv cannot build the environment. Round-35's `v5` has
   the same dependency. Run the ledger predicate on this host.
2. **`P9` sees the gate itself.** `plans/pkg_gate.py` must be committed before the clean-clone
   predicate run; an uncommitted gate is an untracked file and `P9` rejects. My fixture clone added
   it index-only (allowed), which is exactly the landing state after L1 commits.
3. **`P8` parity is round-wide.** If C2's knowledge file lands without its README index row (or the
   reverse) during integration, `P8` goes red; that is correct behaviour but means C1 and C2 landings
   must both be committed before the C1 predicate is scored.
4. **`P7` is a statement test, not a proof.** It requires a falsifier lexeme plus a condition cue; a
   syntactically falsifying sentence that does not actually falsify the entry would pass. Wave-2
   mutation should attack this clause with a tautological falsifier ("falsified if the file changes"
   where nothing is pinned).
5. **D4/D5 are line-shaped.** They take one line from `--file`; a multi-line correction split across
   two lines is rejected as `labelled_lines=1` plus missing patterns — directionally safe (reject),
   but a future genuine multi-line line would need a spec change, not a gate change.
6. **Unexercised by the frozen battery:** P2, P4, P6, P7, P8, P10 (isolated only by my mutants) —
   expected, since the frozen battery is fixed and may not be extended.

## Integration notes for L1

- Copy `.ufo/waves/round-36/build/R36GateA/pkg_gate.py` → `plans/pkg_gate.py`, `chmod +x`, commit
  (sha256 `cd4206a0…59c319`, 397 lines). No other lane file was touched by this seat.
- After the gate and the C2 package are committed: run
  `python3 plans/round36_c1_verify.py --lane .` on a clean clone of the landing tip, then set
  `R35-D1`/`R35-D2` to `status: closed`, `closed_round: 36`; `R35-D3`/`R35-D4` close only after the
  nested-path cleanup and the round-36 lesson `## Gate` erratum (`Erratum (round 36): … S130 …
  13 + 23 + 1 = 37 … denominator 38`) land.
- No tool installs: `uv 0.13.0` was already present at `~/.local/bin/uv`; `uv run --with
  biopython==1.85` reused round-35's cached environment. No pacman transaction was attempted.

VERDICT: gateA-false_green-0-false_red-0-unevaluated-0
