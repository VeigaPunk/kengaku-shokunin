# C1ExecSelftest — audit of the R51-C1 counter's selftest

Seat: executor, kengaku round 51 (hyaku run 11), wave w1.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only).
Item: audit `python3 plans/round51_surfaces.py --selftest`; name the predicate leg each of
the 9 cases exercises; check each case really isolates that leg; propose and demonstrate
additional cases.

Axes named: **freshness** (R51-C1, `plans/round51_surfaces.py` selftest quality) — the
instrument that gates the C1 claim, not the claim's surface. No production file was touched.

## 0. Revision measured

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && git log --oneline -4
4090c3d round-51: v2 wave spec (64 seats) + validated dispatch payload
e07f131 round-51: stage-1 freeze — C1 surface-truth counter+manifest, C2 routing counter, claims, before receipts
297e179 round-50: receipt notes — the scratch FENCE path is not load-bearing, the committed digests are
fa16b87 round-50 verifier spot-check (integrator, hyaku): closure-tip note
```

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

`git status --porcelain` showed only untracked `.ufo/waves/...` wave directories; `plans/` is clean.
The instrument under audit is byte-identical to the stage-1 freeze commit
(`sha256 plans/round51_surfaces.py` = `edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e`).

## 1. Commands run and verbatim output

### 1.1 Frozen selftest (exit 0)

```
$ TMPDIR=/fast/scratch/hyaku/kengaku-r51/C1ExecSelftest python3 plans/round51_surfaces.py --selftest
...
[selftest] cases=9 failures=0
[selftest] ALL PASS
EXIT=0
```

The selftest runs `check()` once per case, so its own stdout is the per-case key attribution.
Counted from that capture: `grep -c 'PREDICATE R51-C1'` → **9**;
`grep -c 'SECTION-MISSING [1-9]'` → **0**; `grep -c 'UNCOVERED [1-9]'` → **3**;
`grep -c 'ANCHOR-DUP [1-9]'` → **1**.

Temp isolation is honoured (no `/tmp` hardcoding): a STALE detail in the capture reads
`missing: /fast/scratch/hyaku/kengaku-r51/C1ExecSelftest/r51surf-8phnmy16/nope-a`, and no
`r51surf-*` directory survived the run (`shutil.rmtree` in `finally` works).

### 1.2 Frozen counting command at the tip (unchanged from the before receipt)

```
$ python3 plans/round51_surfaces.py --lane .
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (...)
  DETAIL DRIFT SF02 prose=present state=absent (...)
  DETAIL DRIFT SF03 prose=present state=absent (...)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=1
