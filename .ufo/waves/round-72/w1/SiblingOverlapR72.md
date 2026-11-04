# SiblingOverlapR72 — round 72 w1: cross-claim / cross-source overlap scan

Seat: leaf connector, wave `round-72/w1`. No subagent dispatch, no battery, no publish, no commit,
no package install (nothing was installed; no tool version to record). Scratch
`/fast/scratch/hyaku/kengaku-r72/SiblingOverlapR72`, created with `mkdir -p` and removed before the
final command of this seat (`trap 'rm -rf -- "$S"' EXIT` arm; verified absent, `## Scratch receipt`).
Port 5000 not bound by any command here, so no `--port-lock` was needed or taken. Read-only across all
siblings: every write in this seat is this file. No predicate, case table, vector, digest, kill rule or
target was touched; the two claim-level findings in §5 are reported, not edited.

## Bytes measured (pre-entry)

Sibling HEADs at capture (`git -C <lane> rev-parse --short HEAD`, rc 0 each):

| lane | HEAD | lane | HEAD | lane | HEAD |
|---|---|---|---|---|---|
| audio | `f9da7ee9` | kagi | `6191805` | mado | `9d91f7f6` |
| chousa | `f748abbb` | kaidoku | `70489de5` | mori | `84c6cbc3` |
| game-dev-2d | `1e033ef0` | kake | `bb2f8eda` | revenger | `5915ad8` |
| game-dev-3d | `39ca397` | kama | `db8b6fb0` | souji | `83d38132` |
| kengaku | `b6336136` | kasegi | `c81eef7` | tabi | `57b29bad` |
| kotoba | `1c8f37e` | kotodama | `c285b2af` | tameshi | `ef57dc2a` |
| kumitate | `3c369336` | lore | `0f044aa` | tsukuroi | `8eeadcb9` |

Twenty-one `*-shokunin` working trees = 20 siblings + this lane. `kengaku` is included so in-lane prior
art is measured on the same rule as sibling prior art (the item asks what the round "introduces").

## What I ran

| # | command (cwd = `/home/vgpnk/Projects/shokunin`) | rc | result |
|---|---|---|---|
| 1 | 8-term `grep -rIl` per lane, files = `SKILL.md` \| `plans/*.{md,py}` \| top-level `*.md` \| `.ufo/waves/<r>/<w>/<seat>.md`; `--exclude-dir` = `.git .jj node_modules .venv __pycache__ .pytest_cache`; case-insensitive substring | 0 | 45,974 line hits |
| 2 | same set, line-level scan splitting the 45,974 into instrument / lane-doc / wave-report / other tiers | 0 | 877 / 1,553 / 39,692 / 3,852 |
| 3 | instrument-shape greps (independent of the 8 words): `bwrap.*clearenv`, `eight-column\|8-column\|eight column`, `null_detected\|survived=[0-9]\|killed=[0-9]\|MUTANTS total`, `transformers_file\|transformers.__file__` over `SKILL.md`, `plans/`, `tools/`, `scripts/` | 0 | the 12 surface sites of §3 |
| 4 | source reads of each candidate instrument (headers, `--selftest`/verdict maps, registry rows) | 0 | classification in §3–§4 |
| 5 | `git -C kengaku-shokunin show d8a77d3f:SKILL.md` / `c80fcdb3:SKILL.md` / `d8a77d3f:plans/round-71-claims.md`, `grep -c 'round71_c1_hf_probe\|round71_c2_routed_defects'` | `git` rc 0 all three; `grep` rc 0 on the claims doc and rc 1 on both `SKILL.md` blobs (no match) | 0 / 0 / 4 matches — §5 F1 |

The counting rule for #1 is the seat's stated metric: a hit is one file line containing at least one of
the eight terms as a case-insensitive substring; ledger identities (`kengaku-shokunin…`) are not matches.
Corpus evidence blobs, `.ufo/evidence/`, `tools/`, `scripts/` and `corpus/{lessons,knowledge}` were
excluded from the *count* and covered instead by the instrument-shape greps of #3, because a receipt
mentioning a word is not a claim of ownership while a script or registry row is.

## §1 Counts

**45,974 line hits, 21 lanes, 8 terms.**

