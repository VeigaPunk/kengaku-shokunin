# C1DecoupledAuditR74 — audit of decoupled discovery in `plans/round74_c1_registry.py` (R74-C1)

Round 74 w1, seat C1DecoupledAuditR74, reviewer role. Claims read in full including
**Amendment A1** (committed `74e2e15`, correcting the R74-C1 Before description; predicate,
counting command, after-target, control and kill rule unchanged). Lane tip at audit time:
`74e2e15abab4095f7b94f171a837f8b913d58a1f`; only `SKILL.md` modified in the working tree
plus untracked `.ufo/waves/round-74/*`. The two C1/C2 scripts are committed clean at HEAD
(`git diff --stat HEAD -- plans/round74_c1_registry.py plans/round74_c2_registry_audit.py`
is empty). All fixtures and mutations were done in
`/fast/scratch/hyaku/kengaku-r74/C1DecoupledAuditR74/` (cleaned up before this report was
finalized); the lane itself was never mutated — read-only counter runs plus one `cp -a`
working-tree copy (noted under Method deviations).

## Verdict: all four audit items PASS. No counter defect found. One receipt-fidelity finding (MEDIUM).

## Frozen-predicate spot check at the current tip (context for the items)

`python3 plans/round74_c1_registry.py --lane .` → `UNIVERSE mode=decoupled files=136
plans_seen=90 self_advertising_prevented=True`, `ADVERTISED total=116`,
`REGISTERED total=116 rows=116`, `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`,
`SELFTEST-UNBACKED 0`, `DUPLICATE 0`, `PREDICATE R52-C2 pass`, `PREDICATE R74-C1 pass`,
rc 0 — every line of the frozen after-target present and exact.
`--selftest` → `SELFTEST cases=4 failures=0`, rc 0.
`--universe legacy` on the live lane → `files=78 plans_seen=0 plans_only=0`,
`ADVERTISED total=115`, `REGISTERED total=115 rows=116`, `MISSING 0`,
`PREDICATE R52-C2 pass`, `PREDICATE R74-C1 fail`, rc 1 — matches Amendment A1's corrected
Before description verbatim and the committed receipt
`corpus/evidence/round74/c1-before.txt` (receipt exists, byte-equal on all counted lines).
The 116→115 rows gap in legacy is the hyphenated census row: legacy regex cannot parse it —
the pre-round-74 flaw the claim fixes.

## Item results

### 1. `self_assessment_files(lane, 'decoupled')` excludes the `## Gate/probe registry` block — PASS

Evidence (live lane, module imported from `plans/round74_c1_registry.py`):
- Scanned source set is exactly: `SCORECARD.md`, `LOG.md`, `corpus/README.md`,
  `SKILL.md (outside registry)`, `corpus/knowledge/*.md` (79 files), `plans/*.md` (36 files)
  — 136 entries.
- Structural: the returned `SKILL.md (outside registry)` text equals full SKILL.md minus the
  block span `stext[:i] + stext[j:]` where `i = find("## Gate/probe registry")` (SKILL.md
  line 587; heading carries the suffix "(PROTOCOL §Gate standard)", matched as prefix) and
  `j` = next `\n## ` (line 805). Byte-equality check passed (133,898 chars).
- Content: none of the block's 116 data rows (`len(data_rows)==116`) appears verbatim in any
  scanned text; the heading string is absent from the outside text; the in-block prose note
  ("… never the exit code", line 804) is absent from the outside text. Control: legacy mode
  scans SKILL.md whole (heading present) — the asymmetry the claim describes.

### 2. Phantom registry row does not self-advertise — PASS

Fixture with the registry block as final section (mirroring the in-script selftest arm 3):
- Baseline clean: adv=4, reg=4, rows=4, MISSING 0.
- Appending row `phantom → plans/phantom.py` (file created): rows=5 (parsed as a registry
  row), `plans/phantom.py` IS in reg, NOT in adv, MISSING 0, ENTRY-MISSING 0. No circular
  self-advertising.
- Ghost variant (row pointing at an absent file): row registered, not advertised, and
  `ENTRY-MISSING 1` flags the absent entry — so registry-only rows are never silently
  accepted when their script is missing.
- Placement checks: a table-syntax line inserted INSIDE the block (before a trailing `## `
  heading) is registered and not advertised (rows=5, adv_has=False); the same line appended
  AFTER a trailing section is not a registry row (rows=4) and is advertised as prose.
  Consistent heading-anchored semantics, not a defect.

### 3. Removing an advertised instrument's row → immediate `MISSING 1` — PASS

- Fixture leg: `plans/tool_b.py` advertised only via a `plans/*.md` doc (the decoupled-only
  source class). Dropping its row: decoupled prints `MISSING 1` naming `plans/tool_b.py`,
  rc 1. Same fixture under legacy: the instrument disappears from adv AND reg
  (`ADVERTISED total=2`, `REGISTERED total=2 rows=3`, `MISSING 0`, `PREDICATE R52-C2 pass`)
  — the frozen control's false green, reproduced. (rc is still 1 via the `R74-C1` leg, which
  by design requires `universe == "decoupled"`; see Finding N3.)
