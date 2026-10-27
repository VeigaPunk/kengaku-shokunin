# R44PlanNext — round-45 data walk: `round_close.py` survivors under the round-44 counter contract + next TB2 coverage task (scout, wave 1)

Seat `R44PlanNext` (leaf, read-only on the lane; nothing frozen touched). Lane clone `$S/lane` at `5e3d3aa06c6b7000929ac3e62563a39159c4501f`
(`git -C $S/lane rev-parse --show-toplevel` = `$S/lane`), `$S=/fast/scratch/hyaku/kengaku-r44/R44PlanNext`. `plans/round_close.py` sha256
`cd581f8a263372b164f5a4fdf20e25eefaa22d2087097de75e463c19043a8144` (unchanged since `ff14d76`, the pin R43PlanNext measured); `plans/order_check.py`
`948d5e1d…`, `plans/anchor_digest_check.py` `11bb2cad…` equal the counter PINS. Every run below went through
`claims/envelope.sh "$S/env" <cmd>`; `local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` at every boundary. Scripts and
outputs in `.ufo/waves/round-44/wave/R44PlanNext/` (all < 11 KB, `SHA256SUMS.txt`).

| run | start→end | exit |
|---|---|---|
| `c1_rc.py` (17 mutants + 4 controls, 11 fixtures) → `run1.out` | 20:38:56→20:39:04 | 1 (dev mode, 4 control survivors) |
| `c1_rc.py` (26 mutants, 15 fixtures) → `run2.out` | 20:40:08→20:40:21 | 1 (same 4 survivors) |
| `tx.py` (text-only 7, direct ref-vs-mutant) → `tx.out` | 20:40:42→20:40:47 | 0 |
| `c1_rc.py --work` inside a git repo → `run3.out` | 20:41:06→20:41:08 | 2 (SETUP refusal, see A.4) |
| `oracle.py` (4 F1 candidates) → `oracle.out` | 20:42:20→20:42:21 | 0 |
| `o1grade.py` host python 3.13.16 / 3.13.8 / 3.13.5 | 20:43:13→20:43:31 / 20:44:36→20:44:48 / 20:44:50→20:45:02 | 0 |

---

## Headline

1. **Calibration (a): of the 33 selftest-survivors of `round_close.py` (R43PlanNext §A.3), 21 are killable from nothing by an exit-code direction under the round-44 contract
   (F1–F6 all enforced), measured, not inferred: 22 mutants killed ATTRIBUTED (`value=differs`) by 15 fixtures built from `git init`, 0 unattributed, 0 invalid, 0 null, `wrong=0 tampered=0 sidechannel=0`.**
   R43PlanNext's count was 17; four of its "text-only" rows (L168, L170, L182, L326-`if`) become `2>0` exit-code directions once the stub census exits 0 and the fixture is
   shaped to slip past the next guard. Remaining 12: **7 stream-only** (reachable, need a stdout/stderr direction the counter lacks), **4 unreachable** (1 env-gated + 3 counter-gated, all four
   survive every fixture I built), **1 equivalent** (L180). 21 + 7 + 4 + 1 = 33.
2. **Coverage (b): pick `password-recovery` (class F1, a different grader shape: whole-line list membership, no guess cap).** Offline oracle in ~1 s from pinned files, zero network. Runner-up
   `sqlite-db-truncate` (F1, threshold set-intersection `score > 6` of 8 constants; python only). O1 is **feasible offline** (the first measured O1 oracle) but only with a pinned older Python:
   the published oracle **FAILS on python 3.13.16 and PASSES on 3.13.5/3.13.8** (floating `python:3.13-slim-bookworm` tag drift) — a finding of its own, but a pinned interpreter download is the
   same kind of policy blocker as D1's 50.6 MB DB.

---

## A. Calibration: the 17 reachable `round_close.py` survivors under the round-44 counter contract

### A.1 Method (commands)

```
S=/fast/scratch/hyaku/kengaku-r44/R44PlanNext; git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane     # HEAD 5e3d3aa0…
python3 $S/mkctr.py            # scratch COPY of plans/round44_c1_verify.py -> $S/ctr/c1_rc.py (outside the lane; final diff: counter.diff)
envelope.sh $S/env python3 $S/ctr/c1_rc.py --lane $S/lane --battery-dir $S/bat --work $S/w   # dev mode: PREDICATE n/a
```