| term | hits | term | hits |
|---|---:|---|---:|
| `provenance` | 26,237 | `clearenv` | 378 |
| `registry row` | 14,772 | `sitecustomize` | 213 |
| `canary` | 2,713 | `mutation matrix` | 141 |
| `Gate/probe registry` | 1,389 | `fixture matrix` | 131 |

| tier | hits | share |
|---|---:|---:|
| A — instrument surfaces (`SKILL.md`, `plans/`) | 877 | 1.9% |
| B — lane docs (top-level `*.md`: `LOG`, `SCORECARD`, `PROVINCE`, `SHONEN`, …) | 1,553 | 3.4% |
| C — historical wave reports (`.ufo/waves/<r>/<w>/<seat>.md`) | 39,692 | 86.3% |
| D — other | 3,852 | 8.4% |

Per lane (both columns are line hits; `instrument` = tier A):

| lane | total | instrument | lane | total | instrument |
|---|---:|---:|---|---:|---:|
| audio | 15 | 0 | mado | 1,442 | 41 |
| chousa | 2,298 | 20 | mori | 4,086 | 20 |
| game-dev-2d | 69 | 0 | revenger | 822 | 7 |
| game-dev-3d | 31 | 3 | souji | 2,219 | 8 |
| kagi | 1,204 | 18 | tabi | 2,518 | 28 |
| kaidoku | 3,819 | 84 | tameshi | 5,623 | 31 |
| kake | 2,580 | 16 | tsukuroi | 2,380 | 136 |
| kama | 989 | 55 | **kengaku** | **3,178** | **296** |
| kasegi | 3,383 | 25 | kotoba | 2,596 | 57 |
| kotodama | 2,277 | 18 | kumitate | 1,846 | 11 |
| lore | 2,599 | 3 | | | |

Two calibration facts before any classification:

1. **The words are not distinguishing.** `provenance` and `registry row` alone are 89.3% of all hits
   (41,009/45,974) and are ordinary lane vocabulary across fourteen rounds of `LOG.md`. Volume says
   nothing about ownership; the scan is decided by instrument identity (§3), not frequency.
2. **`fixture matrix` has zero hits in tier A fleet-wide** (0 in every `SKILL.md` and every `plans/`
   file; its 131 hits are 124 wave-report + 3 lane-doc + 4 other). Of the eight terms it is the only one
   absent from all 21 lanes' *instrument* surfaces, i.e. it is the one term the round names that no lane
   has ever put in a registry row.

## §2 Term-level vs surface-level

Reported at two granularities, because the two answer different questions and one ratio would fake
precision: a shared instrument is claimed by **one** row or script header (a site), not by a
fraction of its word occurrences.

- **Surface-level: 12 sites in 6 siblings** (§3) — a sibling claims the same instrument class or the
  same artefact class.
- **Term-level: 5 mechanism precedents in 3 siblings + 2 in-lane** (§4) — the primitive is shared, the
  instrument is not.
- **Term-level by volume: the remaining 45,974 line hits**, of which 39,692 (86.3%) are historical
  wave-report prose written before this round. No member of that remainder claims a round-72 artefact.

No sibling is term-free: the two lowest lanes (`audio` 15, `game-dev-3d` 31) still carry `provenance`
in `PROVINCE.md`/`LOG.md`. The count of lanes with **zero tier-A hits** is 2 (`audio`, `game-dev-2d`);
that is the only sense in which a lane is uncontaminated, and it is not a claim about that lane's tools,
which were out of the counted set by construction.

## §3 The 12 surface-level sites

Class `(a)` = sandbox/environment provenance witness; `(b)` = registry-conformance gate;
`(c)` = fixture-matrix mutation metric. Line numbers are at the sibling HEAD in §"Bytes measured".

