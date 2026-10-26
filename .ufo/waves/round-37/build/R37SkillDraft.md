# R37SkillDraft — SKILL.md registry rows + service-class grader section (draft only)

- Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, tip `44b7298`
- Scratch: `/fast/scratch/hyaku/kengaku-r37/R37SkillDraft{,2}` (removed at end; `probe-mutant-run.txt` kept)
- Wrote only: `.ufo/waves/round-37/build/R37SkillDraft.md` and `.ufo/waves/round-37/build/R37SkillDraft/`
- Did not edit `SKILL.md`, `plans/`, `corpus/`, any lane file, the lane's index or jj state.

## Axes

| axis | move this seat made | how it is measured |
|---|---|---|
| operability | four rows whose exit-code maps are read from the code, not assumed — including the one place where the exit code lies (`git-webserver-probe` exits 0 on disagreement) | one measured mutant run below; the counter row's map read from `round37_c1_verify.py:383-393` |
| depth | the service-class section turns one probe into a reusable decision table (7 failure mechanisms × probe → observed verdict → citation) plus 6 sandbox requirements | every claim carries `file:line` into the captured grader or the receipt |

## Delivered

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37SkillDraft/SKILL-r37-draft.md`
(paste-ready, 3 parts):

- **Part A** — four registry rows in the existing 8-column shape (`SKILL.md:565-576`, header `:562`):
  `git-webserver-probe`, `round37-c1-mutants`, `round37-c2`, `anchor-digest-check`. Each row validated at
  8 cells: `awk` → `17: pipes=9 cells=8`, `18: pipes=9 cells=8`, `19: pipes=9 cells=8`, `20: pipes=9 cells=8`.
- **Part B** — one `Round-37 registry addendum:` paragraph (after `SKILL.md:591`), stating the runtime cost,
  the exit-code trap, and the anchor check's red state.
- **Part C** — `## Service-class TB2 grader — round 37` (appended after `SKILL.md:711-734`): a 7-row decision
  table (echoed untrusted content · unread exit statuses · split requests · missing `-L`/timeout · exact
  compare after command substitution · catch-all server · instructed port) and a 6-item sandbox list.

Insertion points are named in the draft's header; the L1 integrates, nothing is inserted by this seat.

## Row facts and where each came from

| row | entry | exit map source | pins source |
|---|---|---|---|
| `git-webserver-probe` | `plans/git_webserver_probe.py` | `:256` `2` duplicate id · `:264` `0` dry · `:266-270` `2` capture pin / bwrap · `:281` `1` smoke only · `:303-304` summary then `0` | `PINS` `:44-47`; probe sha256 measured `63cb75cf…` |
| `round37-c1-mutants` | `plans/round37_c1_verify.py` | `:305,312` `2` · `:379-386` killed/survived increments + summary · `:389-393` dev `n/a` vs predicate | `GATE_SHA256` line 59 `ea638822…`; counter measured `dbc9f719…` |
| `round37-c2` | `plans/round37_c2_verify.py` | `:225` per-check `ok`/`DEFECT` · `:226-228` `checks=`, predicate, `0/1` | `CAPTURES` `:48-55`; `PROBE_SHA256` `:56`; `DRY_SHA256` `:57`; measured `SHA256SUMS` `e70bb662…`, spec `4c61d103…`, receipt `83550712…` |
| `anchor-digest-check` | `.ufo/waves/round-37/build/R37AnchorSweep/anchor_digest_check.py` (draft, sha256 `6d7afcd5…d9a323`; proposed `plans/anchor_digest_check.py`) | classes/output shape per the seat's report; 0/1 verified by my run below, `2` for `--evidence-ref bogus` per the seat's fixture matrix | none in code by design; resolves against `git ls-tree -r <evidence-ref> -- corpus/evidence`; the row says so |

## Measurements (command → output)

1. Probe exit code does not encode disagreement. In a shared clone
   (`git clone -q --shared <lane> "$D/lane"`, toplevel verified), one frozen prediction flipped
   (`sed -i 's/Case("no-server", "curl", {}, "fail",/Case("no-server", "curl", {}, "pass",/'`), then
   `python3 plans/git_webserver_probe.py --lane . --work "$S/w"`:
   `cases=22 observed_pass=9 observed_fail=13 mismatches=1`, `MUTANT_EXIT=0`, 1 × `match=NO`, empty stderr,
   57.92 s wall. Full stdout kept at `R37SkillDraft/probe-mutant-run.txt`. So the row must be wired by the
   summary line or by the gate's P10 byte-comparison, never by `$?` — this is the `git-webserver-probe`
   verdict-map cell.
