# R33FGateAttest — `--attest-opened` opened-date attestation bypass

Seat: leaf, lane `kengaku-shokunin`, round 33 (hyaku run 7), 2026-10-25.
Target: the `--attest-opened` path in `plans/sources_adopt.py`.
Frozen claim attacked: C1 (round-33-claims.md, frozen predicate) — the three cited rows
`corpus/SOURCES.md` carry `status=mined`, `opened=2026-10-25`.
Verdict: **CAUGHT** — the flag re-dates a stale/unfetched row's `opened` cell to
`--access-date` with **no fetch, no network, no artifact, no clock check, and no per-row
record**; it is silently ignored in several invocation shapes; and it is structurally
unable to run in the same invocation as the quote/artifact pass. An `opened=2026-10-25`
row therefore does not attest any 2026-10-25 fetch. (Build report R33C1KillRule.md item 10
listed this as UNCAUGHT "guarded by flag"; this seat supplies the measured evidence and the
three additional bypass shapes.)

All fixtures and runs lived in `/tmp/r33-R33FGateAttest/`; no lane file, git/jj state, or
index was touched. No tools installed (host `python3` 3.14.8; `strace`/`unshare` already
present). Lane git state untouched.

## 1. The code path (verified by read/grep)

- `--attest-opened` is defined once: `parser.add_argument("--attest-opened", action="store_true", help=...)` (lines 1004-1008), passed to `build_block` at line 1063, and printed as a blanket line at 1065-1067.
- `build_block` (lines 164-172):

  ```python
  # A row is appended only if it was opened this round and is already mined.
  # The gate cannot verify a fetch, so re-dating a staged `opened` cell requires
  # an explicit attestation; silently stamping it would launder a stale row.
  if cells[7] != "mined":
      return [], [], [f"{row_id}:not-mined"]
  if cells[8] != access_date:
      if not attest_opened:
          return [], [], [f"{row_id}:not-opened-this-round"]
      cells[8] = access_date
  ```

- The module imports only `argparse, contextlib, io, json, re, sys, tempfile, pathlib` — **no socket/urllib/requests/http/ssl**; `grep` for `mtime|stat(|fetch|urllib|socket|http\.|requests` finds only comments saying "the gate cannot verify a fetch" (lines 165-166, 343).

## 2. Attack 1 — stale row accepted, emitted block re-dated (exit 0)

Fixture: `/tmp/r33-R33FGateAttest/` — `registry.md` (1 row S800), `package.md` (S900 fresh, S901 stale opened 2026-10-19, S902 future, S903 queued). Row schema 11 cells per HEADER, source URL `https://example.invalid/never-fetched`.

```
$ python3 plans/sources_adopt.py --registry /tmp/r33-R33FGateAttest/registry.md --package /tmp/r33-R33FGateAttest/package.md \
    --admit-ids S901 --entries corpus/knowledge/x.md --access-date 2026-10-25
registry=1 staged=4 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
  missing: S901:not-opened-this-round
EXIT=5
```

Same command with the flag:

```
$ python3 plans/sources_adopt.py … --admit-ids S901 … --access-date 2026-10-25 --attest-opened --out /tmp/r33-R33FGateAttest/out-attested.md
registry=1 staged=4 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
  attested: the caller asserts every requested source was opened on 2026-10-25
wrote /tmp/r33-R33FGateAttest/out-attested.md rows=1
EXIT=0
```

Emitted block (opened rewritten 2026-10-19 → 2026-10-25):

```
| S901 | fixture source — https://example.invalid/never-fetched | docs | A | fixture scope | doc "quoted sentence from the capture" (5 words) | fixture teaches | mined | 2026-10-25 | 180d | corpus/knowledge/x.md |
```

The source URL is a permanently-unresolvable domain; no fetch was or could be attempted; the
row is admitted.

## 3. Attack 2 — succeeds with zero network capability

```
$ unshare -rn python3 plans/sources_adopt.py --package /tmp/r33-R33FGateAttest/package.md --registry /tmp/r33-R33FGateAttest/registry.md \
    --admit-ids S901 --entries corpus/knowledge/x.md --access-date 2026-10-25 --attest-opened
registry=1 staged=4 … prose=0
  attested: the caller asserts every requested source was opened on 2026-10-25
| S901 | … | mined | 2026-10-25 | …
EXIT=0
```

`unshare -rn` (empty network namespace) was verified to work on this host first
(`unshare -rn python3 -c 'print("netns-ok")'` → netns-ok), so the gate ran with **no
network interfaces at all** and still attested the fetch.

