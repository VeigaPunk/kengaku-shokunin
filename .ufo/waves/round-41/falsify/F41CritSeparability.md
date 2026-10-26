# F41CritSeparability — round 41 wave 2 (falsify): are C1 and C2 separately admissible?

Seat: F41CritSeparability (leaf critic). Lane: `kengaku-shokunin`, HEAD `d7c77895752a2a5f317fa22f2362416ada50a04b`
(wave-2 dispatch), assigned tip `3d0058fbde484c9d6c23fd997d9ee09a0663bcdb` also measured. Frozen digests verified at
clone: `sha256sum -c .ufo/waves/round-41/claims/frozen-digests.txt` → all 11 `OK`.
Scratch: `/fast/scratch/hyaku/kengaku-r41/F41CritSeparability` (clones A–I, removed at the end). Full receipts are
copied to `.ufo/waves/round-41/falsify/F41CritSeparability/` (13 `.txt`/`.out` files + two strace logs).

Every counter/battery run below was executed inside the mandated envelope:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
      /usr/bin/python3 plans/round41_c{,1,2}_verify.py --lane . --work <scratch>
```

Nesting verified first: `bwrap <envelope> bwrap --ro-bind / / ... python3 -c 'print("nested-ok")'` → `nested-ok`.

## 1. The two acceptance runs (each product deleted in its own clean clone, deletion committed)

### A — C2's work product deleted, C1 run

Clone A = tip clone; deleted C2's bytes: `corpus/knowledge/tb2-constraints-scheduling-grader.md`,
`corpus/evidence/round41/constraints-probe.txt`, the ten captures + `SHA256SUMS`, the dry table, `pr245-body.md`;
`git checkout 8ef8b4f -- corpus/SOURCES.md corpus/README.md PROVINCE.md` (the freeze→landing diff shows every
addition in those three files is C2's: `SOURCES +3` = S122–S124, `README +19` = index row + coverage bullet +
§Frontier sub-bullet, `PROVINCE +61` = the Round41 admission section); `SKILL.md` lost the two C2 registry rows
(`round41-c2`, `constraints-probe`) and the `## Scheduling-constraint TB2 grader — round 41` section, and the two
C2 sentences in the shared addendum. Diffstat: `19 files changed, 1 insertion(+), 1467 deletions(-)`.
`SKILL.md` line 573 in clone A is still `| `sources-adopt` | gate | ...` (measured, section 5).

```
$ bwrap <envelope> /usr/bin/python3 plans/round41_c1_verify.py --lane . --work <scratch>
PINS total=2 mismatched=0
FIXTURE ... 48 lines, every one "ok" ...
MUTANT T01 receipts error killed by=r_setup-t01-lane-absent -- ...
... 23 MUTANT lines, every one "killed by=<fixture>" ...
BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=13/13 sources=10/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 pass
EXIT=0
```

