# R44RRevBatAnc1 — residual review: battery44 anchor modules u5_short_a, u5_short_b, u6_long_a, u6_long_b

Round 44 residual, 2026-10-26. Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; reviewed clone: landing
commit `2a263e5a56ef6d48d06805e1ccd106de5de9ba66` (`git -C "$S/lane" rev-parse HEAD` → `2a263e5a…`, `--show-toplevel`
→ `$S/lane`). Frozen claims read in full first (`plans/round-44-claims.md`). Scope: fixture-by-fixture review of the
four anchor battery44 modules for mutant behaviours U5 (`digest-short` label) and U6 (`digest-long` label),
advertised at `plans/anchor_digest_check.py:88` ("any other anchor token must be exactly 64 lowercase hex digits
(`digest-short`, `digest-long`, `digest-uppercase` otherwise)", implemented at `:522`
`cls, why = ("digest-short" if len(tok) < 64 else "digest-long"), f"{len(tok)}-hex"`); honesty of `defects`/`expect`;
re-spelling check against `.ufo/waves/round-44/claims/witness/w_u.py`; counter run `--only U5,U6` inside the envelope.
Nothing frozen was edited; the lane clone and all fixture repos live in scratch.

## 1. Method

1. Read the frozen claims file, the counter docstring + MUTANTS table (`plans/round44_c1_verify.py:230-240`), the
   anchor tool (docstring, `bind_row`, per-token classification `:506-548`), all four modules in full, the witness
   `w_u.py`, and `.ufo/waves/round-44/integrate/shape-diff-battery44.txt`.
2. Counter run on my clone (development mode, envelope; ENVELOPE lines pasted in §5):
   `envelope.sh "$S/env" python3 "$S/lane/plans/round44_c1_verify.py" --lane "$S/lane" --battery-dir "$S/lane/plans/battery44" --only U5,U6 --work "$S/w"`
   (receipt `R44RRevBatAnc1/counter-u5u6-run1.txt`, sha256 `8de94ef21b8a…`).
