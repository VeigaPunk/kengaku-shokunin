# F39XMut — extra non-frozen mutants near M02/M03/M04/M07 (round 39 wave 2, falsify)

Seat: F39XMut (mutation tester). Lane tip measured: `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`
(branch master). Attack: the frozen C1 counter's **kill coverage** — eleven extra `(old,new)`
mutants against `plans/pkg_gate.py`, run over the **full landed battery** (r36 + battery37 +
battery38 + battery39, 90 fixtures) with the frozen counter's own kill rule. A survivor is a
battery coverage gap (round-40 candidate), never a licence to change the contract.

## 0. Method — the frozen counter, unmodified

- Scratch (operator directive): `S=/fast/scratch/hyaku/kengaku-r39/F39XMut`;
  `git clone -q --no-local <lane> "$S/lane" && git -C "$S/lane" checkout -q a6832f53…`;
  `git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane` before any write. Every git call named
  `-C`; nothing committed.
- Harness: `xmut39.py` (receipt dir) imports the **frozen** `plans/round39_c1_verify.py` from the
  clone **unmodified** and appends the eleven tuples to its `MUTANTS` **in memory** (`TOTAL=18`).
  Kill rule, battery build, family filter, `exhibits`, per-mutant digest checks: frozen code, byte
  for byte. The frozen M01–M07 rows are reused verbatim as the **in-run control**. Mutant gate
  copies are written only under the counter's `--work` scratch.
- No lane file was edited. After the run:
  `sha256sum $S/lane/plans/pkg_gate.py` → `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`
  (the frozen pin), `git -C "$S/lane" status --porcelain | wc -l` → `0`, HEAD `a6832f53…`.
- Every `old` occurs exactly once in the pristine gate (pre-verified counts 1/1/1/1 for the four
  anchor strings; the counter's own `gate_src.count(old) != 1` invalid-check passed for all 11 —
  `invalid=0` in the receipt). All 11 mutant gates `py_compile` clean (`witness-run.txt` phase 1).
- Command (one run, wall 65.55 s):
  `python3 $S/xmut39.py --lane $S/lane --work $S`

## 1. The eleven extra mutants (all against `plans/pkg_gate.py`)

Anchor lines (pristine gate): `:114` (P1 sweep), `:130` (P3 word window), `:220` (P7 per-row
provenance), `:352` (D5 flat compare).

| id | clause | dir | old → new (exact strings) |
|----|--------|-----|---------------------------|
| XP1a | P1 | silence | `bad = [rel for rel, dig in pins.items() if sha256(p.root / rel) != dig]` → `bad = [rel for rel, dig in list(pins.items())[:2] if sha256(p.root / rel) != dig]` |
| XP1b | P1 | silence | same old → `bad = [rel for rel, dig in list(pins.items())[-1:] if sha256(p.root / rel) != dig]` |
| XP3a | P3 | silence | `short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi]` → `short = [q.text[:30] for q in p.quotes if not lo - 1 <= q.words <= hi]` |
| XP3b | P3 | mirror | same old → `short = [q.text[:30] for q in p.quotes if not lo + 1 <= q.words <= hi]` |
| XP3c | P3 | mirror | same old → `short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi - 1]` |
| XP7a | P7 | silence | `if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:` → `if (prov.get(sid) or [""])[-1] != p.spec["raw_base"] + row["upstream"]:` |
| XP7b | P7 | silence | same old → `if set(prov.get(sid) or [""]) != {p.spec["raw_base"] + row["upstream"]}:` |
| XP7c | P7 | silence | same old → `if not any(u == p.spec["raw_base"] + row["upstream"] for u in (prov.get(sid) or [""])):` |
| XD5a | D5 | mirror | `r"<[^>]+>"` → `r"<[^>]*>"` (strip also eats empty tags) |
| XD5b | D5 | mirror | `r"<[^>]+>"` → `r"</?[a-zA-Z][^>]*>"` (strip only letter-led tags) |
| XD5c | D5 | mirror | `r"<[^>]+>"` → `r"<.*>"` (greedy across the line) |

The r35 spec (`plans/pkg-spec-r35.json:33-37`) carries **three** pins: `plans/tb2_grader_probe.py`,
`plans/round35_c1_verify.py`, `plans/defect_ledger.py`; `entry_rules.quote_words = [3, 25]`.

## 2. Run receipt (full stdout: `xmut-run.txt` beside this report)

```
PINS total=26 mismatched=0
BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=18 killed=12 survived=6 invalid=0 null_detected=0
PREDICATE C1 fail
```

- `BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0` — identical to the landing
  measurement `.ufo/waves/round-39/integrate/measure-final.txt`; the clone + wrapper are faithful.