```

This reproduces `.ufo/waves/round-51/claims/c1-before.txt` (`REV 297e179...`) exactly on every
counted line; the wave-spec commit did not move the reading.

## 2. The 9 cases: leg, isolation, and what the fixture actually proves

Predicate legs: DRIFT, STALE, UNVERDICTED, NUMBER-DRIFT, ANCHOR-DUP, ANCHOR-MISSING,
UNCOVERED, SECTION-MISSING, plus RESOLVE (floor).

| # | case | fixture | leg it is named for | other keys non-zero (measured) | only failing leg? |
|---|---|---|---|---|---|
| 1 | S0 | consistent doc, both entries present | none — baseline pass | none | n/a (pass case) |
| 2 | S1 | `prose=present`, `state=absent`, row carries `ABSENT 2026-10-28` | DRIFT | none | **yes** |
| 3 | S2 | `state=present`, probe path missing | STALE | none | **yes** |
| 4 | S3 | `state=absent`, `prose=absent`, row undated | UNVERDICTED | none | **yes** |
| 5 | S4 | `count_claim: 3` against `a.txt` (`rows=0`) | NUMBER-DRIFT | none | **yes** |
| 6 | S5 | extra row `\| Surface B \|` with no entry | UNCOVERED | none | **yes** |
| 7 | S6 | `GOOD_ROW` written twice | ANCHOR-DUP | `UNCOVERED 2` | **no** — collateral |
| 8 | S7 | both entries absent + dated, `floor=1`, `present=0` | RESOLVE (floor) | none | **yes** |
| 9 | S8 | entry anchor `\| Surface Z \|` absent from the doc | ANCHOR-MISSING | `UNCOVERED 1` | **no** — collateral |

So: **8 of the 9 predicate legs are exercised, 6 of them in isolation.** S0 exercises no leg.
S6 and S8 trip a second leg as a structural consequence (a duplicated or missing anchor leaves
its row unclaimed, which is by construction `UNCOVERED`), so those two fixtures cannot isolate
their leg without a code change — but see §4.1: the suite cannot tell either way.

**`SECTION-MISSING` is exercised by none of the 9 cases** (`SECTION-MISSING [1-9]` count = 0 in
the capture). It is the one leg with no fixture at all. §3 A6 supplies the pure case.

Probe-kind coverage of the real manifest (19 entries): `paths` 13, `sha256` 3, `count` 1,
`http` 1, `port` 1. The selftest only ever builds `paths` (8 cases) and `count` (1 case):
**`sha256`, `port` and `http` — 5 of the 19 real entries, 26% — are never exercised.**

## 3. Proposed additional cases, demonstrated against the frozen counter

Driver: `/fast/scratch/hyaku/kengaku-r51/C1ExecSelftest/probe_cases.py` (scratch only; removed at
yield). Each case is a fixture directory with its own `PROVINCE.md` + `m.json`; the **unmodified**
frozen counter is invoked as a subprocess with `--lane/--manifest/--province` on it. `expect` is
what a correct counter must print for that fixture.

### 3.1 Cases that make the current counter fail (valid selftest additions)

```
=== A1 sha256 stale pin
    expect=fail observed=fail exit=1 predicate='PREDICATE R51-C1 fail'
    keys={"STALE": 1}
    DETAIL STALE SF01 probe=absent state=present (digest 2d711642 does not start with pin 0000dead)

