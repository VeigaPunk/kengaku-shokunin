# F37XMutD5 — extra (non-frozen) mutants of clause D5, wave 2 falsify

Seat: critic. Target: `plans/battery37/d5.py` (7 fixtures) and clause D5 of `plans/pkg_gate.py`
(`cmd_d5`, lines 327–356), beyond the frozen mutants M48–M55. Nothing in the lane was written; every
run below is on a scratch clone of the integration tip.

## Setup (reproduction)

```
S=/fast/scratch/hyaku/kengaku-r37/F37XMutD5; export TMPDIR=$S
git clone -q --no-local <lane> "$S/fx/lane"
git -C "$S/fx/lane" checkout -q 357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
git -C "$S/fx/lane" rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r37/F37XMutD5/fx/lane
sha256sum plans/pkg_gate.py -> ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41  (= freeze digest)
python3 harness.py --lane "$S/fx/lane" --work "$S" --notes
```

`harness.py` imports `plans/round37_c1_verify.py` as a module and reuses `load_r36`, `Ctx`,
`r36_fixtures`, `battery37_fixtures`, `run_gate`; it builds all fixtures once, exactly as the counter's
`main()` does, then runs the reference gate and each extra mutant over every fixture. Observable result =
(exit code, set of clause ids printing `DEFECT`) — the counter's own tuple, unchanged.

Reference on the tip clone:

```
FIXTURES built=64 reference_accepts=['r36-P0', 'r36-L1', 'r36-L4']
REFERENCE wrong=0
```

64 fixtures / wrong=0 / accepts = P0, L1, L4 reproduce the frozen receipt
`.ufo/waves/round-37/integrate/measure-final.txt:69` (`BATTERY fixtures=64 wrong=0`). The receipt's
`TIP 5c7d5d75` is an ancestor of the tip; `git diff 5c7d5d75 HEAD -- plans/` shows only the added
`plans/round37_c1_attribution.py`, so gate, spec and battery bytes are identical and the receipt's
numbers apply to the tip. Evidence files: `F37XMutD5/harness-run.txt`, `F37XMutD5/witness-run.txt`.

Every pair below occurs exactly once in the gate (`gate_src.count(old) == 1`, checked by the harness;
`invalid=0` in the run) and compiles.

## Four counted mutants (the seat's deliverable)

| id | gate site | `old -> new` | result | killing fixture | fixtures differing |
|---|---|---|---|---|---|
| X1 | line 347 | `any(len(parts) >= 2 and parts[0] == digest` → `any(len(parts) > 2 and parts[0] == digest` | **killed** | `r36-L4` | 1/64 |
| X2 | line 334 | `if len(lines) != 1 or not lines[0].startswith(d5["label"]):` → `if len(lines) > 2 or not lines[0].startswith(d5["label"]):` | **killed** | `d5-m49-two-lines` | 1/64 |
| X3 | line 349 | `for parts in (row.split() for row in sums.splitlines()))` → `… sums.splitlines()[:1]))` | **survived** | — | 0/64 |
| X4 | line 353 | `if re.sub(r"\s+", "", d5["quote"]) not in flat:` → `if re.sub(r"\s+", "", d5["quote"])[:20] not in flat:` | **survived** | — | 0/64 |

Harness lines (verbatim):

```
EXTRA X1 KILLED by=r36-L4 differing=1/64 -- manifest row arity off by one (`>= 2` -> `> 2`): a genuine 2-field SHA256SUMS row stops pinning
EXTRA X2 KILLED by=d5-m49-two-lines differing=1/64 -- line-count threshold off by one (`!= 1` -> `> 2`): a two-line erratum still passes the label gate
EXTRA X3 SURVIVED differing=0/64 -- manifest pin applied to the first row only (`sums.splitlines()[:1]`)
EXTRA X4 SURVIVED differing=0/64 -- quote containment loosened to a 20-character prefix of the quote
```

## Three supplementary probes (not counted, reported because they localise the survivors)

| id | gate site | `old -> new` | result |
|---|---|---|---|
| S1 | line 350 | `if not pinned:\n            bad.append("capture digest is not the one in the manifest")` → `… return False, "capture digest is not the one in the manifest"` | survived (unfalsifiable, see F4) |
| S2 | line 352 | `flat = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", read(capture) or ""))` → `flat = re.sub(r"\s+", "", read(capture) or "")` | survived |
| S3 | line 352 | same line → `flat = re.sub(r"<[^>]+>", "", read(capture) or "")` | survived |

