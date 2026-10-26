# R37BatP5 — C1 battery module p5 (P5 capture-manifest branches, mutants M13–M19)

Seat: R37BatP5 (executor, leaf). Lane `kengaku-shokunin`, round 37 wave 1. Read first, in full:
`plans/round-37-claims.md`, `plans/round37_c1_verify.py`, `plans/pkg_gate.py` (freeze digest
`ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`, the counter printed
`GATE plans/pkg_gate.py sha256=frozen`), `plans/pkg-spec-r35.json`, `plans/round36_c1_verify.py`,
`.ufo/waves/round-37/claims/example_battery/ex_p3_words.py`.

## Deliverable

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37BatP5/battery/p5.py`
(one module, stdlib only, seven fixtures, all fids prefixed `p5-`).

sha256 of the module:

```
bd87f3f2fbec1bdb7253890f5936678c9cdded6051c64699399dbdb55f268322  p5.py
```

Verified receipt copies: `build/R37BatP5/receipt-primary-counter.txt`
(sha256 `295799e477ed184e6cef298637001f86a0d2e975d1bb53a2e0ef7d3728875d07`) and
`build/R37BatP5/receipt-removal-table.txt`
(sha256 `13aef4a3e062a3a153436c97ab3fdc2f3ae3a4c217ca0d699a83496ecb86ba51`).

## Design: one fixture per frozen mutant, one declared clause (P5)

Every builder starts from `ctx.genuine_package(d)` (the real round-35 package, git-inited), makes the
manifest defect, then `ctx.git_add(d)` and returns
`["package", "--root", d, "--require-clean-tree"]` (no `--rerun`, so P10 never runs).

| fid | mutant | the fixture's one defect | unmodified gate | declared `defects` |
|---|---|---|---|---|
| `p5-manifest-absent` | M13 | `SHA256SUMS` deleted from the capture dir | rc 1, `P5 DEFECT capture manifest absent:` | `["P5"]` |
| `p5-manifest-unparsed-line` | M14 | one appended line that is not `<64 hex>  <name>` | rc 1, `P5 DEFECT … unparsed manifest line` | `["P5"]` |
| `p5-capture-bytes-stale-digest` | M15 | bytes of the pinned `task.toml` changed, its pinned digest left stale | rc 1, `P5 DEFECT … manifest digest does not match the bytes` | `["P5"]` |
| `p5-row-capture-unpinned` | M16 | row S105's capture has no manifest line (unpinned) | rc 1, `P5 DEFECT … S105: capture test_outputs.py is not pinned in the manifest` | `["P5"]` |
| `p5-manifest-digest-off-pin` | M17 | one row's manifest line moved to the new bytes' digest, so it differs from the spec pin | rc 1, `P5 DEFECT … manifest digest differs from the spec pin` | `["P5"]` |
| `p5-quote-cites-unpinned` | M18 | one quote re-cited to `.quote-extra.txt:1`, a capture on disk with no manifest line | rc 1, `P5 DEFECT … quote capture .quote-extra.txt is not pinned in the manifest` | `["P5"]` |
| `p5-extra-capture-file` | M19 | `extra-note.txt` added to the capture dir, not pinned, cited by no quote | rc 1, `P5 DEFECT … extra-note.txt: capture file not covered by the manifest` | `["P5"]` |

Why each fixture isolates its own branch (the manifest loop branches share one `bad` list, so a
fixture that leaves two firing cannot demonstrate either mutant):

- **M13** — the manifest is gone, so `c_captures` returns at the `manifest absent` return; no other P5
  branch is reachable. Nothing else reads `SHA256SUMS`.
- **M14** — one extra line; every genuine line still parses, so no digest/coverage branch moves.
- **M15** — the capture is `task.toml`: it is pinned in the manifest but named by no registry row and by
  no quote, so the digest-vs-bytes branch fires alone. P4 reads only quoted captures, so P4 stays green.
  The spec pin for a row is untouched (M17 branch silent).
- **M16** — the single defect is "one registry row's capture is unpinned". Two frozen properties of the
  round-35 package force bookkeeping around it: every row capture is also cited by a quote (dropping the
  pin would also trip the quote-capture branch, M18, in the same clause and M18 would keep P5 red), and a
  file left on disk without a pin trips the not-covered sweep (M19). So the capture's bytes move to a
  byte-identical `<capture>.copy`, pinned with the same digest (bytes unchanged, so the M15 branch is
  silent), and the quotes are re-cited to the copy at the same line numbers (verbatim, so P4 is silent);
  the original name then leaves both the manifest and the directory. One defect class, one clause.
- **M17** — the row's manifest line is rewritten to the digest of the appended bytes, so bytes and
  manifest agree (M15 silent) while the value differs from `spec["rows"][sid]["sha256"]`. The appended
  line lands after the last line any quote cites (highest cited line with the r35 spec: 71 of 73 in
  `test_outputs.py`), so P4 stays verbatim-green.
- **M18** — the new capture is a dotfile. The not-covered sweep skips names starting with `.`, so the
  quote-capture branch is the only one that fires; the quoted text sits verbatim on line 1, so P4 is
  green.
- **M19** — one added file, unpinned and uncited; the row/spec-pin/digest branches and P4 are untouched.

No fixture is name-recognisable: the gate never keys on a path, and the counter's renamed run reported
`renamed_disagree=0`.

## Proof (pasted in full)

`python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round37_c1_verify.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37BatP5/battery --only M13,M14,M15,M16,M17,M18,M19 --work "$S"`

(`$S=/fast/scratch/hyaku/kengaku-r37/R37BatP5`, `TMPDIR="$S"`; `--only`/`--battery-dir` make the
predicate print `n/a` by design — it prints `n/a` for any non-default battery or mutant subset. Exit 0.
Three runs are byte-equal: two before the module docstring was tightened and one after, so the receipt
sha256 is unchanged by that edit (`diff -u` between the first two → no output).)

```
GATE plans/pkg_gate.py sha256=frozen
FIXTURE r36-P0 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-P1 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P2 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P3 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P4 expect=reject declared=- observed_rc=1 observed_defects=P6 ok
FIXTURE r36-P5 expect=reject declared=- observed_rc=1 observed_defects=P1 ok
FIXTURE r36-P6 expect=reject declared=- observed_rc=1 observed_defects=P9 ok
FIXTURE r36-P7 expect=reject declared=- observed_rc=1 observed_defects=P1,P3,P6,P9 ok
FIXTURE r36-L1 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L2 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L3 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L4 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L5 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE r36-L6 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE p5-manifest-absent expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-manifest-unparsed-line expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-capture-bytes-stale-digest expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-row-capture-unpinned expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-manifest-digest-off-pin expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-quote-cites-unpinned expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-extra-capture-file expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
BATTERY fixtures=21 wrong=0 renamed_disagree=0
MUTANT M13 P5 killed by=p5-manifest-absent -- capture manifest absent
MUTANT M14 P5 killed by=p5-manifest-unparsed-line -- unparsed manifest line
MUTANT M15 P5 killed by=p5-capture-bytes-stale-digest -- manifest digest does not match the capture bytes
MUTANT M16 P5 killed by=p5-row-capture-unpinned -- row capture not pinned in the manifest
MUTANT M17 P5 killed by=p5-manifest-digest-off-pin -- manifest digest differs from the spec pin
MUTANT M18 P5 killed by=p5-quote-cites-unpinned -- quoted capture not pinned in the manifest
MUTANT M19 P5 killed by=p5-extra-capture-file -- capture file not covered by the manifest
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Every one of the seven `FIXTURE` lines ends `ok`; `wrong=0`, `renamed_disagree=0`,
`null_detected=0`; each mutant `killed by=` its own fid.

