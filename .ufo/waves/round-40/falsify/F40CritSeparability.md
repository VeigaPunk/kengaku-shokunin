# F40CritSeparability — round 40, wave 2 (falsify)

Item: separability of C1 (calibration, `plans/round40_c1_verify.py`) and C2 (coverage,
`plans/round40_c2_verify.py`) measured at lane tip `ec1005a2a28bc5cfdde7723374368ed4cc956eed` on a clean
clone. Attacks: the frozen claims' `## Separability` paragraph
(`plans/round-40-claims.md:96-99`) and, through it, the admission argument for both claims.

Receipts: `.ufo/waves/round-40/falsify/F40CritSeparability/` (13 files, listed in §9).

**Answer to the two assigned questions: yes, both counters pass with the other's work product wholly
absent — but only for the exact frozen removal sets. The sentence's enumeration "C1 reads only the three
tools, plans/battery40 and a clone of the lane HEAD" is false, and one C2 README line is load-bearing for
C1's predicate (§4).**

## 1. Method (what was measured, where)

Scratch `S=/fast/scratch/hyaku/kengaku-r40/F40CritSeparability`; `S/lane` =
`git clone --no-local` of the lane + `git checkout -q ec1005a…`; `git rev-parse --show-toplevel`
returned `$S/lane` before any write. Every counter, ledger, gate and battery invocation ran inside the
ruled sandbox (`--dev-bind / /`, `~/.local/bin` re-bound read-only, `--tmpfs /run/user/1000`,
`--proc /proc`, `--unshare-pid`, `--die-with-parent`), with `HOME=$S/home TMPDIR=$S/tmp
UV_CACHE_DIR=$S/uvcache XDG_CACHE_HOME=$S/cache` so nothing was written under the real `$HOME`.
No `systemd-run`, no user service, no pacman, no installs. The real lane tree was never written: tip is
still `c9c793ca33fab1cdaf1127c06ba31685c7db1325` at the end (`clone-inventory.txt`).

Counterfactual clones are scratch-only, `git -C $S/<name>` for every git call; **no commit, branch or ref
was created in `$S/lane`** — the lane mirror is untouched (`HEAD=ec1005a… branch=[] status=[0 paths]`).
Three of the counterfactual clones needed a *committed* removal because the C1 counter clones `HEAD` for every
fixture (`plans/round40_c1_verify.py:467-468` and `Ctx.clone` at `:263`) and the C2 gate
reads a work tree; those commits exist only in throwaway clones `c1noc2` (`d8e27cc`), `c2nobat`
(`9fb7484`) and `c2partial` (`4bf5f5d`), all under `/fast/scratch`, all deleted at the end.

C2 removal set (12 deleted paths across 2 modified files, superset of the assigned list — the entry, S119/S120/S121, its `corpus/README.md`
lines, the receipt, plus the dry table and the 9-file capture directory, so that "wholly absent" is literal):
`corpus/knowledge/tb2-db-wal-recovery-grader.md`; 3 SOURCES rows; 19 `corpus/README.md` lines (index row,
coverage bullet, the 15-line "Partly discharged round 40" block, 2 evidence bullets);
`corpus/evidence/round40/{db-wal-probe.txt, db-wal-dry-cases-freeze.txt, tb2-db-wal-recovery/}`.
No residual `db-wal|S119|S120|S121` string survives in SOURCES.md or corpus/README.md.

## 2. Q1 — C1 with the C2 package removed: still passes (both readings)

| clone | C2 state | C1 output | exit |
|---|---|---|---|
| `lane` (baseline) | present | `BATTERY fixtures=21 wrong=0 … MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0 … PREDICATE C1 pass` | 0 |
| `c2gone` | deleted in work tree only, HEAD unchanged | **byte-identical** to baseline | 0 |
| `c1noc2` | deleted **and committed** (`d8e27cc`), so HEAD has no C2 path | **byte-identical** to baseline | 0 |

`cmp` on the three receipts: identical (`rc1-base.txt` ≡ `rc1-c2gone-wt.txt` ≡ `rc1-c1noc2.txt`).

Receipt lines, `rc1-c1noc2.txt`:
```
PINS total=3 mismatched=0
BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 pass
```

**The work-tree-only removal is vacuous for C1, and the claims do not say so.** Because the counter clones
`HEAD` into its own pristine tree and hands *that* to every `build()` (`ctx.lane`), deleting the C2 bytes
from the caller's work tree changes nothing C1 can see: a `git clone --shared` of `c2gone` (the same
operation the counter performs) lists 12 C2 paths while the work tree lists none (measured, §1 method
note; `/workspace`-free probe clone, removed after the check). The claim's own sentence — "C1 reads … a
clone of the lane HEAD for its fixtures" — acknowledges this, so the honest Q1 answer needs the
committed-removal run, which is what `c1noc2` provides: **pass, byte-for-byte unchanged.**

## 3. Q2 — C2 with `plans/battery40` removed: still passes, byte-for-byte

`c2nobat` = clean clone, `git rm -r plans/battery40`, commit (`9fb7484`), tree clean, C2 package intact.

