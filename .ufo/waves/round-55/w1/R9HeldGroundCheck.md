# R9HeldGroundCheck — R55-C3 novelty-of-ground check

Pin: base `798f5e9ef30ef39291295565209b65a17343c00e`. Lane HEAD observed `80afa613` (round-55 freeze). Clean shared clone under scratch; no lane write, no mutating git. Scratch deleted before yield. Receipt: `receipt.txt` in this directory.

## Check 1 — chess-best-move absent before this round

Commands (all `git -C <clone> grep -c chess-best-move 798f5e9e… -- <scope>`):

| scope at pin | hits |
|---|---|
| corpus/knowledge | 0 |
| corpus/README.md | 0 |
| corpus/SOURCES.md | 0 |
| PROVINCE.md | 0 |
| corpus/lessons | 0 |
| corpus/evidence | 15 (`round52/graders/SHA256SUMS` 2, `round53/fetched/C1PriceScoutE-tb2audit-20260120-audit.txt` 1, `round53/pin-tree-2fd12b88.json` 9, `round53/tests-index.json` 3) |

The literal pre-freeze command from the assignment, `git grep -c chess-best-move 798f5e9e… -- corpus PROVINCE.md`, returns 15 hits, not 0. Those hits are all in `corpus/evidence`, not in the four scopes the frozen before-claim names (`corpus/README.md`, `corpus/SOURCES.md`). The frozen before-claim itself (`corpus/README.md corpus/SOURCES.md` → `0 0`) holds.

Working-tree grep (`grep -rn chess corpus/ PROVINCE.md --include=*.md`) shows `corpus/README.md:84`, `SOURCES.md:216-217` and `lessons/round-55.md` hits. Those are round-55 rows from the working tree, not pre-round ground.

Verdict: **HELD** for the knowledge, SOURCES, README and PROVINCE scopes. The grader bytes and a third-party TB2 audit already exist in round-52/53 evidence. The new entry must cite that prior capture and state that no prior corpus knowledge entry read or executed the grader.

## Check 2 — no prior entry already describes full-multiset equality grading

Quoted r45 class sentence (`corpus/knowledge/tb2-password-recovery-grader.md:19`):
> "reduces to an existence check plus exact **line membership** of one hard-coded 23-character constant, `"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses`, computed over `read_text().strip().split("\n")`."

So r45 is membership over lines, not multiset equality over tokens. That distinction holds.

The equality channel is already named as old in several entries:
- `tb2-db-wal-recovery-grader.md:42`: "new verdict channel (list length, **set equality**, per-cell equality and type gates are all old)".
- `tb2-regex-log-grader.md:57` and `:75`: "`assert matches == expected_dates` — **full-list equality**: count, order and type all matter".
- `tb2-circuit-fibsqrt-grader.md:48`: "existence, a line count and **per-value equality** are old".
- `tb2-git-leak-recovery-grader.md:44`: "substring absence, **exact-equality** and a pinned digest are all old".

Full-scope grep for `order-insensitive|set equality|full-multiset|multiset equal|sorted(` in corpus knowledge, lessons, README and PROVINCE finds only the db-wal `sorted(ids)` order check (`:74`) and the db-wal "set equality" wording above. No entry uses the chess class wording.

Verdict: **HELD WITH A WORDING CONSTRAINT**. The artefact class (agent-written whitespace-token move file, order-free, partial/duplicate answers fail) is new relative to r45 and to regex-log's order-sensitive list equality. The verdict channel (equality) is not new, and db-wal already calls set equality "old". The entry must not claim equality as a new verdict channel. It should state the difference from regex-log (order-free vs order-sensitive) and from db-wal (token multiset vs id set).

## Check 3 — S201/S202 are not near-duplicates of held rows

- Exact URL at pin, `git grep -c -F` over `corpus/SOURCES.md corpus/README.md PROVINCE.md`: 0 hits for both candidate URLs (`chess-best-move/tests/test_outputs.py`, `chess-best-move/instruction.md`).
- Pinned-prefix compare: 68 SOURCES lines share the `terminal-bench-2/2fd12b88…` prefix; 59 unique held pinned tails. Tail compare: exact tail hits 0 for both candidates; same-task-dir (`chess-best-move/`) hits 0. The shared pin prefix is not a duplicate.
- Same-filename tails in other tasks exist (15 `tests/test_outputs.py`, 12 `instruction.md`) but different task dirs, so not near-duplicates.
- Census W04 run on a scratch fixture: pinned SOURCES plus two template-shaped rows S201/S202 with the new URLs. Output: no new `W04` and no `E04` lines for S201 or S202. The 15 base W04 lines are unchanged. The fixture also printed `E11` (missing used-by, because the fixture lacks the knowledge tree) and `E12` (rows appended after the Registry section, a fixture-placement artefact). These are not findings against the real rows, which go inside the Registry table. The real census must be re-run after landing.

Verdict: **HELD**.

## Defects and notes routed (not fixed; not this seat's files)

1. Frozen command text `git grep -c chess-best-move <pin> -- corpus PROVINCE.md` returns 15, not 0 (evidence-tree hits). Route to the L1: the freeze text's scope is wrong. The frozen before-claim scope is correct.
2. Claim text says "12 tb2-* knowledge entries". Base has 14 `tb2-*` files: 12 grader entries plus `tb2-grader-vacuity-triage.md` and `tb2-presence-only-triage.md`. The 12-grader count is correct.
3. Stale frontier count: `PROVINCE.md:557` says "8 of 89 read"; `corpus/README.md` says "12 of 89 read" at the pin. The round-55 narrowing ("12 → 13 of 89") is consistent with README, not PROVINCE. Route to the PROVINCE owner.
4. The r53 `C1PriceScoutE` audit already rated chess-best-move coverage 4 and noted "the sorted comparison allows for any order". That is prior third-party reading, held in evidence, not corpus knowledge. The new entry should cite it as prior ground rather than as a first read.

## Commands and exit codes

- `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin <scratch>/clone` → 0
- `git -C <clone> rev-parse HEAD` → `80afa613…`; `cat-file -t 798f5e9e…` → `commit`
- `git grep -c chess-best-move 798f5e9e… -- <scopes>` → as tabled (exit 0 when hits; 1 for none)
- `git grep -ln 'sorted(' 798f5e9e… -- corpus/knowledge` → db-wal only, exit 0
- `git grep -c -F <candidate URLs> 798f5e9e… -- corpus/SOURCES.md corpus/README.md PROVINCE.md` → 0 hits, exit 1 each
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate <fixture-base>` → rc 1 (E11 noise from fixture lacking knowledge tree; base W04 lines listed)
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate <fixture-cand>` → rc 1 (same E11/E12 fixture artefacts); `grep -E 'S20[12]|W04|E04'` → only the E12 fixture-placement lines for S201/S202, grep exit 0
- No installs. No network calls. No writes to the lane outside `.ufo/waves/round-55/w1/R9HeldGroundCheck/` and `.ufo/waves/round-55/w1/R9HeldGroundCheck.md`.

## Dead ends

- The working-tree grep first returned round-55 rows; I checked against the pin instead, which is the requested basis.
- Census fixture first run lacked the knowledge tree, producing E11 noise. Not a finding.

## Verdict line

R55-C3 novelty-of-ground: check 1 HELD; check 2 HELD WITH WORDING CONSTRAINT (artefact class new, equality channel held); check 3 HELD. The seat recommends the entry describe the class as "order-free token multiset over an agent-written file" and explicitly disclaim any new equality verdict channel.