- **Control:** the frozen seven kill identically to `measure-final.txt` — M01←`d5m-n21-manifest-row-2`,
  M02←`p1m-second-pin-appended-bytes`, M03←`p3m39-quote-one-word-above-upper-bound`,
  M04←`p7m39-s105-two-source-lines`, M05←`p23-p2-receipt-deleted`, M06←`r36-P0`,
  M07←`d5m39-tagged-quote-span`.
- The trailing `PREDICATE C1 fail` is the counter's verdict over the **extended 18-mutant list**
  (frozen 7 + 11 probes), not the frozen predicate; the frozen predicate run is `measure-final.txt`
  (7/7, pass), untouched here.

## 3. Verdict: 5 killed / 6 survived

### Killed (5) — every one by an EXISTING battery fixture; no new fixture needed

| id | killed by | mechanism (measured) |
|----|-----------|----------------------|
| XP1b | `r36-P5` | the r36 stub-probe fixture replaces `spec["probe_cmd"][0]` — pin 1 (`round36_c1_verify.py:122-123`: `probe = dest / spec["probe_cmd"][0]`, then `probe.write_text(...)`); a last-pin-only sweep (pin 3) is blind to pin 1. Same class: `p910-probe-exits-1` (battery37/p910.py:12-13: "the probe is a ``frozen_instruments`` entry, so editing it necessarily changes its pinned digest"). |
| XP3a | `p23-p3-two-word-quote` | a 2-word quote (= lo−1) stays inside the widened window [2,25]; ref `P3 DEFECT`, mutant `P3 ok`. |
| XP3b | `r36-P0` | the genuine package carries **six** 3-word quotes (word-count census below); window [4,25] flags them on an accept fixture. |
| XP7c | `p7m39-s105-two-source-lines` | `prov["S105"] = [pinned, other]` contains the pinned URL, so any-of passes; ref `P7 DEFECT`, mutant `P7 ok`. |
| XD5c | `r36-L4` | the genuine quote sits on raw line 276 with tags on **both** sides (`<br />`,`<strong>`,`</strong>` before; `</p>`,`<!--/.str-inner -->`,`</div>` after); greedy `<.*>` swallows first-`<`→last-`>` on that line. Measured on the genuine capture: `quote in flat_XD5c(greedy): False` while ref flat keeps it → ref `D5 ok`, mutant `D5 DEFECT`. |

So the battery already demonstrates: pin coverage beyond the last pin, the lower word bound from
the reject side (2 words) and the accept side (3 words), source-line *any-of* laxness, and
over-greedy tag stripping. It does **not** demonstrate the four gaps below.

### Survived (6) — each non-equivalent, witness exhibited (`witness-run.txt`)

The counter prints `SURVIVED exhibits=none` for all six: no battery fixture distinguishes them in
any direction. Each witness below is a hand-built input the battery lacks; ref vs mutant outputs
are quoted from `witness-run.txt`.

**XP1a — P1 checks only the first TWO pins.** No battery fixture corrupts pin 3
(`plans/defect_ledger.py`): the P1-declaring fixtures corrupt pin 1 (`r36-P5`, `r36-P7`,
`p910-probe-exits-1`) or pin 2 (`p1m-second-pin-appended-bytes`); a plans-tree census
(`grep defect_ledger plans/`) shows only readers (`ledger_tip.py`), no battery writer. M02's kill
therefore proves "not only the first", not "not only the first *k*".
Witness: genuine package + appended bytes on pin 3 →
ref `P1 DEFECT pinned=3 mismatched=['plans/defect_ledger.py']` rc=1 /
mut `P1 ok pinned=3 mismatched=0` rc=0.
**Round-40 candidate:** a battery39 module that appends bytes to the **third** pinned instrument
(pin order read from `ctx.spec["frozen_instruments"]`, as `p1m.py` does for pin 2).