=== A2 http probe returns 500
    expect=fail observed=fail exit=1 predicate='PREDICATE R51-C1 fail'
    keys={"STALE": 1}
    DETAIL STALE SF01 probe=absent state=present (http://127.0.0.1:39209/v1/models -> HTTP Error 500: Internal Server Error)

=== A3 port probe on closed port 44999
    expect=fail observed=fail exit=1 predicate='PREDICATE R51-C1 fail'
    keys={"STALE": 1}
    DETAIL STALE SF01 probe=absent state=present (connect failed: [Errno 111] Connection refused)

=== A4 count probe on missing file
    expect=fail observed=fail exit=1 predicate='PREDICATE R51-C1 fail'
    keys={"STALE": 1, "NUMBER-DRIFT": 1}
    DETAIL STALE SF01 probe=absent state=present (missing corpus/registry.md)
    DETAIL NUMBER-DRIFT SF01 row claims 5, probe says missing corpus/registry.md

=== A5 anchor sits in the wrong section
    expect=fail observed=fail exit=1 predicate='PREDICATE R51-C1 fail'
    keys={"ANCHOR-MISSING": 1, "UNCOVERED": 1}
    DETAIL ANCHOR-MISSING SF02 anchor not found: | Surface B |
    DETAIL UNCOVERED ## Surfaces row line 8 has no manifest entry

=== A6 declared section with no table
    expect=fail observed=fail exit=1 predicate='PREDICATE R51-C1 fail'
    keys={"SECTION-MISSING": 1}
    DETAIL SECTION-MISSING section '### Core' has no table rows

=== A7 section heading absent
    expect=fail observed=fail exit=1 predicate='PREDICATE R51-C1 fail'
    keys={"ANCHOR-MISSING": 1, "SECTION-MISSING": 1}
    DETAIL ANCHOR-MISSING SF01 anchor not found: | Surface A |
    DETAIL SECTION-MISSING section '## Surfaces' has no table rows

=== A8a floor equality floor=2 present=2
    expect=pass observed=pass exit=0 predicate='PREDICATE R51-C1 pass'
    keys={}
    RESOLVE observed_present=2 floor=2 verdict=met

=== A8b floor floor=3 present=2
    expect=fail observed=fail exit=1 predicate='PREDICATE R51-C1 fail'
    keys={}
    RESOLVE observed_present=2 floor=3 verdict=violated
```

Notes that matter for the suite's value:
- **A1/A2/A3 are pure `STALE` cases for the three untested probe kinds** — each fires exactly one
  leg, and each is a distinct real-world failure (stale digest pin, dead endpoint answering 500,
  port not listening). A2 is the case the claims' own §Limits describes ("`:34113` may return",
  i.e. the endpoint can change state) with no selftest fixture behind it.
- **A4 is the only case that shows the two count-probe outcomes are conflated**: an unreadable
  target trips `STALE` *and* `NUMBER-DRIFT`, because the probe reports `absent` and the number
  comparison then reads the word `missing` for digits. See §4.3.
- **A6 is the missing `SECTION-MISSING` case and it is pure** — `keys={"SECTION-MISSING": 1}` with
  every other leg at 0. The 9-case suite has no equivalent.
- **A8a/A8b pin the floor boundary** (equality is `met`, one below is `violated`). S7 only pins the
  violated side; a `>=` → `>` regression would survive the current suite.
- A5 is `ANCHOR-MISSING` + `UNCOVERED` — same inherent coupling as S8, but it covers a distinct
  shape the suite lacks: the anchor *does* exist in the document, just in another section.

### 3.2 Cases the current counter **passes** that a correct counter must fail (defects)

```
=== A9 section with no table borrows next section's rows
    expect=fail observed=pass exit=0 predicate='PREDICATE R51-C1 pass'
    keys={}
    RESOLVE observed_present=2 floor=1 verdict=met

=== A10 count_claim equals a digit run in the missing path
    expect=fail observed=pass exit=0 predicate='PREDICATE R51-C1 pass'
    keys={}
    RESOLVE observed_present=1 floor=1 verdict=met

=== A11 ABSENT marker with invalid ISO date 2026-13-99
    expect=fail observed=pass exit=0 predicate='PREDICATE R51-C1 pass'
    keys={}
    RESOLVE observed_present=1 floor=1 verdict=met

=== A12 unknown probe kind
    expect=fail-with-predicate-line observed=ABORT exit=1 predicate='NO-PREDICATE-LINE'
    keys={}
    stderr_tail=unknown probe kind 'carrier-pigeon'

PROPOSED cases=13 mismatched_expectations=3
```

(The three mismatches are A9/A10/A11; A12 is counted as satisfied by the driver's rule but is a
defect in its own right — see §4.6.)

## 4. Findings against the selftest and the legs it is supposed to protect

### 4.1 `expect_key` is dead: the suite asserts exit codes, never leg attribution (high)

`def run(expect_ok, expect_key=None)` (line 250) never reads `expect_key`; no call site passes it.
Every case therefore asserts only "exit 0" or "exit != 0". Because the predicate is a conjunction
over all keys, **any mutation that swaps which key a leg reports leaves all nine exit codes
unchanged**. Demonstrated with a scratch copy of the frozen counter
(`sha256` differs from the lane file only in one line):

```
# M1: DRIFT's append retargeted to problems["STALE"]
$ python3 mut_key_swap.py --selftest
[selftest] cases=9 failures=0
[selftest] ALL PASS

# M1 against the real lane manifest
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
DRIFT 0
STALE 3
UNVERDICTED 1
NUMBER-DRIFT 1
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

The receipt's headline `DRIFT 3` became `STALE 3` and the selftest still reports `ALL PASS`.
The consequence is direct: **the before/after receipts quote per-key counts (`DRIFT 3`,
`UNVERDICTED 1`, `NUMBER-DRIFT 1`), and the selftest pins none of them** — it pins only the
boolean, which those keys feed.

Contrast — a leg *deletion* is caught, because it flips an exit code:

```
# M2: `if e["prose"] != e["state"]:` -> `if False:`
$ python3 mut_leg_deleted.py --selftest
[selftest] cases=9 failures=1
[selftest] FAIL case 2 expected fail, got pass
[selftest] FAILED
```

So the suite's protection is exactly one bit per leg, and at the after-target state (all keys 0)
even that bit is gone: with every leg at zero, a key swap and a leg deletion are both invisible.
Fix: pass `expect_key` at every call site and assert the *set* of non-zero keys equals the
expected set (which also documents S6/S8's inherent coupling instead of hiding it).

### 4.2 `SECTION-MISSING` has no case, and the section-heading leak makes it unreachable where it matters (high)

`section_rows()` skips any heading line it meets *before* the first row of its own section
(`if line.startswith("#"): if started: break; continue`). A declared section that has no table of
its own therefore silently borrows the next section's table — and `SECTION-MISSING`, which exists
precisely for that shape (`if not rows: problems["SECTION-MISSING"]...`), never fires. Measured:

```
# A9: "## Surfaces" heading with no table, followed by "### Core" and its table
expect=fail observed=pass exit=0
PREDICATE R51-C1 pass
```

The counter accepts a document where a declared section has no table at all, and it accepts an
entry anchored to a row that belongs to another section. A6 shows the leg can fire, so the leg is
implemented; it is just bypassed. Fix: bound the scan at the next heading unconditionally, and add
A6 (pure) plus A9 (leak) as selftest cases.

### 4.3 `NUMBER-DRIFT` compares a scraped digit run, not a count (high)

```python
m = re.search(r"(\d+)", detail)
if not m or int(m.group(1)) != int(e["count_claim"]):
```

`detail` for a count probe is `"%s=%d" % (label, n)` when readable and `"missing %s" % target`
when not. Taking the **first** digit run means (a) a `label` containing digits (`v2rows=7`)
compares `2` against the claim, and (b) a missing target whose path contains digits satisfies the
claim outright. Measured (b):

```
# A10: count target "corpus/round51/registry.md" missing, count_claim 51
expect=fail observed=pass exit=0
PREDICATE R51-C1 pass
```

The row's `51` is "verified" by the `51` in the path. A4 shows the honest shape of the same probe
(missing file, no digits in the path) trips `NUMBER-DRIFT` for the wrong reason — the count was
never taken. Fix: have `probe()` return a structured count (`None` when unreadable) and compare
`None` as its own leg, not as a string scrape.

### 4.4 `ABSENT_RE` accepts a syntactically shaped but invalid date (medium)

`ABSENT\s+(\d{4}-\d{2}-\d{2})` matches `2026-13-99`. Measured:

```
# A11: row marker "**ABSENT 2026-13-99**", state=absent, prose=absent
expect=fail observed=pass exit=0
PREDICATE R51-C1 pass
```

The UNVERDICTED leg's purpose is "an absence nobody dated is not a verdict"; a nonsense date is
not a verdict either. Fix: parse with `datetime.date.fromisoformat` and add A11.

### 4.5 Three of five probe kinds are never exercised (medium)

`sha256`, `port`, `http` — 5 of the 19 real manifest entries (SF03 http; SF10/SF12/SF15 sha256;
SF16 port) — have no selftest fixture. A1/A2/A3 are the missing pure `STALE` cases for them.
This matters because the after-target requires `STALE 0` and the before receipt's only absent
entries of those kinds are the ones the landing will re-date; a regression in those probe bodies
would be invisible.

### 4.6 An unknown probe kind aborts the counting command instead of failing it (medium)

`probe()` ends with `raise SystemExit("unknown probe kind %r" % kind)`. Measured (A12): exit 1,
traceback on stderr, and **no `PREDICATE` line at all** — so the frozen command's final line is
missing rather than `PREDICATE R51-C1 fail`. A manifest typo (e.g. `"kind": "http "` with a
trailing space) turns a verdict into a crash. The `errors` variable that exists for this
(`present = absent = errors = 0`, printed as `errors=0`) is **never incremented anywhere** —
confirmed by `grep -n 'errors'`: assignment at line 190, print at 209, no other use.

### 4.7 Smaller dead or unreachable code (low)

- `stray = used - row_idx` (line 184) can never be non-empty: `anchor_line` only ever holds line
  indices drawn from `rows_by_section[entry.section]`, so `used ⊆ row_idx` by construction.
- `if run(True) != 0: pass` (line 267) is a no-op branch.
- The floor boundary is untested on the equality side (A8a/A8b).
- S6 and S8 are the only two non-isolating fixtures; with §4.1 fixed they should assert their
  coupled key set explicitly rather than appear isolated.

## 5. What the selftest does prove

With all of the above, the honest reading is: the 9-case suite proves the counter's **boolean**
discriminates 7 of its 8 problem legs plus the floor, on `paths`/`count` fixtures, and that the
selftest is temp-isolated and cleans up. It does not prove leg attribution, does not touch
`SECTION-MISSING`, does not touch `sha256`/`port`/`http`, and does not notice three classes of
document the predicate must reject (§4.2–§4.4).

## 6. Limits of this audit

- Findings are against the instrument at `REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7`; the
  stage-1 file hash is recorded in §0 so the L1 can confirm the same bytes at landing.
- No production file was edited. Every fixture lives in
  `/fast/scratch/hyaku/kengaku-r51/C1ExecSelftest/` and is removed at yield; the driver and both
  mutants are reproduced inline above (the mutant diffs are one line each, quoted).
- A2's 500 endpoint and A3's closed port are local point-in-time constructions, not the lane's
  declared surfaces; they prove the probe bodies, not the manifest.
- Observed but not classified as a defect: the `http` probe returns `present` only for status
  **200**, so an endpoint answering any other 2xx (e.g. 204) reads `absent`. Whether that is wrong
  depends on the row's intent ("resolves" vs "answers"); the manifest's only http entry (SF03)
  expects a `/v1/models` 200, so the current behaviour is adequate for it. Flagging for the
  claims' §Limits, not as a fix.
- Not measured: whether the L1's landing adds the new served endpoint (claims §C1 after-target)
  under a probe kind this suite also does not cover.

## 7. Recommendation to the L1

Before the after-measurement is treated as evidence, the instrument needs (in this order):
1. `expect_key` wired at every call site, asserting the non-zero key set (§4.1);
2. `section_rows` bounded at the next heading + an A6-style pure `SECTION-MISSING` case (§4.2);
3. a structured count result instead of `re.search(r"(\d+)", detail)` (§4.3);
4. `date.fromisoformat` for the ABSENT marker (§4.4);
5. A1/A2/A3 for the three unexercised probe kinds (§4.5);
6. `probe()` reporting an unknown kind as a problem key rather than `SystemExit` (§4.6).

None of these changes the C1 predicate text; they make the selftest able to defend it. The
counter's current reading at the tip (`DRIFT 3`, `UNVERDICTED 1`, `NUMBER-DRIFT 1`, exit 1) is
reproduced independently in §1.2 and matches the before receipt line for line.

Tooling: no install or upgrade was needed (nothing in `pacman`, `uv tool`, `npx`, or
`~/.local/bin` was touched).

VERDICT: C1 selftest is a 9-case **exit-code-only** suite — 8 of 9 predicate legs exercised, 6 in
isolation, `SECTION-MISSING` never exercised, `sha256`/`port`/`http` probe kinds never exercised,
and leg attribution unpinned (`expect_key` dead; a key-swap mutant passes 9/9 while changing the
receipt's `DRIFT 3` to `STALE 3`). Three counter false negatives reproduced in scratch (A9
section-heading leak, A10 digit-scraped count, A11 invalid ISO date) plus one crash-instead-of-fail
(A12 unknown probe kind). 13 proposed cases demonstrated; 10 make the current counter fail as a
correct counter must (A1–A8b, including the pure `SECTION-MISSING` case A6), 3 it wrongly passes.
The claim's before-receipt numbers are independently reproduced and stable at the tip.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
