# R36RevBattery — C1 battery review (kengaku round 36, wave 1)

Seat: reviewer of the frozen C1 battery in
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round36_c1_verify.py`
(sha256 `d7c3687c09ed4c8a09a9d7c63efa9232c2b1aff8ffb229fb8a0505578317df73`, equals the freeze digest),
against the four routed items at
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-35-verifier-spotcheck.md:86-89`
and the frozen claims `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-36-claims.md`.

Method: read the counter and spec in full; built a compliant fixture clone
(`git clone -q --no-checkout --shared <lane> $D/lane; git sparse-checkout set --no-cone '/plans/' '/corpus/' '/SCORECARD.md' '/.ufo/waves/round-34/assimilation/captures/'; git checkout master`;
`git -C $D/lane rev-parse --show-toplevel` printed `$D/lane`); then ran the frozen battery against
three purpose-built oracles and one ledger edit. `plans/pkg_gate.py` is absent at the tip, so every
gate below is a review probe in the clone, never a lane file. No lane file was written; no pacman
transaction was run. One transient environment was used: `uv run --no-project --with biopython==1.85`
(uv `/home/vgpnk/.local/bin/uv`, pre-installed; no install into the host).

Clone tip under test: `f9efce3beb0705ec2e04ba3f8f449d10d64cc1dd` (wave-1 spec and dispatch commit).

---

## Answers to the four questions

1. **Does each fixture isolate one defect class?** No. P1 and P4 each violate *two* clauses and are
   rejected by the clause they were not built to test, so both word-count clauses are unfalsified
   (F4). P7 is a composite by design and adds no class beyond P1/P4/P5/P6. P3 is the only parse
   fixture and its bad row is recognizable by straight quotes alone.
2. **Can a gate satisfy `false_green=0` without implementing the class?** Yes, three independent
   ways, each scoring `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`:
   a lane-identity diff gate (F2), a fixture-**name**-keyed gate (F3), and a "spec-lite" gate that
   omits nine frozen clause families (F4/F5). The battery has exactly one genuine state per surface
   (P0, L1, L4), so any comparator or recognizer wins.
3. **Is `P0` + `L1/L4` enough to stop a reject-everything gate?** Yes against a *constant* reject
   function: the frozen control `control-c1-reject-all.txt` shows `false_red=3`, so the predicate
   fails. No against a *conditional* rejector: the three accept points are exactly the three the
   identity oracle hits. The accept set is minimal, not sufficient for calibration.
4. **Is R35-D2's `untracked_anywhere` satisfiable at the landing tip by honest means?** Yes —
   commit all wave evidence, then measure in a clean clone (or in the working lane after the commit);
   the battery writes only into `mktemp` dirs, so it does not dirty the lane itself (verified:
   `git status --porcelain` unchanged except the files I staged). But the observation is
   **tautological at the measurement site**: a fresh `git clone` cannot contain untracked files, so
   `untracked_anywhere=0` is guaranteed by the measurement method, not by lane hygiene (F7). The
   half with teeth is `line_fixtures_wrong=0/6`. R35-D2's substantive ask (read committed bytes,
   `git show <rev>:<path>`) is untestable in this battery and in tension with it (F8).

---

## Findings by severity

### F1 — CRITICAL (counter): the frozen id→check binding is not enforced; the predicate passes with two routed rows genuinely red

`round36_c1_verify.py:338` resolves the check with `fn = CHECKS.get(r.get("check"))` — the *ledger
file's own text* selects which function proves the row. Nothing compares `id`→expected function. The
claims say "its check names and ids are frozen"; the counter does not check that.

Reproduction (clone; spec-lite gate installed; all four rows `status=closed`; **`check` rewritten to
`r35_d1` for all four**; D3 and D4 untouched and still red):

