# R49C2RevAdmission — tag-coverage and order-proof adjudication from committed bytes

seat: R49C2RevAdmission (reviewer), serving R49-C2 (coverage)
date: 2026-10-28
lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin
REV measured (content): `9d2900af41e4d1fc6022eff99010436fde6dbd93` — stage-1 freeze, committed
2026-10-28T09:14:40-03:00, ancestor of lane tip `af88aab1…` (tip adds only the w1 spec/dispatch evidence).
Re-read in a `git clone --shared` clone at `HEAD=9d2900a…`; second worktree pinned at `2c81f38a` (r46
spot-check tip) for the order-gate precedent run. No scored counter run: `plans/round49_c2_verify.py` is
absent at the freeze (a stage-2 artifact by design). Permitted pre-receipt operations only (`--dry`,
read-only git inspection, `order_check`).

## Scope of the item

Adjudicate, from committed bytes only: (i) whether **every frozen tag has a violating case**, and
(ii) whether **the order proof holds** — the claim's own words, not the titles of the rows.

## Commands run and verbatim evidence

### A. Freeze and surface (predates measurement — precondition met)

```
git cat-file -t 9d2900af…           -> commit
git log -1 --format='%H %cI %s'     -> 9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00
                                       "round-49: stage-1 freeze of C1 … and C2 …"
git merge-base --is-ancestor 9d2900af… HEAD -> exit 0 (ancestor of tip)
```

Presence census at `9d2900a`:

| path | state |
|---|---|
| `plans/polyglot_c_py_probe.py` | PRESENT (r46 revision, 526 lines) |
| `plans/round46_c3_verify.py` | PRESENT (913 lines; the v4 base counter to be imported/pinned) |
| `plans/order_check.py` | PRESENT (214 lines) |
| `plans/round49_c2_verify.py`, `plans/mutants49/plan.json`, `plans/pkg-spec-r49.json` | **absent** — stage-2 artifacts, correctly not yet committed |
| `corpus/evidence/round49/` | **absent** — the round-49 dry table/receipt paths are new |

`git log --all --oneline -- corpus/evidence/round49/ plans/mutants49/` → **zero commits** (verbatim: empty).

### B. Tag coverage — the V7 precondition (fail, on committed bytes)

Frozen tag set (probe `TAGS`, `polyglot_c_py_probe.py:90-98`) = dry-table `TAG` lines = 7 tags on 5 lines:
`single-file :1`, `python-run :3`, `c-build :5`, `both-print :7`, `fib-kth :7`, `stdout-only :7`,
`toolchain :9`. A "violating case" is the counter's own definition: a receipt `CASE` line whose
`violates=` token names the tag (`round46_c3_verify.py:399-401` → `{tag}: no receipt case violates it`).

Union of `violates=` tokens, computed over all three committed sources independently:

- probe `CASES` tuples: `{c-build, fib-kth, python-run, single-file, stdout-only}`
- frozen dry table (`corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`, 18 CASE lines): identical
- executed receipt (`corpus/evidence/round46/polyglot-c-py-probe.txt`, 18 CASE `observed=` lines): identical