The scratch counter differs from the frozen one by (`counter.diff`, 10 KB, of which the `MUTANTS` table is most): `TOOLS["round_close"]` + its PIN (+2 lines); an exact-argv-shape branch in
`argv_shape_breach` for round_close (+14 lines: `--lane V`, `--round V`, `--census V`, `--work V`, `--selftest`; exact tokens, no repeat, `--lane` required — the F3 rule applied to a third tool);
26 `MUTANTS` rows. Everything else (legs a–i, R1–R4, F1–F6, value attribution, sidechannel token scan, read-only sandbox) is the frozen counter's code. The battery is `rc_close.py` (15
fixtures, no SIDECHANNEL token: `grep -ciE '<token list>' rc_close.py` → 0). The tool under test is bound at the slot, `cwd` = fixture dir, env pinned (no `SHOKUNIN_ROOT`), `--ro-bind /`.

Stubs the fixtures write (the module contract allows no lane clone): `plans/order_check.py` = `sys.exit(0)` (it is run with `sys.executable`, no exec bit); a census stub
`#!/bin/sh … exit 0|2` installed executable with `ctx.sh("install", "-m", "755", …)` (`chmod` is a banned token; `install` is not).

### A.2 Result (`run2.out`)

```
PINS total=3 mismatched=0 | BATTERY fixtures=15 wrong=0 tampered=0 sidechannel=0
MUTANTS total=26 killed=22 survived=4 invalid=0 null_detected=0 unattributed=0 | MUTANTS-BY-TOOL anchor=0/0 order=0/0 round_close=22/26
(run1.out, 11 fixtures: total=21 killed=17 survived=4; the 17 first-run kills are identical in run2)
```

| line | mutation | direction | killed by (fixture) | attributed | note |
|---|---|---|---|---|---|
| 98 | `== 0 → != 0` (`git_ok`) | 0>2 | `rc-receipt-deleted` | L98 | receipt committed, deleted from work tree |
| 98 | `0 → 1` | 0>2 | `rc-receipt-deleted` | L98 | same |
| 132 | `or → and` | 0>2 | `rc-receipt-deleted` | L132 | same |
| 122 | `== → !=` | 0>2 | `rc-evidence-path-only` | L122 | claims name only a backticked `…/round39/x-probe.txt` |
| 122 | `if → False` | 0>2 | `rc-evidence-path-only` | L122 | same |
| 145 | `and → or` | 2>0 | `rc-census-lane-first` | L145 | two stub censuses: lane's own exits 2, `d/scripts/` (cwd) exits 0; no `--census` |
| 149 | `if → False` | 0>2 | `rc-census-in-parent` | L149 | census only in `d/scripts/`, lane = `d/lane` |
| 175 | `if → False` | 2>1 | `rc-no-claims` | L175 | `--round 40`, only round-39 claims (mutant: traceback rc 1) |
| 178 | `if → False` | 2>1 | `rc-no-order-tool` | L178 | |
| 319 | selftest `if → False` | 2>1 | `rc-selftest-no-census` | L318 | span starts on the `if args.selftest:` line (my `old` began there; harmless) |
| 321 | `return 2 → 0` | 2>0 | `rc-selftest-no-census` | L321 | |
| 322 | selftest `if → False` | 2>1 | `rc-selftest-no-order` | L322 | |
| 324 | `return 2 → 0` | 2>0 | `rc-selftest-no-order` | L324 | |
| 326 | `is → is not` | 0>2 | `rc-gate-ok` | L326 | any accept gate run (4 hits) |
| 328 | `is → is not` | 0>2 | `rc-gate-ok` | L327 | span is the 2-line `old` |
| 328 | `if → False` | 2>1 | `rc-census-absent` | L327 | `--census` names a missing file |
| 331 | `return 2 → 0` | 2>0 | `rc-census-absent` | L330 | |
| **168** | `if top.returncode != 0 → False` | **2>0** | `rc-lane-is-cwd-nonrepo` | L168 | **new vs R43 (was text-only 2>2)**: lane = `.` = cwd, a tree with no repo; mutant's `Path("").resolve()` = cwd = lane slips past L170 |
| **170** | `!= → ==` and `if → False` (2 mutants) | **2>0** | `rc-lane-nested-in-repo` | L170 | **new**: lane = `d/lane/sub`, a lane-shaped dir inside a repo whose top is `d/lane` |
| **182** | `if → False` | **2>0** | `rc-no-registry` | L182 | **new**: stub census exits 0, so the run completes (R43: text-only because the real census failed) |
| **326** | `if args.round is None → False` | **2>0** | `rc-claims-named-none` | L326 | **new**: lane holds `plans/round-None-claims.md` + `Receipt:` line, so `CLAIMS.format(round=None)` resolves |
| 145 | `if env_root → False` | – | none | – | SURVIVED `exhibits=none` — **env-gated**: counter env has no `SHOKUNIN_ROOT`; argv cannot set env |
| 243 ×3 | `if/or/elif` of the R5 clear-reused-`--work` | – | none | – | SURVIVED `exhibits=none` — **counter-gated**: `{WORK}` is created fresh and empty per run; `d` is read-only; `--work` into `d` would make `unlink`/`rmtree` raise in the reference too [INFERENCE, not run]; `..` is refused by `path_ok`. Fixture `rc-selftest-runs` (`--selftest --work {WORK:sw}`, ref rc 1 with the stub order tool) reaches the code and sees no difference |

