Round 56 integrate receipts — measured on the new host, instruments inside WSL2 Ubuntu-24.04

canonical measured revision: 9bc20ab75c1b8881cd915d0e3eab18bf8387ca3d (master checkout, uv-less; A3.4)
environment: canonical-header.txt (git 2.56.0, python 3.12.3, bwrap 0.9.0, biopython 1.85, uv scoped out)

c1-after-landcheck.txt   LANDCHECK PASS n=4, exit 0 at 9bc20ab7 (four legs: registry closure MISSING 0;
                         chess probe re-run byte-equal to the committed r55 receipt; entryargv selftest 4/4;
                         grader CHECKS n=733 mismatches=0 + selftest ALL PASS)
c1-selftest.txt          the checker's own tamper battery, 7/7, exit 0
c1-mutkill-{reg,chess,grader}.txt
                         one mutation each (registry row dropped / chess receipt byte flipped / grader-pinned
                         evidence flipped) in shared clones of 4a5dc42e: each LANDCHECK FAIL failed-legs=1,
                         exit 1 — every leg killable, kill rule not fired
c2-kill-abbreviated.txt  the abbreviated-selftest laundering fixture killed: ARGV-DEFECT + ABBREV-DEFECT naming
                         fixture-gate, PREDICATE R55-C2 fail, exit 0 (= the demonstrated state holds; controls
                         tool polarity per its docstring — the freeze text's "exit 1" misstated it, disclosed)
c2-kill-uvdecoy.txt      the uv-decoy fixture killed: ARGV-DEFECT + WRAPPER-DEFECT naming fixture-gate,
                         PREDICATE R55-C2 fail, exit 0
c2-controls-selftest.txt controls selftest 4/4 under its own uv-present scope (uv 0.13.6 installed for this
                         scoped side-run, removed again per A3.4)
c2-after-full.txt        THE C2 AFTER-PREDICATE: BINDING l1=0 l2=0 l3=0; RUN executed=83 timeout=0 mismatched=0
                         evidence_missing=0 laundered=0; TIPSTATE declared 49g/34r == observed 49/34;
                         SOURCE rev=9bc20ab7 clean=yes lane_rev_equal=yes; PREDICATE R55-C2 pass; EXIT=0
c2-before-thishost.txt   the before-state on this host at base 8db18e23 (final environment): executed=66,
                         evidence_missing=2, laundered=14 — the sixteen rows whose declared green is false here
census-end.txt           fleet sources-census validate at round end: verdict ok, FLEET_CENSUS_EXIT=0
                         (W04 duplicate-url warnings pre-existing)

the committed before-receipts (.ufo/waves/round-56/claims/c1|c2|c3-before.txt) were re-derived at the
pre-freeze base 1355e84c on this host: BINDING l1=17 l2=1 l3=0 reproduced byte-for-byte in structure.
