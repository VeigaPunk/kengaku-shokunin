# F35CritC2 — falsify C2 (persistent routed-defect ledger, D1–D5 closed) at landing tip

Seat: `F35CritC2` (critic, wave 2). Target: `dfee6fff631ebc5f623ba4506e5c7992a215401c`
(branch master). Frozen claims: `plans/round-35-claims.md` C2 section (freeze `11d64530`).
All lane reads were read-only counters in the live lane (allowed); every counterexample ran in a
throwaway fixture clone (`mktemp -d /tmp/k35f-XXXX`, sparse `--shared` clone at the tip, toplevel
verified, deleted after).

## Baseline: frozen predicate holds at tip

`python3 plans/defect_ledger.py --lane .` in the live lane:

```
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
EXIT=0
```

Pristine run in a fresh clone prints the identical line. The literal predicate passes.

## F1 — D4 check is still pure token co-occurrence; a false correction line passes at the tip

Checker (`plans/defect_ledger.py:82-83`) accepts any single SCORECARD line starting
`- **D4 correction (round 34 C2):**` that contains the four substrings
`R34C2CounterDraft.md:8`, `cases=10 failed=0`, `R34MutC2Harness.md:12`, `SELFTEST green failed`
— order and direction never asserted. The committed observation is:
`build/R34C2CounterDraft.md:8` → `SELFTEST cases=10 failed=0` (draft green);
`build/R34MutC2Harness.md:12-13` → exit 1, `SELFTEST green failed (1)` (harness red).
So the *true* correction must say "draft green, harness red".

Counterexample at the landing tip (fixture clone, replaced the one correction line):

```
- **D4 correction (round 34 C2):** the counter draft's selftest was red (SELFTEST green failed at R34C2CounterDraft.md:8, cases=10 failed=0 at R34MutC2Harness.md:12)
```

This asserts the exact opposite of the record. Counter output:

```
R34-D4 status=closed observed=pass agree=yes correction_lines=1
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
EXIT=0
```

The D4 defect (misattribution) is textually unfixed while the check certifies the closure. Same
hole as wave-1 `R35CritC2.md` §2, reproduced at the landing tip.

## F2 — D5 check is still token co-occurrence; a "not present" erratum passes

Checker (`defect_ledger.py:101`) requires one line starting `Erratum (round 35):` containing
`nec-s091-reopen.html` and the substring `present` — which matches inside `not present`.
Counterexample at the landing tip (fixture clone, replaced the erratum line):

```
Erratum (round 35): the staged S091 quote is not present in nec-s091-reopen.html
```

Counter output:

```
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
EXIT=0
```

The erratum states the refusal reason was correct (quote absent) — the negation of the defect
closure — and the check certifies it. Same hole as wave-1 `R35CritC2.md` §3. Secondary gap
unchanged: the observation source `nec-s091-reopen.html` (writable lane content, no hash pin in
the check) also allows manufacturing a pass by editing the capture.

## F3 — D1 remains a vacuous working-tree check, blind to later rounds

`r34_d1` runs `git ls-files --others --exclude-standard -- plans/round34_c1_verify.py
plans/round34_defects.py plans/round34_mutate.py .ufo/waves/round-34` — a workspace query, not
repo bytes (contradicting the checker docstring's "observation computed … from repo bytes").
In any clean checkout it passes without any repair (fixture pristine run: `untracked=0`,
agree=yes). In the live lane today, 61 untracked paths exist — all outside D1's scope:
`git ls-files --others --exclude-standard | wc -l` → 61 vs scoped count 0. So the same defect
class (uncommitted round work) is invisible for the current round's wave tree; D1 only ever
certifies "this run's workspace is clean of round-34 leftovers".

## F4 — D2 close is symptom-honest but process-blind; history keeps all 109,413 paths

Commit `dfcd294` deleted exactly 109,413 committed paths under the three roots
(`mut-entries-scratch` 106,323; `build/R34MutRegistry/mirror` 515; `build/R34MutRegistry/mut`
2,575) = 1,775,084,942 logical bytes (≈1.69 GiB). At the tip, `committed_mirror_paths=0`.

History keeps every one of them, and the check does not care:
- `git log --oneline --all -- .ufo/waves/round-34/mut-entries-scratch` → `dfcd294`,
  `0cbfabd`, `346850e`, `5665913` … (still reachable ancestors of master).
- Blob recoverable after deletion: `git cat-file -t ee636588c…` → blob (round-17 report copy).
- Object-store cost unchanged: `git count-objects -vH` → count 7200, size-pack 1.14 MiB
  (mirrors deduplicated/compressed; deleting from the tip freed no pack bytes).
- 158 deleted paths carry 36 distinct blobs absent from any path in the current HEAD tree
  (6,701,152 logical bytes) — mostly older/mutated corpus snapshots (e.g.
  `mirror/corpus/QUALITY.md`, `mut/m1-column-count/corpus/README.md`) and round-17-era scratch;
  reachable only via git history, no tree path. Live evidence duplicates (e.g.
  `mirror/corpus/evidence/attrib-r21-ds-trials.log` blob == `corpus/evidence/…` blob,
  identical) survived the deletion.

The routed prescription (`round-34-verifier-spotcheck.md:76`): "mutants must run in a temp
clone outside the repo and commit only receipts; record a lesson and a guard". The counter has no
clause for lesson or guard — a tip-only deletion with no lesson passes identically. (The round did
record a lesson at `corpus/lessons/round-35.md:26` and Q23 at
`build/R34Considerthese/q23.md:17`, but D2 does not measure either.) So the close verifies the
present-state symptom, not the anti-recurrence half; on the question "honest?", it is honest
about the tip count and normal git semantics (history retention is inherent; a history rewrite
would be dishonest), and incomplete about the process prescription.

## F5 — The calibration count is mechanically §9-shaped but cannot tell truth from falsity on D4/D5

Addendum §9 (`scripts/hyaku/lane-addendum.md:282-283`): "A calibration claim must count
mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state. It
cannot be an assertion." The ledger counts mismatches in both directions (closed+fail, open+pass)
— the right shape — and D4 ties one row back to SCORECARD text. But the self-assessment the
mismatch count reads is the ledger's own `status` field (a new surface the lane created), and for
D4/D5 the observation is substring presence, not truthfulness. F1/F2 show a *false* self-
assessment yields `mismatches=0`. The instrument is calibrated for presence, not for agreement of
text with record; the calibration value the claim asserts (closing mismatches between
self-assessment and observed state) is therefore not established by the counter on those rows.

## Impacted axes

- **calibration** (primary): D4/D5 false-positive closures reproduce at the landing tip (F1/F2);
  D1 not re-derivable from committed bytes (F3); D2 process half unmeasured (F4).
- **operability**: no material harm from the deletion — duplicates survived; HEAD tree shrank
  109,413 → 9,193 files; the 158 unique-blob paths remain recoverable via history. The D1 scope
  gap leaves current-round untracked work (61 files) observable only outside the ledger.
- **depth**: check semantics remain token-level, not directional; no truthfulness claim is
  warranted by the counter (SCORECARD round-35 C2 row itself discloses the D4/D5 and D1 limits).

**VERDICT: c2-critic-falls-5-findings**
