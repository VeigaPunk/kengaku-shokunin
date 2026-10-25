# R33ScorecardPatch — SCORECARD `## Round 32` section + `## Round 33` skeleton (routed defect N2)

Seat: scribe (leaf, no dispatch). Date: 2026-10-25. Lane: `kengaku-shokunin`.
Access date for every source opened this round: 2026-10-25.
Wrote nothing outside this file. No tool installed or upgraded.

## 0. Premise correction (read first — the state moved before this seat ran)

The assignment says the `## Round 32` section is missing. It is **not missing at this seat's start**.

| Observation | Command | Output |
|---|---|---|
| lane HEAD | `git rev-parse HEAD` | `78955888542258ba369f5aa72c200c913b4c3c90` (detached) |
| section present | `grep -n '^## Round 3[0-9]' SCORECARD.md` | `1094:## Round 32 …`, `1122:## Round 33 …` |
| section committed | `git log --oneline -1 -- SCORECARD.md` | `7895588 round-33: C2 routed-defect repairs (N2 scorecard section, N5/N6 lesson errata), Q22, defects-after receipt` |
| N2 counter | `python3 plans/round33_defects.py --lane .` | `checks=6 defects=0`, `exit=0` |

`7895588` (2026-10-25 14:16:45 -0300) touched `SCORECARD.md` (+41), `corpus/QUALITY.md` (+18),
`corpus/evidence/round33/defects-after.txt` (+5), `corpus/lessons/round-30.md` (+9),
`corpus/lessons/round-31.md` (+9). `git status --porcelain -- SCORECARD.md` → empty: the section is
committed and unmodified. The worktree carries 14 in-flight entries from sibling seats
(`corpus/README.md`, `corpus/SOURCES.md`, the two knowledge entries, `plans/round33_c1_verify.py`,
`.ufo/waves/round-33/assimilation/`, `corpus/evidence/round33/catalogs/`, `corpus/lessons/round-33.md`);
none touch `SCORECARD.md`.

Consequence for integration: a second `## Round 32` heading must **not** be appended. The text below
is a replacement/patch for lines 1094-1121, not an insertion. Appending it would create a duplicate
heading that `check_n2` (`re.search(r"^## Round 32\b", …, re.MULTILINE)`, `plans/round33_defects.py:92-97`)
still passes, so the counter cannot catch that mistake — the L1 must.

## 1. Sources read (each opened this seat)

