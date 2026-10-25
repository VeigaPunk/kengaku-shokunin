# FxEntryRejects — Gate rejection and flip review

candidate: `corpus/knowledge/grader-perturbation-audit.md` (draft only)
reviewer: KengakuR26-2.FxEntryRejects
writer: KengakuR26-2
scope: the three `## Gate` rejections and their flip conditions; no prose edits

## Findings

No Q9 defect found in the scoped rejection reasons or flips.

- **D1 MP — reject stands.** The task contract in the pre-amendment critic record requires exactly one fenced JSON block (`.ufo/waves/round-26/build/CritD1Validity.md:5-10`), while the registered parser selects the last block (`corpus/evidence/round8-horizon/horizon.py:38-41`; `critic-defects.md:37-39`). Appending previous-turn truth therefore changes the task-defined selected answer; it is not an MP transform under this contract. The rejected pre-amendment MP metric's baseline-error-mixture reason is specifically evidenced at `CritD1Validity.md:25-29` (n=1815, baseline PASS=983, invariant k=832). It must not be read as a description of current D1: the amended population is separately PC, 909/909 captured (`.ufo/waves/round-26/falsify/FxFamilyD1.md:13-29`; draft lines 50-52, 71, 81-85). Flip condition is adequate: a changed task contract plus independent proof of the reference block's polarity could make this a semantic-preservation test; current contract does not.
- **Novelty +1 — reject stands.** The fetched S045 source documents both equivalent response changes (including whitespace/fences/trailing prose) and wrong-output mutations rerun through answer graders (PyPI `evalmut` 0.1.0 README, §“The two ways an eval lies”; source receipt `corpus/evidence/round26-sources/gate.md:7,11-13`). This is prior art for the claimed mutation/invariance method, not an independent correctness endorsement. The round's novelty rubric requires a previously unobservable construct, an inspectable instrument, and a fetched-URL prior-art verdict (`SCORECARD.md:244`; plan Amendment 1 §6). A distinct construct beyond the published method, rather than a new lane population alone, is the right flip condition.
- **Pooled CP95 as future confidence — reject stands.** The fixed response corpus and deterministic transforms do not supply independent future-response sampling; the draft reports 1,451 unique raw+want+grader inputs and 513 excess duplicates, correlated turns, and model/conversation format clustering (`drafts/grader-perturbation-audit.md:73-79, 93-107`). Its intervals are explicitly descriptive, with pid composites/strata and no iid generalization claim. A registered target sampling model with independently sampled units is an adequate conditional flip, not satisfied by this census.

## Sources, contract, and admission state

Reopened `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-26-claims.md` (C1, Amendments 1–2), `corpus/QUALITY.md:67-107` (Q9/Q10/Q13), `corpus/lessons/round-26.md:27-66`, the draft, `corpus/SOURCES.md:65-70`, and `corpus/evidence/round26-sources/gate.md:32-41`. Public reopens: CheckList §2.2 PDF p.3 / proceedings p.4904 (S048; quote matches); xFinder v3 Abstract (S044; adjacent extraction-bias scope); evalmut 0.1.0 PyPI README (S045; supports shipped-mechanism existence); Python 3.15 `re` docs (S046; `\s` includes CR). S048 corrects the earlier S043 page; the draft cites S048. Quotes/locations and stated limits match the reopened sources.

The current Gate remains `deferred` (`corpus/lessons/round-26.md:29-37`); integration receipt `integration-revision.txt:1-5` says the knowledge entry is draft-only, and the target is absent from the knowledge inventory. Q13 is therefore **pending**, not passed or claimed: a later admission must name returned Q10 reports and include them in the admitting tree. `read xd://lsp` returned `No such tool` and listed mounted devices; no LSP status/references/definition/diagnostics server is available. No runtime checks or code edits were performed.

VERDICT: PASS — all three Gate reasons and flips survive this scoped Q9 review; the candidate remains unadmitted and Q13 support is still pending.