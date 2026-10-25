# R29a2RejectGate — refusal quality of the Gate block

Seat: `L1Kengaku29.R29a2RejectGate` (leaf; read-only outside this file). Round 29 attempt 2,
audit time `2026-10-25T06:45:32Z`.

Axes named: **coverage** (every refusal on the Gate surface enumerated, none sampled) and
**operability** (each verdict carries the exact edit that flips it, and each attempt-2 refusal
carries the property its reason must cite).

## 1. What was audited, and what could not be

| target | status | evidence |
|---|---|---|
| draft Gate block `/tmp/r29a2-GateBlock/gate.md` | **ABSENT** at audit time | `ls -la /tmp/r29a2-GateBlock/gate.md` → `No such file or directory` — four checks (03:42 the directory itself did not exist, 03:43 quote dir only, 06:45, 06:52) |
| scribe scratch | exists, quotes only | `find /tmp/r29a2-GateBlock -type f` → 13 files under `quotes/` at 06:45, 15 at 06:52 (S077 S078 S078gate S079toml S079tree S080 S080task S080tree S090 S091 S091arc S091live2 S091snap S091ua S105), no `gate.md` |
| scribe seat | still running, no output | `agent://L1Kengaku29.R29a2GateBlock` → "# L1Kengaku29.R29a2GateBlock (running) — No final output yet" |
| fallback ordered by the assignment: attempt-1 Gate surface | audited | `corpus/lessons/round-29.md` md5 `5516a28f5b5479395ef1b8fd4b3b44eb`, §Gate `:24-30`, §Gate — final v3 decision `:106-110` |
| same-round companion Gate surface | audited (extra) | `corpus/lessons/round-29-source-copy-containment.md` md5 `17fe4d693d1389f4c1118f65dad3e872`, §Gate and mistakes `:51-59` |

`lsp` device: **not mounted** — `read xd://lsp` → `No such tool: xd://lsp.` followed by the device
list (ast_edit, debug, aseprite/blender/godot/tripo/unity MCP paths). No semantic
references/definition/diagnostics were therefore available; every locator below is a literal
`file:line` read or a grep with its command shown. This is a disclosure of method, not a claim
about code callers.

Effort was concentrated on the question the assignment asks — *does a refusal's reason bear on the
property the rejected claim asserts, and does it state a flip condition* — because a correct verdict
with a wrong reason is a gate failure under QUALITY Q9 (`corpus/QUALITY.md:67`), whose canonical
instance is `corpus/lessons/round-24.md:31`: "the S023 rejection reason cited S006 (Pro task validity,
~30% broken tasks) as refuting Scale's contamination-resistance claim — a different property".

## 2. Refusal audit — one row per refusal

Columns: the rejected candidate, the reason as written, the property the reason actually addresses,
whether that is the property the claim asserts (T1 = Q9 test), the flip condition as written
(T2 = Q8 test), verdict. "—" means the row states no flip condition at all.

### 2.1 `corpus/lessons/round-29.md` §Gate (`:26-30`)

| # | Refused candidate → property it asserts | Reason as written | Property the reason addresses | T1 | Flip condition stated | T2 | Verdict |
|---|---|---|---|---|---|---|---|
| R1 | "scientific method novelty or a novelty-score increase for this projection" → prior-art novelty of the construct **and** the lane's novelty score | "S074 already implements ordered serialized-text projection; acquired audit repertoire is local, not method novelty." (`:28`) | prior practice for the same construct, at the pinned commit — `corpus/SOURCES.md:96` (S074: "as prior practice for the round29 projection … task.py:55–69 ordered replace then json.loads") | **MATCH** for both conjuncts: the novelty score is mechanically prior-art driven — `SCORECARD.md:47-48` "novelty proxy — fraction of the round's headline claims carrying a prior-art verdict with a fetched URL" | "Flip: separately registered distinct construct and bounded prior-art evidence." (`:28`) | pass — a distinct construct with its own prior-art search is exactly what would reverse it | **SOUND** |
| R2 | "synthetic projections establish deployment configs, task validity or model errors" → **three** properties: real config values; task validity; model-error observation | "No actual env_config values, browser/helper/judge outcome or deployment is observed. Flip: separately pinned sanctioned runtime evidence." (`:29`) | (a) actual `env_config` values → config-reality property; (b) browser/helper/judge outcome → runtime behaviour; (c) **task validity → nothing in the reason** | (a) **MATCH**; (b) **MATCH**; (c) **MISMATCH** — validity is a static property of the task specification, not of a run: a task can be invalid and still execute, and valid and never execute. The reason contains no validity evidence and no validity criterion | "Flip: separately pinned sanctioned runtime evidence." (`:29`) | fails on leg (c): pinned runtime evidence flips (a) and (b) and cannot flip a validity rejection; the property-matched flip is an instrument applied to the actual task set | **UNSOUND** (leg c) |
| R3 | "ambiguous F3 earns calibration credit" → forecast credit accounting | "Resolution criterion was not frozen; correct counts cannot retroactively establish a forecast success." (`:30`) | forecast resolution contract — same property, and the correct rule (`corpus/QUALITY.md:179` Q18 "a forecast freezes its resolution criterion"; `round-29.md:17` M89) | **MATCH** | **none** — the row is the only rejection in the file without a `Flip:` clause (`grep -in 'reject\|deferred' corpus/lessons/round-29.md` minus `flip` yields `:30` and `:110` only) | **fail** — `corpus/QUALITY.md:61` Q8 requires "reason and flip condition"; the reversal exists in Q18/M89 but is never stated in the row | **UNSOUND** (flip) |