```
$ git ls-tree -r --name-only refs/heads/master | grep -cE '^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-'
21
$ test -f corpus/lessons/round-36.md && echo lesson-present || echo lesson-absent
lesson-absent
$ python3 plans/round36_c1_verify.py --lane .
FIXTURES total=14 false_green=0 false_red=0 unevaluated=0
R35-D1 status=closed observed=pass agree=yes ...
R35-D2 status=closed observed=pass agree=yes ...
R35-D3 status=closed observed=pass agree=yes ...      <- 21 nested paths still committed
R35-D4 status=closed observed=pass agree=yes ...      <- round-36 lesson absent
rows=4 closed=4 observed_pass=4 mismatches=0
PREDICATE C1 pass
exit=0
```

Severity: the predicate's kill rule is "any row open, any check failing … → C1 not admitted"; this
bypass admits C1 with 2 of 4 rows failing, with zero lane work. Corollary: `battery()` runs *before*
the ledger is read (`round36_c1_verify.py:333-337`), so a `plans/pkg_gate.py` subprocess can rewrite
`corpus/defects-round35.jsonl` during the run — the L1 need not even edit it by hand. The only
guard is that the ledger's `check`/`id` text is frozen — which this counter never verifies.
Recommended (amendment, since the counter is digest-pinned): assert the literal map
`{"R35-D1":"r35_d1","R35-D2":"r35_d2","R35-D3":"r35_d3","R35-D4":"r35_d4"}` and the frozen `source`
refs; fail on deviation. If not amended, the L1 must attach the four checks' raw output to the
receipt, and a wave-2 mutant must rewrite the ledger.

### F2 — CRITICAL (battery): an identity/lane-diff gate scores 14/14 and closes R35-D1 and R35-D2

