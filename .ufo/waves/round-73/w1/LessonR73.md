# LessonR73 — round 73 w1 scribe

## Behavior and axes

Axes: **coverage, calibration**. Wrote the requested lesson draft, in order: header/claims, Gate, Mistakes, Census, Spot-check. Canonical lesson remains untouched. The draft records S249's real capture, the three required round-72 mistakes, a verified missing-provenance defect in the round-73 census receipt, and the frozen-denominator/amendment conflict. Admission is limited to the source's documentation scope; no claim, entry admission, landing identity or closure agreement is asserted by this seat.

## Gates and execution evidence

No lane gate, audit, selftest, mutant battery, census validator or live fetch was executed by this scribe. Existing receipts are evidence-read, never upgraded into this seat's execution evidence. No verification run followed the writes.

Commands actually exercised (lane cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin` unless otherwise stated):

- `wc -lc corpus/evidence/round73/census-before.txt` → 26 lines, 3285 bytes. In a combined receipt-shape inspection, `grep -nE '^(CMD|rc=|RUN_AT|\$)' corpus/evidence/round73/census-before.txt || echo 'no cmd/rc line'` printed `no cmd/rc line`; the combined shell call returned success, not the census validator's exit status. The file contains only 25 W04 warnings and the final ok path. Its original process exit code is **unavailable**, so the draft expressly refuses to invent rc 0.
- `sha256sum corpus/evidence/round73/census-before.txt corpus/evidence/round73/c1-before.txt corpus/evidence/round73/c2-red-before.txt` → respectively `5bbde4eee78cb5806484850cc0f00ac48e475f62226a9ddf57135ea0d989fcde`, `1a392501ac1095c62686b921b6c145194bb8a881adf9148cc9a320c9904bbb1a`, `9aede37eb17c35be0dcb551589f5a0f286102404c9e656baa4bf6873997bf566`; shell success.
- `sha256sum corpus/evidence/round73/sources/ast-docs.html` and `wc -lc corpus/evidence/round73/sources/ast-docs.html` → `94bead0ac6482efc08bbc790acb1cff809ca4b8a9829a1def2245451a42fe809`, 3338 lines / 362493 bytes; combined shell success. Same digest was observed on the scout's scratch body. No copy or alteration of scout files was made.
- `grep -n 'id="ast.parse"\|id="ast.walk"\|PyCF_ONLY_AST\|Parse the source into an AST node' corpus/evidence/round73/sources/ast-docs.html | head -20` → parse anchor 2678 / quote 2680; walk anchor 2862; PyCF_ONLY_AST anchor 3036. Shell success. Located text was then read around the anchors; HTML tag stripping was used only to view text, not to edit the capture.
- In scout scratch, `cat fetched_utc.txt` and `cat headers` showed `2026-11-04T02:46:48Z`, `HTTP/2 200`, `content-type: text/html`, and response date `Wed, 04 Nov 2026 02:46:48 GMT`; `wc -c body` → 362493; `sha256sum body` matched the landed capture. This is an inspection of another seat's fetch record, **not** a live fetch by LessonR73.
- Read-only `git log -1 --format='%H %cI %aI' d96c3e62`, `git log --format='%H %cI %s' -3`, `git show --stat --format='' 255c261d`, and `git show d96c3e62:plans/round52_c2_registry.py` inspected base/freeze/landing provenance. No git mutations were issued. No landing hash is asserted as this seat's chosen tip.
- One combined shell call inspecting the freeze and old census paths returned **rc 1**: `corpus/evidence/round72/census-before.txt` was absent, while `.ufo/waves/round-72/census-before.txt` existed and hashed to `5bbde4eee78cb5806484850cc0f00ac48e475f62226a9ddf57135ea0d989fcde`. Error diagnostics for absent paths were suppressed by that exploratory command (`2>/dev/null`); no stderr is recoverable from its output. This was not a predicate run.
- Specialized recursive grep for `\bN14\b|\bN20\b` under `corpus` and `plans` found real matches including `plans/round38_c1_verify.py:125,138`, `plans/battery38/d4m.py:2,11,20,25,41,90`, and `plans/battery38/p10a.py:8,18,22,25`. No numeric process exit code is exposed by this tool. It is corroboration of the false “no rows” premise, not a claim to have rerun the historical shell command byte-for-byte.
- Specialized source-table grep for `S249|S250|S251` returned `No matches found` at inspection time. Subsequent L1 source-row landing remains outside this seat's claims.
- Scratch lifecycle: `S=/fast/scratch/hyaku/kengaku-r73/LessonR73; mkdir -p "$S" && trap 'rm -rf -- "$S"' EXIT && printf 'SCRATCH_CREATED_AND_CLEANED_ON_EXIT=%s\n' "$S"` → success, printed the owned path; exit trap removed it. No temporary files or fixtures were created. No post-cleanup verification command was run.

Static evidence reads included the entire frozen claims before commands; the operator rules; godspeed and self-evaluation skills; round-72 lesson/verifier; QUALITY Q3/Q45; round-72 census-after; round-73 before/control/after receipts; scout anchor receipt; dispatch/spec; source-table searches. Additional shell directory listings and static text inspections did not execute product behavior. Early exploration used shell listing/search/paging rather than the preferred specialized tools; that process deviation is not execution evidence for any gate.

## Findings and conflicts

1. **Required round-72 mistakes covered:** reference-drift (39-hex landing citation), attribution/number-drift (census tree label), vacuous (false no-rows sweep). Each row names evidence, captured-by and fix. Prior verifier observations remain explicitly attributed to that verifier.
2. **Round-73 census provenance missing:** `corpus/evidence/round73/census-before.txt` carries neither invocation nor process status. The requested before exit code cannot honestly be supplied from these bytes. The draft gives the intended frozen command and marks exit status unestablished. L1 needs the original runner's record, not a relabelled new run.
3. **Frozen denominator conflict:** original R73-C2 says `INSTRUMENTS total=106 derived=registry rows=106`; `c2-after.txt:3-4` records 114/114. A2 says: “A2 therefore states the denominator as `total>=106` and `total==rows`.” The assignment says: “No seat edits a predicate, counting command, kill rule or target.” These are passed verbatim to the canonical judge; this scribe does not reconcile them by changing the original sentence.
4. **Universe-arm conflict:** A1 describes replacing `plans_only` with `plans_seen`, and calls `ADVERTISED total=113>=111` the unchanged target, while the assignment names 112. Recorded, not adjudicated or adopted as a new instruction.
5. **Source scope:** S249's `ast.parse` and `ast.walk` quotes are real. “Without executing” is explicitly [INFERENCE], not a literal quote. The source does not prove audit completeness. The scout receipt now supplies landed headers and anchors; an earlier partial-capture observation was not retained as a final defect.

## Touched surfaces and artifacts

Only these durable writes were made:

- `corpus/evidence/round73/w1/lesson-draft.md` — draft intended for L1 landing at `corpus/lessons/round-73.md`.
- `.ufo/waves/round-73/w1/LessonR73.md` — this report.

The owned scratch directory was created and removed by its shell exit trap. No files were written in `/tmp`; no product code, predicates, targets, source rows, canonical knowledge/lessons, state, judge, fleet files or sibling files were edited. No installs or updates; no subagent dispatch; no other runtime invoked; no commit/push/publish/deploy.

## Out of scope and handoff

L1 lands the draft and supplies its measured after-census, landing identity and non-author closure agreement/disagreement. The canonical judge decides the A1/A2 conflicts. This seat deliberately leaves those requested integration slots labelled, not falsely completed. No additional tests are represented as passed.

## Self-evaluation

Accuracy 4/5: unrecorded census rc is refused, and historical observations are attributed; original runner provenance remains missing. Completeness 4/5: all five sections exist, but after/closure are intentionally L1-owned. Clarity 4/5: original versus amended claims are separated; the report's command log is lengthy. Actionability 4/5: exact landing draft path and missing census provenance are named; judging amendments is not this seat's authority. Conciseness 4/5: the draft keeps one table row per mistake, though evidence detail enlarges the report. Overall 4.0/5. Highest-impact improvement is to attach the original census invocation/status record if the L1 has it; never fabricate it. User-agreement self-check: the draft is usable without interpreting an unrun check as passed.
