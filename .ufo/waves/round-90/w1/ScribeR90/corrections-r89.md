# Round-89 corrections — append-only texts (draft by ScribeR90, round 90)

For the L1 to append, in order, to `LOG.md` (round-90 entry, "Corrections") and as the correction note named in `corpus/lessons/round-89-verifier-spotcheck.md` §7. Frozen texts are not edited: `plans/round-89-claims.md`, `corpus/lessons/round-89.md`, the round-89 report and the earlier SCORECARD/QUALITY rows stay byte-identical. Each correction below cites bytes the scribe read in this round.

Read-only checks behind these texts (scribe, 2026-11-05):
- `git diff --stat 192e809d a9b8a1a0 -- plans/round88_claim_figures.py` prints nothing, and the same for `0e6bb05f`: the round-88 counter bytes are identical at BASE `192e809d`, at the round-89 measured tip `a9b8a1a0` and at the round-89 instrument commit.
- `git cat-file -e d1c4f1b0:plans/round89-q66-records.json` exits 128 (`exists on disk, but not in 'd1c4f1b0'`); `git rev-parse 0e6bb05f:plans/round89-q66-records.json` = `163f284316141a831484dacb7f69ad4cbbaadfb3`.

---

## Correction (a) — R89-C2 control name (round-89 spot-check §7 item 2, `R89-D2`)

The frozen `plans/round-89-claims.md` line 50 lists the fourth control as `selftest-removed-from-path`. The counter implements it as `selftest-in-path` (`plans/round89_claim_figures.py:546`, `"selftest-in-path": {"selftest_fn": lambda lane_, rev_, work_: ["T-injected-failure"]}`): the fixture injects a selftest failure inside the predicate path and expects the predicate red. It does not remove the selftest from the path. The measured transcript carries the implemented name: `CONTROL selftest-in-path red rc=1` (`.ufo/waves/round-89/attempt2/c2-controls-attempt2.txt`; `PREDICATE R89-C2-CONTROLS pass red=4 of 4 tip=green`).

The frozen text is untouched and stays as written. The name the round-89 transcripts, SCORECARD row and this note use is `selftest-in-path`. Whether the intended fixture was the removed-from-path variant is an operator ruling on the frozen text (L0 `kengaku | round-89`, `.ufo/l0-questions.md:319`); this note does not rule on it.

---

## Correction (b) — round-88 before-count (round-89 spot-check §7 item 3, `R89-D3`)

Two places state the round-88 counter's count on the round-89 control fixtures differently:

- the round-89 report (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-89/kengaku.md` line 89, "round-88 counter 1 of 3 red on the attack fixtures") and `.ufo/waves/round-89/w1/ExecCtrlC2/round88-baseline.txt` say **1 of 3 red**;
- SCORECARD round-89 C2 row (`SCORECARD.md` line 4169, "1 of 4 red, not the predicted 0 of 4") and QUALITY Q67 (`corpus/QUALITY.md` line 1369, "measured 1 of 4 red") say **1 of 4 red**.

Corrected statement: **1 of 3 measured at BASE; the fourth (selftest-in-path) not measured at BASE.** The round-88 counter (`plans/round88_claim_figures.py`) was run on fixtures a (doctored-claimed), b (deleted-figure) and c (doctored-key) only (`round88-baseline.txt`, scenarios a, b, c). Results: a `PREDICATE R88-C2 pass`; b `PREDICATE R88-C2 pass`; c `PREDICATE R88-C2 fail`, rc 1. The only red fixture is c, and it is red through `DEFECT F4-unparsed R87-C1:kv:defect defect absent from TARGET` and `DEFECT F5-missing-known R87-C1 kv:defects`. No `MISMATCH KNOWN` line is printed for c. So the red is a parse failure of the counter's own output, not the KNOWN check firing on the claimed value.

Evidence caveat (stated, not repaired): `round88-baseline.txt` header records its scratch clone at `a9b8a1a0`, not `192e809d`. The counter bytes are identical at both revisions (diff empty above), so the BASE label refers to the counter bytes and the round-89 base; the fixture sources were the round-85/round-87 claims files as they stood in that clone.

Append-only landing: a correction row or note here; SCORECARD round-89 row and QUALITY Q67 are not edited in place.

---

## Correction (c) — SCORECARD round-89 C2 row limitation (round-89 spot-check §7 item 6, `R89-D6`)

The round-89 C2 row (`SCORECARD.md` line 4169) and its honest-limits paragraph (line 4177) say that the record table "pins the claim population at commit B". Limitation, stated as the round-89 spot-check item 6 asked: the round-89 record table `plans/round89-q66-records.json` was **not** blob-pinned by round 89. The frozen round-89 Move element (d), "pinned to its blob sha at the freeze commit", was not implemented: the table does not exist at the freeze commit `d1c4f1b0` (`git cat-file -e` exits 128), and the counter reads the table at the measured revision (`plans/round89_claim_figures.py` `git show {rev}:{RECORD_TABLE}`), with no blob-sha check.

The blob-sha pin first exists in round 90: `plans/counter-pins-r90.json` anchors `plans/round89-q66-records.json` at blob `163f284316141a831484dacb7f69ad4cbbaadfb3` and its creating commit `0e6bb05f3a6c2d9a96bb26db31a4fd39f58c2619` (`git rev-parse 0e6bb05f:plans/round89-q66-records.json`), and `plans/round90_counter_pin.py` checks it at any revision (R90-C2, `RECORD-TABLE blob=163f2843… matched`). The round-89 frozen text is not edited. The residual is the round-89 disclosure: one commit can rewrite the pin ledger and the table together, so the pin narrows the hole and does not close it.

---

Ledger of these notes: this file is the draft; the L1 appends the three texts to the round-90 LOG entry, and the SCORECARD/QUALITY locations above are cited, not rewritten.
