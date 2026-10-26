# F37XMutP6 — four new non-frozen mutants of gate clause P6 (c_sources)

Seat: critic, kengaku round 37 wave 2 (falsify). Target: `plans/battery37/p6.py` (fixtures for M20–M27)
and the frozen predicate claim that the battery calibrates clause P6 of `plans/pkg_gate.py`.

## Environment (measured, not assumed)

Clone of lane `kengaku-shokunin` at the assigned integration tip, made under
`/fast/scratch/hyaku/kengaku-r37/F37XMutP6` (removed before finishing):

```
git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/fx/lane"
git -C "$S/fx/lane" checkout -q 357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
git -C "$S/fx/lane" rev-parse --show-toplevel   -> $S/fx/lane
git -C "$S/fx/lane" rev-parse HEAD              -> 357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
sha256sum plans/pkg_gate.py -> ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41
```

That digest equals `GATE_SHA256` in `plans/round37_c1_verify.py`, so the mutants below are against the
frozen gate bytes. `c_sources` spans gate lines 184–210; the four mutation sites are lines 204, 192, 198, 196.

Baseline of the battery on this clone (harness section, 64 fixtures = 14 round-36 + 50 battery37):

```
BATTERY fixtures=64 wrong=0
```

Every fixture's observed `(exit code, DEFECT set)` matched its declaration, so the battery is green before
any new mutant runs — the survivors below are coverage gaps, not a broken harness.

## The four new mutants (all outside the frozen M20–M27 set)

Each `old` occurs exactly once in the frozen gate (checked in the harness, `occurrences=1`), each compiles,
and a programmatic comparison against `MUTANTS` in `plans/round37_c1_verify.py` confirms none of the four
`(old, new)` pairs — nor any `old` substring — is a frozen pair.

| id | site | old -> new | result | killing fixture |
|----|------|------------|--------|-----------------|
| X1 | line 204 | `if len(cells[6].split()) < rules["min_teaches_words"]:` -> `... < rules["min_teaches_words"] - 1:` | **SURVIVED** | none of 64 |
| X2 | line 192 | `if len(cells) != 11:` -> `if len(cells) < 11:` | killed | `p6-m21-row-with-twelve-cells` (only) |
| X3 | line 198 | `if cells[3] != rules["row_tier"]:` -> `if not teaches and cells[3] != rules["row_tier"]:` | killed | `p6-m23-row-tier-b` (only) |
| X4 | line 196 | `url.group(0) != p.spec["raw_base"] + row["upstream"]` -> compare `.split("://", 1)[-1]` of both sides | **SURVIVED** | none of 64 |

Harness output (`harness-receipt.log`, run as `python3 harness.py --lane $S/fx/lane --work $S/work`):

```
MUTANT X1 P6 SURVIVED -- teaches threshold one below min_teaches_words (off-by-one)
MUTANT X2 P6 killed by=p6-m21-row-with-twelve-cells all=p6-m21-row-with-twelve-cells -- row cell-count equality loosened: 11 required -> at least 11
MUTANT X3 P6 killed by=p6-m23-row-tier-b all=p6-m23-row-tier-b -- tier check runs on the first registry row only
MUTANT X4 P6 SURVIVED -- url check loosened to a scheme/host-blind suffix compare
NEW_MUTANTS total=4 killed=2 survived=2
```

X2 and X3 are killed by a single fixture each, which is the expected single-defect shape: only one fixture
carries a 12-cell row, and only one carries a wrong tier on a row after the first (`S106` is the second
registry row in `spec["rows"]` order, so `not teaches` is false there).

## Are the two survivors real defects or equivalent mutants?

They are real weakened checks: for each I built one single-row tree in scratch that the **frozen** gate
rejects and the mutant accepts (`probe-receipt.log`, `probe.py`):

```
PROBE X1 S105 teaches cell = 7 words (min_teaches_words=8) | frozen_rc=1 frozen_defects=P6 | X1_rc=0 X1_defects=- | survivor_is_real_defect=yes
PROBE X4 S107 pinned raw url scheme swapped https -> http | frozen_rc=1 frozen_defects=P6 | X4_rc=0 X4_defects=- | survivor_is_real_defect=yes
```

So the battery never exercises either boundary. The reason is countable in the 48 package fixtures it
builds (scan over `$S/work/run/fx`, `S105`–`S107` rows of `corpus/SOURCES.md`; the 16 non-package
`d4`/`d5` line fixtures have no registry at all):

```
teaches_word_counts= {1: 6, 5: 1, 23: 92, 30: 46}
url_classes: {'pinned-exact': 144, 'other:https://raw.githubusercontent.com/harbor-framework/terminal-': 1}
```

* X1: the only sub-threshold teaches value in the battery is 5 words (`p6-m26`, plus two round-36 package
  fixtures with a 1-word cell). Nothing sits at 7 = `min_teaches_words - 1`, so lowering the threshold by
  one changes no fixture. A correct battery would need a boundary fixture at exactly 7 words.
* X4: 144 of 145 row URLs are byte-identical to the pinned raw path and the single exception is a
  different **task path** (`regex-log/instruction.md`), which the loosened compare still rejects. No
  fixture varies scheme, host, or appends a query, so scheme/host blindness is invisible to the battery.

## Does each p6.py fixture isolate one defect as its docstring says?

Yes — for all eight, measured three ways: (a) the fixture tree differs from the genuine package in exactly
one file, `corpus/SOURCES.md`; (b) only the registry row named in the docstring differs, and the P6 clause
line reports `bad=1`; (c) restoring the genuine registry (each fixture copied, `SOURCES.md` restored,
`git add -A`) makes the gate accept with no DEFECT.

