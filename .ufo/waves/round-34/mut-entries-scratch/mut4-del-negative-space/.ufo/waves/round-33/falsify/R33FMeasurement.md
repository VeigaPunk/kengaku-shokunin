# R33FMeasurement — frozen-counter measurement at tip (round 33, 2026-10-25)

Seat: R33FMeasurement (leaf executor, measurement lane). No lane/fleet files edited,
committed, or staged by this seat; all probes ran in a fresh `/tmp` sandbox
(`/tmp/r33meas/fleet/kengaku-shokunin`, `git clone --no-hardlinks` of lane HEAD).
Lane repo: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## 0. Scope and method

Assignment: run the exact frozen measurement commands at current tip, report exact
exit/output, compare with the committed after receipts, do not edit.

- Tip: `HEAD = 77ac8c1307ba60e9572a7e2789b71ae31b133440`.
- Working tree at measurement time already had (pre-existing, untouched by this seat):
  `M SCORECARD.md`, `D .ufo/waves/round-33/assimilation/append-package.md`,
  `D .ufo/waves/round-33/assimilation/quotes-rows.txt`, plus untracked build/falsify
  wave artifacts. `git status --porcelain` re-run after all measurements is identical —
  this seat changed no tracked file.
- Each command was run twice at tip and output was byte-identical (deterministic).

## 1. C1 — coverage (adoption_check + round33_c1_verify)

Frozen command 1:
`python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census`

Observed at tip (twice, identical):

```
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
EXIT=0
```

Matches the frozen predicate exactly (`entries=1 indexed=1 cited_rows=3 rows_present=3
rows_mined=3 usedby_ok=1 census=ok` exits 0).

Expect-file digest matches the committed control's pinned digest:
`sha256(adoption-expect.json) = fbd7b47ededdfe251465c13ee1c2b758453f2b691bc0639d8a74df3e0752a214`
(control-nothing.txt `expect_sha256=fbd7b47e…`). The do-nothing control itself exits 1
as recorded (`entries=1 … rows_mined=1 usedby_ok=0 census=ok`, exit 1).

Frozen command 2 (content-level second receipt):
`python3 plans/round33_c1_verify.py --lane .` → `checks=8 defects=0`, exit 0. Matches.

**Comparison to committed after receipt: none exists.** `corpus/evidence/round33/` holds
only `defects-after.txt` and `catalogs/`. The committed SCORECARD round-33 section at HEAD
ends with "measurements follow at landing."; the after values for C1 (and the score
verdicts) exist only in the **uncommitted** working-tree edit of SCORECARD.md. So C1's
"after" state is not recorded at tip — the counter re-runs green, but the landed receipt
is absent.

