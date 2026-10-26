# R37ConnSibling — sibling-overlap scan for round-37 surfaces

Seat: R37ConnSibling (connector, leaf, read-only). Date: 2026-10-26.
Round-37 surfaces scanned against: C1 = mutation testing of the lane's own package gate
(`plans/round37_c1_verify.py`, 55 frozen mutants M01–M55); C2 = pinned TB2
`configure-git-webserver` grader admitted with an executed bubblewrap-sandboxed probe
(`plans/git_webserver_probe.py`, 22 cases; private network namespace per case).

## Method

Read-only. Scanned the three named surface files of all 21 fleet lanes
(`/home/vgpnk/Projects/shokunin/*-shokunin/{PROVINCE.md,corpus/README.md,SKILL.md}`), then
widened to `corpus/knowledge/`, `corpus/SOURCES.md` and lane tools where a surface was silent.
Recorder commands (all run from `/home/vgpnk/Projects/shokunin`):

- `grep -cH -iE 'terminal-bench|grader|TB2' *-shokunin/PROVINCE.md *-shokunin/corpus/README.md *-shokunin/SKILL.md` → only `kengaku-shokunin/*` matched (19 / 35 / 30 hits).
- `grep -nH -iE '\bgrader\b'` on the same 63 files → **no output outside kengaku-shokunin** (zero sibling surface uses the word "grader").
- `grep -rn -i 'git-webserver|configure-git' *-shokunin --include='*.md' --include='*.py' --include='*.json'` → **no sibling hit** (only kengaku-shokunin matches).
- `grep -nH -iE 'nginx|webserver|web server|sysadmin|gitweb|git-web|configure-git'` on the 63 surface files → one non-kengaku hit: kake README (below).
- `grep -nH -iE 'bubblewrap|bwrap|network namespace|netns|unshare|sandbox'` on the 63 surface files → kaidoku, kagi, kumitate, tameshi, tsukuroi (below).
- `grep -nH -iE 'mutant|mutation'` on the 63 surface files → 21 lanes hit; relevance triaged by hand (below).

## S1 — Terminal-Bench task graders: contested = 0, adjacent = 0

Kengaku uniquely holds this ground on its surfaces: `PROVINCE.md:233-240` (r35
`protein-assembly`), `PROVINCE.md:244-246` (r36 `regex-log`), `corpus/README.md:68-69`,
`corpus/README.md:258`, `SKILL.md:711` ("## TB2 regex-log grader — round36"). Round 37 adds the
third task, `configure-git-webserver`.

- **No sibling lane claims TB2 task graders — none contested, none adjacent.** Across all 63
  surface files only kengaku matches `terminal-bench|grader|TB2`; the fleet-wide
  `git-webserver|configure-git` search has zero sibling hits at any depth.
- Nearest non-kengaku mention anywhere: `kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md:29,53,83`
  cites Terminal-Bench as one benchmark inside an arXiv orchestration study's results table
  ("Terminal-Bench (2 tools): Independent +1.7% (0.350) vs SAS 0.344"). Data citation, not a
  grader claim, and not on kumitate's surface files. → none.

## S2 — service/sysadmin task verification (nginx/git/ssh): contested = 0, adjacent = 1

No sibling claims to *verify or grade* service/sysadmin task solutions.

- `kake-shokunin/corpus/README.md:41` — ETag anatomy: the recorded root ETag "decodes to
  mtime-length (nginx format, backend identity [INFERENCE])". Hosting forensics for GitHub
  Pages; a *format* citation, not service verification. → none.
- **kama-shokunin — adjacent.** `SKILL.md:70-195` documents a live HTTP classification probe
  of local endpoints (`curl -sSI`, `:8080`, `:34113`), with verdict classes `DEAD` /
  `NOT_HTTP` / `FOREIGN_SERVICE` / `UNAUTHORIZED_SERVICE` (`SKILL.md:178-182`). Same mechanic
  family as verify.sh's curl-against-a-live-service, different purpose: endpoint *identity*
  for model servers, not grading a task solution. No claim of sysadmin-task verification.
- kagi (`SKILL.md:43`, `SKILL.md:568` — `curl -fsS <endpoint>/health` drift checks), tabi
  (loopback fixtures, `SKILL.md:139-140`), souji (host service census) — operational probing
  only. → none.

## S3 — sandboxing graders (bubblewrap, network namespaces): contested = 0, adjacent = 4

No sibling claims a *sandboxing grader* — a verdict instrument whose authority rests on
running a subject under bwrap/netns for an external task. Kengaku r37's probe (per-case bwrap,
private netns) is unheld ground. Adjacent mechanics, all **sibling-internal** (they sandbox
their own tools, they do not grade others):

- **tameshi-shokunin — adjacent (closest).** `SKILL.md:1785`: "use `bwrap` when mutants are
  untrusted"; `SKILL.md:1929`: defect-probes.py runs "guard-removal mutant[s] … children run
  under bwrap with the fleet read-only". A mutation probe graded inside bwrap — the exact
  C1∧C2 combination, predating r37.
