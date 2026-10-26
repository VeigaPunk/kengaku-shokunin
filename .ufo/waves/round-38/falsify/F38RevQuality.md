# F38RevQuality — review of Q28 and the round-38 erratum on `tb2-git-webserver-grader.md`

Seat: reviewer, round 38 wave 2 (falsify). Target: `corpus/QUALITY.md` Q28 (round-38 criterion) and the
round-38 erratum appended to `corpus/knowledge/tb2-git-webserver-grader.md`, against
`.ufo/waves/round-37/falsify/F37CritC2Map.md` (req-map-2/4), the round-37 probe receipt
(`corpus/evidence/round37/git-webserver-probe.txt`), and `F37CritC2Overclaim.md` (F1–F13).
Questions: corrections right? complete? append-only? Is Q28's check executable and shown able to fail?

All work in scratch clone `/fast/scratch/hyaku/kengaku-r38/F38RevQuality/lane` at landing tip
`8c7422d7a646515d80af44844e8ecc8a1fc1d30a` (toplevel verified; `git status --porcelain --untracked-files=all`
= 0). Receipts: `falsify/F38RevQuality/`. No lane file written; no git mutation in the lane.

## 1. Append-only — holds (byte-verified)

- Base claim (erratum §opening): sha256 `6e3f8c77139f64737bc64094f7c91a3e7f7598e1ebdce91cb0fd92eb4854812a`,
  git blob `68263f2990e0543f8e2e1814307201a0c66f87f1`, read at `2c5f4e0b…` — both re-derived:
  `git show 2c5f4e0b…:corpus/knowledge/tb2-git-webserver-grader.md | sha256sum` → the 64-hex above;
  `git ls-tree` → `100644 blob 68263f2990e0543f8e2e1814307201a0c66f87f1`.
- Byte-level: current file's first 24798 bytes `cmp`—identical to the base file (PREFIX_BYTE_IDENTICAL);
  the erratum is a pure append. `git diff --numstat 2c5f4e0b 8c7422d7 -- <file>` → `155 0` (+155/−0).
  One commit (d93b7d6, 2026-10-26T02:56:10-03:00) between base and tip touches the file.
- `corpus/QUALITY.md` Q28/Q29 section: `+67/−0` from base to tip (append-only).
- The erratum's own §C "untouched" list holds: probe digest `63cb75cf…5eedf` reproduced
  (`sha256sum plans/git_webserver_probe.py`); captures 6/6 OK (`sha256sum -c SHA256SUMS`);
  receipts `d0a608ca90e1…8032fc934` (F37CritC2Map/c2-verify-run.txt), `8e801b0a59a9…be3d2de4`
  (diag-verify-stderr.txt), `1e9f62011880…ef44251` (quotes-check.txt) all reproduce; quotes-check says
  32/32 byte-exact; S114 line-39 quote verified in the capture (`set -e` at `:39`); dry table summary
  `cases=22 predicted_pass=7 predicted_fail=15`; round-37 receipt/dry carry 0 `violates=` tags
  (`grep -c` → 0, 0), round-38 receipt carries 22 and dry table 7 TAG lines.

## 2. Corrections right — verified against receipt + both wave-2 seats + replay

- The erratum §A restated map matches the F37CritC2Map prescription verbatim in substance (row 7
  qualifier, row 8 witness swap to `status-then-content-split`, row 9 `partly` + `token-in-body`), and
  every cited case's observed verdict matches the receipt (`token-in-body` observed=pass at receipt line
  35; `status-then-content-split` pass; `capitalised`/`leading-space`/`not-found`/`wrong-port-8081` fail;
  both `no-server` and `wrong-port-8081` print the same `HTTP 000`).
- Independent replay (R38MapRetro, committed): the derived rule over a seat-authored (non-frozen)
  violates table flags exactly rows 8+9 (disagree=2) matching F37CritC2Map's `req-map-2/4`; the corrected
  map passes (disagree=0). All 13 overclaim findings F1–F13 are folded in §B (I checked each row's
  anchor text; F3's `R37CritCases.md:124` line verified, F4's stderr quote verified, F9's webarena
  `:1,40-41` correction verified, F11's probe `:209`/`:235` verified, F8's `lessons/round-37.md:27`
  verified by grep).
