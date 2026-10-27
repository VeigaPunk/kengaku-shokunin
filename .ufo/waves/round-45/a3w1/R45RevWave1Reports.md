# R45RevWave1Reports — wave-1 report cross-check

Measured lane tip: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD`). Scope: all 39 names in `w1-spec.json` against `w1/*.md`.

## Verdict/report coverage

- **Reportless: 2.** The spec/file-name comparison returned `spec-only: []`, `file-only: []`, `match: 39`; however `R45CriticC2Instrument.md` is a recovered JSON result, not a report with a `VERDICT:` line, and `R45MutV11States.md` is an incomplete `<think>` fragment with no verdict. Command: `grep -n '^VERDICT:' *.md`; output showed no line for either file. Thus all 39 seats have a path, but only 37 completed verdict reports.
- **Verdict overshoots: 0.** Spot-checked more than ten concrete numeric/verdict claims against their cited material or reruns below. I found two narrow factual inaccuracies (not verdict-changing): `R45ProbeFirst.md:322-326` says the listed mechanism quotes are not substrings of their cited lines, but the source at `corpus/evidence/round45/tb2-password-recovery/test_outputs.py:14` contains `read_text().strip().split("\\n")`; likewise line 10 contains `recovered_pass_path.exists()`. Those rows still fail the quoted minimum-two-word condition, so the headline `probe-first-cases-16-mismatches-0` is not contradicted. `R45RevengerOrder.md:207-216` repeats the owner candidate digest `3b540e0d…` as the landed fence, whereas its own `R45ExecControls.md:167` says the landed fence digest is `ac65c032…`. Its `order-origin…behaviour-lost-no` conclusion is bounded to the measured fixture classes and not refuted by this attribution error.
- **Lane-write claims: none found.** Search: `grep -inE '(I|we|this seat) (wrote|edited|patched|modified|committed|added|landed|installed).{0,60}(lane|corpus/|plans/|SCORECARD|LOG\\.md|README|PROVINCE)' *.md`; no positive seat-write admission. Apparent hits were explicit no-write statements or L1/integration observations. `git log --format='%h %an %s' -12` showed the relevant round-45 commits authored by `kengaku-shokunin`, not individual wave seats; this is corroboration, not proof about uncommitted writes.

## Spot-checks (commands and outputs)

1. `git -C ... rev-parse HEAD` → `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc`.
2. Spec/report set comparison → `spec-only: []`, `file-only: []`, `match: 39`.
3. `sha256sum plans/refusals45/f{1_gitfile,2_deep,3_abbrev,4_fifo,5_alternates,6_above}.py` → hashes respectively `bac0df8a…`, `027972c6…`, `05a43c05…`, `6ba6a730…`, `8d56f2f7…`, `e9a599e4…`, matching `R45RevHostiles.md:44-49`; `cmp -s` against round-44 originals returned `identical` for all six.
4. `ls plans/refusals45/ | wc -l` → `10`; battery Python-file counts → `battery42: 5`, `battery43: 7`, `battery44: 10`, confirming the stated 10 refusal modules and the 33-input composition in `R45SonicPinCheck.md:77-90`.
5. `python3 -c` over `corpus/routed-findings.jsonl` → `total rows 60 open+blocked 24`, supporting `R45DistillRouted.md`'s 24 open/blocked rows (its grouping is an analysis, not a counter predicate).
6. `grep -nE 'xo1|xo3|x13' plans/round45_c1_verify.py` → no matches, exit 1, confirming `R45DistillRouted.md:73`'s no-counter-leg observation.
7. `sha256sum -c SHA256SUMS` in `corpus/evidence/round45/tb2-password-recovery/` → all nine capture entries `OK`, supporting `R45SonicPinCheck.md:92-105` and the refetch claim. `sha256sum README.md` → `122bf15e…`, matching both SHA256SUMS and `R45ScoutRefetch.md:9`.
8. `wc -c corpus/evidence/round45/password-recovery-probe.txt` → `4659`; `grep -c ENVELOPE ...` → `0`; receipt ends `regrade cases=16 differ=0` and `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, consistent with `R45ProbeFirst.md:313-315`.
9. `sha256sum R45ExecStageCheck/dry.out .../stage.payload .../dry.payload` → `f1076990…`, `2b4e1594…`, `46036abe…`, matching `R45ExecStageCheck.md:222-225`.
10. `grep -E '^(nop|under-varsea) ' corpus/evidence/round45/password-recovery-dry-cases-freeze.txt` → `nop … tests=F-` and `under-varsea … tests=F-`, supporting the two `F-` dry predictions compared by `R45PytestParity.md:26,41`.
11. `grep -n 'filler\|contradicted' .ufo/waves/round-45/claims/control-c1-fence-r44.txt` → `CALIBRATION advertised=10 contradicted=7`, supporting `R45LabratControls.md:131-135` and the control description in `R45ExecControls.md:180`.
12. `sha256sum plans/pkg_gate.py` → `ea638822…`, matching `R45SonicPinCheck.md:72-74`.
13. `git show 52d7486 -- plans/round-45-claims.md` → one cell changes S149–S157 to S149–S156, matching the historical change reported in `R45Lesson.md:47-52` and `R45CriticSeparability.md:84-93`; the current worktree digest is later and differs, so those reports describe their historical measurement, not current state.
14. `grep -n considerthese plans/round-45-claims.md` → no hits (exit 1); `grep -n considerthese plans/round-44-claims.md` → at line 122, supporting `R45Considerthese.md:85-87`.
15. `wc -l corpus/routed-findings.jsonl` → `60`; independent JSON count also gives 24 open/blocked, supporting `R45Considerthese.md:27`'s reported ledger scale.

## Residual risk and gaps

This is a bounded cross-read, not a re-execution of expensive fixture suites or external network fetches. The reports’ own receipts remain the evidence for those runs. Two seats have no completed report/verdict despite recovered output fragments; the two narrow inaccuracies above should not be treated as predicate-changing without further evidence. No lane file was changed by this reviewer. Scratch cleanup command: `python3 .../plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r45 R45RevWave1Reports /fast/scratch/hyaku/kengaku-r45/R45RevWave1Reports` → `DELETE ... bytes=686850992 size=655.0MiB`.

VERDICT: w1-verdict-overshoots-0-reportless-2