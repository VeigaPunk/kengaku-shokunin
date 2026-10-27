# Round 45 — the advertised fixture fence closed; an eleventh TB2 grader executed (2026-10-26, hyaku run 9)

L1 `KengakuR45` (planner seat; attempt 2 — attempt 1 died on an invalid_prompt policy refusal with no wave,
report or commit, `.ufo/watchdog.log` 22:48). Frozen claims `plans/round-45-claims.md` (freeze `b4fcd35` +
pre-data amendments `9271dda4`); baseline lane tip `9d5f971` (the round-44 non-author spot-check). Wave 1
(build/package, 39 seats) + wave 2 (falsify, 39 seats). Written by the L1 at integration from the seat
reports named in each row.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **A receipt committed with envelope framing around the instrument's bytes** — the L1's first recorded probe run captured the whole `envelope.sh` transcript into `corpus/evidence/round45/password-recovery-probe.txt`; the gate's `c_rerun` (`P10`) requires `r.stdout == want`, and three `ENVELOPE ` lines make the file fail byte-equality even though every verdict inside is right. | `.ufo/waves/round-45/w1/R45ProbeFirst.md` §5 (5243 B vs the probe's 4659 B); gate output `P10 DEFECT fresh probe output is not byte-equal to the receipt` | none at freeze — the receipt was copied straight from the harness transcript | reframed at `7d062c0`: the receipt is bare probe stdout (`cf74f451`, 4659 B); the wrapper transcript moved to `corpus/evidence/round45/probe-run-envelope.txt` and is committed *after* the receipt (the `order_check.py` `CASE_LINE` pattern makes a pre-receipt transcript proof of a pre-freeze run — verified both directions by `R45ProbeFirst` on throwaway fixtures). Rule: **a receipt file is the instrument's stdout only; envelope framing is separate evidence.** |
| **A spec whose row `capture` fields disagree with its own capture manifest** — `pkg-spec-r45.json` rows named flat basenames (`test_outputs.py`, `setup.sh`, …) while `SHA256SUMS` and the counter's `CAPTURES` dict used the upstream directory layout (`tests/test_outputs.py`, `environment/setup.sh`, …). Five rows were "not pinned in the manifest" and twelve `## Located quotes` rows cited files that did not exist under the named convention. | `R45ProbeFirst.md` §5b/§5c; gate output `P5 DEFECT manifest_entries=9 bad=10`, `P4 checked=19 bad=12` | nothing: the draft froze with the split convention (the probe read nested, the spec rows were flat) | the capture tree was flattened to the r44 convention (all 9 digests unchanged — same bytes, flat names) and the probe's reads re-pointed; the receipt it prints is byte-identical on re-run (`9363e03e` → still `cf74f451`-content). Rule: **one capture convention per freeze, checked by running the gate once before the freeze commit.** |
| **A defect class that survives "the tool returned the right verdict"** — the round-44 fence's four routed defects were all of the form *the fence refuses correctly but opens/blocks on a path outside d while deciding* (commondir, config.worktree include, refuse-to-describe, parent-process include read). A counter that only records admit/refuse reads every one of them as a pass. | `corpus/lessons/round-44.md` (routed `R44SentinelFences` V1–V3, `R44LabratLaneInclude`); `plans/round-45-claims.md` §C1 | `control-c1-fence-r44.txt` — the r44 counter's own fence as the fence → `REFUSALS total=10 clean=3 leaked=3 read=4`, `contradicted=7` | the round-45 counter runs the fence under `strace -f -y` inside bwrap and counts `LEAKED` (admits), `READ` (refuses but opens outside) and `HUNG` separately — the observed fence, not the asserted one. Rule: **a refusal verdict that required an outside read is a defect, and the counter must see the read.** |
| **A quote that is verbatim but below the word floor** — four `## Mechanism` rows quoted single tokens (`read_text().strip().split("\n")`, `recovered_pass_path.exists()`); the counter's `len(q.split()) < 2` rule rejects them even though they are byte-exact on the cited line. The seat's diagnosis reported them as "not on the line" because the token floor and the substring check report together. | counter run `V10 DEFECT … constant-crlf / dir-state / crlf-line / under-varsea quote not on the line`; `R45ProbeFirst` follow-up | the counter run itself (mechanism rows are checked at every counter run) | multi-word verbatim quotes on the same decisive lines (`guesses = Path("…").read_text()`, `assert recovered_pass_path.exists(), "Recovery file not found"`). Rule: **cite the line's decisive clause wide enough to clear the word floor — the decision line, not the minimal token.** |
| **A frozen-file digest list that drifted behind the freeze it pins** — `frozen-digests.txt` listed the pre-amendment probe/spec/counter/SHA256SUMS digests while the tree had already been corrected, and held a duplicated counter line. | `R45ProbeFirst` follow-up (the digest table + the note that V5's self-reference needed a claims-file line); `.ufo/waves/round-45/claims/frozen-digests.txt` diff | the seat's bookkeeping audit | regenerated in one shot after the amendment commit; the claims file now carries a "Freeze amendments" paragraph that names each pre-data correction and the re-pin, so the digest list is a statement of the amended freeze, not a silent rewrite. |
| **A gate hygiene clause that races the measurement it protects** — `P9` (`untracked=`) counts seat artefacts landing mid-run, so a back-to-back counter run can fail on files another seat just wrote. Two successive runs on the same tree measured `untracked=2` then `untracked=14`. | `.ufo/waves/round-45/integrate/measure-final.txt` (clean clone: `P9 ok untracked=0`); the live-lane A/B receipts (`corpus/evidence/round45/counter-a-run.txt`, `counter-b-run.txt`, byte-equal) | the counter's own `--require-clean-tree` rerun | run the measured clone: the tip-clone re-measure under the envelope is the conformance evidence; live-lane runs are bookkeeping. A seat that races the counter is *not* a counter defect — the measurement discipline is. |

## Gate

Opened or captured this round. Access date 2026-10-26 for every row; times are -03. The L1 re-fetched all nine
files of the task directory at ~23:05 -03 (`corpus/evidence/round45/tb2-password-recovery/` + `SHA256SUMS`,
`cmp`-identical to the attempt-1 draft). Base URL
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/`.

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `tests/test_outputs.py` (S149) | admit | the executed scoring predicate: exists() + line-membership of one constant; flips to reject if a re-fetch changes its digest |
| `instruction.md` (S150) | admit | the request the map is against; flips on digest change |
| `environment/setup.sh` (S151) | admit | plants the fragments at 1MB/3MB; flips on digest change |
| `environment/Dockerfile` (S152) | admit | installs the forensic toolset, runs the seed; flips on digest change |
| `tests/test.sh` (S153) | admit | reward = pytest exit status; flips on digest change |
| `README.md` (S154) | admit | authors' check description matches the mechanism; flips on digest change |
| `solution/solve.sh` (S155) | admit | the oracle the `oracle-solve-sh` case executes; flips on digest change |
| `task.toml` (S156) | admit | 900 s timeouts, `allow_internet = true`; flips on digest change |
| `gitignore` capture | reject (as row) | the task's dotfile; captured for byte-complete refetch checks, not a row — no claim rests on it |
| `environment/varsea-…dat` seeds | reject | runtime-generated image bytes; the probe recreates them from `setup.sh`, and `/dev/urandom` differs run to run — a capture would record noise, not a fact |

## What was demonstrated

- **Calibration:** `plans/fixture_fence.py` (wave variant A) — `PINS total=33 mismatched=0`,
  `REFUSALS total=10 clean=10`, `HONEST fixtures=104 admitted=104`, `CALIBRATION advertised=10 contradicted=0`,
  `PREDICATE C1 pass` on the landing tip and on a clean clone (`integrate/measure-final.txt`).
- **Coverage:** TB2 `password-recovery` @ `2fd12b88` admitted (S149–S156, tier A); probe `cases=16
  observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0`; `checks=11 defects=0`,
  `PREDICATE C2 pass`; V11 `states=48 grader_pass=18 grader_fail=30 disagree=0`.
- The routed round-44 defects V1–V3 + `R44LabratLaneInclude` are now refusal classes f7–f10 inside the frozen
  counter — the routed-defect loop closed.
