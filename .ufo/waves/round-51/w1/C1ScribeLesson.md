# C1ScribeLesson — round 51, w1 scribe (lesson draft)

Seat: `C1ScribeLesson` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Item: draft `corpus/lessons/round-51.md` — `## Gate` (candidates opened this round, admitted rows,
rejected rows with reason + flip condition, spot-check placeholder), `## Mistakes` (≥2 rows:
class · evidence pointer · captured-by criterion · fix) drawn from the round-50 closure's routed
defects D1/D3/D5/D7 and from this round's own findings, `## Limits` — using the fleet mistake
vocabulary. Read-only against the lane: this report is the only write. No production file touched,
no commit, no push, no mutating git call.

## Axes named (Godspeed)

1. **freshness (assigned)** — every statement in the lesson names the revision it was measured at;
   no number is carried over from another round without its own pointer.
2. **attribution honesty** — a seat report is cited as a seat report, never upgraded to a closure
   verdict; a claim the L1 has not landed is written as a draft obligation, not as an outcome.
3. **vocabulary discipline** — each `## Mistakes` row carries exactly one fleet class (or a named
   compound where the defect genuinely has two causes), with an evidence pointer that resolves.
4. **non-absorption** — round-50's routed defects are cited where they are recorded, not re-derived
   and not silently marked closed.

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

Stage-1 freeze `e07f131cf7037e58a21db6e1f3986cf401ad257c` (commit message: `round-51: stage-1
freeze — C1 surface-truth counter+manifest, C2 routing counter, claims, before receipts`).
`HEAD` and `master` both printed `4090c3db79d11279ab5e5121ba25e74aa316e6e7` at every read in this
seat (15:18–15:33 -03:00); the tip did not move under me. Every wave seat report cited below names
its own `REV 4090c3db…` except `C1ScoutSurfaces.md` and `C1MutRows.md`, which measured the freeze
`e07f131cf…` (both state that the C1 files are byte-identical at freeze and tip, which I re-checked:
`git diff --stat e07f131 HEAD -- PROVINCE.md plans/round51_surfaces.py plans/round51-surfaces.json`
prints nothing).

## Inputs read (in this order)

| path | what it bound |
|---|---|
| `plans/round-51-claims.md` | full file: C1 freshness 8→9, C2 adjacency 8→9, predicates, controls, kill rules, stages, limits |
| `plans/round51_surfaces.py` | full file (probe kinds, `check()`, `_selftest` S0–S8, `tip_rev`) |
| `plans/round51-surfaces.json` | all 19 entries, `sections`, `resolve_floor: 13` |
| `plans/round51_routing.py` | `FIELDS`, `DISPOSITIONS`, `load_owners`, check execution path |
| `.ufo/waves/round-51/claims/c1-before.txt`, `c2-before.txt` | the two before receipts |
| `corpus/lessons/round-50-verifier-spotcheck.md` §6 | D1–D7 routed defects |
| `corpus/lessons/round-50.md` | the lesson that D5/D7 apply to |
| `corpus/lessons/round-49.md` | the `## Gate` / `## Mistakes` form to match |
| `../../LEARNING.md` | `## Gate` contract: candidates, admits, rejects with reasons, spot-check result |
| `../../CORPUS.md` (§mistake classes, per round-25/28/31/36/37 precedent rows) | the class vocabulary in use |
| `PROVINCE.md` lines 8–21, 100–118, 150–166 | the two surface tables, the Core rows, the Historical table |
| `corpus/routed-findings.jsonl` | 71 rows, key union, status histogram, 10 check-less rows |
| `corpus/SOURCES.md` | contract-v1 11 columns; 170 S-rows |
| `.ufo/waves/round-51/w1/*` | the 46 seat reports/artifacts present at drafting (list in §Commands) |

## Commands run (exact) and observed outputs (verbatim where they are evidence)

