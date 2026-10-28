# R50C1ConnOverlap — sibling-overlap scan (serving R50-C1, novelty)

Seat: connector, round 50 (hyaku run 11), wave `w1`. Leaf member, no subagent dispatch.
Item: does any sibling lane own **"git fixture geometry"** or **"sandbox admission"** ground (read
sibling `PROVINCE.md`, read-only)? Cite the sibling path and the closest row; propose absorb vs
report-out per item. Also: does `kumitate` own **tool-instrument standards** this counter should
follow?

## Axes named

| axis | direction | verdict of this seat |
|---|---|---|
| **novelty** (primary — the axis C1 works) | 7 → 8 | **improved**: the C1 novelty claim gets an evidenced boundary and a hardened attribution (finding 1, 2, 5) |
| coverage | untouched (operator-capped, not claimed this round) | not touched, not reached |
| calibration | untouched (that is R50-C2) | **cross-claim coupling found** (finding 5) — reported to L1, not edited |

Axis vocabulary is the claims file's own; no new axis invented.

## Revision measured

    REV kengaku-shokunin  822f3b748306ec6918a415bc713f9688a3de20e7   (worktree read for text)
    REV freeze            3b02d573d58cc6d2e0d27ef92ac0815354912252   (ancestor of both 5c56819 and 822f3b7)
    REV base tip          71f5f5f77591d8c3d19297ee9785436da45209e4   (per claims file, not re-derived)
    REV tameshi           133b2ce6d4d86d783db38607343c3654350194b8
    REV kumitate          14057f3e3899180c95713bace088fb9c0d0046e3
    REV souji             fcdecaaf293f0fee3c39cc148ae91389e04ef63c
    REV mado              3b55b6e91e40f455dd56b2985e4ffc087ada92d5
    REV kaidoku           c0112995817b4d8caddd86705b08e89bdac99640
    REV kotoba            47dbe8781657de563ff867caca6244d28e3db504

Freeze ancestry was asserted **before** any measurement and re-asserted after the lane tip moved
from `5c56819` to `822f3b7`:

    $ git -C kengaku-shokunin merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD && echo ANCESTOR_OK
    ANCESTOR_OK

