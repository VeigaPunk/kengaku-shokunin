# CredentialSentinelR73 — bounded security scan

Axes: coverage, calibration. Read-only review; no instrument, registry, predicate, target, or claim edits. No installation. Evidence: `corpus/evidence/round73/w1/sentinel-scan.txt` contains exact scanner/grep commands, exits, excerpts, path references, and reproductions.

## Credential verdict

`SCAN files=27 skipped=0 hits=0`, rc **0**, stderr empty.

**RISK none** — no credential/push-protection risk detected in that snapshot. **POSSIBLE secrets: none detected.** This is local pattern scanning, not a GitHub push-protection acceptance guarantee. The scan precedes this receipt/report; concurrent arrivals and the eventual landing tip are not certified.

Location aliases: A = `.ufo/waves/round-73/w1-spec.json:80`; B = `.ufo/waves/round-73/w1-dispatch.json:283`.

| Literal shape | Matching lines | Locations only |
|---|---:|---|
| `Bearer ` | 2 | A, B |
| `ghp_` | 2 | A, B |
| `github_pat_` | 2 | A, B |
| `hf_` | 4 | A, B; corpus/evidence/round73/w1/c1-widen-verify.txt:269,271 |
| `AKIA` | 2 | A, B |
| `sk-` | 4 | A, B; corpus/evidence/round73/census-before.txt:20; corpus/evidence/round73/w1/c1-widen-verify.txt:175 |
| `-----BEGIN ` | 2 | A, B |
| `op://` | 2 | A, B |
| `password=` | 2 | A, B |

All nine literal greps exited 0 with empty stderr. A/B contain the requested pattern list; the remaining hits are instrument/knowledge filenames or an upstream pathname, not secrets. Matched credential values are never reproduced.

## Write-scope findings

### Medium — caller-owned work directory recursively deleted

**Evidence:** `plans/round73_c2_registry_audit.py` selftest and mutants resolve the caller-supplied existing `--work` directory and use `shutil.rmtree(work, ignore_errors=True)` on normal completion. Only the existence/type check precedes fixture creation.

**Failure path:** a caller supplies a non-disposable existing directory, including one containing unrelated files. The command deletes that entire directory rather than only its own fixtures. No malicious input is necessary.

**Safe reproduction:** in this seat's scratch only, placed a pre-existing canary in each of two work directories, then executed:

```sh
python3 plans/round73_c2_registry_audit.py --mutants --work /fast/scratch/hyaku/kengaku-r73/CredentialSentinelR73/mut
python3 plans/round73_c2_registry_audit.py --selftest --work /fast/scratch/hyaku/kengaku-r73/CredentialSentinelR73/st
```

Both returned 0: `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=1`; `SELFTEST arms=4 red=3 ok=True`. Both work directories and their unrelated canaries were gone afterward; listings reported “No such file or directory.”

**Impact:** accidental data loss outside the instrument-created fixture set, bounded by caller permissions.

**Smallest remediation:** allocate an owned child under `--work` and remove only that child. Until changed, pass only a new disposable directory. Remediation is outside this seat's write scope and was not applied.

### Outside-root references, classified

- Dispatch/spec reference `/home/vgpnk/.omp/agent/RULES.md` (authorized operator rules), sibling-lane discovery, `/tmp` policy, and `/proc` inspection instructions. These are recorded data/instructions, not proof of an executed sensitive read.
- `corpus/evidence/round73/w1/lesson-draft.md:40` cites the authorized fleet census script/root.
- `corpus/evidence/round73/w1/c1-row-audit.md:13,14,16` describes historical sandbox `/tmp` and home-directory lock writes. That report also explicitly identifies host writes at :22; this seat did not run those historical batteries.
- Interpreter shebang references are not credential access. The path extractor's `/opt` matches in fetched HTML are closing `option` tags, not paths.
- No `/proc`, credential-store, or session-state read found in the two specified instrument sources. This does not assert all historical registered instruments are side-effect-free.

A limited read-only `/tmp` name survey found five pre-existing kengaku-related paths, listed in the receipt. They were not created by this seat, and attribution to R73 is unestablished. They remain untouched because cleanup authority is restricted to this seat's own tree.

## Calibration cautions, not a claim ruling

An earlier moving-tree audit printed `INSTRUMENTS total=114 derived=registry rows=114`, `MISMATCH 0`, rc 0. A later gate snapshot printed `ADVERTISED total=113`, `REGISTERED total=113 rows=115`, `MISSING 0`, rc 0. These are **different times**, not evidence of a same-snapshot parser disagreement. Both counts differ from the frozen exact target lines (106 audit / 112 advertised). L1 must evaluate canonical landing-tip targets; a printed predicate pass line alone does not establish them. No predicates were changed.

The lane-arm before/after sorted git-status comparison was unchanged. This establishes only unchanged status, not bytewise zero mutation; no stronger claim is made.

Other exercised check: `python3 plans/stage_scan.py --selftest` → `SELFTEST cases=33 failures=0`, rc 0. No remote secret validation, credential-store reads, process-environment reads, or offensive automation performed.

## Handoff and cleanup

Only this report, the assigned evidence receipt, and this seat's scratch were written. The seat scratch is removed at exit. Main should rescan the settled staging set, including final reports, because this was a concurrent-wave snapshot rather than landing certification.

Self-evaluation: accuracy 4 (bounded local evidence, no remote push check); completeness 4 (all assigned patterns and sources scanned, moving-tree limitation explicit); clarity 4 (classified references, snapshot aliases); actionability 4 (one concrete cleanup fix; remediation not authorized); conciseness 4 (extra calibration observations retained as cautions). Overall 4.0. Highest-impact improvement belongs to main: repeat the scan after all wave outputs settle.
