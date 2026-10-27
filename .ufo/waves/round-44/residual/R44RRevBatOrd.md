# R44RRevBatOrd — residual review: battery44 `u14c_name_a` / `u14c_name_b` vs `plans/order_check.py`

Seat: R44RRevBatOrd (reviewer, kengaku round 44 residual, 2026-10-26).
Target: the two order-gate battery modules landed in integration commit
`2a263e5a56ef6d48d06805e1ccd106de5de9ba66`, reviewed against frozen
`plans/order_check.py:26-27` (the `Exit: … unparseable round number` docstring sentence) and
`plans/order_check.py:159-163` (receipt normalize → `CLAIMS_NAME.match` → guard → raise →
`int(m.group(1))` dereference). Lane clone verified before any use:
`git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r44/R44RRevBatOrd/lane`,
HEAD = `2a263e5a…`. No frozen file touched; all writes in my residual subdir and scratch.

Ground truth lines (raw reads of the frozen tool): `:26-27` docstring `Exit: 0 order holds · 1 order
broken · 2 setup error (… unparseable round number …)`; `:160 m = CLAIMS_NAME.match(Path(claims).name)`,
`:161 if not m:`, `:162 raise SetupError(f"claims file name is not round-NN-claims.md: {claims}")`,
`:163 round_no = int(m.group(1))`. The counter's own span arithmetic agrees
(`attributed=L161`), so module a's `:161 if not m:` cite is exact.

## Q1 — does each fixture's claims name genuinely fail CLAIMS_NAME for the advertised reason? YES, 8/8

`CLAIMS_NAME = ^round-(\d+)-claims\.md$` is case-sensitive and anchored; matched against the basename
of the repo-relative `--claims` path. Measured reference behavior in every case is exit 2 with
`ORDER ERROR claims file name is not round-NN-claims.md: <path>` (see probe receipt):

| fixture | `--claims` basename | advertised reason | fails because | ref rc |
|---|---|---|---|---|
| a-draft-suffix | `round-44-claims.md.draft` | "leftover `.draft` beside it" | trailing suffix | 2 |
| a-subdir-nohyphen | `round44-claims.md` | "name lost the hyphen" | missing `round-` hyphen | 2 |
| a-uppercase-pair | `ROUND-44-CLAIMS.md` | "case-shifted" | case-sensitive pattern | 2 |
| a-canonical-control | `round-44-claims.md` | control: gate passes | — (matches) | 0 |
| b-registry-suffix | `round-51-claims.md.orig` | "landed under the editor's `.orig` name" | trailing suffix | 2 |
| b-nested-uppercase | `Round-7-claims.md` | "capitalised file name" | case-sensitive pattern | 2 |
| b-round-xx-token | `round-xx-claims.md` | "no digits at all" | `\d+` rejects `xx` | 2 |
| b-underscore-name | `round_44_claims.md` | "Underscore spelling" | separators not `-` | 2 |

Every error fixture's name is unparseable by the pattern — no fixture reaches a parseable-round
failure mode by accident (e.g. none relies on a missing file or bad argv, which would also exit 2 but
for a different advertised reason). The counter agrees: all 8 FIXTURE lines `ok`, expected vs
observed rc exact (`counter-u14c.txt`).

## Q2 — is the argv the exact contract shape? YES, 8/8

Every build returns exactly `["--lane", str(repo), "--claims", V, "--receipt", V]` — 6 tokens, no
`--opt=value`, no extras, repo path inside the fixture dir (`d/<registry|worktree|lane|control|history|inverted|onecommit>`).
Checked three ways: source read of all 8 build functions; the counter's F3 `argv_shape_breach` +
leg-i blob checks passed (`BATTERY wrong=0`); my driver's independent shape assert printed
`argv-shape=True` 8/8. Every `--claims`/`--receipt` path is a committed blob at HEAD of its repo, so
leg i never has to fall back to the tool's own setup error.

## Q3 — would the mutant's continuation really be what kills it? YES

Frozen old→new replaces `:161 if not m:` with `if False:`. Reading the site record mechanics
(`round44_c1_verify.py` TRACER: records `prev>after:<locals digest>` when the previous line executed
was in the span): reference records `161>162` (the raise fires); mutant executes `161` (`if False:`),
skips the raise, next line `163` → records `161>163`, then `int(m.group(1))` raises
`AttributeError: 'NoneType' object has no attribute 'group'` → exit 1. Records differ ⇒ leg g
satisfied; line 161 itself executes in both ⇒ leg f satisfied. Counter: `MUTANT U14c order error
killed by=u14c_name_a-draft-suffix attributed=L161 value=differs hits=7` — 7 hits = every error
fixture, and the kill is attributed on an *error* fixture, not the accept control (control: ref 0 /
mut 0, measured — the mutant is harmless when the name matches, so the guard is the only mover).

