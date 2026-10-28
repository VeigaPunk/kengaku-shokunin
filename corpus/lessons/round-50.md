# Round 50 — honest-geometry instrument, fence repair, self-assessment pointer audit (2026-10-28)

L1 `KengakuR50`, hyaku run 11. Stage-1 freeze `3b02d573d58cc6d2e0d27ef92ac0815354912252`; instrument repair
`c3372a9`; C2 corrections `822f3b7`. One v2 wave of 72 seats was validated and prepared
(`.ufo/waves/round-50/w1-spec.json`, `w1-dispatch.json`, policy v2 accepted, 34 attack roles); the inline dispatcher
mounted 40 seats and produced 50+ seat outputs before the round closed — **no `WAVE-DONE` marker was written**, so
the wave is reported as partially dispatched, not as a settled falsification wave.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **landing** — a fixture test shell `export`ed `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null` into the shared shell; the lane's git credential helper lives in the global config, so every `jj-lane.sh` push failed with the opaque `External git program failed:` and exit 3 until the variables were unset | `.ufo/waves/round-50/claims/` push attempts 14:16–14:18; first landed `f7281bc` at 14:19 only after `unset` | none — no criterion covered shell hygiene; the wave `context` now carries the rule | fixture git env is set per command (`env VAR=… git …`) or in a subshell, never `export`ed; the wave context carries the warning. Shown able to fail: the same push command exited 3 with the leaked env and `landed f7281bc…` without it |
| **landing** — rounds 48 and 49 froze counters in a "counting command" cell that no commit ever held, so their verdicts were unverifiable at the tip for two rounds | `SCORECARD.md` §Round 50 corrections; audit `plans/round50_c2_audit.py` at `71f5f5f`: `unresolved=12` | the new `corpus/QUALITY.md` Q41 (pointer = routed finding with a closing commit) | every counter a row names exists at the tip before the row lands; the audit command is the gate. Shown able to fail: `unresolved=12` at `71f5f5f`, `unresolved=0` after the corrections block |
| **survivor / scope** — the carried r49 mutant battery (23 inline diffs against the r49 candidate) is not a battery for the repaired fence: on the shipped repair 4 of 23 change the verdict vector and 7 do not apply | `.ufo/waves/round-50/w1/R50C1ExecMutRebase-witness.tsv`; L1 re-derivation run | QUALITY Q38 (a frozen mutant's kill direction is witnessed, not assumed) | the frozen battery holds only rows whose kill is witnessed on the shipped fence; unwitnessed rows are dropped and listed. Shown able to fail: the carried battery prints `caught=4 … verdict=unmet` |

## Gate

Candidates opened this round (all in `corpus/SOURCES.md`), each fetched 2026-10-28 from
`https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/<doc>.adoc` at tag `v2.56.0`, captures kept at
`corpus/evidence/round50/*.adoc`:

| row | source | quote (≤25 words) and location | verdict |
|---|---|---|---|
| S173 | gitrepository-layout | `:80-83` "This file records paths to alternate object stores that this object store borrows objects from, one pathname per line." | **ADMIT** — documents the `alternates` shape the n22 class uses |
| S174 | git-init | `:69-72` "create a text file there containing the path to the actual repository. This file acts as a filesystem-agnostic Git symbolic link to the" | **ADMIT** — documents `--separate-git-dir`, the n21 class |
| S175 | git-worktree | `:285-292` "A text file containing the absolute path back to the .git file that points to here." | **ADMIT** — documents the worktree `gitdir` back-pointer |
| S176 | git-replace | `:20-24` "Adds a 'replace' reference in `refs/replace/` namespace." / "The name of the 'replace' reference is the SHA-1 of the object that is replaced." | **ADMIT** — documents `refs/replace` as a ref whose name is an object id |
| S177 | git-fetch | `:42-43` "The names of refs that are fetched, together with the object names they point at, are written to `.git/FETCH_HEAD`" | **ADMIT** — documents the fetch write the plain-init allowlist missed |
| — | `tbench.ai` task hub / live leaderboard (carried lead) | exact historical path returns HTTP 404; the current pages publish no pinned per-task spec | **REJECT** — mutable, unpinned; flip only on a stable versioned endpoint with a digest |

Rows touched old→new: none (no `status`, `recheck` or `used-by` change to an existing row). Registry 165 → 170
rows; tier A=146/B=22/C=2; status mined=154/queued=8/rejected=8;
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` exit 0 before and after.

## Assimilation (considerthese)

Adopted proposal 1 of `considerthese/2026-10-26.md` (2026-10-26): every routed finding is a row with an id, a
status and a closing commit rather than a sentence routed to a round that never reads it. Landed as QUALITY Q41
and as the `SUPERSEDED … -> target|never-landed` corrections block in `SCORECARD.md` (12 rows). `merge/kengaku/`:
not adopted this round — the claims are internal instruments and the package's staged entries are benchmark facts
outside them; the choice is recorded in the report.

## Claim evidence and honest verdicts

- **R50-C1 — novelty, ADMITTED on the predicate.** `plans/round50_c1_verify.py` on the shipped fence at the S3
  tip prints `HONEST fixtures=126 admitted=126 refused=0 error=0`, `REFUSALS total=20 clean=20 leaked=0`,
  `SEALED total=12 clean=12 leaked=0` + `SEALED total=18 clean=18 leaked=0`, `MUTANTS … verdict=met`,
  `PREDICATE R50-C1 pass`, exit 0 (receipt `corpus/evidence/round50/c1-receipt.txt`). Before: the base fence
  `05d5fe03…` printed `HONEST admitted=113 refused=13` (control `.ufo/waves/round-50/claims/c1-control-do-nothing.txt`).
- **R50-C2 — calibration, ADMITTED.** `plans/round50_c2_audit.py --lane .` at the tip prints
  `POINTERS total … unresolved=0`, exit 0; at `71f5f5f` it printed `unresolved=12`, exit 1, and `--selftest`
  proves the check can fail (`.ufo/waves/round-50/claims/c2-before.txt`, `c2-selftest.txt`).