Consolidated measurement, cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin`:

```sh
git rev-parse HEAD; git rev-parse master
git status --porcelain
git diff --stat -- plans/round42_c1_verify.py plans/routed_open.py plans/scratch_guard.py
git diff -- plans/scratch_guard.py
sha256sum corpus/routed-findings.jsonl
git show 4090c3d:corpus/routed-findings.jsonl | sha256sum
wc -l < corpus/routed-findings.jsonl
grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md
find .ufo/waves/round-50 -maxdepth 1 -name "w1-results.json" | wc -l
grep -c ':285-292' corpus/lessons/round-50.md; grep -c ':42-43' corpus/lessons/round-50.md
grep -ci 'spot-check' corpus/lessons/round-50.md
git diff -- plans/round51_routing.py
```

Observed (15:33 -03:00):

```
### HEAD
4090c3db79d11279ab5e5121ba25e74aa316e6e7
### STATUS
 M plans/round51_routing.py
?? .ufo/waves/round-50/w1.ready
?? .ufo/waves/round-50/w1.ready.partial
?? .ufo/waves/round-50/w1/
?? .ufo/waves/round-51/claims/control-c1-declare-all-absent.txt
?? .ufo/waves/round-51/claims/control-c1-drop-entry.txt
?? .ufo/waves/round-51/claims/control-c1-stale-pin.txt
?? .ufo/waves/round-51/claims/control-c1-undated.txt
?? .ufo/waves/round-51/integrate_ledger.py
?? .ufo/waves/round-51/w1-run.err
?? .ufo/waves/round-51/w1.ready
?? .ufo/waves/round-51/w1.ready.dispatched
?? .ufo/waves/round-51/w1/
### LEDGER
39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  corpus/routed-findings.jsonl
39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  -
71
### SOURCES
170
### R50-WAVERESULTS
0
### D5
1
1
### D7
0
```

Earlier in the same seat (15:22 -03:00) `git status --porcelain` additionally showed three
**mode-only** modifications, content identical, since reverted:

```
 M plans/round42_c1_verify.py
 M plans/routed_open.py
 M plans/scratch_guard.py
```

```
 plans/round42_c1_verify.py | 0
 plans/routed_open.py       | 0
 plans/scratch_guard.py     | 0
 3 files changed, 0 insertions(+), 0 deletions(-)
old mode 100755
new mode 100644
```

`ls -l --time-style=full-iso` on those three printed mtimes `2026-10-28 15:22:02.239/.242/.245
-0300`; `corpus/routed-findings.jsonl` mtime was `15:22:02.235` in the same second, while its
sha256 equalled the committed blob at 15:26 and at 15:33 (clean, 71 rows).

The uncommitted C2-counter edit present at 15:33 (`git diff --stat` → `1 file changed, 13
insertions(+), 5 deletions(-)`) changes four things:

```diff
-def load_owners(fleet: Path) -> set[str]:
-    conf = fleet / "shokunin.conf"
+def load_owners(fleet: Path) -> set[str]:
+    """Owner universe: the curated fallback set, the LANES rows of shokunin.conf
+    (`id|repo|axes`), and every `*-shokunin` lane directory on disk."""
     owners = set(FALLBACK_OWNERS)
