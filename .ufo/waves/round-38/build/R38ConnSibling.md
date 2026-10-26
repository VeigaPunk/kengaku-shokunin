# R38ConnSibling — sibling-overlap scan for round-38 surfaces

Seat: R38ConnSibling (connector, leaf, read-only). Date: 2026-10-26.
Round-38 surfaces scanned: C2 = pinned TB2 `build-pmars` build-provenance grader
(`plans/build_pmars_probe.py`, 22 cases; graded state = built artefact + source tree, checked by
presence, `ldd` string scan, directory shape, regex over program output; headline finding: the
`ldd` scan misses a `dlopen()`ed libX11); C1 = gate mutation battery (`plans/battery38/*.py`,
22 frozen mutants N01–N22 of `plans/pkg_gate.py`, attributed kill rule, side-channel token
scan); shared substrate = per-case bwrap grader sandboxes (carried from round 37's
`configure-git-webserver` probe; kengaku r37 PROVINCE records its own per-case bwrap use).

Method: read-only. Grepped all 20 sibling lanes under `/home/vgpnk/Projects/shokunin/` for
`build-pmars|build_pmars`, `terminal-bench`, `\bldd\b`, `bwrap|bubblewrap`,
`dlopen|libX11`, `grader`, `mutant|mutation`, then widened to `corpus/knowledge/`, lane tools
and `.ufo/` receipts where a surface was silent. Recorder commands below; every file:line was
re-read from committed bytes this session. Prior round-37 scan
(`.ufo/waves/round-37/build/R37ConnSibling.md`) covered the git-webserver surfaces; this scan
extends to the build-provenance class and the carried D6 item.

## S1 — TB2 build-provenance grader: contested = 0, adjacent = 0

`grep -r 'build-pmars|build_pmars'` across all 20 siblings → **no matches** (command run this
session over `/home/vgpnk/Projects/shokunin/*-shokunin`, 0 hits outside kengaku). No sibling
holds or contests TB2 task-grader ground (round-37 scan's S1 conclusion stands; kengaku
PROVINCE.md round-35/36/37 admissions are the only TB2 grader claims in the fleet). The
nearest non-kengaku terminal-bench mentions remain data citations, not grader claims:
kumitate-shokunin `.ufo/waves/round-63/build/K63Capture/arxiv-2512.08296v3.html` (arXiv study
naming Terminal-Bench as a benchmark; no grader semantics) and kotoba's census of kengaku's own
S100 row (S6 below).

Overlap for this surface lives in the *instruments* the grader uses (`ldd`, bwrap), not in the
grader class — see S2/S3.

## S2 — ldd/X11 checks: contested = 0, adjacent = 1 → **cite + report-out** (overlap 1)

audio-shokunin is the only sibling with a systematic ldd-for-provenance practice, and its
committed receipts corroborate the C2 headline finding (an `ldd` string scan misses runtime
linkage) from three independent directions:

- `audio-shokunin/reports/round-75/r75-reviewer.md:39` (E11): attribution row whose mechanism
  evidence is `ldd /usr/bin/paplay` **and** `strings /usr/bin/paplay` — "links `libsndfile.so.1`;
  strings include `sf_open_fd`… → the name-blind fd-open attribution reproduces". Audio's
  standing discipline: ldd never stands alone; it is always paired with `strings` or strace
  before a mechanism claim is made.
- `audio-shokunin/corpus/live/r93-scout/RECEIPTS.md:59-63`: "`/usr/lib/spa-0.2/filter-graph/*`
  strings/ldd, the installed `libspa-filter-graph-plugin-ebur128.so` (objdump -d)" plus the
  explicit caution "**Source vs binary divergence flagged in the report… the measured law is
  authoritative.**" — the same canned-vs-real artefact caution class as C2's canned-14-line-C
  observation.
- `audio-shokunin/corpus/live/r64-reviewer/r64rev-formats.c:1683-1684`: the lane's own primary
  domain binary (SoX_ng) loads its format handlers via `lt_dlhandle lth = lt_dlopenext(file);`
  — a concrete instance where `ldd` on the main binary **cannot** show plugin linkage that
  matters; and `audio-shokunin/corpus/live/r64-boundary/runs/strace-stdin-file.txt:247`
  (`openat(…, "/usr/lib/libX11.so.6", O_RDONLY|O_CLOEXEC)`) shows strace, not ldd, is what
  observes libX11 actually being opened at runtime — byte-level sibling evidence for C2's
  "`ldd` string scan misses a `dlopen()`ed libX11" observation.

Recommendation: **cite** these three receipts in the new `corpus/knowledge/tb2-build-pmars-grader.md`
entry as sibling corroboration of the ldd/dlopen limit (they are committed evidence, not
method), and **report-out** to audio per kengaku PROVINCE adjacency (audio is not in kengaku's
Adjacent table; a citation of receipts is not absorption). No contest: audio PROVINCE.md:3-5
owns SFX/music headless analysis, not grader semantics.

