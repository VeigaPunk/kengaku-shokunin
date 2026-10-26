# R39ConnSibling — sibling-overlap scan, kengaku round 39 wave 1

Seat: R39ConnSibling (connector, leaf — no subagent dispatch). Read-only scan; no
fixtures, no installs, no lane writes anywhere. Frozen claims read in full first:
`plans/round-39-claims.md` (C1 = gate mutation-battery calibration M01–M07; C2 =
pinned TB2 `git-leak-recovery` grader coverage, 25-case receipt).

## Axes

Adjacency (this seat's judged axis), coverage (the round's chosen axis; C2 is judged
on its counter). Calibration/operability are touched only where a sibling's measured
evidence can sharpen a frozen limit without editing anything frozen.

## Round surfaces scanned for

1. git secret recovery/removal graders; 2. git object-store forensics; 3. bwrap grader
sandboxes; 4. gate mutation batteries. Siblings: all 20 other `*-shokunin` lanes,
read-only (`PROVINCE.md`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`,
`corpus/knowledge/`), prioritizing kagi (secrets/vault), kasegi (security research),
souji (repo hygiene — the fleet's git tooling lane), tameshi (verification-fixture
craft), kumitate, revenger, kaidoku, chousa, mado.

## Overlaps found (6)

### 1. Secret-removal procedure ownership — souji refuses, routes; kagi owns doctrine → DEFER

- `souji-shokunin/PROVINCE.md:84-85`: "Credential-bearing history (git-filter-repo
  `--sensitive-data-removal`) routes to kagi-shokunin and the operator; souji never
  rewrites history."
- `souji-shokunin/corpus/SOURCES.md:36` (S015, GitHub "Removing sensitive data"):
  teaches "revoke or rotate a leaked secret first; a git-filter-repo rewrite needs
  coordination and has side effects; souji routes this work and never does it" (status
  `queued`, opened 2026-10-19).
- `souji-shokunin/corpus/SOURCES.md:33` (S012, git-filter-repo(1) 2.47.0:
  `--analyze` writes under `.git/filter-repo/` even when it does not modify; fresh-clone
  safety check; `--force` habit removes it). `:53` (S032, git-filter-branch) is a
  REJECTED row: git's own WARNING + history rewrite refused.
- `kagi-shokunin/PROVINCE.md:65-67`: kagi's Core is 1Password custody, SOPS/age
  rotation, Vault/OpenBao clocks; "secret-scanning detection vs verification" is kagi
  Frontier, "explored, not held".

Disposition: **defer**. C2 covers a grader (an eval artifact), not hygiene procedure;
kengaku must not absorb secret-removal procedure (souji's refusal names kagi + operator
as owners) nor rotation doctrine (kagi). The TB2 instruction's removal steps are grader
content — "pattern text is data" (`kengaku-shokunin/PROVINCE.md` round-36 paragraph).

### 2. git object-store forensics — souji holds the same-host measured record → CITE (proposed move)

- `souji-shokunin/corpus/knowledge/jj-dropped-keep-object-lifetime.md` (F1, admitted
  r31; `verified-at: 2026-10-26`): measured on this host's git 2.56.0 — "`git-gc-prune-now`
  leaves `reflog_hits=1` in all three arms, and only `reflog-expire-then-prune` reaches 0";
  "Expiry alone deletes no object: it removes the entry, and an object becomes prunable
  only once nothing reaches it." Record: `souji-shokunin/census/round-31/records/jj-object-clock-run.txt`.
- Its sources are the git-side docs kengaku's C2 receipt leans on:
  `souji-shokunin/corpus/SOURCES.md:84` (S063, git-gc(1) reachability: reflogs are gc
  roots; "Once a ref is gone its objects become prunable after the prune date") and
  `:167` (S222, git-reflog(1) @ tag v2.56.0: what `reflog expire` removes; `--expire=all`
  sentinels; scope explicitly "not the deletion scope of git-prune").
- SKILL rule at `souji-shokunin/SKILL.md:116`: "an object outlives its keep ref, so
  presence is not a receipt" — a reflog entry is a holder "which releases the object
  only when the entries are expired before the prune".

Why it matters: the frozen C2 receipt's headline includes "writing the literal alone
passes 5/5 while the secret commit stays in the reflog/object store (`echo-only`,
`echo-gc-only`, `echo-reflog-expire`)". Souji's r31 fixture measured exactly these levers
on the same host git 2.56.0 the claims file names in its limit ("host git 2.56.0 … stands
in for the image's Ubuntu git"). Citing converts that stand-in caveat from unqualified to
bounded: reflog/gc lever semantics are host-measured; only the image's git version/dash
remain standing in.

### 3. bwrap grader sandboxes — tameshi owns the envelope method and its measured limits → CITE

- `tameshi-shokunin/corpus/SOURCES.md:102` (S093, bwrap(1) bubblewrap 0.13.1, mined
  2026-10-23): documented meaning of `--unshare-all`, `--clearenv`, `--proc`,
  `--die-with-parent`, `--new-session`; scope "not a measured security boundary for any argv".
- `tameshi-shokunin/corpus/knowledge/guard-kill-closure.md:129`: probes run "in the
  bwrap envelope … with `env -i`, a private /tmp, and isolated PID and network
  namespaces… The envelope is a sandbox for the probes, not a proof of containment for
  the tools under test."
- `tameshi-shokunin/corpus/knowledge/regression-tally-completeness.md:42` (v4 counter
  runs each selftest in a bubblewrap sandbox), `:72` (E1 erratum: `--clearenv` keeps PWD
  and the argv then sets four variables — "cleared" overstates), `:74` (E3: "SentinelBwrap
  saw `/proc/1/environ` expose the counter's invoking environment").
- `tameshi-shokunin/corpus/knowledge/mutation-case-kumitate-round-gate.md:141-146`:
  GuardAudit showed "a hostile mutant can still write outside its directory, overwrite a
  sibling mutant, or reach the network"; bwrap confinement is the tested next step for
  untrusted mutants. `tameshi-shokunin/corpus/lessons/round-18.md:27` (G10): a bwrap
  safety envelope for probes/seats was admitted after N01 showed "a /tmp clone with live
  sibling symlinks is not a write boundary".
- Adjacent corroboration: `mado-shokunin/.ufo/waves/round-25/c1/count-v3.py:729-743`
  runs tools under the same envelope shape (`--ro-bind /usr`, `--unshare-all`,
  `--die-with-parent`, `--clearenv`, `/tmp` tmpfs); `mado-shokunin/.ufo/waves/round-25/a3w1/reports/K4Echo.md:42`
  measured that the PID namespace's `/proc` shows only `bwrap`+`python3`.

Kengaku's own probes already run per-case bwrap (`kengaku-shokunin/PROVINCE.md` round-37
paragraph: private network namespace, no root, scratch HOME and /tmp, `/tests`
read-only, scoped PATH). Disposition: **cite** tameshi S093 + guard-kill-closure for the
sandbox discipline and for two named limits (envelope ≠ containment proof;
`/proc/1/environ` class exposure) — kengaku's `git_leak_probe.py` mounts `--proc` too.
Do not absorb: the envelope is kengaku's own probe implementation.

### 4. Gate mutation batteries — tameshi owns the reusable method; kumitate holds the tool precedent → REPORT-OUT (already routed)

- `tameshi-shokunin/PROVINCE.md:1-17`: owns "verification-fixture craft — hermetic
  suites, mutation testing, fail-closed arms…"; "Never edits a sibling's gate code
  (read-only probes; recommendations travel in round reports)"; adjacent = "report,
  never absorb".
- Recorded legs: nine `corpus/knowledge/mutation-case-*.md` entries over kumitate,
  kagi, mado, tsukuroi gates, plus `mutation-score-semantics.md`,
  `witness-scoped-kill-verdict.md`, `oracle-anchored-survivors.md`, `mte-report-interop.md`.
- `kumitate-shokunin/scripts/gate-mutants.mjs` exists (confirmed by directory listing)
  — the kengaku-cited precedent.
- `kengaku-shokunin/PROVINCE.md` (round-37 paragraph) already records this exact
  report-out: "mutation testing of a lane's own gate is a fleet-wide pattern, not
  kengaku ground — tameshi's `tools/mutate-and-run.sh` and kumitate's `gate-mutants.mjs`
  are the precedents".

Disposition: **report-out, already routed**. C1's battery39 stays kengaku's frozen
counter's work product; tameshi may only add `pkg_gate.py` as a further recorded leg
under its own opt-in protocol, never editing the gate. No change needed this round;
this scan re-confirms the routing with current file:line evidence.

### 5. git-history-state gates (order-of-operations, frontier R3) — kasegi holds the sibling precedent → CITE for the frontier step only

- `kasegi-shokunin/corpus/knowledge/repo-git-state.md:1-63` (verified live 2026-09-28):
  git state read as a provenance layer — what `status/branch/rev-list/merge-base/ls-files`
  and the reflog proved at a measurement date ("commit-sourced claims end 2026-09-06,
  but the artifacts run to 2026-09-15"; `git reflog` shows all post-09-06 work is
  working-tree-only). Its r21 wave ran a dedicated seat (R21RepoProvenance) recovering
  what that evidence proved and cannot prove after root loss.
- The frozen claims' Frontier step (R3, not a claim): "a gate that reads git history and
  fails when a committed control shows the frozen probe executed before the first receipt
  commit". Kasegi's entry is the fleet's standing example of git-history-state being used
  as dated proof, and kasegi's `ops/shared.mjs::gitMutationBlocker` (fail-closed preflight
  during active rebase, recorded in the r23 anchor census) is the same mutation-state
  gate family.

Disposition: **cite** kasegi's `repo-git-state.md` in the R3 gate design as sibling
precedent for "git history as order-of-operations evidence". Not part of C1/C2 admission;
nothing frozen is touched.

### 6. Secret doctrine and "secret" vocabulary — kagi owns it; sibling sweep already done → DEFER, no absorption

- `kagi-shokunin/PROVINCE.md:66-67`: secret-scanning detection vs verification is kagi
  frontier; chousa/kasegi/kumitate run "their own secret-shaped tripwires over their
  outputs (hygiene filters, not vault ops)".
- `kagi-shokunin/.ufo/waves/round-25/build/ConnSiblings5.md:29-32` records the
  completed sibling sweep: souji yields secret scope to kagi (`souji-vault-verify.sh`
  refuses `*.env`/`*credential*`/`*secret*` paths), kaidoku treats 1Password asar as
  static analysis only, kotodama's "secret" is anthropological.

Disposition: **defer**. Kengaku's grader coverage names secrets only as the graded
artefact's content; per its own round-36 boundary ("pattern text is data"), no vault,
rotation, or scanning doctrine is claimed or needed.

## Negative results (report-out — no overlap with the four surfaces)

- `revenger-shokunin`: binary/container byte evidence (APK/AXML/ZIP, lessons through
  round 67); its git use is pointer-audit plumbing (`git show/cat-file/reflog` for
  citation integrity), not object-store forensics.
- `kaidoku-shokunin`: shipped-artifact static RE; 1Password asar is a static target,
  credentials redacted (per ConnSiblings5, above).
- `chousa-shokunin`: research-method owner; kengaku already defers capture/citation
  method (`kengaku-shokunin/PROVINCE.md` §Adjacent). No grader/sandbox ground.
- `kumitate-shokunin`: orchestration, seat arrangement, gate census; owns its own
  scripts; no TB2/grader content (a `terminal-bench` hit inside
  `.ufo/waves/round-63/.../forgery-borrowed/` is an archived copy of a kengaku r35
  dispatch payload, not kumitate domain).
- `kasegi-shokunin` otherwise: VDP/CVD/severity corpus; its only kengaku-r39 touch is
  observational — `.ufo/waves/round-35/wave1/CritBoundary.md:141` logs kengaku's commit
  `6a1eb5e` ("round-39: first recorded git-leak probe run") as fleet state during a
  boundary audit.
- `mado`, `tsukuroi`, `mori`, `kama`, `tabi`, `kake`, `kotoba`, `kotodama`, `lore`,
  `audio`, `game-dev-2d`, `game-dev-3d`: no git-secret, object-store, bwrap-grader, or
  mutation-battery ground (fleet-wide grep for `bwrap|bubblewrap`, `reflog|fsck|dangling`,
  `terminal-bench|grader`, `filter-repo|leak|credential` returned only the hits named
  above).

## Proposed move (one, bounded)

Add one adjacent-citation clause to the wave-1 draft of
`corpus/knowledge/tb2-git-leak-recovery-grader.md` (not frozen; C2's work product),
e.g. under Limits/Adjacent: the receipt's `echo-only`/`echo-gc-only`/`echo-reflog-expire`
passes corroborate souji's r31 host measurement on the same git 2.56.0 (gc `--prune=now`
leaves reflog entries; reflog expiry alone removes no object — `souji-shokunin/census/round-31/records/jj-object-clock-run.txt`,
S063/S222), and the probe's per-case bwrap envelope follows the fleet sandbox discipline
tameshi records (S093; `guard-kill-closure.md:129`, with its envelope-is-not-containment
limit). Effect: coverage axis gains a probed instance whose host-git caveat becomes
bounded rather than open; adjacency axis gains two sibling citations; calibration (C1)
untouched; no frozen file, counter, capture, or receipt modified — draft only, L1 decides.

## Risks

- Souji's r31 fixture arms are keep-ref-shaped (jj); the gc-root/remover reasoning is
  repo-generic, but the citation must not imply the TB2 task involves jj — cite the
  Remover-1/Remover-2 findings only.
- Tameshi's S093 is documentation evidence, "not a measured security boundary for any
  argv" (its own scope cell); kengaku's envelope differs in details (`/tests` ro-bind,
  scoped PATH). Cite discipline + limits, never equivalence.
- Routing #4 is already landed in kengaku PROVINCE (r37); repeating it here is
  confirmation, not a new claim — do not relabel battery39 as tameshi's.

## Verification (commands exercised, all read-only)

- `grep` for `reflog|git fsck|dangling|filter-repo|BFG|git-leak|secret…(remov|scrub|purge)`
  over the lane set — hits only at the file:line locations cited above.
- `grep` for `bwrap|bubblewrap|seccomp|landlock` over all 21 lanes — hits in
  tameshi (S093 + knowledge entries), mado (count-v3.py run_tool), kengaku's own
  plans probes; no corpus/knowledge entry in any other lane.
- `grep` for `git-leak|leak-recovery|terminal-bench` over kagi/kasegi/souji/tameshi/
  chousa/kumitate/revenger corpora — no sibling pins the TB2 `git-leak-recovery`
  grader (kengaku r35–r38's four prior TB2 graders are this lane's own series).
- `read` of the frozen claims file and of every cited sibling file at the named lines;
  all quotes ≤25 words and reproduced verbatim above.
- No installs (none needed); no writes outside this report; no scratch created (no
  fixtures were built).

Report: `.ufo/waves/round-39/build/R39ConnSibling.md`

VERDICT: sibling-overlap-6
