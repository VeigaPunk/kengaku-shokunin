# R54 sibling-overlap scan — CN1SiblingOverlap

## Axes and scope

Declared axes: **novelty** (C1, 8→9) and **calibration** (C2, 9→10). Read `plans/round-54-claims.md` in full first. This is local, read-only connector evidence, not admission, a counter run, or an external prior-art search. No frozen file or sibling file was edited. No tools installed, scratch created, network used, runtime invoked, or tests run.

The scan inspected current filesystem bytes; the HEADs below identify the observation boundary, not a claim that every sibling working tree was clean. A bounded keyword absence is not a fleet-wide proof of absence.

## Scan commands / actual tool queries

Used specialized `glob`/`grep` rather than shell `ls`/`grep`:

1. `glob(path='/home/vgpnk/Projects/*-shokunin;/home/vgpnk/Projects/shokunin/*-shokunin', hidden=false, gitignore=false, limit=200)` located the sibling roots (including the separate `/home/vgpnk/Projects/kimi-shokunin`).
2. `grep(pattern='(?i)opentimestamps|blockchain|anchor[^\\n]{0,80}freeze|entry[^\\n]{0,30}truth|entry_argv', path=P, gitignore=false, skip=0)` produced the lexical hits in the table below.
3. `grep(pattern='(?i)opentimestamps|entry_argv', path=P, gitignore=false, skip=0)` returned **No matches found**. This is the actual command producing the exact-signature absence.
4. Controls-method discovery: `grep(pattern='(?i)mutation.battery|mutat|fixture|hermetic', path=<kasegi plans/tools/knowledge; tameshi plans/tools/knowledge; kumitate knowledge>, gitignore=false)`. That broad result paginated; it was discovery only, not an exhaustive count. Narrowed to discovered `kasegi/corpus/instruments/r47-mutbat.py` and read the tameshi notes named below. Kasegi has no `tools/` path; its executable battery is under `corpus/instruments/`.
5. `glob` over kasegi `corpus/instruments/*mut*` and tameshi/kumitate `corpus/knowledge/*` found the method files. `grep` for `hermetic|GIT_CONFIG|fixture|mutation.battery` located kumitate's substrate ownership; reads followed only discovered paths.
6. Read-only tip capture: `for r in kaidoku tsukuroi kasegi kotodama lore mado tameshi kumitate; do git -C /home/vgpnk/Projects/shokunin/$r-shokunin log -1 --format="$r %H"; done`.

Here `P` is the literal semicolon-joined search path:

```text
/home/vgpnk/Projects/*-shokunin/plans;/home/vgpnk/Projects/*-shokunin/tools;/home/vgpnk/Projects/*-shokunin/corpus/knowledge;/home/vgpnk/Projects/shokunin/*-shokunin/plans;/home/vgpnk/Projects/shokunin/*-shokunin/tools;/home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge;!/home/vgpnk/Projects/shokunin/kengaku-shokunin;!**/.git/**
```

## Lexical hit table

Paths relative to each named sibling. Each matching file is represented once.