```
V1 ok listed=8 bad=0 extra=0
    gate: P8 ok index_rows=47 knowledge_files=47 bad=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=8257
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=28 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=6 tags=6 bad=0
checks=7 defects=0
PREDICATE C2 pass
```
`cmp rc2-base.txt rc2-nobattery.txt` → identical. Static corroboration: `grep -c
'battery40|round40_c1'` is **0** in each of `plans/round40_c2_verify.py`, `plans/pkg_gate.py`,
`plans/pkg-spec-r40.json`, `plans/db_wal_probe.py`. This direction is genuinely separate.

## 4. F1 (counterexample) — one C2 line flips BOTH predicates

`c2partial` (`4bf5f5d`, `1 file changed, 1 deletion(-)`): the **single** line
`` | `knowledge/tb2-db-wal-recovery-grader.md` | … `` removed from `corpus/README.md`; entry, S119/S120,
receipt and captures all still present. That line is one of the "README lines" this item was told to
remove, i.e. it is C2 work product.

```
$ python3 plans/round40_c2_verify.py --lane .          → V2 DEFECT spec=frozen gate=frozen gate_exit=1
    gate: P8 DEFECT index_rows=46 knowledge_files=47 bad=2 first=index rows for
          knowledge/tb2-db-wal-recovery-grader.md=0                                        checks=7 defects=1
PREDICATE C2 fail                                       exit=1
$ python3 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r35.json
P8 DEFECT index_rows=46 knowledge_files=47 bad=1 first=knowledge files=47 index rows=46   exit=1
$ python3 plans/ledger_tip.py --lane .
R35-D1 status=closed observed=fail agree=NO fixtures=14 … tip_package_rc=1
rows=9 closed=9 observed_pass=8 mismatches=1                                              exit=1
$ python3 plans/round40_c1_verify.py --lane . --work …
FIXTURE l_rows-open-row      declared=NO:R34-D2 observed_rc=1 observed=NO:R34-D2,NO:R35-D1 WRONG
FIXTURE l_rows-check-crashes declared=NO:R34-D3 observed_rc=1 observed=NO:R34-D3,NO:R35-D1 WRONG
FIXTURE l_rows-unknown-check declared=NO:R34-D5 observed_rc=1 observed=NO:R34-D5,NO:R35-D1 WRONG
BATTERY fixtures=21 wrong=3 tampered=0 sidechannel=0
MUTANTS total=21 killed=18 survived=3 invalid=0 null_detected=0
PREDICATE C1 fail                                        exit=1   (survivors L05, L14, L15)
```

The A/B is clean: `ledgerbase` (master pinned at the tip, C2 intact) prints
`R35-D1 status=closed observed=pass agree=yes`, `rows=9 … mismatches=0`, exit 0; the only difference
between `ledgerbase` and `c2partial` is that one README line. Every other clone in §2 is also detached at
`ec1005a` and passes C1, so the detached-HEAD/`clone-lacks-ref` binding is not the cause.

### Mechanism (the coupling the claims mislocate)

`plans/ledger_tip.py:84` — `"r35_d1": "live"` — evaluates `plans/round36_c1_verify.py:267` `r35_d1`, which
calls `run_gate(lane, ["package", "--root", str(lane), "--rerun", "--require-clean-tree"])`
(`:272`) against `SPEC_REL = "plans/pkg-spec-r35.json"` (`:39`, `:208-214`). That spec points the gate at
the **live** corpus: `"readme": "corpus/README.md"`, `"knowledge_glob": "corpus/knowledge/*.md"`
(`plans/pkg-spec-r35.json:13-14`), which `pkg_gate.py` P8 compares as `index_rows` vs `knowledge_files`.
The predicate runs in every `l_rows*`/`l_refuse*` battery fixture, on a clone of the lane HEAD, so **C1
transitively reads the C2 entry's existence and every C2 README line.**

