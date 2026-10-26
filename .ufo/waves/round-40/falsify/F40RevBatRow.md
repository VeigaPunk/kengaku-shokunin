# F40RevBatRow — non-author honesty review of `plans/battery40/a_row.py` (A06, A08, A09)

Round 40 wave 2 (FALSIFY), 2026-10-26. Lane tip measured: `ec1005a2a28bc5cfdde7723374368ed4cc956eed`.
Target: `plans/battery40/a_row.py` (74 lines, sha256 `7b0b6e9cc48ff65fa9bb3ad37f8536b9bad3feed70e2fe32a3f280a1e6be13bc`),
against `plans/round40_c1_verify.py` (sha256 `4d47800e3551a0c7a39217987f436ffad9d69663d5f0efc840717edfcbd4642c`).
Both files byte-identical between the shared lane and my scratch clone (sha256 compared before any run).

## Method

- Scratch clone `/fast/scratch/hyaku/kengaku-r40/F40RevBatRow/lane` at `ec1005a2`; `git rev-parse --show-toplevel`
  verified equal to the clone before any write; no commit ever made; scratch removed at the end.
- Every line of `a_row.py` read (74 lines: docstring, 3 `build_*` functions, `FIXTURES` list; sole import `re`,
  a_row.py:10).
- Counter run under the HOST-SAFETY sandbox:
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc
  --unshare-pid --die-with-parent python3 <lane>/plans/round40_c1_verify.py --lane $S/lane --battery-dir $S/battery
  --only A06,A08,A09 --work $S/w` with `$S/battery` holding only `a_row.py` (copied from the clone).
- Fixture trees rebuilt **outside the counter** by importing the module's own `build` functions with a replica of the
  counter's `Ctx` (same ENV incl. `HOME=/nonexistent`, same `git clone -q --shared`; harness contract at
  round40_c1_verify.py:31-32), then diffed against the lane working tree.

## Counter run (verbatim; receipt `run-a06-a08-a09.txt`)

```
PINS total=3 mismatched=0
FIXTURE a_row-indent4-wrong tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE a_row-token-in-teaches tool=anchor expect=reject declared=token-outside-anchor observed_rc=1 observed=token-outside-anchor ok
FIXTURE a_row-12-cells tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
MUTANT A06 anchor rc-mirror killed by=a_row-indent4-wrong -- plans/anchor_digest_check.py:31 'Row set — the census shape (... `^ {0,3}\\|\\s*(S\\d{3,})
MUTANT A08 anchor rc-silence killed by=a_row-token-in-teaches -- plans/anchor_digest_check.py:81 'a token outside the anchor cell is `token-outside-anchor`
MUTANT A09 anchor rc-silence killed by=a_row-12-cells -- plans/anchor_digest_check.py:34-35 'A row that matches the census regex but does not have
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```
(counter exit=0; MUTANT label lines truncated at 90 chars by the counter itself)

## Per-fixture verdicts

### `a_row-indent4-wrong` (a_row.py:24-32, declared a_row.py:66-68) — **HONEST**

- Build replaces the S111 row (`corpus/SOURCES.md:126` in the clone) with a 4-space-indented copy of itself whose
  cell-6 digest is swapped to the S108 row's token (a_row.py:27-30).
- The substituted digest is a **real committed capture digest**: S108's row token `345c3bd0…8f72` equals
  `sha256(git cat-file blob HEAD:corpus/evidence/round36/tb2-regex-log/test_outputs.py)` (receipt
  `fixture-build-inspect.txt`, `token == blob digest : True`). So the mutant's rejection is `digest-wrong-capture`
  on another row's real digest, exactly the fixture docstring's "carrying another row's real digest" (a_row.py:24).
- Tree diff vs lane: exactly 1 line changed (`126c126`; the `>` line begins with 4 spaces) — receipt
  `fixture-tree-diff.txt`. No other file differs; the fixture's copy of `plans/anchor_digest_check.py` is
  byte-identical to the lane's.
- Behaviour: reference rc=0 — the indented line is not a row under the census shape `^ {0,3}` (anchor:31 "Row set —
  the census shape … so this check and the census agree on what a row is"); A06 mutant (`{0,3}`→`{0,4}`, one byte)
  rc=1 on the identical tree. rc-mirror kill satisfied; declared defects `[]` == observed.
- Attribution is airtight: same tree, single-byte regex change, rc flips 0→1, so the flip can only come from the
  indented line being counted as a row.

### `a_row-token-in-teaches` (a_row.py:34-41, declared a_row.py:69-71) — **HONEST**

- Build moves S111's `sha256 <hex>` claim from cell 6 to cell 7 via `split("|")` parts (a_row.py:36-39). Cell 6 is
  the anchor cell: anchor:32-33 "the **anchor is cell 6** (index 5)", `ANCHOR_CELL = 5` (anchor:161); the module's
  `parts[6]` on the raw line is the same cell.
- The moved token is S111's **own real committed digest**: `526aee3d…6b37` equals
  `sha256(HEAD:corpus/evidence/round37/tb2-git-webserver/test_outputs.py)` (receipt, `True`). The advertised
  sentence anchor:81 — "a token outside the anchor cell is `token-outside-anchor` — always a defect, whatever its
  value" — is therefore demonstrated with a perfectly valid value: the defect is purely positional.
- Reference rc=1 with observed classes exactly `{token-outside-anchor}` (emission anchor:490-492,
  `detail=sha256-claim-in-cell-7-of-11`); A08 mutant (`if cell_idx != ANCHOR_CELL:` → `if False:`) rc=0 — with the
  token gone from the anchor cell the row raises nothing (anchor:102 "Rows that carry no anchor token raise
  nothing"). rc-silence kill satisfied.
- Tree diff: exactly 1 line changed; after the edit the row's only `sha256` token sits in cell 7 (receipt).

### `a_row-12-cells` (a_row.py:43-47, declared a_row.py:72-74) — **HONEST**

- Build appends a 12th cell `extra` to the S111 row (a_row.py:45-46); the line still matches the census regex,
  cells 11→12 (receipt: `cells 11 -> 12`, `row_match=True`).
- Reference rc=1 with observed classes exactly `{row-malformed}` — anchor:34-35 "A row that matches the census
  regex but does not have 11 cells is a `row-malformed` defect", emitted at anchor:477-479 under
  `len(r["cells"]) != NCELLS` (`NCELLS = 11`, anchor:162).
- A09 mutant (`!=` → `<`) rc=0: 12 cells pass the count check, the cell-6 token still resolves to S111's own
  capture, so the extra cell is silently tolerated. rc-silence kill satisfied.

## Attack-vector checklist (the wave-1 set named in the assignment)

| Vector | Present? | Evidence |
|---|---|---|
| Reading the tool or own program text at run time | NO | only `re` imported (a_row.py:10); no reference to any `plans/*.py` path, no `__file__`/argv introspection; builds read only the clone's `corpus/SOURCES.md` (a_row.py:18) |
| Writing outside d (HOME, PATH dirs, other modules' fixture dirs) | NO | writes are `ctx.clone(d/"lane")` (a_row.py:17) and the clone's SOURCES.md (a_row.py:30); `Ctx.ENV` pins `HOME=/nonexistent` (round40_c1_verify.py:238); each fixture clones into its own counter-owned `dest/fNNN` |
| Relative argv tokens or symlinks pointing out of d | NO | argv is `["--lane", "<absolute path inside d>"]` (a_row.py:31), validated by `path_ok` (round40_c1_verify.py:326-329); `find -type l` over the built tree: none (receipt) |
| `.lock` / `.git/index` names the fingerprint skips | NO | no `*.lock` file anywhere in the built tree (receipt); `.git/index` exists only as `git clone`'s own checkout state, and the tool runs with default `--evidence-ref head` → `ls-tree HEAD`, never reading the index (anchor:187-189, anchor:194-195) |
| Phase detection | NO | the module has no run-time component: `build()` returns argv and nothing module-owned executes during tool runs |
| Bare-string `build()` return | NO | returns a 2-element list (a_row.py:31); the counter rejects non-list argv (round40_c1_verify.py contract, validated at build) |
| Wave-1 A2 git shim / PATH games | NO | module never touches PATH or git config; the counter's Ctx pins `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null` (round40_c1_verify.py:239) |
| Cross-module fixture forgery | NO | no reads of other modules' dirs; `--battery-dir` held only `a_row.py` |
| SIDECHANNEL token scan | clean | counter printed `sidechannel=0` |

## Docstring-accuracy checks (module docstring vs pinned tool)

- "the tool parses rows from the working tree and binds digests against committed evidence, so the edit needs no
  commit" (a_row.py:5-7) — verified: `parse_rows` reads `(lane / "corpus/SOURCES.md").read_text(...)` (anchor:398),
  binding uses `ls-tree HEAD` + `cat-file HEAD:` via `evidence_paths`/`spec_for` with default ref `head`
  (anchor:187-195). The module never commits (no `ctx.git`/`ctx.init` call anywhere in a_row.py), and the tool
  requires `lane/.git` to exist (anchor:579-580) — the clone provides it.
- Exit-code contract: anchor:27 "Exit: 0 no defects · 1 defects found · 2 usage error" matches the counter's
  `EXPECT_RC` accept=0/reject=1 mapping used by all three fixtures.
- The three `adv` sentences exist at the quoted lines: anchor:31 (A06), anchor:81 (A08), anchor:34-35 (A09).

## Residual notes (non-defects)

- Coverage is narrow by design: all three fixtures edit the same row (S111) and reuse S108's digest; each
  demonstrates exactly one advertised row-shape behaviour, and the `defects` declarations are enforced against the
  reference's actual output (`wrong=0`), so nothing is overclaimed.
- `a_row-indent4-wrong` *replaces* the S111 row rather than adding an indented copy beside it, so the reference's
  accept is "no row → no claim" (presence limit, anchor:102). The kill contrast still isolates the advertised rule
  (identical tree, one-byte change), so the demonstration stands; noted for completeness.
- The module's `TOKEN` regex (a_row.py:12) requires 64 lowercase hex — narrower than the tool's token regex
  (anchor:37-39, any-case hex run with optional ellipsis). Irrelevant here (both rows carry full lowercase
  digests); a future row-shape change would fail the build loudly (`ValueError` in `_row_at` a_row.py:15, or
  `AttributeError` on a missing token), not silently pass.
- My scratch lane briefly carried `plans/battery40/__pycache__/` created by my own inspect-script import at
  14:30:20 (after the counter run); removed before the receipt re-run. The shared lane at
  /home/vgpnk/Projects/shokunin/kengaku-shokunin was never written.

## Receipts

- `.ufo/waves/round-40/falsify/F40RevBatRow/run-a06-a08-a09.txt` — verbatim counter output (sandboxed run above).
- `.ufo/waves/round-40/falsify/F40RevBatRow/fixture-build-inspect.txt` — replica build of all three fixtures
  (changed-line and cell analysis) + row-token vs committed-blob digest verification.
- `.ufo/waves/round-40/falsify/F40RevBatRow/fixture-tree-diff.txt` — `diff -rq` f000/lane vs lane, symlink and
  `.lock` scans, per-fixture `corpus/SOURCES.md` diffs.

Tooling record: nothing installed or upgraded (bwrap/python3/git already present; pacman untouched).

VERDICT: battery-a_row-honest-3/3
