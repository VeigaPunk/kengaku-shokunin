# R41MutC2Counter — mutation test of `plans/round41_c2_verify.py` (round 41, wave 1)

Seat R41MutC2Counter (leaf, mutation-tester) · 2026-10-26 · lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(tip `fc79f2a`, freeze `8ef8b4f`, first recorded probe run `f774a87`).
Target: `plans/round41_c2_verify.py`, 309 lines, sha256 `cf1632b50260c48d45a85197bfd1caf10516ad8c50e4b5718da8bd9fd53aa65e`
(`cmp` vs scratch pristine: identical — the lane file was never written; all mutants are scratch copies).

**Result: 24 single-line mutants of V1–V8 + main(); 22 killed, 2 survived (one unreachable-detector, one logically
equivalent). Every kill is backed by a detector proven to fire on the pristine counter first.**

## Method

Three detector environments per mutant; a run is compared on **(stdout, exit code)**:

1. **ctrl** — the committed control `control-c2-nothing.txt` reproduced in a scratch clone: `git clone -q --shared
   <lane> $S/ctrl` (toplevel asserted), then `git -C $S/ctrl checkout -q --detach 8ef8b4fc7c6302c5` (toplevel
   re-asserted; no commit ever made). Expected pristine output: `checks=8 defects=5` (V2,V3,V4,V7,V8), rc 1.
2. **green** — a filler package built in scratch (below). Expected pristine output: `checks=8 defects=0`,
   `PREDICATE C2 pass`, rc 0.
3. **poison** — a copy of green with exactly one injected defect per check (13 poisons). Each poison was first run
   against the **pristine** counter and required to flag (all 13 fired, defects 1–3 each; `runs/pris-*.out`), so no
   kill rests on an inert detector.

- Mutants: 24 single-line replacements, each asserted to occur exactly once in the pristine source and
  `py_compile`d (`driver.py`; the 24 mutant files + `SHA256SUMS` are staged under `mutants/`).
- A mutant is **KILLED** if any detector's (stdout, rc) differs from the pristine run on the same lane; **SURVIVED**
  if identical on every environment it was run (ctrl for all, then green, then its poison).
