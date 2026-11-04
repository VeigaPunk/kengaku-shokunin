# Round 73 — kengaku

Lane: kengaku. Base tip: `d96c3e62`. Axes: coverage and calibration.

- **R73-C1 — coverage:** widen the registry gate's advertised universe to `plans/*.md` and register every advertised instrument; frozen target: `ADVERTISED total=112`, `MISSING 0`, `PREDICATE R73-C1 pass`, rc 0.
- **R73-C2 — calibration:** derive the audit universe from the registry, price all eight fields of all 106 frozen rows, and bind each round-72 erratum item to its own revision; frozen target: `MISMATCH 0`, `PREDICATE R73-C2 pass`, rc 0.

This is the LessonR73 draft, not an admission or a claim verdict. The L1 supplies the landing identity and closure results. Targets above retain the assignment's frozen wording; the amendments and conflicting observations below are evidence, not authority to change it.

## Gate

**S249 — Python `ast` documentation. Admit for the bounded documentation claim; source-row landing remains the L1's responsibility.** URL: `https://docs.python.org/3/library/ast.html`. Access: **2026-11-04T02:46:48Z**. Tier **A**, official Python documentation, scoped to Python **3.15.2** as named by the captured page title (`:20`), not arbitrary Python versions and not the correctness of this lane's audit.

Capture: `corpus/evidence/round73/sources/ast-docs.html`, 362493 bytes, 3338 newline-terminated lines, sha256 `94bead0ac6482efc08bbc790acb1cff809ca4b8a9829a1def2245451a42fe809`. Header evidence: `corpus/evidence/round73/sources/ast-headers.txt`; scout receipt and located passages: `corpus/evidence/round73/sources/ast-anchor.md:7-25,27-87`. The scout records curl rc 0, empty stderr and `HTTP/2 200`; this scribe did not perform a live fetch. This scribe independently read the landed capture and measured its bytes and sha256.

Located quotes (each below 25 words):

- Capture `:2680`, anchor `#ast.parse`: **“Parse the source into an AST node.”**
- Capture `:3038-3039`, anchor `#ast.PyCF_ONLY_AST`: **“Generates and returns an abstract syntax tree instead of returning a compiled code object.”**
- Capture `:2864-2866`, anchor `#ast.walk`: **“Recursively yield all descendant nodes in the tree starting at node (including node itself), in no specified order.”**

Reason: these passages directly support tree generation and descendant traversal. The page does not literally say “without executing”; that clause is **[INFERENCE]** from AST generation rather than a compiled code object, not a quotation. No source quote establishes that this lane's registry parser retains every malformed row, prices every exit path, or binds an erratum correctly. **Flip:** reject any broader use, a version-mismatched citation, or a capture/quote mismatch; restoring the matching captured version and narrowing the claim to its quoted scope restores admission. At this seat's source-table inspection S249 had not yet been appended (`corpus/SOURCES.md` search for S249/S250/S251 returned no matches); the captured opening is real, while a landed SOURCES row is not claimed here. The frozen frontier names only S249 as a new source opening this round.

