# C2ConnTooling — round 51 w1 connector: ownership map for the orchestration/tooling classes

**Seat:** `C2ConnTooling` (connector, leaf — no subagent dispatch). **Item:** decide the owner for the
classes about scratch guards, wave dispatch, prompt craft and citation pins; quote the sibling lines;
return a class → owner table; name every class no sibling owns.
**Axes named:** **adjacency** (C2, the axis this seat measures). **freshness** (C1) is named and left
untouched: no row below proposes a change to a `## Surfaces` / `### Core` table row. One proposal
(§7 R2) appends prose to `PROVINCE.md`, which is C1's anchor file — the interaction is stated there,
not smoothed.
**Revision measured:** `REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7` (lane HEAD, detached).
Stage-1 freeze commit for the binding file: `e07f131cf7037e58a21db6e1f3986cf401ad257c`
(`git log -1 --format=%H -- plans/round-51-claims.md`). Lane tree carries the wave's untracked
`.ufo/waves/round-51/**` files only; no production file was written by this seat.

## 1. What binds the answer

Read in full, in this order: `plans/round-51-claims.md` (the frozen claims), `plans/round51_routing.py`
(the frozen C2 instrument), `corpus/routed-findings.jsonl` (71 rows), then
`kumitate-shokunin/PROVINCE.md` and `kotoba-shokunin/PROVINCE.md` (the two provinces my item names),
plus the three provinces that decide the negative space — `mori-shokunin/PROVINCE.md`,
`souji-shokunin/PROVINCE.md`, `chousa-shokunin/PROVINCE.md` — and kengaku's own `PROVINCE.md` /
`SKILL.md` / `plans/scratch_guard.py`.

The counter's owner test is not "does a human believe this lane owns it". It is
`plans/round51_routing.py:56-68`:

```python
def load_owners(fleet: Path) -> set[str]:
    conf = fleet / "shokunin.conf"
    owners = set(FALLBACK_OWNERS)
    if conf.is_file():
        for line in conf.read_text(errors="replace").split("\n"):
            m = re.match(r"\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{", line)
```

with `FALLBACK_OWNERS` = `{kengaku, kama, kagi, kake, kasegi, kumitate, kotoba, kaidoku, souji, tabi,
mori, chousa, kotodama, tameshi, protocol, aggregator, unowned:integrator}`, and the further rules
`owner == "kengaku"` is refused for `routed`/`referral` rows, and those rows must carry `next`.
Every owner cell in §2 is one of those 17 strings, so it is acceptable to the counter as frozen.

## 2. Class → owner table

`rows` are the `id`s present in `corpus/routed-findings.jsonl` at this REV that fall in the class
family. "Disposition shape" is the shape the C2 predicate admits for that owner, not a per-row ruling.

