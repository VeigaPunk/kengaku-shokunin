# Seat report — M5LedgerDeclMutants (kengaku round 55, wave 1)

Role: mutation-tester. Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Frozen base tip `798f5e9ef30ef39291295565209b65a17343c00e` (claims commit `80afa613…`).
Scratch root (deleted before yield): `/fast/scratch/hyaku/kengaku-r55/M5LedgerDeclMutants/`.

## What I ran

Setup (all read-only w.r.t. the lane; **no mutating git/jj command** was run anywhere — no add/commit/
push/stash/checkout/reset):

```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin worktree add --detach \
    /fast/scratch/hyaku/kengaku-r55/M5LedgerDeclMutants/wt 798f5e9ef30ef39291295565209b65a17343c00e   # exit 0
git clone --shared --quiet wt src-pristine            # exit 0, HEAD=798f5e9e…, clean
python3 mk_mutants.py                                 # exit 0 — builds 4 mutant ledgers + 1 inert control
```

Mutants are copies of `plans/round54-entrytruth.json` placed inside **separate clones of the base tip**;
the pristine lane worktree was never written (ledger sha256 `40a77a3b…` before and after; `git status
--porcelain` empty).

Detector (identical command in every arm; the r54 counter reads the ledger from `--source`):

```
python3 wt/plans/round54_c2_entrytruth.py --lane src-pristine --source <arm-clone> --work work/<arm> --jobs 8
```

| # | arm | ledger sha256 | exit | key output |
|---|---|---|---|---|
| 0 | `--dry` pristine | `40a77a3b…` | 0 | `ROWS registry=78 ledger=78 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1` |
| 1 | `--dry` M1 | `0808512d…` | 1 | `bad_decl=1` + `BAD-DECL config-projection` |
| 2 | `--dry` M2 | `ab1d7aac…` | 0 | static legs clean (well-formed false-red declaration) |
| 3 | `--dry` M3 | `ce25f6d0…` | 1 | `missing=1 extra=0` + `MISSING catalog-probe` |
| 4 | `--dry` M4 | `a5663f84…` | 1 | `LEDGER ledger unreadable: duplicate JSON key`, `ledger=0`, 78×`MISSING` |
| 5 | `--dry` DC control | `2130702a…` | 0 | static legs clean (inert edit) |
| 6 | full **pristine baseline** | `40a77a3b…` | **1** | `PREDICATE R54-C2 fail`; `LAUNDERED defect-ledger`, `LAUNDERED round36-c1-battery`, `LAUNDERED round52-c2`, `EVIDENCE-MISSING round35-c1-coverage`; `RUN executed=78 timeout=0 mismatched=0 evidence_missing=1 laundered=3`; `TIPSTATE declared 62/16 vs observed 59/19` |
| 7 | full **M1** | `0808512d…` | 1 | **new** `BAD-DECL config-projection`; `bad_decl=1`; `executed=77`; `observed_green=58` |
| 8 | full **M2** | `ab1d7aac…` | 1 | **new** `MISMATCH grader-perturb declared exit=1 observed exit=0`; `mismatched=1`; `TIPSTATE declared 61/17 vs observed 59/19` |
| 9 | full **M3** | `ce25f6d0…` | 1 | **new** `MISSING catalog-probe`; `missing=1 extra=0`; `executed=77` |
| 10 | full **M4** | `a5663f84…` | 1 | **new** `LEDGER ledger unreadable: duplicate JSON key`; `ledger=0`; 78×`MISSING`; **no `SOURCE`/`RUN`/`TIPSTATE` line (nothing executed)** |
| 11 | full **DC control** | `2130702a…` | 1 | defect set **identical to the baseline**; only difference `clean=NO` (vs `clean=yes`) |
| 12 | `python3 restore.py` (5 trees) | — | 0 | every tree: `after=40a77a3b… restored=True git_status=''` |
| 13–16 | full detector on the **restored** M1/M2/M3/M4 trees | `40a77a3b…` | 1 each | output **byte-identical to the baseline** (incl. `clean=yes`); every mutant signal gone |

Wall-clock per full arm ≈ 218–240 s (78 rows, `--jobs 8`); ~4 min each, 11 full runs total.

## Files written (lane paths)