C1 is green with every C2 byte removed (entry, rows, README/PROVINCE/SKILL text, receipt, captures, dry table).
The identical run in clone G (the acceptance's exact named set, captures/dry table kept, SKILL untouched) is also
`BATTERY fixtures=48 wrong=0 ... PREDICATE C1 pass` (receipt `G-c2.txt`).

### B — `plans/battery41` deleted, C2 run

Clone B = tip clone, `git rm -r plans/battery41` (7 modules, 894 lines), committed.

```
$ bwrap <envelope> /usr/bin/python3 plans/round41_c2_verify.py --lane . --work <scratch>
V1 ok listed=10 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=29 distinct_quotes=29 distinct_lines=29 out_of_word_range=0
    gate: P4 ok checked=29 bad=0 first=0
    gate: P5 ok manifest_entries=10 bad=0 first=0
    gate: P6 ok rows=2 bad=0 first=0
    gate: P7 ok source_lines=2 bad=0 first=0
    gate: P8 ok index_rows=48 knowledge_files=48 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=5775
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=25 mismatches_named=2/2 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=11 tags=11 bad=0
V8 ok order_exit=0 result=PASS
checks=8 defects=0
PREDICATE C2 pass
```

Both acceptance runs pass: **the two predicates are separable in the required direction.**

## 2. Specificity controls — the converse reds (so the greens are not vacuous)

| clone | mutation | C1 | C2 |
|---|---|---|---|
| A | C2 product deleted (incl. captures/dry) | `fixtures=48 … killed=23` **pass** | `checks=8 defects=7` **fail** (V1,V2,V3,V4,V5,V7,V8) |
| G | exact named C2 set (captures/dry kept) | **pass** | `checks=8 defects=5` **fail** (V2,V3,V4,V7,V8) |
| B | `plans/battery41` deleted, committed | `BATTERY fixtures=0 … killed=0 survived=23` **fail** | **pass** |
| H | pristine tip | **pass** | **pass** |

- G's red is exactly the freeze control: `claims/control-c2-nothing.txt` is `checks=8 defects=5` with the same five
  V-numbers. Deleting only C2's own bytes reproduces the do-nothing control.
- A's extra two defects are V1 and V5, i.e. deleting the capture manifest and the frozen dry table binds exactly
  those two checks (delta explained, no hidden dependency).
- B's C1 output is line-for-line the C1 freeze control (`claims/control-c1-nothing.txt`): `fixtures=0`,
  `killed=0 survived=23`, `PREDICATE C1 fail`. `plans/battery41` is C1's own work product, so this is the expected
  direction.

Replication at the **assigned** tip `3d0058f` (clones E, F; `git diff --stat 3d0058f..HEAD` = only
`.ufo/waves/round-41/falsify-{spec,dispatch}.json`): E (C2 product deleted) → `BATTERY fixtures=48 … PREDICATE C1
pass`; F (`battery41` deleted) → `checks=8 defects=0 … PREDICATE C2 pass`. The result is not an artifact of measuring
the newer tip.

## 3. Byte-level audit (strace) — each counter opens a disjoint lane set

At the pristine tip H, with both products present, `strace -f -e trace=openat,openat2` on each counter:

C1's lane opens (unique): `plans/battery41/` and its 7 modules, `plans/tip_receipts.py`,
`plans/sources_adopt.py`, `plans/round41_c1_verify.py` (self). Grep for C2 identifiers in the trace:
`grep -E 'constraints|S12[234]|pkg-spec-r41|round41_c2|tb2-constraints' H-c1.strace | grep '/H/'` → **no lines**.

C2's lane opens (unique): the entry, the receipt, the dry table, the ten captures, `corpus/SOURCES.md`,
`corpus/README.md`, `plans/{constraints_probe.py,order_check.py,pkg_gate.py,pkg-spec-r41.json,round41_c2_verify.py}`.
Grep for C1 identifiers: `grep -E 'battery41|tip_receipts|sources_adopt|round41_c1' H-c2.strace | grep '/H/'` →
**no lines**.

Source confirmations: `grep -n 'constraints\|S122\|pkg-spec-r41\|round41_c2' plans/round41_c1_verify.py` → none;
`grep -n 'tip_receipts\|sources_adopt\|battery41\|round41_c1' plans/round41_c2_verify.py` → none.
(The only `SKILL.md:573` / witness strings in the C1 counter are `adv`/`witness` cell text, never opened: line 121-122
are constants used only in f-strings.)

## 4. Robustness: uncommitted deletions, and the `--require-clean-tree` claim

- Clone D (battery41 intact, C2 entry/rows/README/PROVINCE/receipt deleted **uncommitted**): C1 still
  `PREDICATE C1 pass`. Clone C (battery41 deleted uncommitted): C2 still `checks=8 defects=0`.
- Clone I (battery41 deleted uncommitted, `git status` shows 7 ` D plans/battery41/*`): gate `P9 ok untracked=0` and
  `V2 ok ... gate_exit=0`, `PREDICATE C2 pass`. Cause: `plans/pkg_gate.py:259-265` defines `c_clean_tree` as
  `git ls-files --others --exclude-standard` only — it counts untracked files, not modified/deleted tracked ones.
- So separability does not depend on the deletion being committed; and C2's own note "`pkg_gate.py package
  --rerun --require-clean-tree`" (counter docstring line 18-19) does not mean the tree is clean, only that it has no
  untracked files.

## 5. Findings (what holds, what breaks, impacted axes)

### H1 — Cross-separability HOLDS at the predicate and byte level (C1 admission, C2 admission)
C1 green with all C2 bytes gone (A, G, E); C2 green with `plans/battery41` gone (B, F, C, I); the file-open audit
shows zero overlap. No counter reads the other claim's product.

### B1 — C1's own documentation is NOT separable from C2's receipt (C1 documentation axis; not the predicate)
Clone A removed only C2 bytes, yet `SKILL.md`'s round-41 addendum (C1's registry prose, lines 659-661 in A) still
reads: "the round-41 receipt reproduces `equal bytes=5775` in ~54 s" (lane `SKILL.md:667-668`) and lists
`round41/constraints-probe.txt` among "3 derived receipts". After the deletion that receipt does not exist, so C1's
advertised measurement names a withdrawn C2 artefact and its "3 derived receipts" count can no longer be reproduced
from the tree. Nothing reads it, so the predicate is unaffected.
Smallest safe correction: at the next unfrozen edit, re-measure that sentence to name only `round39/git-leak-probe.txt`
and `round40/db-wal-probe.txt`, or mark the round-41 receipt "withdrawn with C2" in the same sentence.

### B2 — `SKILL.md:573` is a positional citation that survived this deletion by luck, not by construction (C1 provenance axis)
C1's 10 `sources` mutants quote `SKILL.md:573` as the `sources-adopt` row (counter lines 189-231). It is still that
row in clone A because every round-41 C2 SKILL addition sits *below* line 573 (rows at 596-597, section at 1059).
Any future insertion above 573 (e.g. a new registry row ordered before `sources-adopt`) silently retargets ten
advertisement citations while the counter stays green — the counter never reads `SKILL.md`.
Smallest safe correction: cite the row key plus the row's sha256 (`| `sources-adopt` | … | sha256 …`) instead of a
line number, or derive the line from the row key at freeze time.

### B3 — C2's V6 is a fleet-root dependency, not a lane-only check (C2 admission / portability axis)
`plans/round41_c2_verify.py:82` hardcodes `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`.
Masking only that fleet directory in the envelope (`--tmpfs /home/vgpnk/Projects/shokunin/scripts`) with every C2
byte present yields
`V6 DEFECT error FileNotFoundError: [Errno 2] No such file or directory: '/home/vgpnk/Projects/shokunin/scripts/sources-census.sh'`,
`checks=8 defects=1`, `PREDICATE C2 fail`. This is not C1-coupling, but it means C2's green is a property of this
fleet root, not of the lane clone the predicate claims to measure. Smallest safe correction: resolve the census the
way `plans/round_close.py:138-150` does (`--census PATH`, then `$SHOKUNIN_ROOT`, then lane parents) and keep the
absolute path only as the last fallback.

### B4 — C2's V2 "clean tree" wording overclaims (C2 evidence axis)
`--require-clean-tree` accepts 7 tracked deletions (clone I, §4). This makes C2's separability test easier, never
harder, and V4/P10 still catch a deleted receipt; but the counter's V2 note and the package gate registry row should
say "no untracked files" or add `git diff --quiet HEAD` to `c_clean_tree`. No predicate change is needed for
admission; it is a documentation-accuracy defect in `plans/pkg_gate.py:259-265`'s flag name.

### H2 — The green is the same result whether the deletion is committed or not (calibration)
A/G/B (committed) and C/D/I (uncommitted) agree on every cell. The acceptance does not depend on commit state, and
C1 has no clean-tree requirement at all.

## 6. Limits of this review

- I attack separability only; mutant *count/attribution* (are 23 the right 23?) and C2 prose *quality* are other
  seats' assignments. Nothing here says the battery modules are free of the wave-1 counter vectors
  (`R41CritC1Counter` A1′/A3/F2-F4, `R41SentinelCounter` F1) beyond what the counter's own `sidechannel=0`,
  `tampered=0`, `wrong=0` measure.
- The prose surfaces (SKILL/README/PROVINCE entry) are deleted as data; I did not judge their wording. `QUALITY.md`
  Q31/Q32, `corpus/routed-findings.jsonl` and `plans/routed_open.py` were not part of the named C2 work-product set
  and were left in place (neither counter opens them; the C2 trace confirms).
- The strace audit traces `openat/openat2` only; `stat`/`readlink` of C2 paths by C1 would not appear, but C1's
  `BATTERY fixtures=48` green with those paths absent (A, G) is the behavioural version of the same claim.
- `ENOENT` probes for `uv.toml`/`pyproject.toml` appear in the C2 trace (package-manager style upward search, no
  lane byte read); they do not affect any check.

## 7. Host safety / write scope

- No writes outside `/fast/scratch/hyaku/kengaku-r41/F41CritSeparability` and
  `.ufo/waves/round-41/falsify/F41CritSeparability/`; no `date +%T` stamp was needed outside those paths because
  there were none.
- `/home/vgpnk/.local/bin` untouched; `ls -l /home/vgpnk/.local/bin/git` → `no git in ~/.local/bin` after the runs;
  every run used the read-only `--ro-bind` envelope above.
- Lane: `git -C <lane> status --porcelain --untracked-files=no` → empty; HEAD unchanged `d7c7789`. Clones A and B
  are clean after their runs (`status --porcelain --untracked-files=no` empty); no lane file, index, or jj state was
  touched, and no git mutation ran in the lane.
- No tools installed or upgraded (nothing was needed). Scratch dir removed after the receipts were copied.

VERDICT: separable-both
