# F38MapV7Control — attacking C2 V7's derived-label rule (five map mutants) + the round-37 retro

Seat: mutation-tester, kengaku round 38 wave 2 (FALSIFY), hyaku run 8, 2026-10-26.
Target: `plans/round38_c2_verify.py` V7 — the fix for round-37 closure D2 (a requirement-map label chosen
from one convenient witness). Claim attacked: V7's derived-label rule is able to fail, i.e. it is not a
no-op, and it mechanically reproduces the round-37 `instruction.md:9` disagreement.

## Axes

| axis | probe |
|---|---|
| sensitivity | five map mutants (relabel/citation/duplicate/missing/wrong-line) must each turn V7 DEFECT |
| attributability | in every mutant run V1–V6 stay ok and the package gate stays `defects=0` — the kill is V7's clause alone |
| fidelity | the same rule replayed on the round-37 entry's map must flag `instruction.md:9` (and only the rows D2/F37CritC2Map name) |
| restoration | entry byte-equal to the landing tip after every probe; final baseline re-run green |

## Setup

Scratch clone per the clone rule (`S=/fast/scratch/hyaku/kengaku-r38/F38MapV7Control`, `TMPDIR=$S`,
`--no-local` clone of the lane, checkout `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`):

- `git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r38/F38MapV7Control/lane`;
  `git -C "$S/lane" rev-parse HEAD` → `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`; `status --porcelain` → empty.