- Real-lane leg: on a scratch `cp -a` copy of the working tree whose SKILL.md was
  byte-identical to the lane's at run time, dropping the single `| \`round74-c2\` |` row
  (SKILL.md line 707; `round74_c2_registry_audit` appears nowhere else in SKILL.md) makes
  the frozen command print `MISSING 1` + `  MISSING plans/round74_c2_registry_audit.py`,
  `REGISTERED total=115 rows=115`, rc 1. Same copy under `--universe legacy`: `MISSING 0`
  (instrument dropped from both sides — false green). Exactly the discrimination the claim
  asserts for `plans/round74_c2_registry_audit.py`.

### 4. Hyphenated paths matched by `CMD` — PASS

- `CMD.search("python3 corpus/evidence/round13-coverage/coverage_census.py")` matches the
  full path; `CMD_LEGACY` does not (the `[A-Za-z0-9_]+` flaw). Hyphenated file names under
  `plans/` match too (`plans/round-74-claims-view.py` probe).
- Live: census is advertised in decoupled (sources: `SKILL.md (outside registry)` +
  `plans/round-74-claims.md`) and invisible in legacy — the round-73 blind spot is closed.

## Findings by severity

- **MEDIUM — committed control receipt does not demonstrate the frozen control's legacy
  false-green leg.** `corpus/evidence/round74/c1-control-decoupled.txt` legacy arm prints
  `ADVERTISED total=3`, `REGISTERED total=2 rows=2`, `MISSING 1`, `PREDICATE R52-C2 fail`,
  rc 1 — legacy *detects* the drop there, because that fixture advertises `plans/tool_b.py`
  from a legacy-scanned file (its decoupled arm shows `files=4 plans_seen=0`, so no
  plans/*.md advertisement exists). The frozen control sentence requires a fixture whose
  only advertisement is `plans/*.md`-visible (then, and only then, legacy drops the
  instrument from both sides). I verified the false green IS reproducible with exactly such
  a fixture (above), so the mechanism is real — but the receipt evidences a weaker case and
  a reader comparing receipt to claim will see a contradiction. The kill rule does not
  reference the control receipt, so this does not fail the claim; recommend the L1 either
  regenerate the receipt from a plans/*.md-only-advertisement fixture or annotate it.
- **LOW (residual) — `CMD` hardcodes the single hyphenated evidence path.** The
  `[A-Za-z0-9_.-]+` class is general only under `plans/`; `grader.py` and
  `corpus/evidence/round13-coverage/coverage_census.py` are literals. A future
  `corpus/evidence/<other-hyphen-dir>/x.py` verdict instrument is invisible in BOTH
  universes (probe returned None). Satisfied for the frozen grounding set; scope note only.
- **LOW (residual, latent) — block boundary is "next `\n## ` heading".** A line starting
  with `## ` inside a fenced code block within the registry section would truncate the
  block early: tail rows would go unparsed and tail prose would become scannable (a
  potential circular-leak path). Not present in the live lane (no fence lines between
  SKILL.md lines 587–804; all 116 rows parsed).
- **NOTE — advertisement provenance of the two newest rows.** `plans/round74_c1_registry.py`
  and `plans/round74_c2_registry_audit.py` appear in SKILL.md only inside their registry
  rows (lines 706/707); their entire decoupled advertisement comes from
  `plans/round-74-claims.md`. If that grounding string were ever reworded away, dropping the
  corresponding row would become undetectable by MISSING (adv and reg would both lose it).
  Inherent to the anti-circular design; the claims doc is the intended anchor.
- **NOTE — rc semantics under legacy.** `verdict()` returns 1 for every legacy run
  (`r74` requires decoupled + plans_seen ≥ 1), so the control's "falsely remaining green"
  means `MISSING 0` + `PREDICATE R52-C2 pass`, not rc 0. Matches Amendment A1's wording
  ("can never satisfy `PREDICATE R74-C1`") and the c1-before.txt receipt (rc=1).
- **NOTE — `parse_rows` silently drops non-8-column lines in C1** (INCOMPLETE covers only
  empty cells among parsed rows). Malformed rows are R74-C2's `MALFORMED-ROW` defect class,
  so the C1+C2 pair has no gap, and a malformed row for an advertised instrument still
  yields C1 `MISSING 1` (row lost from reg).

## Method deviations / honesty notes

- Rule 4 names `git clone --shared` for mutation tests; the clone (HEAD `cea7ebf3`) went
  stale when A1 landed (`74e2e15`), so the real-lane leg used a fresh `cp -a` of the working
  tree instead (refreshed after 74e2e15; `cmp` confirmed byte-identity with the lane's
  SKILL.md at run time; `git rev-parse --show-toplevel` asserted on the copy). The lane was
  never mutated; all writes were under the seat scratch dir.
- My first two driver revisions had fixture bugs (rows appended after a trailing `## `
  section; false-green fixture advertised via LOG.md; over-broad leak/heading matchers).
  Those failures were mine, not the script's; the final driver run is the evidence above.
- Receipts `c1-before.txt` (matches live legacy run and Amendment A1) and
  `c1-control-decoupled.txt` (see MEDIUM finding) were read; no other receipts were
  re-executed. R74-C2 script behavior is out of this seat's scope beyond the C1 side of its
  registry row.

Scratch directory cleaned up. No lane files were modified by this seat.
