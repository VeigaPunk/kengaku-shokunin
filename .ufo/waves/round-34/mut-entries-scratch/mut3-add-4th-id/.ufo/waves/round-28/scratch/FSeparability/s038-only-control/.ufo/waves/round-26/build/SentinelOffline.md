# Sentinel Offline

Axes: **calibration**, **novelty**.

## C1 raw-field privacy scan
Pattern-scanned only the `raw` strings in the four committed JSONL files. Credential markers include common token/API-key/password/header forms, JWT/private-key markers; host checks cover local/private URL authorities, private IPv4 addresses, and common home/user paths. No raw text or matched values were emitted.

| File | records / raw records | credential-like | private URL | host-secret | matching record IDs |
|---|---:|---:|---:|---:|---|
| `corpus/evidence/round8-horizon/results.jsonl` | 268 / 258 | 0 | 0 | 0 | none |
| `corpus/evidence/round9-replication/results-r9.jsonl` | 284 / 276 | 0 | 0 | 0 | none |
| `corpus/evidence/round11-power/results-r11.jsonl` | 1473 / 1408 | 0 | 0 | 0 | none |
| `corpus/evidence/round12-ladder/results-r12.jsonl` | 4114 / 4000 | 0 | 0 | 0 | none |

Pattern scan is not a proof against unknown/obfuscated secret formats; no record IDs matched the checked patterns.

## Code and interface review
- `grader.py:52-63` imports only stdlib modules; no network client/API is imported. `grader.py:121-134` extracts with regex/`json.loads` (no `eval`). Main execution is guarded at `5730-5737`; importing its grader functions does not invoke the CLI. The apparent file-write at `4255-4265` is source text in `SYNTH_PROBE_SRC`, not module-executed code.
- `grader.py:5537-5542` uses `subprocess.run` only inside selftest, with an argv list and default `shell=False`. Selftest writes copies/mutations under `tempfile.mkdtemp` and removes that directory (`5526-5534`, `5652-5654`). This is not hard-pinned to `/tmp`: a caller-controlled `TMPDIR`/temp configuration can redirect writes elsewhere.
- `plans/grader_perturb.py` and `plans/gate_timing_check.py` are absent from the current `plans/` listing; their code-level behavior cannot yet be verified. Pre-registration constrains the perturb instrument to stdlib/offline and grader imports (`plans/round-26-claims.md:75-79`), but does not specify a temp-directory policy for selftests. `attrib_calibration.py:143-152` implements `clopper_pearson` as pure math; importing it does not execute its CLI.
- Current `plans/state_check.py` is still v2; P3/v3 is only specified at `plans/round-26-claims.md:126-147`. It has no `shell=True`: `normalize_command` tokenizes then exact-matches the allowlist (`state_check.py:170-180,292-297`), and `subprocess.run` receives argv (`320-329`). The `freeze-check` allowlisted branch only calls `verify_frozen` (`attrib_probe.py:1157-1159`), which reads/verifies the frozen file (`153-193`); although that module imports subprocess/HTTPConnection (`41-45`), this branch does not use them.

### Finding — MEDIUM: `--root` subprocess trust boundary
Exploit path: a caller supplies an untrusted `--root` containing a SCORECARD row with an allowlisted command; `CommandRunner` executes `python3 grader.py` or `python3 plans/attrib_probe.py` from that root. The `--root` argument accepts caller-selected directories (`state_check.py:1306-1325`), commands are run with `cwd=self.root` (`320-328`), and the full parent environment is inherited (`329`). No shell is involved, but repository-controlled Python can access inherited host environment/secrets, network, and arbitrary filesystem writes. This is a risk for untrusted roots, not evidence that the committed lane scripts do so.
Smallest remediation: for v3, avoid running scripts from `--root` (or execute a trusted, digest-pinned checker outside that tree); pass a minimal environment. Keep freeze verification read-only.

### Finding — LOW: selftest temp location is environment-selectable
`state_check.py:1155-1173` and `grader.py:5526-5534` create/write temp trees through `tempfile`; those APIs honor temp-directory environment overrides. Cleanup exists, but writes are not guaranteed to stay under `/tmp`. Pin selftest temp roots with `dir="/tmp"` (or equivalent) to meet the lane scratch boundary.

## Q13 Git boundary
Pre-registration says the check reads lesson content as of a commit (`plans/round-26-claims.md:20-24`); no gate checker implementation is present to audit. The behavior can be restricted to read-only plumbing: `git cat-file blob <commit>:<lesson>` for the lesson and `git cat-file -e <commit>:<report>` (or `git ls-tree -r --name-only <commit>`) for cited report existence. Use fixed argv with `shell=False`, reject absolute/`..` paths, and do not checkout, fetch, update refs, or alter the worktree/index. No Git mutation is required.

VERDICT: No credential-like, private-URL, or host-path matches in the scanned raw fields; grader imports and planned interfaces are offline by contract, but untrusted `--root` execution and environment-selectable selftest temp paths need the stated bounds; Q13 can use read-only Git plumbing. No tools installed.