`strace -f -qq -e trace=%network` over the same run: **0 network syscalls, 0-byte log**
(exit 0). The gate never touches the network, in any mode.

## 4. Attack 3 — a row with *no* opened date is stamped

`package2.md` row S910 has an empty `opened` cell. Without the flag: `missing: S910:not-opened-this-round`, exit 5. With the flag:

```
… --admit-ids S910 … --attest-opened --out out-empty.md
  attested: the caller asserts every requested source was opened on 2026-10-25
EXIT=0
```

Emitted: `| S910 | … | mined | 2026-10-25 | 180d | corpus/knowledge/x.md |` — a row that
never had any opened date at all is now "opened 2026-10-25". Note `row_defects` never
checks the `opened` cell (only status/recheck/source), so the empty cell is defect-free.

## 5. Attack 4 — re-date is free in both directions; no clock check

- Future row S902 `opened=2026-12-31` + `--access-date 2026-10-25 --attest-opened` → **backwards** re-date to 2026-10-25, exit 0.
- `--access-date 2030-01-01` (system date is 2026-10-25) → emitted `opened` cell is `2030-01-01`, exit 0. The only validation on `--access-date` is the ISO regex `^\d{4}-\d{2}-\d{2}$` (line ~1054); it is never compared to the system clock, so "asserts … was opened on --access-date" is satisfiable with a future date.

## 6. Attack 5 — blanket message, no per-row record, mixed batch undistinguished

With `--admit-ids S900,S901` (S900 already fresh, S901 stale) the output is:

```
  attested: the caller asserts every requested source was opened on 2026-10-25
wrote … rows=2
EXIT=0
```

The block contains both rows with `opened=2026-10-25`. The printed line names **no ids**,
and neither stdout nor the block records which rows were actually re-dated vs already fresh.
The attached audit trail cannot reconstruct what the attestation did — the only evidence is
the caller's own flag.

## 7. Attack 6 — the flag is silently ignored in three invocation shapes

The module's own standard for flags a run ignores is line ~1034: "A flag the run ignores is worse than a refused one" (written for `--url-map`, which is `parser.error`d when given without quote mode). `--attest-opened` violates that standard:

- **Quote mode:** `--quote-file … --artifact … --url-map … --attest-opened` → runs the quote pass, prints `ok S901 …`, **exit 0**, attestation silently dropped (no error, no line).
- **No `--admit-ids`:** `--registry … --package … --attest-opened` → `registry=1 staged=4 …`, exit 0, no "attested:" line, no block. A fully green run that did nothing.
- **`--selftest`:** `--selftest --attest-opened` → `SELFTEST cases=17 failed=0`, exit 0, flag ignored.

All three exit 0, so an operator cannot tell the flag was inert.

## 8. Attack 7 — attestation is structurally isolated from quote/capture evidence

The only mode that could tie the row's bytes to a fetch is the quote pass, and it is
**exclusive** with the registry pass:

```
$ python3 plans/sources_adopt.py --registry … --package … --quote-file … --artifact … --url-map … \
    --admit-ids S901 --entries … --access-date 2026-10-25 --attest-opened
sources_adopt.py: error: --quote-file/--artifact cannot be combined with --registry/--package
EXIT=2
```

And the quote pass is date-blind: `capture.txt` (sha256 `b151b15e105ca7e5f4e7d00ec189fba8ac9792c5feae1567e68a750686b58afc`) with mtime **2020-01-01T00:00:00Z** passes as a located/bound capture for a row claiming `opened=2026-10-25`:

```
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=capture.txt mismatch=0 unmapped=0 urlmap=url-map.json entries=1
  ok S901 words=5 at capture.txt quote="quoted sentence from the capture" bound=capture.txt->https://example.invalid/doc
EXIT=0
```

So the full stale pipeline is green: a 2020 capture validates the quote (exit 0), and a
2026-10-19 row is re-dated to 2026-10-25 (exit 0). Nothing in the gate observes the other
half.

## 9. Attack 8 — side effect: attestation can mint an incoherent overdue row

Row S911 (stale opened, `recheck=2026-01-01`, a valid ISO date) with the flag:

```
| S911 | … | mined | 2026-10-25 | 2026-01-01 | corpus/knowledge/x.md |
EXIT=0
```

The past ISO recheck is preserved (only prose rechecks are normalized, line 174-178), so the
emitted row is `recheck 2026-01-01` on `opened 2026-10-25` — 297 days overdue the moment it
is appended.

## 10. What the flag does NOT bypass (scope limits)

