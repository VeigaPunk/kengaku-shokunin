# F41XMutReceipts — near-variant generalisation probe on `plans/tip_receipts.py` (round 41, wave 2)

Date: 2026-10-26. Seat: F41XMutReceipts (mutation-tester, leaf). Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin.

## Axes (godspeed)

1. **Kill breadth** — how many near-variant mutants (outside frozen T01-T13) the landed battery41 kills.
2. **Observability** — which advertised sentences of `tip_receipts.py` have *no* demonstration in battery41 (each survivor = one).
3. **Cost** — one counter pass, 6.05 s wall, everything inside the prescribed bwrap envelope.

## What was measured

- Commit: clone HEAD `d7c77895752a2a5f317fa22f2362416ada50a04b` = the goal's tip `3d0058fb` plus the wave-2
  dispatch commit (`git log`: `d7c7789 round-41: wave-2 (falsify) spec and dispatch`; `3d0058fb IS ancestor of
  HEAD`, `74513c06 IS ancestor of HEAD`). Frozen bytes verified before the run against
  `.ufo/waves/round-41/claims/frozen-digests.txt`: `plans/tip_receipts.py` `e4f49714…`, `plans/round41_c1_verify.py`
  `8835a94b…` — both FROZEN-OK in the clone.
- The frozen counter was **not** edited. A scratch copy `counter_x.py`
  (sha256 `d21923fe1db26f5ded565c1345fa01664a2073269f2a38335e4835205c579b3a`) had its `MUTANTS` list replaced with
  20 single-line near-variants of `tip_receipts.py` (builder: `build_probe.py`, both archived beside this report).
  Every `old` string occurs exactly once in the pristine tool and every variant compiles (`VALIDATION OK`, 20/20).
- Battery: the landed `plans/battery41/` (7 modules, 48 fixtures), untouched. 29 receipts-tool fixtures exercise
  each mutant; the counter also re-ran all 19 sources fixtures for its reference/null passes.
