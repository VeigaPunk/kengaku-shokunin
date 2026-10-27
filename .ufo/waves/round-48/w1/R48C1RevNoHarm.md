# R48C1RevNoHarm — C1 fence cross-axis / security-boundary review

Axes named: calibration (claim axis); security-boundary correctness / containment (primary no-harm concern); operability (secondary); coverage, novelty, depth, freshness, adjacency (potential cross-axis impact).

## Finding: high-risk widening is the `objects/info` exception

The base fence at measured revision `REV a543d92083557dd9b33ee674e9b99b03411f80af` is unchanged from `0f77f9b` (both `plans/fixture_fence.py` SHA-256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`; `git diff 0f77f9b a543d92 -- plans/fixture_fence.py` produced 0 lines). `_objects` currently permits `objects/info` only when empty; any child returns `object-store redirect`. This protects the object-lookup boundary against `objects/info/alternates`, while the honest gc/reflog-gc cases plausibly need commit-graph metadata there. A broad relaxation such as “allow nonempty info” or accepting path-bearing entries would re-admit an object-store redirect and could cause the fenced tool to resolve objects outside the fixture.

**Exact testable risk:** in the repaired fence, an honest fixture with `objects/info/commit-graph` (and any actually required commit-graphs layout) must be admitted, while an otherwise identical fixture with `objects/info/alternates` pointing outside `d` must be refused with zero traced outside access. Test the exact frozen hostile `plans/refusals46/f5_alternates.py`, plus an independently authored alternate-path variant, against the landed repair; require the C1 SEALED/REFUSALS lines to remain clean and traced outside access zero. Keep the exception name/type-specific; do not infer that every `objects/info` child is benign. This is a plausible security harm, not a measured result of the R48 repair (no repaired fence was available in this frozen-base clone).

A separate high-value attack check is that special-casing commit-graph does not weaken symlink/hardlink checks on `objects/info`, `objects/pack`, refs, or packed-refs. Frozen sealed modules `s_objects_link.py`, `s_packed_refs.py`, `s_refs_link.py`, `p_info_redirect.py`, `p_pack_redirect.py`, and `p_refs_redirect.py` encode these redirects. The base source checks symlink/hardlink types and classifies packed refs; preserve those checks when broadening ordinary repository states.

## Evidence quality / limits on inferred repair

The round-46 honest receipt does not establish store-level refusal causes for the nine novel honest fixtures. Exact command run: `grep -E "sealed46/honest_" /fast/scratch/hyaku/kengaku-r48/R48C1RevNoHarm/lane/.ufo/waves/round-46/w2/R46W2C1HoHonest/receipts/c1-counter-override.txt | sort`. Verbatim output pattern for all nine: `FENCE-RUN sealed sealed46/honest_0N.py honest-... BREACH touches=0 calls=425 -- BREACH --lane value '{WORK}/repo' is a placeholder the fence cannot resolve` (N=01..09). Thus the cited 9/9 refusal is confounded by the placeholder argv rejection; it cannot show which store checks, if any, rejected packed refs, annotated tags, detached HEAD, merge commits, `.gitignore`, long history, reflog gc, tag+detached HEAD, or ignored untracked files. Static source does show a narrow detached-HEAD incompatibility: `_store` accepts only `HEAD_REF` (`ref: refs/heads/...`), although `HEX40` exists for detached HEAD. In contrast, `_tree` allows ordinary regular worktree files, and `_packed` already parses packed-ref headers/peeled lines. Therefore do not broaden unrelated tree/config/ref checks absent a real-argv reproducer. For each honest fixture, rebuild with a concrete lane path and report its actual `breach()` reason before choosing an exception.

The round-46 spotcheck records the other relevant boundary failure: `links_special_names.py` admitted a newline-containing filename with `touches=0`; the v3 classification makes zero-touch admission BENIGN-ADMIT, not a leak. This is a separate containment/advertisement test, not evidence that newline filenames cause outside access. A testable robustness check is to retain zero-outside-access tracing for all admitted fixtures and ensure the newline path cannot alter argv/path interpretation.

## Other axes and scope

The frozen claims document says C1 and C2 counters/files are disjoint; static grep finds `fixture_fence` references only in historical C1 plans/counters, not a live C2 consumer. I found no demonstrated direct effect on coverage, novelty, depth, freshness, or adjacency from this file-only repair. Operability could be harmed if the repair adds unbounded parsing or mount traversal: retain bounded reads/walks and verify honest/hostile runs do not hang. The round-46 mount-point note says lexical containment does not prove backing-store containment for bind mounts; R48's stated contract is narrower: admit only when every decision read is inside `d`. Verify with an in-scratch mount-boundary fixture only if safe/available; do not claim mount safety from lexical checks alone.

## Freeze and commands

Stage-1 freeze exists and is committed: `git cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af` → `commit`; its `plans/round-48-claims.md` contains the two-stage freeze and says stage 2 precedes scoring. The frozen-base clone identity was `git rev-parse HEAD` → `a543d92083557dd9b33ee674e9b99b03411f80af`; `git rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r48/R48C1RevNoHarm/lane`. Later commits inspected were dispatch/ready marker files only, not the fence. No scored counter/probe was run; no R48 repair or stage-2 measurement existed in this clone, so this is a source/receipt review only.

Exact commands run (selected evidence commands):
- `git log --oneline -5`
- `git cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af`
- `git show a543d92083557dd9b33ee674e9b99b03411f80af:plans/round-48-claims.md | head -20`
- `git show --stat --oneline 453ddfd`; `git show --stat --oneline bf783c1`
- `git diff 0f77f9b a543d92 -- plans/fixture_fence.py | wc -l`
- `git show 0f77f9b:plans/fixture_fence.py | sha256sum`; `git show a543d92:plans/fixture_fence.py | sha256sum`
- `git clone --shared --no-checkout ... lane`; checkout of frozen base; `git rev-parse HEAD`; `git rev-parse --show-toplevel`
- `grep -E "sealed46/honest_" .../c1-counter-override.txt | sort`
- Read source files/reports named above; no code execution of the fence, counter, or probe.

Source citation protocol (access date 2026-10-27; local URL is `file://`):
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — quote: “The mount-point refusal noted in `w2/R46W2C1Intent.md` is honoured”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — quote: “9/9 novel honest fixtures refused”.
- `file:///fast/scratch/hyaku/kengaku-r48/R48C1RevNoHarm/lane/plans/fixture_fence.py` — quote: “if inner: return f\"{label}/info/{inner[0][0]} present (object-store redirect)\"”.
- `file:///fast/scratch/hyaku/kengaku-r48/R48C1RevNoHarm/lane/plans/refusals46/f5_alternates.py` — quote: “objects/info/alternates”.
- `file:///fast/scratch/hyaku/kengaku-r48/R48C1RevNoHarm/lane/.ufo/waves/round-46/w2/R46W2C1HoHonest.md` — quote: “all nine are newly named modules in the counter's `--sealed` override”.
- `file:///fast/scratch/hyaku/kengaku-r48/R48C1RevNoHarm/lane/.ufo/waves/round-46/w2/R46W2C1HoPaths.md` — quote: “a non-Git repository filename with an embedded newline remains admissible”.
- `file:///fast/scratch/hyaku/kengaku-r48/R48C1RevNoHarm/lane/.ufo/waves/round-46/w2/R46W2C1Intent.md` — quote: “A bind-mounted directory below `d` is an ordinary directory to these checks.”
- `file:///fast/scratch/hyaku/kengaku-r48/R48C1RevNoHarm/lane/plans/round46_c1_verify.py` — quote: “a module is CLEAN only if every fixture it builds is refused”.

Limits: the R46 receipt is historical, not a scored R48 run; the 9 honest refusals are argv-placeholder failures, so exact store-level causes remain unverified. No repaired fence was inspected, no scored execution was run, and this report does not claim C1/C2 admission.

VERDICT: `R48-C1 no-harm risk identified — broad objects/info relaxation can leak alternates; require exact commit-graph allowlisting and real-argv hostile controls. Other-axis harm not demonstrated.`