- Pristine entry digest: `sha256sum $S/lane/corpus/knowledge/tb2-build-pmars-grader.md` →
  `93484367bb0cb7df3a76dfee4f1db4255d36305f7a0841d52f25181987c23e5f` (equals the lane's file).

**Baseline (pristine clone):** `python3 plans/round38_c2_verify.py --lane . --work "$S"` →
`V1…V7 ok`, `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 (receipt `baseline.out`; 1.35 s).

Rule under attack (counter docstring, `plans/round38_c2_verify.py:31-32`): "`enforced` iff all of them are
observed `fail`, `unenforced` iff all are observed `pass`, `partly` otherwise", derived over **all** receipt
cases whose `violates=` set carries the tag, plus the citation clause (every cited id must be one of those
violating cases, `:213-256`). The entry's map (`corpus/knowledge/tb2-build-pmars-grader.md:143-149`) has
seven rows, all `partly`; the violating sets come from the frozen receipt
(`corpus/evidence/round38/build-pmars-probe.txt:4-25`, 22 cases, 15 fail / 7 pass).

## Mutants — every edit in the scratch clone only, then `git -C "$S/lane" add -A`, then the counter

| # | mutation (row edited at `:144`/`:147`/`:148`/`:149`) | V7 note | exit | verdict |
|---|---|---|---|---|
| M1 | `no-x11` `partly`→`enforced`, citing only `canned-x11-linked` (observed `fail`, probe `:8`) — the round-37 witness-picking shape | `no-x11: labelled enforced, receipt derives partly` | 1 | **caught** |
| M2 | `no-x11` keeps `partly` but cites `canned-shape`, which does not violate `no-x11` | `no-x11: cites no case or a case that does not violate it` | 1 | **caught** |
| M3 | `install-path` row duplicated verbatim | `tags missing=0 duplicated=['install-path']` | 1 | **caught** |
| M4 | `results-format` row deleted | `tags missing=['results-format'] duplicated=0` | 1 | **caught** |
| M5 | `debugger-works` row line `:9`→`:8` (frozen binding is `instruction.md:9`, dry table `:7`) | `debugger-works: line 8 is not the frozen instruction.md:9` | 1 | **caught** |

Full outputs: `m1.out`…`m5.out` (this dir). Every mutant run shows `V1 ok … V6 ok`, `V7 DEFECT`,
`checks=7 defects=1`, `PREDICATE C2 fail`. Attributability: the gate inside V2 stayed green in all five
runs (`gate: P9 ok untracked=0`, `gate: P10 ok probe_rerun=byte-equal bytes=5537`, `gate: defects=0` —
e.g. `m1.out`, `m3.out`), so a relabelled/duplicated/decapitated map passes the package gate and **only**
V7's clause kills it. M1 is exactly the admitted round-37 defect shape: label `enforced` written from the
failing witnesses while an observed-`pass` violator (`canned-x11-dlopen`, probe `:9`) sits in the frozen set.

## Retro leg — the derived rule applied to the round-37 entry's map

Round-37 receipt has no `violates=` tag, so the per-case violates-set comes from the wave-1 table
(`.ufo/waves/round-38/build/R38MapRetro/violates-r37.tsv`, 22 justified rows). Run in my clone at the
landing tip (read-only):

```
python3 .ufo/waves/round-38/build/R38MapRetro/map_label_retro.py \
  --entry corpus/knowledge/tb2-git-webserver-grader.md \
  --receipt corpus/evidence/round37/git-webserver-probe.txt \
  --violates .ufo/waves/round-38/build/R38MapRetro/violates-r37.tsv \
  --instruction corpus/evidence/round37/tb2-git-webserver/instruction.md
```

→ `rows=4 disagree=2 problems=0`, `MAP-RETRO disagree=2 rule=violating fail`, exit 1 (`retro-violating.out`):

- `ROW instruction.md:9 labelled=enforced derived=partly agree=NO` — `violating-but-passing=
  ['status-then-content-split', 'token-in-body', 'trailing-newlines', 'wget-token-in-body']`; the filed row
  (`tb2-git-webserver-grader.md:107`) cites only `capitalised`, `leading-space` (both `fail`).
- `ROW instruction.md:8 labelled=partly derived=partly agree=NO` — citation defect: `catch-all-200`
  `NOT-A-VIOLATOR`.

The `instruction.md:9` disagreement, grounded: line 9 of the round-37 capture reads `then I see the output
"hello world".` (`corpus/evidence/round37/tb2-git-webserver/instruction.md:9`), while
`CASE token-in-body tools=curl predicted=pass observed=pass match=yes` (`git-webserver-probe.txt:35`)
serves a body that is not `hello world` and is observed **pass** — so line 9 is not fully enforced, and the
filed `enforced` stands only because round-37's V7 read the cited witnesses. Ablation on the same defective
map: `--rule cited` → `rows=4 disagree=0 problems=0`, `MAP-RETRO disagree=0 rule=cited pass`, exit 0
(`retro-cited.out`; row 9 `cited-verdicts=capitalised=fail leading-space=fail` → derives `enforced`). The
old rule is the blind spot; the new rule sees the same map fail.

The landing tip's `## Errata (round 38)` (`tb2-git-webserver-grader.md:293`, §A table) restates row 9 as
`partly` citing `capitalised`, `leading-space`, `token-in-body` — exactly my driver's derivation — so the
filed table (append-only, still `enforced` at `:107`) and the correction of record disagree, and the
disagreement is now machine-checkable, not prose.

## Restoration

- After every mutant the entry was restored from the pristine copy; `sha256sum` after each restore →
  `93484367bb0cb7df…` (full digest above), byte-equal to the landing tip.
- Final state: `git -C "$S/lane" add -A` after restore → `status --porcelain` empty; baseline re-run on the
  restored tree → `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 (`baseline.out`).
- No lane file, fleet root, sibling lane, jj state or Git index outside the scratch clone was touched; no
  git command ran in the real lane; no tools installed (stdlib Python 3 only); no subagents.

## Limits

- The five mutants are the tasking's set; other V7 clauses (invented tag, unparsable row, empty citation)
  were read in the code (`:216-256`) but not executed here.
- The retro's violates-set is wave-1's judgment table, reused as the driver's input; the two decisive rows
  (9's `token-in-body`, 8's `status-then-content-split`) rest on the entry's own text and the receipt, not
  on my judgment.
- Scratch `/fast/scratch/hyaku/kengaku-r38/F38MapV7Control` removed after filing receipts.

VERDICT: v7-controls-5/5