| Source | What it established |
|---|---|
| `.ufo/reports/round-32/kengaku.md` (fleet) | baseline `f20a1097`; landed tip `bcd2a6c0d49e…`; freeze `0d32691d`; shape 34 build + 34 falsify; the three dispositions; the `a44b5a8`/`112091c` addendum |
| `corpus/lessons/round-32-verifier-spotcheck.md` | non-author closure; C1 receipt quoted verbatim; C2 "seven routed defects"; C3 "failed as declared"; ten untracked wave paths |
| `corpus/lessons/round-32.md` | §Gate, §Mistakes (4 rows), §Round-31 routed defects, §Assimilation (`:25`), §C3 catalog probe |
| `plans/round-32-claims.md` | the seven checks are labelled **R1–R7**; freeze control semantics |
| `.ufo/waves/round-32/claims/{control-nothing,defects-before,catalogs-before}.txt` | the exact before-lines quoted below |
| `corpus/evidence/round32/{adoption-after,defects-after}.txt`; `corpus/evidence/round32/catalogs/after.txt` | the exact after-lines quoted below |
| `.ufo/waves/round-32/build/R32DraftRows.md:106-126`; `falsify/FxKillRule.md:25-40` | the draft-state counter lines (`census=skipped`) |
| SCORECARD.md rounds 29-31 | heading/paragraph/table conventions being matched |
| `plans/round33_defects.py`, `.ufo/waves/round-33/claims/*` | N2 check body; round-33 before-lines |
| `.ufo/reports/round-31/kengaku.md:226-246`; `corpus/lessons/{round-30,round-31}.md` errata tails | N3/N5/N6 state (context only; not this seat's repair) |

## 2. VERBATIM `## Round 32` section

<!-- BEGIN SCORECARD ## Round 32 (replacement for SCORECARD.md:1094-1121) -->

## Round 32 (hyaku run 6, 2026-10-25): assimilation refusal, routed-defect partial, catalog freshness failure

Baseline `f20a1097` (lane HEAD before the round); landed lane tip `bcd2a6c`; non-author closure
`112091c`. Frozen prereg `plans/round-32-claims.md` (freeze `0d32691d`). Lowest non-retired axis:
**coverage 7**, tied with novelty 7; tie-break "most falsifiable with sources an on-host tool can
open"; no stagnation waiver (saturation line 8, novelty below it, a capability row entered at round
31). Round shape: two v1 waves, 34 build + 34 falsify seats in the surviving registries
(`.ufo/waves/round-32/{build,falsify}/swarm-registry.json` → `len(members)=34` each). **This section
lands late, under round 33:** round 32 closed with no `## Round 32` section at its own tip, which is
routed defect N2. Lateness is calibration debt the round incurred; it is not a pass earned
retroactively. Nothing here is re-scored: C1 was refused, C2 is incomplete, C3 failed as declared.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 shokuknow assimilation round 4 — grader-semantics entry under staged ids | **coverage** (lowest non-retired, tie-break) | before: `python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json --census` → `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` exit 1 (freeze control `.ufo/waves/round-32/claims/control-nothing.txt`, expect sha256 `a1a7e860…`) → after: same command → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=fail` exit 1 (`corpus/evidence/round32/adoption-after.txt`), where `census=fail` is the duplicate-id finding that forced the refusal, not a citation failure; the wave's draft-state measurement was `entries=1 indexed=1 cited_rows=3 rows_present=1 rows_mined=1 usedby_ok=0 census=skipped`, rc=1 (`.ufo/waves/round-32/falsify/FxKillRule.md:32`; `build/R32DraftRows.md:121`) — staged S094/S097 collided with live ids and staged S101/S102 identify unrelated SWE-bench sources | **7 → 7 held — refused as declared**; four rejected correction rows recorded (S094, S097, S101, S102), the committed draft stays unadmitted, registry delta 0 |
| C2 calibration — the seven routed defects R1–R7 | **calibration** | before: `python3 plans/round32_defects.py --lane .` → seven `DEFECT R1…R7` lines, `checks=7 defects=7`, exit 1 (`.ufo/waves/round-32/claims/defects-before.txt`) → after: same command → `checks=7 defects=5`, exit 1 (`corpus/evidence/round32/defects-after.txt`, self-labelled "This is not the claimed after-state"); R3/R4 landed (round-31 CLI receipt regenerated from the committed fixtures with a resolving path; `plans/sources_adopt.py` row in `SKILL.md`), R1/R2/R5/R6/R7 remained red | **8 → 8 held — incomplete**; a partial receipt is not closure |
| C3 freshness — public model catalogs re-probed | **freshness** | before: `python3 plans/catalog_probe.py --diff --lane .` → `probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=stale`, exit 1 (`.ufo/waves/round-32/claims/catalogs-before.txt`) → after: `probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=ok`, HF missing fields `author, sha, lastModified, gated` (`corpus/evidence/round32/catalogs/after.txt`) — a summary receipt that says of itself "it is not the raw response" | **8 → 8 held — failed as declared**; the frozen zero-delta predicate cannot honestly pass against a four-field default-projection gap, and it was not relabelled after scoring |

Other axes held: depth 9 (no new instrument claim), novelty 7 (no prior-art or phenomenon claim),
adjacency 8 (the sibling connector found no contest; `PROVINCE.md` unchanged), operability 8 (no gate
change), freshness 8 (the score held although C3 failed as declared — no axis move), coverage 7 (no
admitted entry). The non-author closure `corpus/lessons/round-32-verifier-spotcheck.md` re-derived C1
from committed id lists and the receipt and confirmed all three dispositions; it also recorded the
residual defect of ten untracked wave paths (84 files) at the pushed tip, closed by round-33 commit
`c227e486` — at this drafting tip `git ls-files .ufo/waves/round-32 | wc -l` → 89 and
`git status --porcelain .ufo/waves/round-32 | wc -l` → 0. Nothing in this section claims a pass round
32 did not earn.

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| — none — | the round landed no new capability; the C1 candidate was refused and C3 failed as declared | `corpus/lessons/round-32.md` | — |

Corrections carried (as the round already published them): the staged S094 row misstated the executed
tolerance — 0.05 at the call site, not the 0.1 signature default — and overbroadened the fail-open
claim: credential failures fall through to an implicit `None`, which fails closed; the staged S097
anchor omitted one `L` in "LLMs-as-judges". The fail-open correction is in
`corpus/lessons/round-32.md` §Mistakes (`:23`); the tolerance and citation corrections are in
§Assimilation (`:25`).

<!-- END SCORECARD ## Round 32 -->

## 3. VERBATIM `## Round 33` skeleton

<!-- BEGIN SCORECARD ## Round 33 (replacement for SCORECARD.md:1122-1133) -->

## Round 33 (hyaku run 7, 2026-10-25): renumbered assimilation, routed-defect closure, byte-retained catalogs