This also corrects the sentence's causal clause. It says "a C2 package landing changes what an **anchor**
tip fixture sees". Measured: no anchor fixture moves — with C2 wholly absent (`c1noc2`) the 11 anchor
fixtures are `ok`, `wrong=0`, and the receipt is byte-identical to the baseline. The sensitivity is on the
**ledger** fixtures, it is a README/knowledge-count dependency, and it is not tip-scoped (any later edit of
`corpus/knowledge/*.md` or `corpus/README.md` moves C1's declared class sets). The sentence names the one
group of fixtures that is empirically insensitive and omits the group that is load-bearing.

## 5. Does the separability sentence hold? Clause by clause

| clause (`plans/round-40-claims.md:96-99`) | verdict | receipt |
|---|---|---|
| "C1 reads only the three tools, plans/battery40 and a clone of the lane HEAD" | **FALSE** | §4: C1's ledger fixtures run `ledger_tip.py`, whose `r35_d1` runs the round-35 gate against live `corpus/knowledge/*.md` + `corpus/README.md`. C1 also reads `corpus/defects{,-round35}.jsonl`, `plans/pkg-spec-r35.json`, `plans/pkg_gate.py`, `plans/round36_c1_verify.py`, `plans/defect_ledger.py`, the round-35 package bytes and `.ufo/waves/round-34/…/SHA256SUMS` |
| "C2 reads only its captures, spec, gate, probe, receipt, entry, SOURCES and README" | **incomplete** | it also reads `corpus/evidence/round40/db-wal-dry-cases-freeze.txt` (`plans/round40_c2_verify.py:65`) and the fleet-root `scripts/sources-census.sh` (`:67`) — a path outside the lane |
| "C1's fixtures copy the live corpus, so a C2 package landing changes what an anchor tip fixture sees" | **FALSE as located** | anchor fixtures are byte-insensitively green with C2 wholly absent (§2); the live coupling is ledger→gate P8 (§4) |
| "Each claim's counter passes with the other's work product wholly absent" | **TRUE for the frozen sets only** | §2 (C1: 21/21 killed with C2 committed-absent) and §3 (C2: `checks=7 defects=0` with battery40 committed-absent); falsified as a general property by §4 (one C2 line ⇒ C1 `wrong=3`, `survived=3`) |

So: admission is separable when each package is removed/reverted **consistently**; it is not separable
from a *partial* or *defective* C2 package, because the two claims share one authority (the live corpus
counts) through a third party (`ledger_tip.py` → `pkg_gate.py` P8).

## 6. Impacted axes

- **Calibration (primary).** C1's headline calibration claim is preceded by a false statement about its
  own input surface. Distinct from the wave-1 gameability findings (`R40CritC1Counter.md`,
  `R40SentinelCounter.md`, `R40RevCounters.md`): those attack the battery from inside; this one shows the
  counter's verdict is a function of another claim's package bytes, which no non-author review of
  `battery40` can see.
- **Coverage (C2).** The C2 entry file and its index line are load-bearing for C1's predicate, so a C2
  rejection for a coverage-side defect (P8) also reds calibration. The C2 admission is otherwise
  independent (battery40 absent ⇒ byte-identical verdict).
- Not affected: novelty, depth, freshness, adjacency, operability.

Not a counter defect: C1 red on an unbalanced corpus is *correct* behaviour (the lane's corpus contract is
broken in that state). The defect is in the claim text and in the absent limit, which decides how the round
may report the two axes.

## 7. Smallest safe correction

1. Replace the first and third clauses of `## Separability` (next freeze; the frozen file is untouched) with
   the measured statement: *"C1's counter reads the three pinned tools, `plans/battery40` and a clone of
   HEAD; every fixture runs those tools inside that clone, so C1 also depends on what the tools read there
   — in particular ledger row R35-D1's round-35 package gate, whose P8 counts live `corpus/knowledge/*.md`
   against `corpus/README.md`. Removing the C2 entry and all its README lines together leaves C1
   byte-identically green (measured, `c1noc2`); removing one of them alone turns C1 red (`wrong=3`,
   `survived=3`) and C2 red (V2, `gate_exit=1`). Separability is asserted for the frozen removal set only."*
   The claim that an *anchor* fixture moves is deleted; the ledger/gate mechanism replaces it.
2. Add to C1's "Limits named now": C1 carries the lane's corpus-consistency verdicts through R35-D1
   (`plans/ledger_tip.py:84` → `plans/round36_c1_verify.py:267-274` → `plans/pkg-spec-r35.json:13-14`), so
   a corpus-only defect in another claim's package reds C1.
3. Add the dry table and the fleet-root census script to C2's declared read set.

No counter, battery or pin change is warranted: every input is already digest-pinned, the 21-mutant total
is frozen, and both predicates are green at the tip.

## 8. Scope and limits of this review

- Measured at `ec1005a`; the landing measurement file says `TIP ec172168…`. `git diff ec17216..ec1005a`
  shows one path (`corpus/lessons/round-40.md`, read only for erratum lines by the anchor tool), so the
  two measurement points are equivalent for these counters; my baseline reproduces the recorded C1/C2
  verdicts exactly.
- Not tested: any C2 state other than wholly-present, wholly-absent and the single-line partial; a
  battery40 partial removal (e.g. one module) — C2 does not read the directory at all (grep 0), so the
  verdict cannot move; host-side interference.
- The counterfactual commits (§1) are scratch-only and disclosed deliberately: the C1 counter clones HEAD
  and the C2 gate needs a readable work tree, so a work-tree-only deletion cannot answer "is C1 green with
  C2 absent". The literal work-tree removal was run as well and is reported, with its vacuity named.
- Scratch `/fast/scratch/hyaku/kengaku-r40/F40CritSeparability` deleted; all clones removed; no process left
  running; no tool installed or updated.

## 9. Receipt index (`.ufo/waves/round-40/falsify/F40CritSeparability/`)

`rc1-base.txt`, `rc1-c2gone-wt.txt`, `rc1-c1noc2.txt` (identical), `rc1-c2partial.txt`, `rc2-base.txt`,
`rc2-nobattery.txt` (identical), `rc2-partial.txt`, `ledger-base.txt`, `ledger-c2partial.txt`,
`gate-c2partial-r35spec.txt`, `gate-c1noc2-r35spec.txt`, `c2partial-commit.txt`, `clone-inventory.txt`.

VERDICT: separable-c1-yes-c2-yes
