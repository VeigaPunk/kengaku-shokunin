# C1RowAuditR73 — reviewer report

Axes: coverage, calibration. Recommendation only, not admission, integration or a native verdict. Writer: C1RowAuditR73 (reviewer), distinct from knowledge writer KnowledgeEntryR73. No predicates, scripts, registry rows or claims were edited. No tool installed; python3 was the sole execution runtime. LSP device unavailable (`read xd://lsp`: No such tool); literal source review substituted, not semantic-reference proof.

## Findings by severity

1. **High — dead live registry entry.** `SKILL.md:702` points r69-C1 at absent `corpus/evidence/round69/nginx/receipt.txt`. Exact entry check returned rc 2, `SETUP receipt-missing .../receipt.txt`, stderr empty. Existing receipt-v2.txt yields rc 1 for the legitimate frozen coverage miss (seen_f=6/8). Independently derived row and sibling draft both choose v2. A structural green is not runnable-entry evidence.
2. **Medium — dishonest live write boundaries.** `SKILL.md:701,702,704` advertise battery modes but describe writes as scratch-under-work. Sources write external optional receipt/evidence paths and home lock files: tensor :222–250; nginx69 :267–270,408–484; nginx70 :352–355,501–578. Nginx batteries also start shared-loopback 8080 services. Draft fixes filesystem disclosure; add loopback effects if the scope cell covers non-filesystem effects.
3. **Medium — live r32 rows omit exit 2.** `SKILL.md:699–700` list 0/1 only, despite argparse CLIs. Draft adds usage→could-not-evaluate, but its r32-C1/r66-C1/r69-C2 cells ambiguously classify rc1 exceptions as both failed and could-not-evaluate. Fleet outer rc1 class must be failed; keep exception caveats separate.
4. **Medium — selftest spelling does not prove strict PROTOCOL conformance.** PROTOCOL.md:385–389 requires self-invocation with exit and stable finding-id assertions. r32 verifier :149–164 and defects :207–240 call helper checks and count arbitrary exceptions as red. Tensor :334–369 uses booleans; nginx69 :629–638 and nginx70 :776–786 accept any refusal reason. Real isolated flags exist, but blanket Gate-standard conformance would overclaim.
5. **Coverage residual — regex excludes existing advertised evidence instruments.** `round52_c2_registry.py:36` excludes hyphenated directories: SCORECARD.md:74 advertises `corpus/evidence/round9-fleet/test_harness.py`; SKILL.md:592 advertises `corpus/evidence/round13-coverage/coverage_census.py`. Both exist and are absent from ADVERTISED. Two other broad matches, SKILL.md:599 `plans/fixtures/r29/mutation_witness.py` and LOG.md:521 `plans/fixtures/r28/acceptance.py`, are deliberate fixture-depth exclusions, not necessarily independent instruments.
6. **Low — r32-defects pin cell overclaims its input.** SKILL.md:700 says every R check re-reads gate-cli-exits.txt; only R3 does (script :101–113). Draft's explicit report/lesson/literal inventory is accurate.

## Required deliverable and draft comparison

Full independent eight-field table, source anchors, draft disagreements, sweep and exact command/stdout/stderr/rc receipts: `corpus/evidence/round73/w1/c1-row-audit.md`. Derivation was persisted before opening `c1-rows-draft.md`. Draft initially absent, subsequently located and compared. Seven entry argv/kinds/selftests/owners/pin sources agree substantively. Naming difference only: my round32-c1 vs draft round32-c1-verify. Draft rc1 ambiguity and loopback omission are listed above; eighth audit row is outside my seven-script certification.

SWEEP command_forms=596 distinct_script_spellings=128 existing_lane_scripts=117 gate_ADVERTISED=113 existing_not_advertised=4 (two hyphenated instruments, two explicitly excluded fixture helpers).