- `status != mined` still refuses even with the flag: `missing: S903:not-mined`, exit 5 (attestation only bypasses the opened-date guard, not the status guard).
- A missing requested id still refuses (`missing: S105`, exit 5); collisions/duplicates/malformed are unaffected; the quote mode's exit 6/7/8/9 paths are unaffected.
- `--selftest` pins the re-date behavior: case `prose-recheck-normalized` asserts `stale_missing == ["S014:not-opened-this-round"]` without the flag and `not stale_ok` / opened rewrite with it (lines 706-719). The bypass is **documented, intended behavior** — the falsification is of C1's *semantics* ("opened=2026-10-25" ⇒ opened this round), not of the gate against its own selftest.

## 11. Reproduction (exact)

```bash
D=/tmp/r33-R33FGateAttest                       # fixtures therein; sha256 at end
python3 plans/sources_adopt.py --registry $D/registry.md --package $D/package.md \
  --admit-ids S901 --entries corpus/knowledge/x.md --access-date 2026-10-25
python3 plans/sources_adopt.py --registry $D/registry.md --package $D/package.md \
  --admit-ids S901 --entries corpus/knowledge/x.md --access-date 2026-10-25 --attest-opened
unshare -rn python3 plans/sources_adopt.py --registry $D/registry.md --package $D/package.md \
  --admit-ids S901 --entries corpus/knowledge/x.md --access-date 2026-10-25 --attest-opened
strace -f -qq -e trace=%network -o /tmp/net.log python3 plans/sources_adopt.py --registry $D/registry.md \
  --package $D/package.md --admit-ids S901 --entries corpus/knowledge/x.md --access-date 2026-10-25 \
  --attest-opened --out $D/out-strace.md && wc -c /tmp/net.log
python3 plans/sources_adopt.py --quote-file $D/quote-rows.md --artifact $D/capture.txt --url-map $D/url-map.json
```

Fixture sha256 (all under `/tmp/r33-R33FGateAttest/`): `registry.md 6f401e1d…`, `package.md 71b8304482…`, `package2.md 5db1dd93d7…`, `quote-rows.md 933cd825b8…`, `url-map.json b445183c01…`, `capture.txt b151b15e10…` (mtime 2020-01-01T00:00:00Z), `out-attested.md b168945aa793…`.

## 12. Findings

| # | finding | status |
|---|---|---|
| 1 | Stale row S901 (opened 2026-10-19) admitted as opened 2026-10-25 under `--attest-opened`, exit 0 | **CAUGHT** |
| 2 | Attestation succeeds in an empty network namespace (unshare -rn) with 0 network syscalls (strace) — no fetch exists | **CAUGHT** |
| 3 | Empty `opened` cell stamped without a flag? no; with flag yes, exit 0 | **CAUGHT** |
| 4 | Re-date allowed backwards (future → past) and to a future access-date; no clock check | **CAUGHT** |
| 5 | No per-row re-date record; blanket line only; mixed batches undistinguished | **CAUGHT** |
| 6 | Flag silently ignored (exit 0) in quote mode, without `--admit-ids`, and with `--selftest` | **CAUGHT** (inconsistent with the file's own `--url-map` refusal standard) |
| 7 | Registry pass and quote pass are mutually exclusive; quote pass is date-blind (2020 capture passes) — no invocation can bind `opened` to this round's bytes | **CAUGHT** (structural) |
| 8 | Attestation preserves a past ISO recheck → minted row overdue on append | limitation / side effect |
| 9 | `not-mined` still refused; id/collision/malformed/quote guards unaffected | scope limit (verifies the flag is scoped) |

## 13. Risks / hand-off notes for the L1

- C1's frozen predicate requires `opened=2026-10-25` only; `adoption_check.py` / `round33_c1_verify.py` count that cell and cannot distinguish an attestation-stamped stale row from a genuinely fetched one. If "opened this round" must mean something, the row carries no provenance for it — the flag is a self-assertion in prose.
- Suggested (not implemented here — this is a falsify wave): either refuse `--attest-opened` unless a quote/artifact pass ran on the same rows in the same invocation (the parse currently forbids combining), or record per-row attestation (ids re-dated, source URL, access date) in the block/report so the audit trail is reconstructable, or bind `opened` to fetch evidence (capture mtime/hash/url) instead of a caller assertion. Also decide whether the flag should be a refusal when given without `--admit-ids`/in quote mode, matching the `--url-map` precedent.
- S103/S104's real capture data (R33SourcesAdoptDry.md) is unaffected by this finding: those captures were re-fetched and hash-verified this round by that seat. The bypass is about what the *gate* guarantees, not about whether the lane's actual captures were fresh.
