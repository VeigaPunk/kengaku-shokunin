# Receipt (a) — TB2 grader-replay sibling sweep, kengaku round 95

Sibling working-tree HEADs at scan time (2026-11-05, `git -C <lane> rev-parse HEAD`, read-only):

audio f9da7ee9, chousa 378fda82, game-dev-2d 1e033ef0, game-dev-3d 39ca3973, kagi f5977284,
kaidoku b0a7bb8c, kake 7f5b1b7b, kama 9b4c7af1, kasegi d16d2124, kotoba edc731a9,
kotodama 24eac1e9, kumitate 814068f0, lore 0f044aa7, mado 24ba2a9d, mori 5e2bcf2c,
revenger 05e854ce, souji e063a2fc, tabi 58d84eda, tameshi f256302b, tsukuroi 64f45b79.
Lane kengaku-shokunin at ea19299d (tip; T = afe9c229 per assignment).

Grep tool over explicit `;`-joined lane paths, gitignore=false (glob-form paths silently
return nothing — r94 F6 lesson re-applied). Queries: `fix-code-vulnerability`, `_hkey`,
`bottle\.py`, `CWE-?93`, `report\.jsonl`, `terminal.?bench` (case-sensitive), `2fd12b88`.

## Zero-hit tokens (all 20 sibling lanes)

- `fix-code-vulnerability` — 0 hits.
- `_hkey` — 0 hits.
- `bottle\.py` — 0 hits.
- `CWE-93` proper — 0 hits. The `CWE-?93` sweep matched only CWE-9**32/939/930/934/937**
  prefix false-positives in kasegi's Bugcrowd VRT capture S045
  (kasegi-shokunin/.ufo/waves/round-29/wave1/ExecCapS045.md:36-38,
  corpus snapshots S045.txt:93) — a different CWE id family, bounty-taxonomy ground, not the
  bottle `_hkey` CRLF vuln. The round-95 grader asserts lowercase `cwe-93`
  (corpus/evidence/round95/graders/fix-code-vulnerability/tests/test_outputs.py:52).
- `report\.jsonl` — 0 TB2 hits. All matches are agent-session transcripts named
  `*Report.jsonl` under `/home/vgpnk/.omp/agent/sessions/...` embedded in kaidoku r19 wave
  outcomes and mado r20 corpus-diff receipts — file-name coincidence, no graded-report surface.

## Non-zero tokens: every hit is an echo or routing of kengaku's own bytes

- kaidoku `.ufo/waves/round-41/w2/artifacts/R41W2Reservation/tx-scan.json:19601,19614` — embeds
  the KengakuR41 dispatch (PIN 2fd12b88, constraints-scheduling capture paths).
- kaidoku `.ufo/waves/round-69/w1/ConnectorCross/sweep/s4-receipt.txt:193-212` — sweep *of*
  kengaku SKILL.md instrument rows (r52 population, probes), routed to kengaku.
- kaidoku `.ufo/waves/round-87/w1/ConnectorR87/links.md:56` and
  `.ufo/waves/round-90/w1/ConnectorOverlap/receipts/kengaku.json:10-15` — kaidoku connector
  seats scanning kengaku (r90 overlap receipt quotes a kengaku probe docstring verbatim).
- kake `.ufo/waves/round-92/w1/ConnectorScope/receipts/query-422.txt:74`,
  `query-stale.txt:234`, `.ufo/waves/round-93/w1/ConnectorScope/receipts/sibling-scan.txt:22`
  — kengaku SOURCES/knowledge rows surfaced by kake's scans; routed, no claim.
- kumitate `.ufo/waves/round-63/build/K63RevengerDispatcher/forgery-borrowed/.ufo/waves/round-35/build-dispatch.json:370-471`
  — kengaku's r35 dispatch borrowed as forgery-control material (r94 finding, still present).
- souji `.ufo/waves/round-52/w1/S52connector01/evidence/01-sibling-term-sweep.txt:167-170`,
  kotoba `.ufo/waves/round-71/receipts/census-after.txt:28` (W04 duplicate-url row),
  mado `.ufo/waves/round-44/w2/RerunCensus/census-fleet.txt:32` (same W04 row),
  tabi `.ufo/waves/round-60..64/w1/R60Scout2.md:86`, `R62Exec1/context-6.stdout:255-980`
  (kengaku PROVINCE admission text), `R63Connector/sibling-overlap-scan-r63.tsv:69` and r64
  (`S228 pypi-server grader`, no-claim), tsukuroi
  `.ufo/waves/round-43/w2/AdjFinal/sibling-skillmd-pin-lines.txt:92-96` (kengaku r32/r37
  overlap text quotes).

## Verdict (a)

No sibling lane owns, replays, or captures any Terminal-Bench 2.0 grader, and none holds any
byte of the round-95 member `fix-code-vulnerability` (grader, solve.sh, Dockerfile, upstream
bottle.py) or its tokens. Kengaku remains the fleet's sole TB2 grader owner — the thirteenth
located replay is in-province under the PROVINCE frontier admissions (rounds 35-64) and no
cross-domain bleed exists. Non-lane fleet dirs were covered by the r94 sweep (zero signals);
the only tracked-tree additions since are kengaku's own round-95 surface files.