2. C2 counter on a clean clone of `44b7298` (`python3 plans/round37_c2_verify.py --lane . --work "$S"`, 53 s):
   ```
   gate: P8 DEFECT index_rows=43 knowledge_files=43 bad=2 first=index rows for knowledge/tb2-git-webserver-grader.md=0
   gate: P9 ok untracked=0 first=0
   gate: P10 ok probe_rerun=byte-equal bytes=8443
   gate: defects=5
   V2 DEFECT gate_exit=1
   V3 DEFECT rows=3 bad=['S111:row', 'S112:row', 'S113:row']
   V4 DEFECT receipt or entry absent
   V5 ok probe=frozen dry_byte_equal=True
   V6 ok census_exit=0
   V7 DEFECT receipt or entry absent
   checks=7 defects=4
   PREDICATE C2 fail
   ```
   V1 was `ok` in the same run (7 checks, 4 defects = V2/V3/V4/V7). The probe itself is byte-reproducible:
   `P10 ok probe_rerun=byte-equal bytes=8443`. The reds are the missing C2 entry and its index rows.
3. `anchor-digest-check` draft on the lane, read-only. A first run of the seat's earlier draft (before it
   added `--evidence-ref`) printed four defects:
   ```
   DEFECT S072 anchor token=081c8264… class=digest-unknown detail=not-committed-evidence-and-not-in-a-SHA256SUMS loc=corpus/SOURCES.md:94
   DEFECT S073 anchor token=97b8671f… class=digest-unknown detail=… loc=corpus/SOURCES.md:95
   DEFECT S074 anchor token=f996dfee… class=digest-unknown detail=… loc=corpus/SOURCES.md:96
   DEFECT S110 anchor token=4f7ac05e… class=digest-short detail=63-hex loc=corpus/SOURCES.md:125
   rows=103 tokens=10 defects=4
   EXIT=1
   ```
   The seat's final draft (`sha256sum` → `6d7afcd56a95c59f835be04a16263d43db4840cc8a4b111350be4d7cb8d9a323`),
   re-run identically:
   ```
   DEFECT S070 anchor token=45ddba7b… class=digest-unknown … loc=corpus/SOURCES.md:92
   DEFECT S072 … :94   DEFECT S073 … :95   DEFECT S074 … :96   DEFECT S110 … :125
   rows=103 tokens=11 defects=5
   EXIT=1
   ```
   `/usr/bin/bwrap` present (root, 84464 bytes, 2026-10-14), so the probe's bwrap gate is satisfied here.
   The seat's own report gives `before=5`, `after=0` only with the erratum **and**
   `corpus/evidence/round37/anchor-captures/` staged (erratum alone leaves 4), and 5/5 mutants killed by
   distinct classes over an 11-case fixture matrix (`fixture_matrix.py`, `fixture-receipt.txt`).
4. Digests I measured for the rows (`sha256sum`): probe `63cb75cf…5eedf`, C1 counter `dbc9f719…`, C2 counter
   `b8cba11a…`, `pkg-spec-r37.json` `4c61d103…`, `pkg-spec-r35.json` `e085b435…`, `pkg_gate.py` `ea638822…`,
   receipt `83550712…`, capture `SHA256SUMS` `e70bb662…`.
5. Control receipts quoted in the rows: `control-c1-nothing.txt:17` `BATTERY fixtures=14 wrong=0
   renamed_disagree=0`, `:73` `MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0`, `:74`
   `PREDICATE C1 fail`; `control-c2-nothing.txt:20` `checks=7 defects=4`, `:21` `PREDICATE C2 fail`.

## Section claims, each with its location

