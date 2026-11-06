# ExecC2 — R100-C2 independent re-measurement

Seat ExecC2, lane kengaku-shokunin, BASE 7846037679de77d050141c785996471801e5a19a, T dbe0cefa607cf57f7f58346fce64bcc127144ca0, REF (F~1) 5220b71d337a3703eaba4cdf6b85eaf343497ae0. Clones: /fast/scratch/hyaku/kengaku-r100/ExecC2/{cloneT,cloneBASE,cloneREF} (shared clones, detached). Own checker: .ufo/waves/round-100/w1/ExecC2/checker.py (never imports plans/round100_c2_rowcensus_bind.py; parses c2-pop.txt + c2-live-refetch.txt itself). Frozen counter re-run: c2-at-T.txt / c2-at-BASE.txt. Tooling: none installed (python3 stdlib + git only); RULES.md read, no pacman.

## Frozen counter (lane bytes)
- At T: `PREDICATE R100-C2 pass`, K1–K10 all pass, `pop=9 cleared=9 still=0`, `GATE defects base=33 ref=32 rev=23`, `base_rows=333 base_rows_not_equal=0`, `outside_rows=324 outside_removed=0 outside_added=0 outside_rebound=0`.
- At BASE: `PREDICATE R100-C2 fail` (K1,K4,K5,K7,K9,K10 fail), `cleared=0 still=9`, GATE 33/33/33 — the expected do-nothing direction (BASE predates the freeze commit, so REF falls back to BASE; K7 prints DEFECT K7 no freeze commit).

## Own checker (checker-out.txt — 90 PASS, 0 FAIL)
A) Per population row (S210 S211 S219 S228 S232 S279 S281 S298 S300): blob sha256 at T == pop token == live-refetch sha256 (HTTP 200) == PROVENANCE.md sha cell; exactly one line per row across the three new files (round52: S210 S219 S228 S232 S279 S281; round58: S211; round94: S298 S300); three cells (`| row | file here | sha256 |`), no URL in any new file; no id outside POP in new files; exactly 3 new PROVENANCE.md files.
- Evidence: checker-out.txt `PASS S210-blob-sha==token` … all 9 × (blob, live, one-line, three-cells, no-url, sha-cell, file-is-new) PASS; `PASS no-id-outside-pop`, `PASS url-channel-files-0`, `PASS new-prov-3`.
B) BASE-bytes gate (sha 11bb2cad… == frozen GATE_SHA) `--verbose`: REF (cloneREF @ 5220b71d) DEFECT 32 lines/29 sids → T (cloneT) 23 lines/21 sids. Per-row diff restricted to 333 BASE rows: CLEARED = exactly the 9 pop tokens; ADDED = none; RECLASS = only S300, token fa53d657 `anchor-unbound → abbrev-unresolved` (token preserved; other S300 token 3a905a56 untouched).
- Evidence: checker-out.txt `PASS cleared-exactly-9-pop-tokens`, `PASS no-added-defects`, `PASS reclass-only-S300`, `PASS S300-fa53d657-reclass`; gate-REF.txt / gate-T.txt.
C) Row-level census: all 333 BASE SOURCES.md row lines byte-equal at T (`PASS base-rows-byte-equal-at-T`, `t_rows=341` = 333 + 8 C1 rows S342–S349); `PASS base-rows-333`.

## Falsification (in-checker mutated inputs, all rejected as expected)
good line accepted; four-cell rejected; url line rejected; wrong-sha rejected; duplicate-line count detected (`falsify-*` PASS ×5).

## Bugs found in my own first check (fixed, not lane defects)
1) Scanned all PROVENANCE.md files → substring `\bS\d+\b` hits inside the round-98 file (64 hits/row). Fixed to scan only the 3 new files. 2) Sha cells are backtick-quoted — fixture used exact cell equality. Fixed to strip backticks. 3) Reclass zip assumed parallel ordering — used token+class set membership instead. Checker now ALL PASS; findings above are the corrected results.

## Risks / residual
- Live receipt is the pre-freeze `.ufo/waves/round-100/L1/c2-live-refetch.txt`; verified token equality against it, not re-fetched (network not required; matches frozen K9).
- Gate diff REF→T includes C1's P0 capture effect only via REF (amendment 1: S295 already re-bound at REF, 33→32 BASE→REF); no C2-attributable outside-row change beyond the 9 pop rows.

## Verdicts

R100-C2 pass — Frozen counter at T prints PREDICATE R100-C2 pass with K1–K10 pass, cleared=9/still=0, GATE 33/32/23 — .ufo/waves/round-100/w1/ExecC2/c2-at-T.txt
R100-C2 pass — Own independent checker confirms blob sha256==token==sha cell, one 3-cell no-URL line per row in 3 new PROVENANCE.md files for all 9 rows — .ufo/waves/round-100/w1/ExecC2/checker-out.txt
R100-C2 pass — BASE-bytes gate diff REF→T restricted to BASE rows clears exactly the 9 pop tokens plus only the S300 fa53d657 reclass, nothing else — .ufo/waves/round-100/w1/ExecC2/checker-out.txt
R100-C2 pass — All 333 BASE SOURCES row lines byte-equal at T (341 rows at T incl. C1's 8) — .ufo/waves/round-100/w1/ExecC2/checker-out.txt
R100-C2 pass — BASE failure direction holds (PREDICATE fail, still=9) — .ufo/waves/round-100/w1/ExecC2/c2-at-BASE.txt
