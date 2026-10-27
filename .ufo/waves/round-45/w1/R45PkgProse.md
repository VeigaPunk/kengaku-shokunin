# R45PkgProse — kengaku round 45 wave 1, prose deltas for the `password-recovery` package

Seat: scribe (leaf; no subagents, no counter/fixture/probe run, no lane write). C2 prose only.
Lane read: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at tip `9d5f971` + uncommitted round-45 drafts
(claims frozen at `b4fcd351`). Nothing frozen was touched: this seat wrote **no** file under `corpus/`,
`plans/`, or any lane root file; drafts live in
`.ufo/waves/round-45/w1/R45PkgProse/` (5 files, 32 KB total).

## Axes named (before drafting)

| axis | what this seat can move | how it moved |
|---|---|---|
| **coverage** | C2's claim is coverage; the prose is the surface a reader lands on | 5 paste-ready deltas that carry file:line evidence, not adjectives |
| **adjacency** | each delta must sit at the exact byte the previous round used, so the pattern is visible | every anchor given as `file:line` + length + sha256 + neighbour line |
| calibration / novelty / depth / operability / freshness | not this seat's | untouched; no instrument run, no claim upgraded |

## Deliverables (5, as assigned)

| # | item | draft file | sha256 |
|---|---|---|---|
| 1 | `corpus/README.md` knowledge index row (tenth → eleventh) | `01-readme-index-row.md` | `e1f88d0df252e9a80405f8d5ceb19552e300a49aeb3da1bc0f6a252678d3fba5` |
| 2 | `corpus/README.md` §Frontier narrowing bullet (`10 of 89` → `11 of 89`) | `02-frontier-bullet.md` | `73ea6881540dc21210b7b126c1f254e249354dcfab36391106a45c1e7b1694e4` |
| 3 | `corpus/README.md` §Coverage map bullet (eleventh task) | `03-coverage-map-bullet.md` | `329e6fb0debfaa1fc2affb4e7e7fab37b97655f0dc2b88ee00fdbb179ccf00b4` |
| 4 | `PROVINCE.md` round-45 grader-class paragraph | `04-province-paragraph.md` | `50059979592502f66ea276199feba8bf155f94498405b678d6b8649a6fa1c25e` |
| 5 | `LOG.md` round-45 C2 bullet block (+ optional section heading) | `05-log-c2-block.md` | `5c2f3ee262f14d8b89513bec0ddc6b71a62bfc76918147a83b0d2df085fcd72c` |

Each draft file carries: the byte-exact anchor (line number, byte length, sha256, the neighbouring line), the
unified diff to paste, the gate check the text is written against, and the paste preconditions.

## Anchors found (the exact current wording the assignment asked me to locate first)

| surface | line | bytes | sha256 of the anchor line | neighbour |
|---|---|---|---|---|
| `corpus/README.md` knowledge index | 77 (round-44 row, `tb2-feal-linear…`) | 812 | `c629106e…16092` | `:78` = `\| \`lessons/round-1.md\` \| …` |
| `corpus/README.md` §Frontier, round-44 sub-bullet | 425–427 (the clause `(10 of 89 read)` is at `:425`) | 1235 / — / — | `b31d77b2…ce3e5` (`:425`), `b6994896…78b6` (`:427` = `    behaviour.`) | `:428` = `- **Contamination transparency cards**` |
| `corpus/README.md` §Coverage map, tenth-task bullet | 303 | 411 | `105b0cd2…95e79` | `:304` = ninth-task bullet |
| `PROVINCE.md` round-44 paragraph (EOF) | 644 (last of 644) | one line | `d0701d0c…59d0` | file ends `…are not this lane's.\n` |
| `LOG.md` last line (round-44 shape bullet) | 1372 (last of 1372) | — | `dcfb087a…22a63` | round-44 heading `:1337`; round-44 C2 bullet `:1351-1357` |

Commands (read-only; no instrument executed, so **no ENVELOPE lines apply** — the envelope gates counter,
fixture and probe runs, and this seat ran none):