| claim in Part C | location |
|---|---|
| verdict is a substring of the helper's stdout | `tb2-git-webserver/test_outputs.py:13` (`assert "TEST PASSED" in result.stdout`) |
| stderr and exit status unread | `test_outputs.py:11` (`subprocess.run` without `check`) |
| body echoed into stdout before the compare | `verify.sh:62` (`echo "Content: $CONTENT"`) |
| PASSED/FAILED strings | `verify.sh:64,66` |
| expect/apt-get statuses never read | `verify.sh:5-6,49` |
| scratch HOME needed (`~/.ssh/config`) | `verify.sh:9-13`; probe `HOME=/work/home` at `git_webserver_probe.py:235` |
| writable cwd (`git_test.exp`) | `verify.sh:16` |
| `/tests` absolute path | `test_outputs.py:11` |
| `curl` without `-L`/timeout, `wget` without timeout | `verify.sh:57,75` |
| status and content are two requests | `verify.sh:57,60` |
| exact compare, case-sensitive, newline-stripping | `verify.sh:63` |
| `PATH` decides which branch runs | `verify.sh:55` |
| port 8080 from the instruction | `instruction.md:7` |
| observations | receipt `corpus/evidence/round37/git-webserver-probe.txt:7,11,13,15,19,21,29,31,33,35,37,41,49` |

## Findings the L1 must decide (not fixed here)

1. **`git-webserver-probe` exits 0 on disagreement** (§Measurements 1). If any gate wires it by `$?`, a drifted
   prediction is invisible. The row states the summary-line rule and names P10's byte-comparison as the real
   reproduction check. Recommendation: keep the probe's exit map as measured and do not change the frozen
   file; the row is the guard.
2. **`anchor-digest-check` is red on five anchors, not one.** Beyond S110's 63-hex digest, the final draft
   flags S070, S072, S073, S074 (`corpus/SOURCES.md:92,94,95,96`), whose anchor cells hold 64-hex digests of
   live-fetched upstream bytes that are true but have no in-lane capture — the frozen rule
   (`…and-not-in-a-SHA256SUMS`) cannot resolve them. The seat's `after=0` requires the erratum **and** the
   promotion of `corpus/evidence/round37/anchor-captures/` (5 files, `sha256sum -c` clean); the erratum alone
   leaves 4. My row records the measured state, names the draft digest and states that it asserts nothing
   until the script lands in `plans/`; the L1 should integrate the seat's `before=5`/`after=0` pair from
   `.ufo/waves/round-37/build/R37AnchorSweep.md` (which is where the promotion step is specified).
3. **`round37-c2` V6 depends on an absolute path outside the lane** (`round37_c2_verify.py:58`,
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`), so the row's self-test is not runnable from a
   foreign checkout; the row says so instead of implying portability.
4. **C1 development modes weaken the predicate silently.** `--only`/`--battery-dir`/`--battery r36` print
   `PREDICATE C1 n/a` and exit 0 on a pass of the narrower rule (`round37_c1_verify.py:389-391`); the row
   spells out that only the default invocation counts. A reader who runs `--only M01` and sees `killed` must
   not read that as a class demonstrated.
5. **Probe runtime is ~58 s and needs `/usr/bin/bwrap`** — a host without bubblewrap gets exit `2`, which the
   row records as setup, not as a failed claim.

## Not done (out of scope for this seat)

- No edit to `SKILL.md` (L1 integrates Part A/B/C).
- No C1 battery development and no C1 counter run: `plans/battery37/` does not exist yet in the lane
  (`BATTERY_REL` at `round37_c1_verify.py:57`), and the full mutant sweep belongs to the battery seats. The
  C1 row's kill counts are quoted from `control-c1-nothing.txt`, not re-measured here.
- No C2 entry, index rows or requirement map: that is R37PkgDraft's artifact; I measured the counter's state
  (V2/V3/V4/V7 red) without producing it.
- No claim about `tests/test.sh` reward wiring beyond what the round-37 entry seat writes.

## Limits

- The service-class verdicts are one executed probe under `apt-get`/`expect` absent; the oracle is not run
  and no case performs a real push (`plans/git_webserver_probe.py:21-23`), so the section states what the
  grader's verdict depends on, never that the intended path passes.
- The `anchor-digest-check` row rests on two read-only runs of the seat's draft (earlier 4 defects, final
  sha256 `6d7afcd5…` 5 defects) plus its report; the draft file, its `captures/` staging and its erratum may
  change before landing, and the row says the `0` state is conditional on both landing.
- The C1 row's pinned values are file digests I measured at `44b7298`; if the L1 lands the battery before
  integrating the row, only the counter and gate digests stay frozen — the row says which pins are frozen.

VERDICT: skill-drafted-4-rows