- **kumitate-shokunin — adjacent.** `SKILL.md:618` cap-run: "under `env -i` + `bwrap
  --unshare-pid --die-with-parent --new-session --clearenv`"; `corpus/README.md:93`
  (`agent-isolation-substrates.md`, bwrap PID-1 environ among seven isolation mechanisms);
  `corpus/README.md:145` (`mount-order-and-bind-scope.md`, bubblewrap bind-order knowledge).
- **kaidoku-shokunin — adjacent.** `SKILL.md:606` carrier-guard limits name "bwrap 0.13.1
  exists on the host" as a named bypass class.
- **tsukuroi-shokunin — adjacent (namespace mechanics).** `SKILL.md:3005` / `SKILL.md:3110`:
  score-pacnew-arm-r35b runs "20 stub, 3 namespace, 1 live view" arms in an "unprivileged
  user+mount namespace" (`unshare -rm` child, bind over `/sys/fs/btrfs` never leaving it).
  Mount/user namespaces, not network namespaces.
- mado round-26 nested Hyprland under `bubblewrap --unshare-all` appears only in the fleet
  report `.ufo/reports/round-26/mado.md:22-24`, not on mado's three surface files. → none.
- kagi `SKILL.md:74` ("any uid in the host netns can POST") is a security observation. → none.

## S4 — mutation testing of their own gates/counters: contested = 0, adjacent = 13

Fleet-wide norm; **no sibling contests kengaku's gate or counter** (kengaku's package gate and
the r37 counter exist only in kengaku). Every kaika-style lane mutates its own instruments —
adjacent, with named instruments kengaku should cite rather than re-derive:

| Lane | Evidence (file:line) | Instrument |
|---|---|---|
| tameshi | `SKILL.md:1785`, `SKILL.md:1929`; `tools/mutate-and-run.sh` (106538 bytes, executable) | exit-graded mutation runner; **the fleet's shared harness** — mado pins it as `MADO_VERIFY_HARNESS` (`mado-shokunin/SKILL.md:624`, `:852-857`, `:1050`) |
| kumitate | `SKILL.md:616` | `gate-mutants.mjs` — 43-mutant frozen battery over its own gate suites, per-mutant temp copy, exit-only kill predicate |
| kasegi | `SKILL.md:1067` | `limb-mutation-check.py` — per-limb kill on a scratch copy of own corpus |
| kaidoku | `SKILL.md:1001`, `:1045`, `:1215` | counters with `--build` mutant builders + `replay-gate.py` (runs a counter's argv with a reader substituted) |
| chousa | `SKILL.md:98`, `:129` | research-gate counters + `mutation-check.py` (`MUTANTS_KILLED=5/5` contract) |
| mado | `SKILL.md:651`, `:653` | `counter-selftest.py` mutated-counter runs; q36 fixtures "8/8 mutants killed" |
| mori | `SKILL.md:185` | `count-c2.py --mutants-dir` gate-conformance mutant arm |
| souji | `SKILL.md:224` | `mutation-adequacy.py` (59-literal oracle, expect=killed contract) |
| kagi | `SKILL.md:753` | `identity-swap.py` — row-identity reader's mutation harness |
| revenger | `SKILL.md:297` | `self_assessment_check.py` self-mutants (`SELF_MUTANTS_KILLED=6/6`) |
| tabi | `SKILL.md:2099` | counter-owned nonce/artifact mutants |
| kake | `SKILL.md:868` | runner mutants m2/m4 over its own counters |
| tsukuroi | `SKILL.md:47` | `mode-policy-mutant.json` — policy mutant failing its own 97-case suite |

Lanes with **no** S4 adjacency beyond this list: audio, game-dev-2d, game-dev-3d (engine-behavior
mutants, not gate/counter mutants), lore, kotoba, kasegi-counted, chousa-counted.

## Instruments kengaku should cite rather than duplicate

1. **`tameshi-shokunin/tools/mutate-and-run.sh`** — the fleet's existing general-purpose
   mutation runner (exit-only grading; mado already treats it as shared infrastructure).
   Kengaku's r37 counter implements its own frozen in-process silencing (unchangeable this
   round), but the round report / C1 entry should cite tameshi's harness as prior art for
   exit-graded mutation batteries.
2. **`kumitate-shokunin/scripts/gate-mutants.mjs`** (`SKILL.md:616`) — direct gate-mutation
   battery precedent (frozen manifest, per-mutant temp tree, kill by numeric exit).
3. **tameshi defect-probes bwrap pattern** (`SKILL.md:1929`) — precedent for the C2 probe's
   per-case bwrap sandbox (children under bwrap, fleet read-only).
4. **`kumitate-shokunin/scripts/cap-run.mjs`** (`SKILL.md:618`) — the fleet's bwrap-bounded
   runner; fleet L0 question (kumitate r64) already asks whether forgeable counters should be
   replaced by a bwrap-bounded runner — kengaku's r37 counters sit exactly in that class.

## Notes and non-issues

- kengaku S100 and kumitate S095 both pin the same public `bwrap.xml v0.13.1` — shared public
  source, no contest.
- kumitate's coordinator-topology entry (`corpus/knowledge/multi-agent-coordinator-topologies.md`)
  cites TB2 results data; it does not read or claim TB2 scoring code.
- game-dev-2d/3d mutate engine scenes and fixtures; the surface word "mutant" there is
  engine-behavioral, not gate/counter mutation. Not adjacent to r37 C1.
- No lane mirrors kengaku's r35/r36/r37 TB2 probe pattern (pinned grader capture + offline
  case probe with pre-written predictions); the `pinned-grader-probe` capability row remains
  kengaku-only (`SKILL.md` capability table; no sibling row matches `grader` at all).

## Tally

- Contested lane-surfaces across S1–S4: **0**.
- Adjacent sibling lanes: **14** — kama (S2); tameshi, kumitate, kaidoku, tsukuroi (S3);
  tameshi, kumitate, kasegi, kaidoku, chousa, mado, mori, souji, kagi, revenger, tabi, kake,
  tsukuroi (S4) — union = {kama, tameshi, kumitate, kaidoku, tsukuroi, kasegi, chousa, mado,
  mori, souji, kagi, revenger, tabi, kake}.

VERDICT: sibling-0-contested-14-adjacent