## Exact commands run (all read-only; nothing outside my report was written)

    ls /home/vgpnk/Projects/shokunin/                                  # 26 siblings, 21 git repos
    for d in */; do [ -f "$d/PROVINCE.md" ] && wc -l < "$d/PROVINCE.md"; done
    grep -n -i '(fixture|sandbox|admiss|hermetic|instrument|hostile|mutant|fence|kengaku)' */PROVINCE.md
    sed -n '1,40p' kumitate-shokunin/PROVINCE.md
    grep -n 'Gate registry' -A25 kumitate-shokunin/SKILL.md
    sed -n '1,28p' tameshi-shokunin/corpus/knowledge/witness-scoped-kill-verdict.md
    sed -n '/^## Frontier/,/^## /p' tameshi-shokunin/corpus/README.md
    sed -n '481,520p' tameshi-shokunin/SKILL.md                       # No-permissiveness audit recipe
    sed -n '375,420p' PROTOCOL.md                                     # §Gate standard
    grep -n 'counter-pins|counter-rerun' kumitate-shokunin/SKILL.md
    sed -n '1,40p' kumitate-shokunin/scripts/counter-rerun.mjs
    grep -n "'node'|spawnSync" kumitate-shokunin/scripts/counter-rerun.mjs
    grep -rn 'admitted=|refused=' tameshi-shokunin/{SKILL.md,PROVINCE.md,corpus/README.md} kumitate-shokunin/SKILL.md souji-shokunin/PROVINCE.md
    git -C kengaku-shokunin show 3b02d57:SKILL.md | grep -n 'Gate/probe registry'
    git -C kengaku-shokunin show 3b02d57:PROVINCE.md | grep -n 'Reported out (round 3[78])|owns the \*method\*|re-specify caps'
    grep -n 'EXTS|FILES|TOKEN' kengaku-shokunin/plans/round50_c2_audit.py
    sed -n '140,200p' kengaku-shokunin/plans/round50_c1_verify.py
    for p in plans/mutants50/c1-mutants.json plans/sealed50 plans/honest50/population.txt \
             plans/honest50/build_honest_population.py plans/fixture_fence.py \
             plans/round50_c1_verify.py plans/round50_c2_audit.py; do test -e "$p"; done

Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1ConnOverlap` was created, never populated (no
candidate code was needed for a read-only scan), and is removed. No `git clone` was made: no lane
tool was executed, so no clone was required.

## Findings

### F1 — `tameshi` owns the fixture/mutation *method*; it does **not** own any lane's fixture population

Closest row: **`tameshi-shokunin/PROVINCE.md:3-5`**

> **Domain:** verification-fixture craft — the reusable method of honest
> checks: hermetic suites, mutation testing, fail-closed arms, verdict-line
> discipline, no-permissiveness audits, before/after proof.

and **`tameshi-shokunin/PROVINCE.md:14-17`**

> **Refuses:** product domains — every lane's gate remains its own; tameshi
> owns only the reusable craft (a pattern is admitted from evidence in TWO
> independent lanes before it is claimed general). Never edits a sibling's
> gate code (read-only probes; recommendations travel in round reports).

Corroborated by a third party: **`kotoba-shokunin/PROVINCE.md:27`** — "chousa owns claim-vs-source
research method, **tameshi owns the fixture/mutation method across lanes' gates**, kengaku's
calibration is model-eval".

**The load-bearing negative (this is the novelty finding).** tameshi's method is
**single-directional**. Its own recipe, **`tameshi-shokunin/SKILL.md:481-484`**:

> Goal: prove a change did not make anything pass by absence — no finding went
> quiet, no arm stopped firing, no claim passed on a warning line.

Every one of its eight steps tests *under-refusal* (nothing became too permissive, nothing went
quiet, no claim passed on a warning). Step 6 — "**Zero-work is a defect, not a green**"
(`SKILL.md:504`) — is about zero *findings*, which is the same direction. **There is no step and
no frontier row for the opposite error: a gate that refuses a legitimate input.** tameshi's Frontier
table (`tameshi-shokunin/corpus/README.md` §Frontier, F1–F10) has mutation score, witness-scoped
kills, determinism, golden/snapshot discipline, hermetic env, fixture minimization, re-sweep
granularity, oracle anchoring, LLM mutant generation, PBT generators — none of them an honest-input
denominator.

Therefore R50-C1's `HONEST fixtures=126 admitted=113 refused=13` measures an error class the owning
sibling's method explicitly does not reach. That is the defensible novelty, and it is a *negative*
result obtained by reading tameshi, not an assertion about kengaku.

### F2 — no sibling owns "git fixture geometry"; the nearest rows are souji's and kumitate's, and both are elsewhere

Searched all 20 sibling `PROVINCE.md` files for `fixture|sandbox|admiss|hermetic|instrument|hostile|mutant|fence`. Three near hits, all bounded away:

- **`souji-shokunin/PROVINCE.md:3`** — "**Domain:** fleet repository & workspace hygiene (掃除) —
  receipt-gated". Nearest rows: `:11` dead **worktree *metadata*** (`git worktree prune` after the
  ref is gone), `:27` "`refs/jj/keep/*` pins", `:66` **F2 repository size census** (`git repo
  structure`, `count-objects`), `:91` Core "read-only `git repo structure --format=lines`". This is
  the closest row in the fleet to "git store geometry", and it is **observation of live repos for
  hygiene/size**, not a frozen fixture population of documented store shapes. souji bounds it
  itself at `:101-107`: "this is a refusal fence, not credential hygiene or a secret-content
  scanner … Known namespace checks are not a universal defense against hostile bind mounts,
  hardlinks or concurrent filesystem replacement", and at `:127` "a git failure keeps the existing
  history-unverifiable path". souji declines to adjudicate git state.
- **`kumitate-shokunin/PROVINCE.md:15`** (frontier band) — "Isolation substrates for parallel
  agents (**git worktrees**, harness isolation backends, jj workspaces)". `git worktree` here is a
  **seat-containment mechanism**, not a fixture class.
- **`kaidoku-shokunin/PROVINCE.md:102-103`** — "Malware triage at scale — verdict pipelines, **sandbox
  detonation**, bulk classification `(unowned)`". The only literal "sandbox" hit in the fleet, and
  it is explicitly **unowned** and a different sense (executing untrusted samples).

The two r50 honest classes that make this question sharp — `n20-linked-worktree`,
`n21-separate-gitdir`, `n22-alternates-in-d`, `n17-replace-ref`, `n18-shallow-fetch` — are named by
**no sibling** as ground. Confirmed by the token that would betray a duplicate: **no sibling prints
an admitted/demoted honest denominator at all**:

    $ grep -rn 'admitted=|refused=' tameshi-shokunin/{SKILL.md,PROVINCE.md,corpus/README.md} \
          kumitate-shokunin/SKILL.md souji-shokunin/PROVINCE.md
    (no output)

### F3 — "sandbox admission" is kumitate's for the fleet runner, and kengaku has already conceded it

Closest row: **`kumitate-shokunin/PROVINCE.md:15`** ("Isolation substrates for parallel agents")
whose instrument is `scripts/cap-run.mjs` — "`bwrap --ro-bind / / --unshare-pid --die-with-parent
--new-session --clearenv`, tmpfs `/tmp`/`/run`, cwd bound rw, caller `--bind` **refuses
`/`,`/tmp`,`/proc`,`/sys`,`/dev`,`/run`**" (cited from `kengaku-shokunin/PROVINCE.md:321`). That
refusal list *is* an admission policy for what may enter the sandbox.

kengaku has already recorded the disposition twice, at freeze:

- `kengaku-shokunin/PROVINCE.md:339` — "**kengaku** does not re-specify caps, scopes or bind policy."
- `kengaku-shokunin/PROVINCE.md:311` — "**Reported out (round 38) — sandboxed-probe prior art**",
  the 13-lane table of sandboxed-counter implementations (tameshi, kumitate, mado, kake, mori,
  kotodama, kaidoku).

So there is nothing left to absorb. Note it is also **not load-bearing for C1**: the claims file's
§Named limits says "the repaired fence starts no git child at all", so the S2 predicate needs no
sandbox envelope. If S2 ever sandboxes the fixture *builder*, that must cite `cap-run` rather than
restate binds.

### F4 — `kumitate` does **not** own tool-instrument standards; the fleet `PROTOCOL.md` does

This is the direct answer to the third question, and the answer is *no, with a but*.

- kumitate's province is **`kumitate-shokunin/PROVINCE.md:3`**: "orchestration & tooling — scopes
  OMP task/hub, ufo-fsd scripts & runtime". It says nothing about gate/instrument design.
- Its gate registry is **lane-local**: `kumitate-shokunin/SKILL.md:587` "## Gate registry", `:589`
  "Registry home per the fleet protocol's §Gate standard (round 34)", `:595-596` "Owner: this lane
  (kumitate L1)". It *follows* the standard; it does not own it.
- tameshi says the same about kumitate's contracts: "kumitate owns the gate and its contract
  `kumitate-sources-v1`" (`tameshi-shokunin/PROVINCE.md:80`) — i.e. kumitate owns *its own*
  gate's contract string, not a fleet instrument standard.

The standard that C1's counter must follow is **`PROTOCOL.md:375-419` §Gate standard** (fleet root),
whose Registry clause fixes the child-lane registry home:

> **Registry.** The schema is this section's; a child lane's *registry home* is its own `SKILL.md`.
> Row fields: name, `gate|probe`, entry command, verdict map (code → class), self-test command and
> spelling, pinned-value path, write scope, owner.

kengaku's registry home already exists: **`kengaku-shokunin/SKILL.md:560`** `## Gate/probe registry
(PROTOCOL §Gate standard)`, with the eight PROTOCOL columns at `:562`.

**But** kumitate is the fleet's densest conformant implementation, and it ships two *parameterized*
instruments that are the closest thing to a reusable standard:

| kumitate instrument | row | reusable by kengaku? |
|---|---|---|
| `scripts/counter-pins.mjs` — contract `kumitate-counter-pins-v1`, "checks repo-relative paths, byte sha256, regular-file targets, and a nonempty pin set", takes `--registry <path>` | `SKILL.md:625` | **yes, as pattern** — parameterized, read-only. Only relevant if S2 wants machine-checked instrument digests instead of prose ones. |
| `scripts/counter-rerun.mjs` — probe `COUNTER_RERUN: AGREE\|DISAGREE`, `--probe <abs-probe> --lane <abs-lane> --rev <rev> --runs K` | `SKILL.md:621` | **no, not as-is** — see F6. |

### F5 — cross-claim coupling (second-order): C1's routing home *is* part of C2's frozen pointer surface

The C1 report-out sentence belongs in `PROVINCE.md` (that is where every prior disposition lives:
`:282` round 37, `:311` round 38). But C2's audit reads exactly that file:

    plans/round50_c2_audit.py:41   FILES = ("SCORECARD.md", "SHONEN.md", "PROVINCE.md")
    plans/round50_c2_audit.py:42   EXTS  = ("md","py","json","jsonl","txt","patch","whl","sh","json5","tres")
    plans/round50_c2_audit.py:43-45  TOKEN = (plans|corpus)/….EXTS  |  [0-9a-f]{40}

A pointer is any lane-relative `plans/…`/`corpus/…` path with one of those extensions, **or any
40-hex hash**. So a round-50 routing paragraph appended to `PROVINCE.md` creates C2 pointers that
must resolve, and any commit hash it cites must be an ancestor of the tip.

Measured existence right now:

    EXISTS  plans/mutants50/c1-mutants.json
    EXISTS  plans/honest50/population.txt
    EXISTS  plans/honest50/build_honest_population.py
    EXISTS  plans/fixture_fence.py
    EXISTS  plans/round50_c1_verify.py
    EXISTS  plans/round50_c2_audit.py
    ABSENT  plans/sealed50            (0 modules)

**The trap:** `plans/sealed50` does not exist yet. A routing paragraph written at S2 that names a
sealed module by path (e.g. `plans/sealed50/h01_….py`, `EXTS` includes `py`) before that module is
committed puts an unresolved pointer into `PROVINCE.md` and fires C2's kill rule
("**Kill rule:** any unresolved pointer or hash") — C1's report-out can kill C2. A directory form
(`plans/sealed50/`) is safe because the regex requires a filename with an extension; a bare 40-hex
hash is safe only if it is already an ancestor.

### F6 — kumitate's repeat-run probe cannot host this counter (a real limit, checked, not assumed)

R50-C1 has no flake/determinism arm. The obvious fleet instrument is `counter-rerun.mjs`, and it is
*not* usable here:

    kumitate-shokunin/scripts/counter-rerun.mjs:197
    const r = spawnSync(process.execPath, [o.probe, o.lane, o.rev, ...o.rest], { … });

`process.execPath` is **node**, and the header states "The counter is run with `node`". R50-C1's
counter is `python3 plans/round50_c1_verify.py`. Pointing `--probe` at it yields `node <py>` →
syntax error, i.e. exit 2 fail-closed at best. Adopting it would need a Node shim — a new
unregistered instrument, which fails the very Registry clause in F4. **Report this as a named limit;
do not adopt.**

### F7 — a conformance observation that turned out **not** to be a defect (recorded so nobody re-files it)

I first read `plans/round50_c1_verify.py:300` (`sys.exit(main())`) plus `return 0 if ok else 1` as
"no could-not-evaluate arm". That is wrong, and I checked before reporting: `:159-162` has a setup
arm.

    for rel in (FENCE_REL, POP_REL, BUILDER_REL, K44_REL):
        if not (lane / rel).is_file():
            print(f"SETUP missing {rel}", file=sys.stderr)
            return 2

Verdict map is therefore `0 clean / 1 failed / 2 could-not-evaluate`, which conforms to
`PROTOCOL.md:380-384`. The only real Registry gap is the **missing row**: at the freeze commit,

    $ git show 3b02d57:SKILL.md | grep -c 'round50'        → 0
    $ git show 3b02d57:SKILL.md | grep -c 'round4[0-9]-c[12]' → 16

sixteen registered predecessor counters, zero round-50 rows. `PROTOCOL.md:420-421` makes that
blocking for conformance: "closure grades no gate conformant until its registry row exists at the
lane's *registry home*".

## Absorb vs report-out, per item

| # | item | closest sibling row | disposition | why |
|---|---|---|---|---|
| 1 | **git fixture geometry** (the 126-fixture honest population, `n17`–`n22`) | `souji-shokunin/PROVINCE.md:3,11,27,66,91`; `tameshi-shokunin/PROVINCE.md:3-5,14-17` | **KEEP (neither absorb nor report out)** — population and instrument stay kengaku; add a one-line *citation* of tameshi/souji as nearest neighbours in the round report | No sibling claims the ground; souji observes live repos for hygiene and explicitly declines to adjudicate git state (`:107,:127`); tameshi owns only the method and refuses product domains (`:14-17`) |
| 2 | **the mutation leg** (`MUTANTS`, floor 12, Q38 witnessed kills) | `tameshi-shokunin/tools/mutate-and-run.sh`; `kumitate-shokunin/scripts/gate-mutants.mjs`; `kengaku-shokunin/PROVINCE.md:282-285` | **REPORT-OUT — already discharged at round 37; cite, do not re-report** | kengaku's own PROVINCE: "mutation testing of a lane's own gate is a fleet-wide pattern, **not kengaku ground**". Re-reporting it would manufacture a finding |
| 3 | **sandbox admission** (bwrap bind/cap policy) | `kumitate-shokunin/PROVINCE.md:15` + `scripts/cap-run.mjs:30-38,189-196`; 13-lane table at `kengaku-shokunin/PROVINCE.md:311-333` | **REPORT-OUT — already discharged at round 38; nothing to absorb** | `PROVINCE.md:339` "kengaku does not re-specify caps, scopes or bind policy"; and C1 needs no envelope once the fence starts no git child |
| 4 | **tool-instrument standards** | standard is `PROTOCOL.md:375-419`, not kumitate; kumitate is a conformant implementer (`SKILL.md:587-596`) | **FOLLOW the fleet standard through kengaku's own registry home**; cite kumitate `counter-pins` as the parameterized pin precedent; **reject** `counter-rerun` (Node-only, F6) | kumitate's province is orchestration/tooling, its registry is lane-local ("Owner: this lane (kumitate L1)") |
| 5 | **C1 × C2 interface** (`PROVINCE.md` is both routing home and C2 surface) | `plans/round50_c2_audit.py:41-45` | **REPORT TO L1 (new)** — a constraint on *where* the routing sentence may be written and what it may name | not a sibling question; found while answering it, and it can kill C2 |

## Proposed move (one, bounded)

**Move: in S2, re-anchor C1's novelty on the over-refusal denominator and discharge the method half
by citation — with the routing sentence written to be C2-safe.**

Three mechanical halves, no predicate change, no new instrument, no new fixture:

1. **Attribution** — the round report and the S2 commit message state the novelty in the measured
   direction: *a frozen honest denominator that measures **over**-refusal* (`admitted=113 → 126`),
   citing `tameshi-shokunin/SKILL.md:481-484` as the owning method and noting it is
   one-directional (F1). The `MUTANTS` leg is declared an **application** of tameshi's method to
   kengaku's own fence, exactly as `kengaku-shokunin/PROVINCE.md:340-343` already says of
   `plans/pkg_gate.py` — so `MUTANT_MIN=12` is a robustness floor, never the novelty.
2. **Registry row** — append one row to `kengaku-shokunin/SKILL.md:560` §Gate/probe registry for
   `round50-c1-honesty`: kind `gate`; entry `python3 plans/round50_c1_verify.py --lane .`; verdict
   map `0` clean · `1` failed · `2` could-not-evaluate (`SETUP missing …`); self-test = the four
   control receipts under `plans/controls50/` plus `.ufo/waves/round-50/claims/` (the pattern
   `round36-c1-battery` already uses: "the battery is the self-test"); pinned values = the digests
   already frozen in `plans/round-50-claims.md`; write scope = `--work`/`$TMPDIR` only; owner
   kengaku.
3. **Routing sentence** — append-only, at EOF of `PROVINCE.md`, naming **only** artifacts that exist
   at the commit that lands it: `plans/fixture_fence.py`, `plans/round50_c1_verify.py`,
   `plans/honest50/population.txt`, `plans/mutants50/c1-mutants.json`. **Never** a path inside
   `plans/sealed50/` (absent today, F5), and never a 40-hex hash that is not already an ancestor.

## Risks

- **R1 (can kill C2, high).** Any `plans/…`/`corpus/…` path with an `EXTS` extension, or any 40-hex
  hash, added to `PROVINCE.md` becomes a C2 pointer (`plans/round50_c2_audit.py:41-45`). Writing
  `plans/sealed50/<name>.py` before S2 lands it → `unresolved=1` → C2 kill rule fires. *Mitigation:*
  name directories (`plans/sealed50/`) or already-existing files only.
- **R2 (novelty, medium).** Presenting the instrument as "one command, four legs" invites a judge to
  locate novelty in the mutant leg, which is pre-empted by tameshi and kumitate and already reported
  out by kengaku in round 37. *Mitigation:* move 1.
- **R3 (conformance, medium).** Without the registry row, `PROTOCOL.md:420-421` blocks conformance
  regardless of a passing predicate — a green run with an unregistered gate is still not conformant.
  *Mitigation:* move 2.
- **R4 (over-claim, low).** tameshi admits a pattern as general only "from evidence in **TWO
  independent lanes**" (`tameshi-shokunin/PROVINCE.md:15-16`). C1 must therefore claim **no** general method — only
  its own gate. Both the claims file and the round report must keep that scoping.
- **R5 (false positive, low).** The exit-2 arm exists (F7); do not "fix" it. Recording F7 here is
  the mitigation against a sibling re-filing it.

## Limits

- Read-only text scan. I executed **no** lane instrument and **no** sibling gate (PROTOCOL's Closure
  consequence reserves sibling-gate execution to nobody at this seat; the integrator verifies
  committed evidence). The counter's behaviour is read from source, not measured here; its measured
  behaviour is C1's own S3 receipt.
- `PROVINCE.md` files were read in the **working tree** of each sibling (see REV lines for the exact
  HEAD); sibling worktrees may be dirty — I did not check `git status` on them and do not claim the
  text is at the commit, only that the file is at that HEAD's checkout.
- 20 of 21 sibling git repos carry a `PROVINCE.md`; the sweep covered all 20 files found. One
  sibling (`kengaku`) is my own lane. `AGENTS.md`/`SKILL.md` were consulted only where `PROVINCE.md`
  pointed at them (tameshi recipe, kumitate registry, kotoba census).
- The "no sibling owns git fixture geometry" result is a **negative** from a keyword sweep plus
  direct reads of the three near-hit provinces. It is not a proof over every sibling document; a
  claim hidden in a knowledge entry without those keywords would not be caught.
- I did not evaluate whether the 126-fixture population's *composition* is honest — that is the
  population seat's and the critic's job.
- No claim of R50-C1 or R50-C2 admission is made. No production file was edited; `SCORECARD.md`,
  `LOG.md`, `corpus/` untouched.

## VERDICT

**Sibling ground is clear: nothing to absorb.** "Git fixture geometry" is owned by no sibling — the
nearest rows (`souji-shokunin/PROVINCE.md:3,66,91`; `kumitate-shokunin/PROVINCE.md:15`) observe live
repos for hygiene or contain seats, and neither builds a frozen fixture population.
"Sandbox admission" is kumitate's for the fleet runner and kengaku already conceded it twice
(`PROVINCE.md:311,339`). `kumitate` does **not** own tool-instrument standards — `PROTOCOL.md:375-419`
does, and kengaku's registry home is its own `SKILL.md:560`.

**The novelty axis is improved, in one specific way:** the owning sibling method (tameshi) is
evidenced as **single-directional** (`tameshi-shokunin/SKILL.md:481-484`), so C1's honest-geometry
over-refusal denominator is an uncovered direction rather than a duplicate — provided C1 stops
advertising the four legs equally and states the mutant leg as an application.

**Two routed defects for L1, both conformance-shaped, neither a sibling-overlap question:**
(1) no `round50` row at `kengaku-shokunin/SKILL.md:560` blocks PROTOCOL conformance
(`PROTOCOL.md:420-421`); (2) C1's routing sentence, if written into `PROVINCE.md`, becomes C2
pointer surface and can fire C2's kill rule (`plans/round50_c2_audit.py:41-45`) — `plans/sealed50`
is absent today.

No admission claimed. Scratch tree removed.