| # | sib | file:line | what it claims | class |
|---|---|---|---|---|
| S1 | tabi | `SKILL.md:2478` | `gate-registry-conformance` row: `node scripts/check-gate-registry.mjs --rev REV` | (b) |
| S2 | tabi | `scripts/check-gate-registry.mjs:1-40` | "*derives the lane's gate set from the bytes at a revision (never from the registry itself, so the registry cannot vouch for its own completeness)*"; findings `e1-missing-row`, `e2-field-incomplete`, `e3-row-script-absent`; counted field `nonconformant`; `--selftest` 22 cases; reads 4/5/6/8-column tables **by header name**; latest row wins | (b) |
| S3 | tsukuroi | `SKILL.md:2082` | `registry-coverage` row: `python3 tools/check-registry-coverage.py --revision REV` → `REGISTRY-ROW-MISSING\|DUPLICATE\|ORPHAN\|KIND-INVALID\|SELFTEST-UNRESOLVED\|VERDICT-INCOMPLETE` | (b) |
| S4 | tsukuroi | `tools/check-registry-coverage.py:227` | "*registry header is not followed by an eight-column separator*"; operative table = unique highest `round<N>` heading; exact 8-cell header | (b) |
| S5 | tabi | `.ufo/waves/round-24/w2/MutGateRegistryRows.md:1-…` | 30 row-level mutants against S1, one per required field, with restore verification (`restoredSkillSha == pristineSha` for all 30) and survivor analysis ("*five of the eight predicates are shape-only and accept semantically wrong cells*") | (b)+(c) |
| S6 | kama | `SKILL.md:1546` | `Round-50 C1 replay-bind audit`: `python3 tools/round50-replay-bind-audit.py --repo --tip --scratch --out`; `bind=0/1 teardown=0/1 newrow=0/1 bound=N/3` | (a) |
| S7 | kama | `tools/round50-replay-bind-audit.py:11-15,32,51,485` | env leg: `KAMA_R50_CANARY` fresh random value + a `PYTHONPATH` `sitecustomize.py` that stamps a marker; "KAMA_R50_CANARY is in neither `/proc/<pid>/environ` nor the environ of the server's parent"; defect line "*planted sitecustomize imported by N interpreter(s)*"; also binds `/proc/<pid>/maps` to the frozen model digest | (a) |
| S8 | tabi | `SKILL.md:2558` | `gate-mutants`: `node scripts/check-gate-mutants.mjs --rev REV` → `0=clean (… fault_survivors=0, benign_killed=0)`; catalog `scripts/gate-mutants.json`, mutant `kind fault\|benign` | (c) |
| S9 | kasegi | `SKILL.md:1064` | `limb-mutation-check.py` + `limb-ledger.json`: 13 limbs in frozen order, `limbs=13 killed=13 survivors=0 controls=3 rejected=3`; per row `invalid:live-baseline`, `invalid:find-count`, `invalid:noop`, `invalid:nocompile`, `invalid:timeout`, then `killed` | (c) |
| S10 | kasegi | `SKILL.md:1099` | `kill-rule-check.py`: header `KILL-RULE instrument=… sha256=… floor=19`, `probe <name> pristine=pass\|fail` per probe (`selftest-shape` + eight fixture lanes), `mutant=<name> killed=0\|1`, attribution | (c) |
| S11 | souji | `SKILL.md:300` | `r42-c3-counter`: `SUMMARY mutants=13 killed=13 survived=0 pristine=ok prior=8/8 old_killed=0 equiv=6 equiv_killed=0 anchors=ok`; `--survey` "is never a verdict" | (c) |
| S12 | tameshi | `SKILL.md:1894,1973,2197` | `tools/registry-check.py` — replay every registry row, `differs`/`active`/`superseded` outcomes, `timeout_s` bounds, survivor kills; three rows in three registry generations | (b) |

Distribution: tabi 4, tsukuroi 2, kama 2, kasegi 2, souji 1, tameshi 1. The other 14 siblings carry
**zero** surface-level sites for the round's terms.

## §4 The 5 term-level mechanism precedents

