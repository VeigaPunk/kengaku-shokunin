# F42XMutNear — wave-2 falsify: near-variant mutation probe over the C1 pair

Seat: F42XMutNear (mutation tester) · 2026-10-26 · lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
all runs against a scratch clone at `508434ad55c709337065611691c426f05875492d` (`git -C $S/lane rev-parse HEAD`).
Attack target: the landed C1 calibration (frozen 14 mutants, `plans/round42_c1_verify.py`, `plans/battery42/`).

## 1. Method

- Scratch `S=/fast/scratch/hyaku/kengaku-r42/F42XMutNear`; clone rule followed (`git clone -q --no-local`,
  checkout `508434a`), toplevel asserted = `$S/lane`; `git status --porcelain | wc -l` = `0` afterwards.
- Copy of the counter with `MUTANTS` swapped to the frozen 14 **plus 25 new near-variants** (same branches
  as the frozen mutants, single `old -> new` replacements; every `old` verified `count==1` in its tool,
  every variant `py_compile`-clean, direction/cls rule honoured). Copy kept at
  `.ufo/waves/round-42/falsify/F42XMutNear/verifier.py` (sha256 `d69a24fcd301d43a2541a39b936a594fdf44bc04d162873ecc25cdbad2ace28f`).
- Dev mode (`--battery-dir`, `--only`). Every run inside the mandated envelope, receipts carry the
  envelope line, `date +%T` and `ls -A /home/vgpnk/.local/bin | sha256sum` at both boundaries — the hash was
  `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52` at all six boundaries (nothing written
  to a PATH dir). Host tooling: nothing installed (no need).
- In-run controls: the frozen 14, riding in the same run, were **all killed, attributed** (e.g. `MUTANT X7
  anchor silence killed by=a_class-x7-fabricated-token attributed=L535`) — matching the landing measurement
  (`MUTANTS total=14 killed=14`), so the copy did not distort the detector. `BATTERY fixtures=29 wrong=0
  tampered=0 sidechannel=0`, `null_detected=0 invalid=0 unattributed=0`, `PINS total=2 mismatched=0` and
  `PINS-AFTER mismatched=0` — restoration evidence: the pinned tool bytes were never modified anywhere.

## 2. battery40 is unusable under the round-42 counter (limit, as forewarned)

`--battery-dir plans/battery40` fails at the first module:

> `AttributeError: 'Ctx' object has no attribute 'clone'` (receipt-battery40.txt, SETUP line)

All seven battery40 modules call `ctx.clone(d/"lane")` — the round-40 Ctx API the round-42 counter dropped
(builds now hide the lane). Two modules (`l_rows.py`, `l_refuse.py`) even target non-C1 tools. Per the task,
**battery42 alone** is the measured battery; this is itself a finding: C1's calibration is demonstrated only
over battery42's fixture universe.

## 3. Results on battery42 — 15/25 killed, 10 survived

Command (receipt `receipt-battery42.txt`, sha256 `6eacc0b68e83fca31362b67e5a7d652056dec8aa58deeafb195d4f0038f5af02`):
envelope line above + `python3 $S/verifier.py --lane $S/lane --battery-dir $S/lane/plans/battery42 --work $S/work42 --jobs 8`,
18:16:05→18:16:13, `exit=1` (dev mode, survivors present). Output line:
`MUTANTS total=39 killed=29 survived=10 invalid=0 null_detected=0 unattributed=0` (14 frozen + 25 near).

| id | tool | site (branch of frozen mutant) | mutation (single replacement) | dir | battery42 |
|----|------|-------------------------------|-------------------------------|-----|-----------|
| NA1 | anchor | X9 `!= NCELLS` | `!=` → `<` (over-long rows unflagged) | silence | **SURVIVED** |
| NA2 | anchor | X9 same line | `!=` → `==` (well-formed flagged) | rc-mirror | killed by=a_route-x1-provenance-table |
| NA3 | anchor | X6 `if tok in allowed` | inverted → labels swap | silence | killed by=a_class-x7-fabricated-token |
| NA4 | anchor | X6 `elif tok not in row_scope` | `row_scope` → `allowed` (route dropped) | silence | killed by=a_class-x6-sibling-digest |
| NA5 | anchor | X12 `slugs[d] = pick.rsplit…` | slug keeps `org/task` (url-task dead) | rc-mirror | **SURVIVED** |
| NA7 | anchor | X14 unresolved guard | drop `t not in allowed` | rc-mirror | **SURVIVED** |
| NA8 | anchor | X15 supported list | row-scope → `row_scope or allowed` | rc-silence | killed by=a_row-x15-sibling-digest |
| NA10 | anchor | X1 write side | `prov_sid` append dropped | rc-mirror | killed by=a_route-x1-provenance-table |
| NA11 | anchor | X3 write side | `prov_url` keyed by owner | rc-mirror | killed by=a_route-x3-provenance-url |
| NA12 | anchor | digest-short/long line | `< 64` → `<= 64` | silence | **SURVIVED** (null, §5) |
| NA18 | anchor | URL_RAW commit group | `{7,40}` → `{4,40}` | rc-mirror | **SURVIVED** |
| NA20 | anchor | erratum exemption | `exempt.setdefault` → `pass` | rc-mirror | **SURVIVED** |
| NA21 | anchor | erratum cited_wrong | `t in anchor_tokens` (keyed) | rc-mirror | **SURVIVED** |
| NA23 | anchor | X9 same line | `!=` → `>=` | rc-mirror | killed by=a_route-x1-provenance-table |
| NO1 | order | XO1 clause 1 | `== 0` → `== 1` | rc-silence | killed by=o_clause-freeze-single |
| NO2 | order | XO1 clause 1 | `== 0` → `!= 0` | rc-mirror | killed by=o_clause-clean-order |
| NO3 | order | XO3 clause 2 | ancestry args swapped | rc-silence | killed by=o_clause-receipt-withdrawn |
| NO4 | order | XO3 clause 2 | `freeze !=` → `==` | rc-silence | killed by=o_clause-receipt-withdrawn |
| NO5 | order | XO5 scan loop | `commits` → `commits[:1]` | rc-silence | **SURVIVED** |
| NO6 | order | XO6 GATE_P10 | alternation + `PASS\|OK` | rc-mirror | killed by=o_scan-xo6-pass-verdict-row |
| NO7 | order | P2 excuse regex | drop `(?:: \S+)?` variant | rc-mirror | **SURVIVED** |
| NO8 | order | XO7 CASE_LINE | only `observed=fail` | rc-silence | killed by=o_scan-xo7-timeout-rows |
| NO22 | order | gate-p10 branch | `if m:` → `if False:` | rc-silence | **SURVIVED** |
| NO23 | order | case-observed branch | `if` → `if False:` | rc-silence | killed by=o_scan-xo7-timeout-rows |
| NO26 | order | claims_dir round parse | `round_no` + 1 | rc-silence | killed by=o_scan-xo7-timeout-rows |