```
for spec in "77 corpus/README.md" "303 corpus/README.md" "425 corpus/README.md" "427 corpus/README.md" \
            "644 PROVINCE.md" "1372 LOG.md"; do set -- $spec; printf "%s:%s " "$2" "$1"; \
            sed -n "${1}p" "$2" | sha256sum | cut -d' ' -f1; done
→ corpus/README.md:77 c629106eb51779429eabbe413f4260f4c110570ffe73fe6f4cb4426417516092
→ corpus/README.md:303 105b0cd2f83d0e8ce0401020c39874b34d6ece5ac0b516e98a70ea2d63895e79
→ corpus/README.md:425 b31d77b2fe84d29bef223a149d070e74221a85e43d412f4897682829133ce3e5
→ corpus/README.md:427 b699489674439c98a06deb1fbe5987ad16c192e5b80b7e626c3f26c35ac978b6
→ PROVINCE.md:644 d0701d0c04c417af508203d880519a54c8fdd2754e5cf1210cb333da97f159d0
→ LOG.md:1372 dcfb087ac9a61af49100cf48cfdd672f1ba8589a827def4d019be43b36e22a63
```

## The one substitution in three places: `<<P>>` / `<<F>>`

`corpus/evidence/round45/password-recovery-probe.txt` **does not exist yet** at draft time
(`ls corpus/evidence/round45/` → `password-recovery-dry-cases-freeze.txt  tb2-password-recovery`; seat
`R45ProbeFirst` owns the first recorded run). So no draft states an observed count. Items 2, 4 and 5 each carry
`observed_pass=<<P>> observed_fail=<<F>>`, to be filled from the receipt's own summary line (printed by
`plans/password_recovery_probe.py:358`):

```
cases=16 observed_pass=P observed_fail=F mismatches=0        # plans/password_recovery_probe.py:358
regrade cases=16 differ=0                                    # plans/password_recovery_probe.py:357
```

The frozen dry table's `cases=16 predicted_pass=5 predicted_fail=11`
(`corpus/evidence/round45/password-recovery-dry-cases-freeze.txt:26`) is a **prediction** and is not pasted as
an observation. Per the frozen kill rule, `mismatches` ≠ 0 makes the receipt defective, and then none of items
2, 4, 5 may be pasted.

## Findings (evidence-bearing, cheap to fix before integration)

1. **V9 forces the PROVINCE paragraph onto one physical line.** `plans/round45_c2_verify.py:326-327`:
   `any(TASK in l and name in l for l in province.splitlines())` — `password-recovery` **and**
   `tb2-password-recovery-grader.md` must share a line. Rounds 35–43 wrote *wrapped* PROVINCE prose
   (`:570`-style sections), so a writer copying that style would fail V9 with prose that reads identically.
   Item 4's paragraph is one line for this reason.
2. **PROVINCE shape diverged at round 44 and my model follows the divergence, not the older habit.** Rounds
   35–43 open `## RoundNN partial frontier admission (2026-10-26)` sections (`:192`, `:204`, `:213`, `:230`,
   `:242`, `:264`, `:287`, `:369`, `:419`, `:470`, `:537`, `:570`); round 44 has **no** such heading — it is a
   single paragraph appended at EOF (`:644`). `grep -n "Round 43\|Round 44 (2026" PROVINCE.md` returns only
   `:644`. Item 4 says: keep the round-44 precedent, do not add a `## Round45` heading (a heading neither helps
   nor hurts V9; the L1 may add one for symmetry without breaking the check).
3. **The §Frontier count is per-bullet, so the `10 of 89 → 11 of 89` move is an append, not an in-place
   rewrite.** `corpus/README.md:425` records round 44's count at its own state; editing it would rewrite round
   44's observed record. Item 2 appends a round-45 sub-bullet whose clause reads `(11 of 89 read)`, matching the
   frozen claims' "§Frontier narrowing (11 of 89)". **This is the one place my reading of the assignment and the
   repo's own history differ from a literal "change 10 to 11"; reported, not silently chosen.**
4. **The §Coverage map is already out of chronological order** (`:303` tenth, `:304` ninth). Item 3 inserts the
   eleventh bullet after `:303` (so 10th and 11th are adjacent); inserting after `:304` would give 8th, 10th,
   9th, 11th. Either satisfies gate P8; adjacency argues for after `:303`.