| # | sib | file:line | why term-level, not surface |
|---|---|---|---|
| T1 | kumitate | `SKILL.md:618` | `cap-run` already runs its child under `env -i` + `bwrap … --clearenv` with an explicit allowlist (`{PATH, XDG_RUNTIME_DIR}`), refuses `--bind` of `/ /tmp /proc /sys /dev /run`. It owns the *runner with a cleared env*, not a witness of what the child loaded. |
| T2 | kumitate | `SKILL.md:622` | `bind-oracle` proves requested mount binds **from inside** a `cap-run` child and has a visibility control (`CONTROL_VISIBLE`). Same witness *shape* (in-child evidence + a control arm) but the witnessed object is mounts, not import provenance. |
| T3 | tameshi | `SKILL.md:2018,2188` | `tools/env-diff.py` — finite 7-profile environment differential (`host, clean, clean_repeat, tz, locale, home, columns`) over pinned selftests; "*the clean control must pass; a changed repeated clean tuple is nondeterminism*". Profiles, not an allowlist of names; nine **pinned surfaces**, not nine variables. |
| T4 | kengaku | `SKILL.md:663`; `plans/round52_c2_registry.py:24-34` | R52-C2 already derives an `ADVERTISED` universe of `python3 plans/*.py\|corpus/evidence/*/*.py\|grader.py` commands from `SCORECARD.md`, `SKILL.md`, `LOG.md`, `corpus/README.md`, `corpus/knowledge/*.md` and grades `MISSING/INCOMPLETE/ENTRY-MISSING/SELFTEST-UNBACKED`. In-lane registry-conformance instrument, two rounds before the defect it failed to catch. |
| T5 | kengaku | `plans/round64_c1_kvstore_probe.py:544`, `round65_c1_sqlite_probe.py:402`, `round66_c1_tensor_probe.py:179`, `round67_c1_pipeline_probe.py:176` | `--clearenv` is already in this lane's four round-64…67 probes. Round 71 **dropped** it; round 72 restores it. |

T4 and T5 are the two most load-bearing entries in this report and they are not sibling findings — see §5.

## §5 Findings for the round (reported, not edited)

**F1 — R72-C2's `E1a` does not close the class it is written to close; the escape mechanism is
identifiable and unfixed.** The claim sentence says the four rows are appended "*so the class cannot
recur silently*". `E1a` iterates a frozen constant:
`INSTRUMENTS = (round71-c1, round71-c2, round72-c1, round72-c2)` (`plans/round72_c2_routed_defects.py:56-61`).
A fifth kengaku instrument registered nowhere still prints `DEFECTS n=0`.

The mechanism of R71-R1 is measurable, and it is *not* "no one looked":

- `git show d8a77d3f:SKILL.md | grep -c 'round71_c1_hf_probe\|round71_c2_routed_defects'` → **0**
  (`git` rc 0, `grep` rc 1: no match).
- `git show c80fcdb3:SKILL.md | …` → **0** (same rcs).
- `git show d8a77d3f:plans/round-71-claims.md | …` → **4**.
- `plans/round52_c2_registry.py:29` → `SELF_FILES = ("SCORECARD.md", "SKILL.md", "LOG.md", "corpus/README.md")`.

R52-C2 was live, registered and green; its advertised universe simply does not include `plans/`, so an
instrument advertised **only** in a claims doc never enters `ADVERTISED` and the `MISSING` leg cannot
fire. Appending four rows does not widen that universe. Two fleet instruments do close the class —
tabi `check-gate-registry.mjs` (S1/S2) derives the gate set from the revision's bytes *by design* and
tabi's own round-24 matrix already found the exact weakness family (shape-only predicates accepting
semantically wrong cells, S5) — and neither is cited in `plans/round-72-claims.md`.

This is a finding, not an edit: the frozen predicate as written (`E1a ok`) is satisfiable and I am not
proposing a different one. But `R72-C2`'s calibration evidence should not be read as "class closed"; it
is "this instance closed, class still open on the fifth instrument".

**F2 — R72-C1's provenance witness is (i) a restoration, (ii) self-reported, (iii) unrepeated.**
(i) `--clearenv` is present in `round64/65/66/67_c1_*_probe.py` (T5); the round-71 probe removed it.
The round's framing "gains a provenance witness" is right about the *witness line*, not about the
mechanism, and the report should say so — a reader who takes "new" literally will look for the novelty
in the wrong place.
(ii) `env_cleared=True` and `allowlist_seen=9/9` are computed **inside** the sandbox by
`/probe/harness.py` and printed into `LEGS-JSON` (`round72_c1_hf_probe.py:197-199`, `:607-618`); the
same process that is under test self-reports its own isolation. kama's instrument (S7) reads
`/proc/<pid>/environ` **from outside** for exactly this reason, and its round-49 routed item R1 names
the defect it closed as "*a PYTHONPATH/sitecustomize hijack of the inherited environment met it*" — the
same mechanism R71-R6 found here. `--stub-control` is a behavioural arm, not an outside observation.
(iii) `distinct=1` is one distinct `transformers_file` across nine *cases*, not one case repeated;
tameshi's `clean_repeat` profile (T3) exists because a single tuple cannot separate determinism from
environment insensitivity. No repeat arm is named in the receipt's `PROVENANCE` line.