Host/portability coupling: the census clause hardcodes
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` and derives root = lane parent,
lane name = lane dir minus `-shokunin`. On a clean clone placed under
`/tmp/r33meas/fleet/kengaku-shokunin` with the real conf copied but
`SHOKUNIN_ROOT`/lane paths pointed at the sandbox, C1 prints the same line and exits 0.
On a pure lane clone without the host fleet conf, C1 exits 1 with `census=fail`. The
`exit 0` is therefore reproducible only inside the host fleet layout.

Probe (sandbox): mutating a cited `source:` line S103→S999 flips adoption to
`rows_present=2 rows_mined=2 …` exit 1, and c1_verify to `DEFECT V2 …` `checks=8
defects=1` exit 1. Both counters catch source/identity tamper.

## 2. C2 — calibration (round33_defects)

Frozen command: `python3 plans/round33_defects.py --lane .`

Observed at tip (twice, identical):

```
checks=6 defects=0
EXIT=0
```

Matches committed after receipt `corpus/evidence/round33/defects-after.txt`
(`checks=6 defects=0`, `exit=0`). Note the receipt's header pins revision `c227e486`;
tip is `77ac8c1` — the counter re-derives green at the newer tip, so the receipt holds
but its revision label is a snapshot, not the current tip.

Probes (sandbox): adding one untracked file under `.ufo/waves/round-32/` →
`DEFECT N1 …` `checks=6 defects=1` exit 1; removal restores exit 0. N1 is live.

Host/portability coupling: N3/N4 read absolute host fleet report paths
(`/home/vgpnk/Projects/shokunin/.ufo/reports/round-31/kengaku.md`,
`round-32/kengaku.md`) with no override flag. Masking the host reports via a
bind-mount in a private mount namespace (no persistent change) made N3/N4 fail:
`checks=6 defects=2`, exit 1. C2's green depends on the host fleet reports existing at
that absolute path; a lane-only checkout would fail N3/N4.

## 3. C3 — freshness (catalog_probe --verify)

Frozen command: `python3 plans/catalog_probe.py --verify --lane .`

Observed at tip (twice, identical):

```
raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok
HF missing fields: author, sha, lastModified, gated
EXIT=0
```

Matches the committed receipt `corpus/evidence/round33/catalogs/after.txt`:
`hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0`, and the committed
`SHA256SUMS` digests verify against the raw files on disk (`96aba4d1…`, `9755544573…`).
`--verify` is offline by construction (its code path reads only committed bytes; the
network `fetch` helper is used only by `--capture`/probe).

**Receipt-vs-tip discrepancy:** `after.txt` records `entry=pending`, but the tip entry
`corpus/knowledge/open-model-catalogs.md` carries the `## Re-probe 2026-10-25 (round
33)` block (added in commit 66c734c, after the receipt was committed at b54feca).
`--verify` validates only the four numeric tokens and the block's presence in the entry;
it does not validate the receipt's own `entry=` token, so the stale `entry=pending`
line passes silently. The receipt is not false (numbers re-derive), but its
self-description is stale at tip.

Probes (sandbox):
- Byte flip in `hf.raw.json` → `raw=invalid digest mismatch …` exit 1. Digest check binds.
- Oversize raw (68 KiB, digest updated to match) → exit 1 (`exceeds the 65536-byte
  bound`).
- Receipt token tolerance: rewrite `hf_models=50` → `hf_models=500` in after.txt still
  exits 0 (the check is substring containment: `hf_models=50` ⊂ `hf_models=500`);
  rewrite to `hf_models=5` exits 1 (`receipt-mismatch missing:hf_models=50`). The
  receipt comparison tolerates appended digits but not deletion of the true count.
- Removing the entry block → `raw=ok entry-mismatch missing:## Re-probe …` exit 1.

## 4. Verdict

| item | verdict | basis |
|---|---|---|
| C1 adoption_check at tip | pass | exact line + exit 0, twice; expect digest matches pinned control |
| C1 round33_c1_verify at tip | pass | `checks=8 defects=0`, exit 0 |
| C1 committed after receipt | **absent** | no adoption-after receipt anywhere under `corpus/evidence/round33/`; committed SCORECARD still says "measurements follow at landing."; after row exists only in uncommitted working tree |
| C2 round33_defects at tip | pass | `checks=6 defects=0`, exit 0, matches defects-after.txt |
| C3 catalog_probe --verify at tip | pass | exact line + exit 0, digest-verified raw bytes, numbers re-derive from bytes |
| C3 after.txt self-description | stale | `entry=pending` vs tip entry block; verify ignores its own `entry=` token |
| Environment coupling | limitation | C1 census and C2 N3/N4 hardcode host fleet paths; green not reproducible on a lane-only checkout |
| Counter sensitivity (spot probes) | ok | C1 source mutation caught; C2 N1 untracked caught; C3 tamper/oversize/block-removal caught; receipt numeric match is substring-based (tolerates appended digits) |

No frozen claim was falsified by the measurement runs themselves: all three counters
print the frozen lines and exit 0 at tip. Reported limitations are receipt
self-description staleness, the missing committed C1 after receipt, host-path
coupling of C1's census and C2's N3/N4, and the substring-based receipt-token
comparison in C3's `--verify`.

## 5. Exact evidence retained

- Tip: `77ac8c1307ba60e9572a7e2789b71ae31b133440`.
- C1: 2× `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` / exit 0; `checks=8 defects=0` / exit 0.
- C2: 2× `checks=6 defects=0` / exit 0.
- C3: 2× `raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok` + HF-missing-fields line / exit 0.
- Sandbox: clean clone of HEAD (77ac8c1); probes as described; `git status` clean before/after each probe.
- No installs performed (no tooling directive action needed).

## L1 integration correction

After this measurement snapshot, `corpus/evidence/round33/adoption-after.txt` was added with both C1 outputs; `defects-after.txt`'s revision pointer was corrected from `c227e486` to the actual repair commit `7895588`; and `after.txt` now explains `entry=pending` as a capture-stage marker with the later entry block verified. The C1 verifier's V8 column index was also corrected (`teaches` is `row[6]`) and a red/green regression fixture added; its frozen lane command remains `checks=8 defects=0`.
