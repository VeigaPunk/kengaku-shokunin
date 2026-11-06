# ReviewerC2 — scoped findings (R95-C2 instruments at T afe9c229)

Full report and raw receipts: `.ufo/waves/round-95/w1/ReviewerC2/report.md`, `.ufo/waves/round-95/w1/ReviewerC2/receipts/`.

Reproduced at T: honest counter rc 0 (`TARGET legs_passed=5 of 5`, `PREDICATE R95-C2 pass`); census rc 0 (`FALSEGATES total=14 passing=0 designated_red=14 honest=pass`). Designated legs are the reason for 14/14 rows. Nothing below flips R95-C2 at T.

FINDING C2-F1 major: the census's green path trusts the counter's own printed designated RED lines; a forged counter that prints them when given `--tool-file` passes the census (`PREDICATE R95-C2 pass`, rc 0). Receipt `ReviewerC2/receipts/held/census-H4.txt`.
FINDING C2-F2 major: W3 requires only that some battery case goes red for each probe, not the designated case; a battery with 12 of 15 cases hollowed passes R95-C2 (H2, rc 0), and so does one hollowed case (H1, rc 0). Receipts `held/out-H2-hollow-except-probed.txt`, `held/out-H1b-B07-hollow.txt`.
FINDING C2-F3 major: the tsv exclusion of M10 ("no observable") is false. With the rev-list rc guard dropped and a damaged object store, the gate reports a post-freeze edit as `intact` with rc 0, where gate v2 gives could-not-evaluate rc 2. The counter passes it (rc 0). Not a flip at T (M10 not in the population; gate v2 has the guard). Receipts `ReviewerC2/receipts/cli-checks/M10-damaged-object-store.txt`, `held/out-M10-rev-list-rc-ignored.txt`.
FINDING C2-F4 minor: W3 and W5 are byte-anchored; a semantically identical refactor of gate v2 makes R95-C2 FAIL (`W3 P2/P3 anchor-missing`, `W5 K7 anchor-missing`, rc 1). Receipt `held/out-H7-equivalent-refactor.txt`.
FINDING C2-F5 minor: the M04 exclusion's "equivalence" is wrong: on an absent-at-freeze claims row it crashes (`TypeError`, rc 1, no PREDICATE/summary) and its reason strings differ. It cannot turn a breach into a pass, so the population stays valid; the counter passes it (H3, rc 0). Receipt `ReviewerC2/receipts/cli-checks/M04-absent-at-freeze-row.txt`.
FINDING C2-F6 info: the M18 exclusion is justified (verdict-neutral; only the echoed FREEZE id differs for an annotated-tag freeze). Receipt `cli-checks/M18-annotated-tag-freeze.txt`.
FINDING C2-F7 info: all 14 designated legs are the reasons; some rows also trip side legs (anchor-missing, predicate mismatch). Receipts `census-out/`.
Controls caught as designed: H5 (edit-then-revert accepted), H6 (first-parent), both FAIL.