All three are limitation candidates in the round's item (v)/(ii) register, not predicate changes.

**F3 — "fixture matrix" is a new *label*, not a new artefact, and the distinction is worth one
sentence.** Zero tier-A hits fleet-wide (§1), so no lane has ever registered the term — but this lane has
been running mutant × fixture matrices since round 37 (`.ufo/waves/round-37/build/R37SkillDraft.md:88`,
`round-40/falsify/F40RevBatMan.md:61,153`) and the surviving-artefact vocabulary across the fleet is
`mutant matrix` (141) with three named ownership variants in §3. R72-C2's metric is a legitimate
*variant* — its `null_detected` **counts and attributes** a deliberate no-op, where kasegi marks a no-op
`invalid:noop` (excluded, S9), tabi requires a benign mutant to *survive* (`benign_killed=0`, S8), and
souji requires equivalence mutants to *not* be killed (`equiv_killed=0`, S11). That fourth position is
the only thing in R72-C2's metric that is not already owned elsewhere, and it is worth naming as such.

## §6 Routing verdict

**Report out, do not absorb:** no sibling claims this round's two artefacts (a nine-case table with
`K9 400-no-error-field` reachable at `tests/test_outputs.py:107`, and a four-row registry closure with an
appended errata block), but **six siblings own its three instrument classes** — tabi owns both the
registry-conformance gate and its row-level mutant matrix (S1/S2/S5), tsukuroi a second registry gate
(S3/S4), kama the closest environment/stub provenance witness (S6/S7), and tabi/kasegi/souji the
mutant-matrix no-op arm (S8/S9/S11) — so R72-C2 must be scoped and cited as a *four-instrument,
`plans/`-path, list-bounded, lane-local* instance that closes R71-R1's reported rows, with F1 stated as
the class still open; and R72-C1 must cite kama's outside-`/proc` env witness and this lane's own
round-64…67 `--clearenv` probes as prior art, with F2 (i)–(iii) as limitations.

## §7 Limits of this scan

1. The count is a **substring** count. `provenance` matches `PROVINCE.md` prose and `registry row`
   matches prose *about* rows equally; only §3/§4 sites were read as claims.
2. Tier C (86.3% of hits) is historical prose from rounds before 72; it proves a term is established
   vocabulary, never that a live instrument exists. Instrument-shape greps (#3) were used to find live
   instruments, and those greps are not exhaustive for tools with unusual names.
3. `tools/` and `scripts/` were excluded from the counted set and inspected only for the three named
   instrument classes. A fourth ownership class I did not look for is not excluded by this report.
4. Sibling HEADs are working trees, not published tips; a sibling mid-edit could have been read at a
   state neither of us will see again. The 12 surface sites are each stable text (a registry row or a
   script docstring), so a concurrent edit would be a diff, not a different classification.
5. Nothing here re-ran a sibling instrument. Every claim about a sibling is a **read of its committed
   bytes and its own stated contract**, including each sibling's own recorded tallies (`nonconformant=3`,
   `30 mutants`, `killed=13`) — those are quoted, not verified by this seat.

## Scratch receipt

`S=/fast/scratch/hyaku/kengaku-r72/SiblingOverlapR72` held `scan.py` and `hits.json` (the 45,974-row
line-hit inventory). Both were scratch-only; the counting rule is reproduced in §"What I ran" so the
inventory is re-derivable without them. `rm -rf -- "$S"` ran before this file's final read; nothing in
`/tmp`, nothing in `.scratch/`, nothing in `.ufo/state/`, no sibling written, no `git`/`jj` mutation.