Counting by R43's 33 sites: 17 (the original R list) + 4 (L168, L170, L182, L326-if) = **21 rc-directional**; the 22nd killed mutant is the extra L170 `!=→==` variant I added.

### A.3 The other 12 (measured, `tx.out`, direct ref-vs-mutant, same normalisation as R43's `rcmeasure2.py`)

| line | mutation | witness | class |
|---|---|---|---|
| 116 | `and → or` (dedupe `rel not in found`) | claims naming one receipt twice (rule (a) + rule (c)): rc 0>0, stdout differs | stream-only |
| 165 | `if not lane.is_dir() → False` | `--lane <file>`: rc 2>2, stderr differs (L168 then catches it: rc-equivalent) | stream-only |
| 200 | `or → and` | rc 0>0, stdout differs (extra blank line) on 4 fixtures | stream-only |
| 200 | `not x → x` | stub order tool printing no trailing newline: rc 0>0, stdout differs | stream-only |
| 201 | `if r.stderr.strip() → False` | stub order tool writing stderr: rc 0>0, stderr differs | stream-only |
| 210 | `if r.stderr.strip() → False` | stub census writing stderr: rc 0>0, stderr differs | stream-only |
| 300 | selftest `if not ok → False` | selftest over the stub lane (ref rc 1, 30 stderr lines): rc 1>1, stderr differs | stream-only |
| 180 | `if not census.is_file() → False` | none | **equivalent** (`find_census` returns only existing files) |

Counter price of a stream direction (priced, not built): `Runner.run` currently returns `(rc, classes(stdout))` and drops stderr; a `text` direction needs `r.stderr` kept (1 line),
a scratch-path normaliser (R43's `norm`: `/fast/scratch/\S*|/tmp/\S*|\d+\.\d+s|round-close-selftest-\S*`), one `exhibits` branch and a `TOTAL`/`FLOORS` entry: ~15 lines, no new leg (g works on the
span as is).

### A.4 Contract findings that change the plan (measured)

- **F6 makes a non-repo `--lane` fixture environment-dependent.** `lane_breach` runs `rev-parse` with no ceiling; for L168's fixture (`--lane .`, no repo) the walk goes above `d`. With
  `--work $S/repo/w` where `$S/repo` is a git repo: `SETUP fixture 'rc-lane-is-cwd-nonrepo' … --lane rev-parse --show-toplevel=…/repo is outside the fixture` (`run3.out`, exit 2).
  Under the predicate run (`--work` default `$TMPDIR`) this passes only if no ancestor of the scratch root is a repo. Either drop L168 (20 environment-independent mutants) or fix
  `lane_breach` to use `GIT_CEILING_DIRECTORIES=d.parent` as the tool run's own discovery does (the tool run's ceiling is the scratch root, so discovery from inside it cannot see an ancestor repo).
