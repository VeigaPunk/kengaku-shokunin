# RevF4 — recheck of W3ReviewKengaku F4 (S023 rejection non-sequitur) at lane tip 3f371d2

Axes (godspeed): calibration (registry reason hygiene, Q9 criteria) + novelty (coverage of the
correction path). Read-only; nothing mutated.

## Verdict: FIXED — at `e21f9ea` "round-24: post-review fixes", exactly by the prescribed mechanism

1. **Superseding row present.** `git -C <lane> log -S 'supersedes S023' --oneline --all` →
   `e21f9ea`, `a42bb40` (spotcheck lesson). `corpus/SOURCES.md:48` = S026 (rejected, tier C),
   teaches opens `supersedes S023 — REJECTED: ... S006 does not bear on it — S006 reports Pro
   task validity (~30% broken tasks), a separate property`. Matches the F4 prescription
   (kengaku-review.md:133: "correct it with a new row whose teaches opens `supersedes S023 —`").
   The S023 row itself is untouched at `corpus/SOURCES.md:45` — append-only respected
   (`git show e21f9ea -- corpus/SOURCES.md | grep -c '^-|'` = 21, and every deleted row is a
   recheck-normalized rewrite of S020–S022/S024/S025, not S023).
2. **Receipted.** `corpus/evidence/round24-sources/gate.md:34` adds the S026 receipt: sha256
   `171087c5…673b` (128,773 bytes), quote "We use code that models haven't been trained on.
   This is sourced from public codebases governed by strong copyleft licenses (e.g., GPL)",
   location Data Contamination → The Solution. gate.md grew exactly +1 line in `e21f9ea`.
3. **Learned, as the review's §7 demanded** ("discernment becomes harmed if F4 is not learned").
   `corpus/lessons/round-24.md:31` = M21 (DISC: reason cited S006, a different property; caught
   only by the non-author spot-check) → new criterion `corpus/QUALITY.md:67-73` **Q9**: "A
   correct verdict with a wrong reason is a gate failure." (M22→Q10 at :75 also landed.)
4. **Recorded both sides.** `corpus/lessons/round-24.md:123-137` documents the spot-check
   disagree + new row + the 21 recheck-cell normalizations (old→new, contract rule 2);
   `corpus/lessons/round-24-verifier-spotcheck.md:13` and `:17` record the verdict and the
   ADMITTED-after-`e21f9ea` adjudication. After `e21f9ea`, only `a42bb40` touches these files
   (it adds the spotcheck lesson); no later commit re-edited the S023/S026 rows.
5. **RESIDUAL (low severity) — search-log line still carries the non-sequitur unqualified.**
   `corpus/SOURCES.md:63` (round-24 Search log) still reads: "Exclusion reason: vendor
   marketing; its contamination-resistance claim is **contradicted by** a later OpenAI
   self-reported audit (S006: ~30% broken tasks)." F4 cited both `:45` and `:62`; the fix
   addressed the registry row (superseding row) but left this historical line as-is. It is
   corrected in the chain (S026, M21, Q9, spotcheck record) but taken alone it asserts the
   retracted relation. No admitted claim cites S023 (used-by `—`), so nothing downstream
   inherits the error.
6. **Smallest append-only fix, if the operator wants the residual closed this round** (one
   appended Search-log line, dated, no in-place edits, no registry cells touched):
   `Scale SWE-Bench Pro entry superseded: its 2026-10-19 exclusion reason cited S006 (Pro task
   validity), which does not bear on Scale's contamination-resistance claim — see S026 and
   QUALITY Q9.` Alternatively a one-line note in the round-25 lesson's `## Gate`. Not required
   for round-25 admission by F4's own terms (the prescription was the new row; it landed).
7. **Flip conditions (informational).** S023's flip ("peer-reviewed paper plus an independent
   task-level audit surviving external re-annotation") is superseded by S026's operative flip
   ("a peer-reviewed paper or an independent audit testing Pro for contamination, e.g.
   gold-patch recall probes on the public set"). Consistent with supersession semantics.

## Checks run

- `git -C <lane> log -S 'supersedes S023' --oneline --all` → e21f9ea, a42bb40 (fixing commit).
- `git -C <lane> show e21f9ea --stat` (7 files, +118/−21) and full `corpus/SOURCES.md` diff.
- `grep -n S023` over `corpus/SOURCES.md`, `corpus/lessons/*.md`, `LOG.md` — every remaining
  hit is a historical record correctly annotated by the chain above; LOG.md has none.

No installs. No fix applied (read-only seat). Residual risk: only finding 5; a future reader
quoting the search-log line without following S026 would re-import the non-sequitur.

VERDICT: F4 is FIXED at e21f9ea — superseding row S026 (SOURCES.md:48) + receipt (gate.md:34) + lesson M21 + QUALITY Q9, append-only respected; sole residual is the stale search-log wording at corpus/SOURCES.md:63, closable with one appended dated log line.