Three uv-wrapped python3 forms are recognized, not gaps. Two python -m forms are pip-install examples (plans/round-63-claims.md:34; round-68-claims.md:64), not existing lane script entries. No existing extra-dot lane script was found in the broad python3 extraction. README document-relative coverage-census spelling duplicates the same instrument.

## Executed verification and limits

Seven --help commands: rc0, stderr empty. Six authorized selftests: rc0; exact outputs in evidence. r69-C2 selftest not executed because it internally git-adds/commits, forbidden here. Full tensor/nginx live batteries were not executed to avoid out-of-scope home locks and service effects; check-receipt mode was executed instead.

Entry/check rc in seven-script order: 1,1,0,1,1,0,0. Reds: r32-C1 S094 has no URL; r32-defects historic report lacks current master; r69-C1 only six failure-covered legs; r69-C2 E7 depth receipt differs. These are not silently turned green. Separate exact live r69 bad entry rc2 is recorded.

Coverage command `python3 <lane>/plans/round52_c2_registry.py --lane <lane>` returned rc0 and ADVERTISED113, REGISTERED113 rows115, MISSING0, INCOMPLETE0, ENTRY-MISSING0, SELFTEST-UNBACKED0, DUPLICATE0, R73-C1 pass. This is a moving-worktree sample, not a claimed landing commit and not the assignment's exact target112. The gate source changed concurrently: original read required plans_only>=1; reread :133–161 explicitly uses Amendment A1 plans_seen>=1. I changed no rule and do not regard an amended passing token as evidence under an unchanged frozen contract. No C2 execution or A2 approval is claimed.

Residual risk: legacy pins often identify mutable inputs without full digest snapshots; FROZEN in round32_defects.py:204 derives directly from CHECKS and is not an independent oracle. No runtime-routing/resume implementation is changed by this assigned diff; same-identity and resume_continuity_v1 checks are not applicable to these rows. Saturation is only regex-universe saturation, not every Python instrument or behavioral declaration truth.

## Additional knowledge reread requested by L1

Candidate: `corpus/knowledge/instrument-registry-derivation.md`; proposed text read from `corpus/evidence/round73/w1/knowledge-draft.md:1–64`. Independent captured-source reread: `corpus/evidence/round73/sources/ast-docs.html:2680` literally says “Parse the source into an AST node.” Seven whitespace-delimited words, exact quote and location confirmed. Warning :2708–2715 explicitly denies that successful parsing guarantees executable Python and says ast.parse does not perform scoping checks. The draft correctly limits AST evidence to syntax rather than behavior. S249 is now present at corpus/SOURCES.md:265; draft :1,7,60 still describes it as pending/planned and should be updated as editorial state, not treated as missing source evidence.

**Final knowledge recommendation: HOLD for full-entry admission on this report alone.** The seven-word quote and warning receive positive independent support, but Q10 requires every cited quote/location and number to be reread. This seat did not reopen the additional PyCF_ONLY_AST/ast.walk passages or every round72/round73 historical numeric receipt the draft cites. Q13/Q14 can cite this named reviewer report as partial source support (writer differs), not a complete reread or automatic admission. A complete independent reread resolving these gaps may support admission; frozen denominator failures must remain disclosed, not repriced by assuming A2 admissible.

## Cleanup and self-evaluation

All fixtures were inside `/fast/scratch/hyaku/kengaku-r73/C1RowAuditR73`; explicit cleanup completed, observed `scratch_removed=True`. TMPDIR was set to that directory, PYTHONDONTWRITEBYTECODE=1; no /tmp fixture or PATH edit was made. No git mutation was invoked; the two read-only diff commands inspected actual registry changes against current state/base.

Self-evaluation: accuracy4 (moving worktree limits revision attribution); completeness4 (seven rows and sweep complete; additional knowledge reread is partial and held); clarity4 (full receipts intentionally separated into evidence); actionability4 (exact bad argv, corrected existing receipt and source anchors supplied); conciseness4 (broad audit requires a longer evidence table). No unrun check is reported passed.
