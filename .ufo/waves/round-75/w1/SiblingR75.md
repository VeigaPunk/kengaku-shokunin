# SiblingR75 — cross-lane overlap scan

## Axes and evidence scope

- **Coverage:** R75-C1, L0-capped at 7. **Calibration:** R75-C2, ceiling 10 exercised; no score change proposed.
- Read `plans/round-75-claims.md` in full before the first shell command. Frozen predicates, targets, controls and kill rules remain unchanged.
- Read-only searches covered all six named sibling repositories. Evidence below is local source inspection, not execution or certification of sibling gates. Paths in the table are relative to the fleet root, not this lane.
- Ran the `grep` tool with `parity|expected.{0,15}(id|finding)|null.arm|measured.revision|revision.stamp|receipt.{0,25}(revision|commit)` separately over kumitate, kotodama, kama, chousa and mori (excluding wave artifacts, corpus, plans, reports and historical logs for the initial production scan); separately searched tabi `scripts/` for `null.arm|expected.{0,15}(id|finding)|index.parity|measured_revision_not_ancestor|counter_digest_mismatch`. Follow-up targeted greps located the exact code lines below. Grep returns printed matches rather than a shell exit status; quoted lines below are the observed output evidence. No sibling runtime was invoked.

## Hits and disposition

“Duplicate” denotes the named mechanism, not byte-identical code or equal universes. “Adjacent” means overlapping purpose with a different contract. “New” means an additional mechanism relative to the two frozen R75 instruments, not novel across the fleet.

| Lane / surface | Grepped path:line and observed code/text | What it does; disposition relative to R75 |
|---|---|---|
| kumitate / index parity | `kumitate-shokunin/scripts/readme-map.mjs:189-202`: `const fileSet = new Set(cf.files)`, `orphan-row`, `if (!rowSet.has(f)) bad.push(\`uncovered:${f}\`)` | **Duplicate, C1 knowledge/lessons portion:** compares path identities in both directions rather than trusting equal counts; default directories at :85 are knowledge and lessons, so this is not evidence of the third R75 evidence-directory universe. |
| kumitate / retention ratchet | `kumitate-shokunin/scripts/readme-map.mjs:28-39,48-58`: `covered-not-file`, `stale-covered`, `duplicate-row`, `unpinned` | **New relative to C1:** a pinned historical covered set and duplicate/type checks additionally catch coordinated file-and-index deletion; importing this would expand the frozen contract, so do not absorb this round. |
| kumitate / freeze-time parity | `kumitate-shokunin/scripts/plan-before-ready.sh:26-46,165-168`: runs the map inside `git archive PLAN`; `a late repair cannot launder a freeze made over a red map` | **Adjacent, C1:** checks parity at plan freeze, whereas R75 explicitly permits a red-before index and repairs it at landing; treating this as an interchangeable gate would contradict the frozen before/after design. |
| kumitate / receipt reproduction | `kumitate-shokunin/scripts/receipt-evidence.mjs:185-194`: replays recorded argv and compares child exit plus stdout/stderr SHA256 | **New relative to C2:** establishes reproducibility beyond stamp ancestry; its nonce/ledger/span requirements (:11-35) are separate obligations, not implications of R75 stamp success. |
| tabi / registry | `tabi-shokunin/scripts/check-gate-registry.mjs:373-376`: sorts actual and expected finding IDs and requires exact equality plus exit agreement | **Adjacent, C2:** registry selftests use attributed findings; this is not itself the R75 mutant metric or its disk corpus parity universe. |
| tabi / provenance | `tabi-shokunin/scripts/check-measurement-binding.mjs:575-613`: `measuredRevisionNotAncestor`, `counterDigestMismatch`, `counterChangedSinceMeasurement`, `countedInputChanged` | **Adjacent, C2:** shares ancestor validation but additionally binds producer digest and counted inputs at measured/evaluated revisions; an ancestor stamp alone is weaker. |
| tabi / mutation controls | `tabi-shokunin/scripts/check-gate-mutants.mjs:215-244`: `const killed = !res.clean`, separates faults and benign mutants; :296 declares `crash-counts-as-killed` | **Adjacent, C2:** benign rewrites supply a null-like negative control, but any unclean run kills a fault; it does not implement R75 expected-finding attribution. Do not substitute its kill count for R75's. |
| kotodama / attributed controls | `kotodama-shokunin/tools/check-evidence-coupling.py:1559-1568`: compares `(expected_exit, sorted(finding_ids))` with `(code, sorted(actual IDs))`; :1833-1838 requires stable IDs on domain controls | **Duplicate, C2 attribution primitive:** expected exit/ID pairs reject unrelated failures; its packet controls are not evidence that the R75 nine-mutant/null battery ran. |
| kotodama / sequencing | `kotodama-shokunin/tools/check-receipt-seq.py:142,155,174-175,188-197`: header equality, tree/digest comparison and `parent == h["stamped"]` | **New relative to C2:** binds measured/evaluated/stamped identities and receipt-carrier parentage; carrier topology is stronger and different from ancestor acceptance. Its documented post-records restriction (:18-22) avoids demanding a not-yet-existing carrier. |
| kama / expected findings | `kama-shokunin/tools/kama-ollama-evidence.py:438-443`: appends `exit_mismatch` / `finding_mismatch` and passes only with no mismatch reasons | **Duplicate, C2 attribution primitive:** ordinary CLI fixtures require the intended exit and diagnostic, not merely nonzero exit; no R75 mutant/null execution inferred. |
| kama / ancestor plus intervening drift | `kama-shokunin/tools/round72-receipt-tip-binding.py:60-68,184-185`: conflicting headers refused, ancestor checked, intervening non-record changes classified `shifted` | **Adjacent, C2:** ancestry is shared; a recorded ancestor is insufficient if later instrument/input edits occurred. Population is round-cited receipts, unlike R75's immediate `*.txt` stamp population. |
| chousa / receipt bytes | `chousa-shokunin/tools/receipt-pin.py:54-67,89-92`: selected revision/header equality, canonical relative path, digest equality before `RECEIPT_PIN=PASS` | **Adjacent, C2:** binds a producer blob, but explicitly says at :10-12 that header consistency is not execution authenticity. No ancestry/null-arm equivalence claimed. |
| mori / registry population | `mori-shokunin/tools/mori-gate-registry.py:31-43,404-440`: enumerates declared tool population, rejects unregistered paths and absent real selftest branches | **Adjacent, C2:** same registry completeness/real-flag concern; tool universes and parser rules differ from R75, and this does not replace C1 corpus indexing. |
| mori / bound receipt inputs | `mori-shokunin/tools/mori-retention-reconcile.py:169-177,195-198,239`: resolved full revision, `measured_not_ancestor`, input equality, inner/wrapper revision agreement, `receipt_authenticity: unattested` | **Adjacent, C2:** shares ancestry checks while adding input/inner-result binding and expressly withholding authenticity; no claim of executing R75 instruments. |