#### R2 detail — the property-matched reason the lane already owns

The lane has the right evidence class for leg (c) and used it in a neighbouring round:
`corpus/SOURCES.md:28` (S006) — "agent-plus-human audit flagged ~30% of SWE-Bench Pro tasks broken
across four failure categories". Round 28 states the same rejection with the property named:
"Structural schema compatibility cannot establish intent completeness, runtime state, model ability,
or contamination freedom. Flip: independently observed sanctioned task-level validity evidence"
(`corpus/lessons/round-28.md` §Gate, the "812 inventoried task specs imply 812 semantically valid
tasks" row). Round 29's compressed three-legged row keeps the config/runtime clauses and drops the
validity clause, then reuses the runtime flip for all three legs.

Required shape of the fix, per Q9 ("otherwise the reason is rewritten as a superseding row"): the
landed row is historical and stays byte-identical; the attempt-2 Gate either splits the candidate
into three rows or writes one row whose reason names, per leg, the property-matched evidence and
whose flip is per leg (validity ← an S006-class audit of the actual tasks, not a pinned run).

### 2.2 `corpus/lessons/round-29.md` §Gate — final v3 decision (`:108-110`)

| # | Refused candidate → property | Reason as written | Property the reason addresses | T1 | Flip condition stated | T2 | Verdict |
|---|---|---|---|---|---|---|---|
| R4 | `knowledge/webarena-config-projection.md` v3, deferred → entry conformance at one byte revision | "Exact-v3 PASS re-reads returned, but FEntrySources found renderer-dependent Python-doc line locators. V4 replaces only that header locator with stable section/API fragments through new correction S075. No v3 admission was landed." (`:110`) | locator stability of a cited anchor — a conformance defect (Q10 location re-read, Q1 `source:` anchor) | **MATCH** — the refusal is grounded in the same property the candidate claims (conformance), and the defect is named concretely | **not labelled**; the row names the repair (V4 + S075) but never the condition under which the candidate becomes admissible | **fail as written** — the actual flip, visible in the later admit row (`:124`): two registered reviewers distinct from the writer returning complete re-reads with matching sha256 on the corrected bytes | **UNSOUND** (flip) |

Contrast that makes this a real finding rather than style: round 27's deferred row enumerates its
conditions ("L1 must first finish measurements, freeze exact bytes, receive complete second-seat
source/number re-reads with matching sha256, resolve findings, and retain eligible returned reports
in the actual admission commit", `corpus/lessons/round-27.md` §Gate) — that enumeration functions as
a flip. Round 29's names a repair path and no acceptance condition.

### 2.3 companion lesson `round-29-source-copy-containment.md` §Gate and mistakes (`:53-59`)

These are the round's other recorded rejections; their third column is "Decision / prevention"
rather than reason+flip, and the file contains **0** occurrences of `flip`
(`grep -ci flip corpus/lessons/round-29-source-copy-containment.md` → `0`).

| # | Refused candidate → property | Reason as written | Property the reason addresses | T1 | Flip | T2 | Verdict |
|---|---|---|---|---|---|---|---|
| C1 | "Treat five absent loose paths as all material absent" → scope of an absence claim | "Rejected: distinguish path scope from archive/member scope and name all inspection limits." (`:55`) | scope of the check performed | **MATCH** | stated only as the replacement rule ("distinguish path scope from archive/member scope"), not as a condition | partial | **UNSOUND** (flip not stated as a flip) |
| C2 | "Keep the unrelated fetched wheel in the current corpus" → retention decision | "Rejected: remove the known carrier, retain only sanitized metadata…" with "No active production dependency; flagged module is still present in the package" (`:56`) | dependency need **and** carrier presence — the retention property | **MATCH** | **none** as a condition | fail | **UNSOUND** (flip) |
| C3 | "Treat tip containment as historical purge or credential remediation" → history state | "Rejected: … The introducing commit remains reachable from the advertised master baseline" (`:57`) | reachability of the introducing commit | **MATCH** | **none** — the reversal condition would be non-reachability or a rewrite | fail | **UNSOUND** (flip) |

### 2.4 same lesson, outside the Gate tables — the withdrawn mistake row (`:21-22`)

| # | Refused candidate → property | Reason as written | Property the reason addresses | T1 | Flip | T2 | Verdict |
|---|---|---|---|---|---|---|---|
| R5 | the draft lesson's proposed `M85` row and its claim that "the plan required URL-only substitution" → (i) uniqueness of a mistake-row identifier; (ii) what the plan actually requires | "r28 already used M85/M86. Its statement that the plan required URL-only substitution was false; URL-only is a negative control, not the required oracle." (`:21-22`) | (i) an identifier collision with `round-28`; (ii) the plan's requirement, asserted without a locator | **MATCH** on both properties, with an evidence-pointer gap on (ii): the falsity claim names no plan line, and this row is the only place the withdrawal is recorded | **none** stated | fail | **UNSOUND** (flip); add a plan/prompt locator for the "false" conjunct and a reversal condition |

## 3. Attempt-2 obligations — refusals the new Gate must carry, with the property each must cite

The attempt-2 Gate does not exist yet, so these are pre-registered obligations derived from the
frozen claims and from receipts already on disk. Each line names the trap that would make the reason
unsound under Q9.

| obligation | candidate | property the reason MUST cite | property that would be UNSOUND (M21 shape) | property-matched flip | evidence |
|---|---|---|---|---|---|
| O1 | the staged rows this round does not append | **scope** — the row is not cited by `corpus/knowledge/benchmark-task-validity-checklist.md` | "recheck-prose" / "malformed" — registry-hygiene properties; 171 of 173 staged rows carry only that defect, so a single bucket would silently refuse 168 rows for the wrong reason | a later round whose frozen `adoption-expect.json` names the row | `.ufo/waves/round-29/attempt2/package-gate.txt:1` `registry=76 staged=173 collisions=0 malformed=2 duplicates=0 defects=171`; `adoption-expect.json` names exactly 5 sources; 171 `defect …: recheck-prose` lines at `:3-173` (`grep -c 'defect .*recheck-prose'` → `171`), `exit=4` at `:174`, file length 174 lines |
| O2 | S093 and S101 | **row schema** — an escaped `\|` inside a cell | "not primary" / "out of scope" — a provenance property, not a schema one | a rewritten row with the pipe removed, re-run through the gate | `package-gate.txt:2` `malformed: S093:escaped-pipe S101:escaped-pipe` |
| O3 | "C2 delivers clause 3 (prose `recheck` normalized)" if it is refused | **reachability of the normalization path from `main()`** — `check()` returns `EXIT_MALFORMED` before `build_block` runs | "case 6 fails" — it does not fail; it PASSes on a branch the product cannot execute | a case that composes `check()`→`build_block` on a prose row and turns red when the normalize branch is deleted | `.ufo/waves/round-29/attempt2/build/R29a2FixtureMutations.md:112-125` ("case 6 tests a function the CLI can never reach in that state"; the two frozen clauses are "in direct tension") |
| O4 | S091 / S105, if any row is kept for them | **register labelling** — `quote-column misbinding` / extraction artifact; the registered string is the recheck command, not a quotation | "payload-absent" / "content fabricated" — the row's own scout asserts the opposite | the register row corrected to bind the actual quote column | `.ufo/waves/round-29/attempt2/build/R29a2QuarS091.md:22-23` "the register's own header says an ABSENT row is 'a CANDIDATE, not a verdict' … Corrected quote is available; **no refusal needed**" |
| O5 | S090 quote wording, if touched | **wording of the served page** — exact match found; the fix is narrow | "quote absent / source refused" — would contradict the landed entry's axis D and canary rows | — (no refusal is warranted at all) | `.ufo/waves/round-29/attempt2/build/R29a2RevQuoteS090.md:52` "Wording on the page is exact, so the fix is **narrow, never refuse**" |
| O6 | the entry as a whole, if any of the five rows is refused | **that row's own failure** (not openable on 2026-10-25, or no locatable ≤25-word quote) | "insufficient coverage" / "weak tier" — a coverage property used to justify an atomicity refusal | the refused row re-opened with a located quote in the opened bytes | `plans/round-29-attempt2-claims.md:42-47` kill rule ("that row is refused and the entry is refused as a whole"; "A refused entry is recorded with reason and flip condition") |
| O7 | the entry's corrected package-unit counts, if recorded at all | **package unit convention** (file vs directory counting) | "entry claim wrong" — the entry states the package's *claims* were right, its *units* off | the package restated in the entry's unit convention | `corpus/knowledge/benchmark-task-validity-checklist.md:66-68` ("Both counts correct the staged package, which said \"92 top-level task directories\" and \"109 task directories\". The package's *claims* were right; its *units* were off") |

Two positive requirements that follow from §2: every attempt-2 rejection row must carry an explicit
`Flip:` clause (R3/R4/R5/C1–C3 all failed that), and any multi-leg candidate must be split per
property before a reason is written (R2).

## 4. Residual risk and verification gaps

1. **The audited draft is not the attempt-2 draft.** `/tmp/r29a2-GateBlock/gate.md` did not exist at
   any of my four checks; the attempt-2 rows cannot be judged until the scribe publishes. If the
   scribe reuses the attempt-1 row shapes, R2's three-legged compression and R3/R4's missing flips
   carry over.
2. **No LSP device**, so no semantic proof of callers existed for any code claim; I did not make
   code-caller claims, and the one code-adjacent observation (O3) is quoted from a seat's report
   rather than re-derived.
3. **Moving target.** `plans/sources_adopt.py` was modified and uncommitted during the audit
   (`git diff --stat` → `1 file changed, 47 insertions(+), 13 deletions(-)`), and the diff is itself a
   scoped-mode rewrite of the clause-2/clause-3 tension in O3 (it rewrites `check()` to filter
   `clash`/`dupes` to the requested ids and to stop treating a prose `recheck` as fatal). My
   observation `python3 plans/sources_adopt.py --selftest` → `SELFTEST cases=10 failed=0`, exit 0,
   is of that working copy at audit time, **not** of committed blob `8c14a5d`. Any Gate claim about
   C2 must pin a blob, not the worktree.
4. **O1 is an interpretation of Q8, stated as such.** Q8 requires a reason for every candidate
   "screened and not admitted"; whether 173 staged rows are 173 candidates or one package is the
   L1's call. Either way the reason must cite the property that actually decided the exclusion, and
   the trap named in O1 is real regardless of which reading wins.
5. `corpus/knowledge/benchmark-task-validity-checklist.md` was untracked at audit time
   (`git status --porcelain`), so no admission claim can be checked; nothing in §3 depends on it
   being landed.

Tool installs or upgrades this seat: **none** (no pacman transaction, no `uv`/`npx` install; the
`--selftest` run needs only the preinstalled `python3`).

## Appendix — scribe scratch inventory inlined (the draft-absence evidence)

Scratch is not durable (sibling lanes saw `/tmp` seat dirs swept and re-created within minutes), so
the only finding that depends on `/tmp` is recorded here as bytes rather than as a path. Observed at
`2026-10-25T06:45Z`; `find /tmp/r29a2-GateBlock -type f` returned 13 files, all under `quotes/`, and
`gate.md` did not exist at any of four checks (03:42, 03:43, 06:45, and one re-check after the first
report write). A later check at 06:52 returned 15 quote files — the seat is still fetching, which is
consistent with "running, no published draft" and is not evidence that a draft exists.

```
S077 41842      S078 6858       S078gate 1659   S079toml 973
S079tree 26062  S080 16883      S080task 227    S080tree 29447
S090 53390      S091 418        S091arc 270     S091live2 418
S091snap 60132  S091ua 418      S105 13027
```

(15 files, 252 024 bytes total; `ls -l /tmp/r29a2-GateBlock/quotes/ | awk 'NR>1{s+=$5; n++} END{printf "files=%d bytes=%d\n", n, s}'` → `files=15 bytes=252024`.)

If the scribe publishes after this audit, the attempt-2 Gate rows are unjudged by this report; the
obligations in §3 are the checklist to apply to them, and R2/R3/R4 are the attempt-1 shapes that
should not be copied unchanged.