| Repo / evidence path | What the inspected lines do | Duplicate / adjacent ruling |
|---|---|---|
| kaidoku `tools/round-43/c1-counter.py:24–55` | Binds interpreter, evaluator and table bytes to an earlier git freeze and compares the manifest's declared tuples. | **Adjacent C1**, not external anchoring: the anchor is a repo commit; no independent time witness appears in this inspected mechanism. |
| kaidoku `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md:94–106` | Explains version-dependent native evidence IDs; `EntryTruth` is a cited seat name. | **Lexical-only**, neither instrument duplicate. |
| tsukuroi `tools/lint-grounding-r51.py:1–25` | Checks quote/citation grounding, source ranges and movable source-row anchors; freeze is retained in git history. | **Adjacent integrity discipline**, not timestamped freeze or registry entry execution. |
| kasegi `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md:18,90–111` | Distinguishes Blockchain/DLT severity classes and source-quote line anchors. | **Lexical-only** blockchain reference, no timestamp/registry instrument. |
| kotodama `corpus/knowledge/myth-symbol/binding-speech-complex.md:32–37` | Records calibration/source limits for oath and binding-speech knowledge. | **Lexical-only**, unrelated instrument. |
| kotodama `corpus/knowledge/verification/verification-independence-anti-circularity.md:20–61` | Separates author/certifier, evidence/generator and claim/anchor; catalogs self-captured green receipts, unpinned freeze docs and re-pin hazards. | **Substantive adjacent C1/C2 prior method**. Independently retained digest/git blob is not the C1 external time witness. Its selftest-versus-frozen-run warning already owns the generic distinction. |
| lore `corpus/knowledge/r99-gate-blind-spot-table.md:9–26,278–280` | Separates semantic dependency findings, digest mismatch and invalid CLI invocation through planted mutations. | **Adjacent controls/calibration**, not either complete R54 instrument. |
| mado `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:318–337` | Source-truth errata cite an `entry-truth.md` seat; explicitly claim no runtime dispatch measured. | **Lexical-only**, not registry-entry execution. |

## Targeted CONTROLS and entry-method overlap

| Repo / evidence path | What it does | Duplicate / adjacent ruling |
|---|---|---|
| kasegi `corpus/instruments/r47-mutbat.py:2–33,144–195` | Runs single-edit counter mutants against selftests on scratch copies; requires clean baseline, exact-one edit target and explicit caught/equivalent/uncaught outcome. Separates tree-fixture probes from counter mutants. | **Same fleet-wide generic own-gate mutation pattern**, not a new R54 construct. Adjacent to both R54 CONTROLS legs; no complete anchor or registry entry-truth counter established here. |
| tameshi `corpus/knowledge/hermetic-env-differential.md:6–58,95–102` | Pins target blobs, runs fresh bwrap fixtures under seven profiles including clean repeat, compares raw exit/stdout/stderr, and limits inference to finite observed profiles. | **Adjacent C2 ENV method**, not a universal hermeticity proof or the 78-row entry ledger. Its profiles exercise selftests, not mandatory registry entry argv. |
| tameshi `corpus/knowledge/gate-row-exit-map.md:7–18,67–89` | `registry-check.py --rev REV` clones and executes declared row argv, requires expected exit and output needles; demonstrates selftest green while a recorded lane command fails. Three staged rows do not cover all CLI refusal codes. | **Strongest C2 overlap**: same command-truth/selftest distinction and cloned registry execution already exist. Adjacent, not an established duplicate of R54's all-rows, entry-only and git-env-scrub conjunction. Generic entry execution cannot be called novel. |
| tameshi `corpus/knowledge/repeated-control-precondition.md:24–35,47–54,68–73` | Distinguishes finite stream agreement, unusable baselines, mismatches and mutation kills; refuses retry-until-green semantics. | **Adjacent controls interpretation**. A fixture/control green is not an admission or proof of determinism. |
| kumitate `corpus/knowledge/agent-isolation-substrates.md:18–19,88–92,161–180,235–240` | Routes bwrap environment testing to tameshi; documents surviving `GIT_CONFIG_GLOBAL`/HOME contamination, minimal launcher env, clone/worktree shared-state boundaries and stronger git config guards. | **Substantive adjacent C2 substrate ownership**. R54's git-environment fix must not be presented as newly discovered fleet isolation technique or full sandbox containment. |

## Observed HEAD boundary

```text
kaidoku  1842addcef3458515859b928b92d9bbd0a46c5d5
tsukuroi d4f2ffe17a461140017ad596f73d0f2d9d8d6c22
kasegi   fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8
kotodama 44f76d456c1b326a71ffdb381590af825cbf11be
lore     0f044aa7c7e4e17cfd5b6278179709b60db45d61
mado     f808ca67dc003f1d4c7ffd70b757cbeec0d42f0d
tameshi  29a89c5e6fd5f2814c1b281ef3354e10130f0f7b
kumitate 14057f3e3899180c95713bace088fb9c0d0046e3
```