| class family | owner | disposition shape | basis (sibling line) | rows at this REV |
|---|---|---|---|---|
| **scratch guard** — sentinel-bound shared scratch root, `check`/`safe-rm` exit contract, guard selftest, guard registry row | **`kengaku`** (self) | `fixed-verified` when the tool's own check is green; `accepted-risk` where the lane already refused | no sibling declares the artifact: kumitate's scope line is `**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime` (`kumitate-shokunin/PROVINCE.md:3`) and its only scratch-root surface is its *own* sighting script's `DEFAULT_SCRATCH_ROOT` (`kumitate-shokunin/corpus/knowledge/sighting-wall.md:170`); souji owns residue listing, not the guard (`souji-shokunin/SKILL.md:381`); mori reports runway and refuses the mechanism (`mori-shokunin/PROVINCE.md:12`). The tool is in-lane and registered: `plans/scratch_guard.py:1` and `SKILL.md:608` | `R39-R5`, `R42-R2`, `R42-R2.1`, `R42-R2.2`, `R42-R6`, `R42-R3-26`, `R42-R3-27` (7 by class name); `R42-R3-25`, `R42-R3-28` (2 more pin `scratch_guard.py` under other class names) |
| **wave dispatch** — plan/run/record/collect semantics, task-call shape, registry, retry, re-dispatch, result acceptance | **`kumitate`** | `routed` + `next` (non-kengaku owner) | `kumitate-shokunin/PROVINCE.md:3`; `:24` "orchestration topology **decisions** (how a wave's seats are arranged …)"; `mori-shokunin/PROVINCE.md:46` "kumitate owns orchestration/result semantics"; `:136-137` "Planning, slot acquisition, retrying and adjudicating dispatch remain **kumitate/operator**-owned"; `chousa-shokunin/PROVINCE.md:10-11` "orchestration, multi-agent dispatch and agent lifecycle (→ kumitate …)"; `kotoba-shokunin/PROVINCE.md:68` "kumitate owns dispatch/orchestration tooling" | **none** — 0 of 71 rows name a dispatch class |
| **wave settlement reporting** — did a member's report file exist / settled-partial | **`mori`** for the reading, **`kumitate`** for acceptance | `routed` + `next` | `mori-shokunin/PROVINCE.md:150` "result acceptance and re-dispatch stay **kumitate**'s; a misrooted file is routed to its lane L1" | none |
| **dispatch-prompt craft** — seat prompt wording, output contract, guard-sentence phrasing | **`kotoba`** | `routed` + `next` (the *rule*); the instance text stays in-lane `kengaku` | `kotoba-shokunin/PROVINCE.md:3` "**Domain:** prompt & skill craft — scopes SKILL.md/AGENTS.md quality, trigger fidelity"; `:13` "Agent-definition, always-on (AGENTS.md-class) and **dispatch-prompt craft**"; `kumitate-shokunin/PROVINCE.md:28` "Prompt and skill craft → kotoba."; `kotoba-shokunin/PROVINCE.md:68` "kotoba owns the wording, kumitate the runtime" | **none** — 0 of 71 rows name a prompt class |
| **citation pins inside kengaku's own committed artifacts** — a claim pinned to a line/anchor/pointer that does not carry it | **`kengaku`** (self) | `fixed-verified` (re-read the pinned bytes) | nobody owns a line pin inside another lane's file: chousa owns the *method* (`chousa-shokunin/PROVINCE.md:5` "citation chaining and hop resolution; claim-vs-source verification"); kotoba owns compound-clause citation "on **this lane's** scoped-rule Action cells" (`kotoba-shokunin/PROVINCE.md:27`). kengaku already cedes the method: `PROVINCE.md:137`, `:262` "capture and citation method stay chousa's" | `R42-R3-02`, `R42-R3-04`, `R42-R3-05`, `R42-R3-06`, `R42-R3-13`, `R42-R3-14`, `R42-R3-16`, `R42-R3-22`, `R42-R3-29`, `R42-R3-30`, `R42-R3-39`, `R45-S5-1` (12) |
| **external claim-vs-source** — does the cited page support the sentence | **`chousa`** | `routed` + `next` | `chousa-shokunin/PROVINCE.md:5` (same line as above) | none in the ledger today |

The three open guard rows (`R42-R6`, `R42-R3-26`, `R42-R3-27`) are the same defect seen three times
(exit 2 promised, exit 1 printed, no selftest case) and are attributable to `kengaku` with a check
that is red today — legal under the predicate, which only runs checks for `fixed-verified` rows.

## 3. Classes no sibling owns → `unowned:integrator`