## Load-bearing check: delete one fixture at a time

Each variant module is the deliverable with exactly one `FIXTURES` entry removed
(`grep -v '"fid": "<fid>"' p5.py`, in scratch); same command with `--battery-dir <variant>`:

```
### removed p5-manifest-absent
BATTERY fixtures=20 wrong=0 renamed_disagree=0
MUTANT M13 P5 SURVIVED -- capture manifest absent
MUTANT M14 P5 killed by=p5-manifest-unparsed-line -- unparsed manifest line
MUTANT M15 P5 killed by=p5-capture-bytes-stale-digest -- manifest digest does not match the capture bytes
MUTANT M16 P5 killed by=p5-row-capture-unpinned -- row capture not pinned in the manifest
MUTANT M17 P5 killed by=p5-manifest-digest-off-pin -- manifest digest differs from the spec pin
MUTANT M18 P5 killed by=p5-quote-cites-unpinned -- quoted capture not pinned in the manifest
MUTANT M19 P5 killed by=p5-extra-capture-file -- capture file not covered by the manifest
MUTANTS total=7 killed=6 survived=1 invalid=0 null_detected=0
### removed p5-manifest-unparsed-line
MUTANT M14 P5 SURVIVED -- unparsed manifest line
### removed p5-capture-bytes-stale-digest
MUTANT M15 P5 SURVIVED -- manifest digest does not match the capture bytes
### removed p5-row-capture-unpinned
MUTANT M16 P5 SURVIVED -- row capture not pinned in the manifest
### removed p5-manifest-digest-off-pin
MUTANT M17 P5 SURVIVED -- manifest digest differs from the spec pin
### removed p5-quote-cites-unpinned
MUTANT M18 P5 SURVIVED -- quoted capture not pinned in the manifest
### removed p5-extra-capture-file
MUTANT M19 P5 SURVIVED -- capture file not covered by the manifest
```