+    conf = fleet / "shokunin.conf"
-            m = re.match(r"\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{", line)
+            m = re.match(r"\s*([a-z][a-z0-9-]{1,15})\s*\|", line)
+        for d in fleet.glob("*-shokunin"):
+            if d.is_dir():
+                owners.add(d.name[: -len("-shokunin")])
-                out = subprocess.run(["bash", "-lc", cmd], cwd=str(tmp),
+                out = subprocess.run(["bash", "-lc", cmd], cwd=str(lane),
                                      capture_output=True, text=True, timeout=60,
-    ledger = Path(args.ledger) if args.ledger else lane / "corpus/routed-findings.jsonl"
+    ledger = Path(args.ledger).resolve() if args.ledger else lane / "corpus/routed-findings.jsonl"
```

Seat-artifact census at drafting (64 seats in `.ufo/waves/round-51/w1-spec.json`; artifacts
matched by filename prefix in `.ufo/waves/round-51/w1/`): 49 seats had produced an artifact,
15 had not — `C1CritUndated`, `C1ScribeProvince`, `C1ScribeLesson` (this seat), `C2ConnProtocol`,
`C2ExecOpenChecks`, `C2CritSpotAttribution`, `C2RevRecount`, `C2RevFieldLoss`, `C2ScribeReportOuts`,
`SrcHFRevision`, `CritClaimSizing`, `RevSeparability`, `CritAdmission`, `CritSurvivor`,
`ScribeSourcesAppend`. This is a census, not a settled/dead judgement (see §Limits).

No tool was installed or upgraded; no pacman transaction attempted; no network fetch was made by
this seat (every quote below is from a lane file or a seat report).

## Draft — `corpus/lessons/round-51.md`

The block below is the deliverable. It is written for the L1 to land verbatim after filling the
marked `[L1 fills: …]` slots at the landing tip. Nothing in it is a closure verdict.

```markdown
# Round 51 — surface truth (C1) and routed-finding attribution (C2) (2026-10-28)

L1 `KengakuR51`, hyaku run 11. Base tip `297e17927ba9342a87ba27a48cc5270a001de7cb`; stage-1 freeze
`e07f131cf7037e58a21db6e1f3986cf401ad257c`; wave-1 dispatch `4090c3db79d11279ab5e5121ba25e74aa316e6e7`
(64 seats). [L1 fills: seats settled / WAVE-DONE / `w1-results.json` hash / landing tip.]
Every number below names the revision it was measured at; the wave-time revision is `4090c3d`.

## Gate

No source candidate was carried into this round. Three things were opened: two primary-source rows
for the lane's registry and one new host surface. The wave falsified one path premise, one digest
conjunct, and one recorded reading.

| candidate | decision | evidence (revision) | flip condition |
|---|---|---|---|
| llama.cpp HTTP server docs, `tools/server/README.md` @ tag `v0.8.0` (commit `8642541b255bfb5dc39cd351a178be09013a55d6`), 135608 bytes, sha256 `8fd5abde…`, opened 2026-10-28 | **ADMIT** — tier A, kind `docs`, status `queued`; five located quotes ≤25 words each: L1376 (`--alias` renames `id`), L1349 (`/v1/models` is a one-element list), L482 (`/health` public, `/v1/health` also works), L1019 (`total_slots` = `--parallel`), L491 (200 when ready) | `w1/SrcLlamaServer.md` §§2–4; bytes + headers + sha256 in `w1/SrcLlamaServer/` (REV `8642541b…`; lane `4090c3d`) | — (re-open at each tagged release; `recheck: on-release`) |
| HF Hub model-revision/commit docs (`SrcHFRevision`) | [L1 fills: the seat had not reported at drafting — admit with its anchor+quote, or reject with its recorded failure] | `w1/SrcHFRevision.md` [L1 fills] | [L1 fills] |
| the round item's stated path `docs/server.md` | **REJECT** — `404 14` at the pinned tag *and* at `master`; `GET /repos/ggml-org/llama.cpp/commits?path=docs/server.md` returns an empty list, so no file has ever existed there | `w1/SrcLlamaServer.md` §2.1 | a server page returning 200 at `docs/server.md` at a pinned revision |
| new declared surface — the live served endpoint on this host (llama-server router `127.0.0.1:1234`, child instance `LFM3-1.7B` on `:45669` at capture) | **ADMIT as a host-state surface**, pinned at capture: id + model path + `/proc` argv equality; **never a served digest** | `w1/C1ExecNewSurface.json` (SF20 entry, present 13→14, no new problem line); `w1/C1ExecEndpoints.md`; `w1/C1CritEndpointId.md` — the digest conjunct is FALSIFIED (`:45669` serves `"digest":""`, `:1234` has no digest field), so the row must assert id/path/argv, not a digest | the endpoint disappearing flips the row to `STALE` by design (point-in-time host state); a served digest field appearing would permit a digest pin |
| the 14 out-of-table declarations ranked by the surface scout (`plans/pkg_gate.py`, twelve TB2 grader admissions r35–r46, the r39/r40 C1 harness) | **REJECT for this manifest** — C1 is scoped by its own claims to the two tables `## Surfaces` and `### Core`; adding them after the before-receipt would widen the claim after data | `w1/C1ScoutSurfaces.md` (ranked list 1–14; the seat explicitly does not promote them) | a round freezes a manifest whose `sections` name those regions *before* its before-receipt |
| `### Historical — absent, not governed` rows (`~/wikillm/llm-wiki`, `~/bench-arena`, `/proc/1299/cmdline`, the qwen-coder systemd unit, `qwen-coder-godspeed.jinja`, `~/Projects/the-bounty-hunter`, `/tmp/bench-r{4..7}`) | **REJECT as live surfaces** — declared absent and ruled "not current dependencies" (`PROVINCE.md:150-166`); all re-probed ABSENT | `w1/C1ScoutSurfaces.md` row 15; `w1/C1ExecPaths.md` | a row moving into `## Surfaces`/`### Core` |
| C2 attribution "`routed` but owned by `kengaku`" | **REJECT** — that is absorption, not routing; the frozen counter calls it `NEXT violations` | `plans/round51_routing.py` (`NEXT` leg); `w1/C2CritDisposition.md` | a non-`kengaku` owner **plus** a `next` field |
| C2 disposition `fixed-verified` granted on a scratch-cwd green | **REJECT for two rows** (`R42-R3-07`, `R42-R3-08`): the checks are negative greps that went green only because the file was missing in the scratch cwd | `w1/C2ScribeSchema.md` F1/F2; `w1/CritSurvivor.md` verdict (3 instrument defects — cwd semantics, colon token rule, vacuous-disjunction acceptance — block the after-target as frozen) | re-run with `cwd=lane` and a positive-form check; fix the token rule and the disjunction acceptance before any `disposition` is granted |

Rows touched in the registry: [L1 fills: the S-numbers appended for the llama.cpp row and, if
admitted, the HF row]. Registry 170 → [L1 fills]; `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kengaku` exit [L1 fills].

Spot-check: **pending — no non-author closure exists yet.** `LEARNING.md` requires at least one
admit and one reject re-opened by a non-author with `agree`/`disagree` recorded here. The closure
must re-open the llama.cpp row (admit) and either the `docs/server.md` reject or the HF row, and
append its result to this section. Round 50's lesson is still missing this line (D7, open at
`4090c3d`: `grep -ci 'spot-check' corpus/lessons/round-50.md` → `0`), so this round must not repeat
the omission.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **landing** — a round closes with its wave outputs uncommitted and its wave unsettled: round 50's `.ufo/waves/round-50/w1/` (113 files), `w1.ready`, `w1.ready.partial` are still untracked at `4090c3d`, and round 50 has no `w1-results.json` although rounds 45/46/48/49 each have one | `git status --porcelain` at `4090c3d`; `find .ufo/waves/round-50 -maxdepth 1 -name w1-results.json \| wc -l` → `0`; round-50 spot-check §6 D1/D3 | the round-50 closure (§6), which routed it; no lane criterion measures "wave outputs committed and WAVE-DONE before the report" | the round report cites a committed `w1-results.json` and a WAVE-DONE marker; a settled seat with no report file is its own routed defect class. Shown able to fail: the round-50 tree at `4090c3d` still prints the three untracked wave paths |
| **landing** — the frozen instrument is edited in the lane working tree *after* the freeze and before any receipt: `plans/round51_routing.py` carries an uncommitted `13 insertions(+), 5 deletions(-)` diff at wave time (`load_owners` now parses `LANES` rows and lane dirs; checks run `cwd=lane` with a 90 s timeout; `--ledger` resolves) | `git diff -- plans/round51_routing.py` at `4090c3d`, 15:33 -03:00; the freeze commit `e07f131` holds the unfixed bytes | none — the claims freeze the command, not the bytes, and no receipt names the counter's digest | commit the repaired counter and record the deviation and its new digest in `plans/round-51-claims.md` (round-50's precedent for `850ec790…`), then measure the after receipt with the committed bytes; a receipt that does not name the counter digest cannot distinguish the two |
| **attribution** — round 50's lesson carries no spot-check result, so the round's only discernment verdict lives in the verifier file and never reaches the gate record | `grep -ci 'spot-check' corpus/lessons/round-50.md` → `0` at `4090c3d`; round-50 spot-check §6 D7 | `LEARNING.md` §Discernment is checked from outside — the rule exists but nothing reads the lesson for the line | append the closure's `agree`/`disagree` line to the lesson's `## Gate` and cite the closure file; the next round's lesson carries the placeholder from the start (this lesson does) |
| **reference-drift** — two admitted quote locations were wrong: S175's quote belongs to `gitrepository-layout.adoc:285-286`, not `git-worktree.adoc:285-292`; S177's quote starts at `git-fetch.adoc:41`, not `:42` — and both rows are still uncorrected in the lesson at `4090c3d` | `grep -n 'S175\|S177' corpus/lessons/round-50.md` → `:27` and `:29` unchanged; round-50 spot-check §6 D5 | Q10 (a second-seat re-read) ran, but it re-read the *digest*, not the location cell against the file at the pin | supersede the two rows append-only and correct the lesson table; the digests were right and the locations were not, so the fix is a location erratum, not a re-admission |
| **reference-drift** — both counters resolve lane-relative references from the process cwd: C1's `paths`/`sha256` probes use `expand()` instead of `lane / …`, so 10 of 19 entries flip to `absent` (`STALE 10`) when the same script runs from the fleet root; C2 runs each `check` with `cwd=<scratch tmpdir>`, so two negative greps pass only because the file is missing | `w1/C1RevProbes.md` F1 (verbatim `PROBES run=19 present=3 absent=16`, `STALE 10` from the fleet root); `w1/C1CritDeclareAllAbsent.md` F5; `w1/C2ScribeSchema.md` F1/F2 | none — the frozen counting command is written `--lane .` from the lane root, so cwd was never varied by the claim | join `lane` for every path/sha256 probe and run C2 checks with `cwd=lane`; freeze a selftest case that runs the counter from a foreign cwd and expects the same verdict. Shown able to fail: the fleet-root run prints `STALE 10` |
| **vacuous** — the C1 predicate's two document-facing legs never read the document: `DRIFT` compares the manifest's `prose` to the manifest's `state`, and `NUMBER-DRIFT` compares `count_claim` to the probe, never the anchored row, so `DRIFT 0`/`NUMBER-DRIFT 0` are reachable by editing the manifest alone; a *wrong recorded reading* is therefore indistinguishable from a real drift — the wave's independent row audit rules SF01's `prose=present` WRONG (the row already carries `ABSENT 2026-10-20`), which makes the honest tip count `DRIFT 2`, not 3 | `w1/C1RevPredicate.md` F1/F2/F3 (and its FAIL verdict); `w1/C1RevProbes.md` F2 (scratch manifest prints `NUMBER-DRIFT 0` while `PROVINCE.md:112` still says "25 rows"); `w1/C1MutManifest.md` F1; `w1/CritProseRead.md` ("18 RIGHT, 1 WRONG", SF01) | none — the claims froze the counter before any seat read which inputs each leg consumes | the landing receipt must show the row text and the manifest moving together (dated append + `count_claim` re-recorded + SF01 `prose` corrected in a stage-1 amendment), and round 52 freezes a counter whose `DRIFT`/`NUMBER-DRIFT` parse the anchored row line. Shown able to fail: the scratch-manifest run above. The dated-absence leg is shape-only in the same way: `ABSENT 2019-01-01` and `ABSENT 9999-12-31` both pass and a full-pass fixture with a 2019 date reaches `PREDICATE R51-C1 pass`, exit 0 (`w1/C1CritUndated.md` verdict) — so `UNVERDICTED 0` proves a marker's presence, never its freshness |
| **number-drift** — `PROVINCE.md:112` says the registry holds "25 rows" while `corpus/SOURCES.md` holds **170** S-rows (S001–S177, 0 duplicates); the cell has been stale through four rounds (25 → 37 → 42 → 170) and every correction was appended as prose, never as the cell | `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → `170` at `4090c3d`; `w1/C1ExecCounts.md` verdict; `w1/C1RevProbes.md` F3 | the frozen counter reports `NUMBER-DRIFT 1`, which is the criterion — but it can be cleared without the cell moving (row above) | date the `:112` cell append-only with the measured 170 and re-record `count_claim: 170` in the same commit, so the receipt shows both moved; a `NUMBER-DRIFT 0` alone is not evidence the cell was corrected |
| **stale-premise** — the frozen claim's control 1 states that declaring everything absent violates the resolve floor; it does not: the floor counts *probes that resolve*, not declarations, so the control fails on `STALE 13` while `RESOLVE observed_present=13 floor=13 verdict=met`; the same false sentence sits in the instrument's own docstring | `.ufo/waves/round-51/claims/control-c1-declare-all-absent.txt` (`RESOLVE … met`, `PREDICATE R51-C1 fail`); `w1/C1CritDeclareAllAbsent.md` F1; `plans/round51_surfaces.py` module docstring | none — the control prose was written from the intent, not from a run of the control | amend the claims' control-1 text and the docstring to name `STALE` as the failing leg and state the floor as "surfaces that may disappear from the host"; do **not** make `present` count declared state (that turns the floor into a tautology) |
| **survivor** — the frozen predicate survives row-level and entry-level mutation: 3 of 5 row mutants survive (`C1MutRows`: row-only number edit, dated marker on a present row, reorder), row deletion exits 0 at `rows=8` because the claims' `ROWS >= 9` kill rule is not a leg of the counter, and 3 of 5 manifest mutants survive (`C1MutManifest`: entry duplication inflates `RESOLVE`, the probe target is a free parameter) | `w1/C1MutRows.md` verdict; `w1/C1MutManifest.md` F1/F2/F3; `w1/C1MutCounter.md` F2 (the frozen counting command kills 0/5 of its own legs; only `--selftest` kills them) | the kill rules are prose in `plans/round-51-claims.md`, not legs in `plans/round51_surfaces.py` | enforce the row-count floor and a duplicate-entry leg inside the counter, and freeze the survivors as next round's fixtures (QUALITY Q38: a mutant's kill is witnessed, not assumed); the after receipt must carry the `--selftest` line as well as the counting line |

## Limits

- This lesson is drafted **before landing**. Every figure is at `4090c3d` (or the seat's own `REV`
  line); the L1 must re-measure at the landing tip and replace the `[L1 fills: …]` slots. No claim
  verdict, score or axis move is asserted here.
- The `prose` readings are judgements, not measurements. The wave's independent audit rules 18 of 19
  RIGHT and SF01 WRONG; that single disagreement is the reason the `DRIFT 3` figure must not be
  copied into the landing receipt without the stage-1 amendment.
- Seat reports are seat-level evidence, not closure verdicts. A seat that settles without its named
  report file is a routed defect class, not a finding of this lesson.
- Host probes (ports, `/health`, `/proc`) are point-in-time. An endpoint that returns flips a
  `present` row to `STALE` by design; that is the intended behaviour of the instrument, not a defect.
- The registry row ids are unassigned in the seat draft (`S0??`); assigning them is the integration
  owner's call, and the census (`scripts/sources-census.sh validate`) must pass before the rows land.
- No capability entered, no score changed, no axis harmed is asserted by this lesson; those are the
  L1's verdicts at landing. No tool was installed or upgraded; no pacman transaction was attempted.
```