| fixture | differing rows | source diff lines | P6 clause line | declared/observed | restore -> rc | isolates |
|---|---|---|---|---|---|---|
| p6-m20-registry-row-duplicated | S105 | 1 (insertion) | `P6 DEFECT rows=3 bad=1 first=S105: rows=2` | P6/P6 | 0 | yes |
| p6-m21-row-with-twelve-cells | S106 | 2 | `P6 DEFECT rows=3 bad=1 first=S106: cells=12` | P6/P6 | 0 | yes |
| p6-m22-url-off-the-pinned-raw-path | S107 | 2 | `... first=S107: url not the pinned raw path` | P6/P6 | 0 | yes |
| p6-m23-row-tier-b | S106 | 2 | `... first=S106: tier='B'` | P6/P6 | 0 | yes |
| p6-m24-row-status-queued | S105 | 2 | `... first=S105: status='queued'` | P6/P6 | 0 | yes |
| p6-m25-used-by-another-path | S107 | 2 | `... first=S107: used-by is not the entry` | P6/P6 | 0 | yes |
| p6-m26-five-word-teaches-cell | S105 | 2 | `... first=S105: teaches words=5` | P6/P6 | 0 | yes |
| p6-m27-two-identical-teaches-cells | S107 | 2 | `... first=teaches cells are not pairwise distinct` | P6/P6 | 0 | yes |

(`rows=3` in the P6 message is `len(spec["rows"])`, the three spec rows, not registry lines.)

Each docstring claim also checks out cell-by-cell against the genuine row (`claim ok` for every item):

* M20: exactly two `S105` rows, byte-identical to the genuine row, `S106`/`S107` untouched.
* M21: 12 cells, cells 0–10 equal the genuine values, the extra cell is the only addition.
* M22: only cell 1 changed; it is a real `https://raw.githubusercontent.com/...` URL and not
  `raw_base + upstream` (observed `.../regex-log/instruction.md`).
* M23: `S106` tier `B` vs genuine `A`, cell 3 the only change. M24: `S105` status `queued` vs `mined`,
  cell 7 the only change. M25: `S107` used-by is the regex-log knowledge file, not the entry, cell 10 the
  only change.
* M26: `S105` teaches 5 words < 8, cell 6 the only change, all three teaches cells stay pairwise distinct
  (so the fixture does not accidentally also trip the distinctness check).
* M27: `S107` teaches equals `S106`'s, both ≥ 8 words, differs from the genuine cell, cell 6 the only
  change — it dodges M26 by construction.

Two honest caveats. Isolation holds relative to the gate's clause set: M22 leaves a row whose URL names
another task while its sha256 still pins the protein-assembly capture, so a stricter gate could count two
defects there — the frozen gate has no such cross-check and reports `bad=1`. And each builder injects
exactly one edit by construction (`ctx.genuine_package` then one mutator), so the battery cannot represent
a tree with two simultaneous defects, which is what a row-skipping weakening would need.

## Axes and impact

* **Calibration (C1)**: unaffected as frozen. Nothing here changes `MUTANTS total=55 killed=55` — the two
  survivors are new mutants outside that set, and no lane file was touched. The falsification is about what
  "killed=55" covers for P6, not about the 55 being wrong.
* **Battery breadth / claim honesty**: P6's demonstrated surface is equality and exactness, not boundaries.
  The battery proves the gate catches *far*-wrong values (5-word teaches, another task's URL) but not
  one-step-wrong ones (7-word teaches, scheme-swapped URL). Two of four plausible weakenings of the same
  clause are invisible.
* **Isolation (fixture quality)**: p6.py is clean — no fixture leaks a second defect, no cell collateral,
  no non-registry file drift.

## Smallest safe correction

Do not amend the frozen claim: it remains true as written, and repairing a battery limit by editing the
frozen predicate is exactly the move this seat must refuse. If P6 coverage is to be widened in a later
round's battery (not this one), the smallest additions are two fixtures mirroring X1 and X4 —
`S105` teaches exactly `min_teaches_words - 1` = 7 words, and `S107` URL with the scheme swapped to `http`
at the pinned path — each declaring `expect=reject`, `defects=["P6"]`. Both were shown to separate the
frozen gate (reject) from the weakened mutant (accept), so they would kill X1 and X4 without touching the
gate. Catching row-skipping weakenings needs a two-defect fixture, which the current single-defect builder
cannot express; not measured here, so not claimed.

## Receipts

All under `.ufo/waves/round-37/falsify/F37XMutP6/` (scratch `/fast/scratch/hyaku/kengaku-r37/F37XMutP6`
removed; no `plans/`, `corpus/` or lane writes):

```
415510f5c0118773f081b7fb14cb34cc48578563783894a3d77e94d57ac293cb  harness.py
fb0be3edcb10c7f89f7560c73e91402bb77416c16977d9a2005e570e23b9a7af  probe.py
388ffb8ad16e4511e2e97a9347efb95795590fc5eaba741a1fe5c4e775967610  harness-receipt.log (139 lines)
828412e4476553e6c3c3a6506ef09399228c457c1d438c7adba2cd965aabd2b6  probe-receipt.log (12 lines)
```

The harness imports `plans/round37_c1_verify.py` as a module from the clone and uses its
`load_r36`, `Ctx`, `r36_fixtures`, `battery37_fixtures` and `run_gate`, building the fixtures once and
running the reference plus each mutant over all 64. Tooling: no installs or upgrades were needed
(none performed).

VERDICT: extra-mutants-p6-killed-2/4