3. Independent probe (receipt `R44RRevBatAnc1/probe-run1.txt`, sha256 `f37eb0abdb7e…`): inside the envelope I
   rebuilt all 14 fixtures of the four modules from nothing with a minimal re-implementation of the counter's
   `ctx` (fixture identity, fixed date, exactly like the counter's contract) and ran the reference tool from my
   clone — with `--verbose` on the five fixtures whose modules claim a verbose/index path — plus a scratch COPY of
   the tool with the single-line U5 (resp. U6) replacement, to observe the declared silence direction directly.

## 2. Fixture-by-fixture: does each demonstrate the `:88` behaviour in a realistic shape?

All 14 fixtures: reference `rc=1`, defect set exactly the declared singleton. Counter: `wrong=0` over 33; probe
reproduces every row. `hits=7` for each mutant (all 7 U5 fixtures, all 7 U6 fixtures kill — no single point of
failure); both mutants `killed by=… attributed=L522 value=differs`.

| fixture | shape (realism evidence) | ref observed | probe mutant |
|---|---|---|---|
| u5_short_a-manifest-registry | 6 rows / 3 commits; url-task binding via `task.toml` slugs + `SHA256SUMS` beside each capture; defect is a one-digit truncation of a manifest-listed capture's digest (S205, 63-hex) — the S110 shape | `DEFECT S205 … class=digest-short detail=63-hex`, `rows=6 tokens=3 defects=1` | rc=1 `classes=['digest-long']` |
| u5_short_a-index-staged | `--evidence-ref index` over a seed commit; capture + registry staged, never committed — the exact seat state the tool advertises that ref for; 16-hex token prefixes nothing (module guards this with a ValueError check) | `DEFECT S210 token=0123456789abcdef class=digest-short detail=16-hex` | rc=1 `classes=['digest-long']` |
| u5_short_a-abbrev-neighbour | 2 commits; same anchor cell carries a resolving `sha256 <12hex>…` abbreviation AND a 63-hex truncation; `--verbose` claim verified: `ABBREV S220 prefix=fa5cd97fb107 matches=fa5cd97fb1076e10…` printed, then `DEFECT S220 … class=digest-short` — the class comes from the length branch, not the abbrev branch | as left | rc=1 `classes=['digest-long']` |
| u5_short_b-registry-url-task | 6-row registry, url-task binding; defect token `"e"*63` (constant, not a truncation — see §4 observation O1) | `DEFECT S138 … class=digest-short detail=63-hex`, `rows=6 tokens=2 defects=1` | rc=1 `classes=['digest-long']` |
| u5_short_b-index-ref-staged | staged-only capture under `--evidence-ref index`; 8-hex token at the short boundary | `DEFECT S202 token=0badc0de class=digest-short detail=8-hex` | rc=1 `classes=['digest-long']` |
| u5_short_b-lane-path-manifest | 9 rows, `--verbose`; a STALE `SHA256SUMS` entry legitimately resolves S301 (probe: `RESOLVED S301 … via=…/report.md bind=row-path listed=…/SHA256SUMS:report.md`); defect is a 40-hex (git-sha1-length) paste S302 | `DEFECT S302 … detail=40-hex`, `rows=9 tokens=2 defects=1` | rc=1 `classes=['digest-long']` |
| u5_short_b-history-truncation | 2 commits: row correct (64-hex, resolves) at c1, truncated to 20-hex by a later review commit | `DEFECT S400 … detail=20-hex`, `rows=2 tokens=1 defects=1` | rc=1 `classes=['digest-long']` |
| u6_long_a-registry-65 | 5-row registry; defect token = the row capture's TRUE digest + one digit (probe shows the 65-hex token starting `95269be6877152cc…ff7`) — validates the docstring claim that length alone decides, not membership | `DEFECT S963 … class=digest-long detail=65-hex`; 4 clean rows `RESOLVED`, `rows=5 tokens=5 defects=1` | rc=1 `classes=['digest-short']` |
| u6_long_a-manifest-96 | capture exists only as a `SHA256SUMS` entry (`bulk.bin` never committed); row binds through the manifest; 96-hex token | `DEFECT S971 … class=digest-long detail=96-hex`, `rows=1 tokens=1 defects=1` | rc=1 `classes=['digest-short']` |
| u6_long_a-provenance-128 | row names no path/URL; binds via PROVENANCE.md table (`bind=provenance-row` in probe); 128-hex (sha512-length paste) beside a clean sibling row from the same table | `DEFECT S981 … class=digest-long detail=128-hex`, `rows=2 tokens=2 defects=1` | rc=1 `classes=['digest-short']` |
| u6_long_a-history-200 | 2 commits; clean 64-hex row first, 200-hex row appended later — no upper bound on the label | `DEFECT S992 … class=digest-long detail=200-hex` | rc=1 `classes=['digest-short']` |
| u6_long_b-registry-80hex | 5-row otherwise-green registry with a `SHA256SUMS` listing all five captures; 80-hex paste on S702 | `DEFECT S702 … class=digest-long detail=80-hex`, `rows=5 tokens=5 defects=1` | rc=1 `classes=['digest-short']` |
| u6_long_b-provenance-129hex | 2 commits; second adds PROVENANCE.md and a provenance-bound row (no path/URL in the row — the only binding route), 129-hex odd length | `DEFECT S712 … class=digest-long detail=129-hex`, `rows=2 tokens=2 defects=1` | rc=1 `classes=['digest-short']` |
| u6_long_b-index-pair-96hex | anchor cell carries the capture's true 64-hex digest AND a 96-hex paste; read via `--evidence-ref index` where the capture is staged-only. Probe under `--verbose`: `RESOLVED S722 digest=f69cae79… via=corpus/evidence/r44b-index/late.md` then `DEFECT S722 … class=digest-long detail=96-hex`, `rows=2 tokens=3 defects=1` | as left | rc=1 `classes=['digest-short']` |

Every module docstring's shape claims matched observation, including the two path-exercising claims
(`--verbose` abbreviation note in u5_short_a; stale-manifest + index resolution above).

## 3. Honesty of `defects`/`expect`

Machine-checked twice. Counter: `FIXTURE … declared=… observed=… ok` for all 14 target fixtures and
`BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0`. Probe: all 14 rebuilt from scratch reproduce `rc=1` with
exactly the declared singleton class set; `expect=reject` matches exit 1. The declared direction `silence` is real:
my scratch-copy mutant runs print the flipped class with the SAME exit status 1 on every fixture (U5: digest-long;
U6: digest-short), i.e. only the label betrays the mutant — as declared in MUTANTS (`round44_c1_verify.py:231-240`)
and in both u6 module docstrings ("the kill is silent (same exit status, different class set)").

## 4. Re-spelling check against `witness/w_u.py`

`w_u.py` anchor fixtures are bare: one row, one capture, `u5_short` token `DIG[:63]`, `u6_long` token `DIG+"a"`
(`lane(ctx,d,…)` helper, argv `["--lane", str(r)]`). None of the 14 reviewed fixtures is that shape: all are
multi-row (2-9 rows) and/or multi-commit, and each reaches the labelled token through a different real binding
route (url-task, row-path+SHA256SUMS, stale-manifest, provenance-row, staged-index) with different token lengths
(8/16/20/40/63 | 65/80/96/128/129/200). My own reading agrees with the integration shape-diff
(`shape-diff-battery44.txt`): fixture-vs-witness best 0.224-0.425 across the four modules, threshold 0.80,
`flagged=0`; only the row-FORMATTER helpers score high (`u5_short_a:row` 0.977, `u6_long_a:row` 0.965,
`u6_long_b:row` 0.944, `u5_short_b:_row` 0.853 vs witness `row`) — that similarity is dictated by the tool's
census contract (`NCELLS=11`, `ANCHOR_CELL=5`), is advisory in the diff, and carries no fixture logic. No module
imports or reads anything but `hashlib` (`grep "^import\|^from"`: one line each); none references the witness or a
sibling battery module.

## 5. Counter run — pasted lines (envelope)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44RRevBatAnc1/env /fast/scratch/hyaku/kengaku-r44/R44RRevBatAnc1/env --bind /fast/scratch/hyaku/kengaku-r44/R44RRevBatAnc1/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /fast/scratch/…/lane/plans/round44_c1_verify.py --lane /fast/scratch/…/lane --battery-dir /fast/scratch/…/lane/plans/battery44 --only U5,U6 --work /fast/scratch/…/w
ENVELOPE start 20:50:57 cwd=/fast/scratch/hyaku/kengaku-r44/R44RRevBatAnc1
PINS total=2 mismatched=0
MUTANT U5 anchor silence killed by=u5_short_a-manifest-registry attributed=L522 value=differs hits=7 -- plans/anchor_digest_check.py:88 '…
MUTANT U6 anchor silence killed by=u6_long_a-registry-65 attributed=L522 value=differs hits=7 -- plans/anchor_digest_check.py:88 '…
BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=2/2 order=0/0
ADVERTISED direct=2 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:51:00 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

(The 14 `FIXTURE … ok` lines are in the receipt; elided here for brevity.) Probe run: same envelope,
`ENVELOPE start 20:52:13 … end 20:52:16 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f
unchanged`. Both measurements count (digest unchanged). Sidechannel scan of the four modules against the counter's
token list: no hits (`grep -inE` over the 33 tokens, case-insensitive), consistent with the counter's
`sidechannel=0`.

## 6. Findings by severity

No blocking or major findings. Observations (non-blocking):

- **O1 (minor, cosmetic):** `u5_short_b-registry-url-task`'s defect token is the constant `"e"*63`, not a
  truncation of a real digest — the S110 shape is a truncation (tool docstring :85-87). Not a defect: the module's
  other fixtures cover true truncations (63-hex S205, 20-hex S400), and a constant token sharpens the
  length-alone property of the `:88` label; the registry shape itself (url-task binding, manifest) is realistic.
- **O2 (minor, cosmetic):** `u6_long_a-history-200`'s 200-hex token is longer than any plausible digest paste; it
  demonstrates only that the label has no upper bound. Neighbouring fixtures already carry realistic long-paste
  lengths (65/80/96/128/129), so the fixture adds coverage, not realism.

## 7. Residual risk and verification gaps

- The declared direction is `silence`: any consumer keying on exit code alone cannot distinguish mutant from
  reference; the class set is the only observable. This is the frozen pricing, honestly declared — not a module
  defect.
- I verified the two anchor mutants (U5, U6) and the 14 anchor fixtures of my scope only; U7/U9/U14c modules and
  the order tool are other seats' scope. I ran the counter in development mode (`PREDICATE C1 n/a`); the landing
  predicate run itself was measured by the L1 (`MUTANTS total=5 killed=5 … PREDICATE C1 pass`).
- `PINS total=2 mismatched=0` confirms my clone's tools equal the frozen digests, so this review's surface is the
  frozen surface.
- Scratch `S=/fast/scratch/hyaku/kengaku-r44/R44RRevBatAnc1` removed after receipt copy; receipts live at
  `R44RRevBatAnc1/counter-u5u6-run1.txt` (sha256 `8de94ef21b8a9d1bf405f3cdc77537aa777fa72e15ea801101401f191312d57a`,
  5126 B) and `R44RRevBatAnc1/probe-run1.txt` (sha256 `f37eb0abdb7ea0fa82bfabae3c2e1b934f8776279e20da8cd1466dd860cc0130`,
  7238 B), both well under 1 MiB.

All four modules honest: every fixture demonstrates the advertised `:88` short/long label through a distinct,
realistic binding route; `defects`/`expect` exact under both machine checks and my independent rebuild; none is a
re-spelling of the witness.

VERDICT: anchor-modules-1-honest-4/4