Baseline `112091c2d9077e484b53512ca363d2fe6ba6fc5c` (local = remote, `ahead=0`); frozen prereg
`plans/round-33-claims.md` (freeze `f0b20aea`, inherited-state commit `c227e486`). Lowest non-retired
axis: **coverage 7**, tied with **novelty 7**; no stagnation waiver (saturation line 8, novelty below
it, a capability row entered at round 31). Three claims, three distinct axes, frozen before any wave
seat ran; a predicate changed after a seat has scored is not this claim's predicate. **Every row below
is frozen at `f0b20aea`; measurements follow at landing.**

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 grader-semantics entry admitted under renumbered ids S103/S104 (staged S094/S097 re-pointed by document across S093/S103/S104) | **coverage** (lowest non-retired, tie-break) | before: `python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census` → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=ok` exit 1 (freeze control `.ufo/waves/round-33/claims/control-nothing.txt`, expect sha256 `fbd7b47e…`) → after: _frozen at `f0b20aea`; measurements follow at landing_ | **frozen at `f0b20aea`; measurements follow at landing** |
| C2 six routed defects N1–N6 closed | **calibration** | before: `python3 plans/round33_defects.py --lane .` → `checks=6 defects=6` exit 1 (`.ufo/waves/round-33/claims/defects-before.txt`) → after: _frozen at `f0b20aea`; measurements follow at landing_ | **frozen at `f0b20aea`; measurements follow at landing** |
| C3 catalog re-probe with committed bounded raw bytes and sha256 digests | **freshness** | before: `python3 plans/catalog_probe.py --verify --lane .` → `raw=absent` exit 1 (`.ufo/waves/round-33/claims/control-verify.txt`) → after: _frozen at `f0b20aea`; measurements follow at landing_ | **frozen at `f0b20aea`; measurements follow at landing** |

No score above the round-32 table is claimed until the three counters print at landing; the
round-32 rows and their verdicts stand as written.

<!-- END SCORECARD ## Round 33 -->

## 4. Delta against the currently landed section (so the L1 patches, not duplicates)

The landed section (SCORECARD.md:1094-1121) is close; my draft differs in five places. Four are
corrections, one is an addition:

1. **C1 after-counter is misquoted.** Landed: `… rows_mined=1 usedby_ok=0 census=fail` citing
   `corpus/evidence/round32/adoption-after.txt`. That file (unchanged since its only commit
   `bcd2a6c`, `git log --oneline -- corpus/evidence/round32/adoption-after.txt`) prints
   `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=fail`, exit 1 —
   the closure quotes the same line verbatim
   (`corpus/lessons/round-32-verifier-spotcheck.md` §2 C1). My draft quotes the receipt and keeps
   `rows_mined=1 usedby_ok=0` as the separately-cited draft-state line with its true token
   `census=skipped`.
2. **Defect labels.** Landed C2 row says "the seven routed defects **D1–D7**". The round-32 counter
   prints `R1…R7` and the claim file names them R1–R7 (`plans/round-32-claims.md:64-73`);
   D1–D6 belong to the round-**31** closure's item list. My draft says R1–R7.
3. **Correction provenance.** Landed: "All three are in `corpus/lessons/round-32.md` §Mistakes." The
   §Mistakes table carries the fail-open row only; the tolerance and the dropped-`L` statements are
   in §Assimilation (`:25`). My draft names both sections.
4. **Axis lines.** Landed "Other axes held" omits operability/freshness and states no closure-verified
   counts. My draft keeps the same register but lists every axis and the tracked-path counts.
5. **Addition:** the C1 cell now explains that `census=fail` is the duplicate-id finding (the refusal
   cause), so a reader cannot mistake it for a missing citation.

The `## Round 33` skeleton in both versions carries the same three before-lines; the only difference
is that each of my rows and verdict cells carries the literal marker
`frozen at f0b20aea; measurements follow at landing`, as the seat's acceptance requires.

## 5. Findings, reported verbatim for the canonical judge

**F1 — the assignment's C1 counter string exists in no committed artifact.**
Requested cell: `entries=1 rows_mined=1 usedby_ok=0 census=fail exit 1`. Exhaustive check:
`grep -rn 'rows_mined=1' --include='*.md' --include='*.txt' --include='*.json' .` returns exactly
three *distinct* states, none matching:
- `.ufo/waves/round-32/build/R32DraftRows.md:121` and `.ufo/waves/round-32/falsify/FxKillRule.md:32`:
  `entries=1 indexed=1 cited_rows=3 rows_present=1 rows_mined=1 usedby_ok=0 census=skipped`, rc=1.
- `.ufo/waves/round-33/claims/control-nothing.txt:5`:
  `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=ok`, exit 1.
- `.ufo/waves/round-29/attempt2/build/R29a2CritClaimC1.md` (round-29, unrelated):
  `… rows_mined=1 usedby_ok=1 census=ok`.
So `rows_mined=1` never co-occurs with `census=fail`. I did not synthesize the requested line; the
draft quotes the two states that do exist, each with its own pointer. The refusal verdict is
unchanged either way.