## Findings routed to the L1 (from this seat)

1. **F1 — the lesson's Gate has one unfillable row at drafting.** `SrcHFRevision` had no artifact at
   15:33; `ScribeSourcesAppend` (which consumes it) was also absent. If the HF page was unfetchable,
   the Gate must carry it as a reject with the seat's recorded failure and flip condition — not as a
   blank admit.
2. **F2 — the C2 counter is being edited in the working tree, uncommitted.** `plans/round51_routing.py`
   at `4090c3d` carries `13 insertions(+), 5 deletions(-)` beyond the freeze bytes (see §Commands).
   The four changes are exactly the defects two seats found (`load_owners` provenance: C2ConnLedgerSchema
   §4, C2ScribeSchema F3; check cwd: C2ScribeSchema F1/F2). Landing them is correct; landing them
   **uncommitted** reproduces round-50 D2. Commit and record the digest + deviation in
   `plans/round-51-claims.md`, then receipt against the committed bytes.
3. **F3 — the `## Gate` spot-check placeholder is a real obligation, not a formality.** `LEARNING.md`
   requires one admit and one reject re-opened by a non-author; round 50's lesson never got the line
   (D7). The closure must append `agree`/`disagree` here and cite the closure file.
4. **F4 — SF01's `prose` needs a stage-1 amendment before the after receipt**, or the receipt will
   claim a `DRIFT 3 → 0` that was partly produced by a wrong recorded reading. The wave's reading
   (`w1/CritProseRead.md`) is that the honest tip count is 2 and row 12 needs no correction.