All kills are ATTRIBUTED (traced re-run reproduced the result and executed the replaced span), e.g.
`MUTANT NO26 order rc-silence killed by=o_scan-xo7-timeout-rows attributed=L163 hits=2`.

## 4. The 10 survivors probed: 9 real coverage gaps, each with a demonstrated killer

Probe battery `w2_probe.py` (sha256 `cb4d2c4105ca19289b381ec4827f987919e356464c8f4d55eeaf3cc28acf1d27`,
kept beside this report; 7 self-contained fixtures, contract-identical to battery42). Run
(receipt `receipt-probe-w2.txt`, sha256 `f37886ff8b31040162febb717a9314b6a28ea20c5da02844e8682221c9f5d0f4`):
`BATTERY fixtures=7 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=10 killed=9 survived=1`, 18:21:47→18:21:48.

Round-43 candidates (witness: battery42 has no fixture of this shape; the probe fixture kills, attributed):

1. **NA1** — battery42's two `row-malformed` fixtures are both under-length (10-cell); no 12-cell row
   fixture. `w2-long-row` kills (`attributed=L477`).
2. **NA5** — both url-route accept fixtures bind via slash-less names; no green fixture binds via
   `name = "<org>/<task>"` with a slash. `w2-slashed-name-url` kills (`attributed=L258`).
3. **NA7** — no accept fixture carries a *valid* erratum line (both erratum fixtures expect reject).
   `w2-green-erratum` kills (`attributed=L458`).
4. **NA18** — no fixture pins a URL with a short commit segment. `w2-short-commit-url` kills
   (`attributed=L154`).
5. **NA20** — the exemption route (the erratum feature's headline) is never the reason a lane stays green in
   battery42. `w2-green-erratum` kills (`attributed=L468`).
6. **NA21** — same gap, other site: cited_wrong membership. `w2-green-erratum` kills (`attributed=L456`).
7. **NO5** — every reject fixture's forbidden claims blob is first seen in the oldest claims commit; no
   fixture edits a claims blob in a *later* commit before the receipt. `w2-late-claims-edit` kills
   (`attributed=L120`).
8. **NO7** — battery42's only excused shape is the bare `receipt unreadable` (o_clause clean_order); the
   P2 echo `receipt unreadable: <path>` is undemonstrated green-side. `w2-p2-excuse` kills
   (`attributed=L60`).
9. **NO22** — no reject fixture is clause-3-gate-p10-only (clause-3 rejects are reached only in the mirror
   direction via o_scan-xo6-*). `w2-late-claims-edit` kills (`attributed=L105`).

Merged view: **24/24 behaviour-bearing near-variants have a demonstrated attributed kill** — 15 on battery42
itself, 9 on one fixture each that battery42 could adopt. The falsify wave's C1 admission caveat therefore
sharpens to: battery42 demonstrates the 14 frozen behaviours honestly, but 9 neighbouring behaviours of the
same branches rest on no fixture yet.

## 5. NA12 is a null mutant (excluded from the findings)

`<= 64` differs from `< 64` only at `len==64`, excluded by the enclosing `if len(tok) != 64:` guard
(plans/anchor_digest_check.py, the digest-short/long branch), so the mutated line is unreachable for any
64-hex token; the dedicated uppercase fixture still cannot execute it. Design error of mine, caught by the
probe; not a coverage finding and not evidence about the counter.

## 6. Receipts and restoration

- `receipt-battery42.txt` (10.6 KiB), `receipt-battery40.txt` (1.1 KiB), `receipt-probe-w2.txt` (3.2 KiB) —
  each carries envelope line, times, PATH-dir hashes, full counter output. None over 1 MiB.
- Restoration: lane clone untouched (porcelain 0, HEAD `508434a`); `PINS-AFTER mismatched=0` in all runs;
  `~/.local/bin` listing hash identical at every boundary. Scratch `S` is disposable; `verifier.py` and
  `w2_probe.py` are preserved in this report dir for the L1.

VERDICT: near-variants-killed-15/25