| class | why no sibling owns it | evidence |
|---|---|---|
| **U1 — the hyaku wave driver instance** (`scripts/hyaku/`: `wave-slot.sh`, `disk-guard.sh`, `inline-dispatcher.py`, `wave-live.py`, `append-closure.py`) | kumitate's scope line enumerates `OMP task/hub, ufo-fsd scripts & runtime` (`kumitate-shokunin/PROVINCE.md:3`); the hyaku scripts are fleet-root, not `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/`. Measured: `grep -n -i 'hyaku' kumitate-shokunin/PROVINCE.md kumitate-shokunin/SKILL.md` → no output. mori *records* the assignment (`mori-shokunin/PROVINCE.md:136-137` "**kumitate/operator**-owned") without kumitate's province naming the surface | `ls scripts/hyaku` → `wave-slot.sh` present; 0 hits for `hyaku` in kumitate's province and skill |
| **U2 — fleet-wide scratch-root policy** (every hyaku seat's root carries a sentinel; a seat removes its own tree before yield) | the *tool* is kengaku's, the *rule over other lanes' seats* is nobody's: kumitate names no scratch surface, souji owns removal of residue (`souji-shokunin/PROVINCE.md:8` "stray checkpoint/scratch files"), mori owns the runway reading (`mori-shokunin/PROVINCE.md:10`, `:26`) | `kumitate-shokunin/PROVINCE.md` has 0 occurrences of "scratch"; the only fleet-wide sentence lives in this round's seat contexts |
| **U3 — line-level citation pins as a fleet rule** | chousa owns the method, not another lane's artifact; kotoba owns its own cells; no province claims "a lane's own committed line pins are checked" as a rule | `chousa-shokunin/PROVINCE.md:5`; `kotoba-shokunin/PROVINCE.md:27` |

`unowned:integrator` is a member of `FALLBACK_OWNERS` (`plans/round51_routing.py:44-45`), so these
three classes can be attributed today without touching the counter.

## 4. Contradictions stated, not smoothed

**C-a — "dispatch-prompt craft" is claimed by kotoba; "how a wave's seats are arranged" by kumitate.**
`kotoba-shokunin/PROVINCE.md:13` claims `dispatch-prompt craft`; `kumitate-shokunin/PROVINCE.md:24`
claims `orchestration topology **decisions** (how a wave's seats are arranged: which topology, what a
coordinator may delegate, what the arrangement costs)`. Both sentences are true if "craft" means the
words and "arrangement" means the roster. The split is stated **on kotoba's side only** —
`kotoba-shokunin/PROVINCE.md:68` "kotoba owns the wording, kumitate the runtime, and neither edits the
other's SKILL.md" — while kumitate's province states no reciprocal sentence (its `:28` routes
"Prompt and skill craft → kotoba" without naming dispatch prompts). This is the same one-sided shape
kotoba records for tsukuroi (`PROVINCE.md:74` row: "a split stated on kotoba's side alone"). Do not
read it as a settled tie-break; read it as a wording-vs-runtime split with one signatory.

**C-b — a sibling's record attributes a surface its province does not name.**
`mori-shokunin/PROVINCE.md:136-137` says "Planning, slot acquisition, retrying and adjudicating
dispatch remain **kumitate/operator**-owned; `wave-slot.sh` grant lines are recorded as evidence
only", but `wave-slot.sh` is `scripts/hyaku/wave-slot.sh` at the fleet root and kumitate's scope line
names ufo-fsd scripts and the OMP task/hub. Either kumitate's scope line is narrower than its actual
dispatch surface, or U1 belongs to the integrator. I record both readings and do not choose one for
the lane; the table above resolves it as *semantics → kumitate, hyaku instance → unowned:integrator*.

**C-c — two lanes own "citation", neither owns a line pin.**
`chousa-shokunin/PROVINCE.md:5` "citation chaining and hop resolution; claim-vs-source verification";
`kotoba-shokunin/PROVINCE.md:27` "Compound-clause citation on this lane's scoped-rule Action cells".
Neither sentence reaches a line pin inside kengaku's corpus, so the 12 rows in §2 are kengaku's by
artifact ownership — not by sibling grant. This matters for C2: marking them `routed` to chousa would
be false (chousa never edits this lane's bytes) and the counter would also demand a `next` that
chousa has no reason to accept.

## 5. Findings for the L1 (each with the check that proves it)

**F1 — `PROVINCE.md:262` pins kotoba's wording rule at the wrong line.**
The sentence: "prompt/skill wording stays kotoba's (`kotoba-shokunin/PROVINCE.md:61`)".
`kotoba-shokunin/PROVINCE.md:61` is the **kagi** row:
`| kagi | adjacent | 69b61db4… | kagi owns secrets and vault ops, credential custody and hygiene
evidence …`. The supporting line is `:68`: "kotoba owns the wording, kumitate the runtime, and
neither edits the other's SKILL.md" (or `:3`, the domain line).
Class: citation-pin (the `entry-wrong-citation` family). Owner `kengaku`.
Check that is red today: `sed -n '61p' kotoba-shokunin/PROVINCE.md | grep -q 'kotoba owns the wording'`
→ exit 1. Check that is green after the fix: same against `68p` → exit 0.

**F2 — the same line pins kumitate's seat-arrangement rule at the wrong lines.**
The sentence: "seat arrangement, not evaluation, stays kumitate's
(`kumitate-shokunin/PROVINCE.md:23,28`)". `:23` is the durable-execution entry; `:28` is the
Adjacent routing line `Local model serving and endpoints → kama. Prompt and skill craft → kotoba.
Research method → chousa.` The seat-arrangement sentence is `:24` ("how a wave's seats are arranged").
Class: citation-pin. Owner `kengaku`.
Check: `sed -n '24p' kumitate-shokunin/PROVINCE.md | grep -q "how a wave's seats are arranged"` → 0.

**F3 — the counter cannot accept 7 of the fleet's lanes as owners, contradicting its own claim text.**
`load_owners` parses `shokunin.conf` with `^\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{`. Measured:
`conf lane-rows matching counter regex: 0` — the conf lists lanes as `lane|repo|axes` inside
`LANES="…"`. So `load_owners` returns exactly the 17 `FALLBACK_OWNERS`:
`['aggregator','chousa','kagi','kaidoku','kake','kama','kasegi','kengaku','kotoba','kotodama','kumitate','mori','protocol','souji','tabi','tameshi','unowned:integrator']`,
and `game-dev-2d in? False | tsukuroi in? False | revenger in? False` (also absent: `game-dev-3d`,
`lore`, `mado`, `audio`). A correct attribution to any of those lanes prints
`owner %r not a fleet lane` and fails the predicate — while `plans/round-51-claims.md` §C2 promises
"every `owner` names a fleet lane from `../shokunin.conf`". This is a live hazard for the wave's
attribution seats, not a theoretical one: `tsukuroi` owns host hooks, `revenger` owns RE ledgers,
`game-dev-2d/3d` own engine work, and rows in those domains will be opened eventually.
Reproduce: `python3 -c "import importlib.util as u; …load_owners(Path('.').resolve().parent)"` → `n= 17`.

**F4 — the counter's `SOURCE` test is file-granular, so a wrong line pin passes.**
`src = (r.get("source") or "").split(":")[0]` — only the path is tested for existence. Measured:
`SOURCES resolved=71 missing=0`. Concrete counterexample in the ledger: `R42-R2.2`'s source is
`SKILL.md:562`, and `SKILL.md:562` is the registry **table header**
(`| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |`), not a row
about the guard. The predicate says "every `source` pointer resolves in the lane"; at line
granularity it does not. If C2 is to carry the citation class at all, this is the hole that lets a
`fixed-verified` attribution cite nothing.

**F5 — two closed rows assert a registry absence that is false at this REV.**
`R42-R2.2` ("The landed guard has no SKILL.md registry row (grep -c … -> 0 at d33350f)") and
`R42-R3-28` ("The landed guard has no SKILL.md registry row (grep -c -> 0; PROVINCE.md 0, README.md
0; only LOG.md:1299 mentions the landing once)") are both `closed`, and the row now exists:
`SKILL.md:608` `| \`scratch-root-guard\` | gate | \`python3 plans/scratch_guard.py check <root>\` and
\`python3 plans/scratch_guard.py safe-rm <root> <seat> <path>\` …`. A `fixed-verified` attribution
needs a check that is green now: `grep -q '^| `scratch-root-guard`' SKILL.md` → 0. The *notes* are
stale; the *status* is right.

**F6 — no row in the ledger carries a dispatch or prompt class (measured: 0 of 71).** The two families
my item asks about have no rows to attribute this round. That is a fact about the ledger, not a gap in
the map: attribution seats must not invent rows for them (the claim's kill rule forbids adding a row
without an owner, and the row count is a state record at 71).

## 6. Commands run and verbatim outputs

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
export TMPDIR=/fast/scratch/hyaku/kengaku-r51/C2ConnTooling
git rev-parse HEAD                      # 4090c3db79d11279ab5e5121ba25e74aa316e6e7
git log -1 --format=%H -- plans/round-51-claims.md
                                        # e07f131cf7037e58a21db6e1f3986cf401ad257c
python3 plans/round51_routing.py --lane .
```
Verbatim (no `--run-checks`, so no check is executed and nothing in the lane is written):

```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
PREDICATE R51-C2 fail
real_exit=1
```

Owner-set measurement (imports the frozen instrument's own function, read-only):

```
n= 17
['aggregator', 'chousa', 'kagi', 'kaidoku', 'kake', 'kama', 'kasegi', 'kengaku', 'kotoba',
 'kotodama', 'kumitate', 'mori', 'protocol', 'souji', 'tabi', 'tameshi', 'unowned:integrator']
game-dev-2d in? False | tsukuroi in? False | revenger in? False
conf lane-rows matching counter regex: 0
```

Family census over the 71 rows:

```
guard-family n=7 ['R39-R5', 'R42-R2', 'R42-R2.1', 'R42-R2.2', 'R42-R6', 'R42-R3-26', 'R42-R3-27']
citation-family n=12 ['R42-R3-02', 'R42-R3-04', 'R42-R3-05', 'R42-R3-06', 'R42-R3-13', 'R42-R3-14',
 'R42-R3-16', 'R42-R3-22', 'R42-R3-29', 'R42-R3-30', 'R42-R3-39', 'R45-S5-1']
dispatch/prompt-family n=0 []
statuses guard: [('R39-R5','closed'), ('R42-R2','closed'), ('R42-R2.1','closed'),
 ('R42-R2.2','closed'), ('R42-R6','open'), ('R42-R3-26','open'), ('R42-R3-27','open')]
```

Read-only citation checks used for F1/F2/F4/F5 (`sed -n`/`awk` over sibling and lane files; no
mutating git command was run anywhere):

```
awk 'NR==61 || NR==68 {…}' kotoba-shokunin/PROVINCE.md      # :61 = kagi row, :68 = kumitate row
awk 'NR>=22 && NR<=28 {…}' kumitate-shokunin/PROVINCE.md    # :23 durable exec, :24 arrangement, :28 routing
awk 'NR>=560 && NR<=563 {…}' kengaku-shokunin/SKILL.md      # :562 header, :608 the guard row
```

Exit codes of the four checks the findings name (run from `/home/vgpnk/Projects/shokunin`):

```
sed -n '61p' kotoba-shokunin/PROVINCE.md  | grep -q 'kotoba owns the wording'          -> 1
sed -n '68p' kotoba-shokunin/PROVINCE.md  | grep -q 'kotoba owns the wording'          -> 0
sed -n '24p' kumitate-shokunin/PROVINCE.md| grep -q "how a wave's seats are arranged"  -> 0
sed -n '23p' kumitate-shokunin/PROVINCE.md| grep -q "how a wave's seats are arranged"  -> 1
grep -q '^| `scratch-root-guard`' kengaku-shokunin/SKILL.md                            -> 0
```

## 7. Proposed move (one, bounded) and its risks

**Move:** land the §2 table as the attribution key for the 19 rows it names — 7 guard rows and 2
guard-artifact rows to `kengaku`, 12 citation rows to `kengaku`, with the check being the re-read of
the pinned bytes — and land F1/F2 as **one appended correction paragraph** at EOF of `PROVINCE.md`,
naming `kotoba:61 → 68` and `kumitate:23,28 → 24`. Do not rewrite `:262` in place: the lane's
record-correction rule is append-only (`corpus/QUALITY.md:759`, cited by `R42-R3-24`), and the C1
manifest's anchors are text prefixes, not line numbers (measured: first entry
`"anchor": "| Research notes (SSOT for eval craft) |"` in `plans/round51-surfaces.json`), so an EOF
append cannot move them.

**Risks.**
- **R1 (freshness):** the appended paragraph sits in C1's `anchor_file`. It is prose, so it cannot
  create an `ANCHOR-DUP`; but if the correction is written as a *table* whose first cell repeats an
  existing anchor prefix, `ANCHOR-DUP` fires. Write prose.
- **R2 (adjacency, self-inflicted):** F3's fix (`plans/round51_routing.py`) edits a frozen
  instrument. The claims file froze the counter; changing its owner parser after the freeze needs an
  L1 erratum line in the landing note, and the change must be shown not to loosen the predicate (it
  only widens the accepted owner set to the lanes the conf already declares). If the L1 will not
  touch the frozen counter, then every attribution this round MUST stay inside the 17 fallback names —
  which is why §2 uses only those.
- **R3:** F1/F2 make two *new* defects visible in a file the lane has already published; the
  correction paragraph should name them as corrections, not silently restate the sentences, or a
  future spot-check will read it as a third in-place rewrite (`R45-S5-3` class).

## 8. Limits

- This is an ownership map, not an attribution run. I did not assign `disposition`, `close` or
  `check` per row beyond the shape each owner permits; that is the L1's integration call.
- The map is read at `REV 4090c3db…`. Sibling provinces were read from their working trees, not at
  pinned commits; if a sibling edits `PROVINCE.md` mid-wave, the quoted lines can move.
- The negative-space claims (U1–U3, F3's absent lanes) are greps over province/skill text, not proof
  that a sibling's *corpus* never discusses the class. `kumitate-shokunin/corpus/knowledge/sighting-wall.md:170`
  does discuss scratch roots — as a parameter of its own script. I report the province boundary, which
  is what a sibling's ownership claim is written in.
- No sibling was messaged; the item is self-contained and the L1 owns integration. No subagent was
  dispatched (leaf member).

## 9. Scratch

`/fast/scratch/hyaku/kengaku-r51/C2ConnTooling` was created and used as `TMPDIR` for the one counter
run and its captured output; it was removed before this report was finalised (verified absent). No
fixture git repository was created, so no `git -C "$D"` fixture call was made. No committed tool was
touched; nothing citable lives outside this wave directory and the lane tree.

VERDICT: adjacency — owner map returned. Scratch guards → `kengaku` (self, 9 rows incl. 2
guard-artifact rows under other class names); wave dispatch → `kumitate` (0 rows today);
dispatch-prompt craft → `kotoba` for the rule, `kengaku` for the instance (0 rows today); citation
pins in-lane → `kengaku` (12 rows); external claim-vs-source → `chousa`. Three classes are
`unowned:integrator` (hyaku wave driver instance, fleet-wide scratch-root policy, line-pin rules as a
fleet rule). Two citation pins in `PROVINCE.md:262` are wrong at this REV (F1, F2), and the frozen
counter rejects 7 of the fleet's lanes as owners while its claim text promises they are accepted (F3).
No production file written; report complete.
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