## S3 — bwrap grader sandboxes: contested = 0, adjacent = 4 → **cite** (overlaps 2–3), **report** (overlap 4), **defer** (overlap 5)

No sibling claims a *sandboxing grader* (round-37 S3 verdict stands). Adjacent mechanics, all
sibling-internal — kengaku's r37 per-case bwrap probe remains unheld ground:

- **Overlap 2 — tameshi bwrap defect-probes (CITE; completes routed D6).**
  `tameshi-shokunin/.ufo/evidence/round-18/coldread/traces/CR04/17.json:6` and
  `CR05/10.json:4` record tameshi executing *sibling* gates (kagi `corpus/surface-census.sh`,
  kumitate `kimi-census.mjs`) inside `bwrap --ro-bind / / --unshare-net --die-with-parent`
  sandboxes — the direct precedent for running a subject gate/grader under bwrap with the lane
  bound read-only. With it, `tameshi-shokunin/.ufo/evidence/round-16/coldread/skill-versions/SKILL.05a2247.md:1779-1783`:
  "use `bwrap` when mutants are untrusted" **and** "Grade by exit, not by stdout bytes" (three
  pristine runs differ byte-for-byte yet exit 0 → a repeated-control byte comparison reports
  `controls_mismatch`). The second half is method prior art for C1: kengaku's attributed kill
  rule compares printed `DEFECT` lines (safe because the gate's output is deterministic), but
  tameshi's exit-not-bytes rule is the fleet's standing caution for exactly this comparison
  shape — worth one pointer line in the C1 claims report.
- **Overlap 3 — kumitate `cap-run.mjs` (CITE; completes routed D6).**
  `kumitate-shokunin/scripts/cap-run.mjs:1-16` (contract `kumitate-cap-run-v2`): a bounded
  child runner giving one child "a native-memory cgroup cap, an explicit environment, a total
  budget, descendant and signal cleanup and its own PID namespace"; bwrap invocation
  (`--ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --tmpfs /run --unshare-pid --clearenv`)
  with `/`, `/tmp`, `/proc`, `/sys`, `/dev`, `/run` refused as binds (round-47 v2, :24-31).
  This is the instrument D6 names and the round-37 report-out cited without file:line
  (kengaku PROVINCE.md round-37 paragraph). Pointers now supplied.
- **Overlap 4 — mado live-counter sandbox (REPORT, not cite).**
  `mado-shokunin/quality/counters/c1-r40-live-v2.py:19-22` runs its live compositor fixtures
  inside `bwrap --unshare-all --cap-drop ALL` with "a fresh /proc and /dev"; `:496` raises
  `sandbox_unavailable bwrap rc=…` → "No bwrap -> SETUP, exit 2 (never" (:22) — fail-closed
  sandbox-unavailable handling, a pattern battery38 could adopt if it ever sandboxes fixture
  builds. Lane-internal to mado; report only.
- **Overlap 5 — kaidoku bwrap version-pairs (DEFER).**
  `kaidoku-shokunin/.ufo/waves/arc2-loop1-round2/E9.md:18` records "live compares on
  expac/bwrap pairs" (`corpus/knowledge/2026-10-13-r2-version-diff-compare.md`); kaidoku owns
  multi-version binary comparison craft and holds bwrap as a *subject*. If the C2 probe's
  host-substitution limits (host bash for Debian dash, host glibc ldd — claim's own Limits)
  ever need version-compare discipline, defer to kaidoku. No action this round.
- (kagi `considerthese/2026-10-21.md:113-117` proposes bwrap for ledger rows; mori's bwrap
  nonces are recorded in chousa `.ufo/waves/round-51/w1/R51ConnCrossClaim.md:39-41`. Both
  noted in round-37 S3; unchanged.)

## S4 — gate mutation batteries: contested = 0, adjacent = 2 → **cite** (overlaps 6a–b), **report** (overlap 7)

- **Overlap 6a — tameshi owns the mutation-method; C1's attributed kill rule has direct prior art (CITE).**
  `tameshi-shokunin/PROVINCE.md:3-5` (Domain: "verification-fixture craft — … mutation
  testing, fail-closed arms, verdict-line discipline"), `:14-17` ("every lane's gate remains
  its own… Never edits a sibling's gate code"). The attributed kill rule is not new fleet
  ground: `tameshi-shokunin/corpus/knowledge/witness-scoped-kill-verdict.md` (S006 shmutant
  witness grammar — a kill counts only when the suite goes red "on its witness", else
  "accidental"; witness declarations pre-registered before the sweep) is the same
  attribution discipline as kengaku's silence/mirror/RUN/MAIN rule (a kill must bind to the
  mutant's own clause). `tameshi-shokunin/corpus/knowledge/mutation-score-semantics.md` maps
  the verdict vocabulary across Stryker/cargo-mutants/mutmut/shmutant and excludes
  inconclusives — parallel to kengaku's `invalid=0 null_detected=0` guards.
  `tameshi-shokunin/corpus/knowledge/r43-survivor-resolution-rule.md` (K/D/E/U rule; an
  equivalent mutant is reported as a limit, never removed) matches C1's kill-rule sentence
  "A mutant later shown equivalent is reported as a limit, never removed from the list."
  C1 mutates only its own gate, which tameshi's province explicitly leaves to the lane — no
  contest. Kengaku's r36 PROVINCE already names tameshi adjacent; the round-38 battery should
  cite these three entries by file:line in its module-header comments (new files, not frozen).
- **Overlap 6b — kumitate `gate-mutants.mjs` K43 (CITE).**
  `kumitate-shokunin/scripts/gate-mutants.mjs:10-18` (contract `kumitate-gate-mutants-v2`):
  "a mutant is KILLED iff its run is evaluable (no timeout, no overflow, … a parseable case
  summary whose total equals the control's), the selftest exits with a numeric non-zero
  status, stdout carries the exact line `VERDICT: FAIL`, and an immediate second run of the
  same mutated bytes meets the same conditions" — a frozen kill predicate with determinism
  re-run, the same shape as kengaku's counter (reference vs mutant output compare under a
  pinned fixture set). Fleet precedent, already named in kengaku PROVINCE round-37
  report-out; supply the file:line.
- **Overlap 7 — chousa runs the same pattern on its own gate (REPORT).**
  `chousa-shokunin/.ufo/waves/round-38/w1/RevErrataCtx.md:13,26`: chousa's round-38 wave-1
  measured a scratch `gate-mutant-command-env.sh` of its own `tools/research-gate.sh`
  (sed-copy in /tmp, "The landed gate was not modified"). Corroborates tameshi's
  two-independent-lanes rule that lane-gate mutation is fleet-wide method, not kengaku
  ground. No kengaku action; noted so C1's claims report can say "fleet pattern" with a
  second current instance.

## S5 — fleet registry hygiene (REPORT; overlap 8)

`kotoba-shokunin/.ufo/waves/round-71/receipts/census-after.txt:28` (census run against
`/home/vgpnk/Projects/shokunin`): `kengaku W04 S100 duplicate url
github.com/laude-institute/terminal-bench-2 across scopes`. C2 adds S115/S116 (new
build-pmars URLs — no new duplicate), but the standing W04 flag on kengaku's registry is
unchanged and is the kind of finding the round-38 entry work should not worsen (keep one row
per URL scope). Not an overlap claim; report to the L1 for the SOURCES appendix.

## Synthesis — one bounded move (drafts for L1; nothing frozen touched)

Round-37 routed D6 ("sibling prior art uncited", spot-check §5 item 6) is carried into round 38
(`plans/round-38-claims.md` Frontier step). All four citations above land in **non-frozen** work
products, so a wave-1 seat can execute them:

1. **C2 entry** (`corpus/knowledge/tb2-build-pmars-grader.md`, new this round): add a
   "Sibling prior art (corroboration)" appendix citing audio `r75-reviewer.md:39`,
   `r93-scout/RECEIPTS.md:59-63`, `r64-reviewer/r64rev-formats.c:1683-1684` and
   `r64-boundary/runs/strace-stdin-file.txt:247` for the ldd/dlopen limit. Improves adjacency
   and coverage support; harms none (append-only, entry is not frozen).
2. **C1 battery38 module headers** (new files): a three-line header comment citing tameshi
   `witness-scoped-kill-verdict.md` + `mutation-score-semantics.md` +
   `r43-survivor-resolution-rule.md` (attributed kills / verdict vocabulary / equivalent-as-limit),
   kumitate `gate-mutants.mjs:10-18` (frozen kill predicate) and tameshi
   `SKILL.05a2247.md:1779-1783` (grade-by-exit caution). Battery modules are new, so this does
   not touch the frozen counter or gate. Improves adjacency; harms none.
3. **C1 claims report** (new): one report-out line naming audio (ldd receipts cited, not
   absorbed), mado (bwrap fail-closed pattern noted), chousa (fleet-pattern corroboration),
   kotoba W04 (registry flag standing).

Risks: (a) citing sibling receipts inside a C2 entry binds the entry to sibling paths that can
drift — mitigated by quoting byte-level anchors (file:line + the 9-word E11 quote) rather than
paraphrase; (b) tameshi's province says recommendations travel in round reports — the citations
here are evidence pointers, not method transfer, and tameshi is named as owner in each pointer.

No installs/upgrades this seat (read-only scan; nothing fetched).

VERDICT: sibling-overlap-8