- F3 needs a third shape for round_close (the frozen `argv_shape_breach` would fall through to the anchor branch and refuse `--round`): A.1.
- Leg i (`order_argv_breach`) does not apply: round_close reads claims/receipt itself from `--lane`; the order tool inside the fixture is the fixture's own stub, so these kills price the
  *gate's* legs only, not `order_check.py` (named limit; the order tool is already priced by U14c etc.).
- `adv` sentences exist at `plans/round_close.py` docstring lines: `:18-20` (exit codes, "no claims file, no order tool, no census script"), `:25-31` (receipt rules (a)(b)(c)),
  `:33-35` ("neither a file in the lane nor committed in HEAD … dropped"), `:37-40` (selftest), `:52-53` (census search order). My `adv` cells in the scratch counter are placeholders; a freeze needs real quoted sentences
  with file:line (L168/L170 map to the Limits bullet "`--lane` must be the git work-tree top").
- Cost: 15 fixtures, one 6 KB module, ~13 s for 26 mutants with attribution; `FLOORS` would become `{anchor:4, order:1, round_close:21}`.

---

## B. Coverage: next uncovered class

### B.1 Candidate table (pinned `2fd12b88…` tree via `gh api …/git/trees/<pin>?recursive=1` → 1038 blobs; sizes from it)

| task | class | grader shape | offline oracle (measured) | blocker |
|---|---|---|---|---|
| **password-recovery** | F1 | `Path(...).read_text().strip().split("\n")`; `assert P in guesses` — **whole-line list membership, no cap on guesses** (`test_outputs.py:13-16`) | setup.sh (zip, strings, dd, urandom) + solve.sh, paths remapped: `pw solve rc 0`, grader both tests pass | none; host has zip/strings; recipe is pure bash |
| **sqlite-db-truncate** | F1 | set of `(word,value)` tuples ∩ 8 embedded constants, `score > 6` (`:31`) — **threshold tolerance** | `trunc.db` 4096 B pinned; `solve.sh` python → grader pass | none (stdlib only) |
| vulnerable-secret | F1 | exact `content == FLAG{…}` after `.strip()` + prefix/suffix/len tests | `gcc` default **fails** on host gcc 16.2.1 (`gets` implicit decl); `-std=gnu99` builds, oracle passes | toolchain divergence (image gcc 12) must be a named limit |
| code-from-image | F1 | `output.strip() == "bee26a…"` | sha256 chain over the pinned `code.png` (95041 B) with SALT → `H == bee26a133f10…defe` True | 95 KB binary capture; answer is also a constant in the grader |
| fix-git | F1 | md5 of two working-tree files | – | `setup.sh` does `git clone https://github.com/…` (network) |
| break-filter-js-from-html | **O1** | grader runs the grader-owned `filter.py` then headless Chromium + selenium alert | oracle **PASS on 3.13.5 and 3.13.8** (0.3 s; failing cases 5.3 s each = alert timeout); **FAIL on 3.13.16** | needs selenium 4.35.0 + bs4 4.13.4 wheels (PyPI) and a pinned older CPython via `uv python install` (download) |
| query-optimize | D1 | runtime ≤ 1.05× golden over 5 alternating runs; DB hash pin | R43: 40/40 pass | 50,606,080 B DB download (unchanged) |
| pytorch-model-recovery | W1 | `torch.allclose` vs `tests/weights_gtruth.pt` | – | 3 pinned `.pt` files (5.0+5.0+0.2 MB), `import torch` fails on host |
| train-fasttext | W1 | accuracy threshold on a hidden test set | – | `tests/private_test.tar.gz` 11,506,423 B, no `fasttext` on host |
| qemu-startup / qemu-alpine-ssh / install-windows-3.11 | V1 | emulator/VM | – | `qemu-system-x86_64` not installed; images not in the pin |

### B.2 `password-recovery` measured (`oracle.out`, `oracle.py`)

Grader: `guesses = read_text().strip().split("\n")`, `assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses`. Cases (host python, `/app` remapped):

| case | result |
|---|---|
| oracle (solve.sh, 2 lines written) | pass / pass |
| exact line; constant without newline; constant + `\r\n`; constant + trailing space; leading blank line | pass |
| 100,000 decoy lines + the constant | pass (no guess cap) |
| `PASSWORD=8XDP5Q2RT9ZK7VB3BV4WW54` — **the format the instruction shows** | **FAIL** (list membership, not substring) |
| empty file / wrong constant | FAIL |