I did not trust the trace alone: my probe ran a hand-mutated scratch copy (digest-verified identical
to the pinned tool before the one-line edit) against every fixture built from nothing. All 7 error
fixtures: ref 2 → mut 1 with exactly that AttributeError at the `m.group` dereference; control 0→0.
The continuation both docstrings advertise — "dies later on `m.group(1)` with exit 1 — never 2"
(u14c_name_a) / "the next statement dereferences the None match: the gate dies with exit 1"
(u14c_name_b) — is the measured behavior, and it is what moves `error` direction (ref 2, mut in
{0,1}).

## Contract compliance and hygiene

- FIXTURES entries carry exactly `fid`/`tool`/`expect`/`defects`/`build`; `tool=order`,
  `defects=[]` throughout (order prints no `class=` token), `expect` matches measured reference rc.
- Builds fill only the empty dir `d` via `ctx.init/ctx.write/ctx.git`; no lane clone is read; all
  argv paths inside `d` (counter's lane/repo/symlink breaches all clean).
- Sidechannel: counter `sidechannel=0`; my own case-insensitive grep of the 27-token list over both
  modules: no matches (exit 1). Module digests:
  `u14c_name_a.py 6e8dc5d0db31416ab21b7278e2b3dd70c4265c36f212708d03f998f13cd9bcf9`,
  `u14c_name_b.py 7ac8f05ebf07d78087cdf3239dccb4d4c550b9bc154c1f0ce89c156deef62620`.
- Not a re-spelling of the witness: `w_u.py`'s sole order fixture `u14c-odd-claims-name` is a flat
  two-commit lane passing `plans/odd-claims.md` + `corpus/evidence/round7/x-probe.txt`. The battery's
  8 fixtures share neither name, receipt path, nor history shape (three-round registry, merge-commit
  subdirectory lane, one-commit uppercase pair, six-commit registry, nested capitalised round-7 lane,
  receipt-first inverted lane, one-commit underscore pair, plus a canonical control). Different
  failure vocabulary, no copied code paths (witness uses a shared `lane()` builder; battery modules
  have their own `_commit`/`_registry` helpers with different content).
- 33-fixture battery all built and behaved (`BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0`),
  pins intact before/after (`PINS total=2 mismatched=0`, `PINS-AFTER mismatched=0`).

## Findings by severity

- HIGH: none.
- MEDIUM: none.
- LOW: none.
- INFO 1 — module b's docstring reads "`plans/order_check.py:161-162` normalizes `--claims` and then
  refuses…": normalization (`repo_path`) is at :157-158; :161-162 are exactly guard+raise, which is
  what the sentence's quote cites. Loose wording only, no wrong claim survives a check.
- INFO 2 — inert shape decoration: a-uppercase-pair ("both added by the very first commit"),
  b-round-xx-token (receipt commit precedes claims), b-underscore-name (one-commit freeze) build
  order-breaking histories that neither the reference (exits 2 at the guard) nor the mutant (crashes
  at :163 before any ORDER check) ever exercises. Honest diversity, zero kill power; docstrings do
  not claim otherwise (b's underscore comment even says "history order cannot answer it").
- INFO 3 (self) — my first probe run compared the reference against itself (copied
  `order_mut.py` but had not applied the edit), producing 7 meaningless `mut=2` MISMATCH lines.
  Discarded; the receipt is the corrected rerun, and the counter run is independent of that mistake.

## Verification (Q32 envelope lines; full receipts in this seat's subdir)

Counter (`--only U14c`, exit 0):
`ENVELOPE start 20:51:08 … end 20:51:11 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`
→ `PINS total=2 mismatched=0` … `MUTANT U14c order error killed by=u14c_name_a-draft-suffix
attributed=L161 value=differs hits=7` → `BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0` →
`MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0` →
`MUTANTS-BY-TOOL anchor=0/0 order=1/1` → `ADVERTISED direct=1 indirect=0 none=0` →
`PINS-AFTER mismatched=0` → `PREDICATE C1 n/a (non-default battery or mutant subset)`.

Probe (reference vs hand-mutated copy, exit 0):
`ENVELOPE start 20:52:55 … end 20:52:57 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`
→ `ok` × 8 (7× ref 2/mut 1 AttributeError at `m.group`, control 0/0) → `DRIVER fixtures=8 mismatches=0`.

Receipts: `.ufo/waves/round-44/residual/R44RRevBatOrd/counter-u14c.txt` and
`…/probe-u14c.txt` (both far under 1 MiB). No tool installs were made.

## Residual risk and verification gaps

- I did not re-run the full 5-mutant battery (`PREDICATE C1 pass` stays the L1's measurement); this
  seat's mandate was `--only U14c`.
- I verified leg-g semantics by construction and by the counter's `value=differs` verdict, not by
  re-reading the tracer's emitted site bytes; the independent probe pins the same continuation
  (`raise` skipped, crash at :163, exit 1), so the attribution cannot rest on a coincidental record.
- Probe repos were built with a minimal `ctx` and isolated git identity; commit metadata may differ
  from the counter's builds, but the guarded behavior is commit-content independent and both runs
  agree fixture-for-fixture.
- Both modules are honest as landed; nothing in scope requires a change.

VERDICT: order-modules-honest-2/2