- Run envelope (orchestrator-prescribed):
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent python3 counter_x.py --lane $S/lane --work $S/wrk --jobs 8 --only N01,…,N20`
  with `$S=/fast/scratch/hyaku/kengaku-r41/F41XMutReceipts` (scratch-only mutated copies; lane untouched).
  `--only` puts the counter in dev mode → `PREDICATE C1 n/a (non-default battery or mutant subset)`, exit 1
  (`survived>0` in dev mode). That exit is the probe's signal, not a battery failure.
- No tool installs were needed; nothing was installed.

## Result

Full log: `c1x-run.txt` (archived). Key lines:

```
BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0
MUTANTS total=20 killed=6 survived=14 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=6/20 sources=0/0
PINS-AFTER mismatched=0
```

Reference behavior intact on all 48 fixtures (every `FIXTURE … ok`), battery deterministic (`null_detected=0`),
no sidechannel tokens, tool pins unchanged after the run. All six kills are in the mutant's declared direction.

### Killed 6/20

| id | mutated line | direction | killed by | advertised sentence now pinned beyond the frozen list |
|----|---|---|---|---|
| N08 | 222 `nb = b ^ 0x01` → `nb = b` (flip no-op) | rc-mirror | `r_ctl-t08-derived-uv-absent` | ":25-26 '`--tamper REL` … flips one byte … must answer `differ`'" |
| N11 | 260 `--list` skip reason text → `no-re-run-command` | silence | `r_map-t09-shared-stem-separators` | ":18-19 'printed on its own `skip reason=no-committed-re-run-command` line'" |
| N13 | 245 table plan kind → `"byte"` | rc-mirror | `r_run-t04-temp-paths-masked` | ":57 'kind \"byte\" must reproduce exactly; kind \"temp-paths\" declares embedded mkdtemp paths'" |
| N14 | 318 compare-side kind branch → `False` | rc-mirror | `r_run-t04-temp-paths-masked` | ":21 'A receipt that declares embedded scratch paths (`temp-paths`) is still re-run'" |
| N16 | 340 auto-control `equal` list → `[]` | silence | `r_ctl-t08-derived-uv-absent` | ":29-30 '0 … and the control reports `differ`'" |
| N19 | 264 work-parent `mkdir` → `False` | rc-mirror | `r_ctl-t08-derived-uv-absent` | ":35 'TMPDIR/TEMP/TMP inside the work directory (--work …)'" |

Counter lines, verbatim: `MUTANT N08 receipts rc-mirror killed by=r_ctl-t08-derived-uv-absent`, `MUTANT N11 …
killed by=r_map-t09-shared-stem-separators`, `MUTANT N13 … / N14 … killed by=r_run-t04-temp-paths-masked`,
`MUTANT N16 … / N19 … killed by=r_ctl-t08-derived-uv-absent`.

Reading: the battery generalises past the frozen T-lines for the byte-flip control, the `--list` skip grammar,
the temp-paths kind branch (both assignment and comparison), the auto-control trigger, and work-dir creation.

### Survived 14/20 — the sentence each survivor leaves undemonstrated (round-42 candidates)

Every survivor printed `exhibits=none`: no fixture showed any exit-code or class deviation. These are total
blind spots, not near-misses.

| id | mutated line | broken advertised sentence |
|----|---|---|
| N01 | 52 drop `re.IGNORECASE` from `CANDIDATE_RE` | ":12 'Population, stated mechanically: committed files `corpus/evidence/**/*probe*.{txt,log}`'" — case-blind candidate selection; no fixture commits an uppercase-named receipt |
| N02 | 85 `stem()` drops `.lower()` | ":15-16 'with non-alphanumerics dropped and case folded, the receipt stem … and the script stem … are the same token'" — script-side folding; `r_map-t09-shared-stem-case-fold` only shows the *unmapped-skip* path (its receipt stays unmapped under both mutant and reference) |
| N03 | 118 `which("git")` guard → `False` | ":30-31 '2 usage/setup (…, absent git, …)'" — no fixture runs with git off PATH |
| N04 | 146 drop `base in s` | ":7-8 'resolves each one's committed re-run command from the probe script's own `Run as:` line'" — nothing pins the command to the script's own name |
| N05 | 149 `shlex.split(re.split(r"\s{2,}", s)[0])` → whole line | ":147 'docstrings pad the command with 2+ spaces before a prose description: keep only the command'" — no fixture Run-as line carries trailing prose |
| N06 | 155 `if script in FALLBACK:` → `False` | ":67 'Fallback argv tails, used only when a script's `Run as:` line cannot be parsed.'" — fallback never exercised; note the fallback/no-command `origin` is *contract-invisible* anyway: the class grammar truncates the reason at the first `:` |
| N07 | 190 `first_diff` line number `+1` → `+0` | no advertised sentence (`adv_kind=none`) — differ diagnostics text is unobserved by the class extractor |
| N09 | 250 `--only` mapped filter → `True` | ":235 'restrict to receipts whose rel path contains this'" — no fixture passes `--only` at all |
| N10 | 251 `--only` unmapped filter → `True` | same help sentence, unmapped half — wholly undemonstrated |
| N12 | 275 `if head != tip:` → `False` | ":9 'clones the lane at HEAD into a scratch directory'" — guard untriggerable by construction (clone of the lane at HEAD always equals tip) |
| N15 | 341 `min(equal, …)` → `max(...)` | ":26-27 'one control runs automatically on the cheapest byte-equal receipt'" — the class grammar records `control:verdict` without the receipt, so *which* receipt is chosen is invisible |
| N17 | 351 control-side mask ternary → `False` | ":22 'equality after masking is a reproducibility claim up to those paths'" (control branch) — dead in battery: tamper fixtures only hit skipped/unavailable receipts, never a *ran* temp-paths receipt |
| N18 | 333 comma-split of `--tamper` → `list(args.tamper)` | ":25 '`--tamper REL` (repeatable, comma-splittable)'" — no fixture passes a comma-joined list |
| N20 | 357 `shutil.rmtree(ws, …)` → `pass` | ":36 'the work directory is removed on exit'" — cleanup invisible: run dirs are per-run scratch the counter wipes; fixture fingerprints never see them. Contrast N19: work-dir *creation* is observed (mkdtemp crash), *removal* is not |

### What holds, what breaks

- **Holds:** C1's demonstrated core is robust beyond its frozen points — the six kills show battery41 pins the
  control byte-flip, the `--list` skip grammar, the temp-paths kind handling, the auto-control trigger and the
  work-dir creation against arbitrary single-line corruptions of neighbouring lines, not just the frozen sites.
  The battery itself is clean and deterministic under a 20-mutant foreign load (no tamper, no null, no sidechannel).
- **Breaks (coverage, not the contract):** fourteen advertised behaviours have no killing fixture. Cheapest
  round-42 admissions are new fixtures, not grammar edits: `--only` (one fixture, mapped+unmapped halves),
  comma-joined `--tamper`, git-absent PATH, prose-padded `Run as:` line, uppercase script stem mapping, a tamper
  on a temp-paths receipt that actually ran. Two findings are contract-level, fixture-resistant as-is: the
  control-receipt choice (N15) and work-dir removal (N20) are invisible to the class grammar/fingerprinting —
  closing those needs a counter change (e.g. record the control receipt in the class; check the run dir is empty
  after exit), which would ripple into the frozen predicate, so they are round-42 design items, not battery items.

## Restoration evidence

- Only scratch copies were mutated: pristine `tip_receipts.py` sha256 before run `e4f49714…f88f3` (frozen pin),
  after run identical; `round41_c1_verify.py` `8835a94b…` before and after identical — both equal their
  `frozen-digests.txt` entries. `PINS-AFTER mismatched=0` in the run itself. The 20 variant files lived only in
  `$S/val/` (hashes archived in this report dir's `c1x-run.txt` companion — see below; variant sha256s recorded
  in the run transcript kept at `.ufo/waves/round-41/falsify/F41XMutReceipts/variants-sha256.txt`).
- Scratch `$S=/fast/scratch/hyaku/kengaku-r41/F41XMutReceipts` deleted after receipt copy, with the mandated
  guard (`case "$T" in "$S"|"$S"/*) ;; *) refuse;; esac`). No writes outside this report dir and scratch.

## Receipts (this dir)

- `c1x-run.txt` — full counter output (48 FIXTURE lines, 20 MUTANT lines, BATTERY/MUTANTS/PINS-AFTER lines)
- `counter_x.py` — the scratch counter copy that ran (sha256 `d21923fe…`)
- `build_probe.py` — mutant list + splice/validation script (`VALIDATION OK`, per-mutant line numbers)
- `variants-sha256.txt` — sha256 of each mutated variant (before/after byte identity evidence)

VERDICT: near-variants-killed-6/20