The additional corpus-parity search used `readme.map|unindexed|orphan|UNINDEXED|missing.*index|index.*missing|knowledge.*glob|glob.*knowledge` over all six lanes' script/tool directories. It located kumitate's bimap and kotodama's cited-evidence orphan checker, not a demonstrated identical three-universe R75 gate. This is a bounded search result, not proof that other implementations do not exist.

## Explicit contradictions and limits

1. **Ancestry is not freshness or authenticity.** R75 `plans/round75_c2_registry_audit.py:133-155` checks stamp presence/resolution/ancestry; tabi additionally checks producer/input drift, kama checks intervening changes, and chousa/mori explicitly withhold authenticity. These contracts cannot be summarized as the same provenance guarantee.
2. **A crash kill is not an expected-ID kill.** Tabi explicitly counts a crash as a kill; R75's frozen claim requires the declared finding. Benign survival does not repair wrong-cause attribution.
3. **Freeze-green is not landing-green.** Kumitate's PLAN-time gate would reject precisely the red-before state R75 preregistered for repair. Reusing it unchanged would harm the experiment's contract rather than improve coverage.
4. **Index completeness is not historical retention.** Removing a corpus file and its row together can preserve current-set parity; kumitate's covered-set ratchet addresses an additional requirement. Do not silently attribute it to R75-C1.

## One bounded proposed move

**Route one evidence-qualified instrument crosswalk to protocol/integrator; keep the lane instruments unchanged.** The crosswalk should distinguish (a) live-set parity versus historical retention, (b) stamp ancestry versus producer/input binding versus replay, and (c) benign survival versus expected-ID attribution, using the located rows above. Include the explicit statement: “R75-C2 stamp success establishes resolvable ancestor provenance, not landing-tip reproducibility or execution authenticity.” This report supplies the scoped content; L1 alone decides whether to file the report-out.

- **Affected axes:** calibration improves by preventing substitution of weaker kill/provenance metrics; coverage improves in the overlap map by distinguishing the third evidence-directory universe from knowledge/lessons-only precedent. These are proposed explanatory gains, not measured axis deltas.
- **Runtime effect:** zero new execution, dependency, replay, or sibling gate invocation; do not copy another lane's runtime or require its availability.
- **Contract effect:** no amendment to frozen R75 targets, controls or kill rules; do not turn a routed standard into an additional R75 acceptance leg.
- **Substrate effect:** report-only crosswalk; no second fleet schema, receipt format migration, shared helper or retention registry is introduced.
- **Verification effect:** keep R75 counting commands as the only R75 predicate measurements; treat sibling source locations as overlap evidence, never as passing receipts.
- **Risks:** a report-out could be misread as a mandated fleet standard or global novelty claim; label it a scoped candidate taxonomy, preserve lane-owned universes and the non-equivalence statements. Ancestor-qualified receipts must not be relabeled “at landing tip” without separate evidence.
- **No-harm status:** [INFERENCE] a report-only clarification introduces no runtime or predicate regression; no empirical no-harm result is claimed.

## Route out, do not absorb

Fleet-wide index universes/row grammar, a common receipt-carrier protocol, fleet replay/authenticity requirements, and a common mutation outcome taxonomy belong to protocol/integrator coordination. Kengaku can describe and evidence those distinctions, not impose a sibling gate, promote a fleet standard, or own sibling implementations. Domain payloads remain with their lanes (browser evidence, language packets, model-serving evidence, research receipts, host retention).

## Verification and handoff

Performed: full frozen-claims read, six-lane production search, targeted source greps and range reads. Observed evidence consists of the printed source lines cited above. No gate, selftest, mutation battery or counting command was executed; consequently this seat reports no reproduced R75 pass/fail or sibling runtime result.

For L1's existing verification phase only, retain the frozen commands:

- `python3 plans/round75_c1_index_parity.py --lane .` — require the three frozen universe lines, `PREDICATE R75-C1 pass`, rc 0 and the required clean revision stamp.
- `python3 plans/round75_c2_registry_audit.py --lane . --mutants --check-stamps corpus/evidence/round75` — require the frozen mismatch/defect/mutant/stamp lines and rc 0.
- Retain both frozen selftests and controls; this proposal adds no runtime check.

No scratch directory or fixture was created; none remains to delete. No installs, git mutations, sibling edits or production edits were performed. Only this authorized report was written.