**XP3c — upper word bound not tightened by one (`hi − 1`).** Genuine-quote word census (gate's own
parser over `corpus/knowledge/tb2-protein-assembly-grader.md`): `{3:6, 4:3, 7:4, 9:1, 10:1, 11:3,
14:1, 15:1, 17:1, 19:1}` — 22 quotes, min 3, **max 19**. The only above-bound fixture is
`p3m39-quote-one-word-above-upper-bound` (26 words, ref `P3 DEFECT` — not mirror-able). Every
accept package fixture's quotes top out at 19, so any `hi' ∈ [19,25]` behaves identically on the
battery: the bound's *value* is demonstrated only from above.
Witness: accept package whose last quote is exactly 25 words (verbatim tail of `task.toml:6`) →
ref `P3 ok rows=22 … out_of_word_range=0` rc=0 / mut `P3 DEFECT … out_of_word_range=1` rc=1.
**Round-40 candidate:** an accept fixture whose longest quote is exactly `hi` words.

**XP7a — pinned URL required only as the LAST source line.** `p7m39` plants `[pinned, other]`
(pinned first); the order-flipped case is uncovered.
Witness: S105 source lines `[other-url, pinned-url]` (unpinned line inserted *before* the pinned
one) → ref `P7 DEFECT … first=S105: source line not the pinned url` rc=1 / mut `P7 ok … bad=0` rc=0.
**Round-40 candidate:** plant the unpinned `source:` line *before* the pinned one.

**XP7b — source lines compared as a set (duplicate pinned line passes).** No fixture duplicates a
pinned source line (`p7m39` plants a *different* URL).
Witness: S105 source lines `[pinned-url, pinned-url]` (verbatim duplicate) →
ref `P7 DEFECT … first=S105: source line not the pinned url` rc=1 / mut `P7 ok … bad=0` rc=0.
**Round-40 candidate:** duplicate the pinned `source:` line verbatim.

**XD5a — tag strip also eats empty tags (`<[^>]*>`).** Equivalent **on the frozen corpus**: the D5
capture `.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html` contains no `<>`
(measured: `contains '<>': False`) and the frozen quote has no `<`. Distinguishing input exists in
principle (a quote containing a literal `<>` that the capture carries verbatim).
Witness: capture appended `A<>B`, probe-owned spec quote `A<>B` →
ref `D5 ok directional=True digest_pinned=True bad=0` rc=0 /
mut `D5 DEFECT … bad=['quote absent from the capture']` rc=1.
**Round-40 candidate:** a d5 fixture owning a spec whose quote contains a literal `<>` present in
the capture (the battery38 contract allows a fixture-owned `--spec` inside the fixture dir).

**XD5b — tag strip removes only letter-led tags.** Equivalent on the frozen corpus: `d5m39`'s
inserted markup is all letter-led (`<b>`, `<span class="str-inner">`, `<em>`), and the genuine
capture's comments (`<!--/.str-inner -->` on line 276) sit *after* the quote, never between its
parts (measured: `quote in flat_XD5b: True`). Distinguishing input: a non-letter-led tag **between**
quote parts.
Witness: capture line `A<x>B<!c>C`, spec quote `ABC` →
ref `D5 ok directional=True digest_pinned=True bad=0` rc=0 /
mut `D5 DEFECT … bad=['quote absent from the capture']` rc=1.
**Round-40 candidate:** the `d5m39`-style tagged-quote fixture with a comment (`<!-- … -->`) as one
of the separators inside the quote span.

## 4. Reading for round 40

The four frozen survivors M02/M03/M04/M07 were each killed by exactly ONE new fixture, planted at
the first distinguishing input its author thought of. The six survivors here show those fixtures
are **point** fixes, not coverage: pin *order* (XP1a vs XP1b), bound *value* on the accept side
(XP3c), source-line *order* and *multiplicity* (XP7a, XP7b), and tag-strip *charset* (XD5a, XD5b)
are all undemonstrated. Each candidate fixture above is one battery39 module in the existing
contract; none requires touching the frozen counter, gate, or spec.

## 5. Limits

- Kill rule is the frozen counter's; a kill records a direction difference, not fixture intent
  (carried limit, `plans/round-39-claims.md` C1 limits).
- XP1a/XP3c/XP7a/XP7b survivors are genuine coverage gaps (distinguishing inputs exist and are
  exhibited). XD5a/XD5b are equivalent **on the frozen corpus** — their witnesses use
  probe-authored inputs (a fixture-owned spec quote / appended capture line), which is exactly the
  input class the battery lacks; treat them as weaker candidates.
- No pre-freeze witnesses for the extras (unlike M01–M07): directions are argued from the gate
  source and corpus census, and exhibited post-hoc in `witness-run.txt`.
- The extras were not checked against the round-38 counter's battery alone; the run is full-battery.
- Wave-1's counter gameability findings (A1/A3/A4/A5) are out of scope here; this probe assumes the
  counter's own kill rule and measures the battery against it.

## 6. Artifacts (this directory)

`xmut39.py` (wrapper: frozen counter + 11 extra mutants), `witness.py` (survivor witnesses),
`quote_locate.py` (capture/quote mechanism probe), `xmut-run.txt` (full 18-mutant run stdout),
`witness-run.txt` (witness stdout). Replay: clone the lane at `a6832f53…`, run
`python3 xmut39.py --lane <clone> --work <scratch>`. Tool installs: none. Scratch
`/fast/scratch/hyaku/kengaku-r39/F39XMut` removed after receipts were copied.

VERDICT: xmut-killed-5/11
