# F39RevBatD5 — review of `plans/battery39/d5m39.py` (M07 kill: markup inside the quote span)

Seat: reviewer, kengaku round 39 wave 2 (FALSIFY). Target: the battery39 module `d5m39.py`
(fixture `d5m39-tagged-quote-span`), measured at lane tip `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`.
Clone: `/fast/scratch/hyaku/kengaku-r39/F39RevBatD5/lane` (`git rev-parse --show-toplevel` verified;
every `git` call named `-C`). Writes only in this report dir and that scratch; scratch removed at the end.
Lane untouched: `git -C "$L" status --porcelain` printed nothing after the build, after every gate run and
after both counter runs. Receipts: this directory (paths at the bottom).

## Axes named

1. **Cause isolation** — is the mutant's `D5 DEFECT` caused by the missing tag strip alone?
2. **Ownership** — does the fixture own its capture dir and spec inside `d`?
3. **Byte faithfulness** — are the docstring's measured claims reproducible?
4. **Load-bearing** — does removing the module flip M07 to `SURVIVED`, as the module claims?

## 0. Baseline

The frozen gate in the clone is the pinned gate: `sha256(plans/pkg_gate.py)` equals
`PINS["plans/pkg_gate.py"]` (`gate_digest_matches_pin True`, `probe-d5m39.txt:1` area). The landing
measurement already shows the fixture green and load-bearing on a clean clone
(`.ufo/waves/round-39/integrate/measure-final.txt`): `FIXTURE d5m39-tagged-quote-span expect=accept
declared=- observed_rc=0 observed_defects=- ok`, `MUTANT M07 D5 mirror killed
by=d5m39-tagged-quote-span`, `MUTANTS total=7 killed=7 …`, and the audit adds
`AUDIT nondeterministic_kills=0` / `AUDIT C1 clean`. Everything below re-demonstrates the mechanism,
not just the receipt.

## 1. Reference vs mutant on the built fixture — the kill, isolated

Fixture built through the counter's own child path
(`python3 plans/round39_c1_verify.py --build-module plans/battery39/d5m39.py --dest … --lane …`,
`d5m39-built.json`): one fixture, `argv[0]=d5-line`, `--file <d>/erratum.md`,
`--capture-dir <d>/captures`, no `--spec`.

* Reference (`plans/pkg_gate.py`): rc=0, `D5 ok directional=True digest_pinned=True bad=0`.
* M07 gate (frozen `old -> new` applied, `old_count_in_gate 1`): rc=1,
  `D5 DEFECT directional=False digest_pinned=True bad=['quote absent from the capture']`.

`digest_pinned=True` on **both** legs: the manifest re-pin works, and the *only* difference the mutant
shows is the quote absence. The declared pair (accept, `defects=[]`) matches the reference exactly, so
`wrong=0` is honest.

## 2. Is the DEFECT caused by the tag strip alone? — yes, three receipts

1. **The mutation is one line and only that line.** M07 (`plans/round39_c1_verify.py:146-151`) replaces
   `flat = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", read(capture) or ""))` with the same expression
   minus `re.sub(r"<[^>]+>", "", …)` (`plans/pkg_gate.py:352`); `gate_src.count(old) == 1`. No other
   behaviour of the gate changes.
2. **Untagged control: the mutant is indistinguishable from the reference.** Same D5 erratum line, the
   frozen capture dir copied as-is (no markup, no re-pin): reference rc=0 `D5 ok directional=True
   digest_pinned=True bad=0` **and** mutant rc=0 `D5 ok directional=True digest_pinned=True bad=0`
   (`CTL_UNTAGGED_*`, `probe-d5m39.txt`). Without the markup the mutant exhibits nothing — the markup
   insertion is the sole trigger.
3. **Flat-text algebra on the built capture.** With the strip, the flat quote is present
   (`quote_in_flat_with_tagstrip_built True` → reference accepts); without it, absent
   (`quote_in_flat_no_tagstrip_built False` → mutant defects); on the frozen capture without the strip,
   present (`quote_in_flat_no_tagstrip_frozen True` → control passes). The markup adds no whitespace
   (delta is exactly the 47 tag bytes, §4), so whitespace-stripped flats differ only by the tags — the
   mirror direction is produced by the strip and nothing else.

## 3. Does the fixture own its capture dir and spec inside `d`? — capture dir yes; no spec passed

* **Capture dir and erratum:** `build()` copies the frozen capture dir into `d/captures` and writes
  `d/erratum.md`; the fixture tree is 14 paths, all under `d`
  (`captures/nec-s091-reopen.html`, `captures/quarantine-SHA256SUMS`, `captures/tb2-eval/*`, …,
  `erratum.md`; `fixture_tree`, `probe-d5m39.txt`). Measured: `file_inside_d True capdir_inside_d True`.
  The build never writes to the lane: `git -C "$L" status --porcelain` empty after the build.