- Every counter/gate/probe run inside the mandated envelope
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc
  --unshare-pid --die-with-parent`. Scratch `/fast/scratch/hyaku/kengaku-r41/R41MutC2Counter` (TMPDIR and
  UV_CACHE_DIR pointed into it); no writes outside scratch and this report dir; no pacman; no tool installs (none
  needed). Scratch is deleted at the end of this seat; artifacts were copied here first.

## Baselines

- **Control reproduced** (`bwrap … python3 base/pristine.py --lane $S/ctrl --work …`): `checks=8 defects=5`
  (V2,V3,V4,V7,V8), `PREDICATE C2 fail`, rc 1. Byte-diff vs the committed control: **two disclosed lines only** —
  gate P9 (`untracked=30 first=.ufo/waves/round-41/claims/c2-stage-check.txt` in the committed control, which was
  captured pre-commit in the live lane; `untracked=0` on a clean freeze checkout) and the trailing `exit=1`
  annotation (compared separately as rc). The C2 defect set and headline lines are identical.
- **Green filler**: the wave's in-flight package mirrored into scratch. The lane moved under this seat mid-run —
  between my clone and my reads, the scribe seats landed `corpus/SOURCES.md` rows S122–S124, the README index row +
  coverage bullet, and `corpus/knowledge/tb2-constraints-scheduling-grader.md` (41764 bytes, 15:52) in the lane
  working tree; the filler copies those three files verbatim from the lane tree (read-only) on top of a tip clone,
  plus index-only `git add -A` (toplevel asserted; no commit). Pristine counter on green:
  `checks=8 defects=0`, `PREDICATE C2 pass`, rc 0 — gate P10 `probe_rerun=byte-equal bytes=5775`.
- **Probe rerun cost** (measured once, envelope, lane clone): `constraints_probe.py --lane … --work …` → rc 0,
  13 s, output `PROBE-BYTE-EQUAL` to the committed receipt. Every green/poison counter run pays this once (V2→P10).

## Poison inventory (each = green copy + one edit; pristine observation quoted)

| poison | injected defect | pristine observation |
|---|---|---|
| capbyte | one byte appended to capture `README.md` | `V1 DEFECT bad=['README.md']` + gate P5 → `V2 DEFECT` (defects=2) |
| capextra | `extra.txt` + its manifest line added | `V1 DEFECT extra=['extra.txt']` only (defects=1; after re-staging — first build also tripped P9, repaired) |
| anchor | S122 anchor digest last hex char flipped | `V3 DEFECT bad=['S122:anchor_digest']` |
| mcount | receipt summary `mismatches=2`→`3` | `V4 DEFECT 'summary disagrees with the CASE lines'` + V2 (P10 rerun mismatch) |
| name | every `` `seconds-30` `` de-backticked in the entry | `V4 DEFECT "mismatch cases not named in the entry: ['seconds-30']"` |
| order | receipt `CASE nop` → `CASE nopx` | `V4 'case ids differ from the frozen table'` + V7 cite + V2 (defects=3) |
| census | S121 row used-by → nonexistent path | `V6 DEFECT census_exit=1` (census E11) |
| label | window map label `enforced`→`partly` | `V7 DEFECT 'window: labelled partly, receipt derives enforced'` |
| cite | window row cites `` `oracle-solve-sh` `` | `V7 DEFECT 'window: cites no case or a case that does not violate it'` |
| line | window row `instruction.md:1`→`:2` | `V7 DEFECT 'window: line 2 is not the frozen instruction.md:1'` |
| miss | window map row deleted | `V7 DEFECT "tags missing=['window'] duplicated=0"` |
| orderrc | `plans/order_check.py` success `return 0`→`1` (scratch copy; helper not digest-pinned by this counter) | `V8 DEFECT order_exit=1 result=not-PASS` |
| orderstr | `plans/order_check.py` success prints `ORDER RESULT FAIL`, rc 0 | `V8 DEFECT order_exit=0 result=not-PASS` |

## Mutant table (24)

| id | target | weakened clause (single line) | caught-by | status |
|---|---|---|---|---|
| M01 | V1 capture bytes | drop `sha256(capdir / n)` half of `bad` | poison:capbyte | KILLED |
| M02 | V1 extra manifest | `extra = sorted(...)` → `extra = []` | poison:capextra | KILLED — verdict-level |
| M03 | V1 digest pin | `CAPTURES["alice_calendar.ics"]` last char | ctrl | KILLED |
| M04 | V2 gate rc | `return r.returncode == 0` → `return True` | ctrl | KILLED |
| M05 | V2 spec pin | `SPEC_SHA256` last char | ctrl | KILLED |
| M06 | V3 anchor compare | `if toks != [row["sha256"]]:` → `if not toks:` | poison:anchor | KILLED |
| M07 | V4 summary agreement | drop `m == len(no)` | poison:mcount | KILLED |
| M08 | V4 mismatch naming | `unnamed = [...]` → `unnamed = []` | poison:name | KILLED |
| M09 | V4 case-id order | drop `ids != frozen_ids` | poison:order | KILLED |
| M10 | V5 dry pin | `DRY_SHA256` last char | ctrl | KILLED |
| M11 | V5 probe pin | `PROBE_SHA256` last char | ctrl | KILLED |
| M12 | V5 byte-equal | drop `r.stdout == (lane / DRY_REL).read_text()` | — | **SURVIVED** |
| M13 | V6 census rc | `return r.returncode == 0` → `return True` | poison:census | KILLED |
| M14 | V7 derive | `return "enforced"` → `return "unenforced"` | green | KILLED |
| M15 | V7 label | `if label != want:` → accept `partly` too | poison:label | KILLED |
| M16 | V7 violating set | `if tag in v` → all receipt cases | green | KILLED |
| M17 | V7 citations | drop `any(c not in violating ...)` | poison:cite | KILLED |
| M18 | V7 frozen line | `if tags[tag] != f"instruction.md:{line}":` → `if False:` | poison:line | KILLED |
| M19 | V7 missing/dup | `if missing or dup:` → `if False:` | poison:miss | KILLED |
| M20 | V8 result string | drop `"ORDER RESULT PASS" in ...` conjunct | poison:orderstr | KILLED |
| M21 | V8 order rc | drop `r.returncode == 0` conjunct | poison:orderrc | KILLED |
| M22 | V8 verdict | `return passed` → `return True` | ctrl | KILLED |
| M23 | main exit | `return 0 if defects == 0 else 1` → `return 0` | ctrl | KILLED — exit code only |
| M24 | V4 summary agreement | drop `p == cp` | — | **SURVIVED** (equivalent) |

Per-kill first-differing-line evidence for all 22 kills: `KILL-EVIDENCE.txt` (staged). Representative flips:
M01 `V1 DEFECT bad=['README.md']` → `V1 ok`; M07 `V4 DEFECT …'summary disagrees…'` → `V4 ok`; M14 green
`V7 ok rows=11 tags=11 bad=0` → `V7 DEFECT bad=['window: labelled enforced, receipt derives unenforced', …]`;
M20 `V8 DEFECT order_exit=0 result=not-PASS` → `V8 ok … result=PASS`; M23 stdout identical, pristine rc 1 →
mutant rc 0 (`base-ctrl-rc.rc` / `M23-ctrl-rc.rc`).

## The two survivors

- **M12 (V5 byte-equal clause).** Identical (stdout, rc) on ctrl, green **and** poi-mcount (`M12-*.out`). The clause
  sits behind `if sha256(lane / PROBE_REL) != PROBE_SHA256 or sha256(lane / DRY_REL) != DRY_SHA256: return False` —
  any byte change to either file flips the digest check first, so no reachable input makes the rerun output differ
  while both digests still match. It is defense-in-depth against a between-checks race, not a load-bearing decision.
  Coverage limit of any detector set built from file edits; not a counter defect. The counter is frozen and was not
  touched.
- **M24 (V4 `p == cp` dropped).** Identical on ctrl, green and poi-mcount (`M24-*.out`). Equivalence proof: the same
  conjunction enforces `p + f == n`; the ids clause enforces `len(parsed) == len(ids)` with `n == len(frozen_ids)`;
  the CASE regex admits only `observed ∈ {pass, fail}`, so `cp + cf == len(parsed) == n`; hence `p == cp ⟺ f == cf`.
  The two clauses are redundant with each other — one could be deleted without behavioral loss (a
  counter-simplification observation for a future round, not a defect).

## Findings for the L1

1. The C2 counter's decision logic is fully mutation-priced at the single-line grain: **22 of 24 killed**, every
   kill backed by a detector proven to fire on pristine first.
2. **M02 is the one verdict-level kill**: dropping V1's extra-manifest clause makes the counter print
   `PREDICATE C2 pass`, rc 0 on a package carrying an unmanifested capture file — that clause is load-bearing for
   the predicate, not just for the note. All other kills are check-level (a DEFECT line flips) or rc/note-level.
3. The committed control's `exit=1` trailer is load-bearing: M23 changes only the exit code (stdout identical).
4. V8's two conjuncts are each load-bearing, but only against a *broken* `order_check.py` — which P1 does not pin
   (it pins probe + gate only), so the poisons had to edit the helper in scratch copies. If hardening is ever
   wanted, an `ORDER_SHA256` pin in the counter would make such kills reachable without editing the helper
   [INFERENCE — the pin's effect is untested; the counter is frozen this round].
5. The round-40 "informed filler" limit (claims §C2 Limits) is priced, not just carried: a green package was
   buildable in scratch in minutes because the spec + gate fully determine the contract, and V1–V8 held against a
   faithful mirror of the in-flight package (including the L1's entry as landed at 15:52).

## Artifacts (this dir) and commands

- `RESULTS.tsv` (24 rows, as produced), `KILL-EVIDENCE.txt`, `base-ctrl.out`, `base-green.out`,
  `M12-{ctrl,green,poi-mcount}.out`, `M24-{ctrl,green,poi-mcount}.out`, `base-ctrl-rc.{out,rc}`,
  `M23-ctrl-rc.{out,rc}`, `pris-mcount.out`, `driver.py`, `mutants/` (24 mutants + `SHA256SUMS`).
- Every run: `bwrap … python3 <counter> --lane <lane> --work <dir>` (envelope above); comparison on (stdout, rc).
- Control diff: `diff .ufo/waves/round-41/claims/control-c2-nothing.txt runs/base-ctrl.out` → P9 line + exit
  trailer only.
- Probe rerun: `python3 plans/constraints_probe.py --lane $S/lane --work $S/w` → rc 0, 13 s, byte-equal.
- Scratch `/fast/scratch/hyaku/kengaku-r41/R41MutC2Counter` deleted after staging; lane untouched (pristine counter
  `cmp`-identical to the lane file; no lane path was ever written).

VERDICT: c2-counter-mutants-caught-22/24