* `.ufo/waves/round-55/w1/M5LedgerDeclMutants.md` — scoped findings (the `Report:` trailer path)
* `.ufo/waves/round-55/w1/M5LedgerDeclMutants/mutants.md` — full observed outputs, hashes, verdicts
* `.ufo/waves/round-55/w1/M5LedgerDeclMutants/report.md` — this report

Nothing else in the lane was created, modified or deleted. Scratch deleted at end of seat (worktree
registration removed first, so the lane's `.git/worktrees` is clean).

## Defects found

1. **Four false declarations already in the r54 ledger at the frozen base tip** (measured by the frozen r54
   counter on a clean clone): `defect-ledger` (green/0, observed exit 1), `round36-c1-battery` (green/0,
   observed exit 1), `round52-c2` (green/0, observed exit 1 — the r52 registry regression R55-C1 repairs),
   `round35-c1-coverage` (red/1, declared evidence fragment absent from the output). The claim's correction
   list names only the last two; `defect-ledger` and `round36-c1-battery` are unnamed and are still declared
   `green/0` in the lane's current working-tree ledger (83 rows, checked after the L1's `248a42b8`).
   R55-C2's after-predicate demands `laundered=0 evidence_missing=0` and `TIPSTATE declared == observed`,
   so these two rows must be re-declared from observed behaviour at the landing revision (ledger **data**
   fix; no rule change).
2. **Direction corrections to the seat brief** (observed): a false-**red** declaration fires `MISMATCH`, not
   `LAUNDERED`; a deleted ledger row fires `MISSING` (registry→ledger direction), not `EXTRA`; a duplicate
   JSON key surfaces as `LEDGER ledger unreadable`, not via the `duplicate_names=0` field.
3. **The bogus evidence fragment of a false-red declaration is never tested**: the exit mismatch
   short-circuits before the evidence leg, so `evidence_missing` stays 0 for that row. The r54 counter's
   evidence leg only ever runs on rows whose declared exit already matches the observed exit.
4. **A malformed declaration makes a row unmeasured rather than measured-and-wrong**: M1's bad row is
   excluded from execution (`executed=77`, `observed_green` 59→58); the `executed == n_reg` conjunct is what
   catches the exclusion, so nothing is laundered — but the row's true state is never established.
5. **Reporting nit in the frozen r54 counter** (reported, not fixed — the counter is frozen): its
   `duplicate_names=N` field counts duplicate SKILL.md *registry* rows, not duplicate ledger JSON keys, so
   the JSON-duplicate class is invisible to a reader scanning that field. The ledger still fails closed.

## Dead ends / notes

* A bounded arm with `--timeout 45` was started and then cancelled (the canonical unbounded arm finished in
  3 m 53 s — the `uv run --with biopython==1.85` row resolves from uv's cache, so no arm needed bounding).
  Cancelled rather than left to burn host CPU.
* The first M4 full run was quoted from a `head -12`-truncated pipe and its `PIPESTATUS` had been clobbered
  by a second pipeline; M4 was re-run capturing the whole output in a shell variable — the re-run is the
  quoted evidence (arm 10 above).
* `git clone --shared` of a detached-HEAD worktree prints "Note: switching to …" on stderr; that noise is
  filtered out of the receipts (the counter's own output is stdout).
* Tool installs: **none** (no `uv tool install`, no pacman, no binaries added to any PATH directory).
* Network: **no** network use; the counters ran fully offline. `uv` used its local cache for biopython.
* During the seat the lane HEAD moved `80afa613…` → `248a42b8` ("LOG honest-stop entry … released un-settled
  at operator wrap-up") and other seats' uncommitted ledger corrections appeared in the lane working tree.
  Those are not mine: my scratch clones were cut from the frozen base tip `798f5e9e…` and the lane's own
  files were only ever read.

## Checks the integrator (main agent) should run

1. At the landing revision, re-measure `defect-ledger` and `round36-c1-battery` with the R55-C2 counter and
   re-declare them from observed behaviour (ledger data fix) — otherwise `laundered≥2` and the after-predicate
   fails; the base-tip measurements in `mutants.md` are the evidence to compare against.
2. Re-run the four mutants against the *new* counter `plans/round55_c2_entryargv.py` at the landing revision
   (my arms were measured against the frozen r54 counter at the base tip, per the seat brief) — the new
   counter reuses the r54 static legs, so `bad_decl` / `MISSING` / `LEDGER unreadable` should still fire, and
   its L1–L3 binding legs are the ones that must not miss ledger-side tampering.