Two things a round-45 entry could say, both absent from the feal-linear entry: the **line-membership vs substring contrast** (feal: `c in data`; here: `in list`), and an instruction/grader gap
(instruction `:4` describes `PASSWORD=XXXX…` as the file format; the grader wants the bare value). It also re-uses V11's predictor machinery directly: the round-44 predictor controls
already include an "exact-lines reading" (`control-c2-predictor.txt`, 18 disagreements on feal), which is precisely this grader's semantics. Dockerfile installs forensic tools the oracle never
calls (`solve.sh` uses `grep -aob`/`dd`); recipe = `setup.sh` verbatim minus `/app` paths.

### B.3 `sqlite-db-truncate` measured (runner-up; `oracle.out`)

oracle pass; 6 of 8 rows FAIL, 7 of 8 pass, 7 right + 1 wrong value pass, 7 right + junk row pass, 8 ints for float constants pass (`10 == 10.0` hashes equal), 7 duplicates of one row FAIL (set),
string values FAIL, no file → `FileNotFoundError` (an error, not an assertion). Constants (8 rows) are public in the grader; the threshold means a partial attack passes.

### B.4 O1 measured (the part R43 left "not tried")

`uv venv` + `uv pip install selenium==4.35.0 beautifulsoup4==4.13.4` into scratch (envelope; channel `uv`, official; nothing installed outside scratch). Host Chromium 154.0.8037.97 and chromedriver
154.0.8037.97 (pacman, pre-installed). Grader `test_out_html_bypasses_filter` run with `/app` and `/tests/filter.py` remapped:

```
python 3.13.16 (uv default):  ORACLE FAIL "No alert detected after filtering"   (filter.py turns '<!-->asdf<script>…' into '<!-- -->asdf --&gt;')
python 3.13.8:                ORACLE pass 0.3 s    no-file FAIL 0.0    plain-script FAIL 5.3    empty FAIL 5.3
python 3.13.5:                ORACLE pass 0.3 s    same other cases
```

Raw `<script>alert(1)</script>` page: `ALERT in raw script page: 1` (headless Chromium works inside the envelope with `--no-sandbox`). Verdict depends on the interpreter's `html.parser` patch level
(bs4 4.13.4 pinned, Python tag floating): a hosts-vs-image divergence that decides pass/fail, which makes O1 a better novelty than another F1 but a worse first offline counter (needs a
pinned CPython + wheels; no clean-clone rule for that yet).

### B.5 Recommendation for round 45

- **Coverage:** `password-recovery` (F1; 9 files, 10,129 B total from the pin (tree sizes); `setup.sh` + `solve.sh` run in ~1 s; no network). Second-choice batch item: `sqlite-db-truncate` (threshold shape).
  Not recommended without a policy decision: O1/D1/W1/V1 (downloads or missing emulators).
- **Calibration:** 21 round_close mutants + 7 stream-only (needs the ~15-line stream direction) + decide L168 (env-dependent under F6). `FLOORS` literal changes; the three-tool counter keeps
  C1's one-sentence predicate shape (`PINS total=3`).

---

## Limits

- The scratch counter is a modified copy, not the frozen counter; its kills are measured under the same code paths but are not a landing receipt. `adv` cells are placeholders.
- Fixtures are mine, scratch only, not offered as battery material; stub order/census tools mean the kills price round_close's own legs, not the real order tool/census.
- The 7 stream-only rows were measured outside the counter (`tx.py`, direct runs, scratch paths normalised); the counter has no stream direction to attribute them.
- Unreachability of the 4 is by reading plus failure to construct (`exhibits=none` on 15 fixtures), not a proof for every conceivable fixture.
- vulnerable-secret needed `-std=gnu99`; password-recovery's image (ubuntu:24.04) is not pulled, host `zip`/`strings`/bash stand in. O1's host Chromium 154 stands in for Debian's.
- No prior-art search for any candidate was run (a wave item before any novelty sentence).
- `mkctr.py` in the report dir is the first-run generator (17+4 rows); the final counter delta is `counter.diff` (26 rows).

Scratch `$S` removed with `plans/scratch_guard.py safe-rm` after this report.

VERDICT: plan45-calibration-21-coverage-password-recovery
