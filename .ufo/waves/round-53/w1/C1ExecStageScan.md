# C1ExecStageScan — round 53 wave 1 (executor)

Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ExecStageScan/stage_scan.py`
(the L1 installs it as `plans/stage_scan.py`; usage `python3 plans/stage_scan.py PATH...`). Nothing outside the seat dir was written.

## Behaviour
- Exit 0 no hit; 1 any `HIT <path>:<line> <rule> prefix=<4 chars>` (matched bytes never printed; one line per rule per line); 2 setup error (no args, missing path, unreadable file/dir — a scan that could not read never says 0).
- `SKIP <path> binary|size|symlink` (NUL in first 8 KiB; > 5 MiB; symlinks not followed). `.git` directories are not entered. Ends with `SCAN files= skipped= hits=`.
- 11 rules: github-pat (ghp/gho/ghu/ghs/ghr), github-finepat, huggingface (hf_ + >=30), sk-key (sk-/sk-ant-, not in-word), aws-key-id, aws-secret (40-char after aws…secret), slack, google-api, private-key, generic, op-ref. Regexes are documented in the docstring.
- Deviation to flag: `generic` is the spec regex widened with `[\w-]*['"]?` between the keyword and the separator so `api_key = "…"` and `"token": "…"` hit. This is the source of all false positives below.
- `--selftest [--tmp DIR]`: 33 cases (14 rule positives, 7 near-miss negatives incl. 10-char hf_, in-word sk-, 15-char and over-long AKIA runs, 40-char value without an aws name, public-key header, short generic value; binary; >5 MiB; nested dir with exact line number; .git skipped; symlink; multi-rule lines; multi-path; missing path; no args; unreadable; self-scan). Fixtures built from fragments; secrets never appear in captured stdout/stderr (asserted).

## Commands and numbers
- `python3 stage_scan.py stage_scan.py` → `SCAN files=1 skipped=0 hits=0`, exit 0 (own file clean).
- `python3 stage_scan.py --selftest --tmp /fast/scratch/hyaku/kengaku-r53/C1ExecStageScan` → `SELFTEST cases=33 failures=0`, exit 0 (`selftest.txt`).
- Mutation check (scratch copies): hf `{30,}`→`{5,}` fails `neg-hf-10char`; dropping the sk- lookbehind fails `neg-sk-inside-word`; dropping the AKIA trailing lookahead fails `neg-aws-run-too-long` (this one initially survived; the case was added).
- Scans, run from the lane root (outputs in the seat dir `scan-*.txt`):
  - `corpus/evidence/round52` → files=188 hits=0, exit 0
  - `corpus/evidence/round53` → files=2 hits=0, exit 0
  - `.ufo/waves/round-52` → files=987 hits=7, exit 1 (skipped=0)

## The 7 hits (all generic-rule false positives; I viewed each line, none is a credential)
| location | why it matched |
|---|---|
| `w1/C1ScoutTaskShapes/shapes.json:4` | JSON key `tree_api` with a github API URL value |
| `w2/W2CritRoundHonesty/receipts/lacuna-secondary-summary.html:117` | JS `API="/api/v1/reading-list"…` |
| `w2/W2ExecEntryDraft/build.py:31` and `candidate-audit.json:801` | task name `password-recovery` as a key / `test_password_match:` prose; the quoted value is a benchmark's expected-answer string, not matched by any provider rule |
| `w2/W2ExecEntryDraft/build.py:40` | task name `vulnerable-secret` as a dict key |
| `w2/W2RevClassifierImpl/receipts/fixtures.py:26,29` | task name `password-recovery` as a dict key |
No provider-specific rule (GitHub, HF, sk-, AWS, Slack, Google, PEM, op-ref) fired anywhere. The pushed-and-blocked round-52 fixture is therefore not in these trees.

## Risks
- `generic` is deliberately loose; expect false positives on task names containing password/secret/token and URL-valued keys. There is no allow-list; the cure is to review the HIT line (only path:line + 4-char prefix is shown). Not adding one was a scope choice.
- Not run as a git hook; wiring it into staging is L1's call.

Tools installed: none. No tool anomalies. Scratch dir removed.
