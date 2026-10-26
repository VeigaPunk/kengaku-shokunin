# F39ConnFrontier — frontier consistency after integration (kengaku r39 wave 2, falsify)

Seat: F39ConnFrontier (connector, leaf). Measured at lane tip `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` (branch master) on a clean `--no-local` clone at `/fast/scratch/hyaku/kengaku-r39/F39ConnFrontier/lane` (toplevel verified `git rev-parse --show-toplevel` = the scratch lane; scratch removed before finish). No lane file edited; report only.

Method: enumerated every count cell in tracked, non-`.ufo/` files (`git ls-files | grep -vE '^\.ufo/' | xargs grep -nE '[0-9]+ of 89|remaining 8[4-9]|are read'`), read each §Frontier sub-bullet, coverage-map bullet, index row, PROVINCE round-39 paragraph, SCORECARD/LOG/SKILL round-39 sections.

## 1. The current-state "5 of 89" cell — present and consistent on every surface

| Surface | Location (lane tip) | Cell | Status |
|---|---|---|---|
| README §Frontier round-39 sub-bullet | `corpus/README.md:308-323` | "...it stays open for the remaining TB2 task graders (5 of 89 read)" (`:320`) | ✓ |
| Coverage-map bullet | `corpus/README.md:265` | "A fifth instance of the same ground (5 of the 89 TB2 task graders; not breadth...)" | ✓ |
| Index row | `corpus/README.md:72` | "A fifth Terminal-Bench 2.0 task grader read and executed: `git-leak-recovery` scores five pytest functions..." | ✓ |
| PROVINCE round-39 paragraph | `PROVINCE.md:369-409` | "...or speak for the remaining 84 TB2 task graders (89 carry `tests/test.sh`; 5 are read)" (`:397`) | ✓ |
| Knowledge entry | `corpus/knowledge/tb2-git-leak-recovery-grader.md:46` | "the clause stays open for the remaining TB2 task graders (5 of 89 read at `2fd12b88`)" | ✓ |
| SCORECARD round-39 header | `SCORECARD.md:1375` | "a fifth TB2 grader executed" | ✓ |
| Round-39 evidence section | `corpus/README.md:472-476` | `evidence/round39/` captures, receipt, battery39 listed | ✓ |

Arithmetic: 89 − 5 = 84 ✓ (`PROVINCE.md:397`). Distinct fifth task confirmed: `git-leak-recovery` is a distinct task directory from protein-assembly/regex-log/configure-git-webserver/build-pmars (S117/S118 rows `corpus/SOURCES.md:132-133`; SOURCES S-row count = 111, matching SCORECARD "SOURCES 109→111").

## 2. Older sub-bullets still say "3/4 of 89" — but only as dated historical records; no contradiction

All older count cells present at tip (all found by the enumeration):

- `corpus/README.md:292` — round-37 bullet: "(3 of 89 read)", inside "*Partly discharged round 37 (2026-10-26):*"
- `corpus/README.md:305` — round-38 bullet: "(4 of 89 read)", inside "*Partly discharged round 38 (2026-10-26):*"
- `PROVINCE.md:276` — round-37 paragraph: "remaining 86 TB2 task graders (89 carry `tests/test.sh`; 3 are read)", under "## Round37 partial frontier admission (2026-10-26)"
- `PROVINCE.md:303` — round-38 paragraph: "remaining 85 ... 4 are read", under "## Round38 partial frontier admission (2026-10-26)"
- `corpus/knowledge/tb2-build-pmars-grader.md:44` — round-38 entry: "(4 of 89 read at `2fd12b88`)", entry `verified-at: 2026-10-26` (`:5`)

Assessment: each cell sits inside a bullet/section explicitly labeled with its round number and date, and each records the state *as of that round*. The counts are monotonic with correct arithmetic at every step (3+86=89, 4+85=89, 5+84=89). The identical relationship already existed when round 38 landed — round-37's "(3 of 89 read)" sat beside round-38's "(4 of 89 read)" — and the round-38 falsify connector reviewed both bullets without flagging a contradiction (`build/R38ConnFrontier.md` was superseded; `R38PkgProse` and the round-38 landing kept r37 byte-identical). The round-39 landing follows that same convention: `R39PkgProse/readme-frontier-round39.md:6` states the round-38 sub-bullet's text "is left byte-identical; this sub-bullet narrows that clause", and `PROVINCE.md:409` anchors "The round35/36/37/38 paragraphs above stay as written; this paragraph narrows only their 'remaining TB2 tasks' clause".

Conclusion: the retained "4 of 89 read" is a dated record of round 38, not a current-state claim; it does not contradict the "5 of 89 read" cell, which is the only current-state cell and appears consistently on every surface. (Readability nuance: a reader skimming only the bullet tails sees 3/4/5 sequentially; the per-round dating makes this the established ledger convention, and it is the same pattern accepted at round 38. Not a defect.)

## 3. No stale self-assessment line found

- PROVINCE round-39 paragraph explicitly disclaims scope: "does not validate or certify the task... or speak for the remaining 84" (`:394-397`) and "recipe round35/36/37/38 paragraphs above stay as written" (`:409`) — self-aware, not stale.
- No tracked surface asserts "4 of 89" as current: the only current-state cells are the five listed in §1, all reading 5.
- SCORECARD round-39 C2 row's "knowledge files/index rows 45→46, SOURCES 109→111" (`:1386`) match reality (index row 72 added; S117/S118 at `SOURCES.md:132-133`, S-row count 111).
- SKILL.md round-39 registry rows (`git-leak-probe`, `round39-c1-mutants`, `round39-c2`, `:587-589`) and "## Repository-history TB2 grader — round 39" (`:867+`) carry no count cells; probe summary `cases=25 observed_pass=13 observed_fail=12 mismatches=0` matches the receipt.
- LOG.md round-39 section (`:1150-1175`) matches the SCORECARD narrative (C1 7/7, C2 probe counts, order gate Q30 green on round 39).
- `corpus/knowledge/local-model-index.md` is the Bailian model-catalog index (not the knowledge index); absence of TB2 rows there is by design, not a gap.

## 4. Note on the wave-1 connector recommendation (observation, not a defect)

Wave-1 `build/R39ConnFrontier.md:31-32` recommended bumping the round-38 tail "(4 of 89 read)" → "(5 of 89 read)". The L1 instead landed the round-39 sub-bullet and left the round-38 text byte-identical (documented in `R39PkgProse/readme-frontier-round39.md:6`). The landed state is internally consistent under the dated-record convention (accepted precedent), and the round-39 bullet is the only cell carrying the current count, so consistency holds; the recommendation's non-adoption is a prose choice, not a contradiction.

## Evidence commands

- `git ls-files | grep -vE '^\.ufo/' | xargs grep -nE '[0-9]+ of 89'` → cells in §1/§2 (output in report preamble runs).
- `grep -n -B2 -A2 -iE 'of 89|are read|remaining 8[4-9]' PROVINCE.md` → `:276` (86/3), `:303` (85/4), `:397` (84/5).
- `sed -n '308,323p' corpus/README.md` → round-39 sub-bullet text.
- `grep -cE '^\| S' corpus/SOURCES.md` → 111.
- `sed -n '1,12p' corpus/knowledge/tb2-build-pmars-grader.md` → `verified-at: 2026-10-26` (dated entry context).

VERDICT: frontier-ok