**`both-print` and `toolchain` are cited by zero cases in every committed source.** The precondition
"every frozen tag has a violating case" is FALSE on committed bytes — the routed defect
(`round-48-verifier-spotcheck.md` §3 `w1/R48C2ExecTagInv.md`: "5/7 frozen tags have executable violating
cases") re-confirmed byte-for-byte. The r46 landing's own verdict names it:
`.ufo/waves/round-46/integrate/c3-landing.txt` → `tags missing=['both-print', 'toolchain']`.

Under the committed MAP_ROW (`round46_c3_verify.py:135`, labels `enforced|unenforced|partly`), the
entry's two `not exercised` rows (`tb2-polyglot-c-py-grader.md:86,89`) also trip the "unparsed row" arm —
5 of 7 rows parse. So V7 fails on committed bytes both ways: unparseable map rows and missing cases.

**Feasibility of the frozen fix (adjudicated, not asserted):** both tags admit honest violating cases.
`both-print`: a polyglot whose one side writes nothing to stdout (e.g. C side `fprintf(stderr,…)` only)
fails the printed-value check for one runtime while the other still prints — violating exactly "Both of
these should print to stdout". `toolchain`: the probe itself binds host `gcc`/`python3`
(`probe:49-52,84-85`) against the frozen `python3 3.12.3 and gcc 13.2.0`; any passing case may carry
`violates=toolchain` as an unseen-requirement token per the committed rule (`probe:45-47`: "tags on a
passing case name a requirement the grader does not see"). No infrastructure beyond the committed probe
machinery is required — the amendment is a case-table/dry-table change, exactly what the freeze allows.

### C. Order proof — the V8 mechanism (satisfiable, with one named residual)

Committed mechanism = `plans/order_check.py` (frozen read-only input) + the amended V8 delta
(claims lines 117-122: first-commit == stage-3 commit ∧ descendant of stage-2 ∧ receipt carries
`CASE … observed=`).

1. **Receipt path is order-clean.** `corpus/evidence/round49/polyglot-c-py-probe.txt` has zero history;
   its first-commit cannot be anything but the stage-3 commit that creates it, which is by construction
   a descendant of the stage-2 commit. The `CASE … observed=` requirement is automatic — the probe
   emits exactly that line shape (`probe:514`).
2. **Claims-dir is clean at the freeze.** `.ufo/waves/round-49/claims/` absent →
   `git rev-list --all -- .ufo/waves/round-49/claims/` empty → `scan_claims` starts from zero blobs.
3. **Mechanism proved on committed precedent.** Run on a worktree at r46 tip `2c81f38a` (read-only):

```
python3 plans/order_check.py --lane $D --claims plans/round-46-claims.md \
    --receipt corpus/evidence/round46/polyglot-c-py-probe.txt
ORDER claims=plans/round-46-claims.md round=46 freeze=fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f
ORDER receipt=corpus/evidence/round46/polyglot-c-py-probe.txt receipt_commit=8d7f74ce63c25ad200c69fe0d90158cc7099def6
ORDER scanned commits=2 file_entries=25 distinct_blobs=17
ORDER HIT .ufo/waves/round-46/claims/control-c3-echo.txt@4fdeebaa546c:15 kind=gate-p10 `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`
ORDER FAIL probe-executed-before-receipt hits=1
ORDER RESULT FAIL     (exit 1)
```

   The gate correctly re-derives the r46 V8 failure from committed bytes: one claims-dir blob carried a
   probe-executed P10 line. This is exactly the defect class the r49 P10-disabled-controls rule exists to
   prevent.

4. **Residual the wave must close (verification gap, not a defect of the freeze):**
   `order_check.py` itself cannot test "receipt's first-commit IS the stage-3 commit" — it only knows
   freeze-not-containing-receipt, receipt-not-before-claims, and the claims-dir blob scan. The new literal
   rule lives only in the claims text; `round49_c2_verify.py` must implement it explicitly
   (`git log --diff-filter=A` on the receipt path == the stage-3 commit ∧ ancestry). Wave authors must
   also keep every committed `claims/` blob free of `P10\s+(DEFECT|ok)` lines other than
   `P10 DEFECT receipt unreadable…` (`order_check.py:53-60`) and free of `CASE … observed=` lines —
   dry-table `CASE … predicted=` lines are safe. A P10-disabled leg printing `P10 DEFECT <anything else>`
   re-creates the r46 hit.

### D. Consistency check on the freeze's own evidence

`python3 plans/polyglot_c_py_probe.py --lane . --dry` (exit 0) is byte-equal to
`corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` — the committed probe is the committed
table, so the stage-2 amendment delta is real work on this file, not a no-op.

## Limits

- No scored run was made or attempted: the v4 counter does not exist in the tree; nothing was mutated in
  the lane. This adjudicates committed-byte properties, not the future landing.
- The order proof's *satisfiability* is proved; its *satisfaction* is unadjudicable until stage-2/stage-3
  commits exist (receipt commit, amended counter) — flagged as the one item needing re-verification at
  landing review.
- No external source was opened this seat; the only re-opened artifact is the lane's own pinned S166
  capture, already gated. Committed bytes cited: `tb2-polyglot-c-py-grader.md:86` located quote
  "no frozen case violates it" (4 words, accessed 2026-10-28).

## VERDICT

**Tag coverage: FALSE on committed bytes — `both-print` and `toolchain` carry no violating case in any
committed table/receipt (routed defect 3 re-confirmed at byte level); satisfiable via the declared
stage-2 probe amendment, which is feasible on the committed machinery.
Order proof: MECHANICALLY SATISFIABLE — receipt path virgin (first-commit ≡ stage-3 by construction),
claims-dir clean, gate mechanism validated on the r46 precedent; the new "first-commit == stage-3" test
must be implemented by the absent stage-2 counter (named residual, not a freeze defect).
Not an admission of R49-C2; a settled adjudication of the two named preconditions.**