The round-72 knowledge entry remains on **hold**; this source decision does not discharge its second-wave Q13/Q14 requirement (`plans/round-73-claims.md`, Non-claims item 3). No new entry is admitted by this draft.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| reference-drift | `corpus/lessons/round-72-verifier-spotcheck.md`, §1 cited-commits row and §6 R72-V1, records the round-72 report's 39-hex landing citation `08df910a461620741d433def3df38a8406efe9f` at report lines 5/175/187/310; the valid full value reported there is `08df910ab461620741d433def3df38a8406efe9f`. The underlying report is `.ufo/reports/round-72/kengaku.md` in the fleet, not a lane-owned report. | No hash-length check in the report contract; the non-author verifier subsequently detected it. This seat read that record, not a fresh object-resolution check. | The report cites `git rev-parse` output only; append an explicit erratum rather than silently rewriting the filed report. |
| attribution / number-drift | `corpus/evidence/round72/census-after.txt:1-4` labels `LANE_TIP: b6336136e0e891522b113a94d8e0bd65e0eae8de` and `RUN_AT: 2026-11-04T02:26:17Z`; `corpus/lessons/round-72-verifier-spotcheck.md`, §1 conformance defects (b) and §6 R72-V2, establishes that this was a landing-tree run, not a run of the named freeze tree. | None in the original receipt; later exposed by the non-author verifier. | The census receipt records the tree it measured, distinguishing an uncommitted measured tree from a committed revision when necessary. |
| vacuous | `corpus/lessons/round-72.md:78-81` says `grep -rn 'N14\b\|N20\b' corpus plans` → “no rows”. `corpus/lessons/round-72-verifier-spotcheck.md:108` rejects that rendering. This seat's recursive tool search independently found `plans/battery38/d4m.py:2,11,20,25,41,90`, `plans/battery38/p10a.py:8,18,22,25`, and `plans/round38_c1_verify.py:125,138`, plus the lessons themselves; these are mutation labels, not proof of a ground-id registry. | QUALITY.md's quote-location rule (`corpus/QUALITY.md:31-33`, Q3), exposed by the verifier and independently corroborated here. | Quote the command's observed output. Drop the false “no rows” ground or narrow a new search to a named ground registry; the separate rejection grounds remain separate. |
| attribution | `corpus/evidence/round73/census-before.txt:1-26` is stdout only: 25 W04 lines and the final `ok` path; no command, run timestamp, measured revision or exit status. This seat measured 26 lines / 3285 bytes, sha256 `5bbde4eee78cb5806484850cc0f00ac48e475f62226a9ddf57135ea0d989fcde`. | LessonR73's receipt-shape inspection; no receipt-level provenance check captured it beforehand. | Preserve this original; attach the original runner's command and observed exit status with measured-tree identity. A new run must be labelled a new run, not retroactively substituted for the before receipt. |
| number-drift / scope | Frozen `plans/round-73-claims.md` R73-C2 sentence says `INSTRUMENTS total=106 derived=registry rows=106`; `corpus/evidence/round73/c2-after.txt:3-4` instead records `INSTRUMENTS total=114 derived=registry rows=114` and `PARSED scripts=114 failed=0`, followed by `MISMATCH 0`, rc 0. Amendment A2 (`plans/round-73-claims.md:116-125`) explicitly changes the denominator to `total>=106` and `total==rows`. | LessonR73 read the frozen sentence, the after receipt and the appended amendment; no gate replay by this seat. | Preserve both statements verbatim for the canonical judge. Do not equate the amended denominator with satisfaction of the original literal sentence. Future freezes must account for their own planned row additions before scoring. |

**Frozen-rule conflict, not resolved by this draft.** The assignment states: “No seat edits a predicate, counting command, kill rule or target.” The frozen claims also state: “A rule changed after a seat scores is not this claim's rule.” Amendment A1 says its implementation “gated the extra arm on `plans_only`” and changes the arm to `plans_seen`; A2 says “A2 therefore states the denominator as `total>=106` and `total==rows`.” The original target names 112 advertised instruments; A1's paragraph calls `ADVERTISED total=113>=111` the unchanged target. These texts and `c2-after.txt` are recorded as conflicts for the canonical judge, not adopted as replacement instructions by this scribe.

## Census

- **Before command:** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` is the counting command named by the frozen frontier; **the before receipt does not record the invocation**, so this is the intended command, not a command independently attributable to that receipt.
- **Before exit code:** **not recorded / not independently established**. `corpus/evidence/round73/census-before.txt:26` says `kengaku ok /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md`; that text is not a captured process exit code. Receipt: 26 lines, 3285 bytes, 25 W04 warnings, no row tally. No census rerun was made to decorate this record.
- **After — L1 fills:** measured tree, exact command, observed exit code, receipt path, warnings and any independently derived row tally.

## Spot-check

Non-author closure records **agree/disagree here** — L1 fills from the returned non-author closure record, with its path and reasons. This draft does not pre-claim agreement.