* **Spec:** the fixture passes **no** `--spec`, so `run_gate` appends the frozen, pinned
  `plans/pkg-spec-r35.json` (`plans/round39_c1_verify.py:210-212`), the same spec every fixture gets.
  The battery38 contract sentence "a `--spec` it passes must lie inside d"
  (`plans/round39_c1_verify.py:39-42`) is vacuously satisfied — nothing outside `d` is *passed* by the
  fixture. The gate's `d5-line` reads only `spec["d5"]` and its argv
  (`plans/pkg_gate.py:327-356`): label/require/forbid/capture_name/manifest_name/quote, all from the
  pinned r35 spec the fixture itself read via `ctx.spec["d5"]` — one source of truth, no divergence.
* **Audit boundary (residual, not a defect of this fixture):** the L1 audit confines the
  parent-created dir, a package argv's `--root` and any `--spec` (`plans/round39_c1_audit.py:320-325`);
  it does not re-confine `d5-line`'s `--file`/`--capture-dir`. For this fixture both are constructed
  from `d` and measured inside it; for a hostile module this is the already-ledgered A5 class.

## 4. Byte provenance — every docstring number reproduced

Measured on the built capture vs the frozen capture (`probe-d5m39.txt`):

* `bytes_frozen 60335 bytes_built 60382 delta 47` — matches the docstring's 60,335 → 60,382, and the
  round-34 erratum's "60,335 B" (`corpus/lessons/round-34.md:45`).
* `built_equals_in_place_marked_rewrite True` — the build is exactly the in-place markup insertion.
* `tagstrip_equal_frozen_vs_built True` — the tag-stripped capture text is unchanged.
* `cr_frozen 21 cr_built 21 lf_frozen 422 lf_built 422` — CR/LF unchanged.
* `quote_raw_lineno_frozen 276 … changed_raw_lines 1` — the quote stays on raw HTML line 276, matching
  the erratum's "raw HTML line 276", and only that one line differs.
* `quote_count_frozen_text 1` — the in-place rewrite is unambiguous.
* Manifest `quarantine-SHA256SUMS`: 2 rows, exactly 1 changed, digest field only, rest of the row
  identical, row names the capture, new digest = sha256(built capture), old digest = sha256(frozen
  capture), and only 1 frozen row names the capture (no collateral re-pins).

## 5. Load-bearing — removing the module flips M07 to SURVIVED

Same clone, counter dev mode (predicate prints `n/a`, cannot be mistaken for the frozen predicate):

* `--only M07` (full battery, 90 fixtures): `BATTERY fixtures=90 wrong=0 renamed_disagree=0
  sidechannel=0`, `MUTANT M07 D5 mirror killed by=d5m39-tagged-quote-span`, `MUTANTS total=1 killed=1
  survived=0 …` (`run-onlyM07-full.txt`, exit 0).
* `--only M07 --battery r38` (86 fixtures, no battery39 — includes the other D5 accept fixture
  `d5m-n21-manifest-row-2`): `MUTANT M07 D5 mirror SURVIVED exhibits=none`, `MUTANTS total=1 killed=0
  survived=1 …` (`run-onlyM07-r38.txt`, exit 1 by the dev rule).

So the module's own claim holds: with d5m39 removed, M07 survives; no other fixture kills it, and the
mutant exhibits no other direction anywhere.

## 6. Residual risk and verification gaps

* M07's advertisement is declared *indirect* (Q24) in the mutant cell itself
  (`plans/round39_c1_verify.py:147-148`) — carried limit, not a new gap.
* The gate's flat compare strips tags over the whole capture, so a quote reassembled across other tags
  would also pass; that breadth is outside M07's declared direction and outside this fixture's claim.
* The counter-level attack classes (A1 mid-run flip, A3, A4, A5) are ledgered by wave 1
  (`R39CritC1Counter.md`); for this fixture the audit's nondeterministic recheck printed 0 on the
  landing run, and nothing in `build()` holds state across phases (pure copy + rewrite of `d`).
* I did not re-run the full frozen predicate; the landing receipt (`measure-final.txt`) covers it and my
  two dev-mode runs plus the child-path build agree with it on every line this seat touches.
* Tooling: none installed. No background processes; scratch deleted after receipts were copied.

## Artifacts (this directory)

`d5m39-built.json` (child-path BUILT line), `probe-d5m39.txt` (ref/mutant/untagged-control runs, byte
provenance, manifest diff, ownership checks), `run-onlyM07-full.txt`, `run-onlyM07-r38.txt`.

VERDICT: d5m39-honest