Oracle: ~60 lines that implement **no** package semantics — no quote parsing, no word counts, no
SOURCES checks, no sha pins, no rerun. It accepts a package iff each spec-named file equals the
lane's own file and the capture dir is byte-equal; it accepts a d4/d5 line iff it equals the lane's
own line (and, for d5, the capture dir equals the lane's). Receipt:

```
FIXTURES total=14 false_green=0 false_red=0 unevaluated=0
R35-D1 status=closed observed=pass agree=yes ... tip_package_rc=0
R35-D2 status=closed observed=pass agree=yes untracked_anywhere=0 line_fixtures_wrong=0/6
```

Why it works: every junk fixture is *different from the lane bytes* and every accept fixture is
*identical* to them, so "equal to the lane" is a perfect classifier. The battery therefore measures
"does the gate compare bytes?", not "does the gate implement the clauses". Note the gate is handed
the real spec path (`run_gate` passes `str(lane / SPEC_REL)`), so the lane is reachable from every
fixture run. Freeze rule: this is a limit to report, not a fixture to repair — but it must be
reported, because the C1 predicate as written cannot distinguish the intended gate from this one.

### F3 — HIGH (battery): fixture-name recognition scores 14/14, and the claims explicitly ban it

The claims: "A gate must never recognise fixtures by name, path, or marker string." Oracle: a gate
that returns 0 iff `"k36-P0-" in root.name`, or the `--file` basename is `d4-genuine.txt` /
`d5-genuine.txt`, else 1. Receipt: `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`.
The battery leaks the identity it forbids: package fixtures live in `mkdtemp(prefix=f"k36-{pid}-")`
(`round36_c1_verify.py:146`) and line fixtures are named `d4-genuine.txt`, `d4-swapped.txt`,
`d4-notoken.txt`, `d5-genuine.txt`, `d5-negated.txt`, `d5-altcap.txt` (`:189-203`), with the full
path passed to the gate. The battery cannot enforce its own anti-overfitting rule; wave-2 mutation
seats must therefore vary names *and* re-run both oracles above.

### F4 — HIGH (calibration): the two word-count clauses are unfalsified; R35-D1's "one-word quotes" survives

Measured properties of the mutations (importing the frozen counter, applying its own mutators to the
genuine entry):

```
P0/genuine: rows=22 parsed=22 distinct_quotes=22 distinct_locs=22 words=[3,4,7,9,10,11,14,15,17,19]
P1 one-word: rows=8 parsed=8 distinct_quotes=7 distinct_locs=8 words=[1]   <- two rows share "assert"
P2 duplicates: rows=8 distinct_quotes=1 distinct_locs=1
P3 unparsed: rows=23 parsed=22
P4 S105 teaches='junk' words=1 ; S106 'junk' ; S107 'junk' ; teaches distinct: False
```

P1 is rejected because it has only **7 distinct quotes** (two mutated rows both start with `assert`),
not because any row is one word; P4 is rejected because all three teaches cells are **identical**,
not because they are one word. A gate that keeps 3..25-word and ≥8-word rules out of its code passes
the battery. Proof — a "spec-lite" gate (parse-all rows, ≥8 distinct quotes/locations, teaches
present+pairwise-distinct, probe sha pin, clean tree, the d4 patterns, d5 require/forbid + manifest +
quote-present) scores:

```
FIXTURES total=14 false_green=0 false_red=0 unevaluated=0
R35-D1 status=closed observed=pass agree=yes ... tip_package_rc=0
```

and then **accepts** the very round-35 defect:

```
8 distinct one-word quotes, each verbatim on its cited line -> spec-lite rc = 0 (ACCEPT)
3 distinct one-word teaches cells                          -> spec-lite rc = 0 (ACCEPT)
```

So the routed defect "frozen counters accept … one-word quotes" (lessons:86) is **not closed by the
battery**: the fixture that should prove it is rejectable on distinctness alone. Minimal repair
outside the freeze: a P1' whose 8 one-word quotes are pairwise distinct, and a P4' whose three
teaches cells are distinct but <8 words each. That is a fixture change the kill rule forbids
repairing into the frozen battery — report as a limit, and add both as wave-2 law (a mutant gate
without word bounds must be caught).

### F5 — MEDIUM (coverage): nine frozen clause families have no fixture at all

The battery's 11 reject fixtures falsify only: parse-all rows (P3), distinct quotes/locations (P2,
incidentally P1), teaches present+distinct (P4), probe identity via sha pin (P5), clean tree (P6),
d4 citation binding (L2/L3), d5 negation + capture integrity (L5/L6). No fixture exercises:

- each quote **verbatim on the cited capture line** — the central package clause; a gate that never
  opens a capture passes 14/14 (both oracles in F2/F3 do);
- the **receipt sha256 pin** — P5 leaves the receipt byte-intact;
- the **package** capture `SHA256SUMS` — only the d5 manifest is attacked (L6);
- the other two **frozen-instrument** pins (`round35_c1_verify.py`, `defect_ledger.py`) — P5/P7 only
  stub the probe, and the spec-lite gate pinned only the probe and still passed;
- SOURCES **11 cells / tier A / status mined / pinned URL / used-by** — P4 touches teaches only;
- the entry **provenance trio** and `## Negative space` falsifier — no fixture alters either;
- **README index row + coverage bullet, knowledge files == index rows** — no fixture alters the
  README or the index (the genuine lane currently holds 42 == 42, so P0 accept depends on the L1
  keeping parity when C2 adds the 43rd);
- `--rerun` **receipt byte-compare** — the spec-lite gate ignored `--rerun` and `r35_d1` still
  passed with `tip_package_rc=0`.

Consequence: "the gate closes R35-D1..D4" is evidenced only for the subset above; eight of the
hardened clauses are asserted by the gate's own code, not by the battery.

### F6 — MEDIUM (reachability): `probe_cmd` in the frozen spec is not the runnable command

`pkg-spec-r35.json` `probe_cmd` is `["plans/tb2_grader_probe.py","--lane","."]`; run under the
counter's interpreter it dies:

```
$ python3 plans/tb2_grader_probe.py --lane .
ModuleNotFoundError: No module named 'Bio'     (probe:145, "fail loudly if Biopython is absent")
```