## Witnesses: what one added fixture would do (`witness.py`)

Each witness is one fixture the battery does not contain, built in scratch from lane bytes; the
reference gate's result on it is shown first, so the witness is a genuine accept/reject state and not a
broken tree.

```
W3-manifest-match-row-2 rc=0 :: D5 ok directional=True digest_pinned=True bad=0        (decoy row first, real digest second)
W4-quote-truncated-to-20 rc=1 :: D5 DEFECT … bad=['quote absent from the capture']     (capture holds quote[:20], manifest re-pinned)
W5-quote-split-by-tags rc=0 :: D5 ok directional=True digest_pinned=True bad=0          (quote split by </b><b>)
W6-quote-split-by-newline rc=0 :: D5 ok directional=True digest_pinned=True bad=0       (quote split by a newline)
WITNESS X3 KILLED by=W3-manifest-match-row-2
WITNESS X4 KILLED by=W4-quote-truncated-to-20
WITNESS S2 KILLED by=W5-quote-split-by-tags
WITNESS S3 KILLED by=W6-quote-split-by-newline
WITNESS S1 SURVIVED
```

So X3, X4, S2, S3 are **missing-fixture gaps, not gate defects**: one battery row each would kill them.
S1 is not killable by any fixture (F4).

## Isolation audit of `plans/battery37/d5.py`

The frozen predicate discards the gate's note text, so "one defect per fixture" is not measured by C1 at
all — it can only be read from the notes. Reference notes on the seven d5 fixtures (`--notes`):

```
d5-m48-file-unreadable  rc=1 :: D5 DEFECT file unreadable
d5-m49-two-lines        rc=1 :: D5 DEFECT line_count=2 labelled=False
d5-m50-label-altered    rc=1 :: D5 DEFECT line_count=1 labelled=False
d5-m51-require-missing  rc=1 :: D5 DEFECT directional=False digest_pinned=True bad=["missing 'is present'"]
d5-m52-forbid-present   rc=1 :: D5 DEFECT directional=False digest_pinned=True bad=["carries 'not present'"]
d5-m53-capture-missing  rc=1 :: D5 DEFECT capture unreadable
d5-m55-quote-absent     rc=1 :: D5 DEFECT directional=False digest_pinned=True bad=['quote absent from the capture']
```

Verdict per fixture: **all seven isolate one defect**, as the module docstring says. Independent
evidence, not just the note: X2 (which lets a two-line file through) turns `d5-m49` into an **accept**,
which proves nothing behind the line-count early return also fails (required token present, forbidden
token absent, digest pinned, quote present). `d5-m55`'s note prints `digest_pinned=True`, proving the
manifest rewrite pinned the new bytes so the failing check is the quote alone. `d5-m50` rewrites only a
same-length label prefix (`round 35` → `round 34`), leaving every later byte genuine.

Caveats, none of which breaks the frozen predicate:

- `d5-m49`'s and `d5-m50`'s notes both read `labelled=False`; for `d5-m49` the label *is* present (the
  message is the fixed string `f"line_count={len(lines)} labelled=False"`). Message-only; the observable
  is the clause id.
- `d5-m55` also drops the second row (`geniac-s105-reopen.html`) of the manifest. No D5 check reads
  sibling rows, so it is not a second defect today; a future row-count check would make the fixture
  multi-defect.
- The declaration `"defects": ["D5"]` on every reject is **vacuous**: `d5-line` runs exactly one clause,
  so `{D5}` is the only possible non-empty set. What the counter actually constrains is `expect=reject`.

## Findings

**F1 — `d5.py` has no accept-side fixture, so the module alone cannot catch an over-strict D5.**
X1 (`>= 2` → `> 2`, a gate that no longer pins a genuine two-field SHA256SUMS row) differs on exactly one
fixture, `r36-L4`, i.e. the round-36 battery — **zero of the 7 d5 fixtures**. `plans/battery37/d5.py:140-146`
declares `expect: "reject"` seven times. Any D5 mutant that only *adds* a reject survives the whole
module. Axis: C1 calibration (module self-sufficiency), not the predicate — the battery as a whole kills
it. Same shape as the documented M54 delegation (`measure-final.txt:123`, `M54 D5 killed by=r36-L6`), but
undeclared for the accept side.