## One bounded proposed move: split instrument provenance from control provenance

In the L1's round report, add **one two-level provenance table**: for C1 and C2 separately, name the exact R54 instrument delta, then list the inherited sibling method/control substrate and its limits. Reuse existing controls receipts; introduce no new predicate, threshold, test population or frozen-file edit.

* C1 delta: an outside-repo time witness, not the generic freeze/pin/anti-circularity method already present in kaidoku/kotodama.
* C2 delta: entry-only population closure plus the exact git-env normalization and declared/observed comparison; do not claim invention of registry command execution (tameshi) or environment isolation (kumitate/tameshi).
* Controls: mark own-gate mutation and fixture differentials as inherited fleet techniques, with R54-specific falsifiers separately named.

**Affected axes:** calibration improves through narrower attribution; novelty evidence becomes more discriminating without inventing novelty credit. [INFERENCE] This can preserve the honest frontier because no instrument behavior changes. It does not justify either numeric upgrade.

**Second-order effects:** runtime unchanged; canonical frozen contract untouched; substrate ownership remains kumitate/tameshi; verification reports stop conflating selftest capability, fixture behavior, entry-command observations and independent external attestation. No extra execution load or secret exposure is introduced.

**Contradictions, not averaged away:**

1. The frozen C1 rubric explicitly holds novelty at 8 if externally timestamped preregistration is published practice. This local no-match cannot override that kill/replication condition; external prior-art work is outside this seat.
2. C2's local improvement can coexist with substantial sibling method overlap. Existing tameshi command-truth evidence contradicts any fleet-first generic entry-truth claim; it does not alone refute R54's calibration claim.
3. A normalized git environment is narrower than a complete filesystem/process/network security boundary. Kumitate's bwrap launcher and shared-state warnings remain applicable; this scan makes no claim that R54 implements them.

**Risks:** over-reading keyword absence, treating separate explorer URLs as independent trust roots, treating a sibling receipt as a new R54 execution, or widening frozen predicates to copy stronger sibling methods. None is authorized by this proposal.

**Verification for L1 (not executed here):** check the final report's provenance table against the paths above; ensure each claimed new construct excludes inherited techniques; preserve the frozen claims bytes and existing counting commands; cite already-produced R54 control receipts only for their measured surface. Outside closure still decides the claims. No additional test is proposed as a scoring gate.

## Report-outs (advisory routes, not dispatch)

- **tameshi:** registry row exit truth and selftest/entry separation — `corpus/knowledge/gate-row-exit-map.md:7–18`; bounded fixture/environment comparison — `hermetic-env-differential.md:20–58`.
- **kumitate:** worker git/env isolation and containment boundary — `corpus/knowledge/agent-isolation-substrates.md:88–92,161–180,235–240`.
- **kasegi:** own-counter mutation battery precedent — `corpus/instruments/r47-mutbat.py:2–33`.
- **kotodama:** anti-circularity and claim-versus-anchor attribution — `corpus/knowledge/verification/verification-independence-anti-circularity.md:20–61`.

## Self-evaluation

Accuracy 4/5: claims are tied to inspected lines, but sibling cleanliness was not asserted. Completeness 4/5: both instruments and named controls owners covered; keyword scope is deliberately bounded. Clarity 4/5: lexical and substantive overlap separated, though the hit table is long. Actionability 4/5: one report-only table proposal and exact evidence paths; integration remains L1-only. Conciseness 4/5: retained scan details for reproducibility rather than a shorter unsupported absence. Overall 4.0/5. Improvement priority: L1 should revision-bind reused sibling citations when integrating and retain the local-scan limitation. Would the user agree? Likely: this delivers the requested scoped evidence without changing frozen rules.