The canonical runtime exists but only in prose: `plans/tb2_grader_probe.py:11-12` documents
`uv run --no-project --with biopython==1.85 python3 …`, and the round-35 counter implemented exactly
that fallback (`plans/round35_c1_verify.py:163-169`). Verified here:

```
$ uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .
cases=18 observed_pass=5 observed_fail=13 mismatches=0
$ cmp run.txt corpus/evidence/round35/tb2-grader-probe.txt   -> IDENTICAL
```

A gate that faithfully executes the spec's `probe_cmd` fails `--rerun` and reds R35-D1; a gate that
hardcodes the `uv` wrapper implements something the frozen spec does not say. `--rerun` is reachable
(the uv path reproduces the receipt byte-for-byte), but the spec should have carried the command.

### F7 — MEDIUM (R35-D2): the untracked observation is vacuous at the stated measurement site

`r35_d2` reads `git ls-files --others --exclude-standard` in the lane (`:279`). On a clean clone of
the landing tip that set is empty *by construction*; the claim itself specifies that measurement
("measured on a clean clone of the landing tip (no untracked files)"). Honest satisfaction therefore
requires only that the L1 commits the wave evidence and runs the counter where the claims say; it
cannot distinguish a lane that committed its evidence from one that never had leftovers. The gate
`--rerun` runs (`r35_d1`) *before* `r35_d2` scans, so a gate that writes any new file into the lane
flips D2; the probe itself is safe (it writes only inside `tempfile.TemporaryDirectory()`,
`plans/tb2_grader_probe.py:122-124`, and the pre/post untracked set was empty in my run).

### F8 — MEDIUM (fairness tension with R35-D2's fix): package fixtures have no commit

`build_package_fixtures` does `git init` + `git add -A` only — `round36_c1_verify.py:154`:
`git(d, "add", "-A")  # index only: no commit, no identity`. Confirmed:

```
$ git init -q; echo x > f; git add -A; git rev-parse HEAD
fatal: ambiguous argument 'HEAD' …
rev_parse_rc=128
```