**F2 — battery-wide gap: no fixture has a manifest whose matching row is not the first row.**
X3 survives 64/64 and is killed by one artificial row (W3: decoy digest row first, genuine row second,
which the unmodified gate accepts — `W3 … rc=0 … digest_pinned=True bad=0`). A gate that stopped reading
after the first manifest line would still be C1-green. Every existing D5-adjacent fixture (`d5-m53`,
`d5-m55`, `r36-L4`, `r36-L6`) uses a manifest whose matching row, if any, is row 1.

**F3 — battery-wide gap: the quote check's normalisation is dead weight for the whole battery.**
Measured on the genuine capture (`plans/pkg-spec-r35.json` `d5.quote`, 70 chars, no whitespace):

```
quote raw in capture: True      quote in tagstripped: True
quote_ws_stripped in flat: True  quote in ws_only_stripped: True
```

The quote is already verbatim in the raw bytes, so the two `re.sub` steps on line 352 never change an
outcome for any fixture: m55 *deletes* the quote, `r36-L6` injects it verbatim inside `<html>…</html>`.
Consequently X4 (quote match loosened to a 20-char prefix), S2 (tag-strip removed) and S3 (whitespace
removal removed) all survive 64/64, while W4/W5/W6 kill each of them with a single fixture. The gate's
claim that a quote is found "after tag-strip and whitespace removal" (the erratum line's own wording) is
demonstrated by nothing.

**F4 — one class of D5 mutant is unfalsifiable under the frozen observable, so it is a limit of C1's
observable, not a missing fixture.** S1 converts `if not pinned: bad.append(...)` into
`return False, ...`: the digest failure then shadows the later quote check. Both versions report
`D5 DEFECT` and exit 1 for every possible input, so **no fixture can ever kill it**. More generally,
`run_gate` keeps only `(rc, {clause ids})`, so any mutation confined to *which* D5 sub-check fails is
invisible. The claims already name this horizon ("demonstration is observational … not proof that each
check is the right check"); S1 is the sharpest instance and shows the same blindness is why the "one
defect per fixture" property of `d5.py` cannot be asserted by C1 — it is only readable from notes the
predicate throws away.

**F5 — the frozen claim is not violated by any of this.** C1's predicate is about the 55 frozen mutants
and the battery declarations; both still hold on the tip clone (reference `wrong=0`, 64 fixtures, the
frozen receipt's `killed=55`). X1–X4 and S1–S3 are additional, non-frozen mutants of the same clause; the
frozen kill rule says an equivalent-or-extra mutant found later is reported as a limit of the freeze and
never folded into it. `d5.py`'s own docstring table (M48–M53, M55 with M54 delegated to `r36-L6`) is
accurate against the receipt.

## Impacted axes

- C1 calibration: battery completeness for D5 (F1–F3), and the precision of what C1 measures for D5 (F4).
- Lane self-assessment / frontier: `plans/battery37/d5.py` is described as "One fixture per frozen gate
  mutant of the D5 branch"; that is true for the eight frozen mutants but is not a statement of D5
  sensitivity, which is what a reader of the capability row may assume.

Not impacted: the C1/C2 predicates, the gate bytes, the frozen mutant list, the coverage artefacts.

## Smallest safe correction (reported, not applied — claim frozen)

Four rows in `plans/battery37/d5.py`, no gate change:

1. decoy-first manifest row, genuine row second, genuine erratum — must be **accept** (kills X3);
2. capture holding `quote[:20]` only, manifest re-pinned — reject (kills X4);
3. capture with the quote split by an HTML tag, manifest re-pinned — **accept** (kills S2);
4. capture with the quote split by a newline, manifest re-pinned — **accept** (kills S3).

Rows 1/3/4 are accept fixtures, which `d5.py` currently has none of (F1). S1's class cannot be fixed by a
battery row at all; it needs the counter's observable to include the failing note, which would change the
frozen predicate and therefore belongs to a later round, not this freeze.

## Cleanup

`rm -rf /fast/scratch/hyaku/kengaku-r37/F37XMutD5` (clone, fixtures, temp gate copies). Receipts kept in
`.ufo/waves/round-37/falsify/F37XMutD5/` (`harness.py`, `witness.py`, `harness-run.txt`,
`witness-run.txt`). No lane file, Git index, jj state, fleet-root or sibling lane was written; no corpus/
or plans/ tree was copied into the falsify directory.

VERDICT: extra-mutants-d5-killed-2/4