**F2 — the round-32 closure receipt's on-disk after-line is the `rows_mined=3 usedby_ok=1` one, and
the landed SCORECARD row contradicts it.** See §4.1. A SCORECARD row is supposed to be re-runnable at
its own pointer; this one is not. Highest-priority patch of this seat.

**F3 — `corpus/evidence/round33/defects-after.txt` names a revision at which its own numbers cannot
print.**
File content: `checks=6 defects=0`, `exit=0`, `# revision: c227e486a622ff82aae780c6fc58f023dcc82430`.
Re-derivation at that revision, read-only, from a `git archive c227e486` extraction:
`python3 plans/round33_defects.py --lane .` prints
`DEFECT N2 scorecard-round32-section: SCORECARD.md carries no '## Round 32' section…`,
`DEFECT N5 …`, `DEFECT N6 …`, `checks=6 defects=4` (N1 additionally red only because the extraction
carries no git metadata). Since N2 is red at `c227e486`, `defects=0` cannot have been produced there;
the receipt's numbers are current-tree, its revision line is not. The receipt should name `7895588`
(or the landing commit), not the inherited-state commit. This is a round-33 C2 provenance defect, not
a round-32 one, and it is invisible to `check_n2`, which only greps for the heading.

**F4 — the premise "section missing" is stale at this seat's start.** §0. `check_n2` reads only a
heading pattern, so it now passes on a section whose cells can be wrong (F2) — the counter cannot
distinguish content from a heading. Worth a Q22-style note at landing: N2's check is a presence
check, not a content check.

**F5 — registry refusal rows share the ids they refuse.** `git show HEAD:corpus/SOURCES.md | grep -n
'(S094|S097|S101|S102)'` → lines 114-117, rows `| S094 | supersedes S094 …`, `| S097 | supersedes
S097 …`, `| S101 | …`, `| S102 | …`, all `status=rejected`. The section text says "four rejected
correction rows recorded", which is exactly what exists; it does **not** say "ids never reused". The
round-33 claim's phrase "ids never reused; CORPUS.md rule 2" is therefore about the *staged* rows,
while the *registry* now holds a second row under each of those four ids — flagged here for the C1
counter's collision guard, not repaired (out of this seat's scope).

## 6. What this seat ran (all read-only; author-side, no non-author credit claimed)

| Command | Output |
|---|---|
| `git rev-parse HEAD` / `git status --porcelain` | `7895588…` detached; 14 worktree entries, `SCORECARD.md` clean |
| `grep -n '^## Round 3[0-9]' SCORECARD.md` | 1012 / 1045 / 1094 / 1122 |
| `python3 plans/round33_defects.py --lane .` | `checks=6 defects=0`, exit 0 |
| `git cat-file -t f20a1097 0d32691d bcd2a6c 112091c c227e486 f0b20aea ae95fe0 a44b5a8` | first seven `commit`; `a44b5a8` → `fatal: Not a valid object name` (phantom, as routed) |
| `git ls-files .ufo/waves/round-32 \| wc -l`; `git status --porcelain .ufo/waves/round-32 \| wc -l` | `89`; `0` (N1 closed by `c227e486`) |
| `git archive c227e486 \| tar -x -C /tmp/r33-scorecard-check` + counter on that tree | `checks=6 defects=4`, exit 1; N2 red (F3) |
| registry scan `git show HEAD:corpus/SOURCES.md \| grep -nE '(S094\|S097\|S101\|S102)'` | lines 114-117, four `rejected` correction rows |
| `git show HEAD:corpus/knowledge/benchmark-grader-semantics.md \| grep -n '^source:\|^verified-at:'` | three `source:` lines (S093, S094, S097) + `verified-at: 2026-10-25` — the unadmitted draft, unchanged |
| fleet `git log --oneline -1 -- .ufo/reports/round-3{1,2}/kengaku.md` | both last touched by `3d3ca566` (N3/N4 erratum appends) |

Scratch used: `/tmp/r33-scorecard-check` only (one archive extraction, well under 60 MB). No
repository was cloned; no campaign or mutating command was run in any repo.

## 7. Not done, deliberately

- No production edit: `SCORECARD.md`, `corpus/*`, the fleet reports and the knowledge entries are
  untouched by this seat; the section text above is the payload the L1 integrates.
- No C1/C2/C3 claim measurement — this seat drafts, it does not score; the only counters run were
  `round33_defects.py` (read-only, to establish N2's state) and the archive re-derivation in §6.
- No census, no `catalog_probe.py --verify`, no URL fetch: round-32 facts were read from committed
  bytes, and the round-33 counters belong to their own seats.
- No git mutation, no `jj`, no write under `/home/vgpnk/Projects/shokunin` or `shokuknow`.
- Calibration credit for this seat: none. It is an author-side draft; the closure that reads it decides.

VERDICT: scorecard-drafted