So the battery **cannot** exercise R35-D2's stated remedy ("read committed bytes, `git show
<rev>:<path>`", lessons:87): a gate that implements it gets rc≠0 on all eight package fixtures
(unevaluated/reject), i.e. the honest hardening R35-D2 asks for is penalized. Related docstring
inaccuracy: `:9-11` says fixtures are built "from the lane's committed round-35 package bytes (never
from the working lane tree's git state)", but `copy_package` does `shutil.copy2(lane / rel, …)`
(`:60`) — working-tree bytes. At the clone measurement site the two coincide; on a dirty lane they
would not. This is the one *conditional* unfairness: P0 is fair under the frozen text, unfair under
the R35-D2 reading.

### F9 — LOW: a hanging gate crashes the counter instead of counting `unevaluated`

`run_gate` (`:208-215`) sets `timeout=300` with no `try/except`; `subprocess.TimeoutExpired`
propagates through `battery()` → `main()`, so no `FIXTURES`/`PREDICATE` line is printed and the
docstring's "other = unevaluated, never a rejection" does not hold for a hang. Similarly `OSError`.

### F10 — LOW: `r35_d3` reads `refs/heads/master`, not the resolved tip

`:293` uses `git ls-tree -r --name-only refs/heads/master` in a **jj** lane (`kengaku-shokunin/.jj`
exists). It works when the landing tip is exported as `master` (the clone's `master` = `f9efce3`),
but if the L1 lands on another bookmark/ref the check silently measures a different tree. Resolve
`HEAD` (or the clone's checked-out commit) instead.

---

## Fixture-by-fixture fairness table

| id | expect | measured content | what it actually falsifies | isolates? | fair? |
|---|---|---|---|---|---|
| P0 | accept | 22 rows, 22 distinct quotes, 22 distinct locations, 3..19 words, all 22 verbatim on the cited line; S105-107 one row each, 11 cells, tier A, mined, used-by = entry, teaches 30/23/23 words pairwise distinct; `tb2-eval/SHA256SUMS` verifies; README 42 index rows == 42 knowledge files; `## Negative space` carries an explicit `**Falsifier:**` paragraph | — | — | yes (accept is well-founded) |
| P1 | reject | 8 rows, all 1 word, **7 distinct**, still verbatim | distinctness, not word length | no | yes, but does not test length |
| P2 | reject | row 1 ×8: 1 distinct quote, 1 distinct location | duplication/distinctness | yes | yes |
| P3 | reject | 22 genuine rows + `\| a claim \| "straight quotes row" \| \`test_outputs.py:13\` \|` | parse-all-rows | yes (only fixture) | yes, but a curly-quote key also passes |
| P4 | reject | S105-107 teaches = `junk` ×3, 1 word, identical | teaches distinctness, not ≥8 words | no | yes, but does not test word count |
| P5 | reject | stub probe printing the receipt, receipt intact | probe sha pin only | yes | yes (receipt pin untested) |
| P6 | reject | `plans/round35_scratch.py` untracked after `git add -A` | clean-tree | yes | yes |
| P7 | reject | P1-style short quotes + junk teaches + stub probe + stray file | union of P1/P4/P5/P6 | composite by design | yes, adds no class |
| L1 | accept | genuine SCORECARD.md D4 line; all three spec patterns match, incl. `…md:12\` (continued on line 13) records exit 1 with \`SELFTEST green failed (1)` | — | — | yes |
| L2 | reject | the two `file:line` citations swapped | citation binding (patterns 1 **and** 2 break) | yes | yes |
| L3 | reject | `SELFTEST green failed` → `SELFTEST red` (substring present in the genuine line, so the mutation is real) | harness token (pattern 2 only) | yes | yes |
| L4 | accept | genuine round-34.md erratum; quote verbatim in `nec-s091-reopen.html` (60,335 B, raw line 276); manifest self-consistent | — | — | yes |
| L5 | reject | `is present` → `is not present` | negation | yes | yes |
| L6 | reject | genuine line over `<html>quote</html>` with the original manifest copied | capture integrity (manifest digest mismatch; quote also off line 276 and size differs) | yes | yes |

Unconditional unfair fixtures: **0**. Conditional: **1** (P0, under a gate that reads committed
bytes per R35-D2 — F8). Operational unfairness: R35-D1's `--rerun` to a gate that executes the
spec's `probe_cmd` verbatim (F6).

---

## Residual risk and verification gaps

- The C1 predicate can be passed today by (a) an identity gate, (b) a name-keyed gate, (c) a gate
  omitting nine clauses, and (d) a one-field ledger edit. Only (d) requires no gate at all. C1's
  calibration evidence should be read as "rejects 11 specific byte deviations and the 6 directional
  line mutations", not "implements the hardened semantics".
- I did not audit the L1's eventual `plans/pkg_gate.py` (absent at every tip I read); a wave-2 seat
  must re-run F2, F3 and a no-word-bounds gate against the landed file.
- I did not verify the 912 round-28 nested paths (named as a limit at freeze) or the D3/D4 honest
  closure (L1 work: move 21 round-34 paths, write the round-36 `## Gate` erratum — the frozen
  recount is well-founded: `parts [13, 23, 1] sum 37 denominator 38` from
  `corpus/evidence/round36/toolathlon-package.md`, digest `00132ab0…` matching the freeze list).
- Environment fact: `/usr/bin/python3` has no Biopython; `uv run --no-project --with
  biopython==1.85` reproduces `corpus/evidence/round35/tb2-grader-probe.txt` byte-identically. A
  receipt produced by any other runtime is not the canonical one.

VERDICT: battery-review-8-unfair-1-gameable