Every row above is the exact line the counter printed; the full block (all `BATTERY`, `MUTANT` and
`PREDICATE` lines for all seven variants, `fixtures=20 wrong=0 renamed_disagree=0` each) is retained at
`build/R37BatP5/receipt-removal-table.txt`. The mapping is a clean diagonal: removing fixture X flips
exactly mutant X from `killed` to `SURVIVED` and leaves the other six killed. Each fixture is
load-bearing; no mutant is killed by a sibling.

## Scope, tools, scratch

- Files written inside the lane: `build/R37BatP5/battery/p5.py`, `build/R37BatP5.md`, the two receipt
  copies. No lane file (`corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`,
  `PROVINCE.md`, `SHONEN.md`), no index, no jj state touched; the frozen gate, counters, probe, mutant
  list and spec were only read. No `git`/`jj` mutation in the lane; the counter's fixture repos live
  under `$S` and are removed.
- Tools installed: none (no package manager transaction; nothing was needed).
- Scratch `/fast/scratch/hyaku/kengaku-r37/R37BatP5` removed at the end; receipts copied out first.
- No subagents, no background jobs, no `task`.

## Risks / limits

- **Lane-consistency dependency of the whole gate run.** My fixtures run the full `package` check set,
  so they inherit the r36-C1 separability condition: the copied tree's `corpus/knowledge/*.md` and the
  README index rows must be consistent (both C2 files present or both absent). A half-landed C2 entry
  would add a `P8` defect to my fixtures (and to `r36-P0`), i.e. a `wrong` declaration, not a P5 kill.
  Observed at this tip: `wrong=0`.
- **Frozen-package dependence.** The four isolation tricks are keyed to frozen facts, not to fixture
  names: `task.toml` is pinned but neither a row nor a quote (M15), the highest quoted line is 71 of 73
  (M17 appends at the end), every row capture is quoted (M16's byte-identical copy), and the not-covered
  sweep skips dotfiles (M18). If the round-35 spec or captures are ever re-frozen, these fixtures must be
  re-derived, not patched.
- **M16 is the least literal fixture.** Its defect is exactly "a registry row's capture is unpinned", but
  reaching that branch alone requires moving the capture to a pinned byte-identical copy and re-citing the
  quotes. A reader who expects "delete the manifest line" will not find it; the docstring states why.
- **Demonstration is observational**, as the claim names: these fixtures show each P5 branch is reached
  and changes the gate's observable result; they do not show that each check is the right check.

VERDICT: battery-p5-killed-7/7-wrong-0