- The F5 anchor correction is right: "the grader reads nothing from the filesystem" sits at `:162-163`
  (verified), not the overclaim seat's `:167-168`.

## 3. Q28's check — executable and shown able to fail

- Executable: `python3 plans/round38_c2_verify.py --lane . --work <scratch>` on a clean clone at the
  landing tip → `V7 ok rows=7 tags=7 bad=0`, `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0
  (receipt `c2-verify-green.txt`), byte-identical on the C2 block to the landing measure
  (`integrate/measure-final.txt`). V7's code (`round38_c2_verify.py:213-252`) matches Q28's statement:
  `derive` over the `violates=` violating set (`:205-210`), `label != want` (`:244-245`), cited-id
  membership (`:246-248`), `MAP_ROW` four-cell regex (`:66`).
- Shown able to fail (my own mutations on the committed round-38 entry in scratch, each restored and
  re-verified green):
  - label leg: `results-format` partly→enforced → `V7 DEFECT … bad=['results-format: labelled enforced,
    receipt derives partly']` (receipt `c2-counterA-label-flip.txt`);
  - citation leg: `no-x11` cites `canned-shape` (non-violating) → `bad=['no-x11: cites no case or a case
    that does not violate it']`;
  - unparsed-row leg: `debugger-works` row made three-cell → `"unparsed row '…'"` +
    `tags missing=['debugger-works']`.
  Committed corroboration: `build/R38MutC2Counter/` M1/M2 (11/11 killed) and `R38MapErratum.md`
  controls B–D show the same legs.
- Limits disclosed in Q28 itself are honest (untagged violating cases invisible; human-labeled `violates=`;
  one label per tag collapses two-clause lines; thin tag sets derive cheaply; no retro-application).
  The erratum §A.4 states the machine check cannot run on the round-37 entry (no tags, three-cell rows) —
  consistent with what I verified; the round-37 correction is hand-adjudicated and matches the replay.

## 4. Findings (low severity; both in the erratum's own apparatus, neither affects the corrected map)

1. **§A.3 misattributes `trailing-newlines` to the `:122-124` prose.** The row-9 prose at `:122-124`
   names only the four failing phenomena ("a trailing space, a `\r`, a BOM and an empty body");
   `trailing-newlines` is named in the body-normalisation group table (~`:156`) and the structural-
   consequences bullet (~`:92`). The Map seat's note said "the current prose" without a pin; the erratum
   pinned it to `:122-124`, which is wrong for that one case id. The restated cell (excluding
   `trailing-newlines` as a non-violating control) is unaffected and correct.
2. **§B F8 anchor `:222-224` misses its quoted clause by one line.** The §Negative space phrase "no run
   of the image" is at `:225` (grep-pinned); `:222-224` holds the section header and the paragraph's
   first line. This is the same anchor-drift class the erratum itself corrected for F5 (`:162-163` vs
   `:167-168`); F8's anchor was inherited from the overclaim seat's `entry:222` and not re-pinned.

Notes (not counted): the erratum's parenthetical "(that is the case-independence caveat)" for `:167-168`
is loose wording — `:167-168` is the headline-1 separation caveat; the §Case independence bullet is at
`:204-208`. Q28's "Shown able to fail: the round-37 row 9… trips the label != want leg" is demonstrated on
the round-38-format controls (M1/control B) and the standalone replay, not — as the erratum discloses — on
the round-37 entry itself; grounded, but the sentence is counterfactual absent that disclosure (R38MapRetro
tagged `trailing-newlines` as violating line 9 while the erratum does not — a disclosed judgment split that
changes no derived label).

## Evidence / receipts (`falsify/F38RevQuality/`)

- `c2-verify-green.txt` — green run at tip (V7 ok rows=7 tags=7, checks=7 defects=0, pass, exit 0).
- `c2-counterA-label-flip.txt` — label leg fires; V7 DEFECT, C2 fail, exit 1.
- `c2-counterBC-cite-unparsed.txt` — citation leg + unparsed-row leg fire; C2 fail, exit 1.
- `c2-final-green.txt` — after byte-restore (sha256 `93484367bb0cb7df…`), green again, exit 0.

VERDICT: quality-2-defects