5. **Gate P8's two hard constraints on my prose** (`plans/pkg_gate.py:29,238-247`): the index row must match
   `^\|\s*`(knowledge/[^`]+\.md)`\s*\|` and cite **every** registry id (`S149`…`S156`, from
   `plans/pkg-spec-r45.json`); the coverage bullet must be a `- ` line containing both `tb2-password-recovery-grader.md`
   and the receipt **relative to `corpus/`** — `evidence/round45/password-recovery-probe.txt`
   (`receipt_rel = spec["receipt"].split("/", 1)[1]`), not a `corpus/evidence/…` prefix. Items 1 and 3 comply.
6. **The graded constant is published twice upstream, which is the class point, not an accident of capture.**
   `README.md:31` prints `8XDP5Q2RT9ZK7VB3BV4WW54` in the task's own verification prose; `setup.sh:25` seeds it
   with `echo "PASSWORD=8XDP5Q2RT9ZK7VB3BV4WW54"`. The grader then requires the *bare* value as a whole line
   (`test_outputs.py:18`), so the file's own format fails (`password-eq`) while a copy of the published answer
   passes (`constant`).
7. **`test_outputs.py:16` cannot fire.** `Path(...).read_text().strip().split("\n")` never yields an empty list
   (`''.split('\n') == ['']`), so `assert len(guesses) > 0` is dead on every input; the membership assert at
   `:18` is the only live predicate besides existence at `:8-10`. Stated as such in items 1, 2, 3, 5.
8. **`solve.sh` is cwd-dependent.** `solution/solve.sh:51` sets `OUTPUT_FILE="recovered_passwords.txt"`
   (relative); the oracle lands at the graded path only because `environment/Dockerfile:20` sets `WORKDIR /app`.
   The frozen case `under-varsea` (dry table `:25`) is exactly this failure. Item 5 records it; no case verdict
   is asserted beyond the frozen prediction.
9. **V11's numbers for this task are read from the control, not inferred.** `.ufo/waves/round-45/claims/control-c2-predictor.txt`:
   `CONTROL predictor=membership V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0` — 18/30, i.e. the
   16-kind `random.Random(45)` state table is mostly failing, unlike round 44's balanced 24/24. Item 5 cites this
   line and not a post-admission counter run (which this seat did not perform).

## Touched surfaces

None in the lane. Written: `.ufo/waves/round-45/w1/R45PkgProse.md` (this report) and
`.ufo/waves/round-45/w1/R45PkgProse/{01..05}-*.md`. Scratch `/fast/scratch/hyaku/kengaku-r45/R45PkgProse` was
**not created** — no command ran that writes a relative path, and no counter/fixture/probe was executed. No tool
installed, upgraded or named to pacman; `~/.local/bin` untouched.

## Out of scope, deliberately

- The knowledge entry `corpus/knowledge/tb2-password-recovery-grader.md` (seat `R45PkgEntry`) — my prose refers to
  a `## Predictor` section and to the file existing; item 4's paste precondition names the dependency.
- `corpus/SOURCES.md` rows S149–S156 (seat `R45PkgRows`) — item 1's id list is the only coupling; if that seat
  renumbers, re-cut the row's id list, not the sentence.
- The probe receipt (seat `R45ProbeFirst`), the C1 fence and its counter (other seats), SCORECARD/LOG round
  headings for C1, the routed ledger.
- No verification run: the L1 runs `python3 plans/round45_c2_verify.py --lane <clone>` after integration —
  before-state is `checks=11 defects=8`, `PREDICATE C2 fail`
  (`.ufo/waves/round-45/claims/control-c2-nothing.txt`, tail: `V11 DEFECT entry absent` / `checks=11
  defects=8` / `PREDICATE C2 fail`).

## Needs the L1's decision (not mine)

1. Whether the LOG C2 bullet says `predicate met` (only after the counter prints `PREDICATE C2 pass`).
2. Whether a coverage-score sentence rides the LOG bullet (`Coverage held at 7 (L0 cap).` was round 44's; the
   claims carry coverage 7 *capped by the open L0 question `kengaku | round-33`*).
3. Whether round 45 gets a `## Round45 partial frontier admission` PROVINCE heading (round 44 did not).
4. Whether the optional limits sentence in item 4 is wanted (round 43 carried one, round 44 did not).

VERDICT: prose-drafts-5