5. **F5 — the new SF20 row's probe is `http://127.0.0.1:1234/health`, not the child `:45669`.** The
   child port is instance state assigned per spawn; pinning it would go `STALE` at the next respawn.
   `w1/C1ExecNewSurface.json` states this; the landing must not "improve" it to `:45669`.
6. **F6 — `C1ScoutSurfaces`' 14 out-of-table surfaces are a next-round manifest, not this round's.**
   The lesson rejects them with a flip condition; if the L1 adds them now, the C1 claim's scope
   widens after its before-receipt and the kill rule's `ROWS` floor stops meaning anything.
7. **F7 — two PROVINCE rows the manifest probes narrower than the row asserts** (SF11 probes 7 of the
   12 loop dirs; the row's "28 root receipt logs" carries no `count_claim`) — `w1/C1ExecEvidenceTrees.md`.
   Recording this in the lesson's Limits is enough for this round; a `count_claim` would be a
   predicate change and must wait for a freeze.
8. **F8 — mid-wave working-tree events were real and are now gone.** At 15:22:02 three production
   files were mode-changed `100755 → 100644` (content identical) and one seat observed
   `corpus/routed-findings.jsonl` at 0 rows; both were transient, and the ledger's sha256 equals the
   committed blob at 15:26 and 15:33. No seat claims either event and this seat does not attribute
   them. The lesson records the class (`landing`) without naming a culprit; if the L1 can attribute
   them, the row should be sharpened before landing.
9. **F9 — dating SF04 breaks coverage unless the manifest anchor is shortened.** The frozen SF04
   anchor embeds `**ABSENT**` (`plans/round51-surfaces.json:57`), so adding the ISO date to
   `PROVINCE.md:15` without shortening the anchor yields `ANCHOR-MISSING 1` + `UNCOVERED 1`
   (`w1/C1CritUndated.md` verdict); with the anchor shortened, coverage holds and the after-shape is
   reachable. The same report records that the counter prints `REV` but no dirty-tree marker, so
   landing receipts must be taken from a clean clone (round 50's counter printed `TREE dirty=`).

## Limits of this seat

- I drafted the lesson; I did not land it, did not run either frozen counter as a scoring gate, and
  did not edit any production file. The only write is this report.
- Every quoted seat finding is quoted from `.ufo/waves/round-51/w1/` at the revision that report
  names; I did not re-run a seat's measurement to confirm it (role rule: do not rerun to decorate).
- My own measurements are the five consolidated commands above plus file reads; they are point-in-time
  at 15:18–15:33 -03:00 and the working tree moved during that window (documented in F8 and F2).
- Seat-completeness is a census, not a verdict: 15 of 64 seats had no artifact when I counted, and a
  seat still running is not a dead seat. No `provider`-class defect is claimed by this lesson.
- The `## Mistakes` rows cite the round-50 closure and this round's seat reports; where a row's class
  is compound in the source (`survivor / scope` in round 50), I split it into the single class the
  evidence supports and say so in the row text.
- Scratch `/fast/scratch/hyaku/kengaku-r51/C1ScribeLesson` was created for `TMPDIR`, held no clone
  and no receipt, and was removed before yield (verified absent).

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

VERDICT: DRAFTED — `corpus/lessons/round-51.md` is drafted in full at `REV 4090c3d` with a `## Gate`
(two source candidates and one new surface: the llama.cpp `tools/server/README.md` row ADMITTED at
pin `8642541b…`/sha256 `8fd5abde…`, the HF row pending for the L1, the `docs/server.md` premise and
the 14 out-of-table declarations REJECTED with flip conditions, SF20 admitted as a host-state surface
without a digest, two C2 dispositions rejected), a `## Mistakes` table of nine rows in the fleet
vocabulary (`landing` ×2, `attribution`, `reference-drift` ×2, `vacuous`, `number-drift`,
`stale-premise`, `survivor`) drawn from round-50 D1/D3/D5/D7 and this round's own findings, and a
`## Limits` section; the spot-check line is a placeholder because no non-author closure exists yet.
Nine findings are routed to the L1, the sharpest being that the frozen C2 counter is currently
modified in the working tree (uncommitted, `13+/5-`), that C1's `DRIFT`/`NUMBER-DRIFT` legs never read
`PROVINCE.md` (so the after receipt must show the row moved), and that SF01's recorded `prose` is
wrong, making the honest tip `DRIFT` count 2 rather than 3; F9 records that dating SF04 breaks
coverage unless the manifest anchor is shortened.
