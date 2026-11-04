# DepthGateRerun — round 71 w1: structural gates re-run (depth, trio, census)

Seat: leaf executor, wave `round-71/w1`. No subagent, no battery, no port-5000 use (so no `--port-lock`
was taken or needed), no commit, no package install. Scratch `/fast/scratch/hyaku/kengaku-r71/DepthGateRerun-2`.

## Bytes measured (pre-entry)

- Lane tip: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master` →
  `d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0` (freeze commit of this round; base tip in the claims doc is
  `1cb49cac…`, so the tip has advanced by the freeze commit only).
- `sha256sum SKILL.md` → `baf3c714a67d135847966a9307ab656c3ff88dd2a681c69cb311582383353cd0`
- `sha256sum corpus/evidence/round62/class-survey.txt` → `ee30c6984c13985fe3efaa2d81c908b915da0f178ce5ca267bc0f0a37cd45613`
- `sha256sum corpus/knowledge/tb2-nginx-request-logging-offline.md` → `fcb246dc09601519b57a22dffbfe891df58f3d9579f4beda0cc56a3357dc2305`
- `sha256sum corpus/SOURCES.md` → `b1acdb73e3d2cfb10fc9cab59ed4ec8b6697a6ae556b1a95d95cc2571015e8f9`
- `git status --porcelain -- SKILL.md corpus/SOURCES.md corpus/knowledge corpus/lessons LOG.md corpus/README.md`
  printed nothing: the tree is clean at capture, so every line below is the committed tip, not a sibling's edit.

**Pre-entry, stated explicitly.** At capture: no `hf` token anywhere in `SKILL.md`
(`grep -n 'round71\|hf-model-inference\|hf/' SKILL.md` → no match), no round-71 knowledge entry under
`corpus/knowledge/`, no `S245`/`S246` rows (`grep -nE '^\|[[:space:]]*S24[56][[:space:]]*\|' corpus/SOURCES.md`
→ rc=1; max id on disk is `S244`), `grep -c 'executed 3 of 8' SKILL.md` = **1** and
`grep -c 'executed 4 of 8' SKILL.md` = **0**. The L1 must re-run the depth gate (and the trio gate on the
new entry) at integration, on the landed tip.

## What I ran

| # | command (cwd = L) | rc | receipt |
|---|---|---|---|
| 1 | `python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt` | **0** | `corpus/evidence/round71/gates/depth-gate.txt` |
| 2 | `python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-nginx-request-logging-offline.md` | **0** | `corpus/evidence/round71/gates/trio-nginx.txt` |
| 3 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (TMPDIR=scratch) | **0** | `.ufo/waves/round-71/census-before.txt` (reproduced byte-identically; tree stays clean) |
| 4 | `python3 plans/round63_gate_checks.py --selftest --work <scratch>/selftest` | **0** | below |
| 5 | `scripts/sources-census.sh selftest` (TMPDIR=scratch) | **0** | below |
| 6 | depth negative controls p1/p2/p3 on scratch copies of `SKILL.md` | 1/0/1 | below |
| 7 | trio negative control on a scratch copy of the nginx entry | **1** | below |

Exact gate output (files 1–2, verbatim):

```
ROWS n=16 class_match=True count_mismatch=0 paths total=34 resolved=34 share=1.00
PREDICATE R63-C2 pass
```
```
TRIO pass corpus/knowledge/tb2-nginx-request-logging-offline.md
```

Both receipt files carry a leading
`TREE-CAPTURE … tip=d8a77d3f… SKILL.md sha256=baf3c714… … PRE-ENTRY` line.

## Census (item 3)

- `rc=0`; stdout is 26 lines: **25 `W04` warnings + 1 `ok`** line
  (`kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md`).
- The 25 `W04` rows are all `duplicate url … across scopes` and are the same set that was committed at
  freeze: `diff` of my fresh capture against the frozen `.ufo/waves/round-71/census-before.txt` is empty, and
  after copying my capture back over that path `git status --porcelain` for it is empty — i.e. the freeze
  baseline reproduces byte-for-byte (`sha256 5bbde4ee…9fcde`). No new warning appeared.
- Row count: **236**. My seat spec's counting command is mangled and reports 0 —
  `grep -cE '^\|[[:space:]]*S[0-9](3,)[[:space:]]*\|' corpus/SOURCES.md` → `0` (rc=1), because in ERE `(3,)`
  is a literal group, not a repetition. The intended pattern
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **236** (rc=0), and an independent
  count over `^\| *S<digits>` rows agrees (`awk`: 236). Status split: **214 mined, 8 queued, 14 rejected**;
  id range `S001`–`S244`. Reported, not edited: the rule text is the L1's, and 236 is the number to compare
  against after S245/S246 land (expect 238).
- `sources-census.sh selftest` → `selftest ok`, rc=0, **96 `killed` lines, 0 `survived`** — the validator's
  own mutant battery is live, so the `W04` silence for the new rows will mean something.

## Is the depth gate live, and what does it actually bind?

`plans/round63_gate_checks.py --selftest --work <scratch>` → rc=0, four fixtures behave:
`GOOD rc=0`, `BAD-COUNT rc=1`, `NO-SECTION rc=1`, `BAD-ESCAPE rc=1`, then `SELFTEST pass`.

Targeted mutants on scratch copies of `SKILL.md` (never the lane file), each run through the same command:

| mutant | bytes changed | result |
|---|---|---|
| p1 | one dead token appended to `network-service`'s receipt-pointer cell (`corpus/evidence/round71/hf/dead-token.txt`) | `paths total=35 resolved=34 share=0.97`, `DETAIL unresolved=…`, **`PREDICATE R63-C2 fail`, rc=1** |
| p2 | the whole `executed 3 of 8 (round 64 …)` cell replaced by `zzz-no-counter` | `paths total=33 resolved=33`, **`PREDICATE R63-C2 pass`, rc=0** |
| p3 | `network-service` count cell `8` → `9` | `count_mismatch=1`, `DETAIL count-mismatch=network-service:got=9,want=8`, **fail, rc=1** |
| trio-q | `recheck:` injected ahead of `verified-at:` in the nginx entry header | `TRIO fail missing=recheck`, rc=1 |

Reading (`plans/round63_gate_checks.py:296-334`): `ok` requires `resolved == total` **and**
`share >= 0.90`, so the dead-token miss is caught by the equality, not by the share floor; each row's
pointer cell must also hold ≥1 resolving token; `count_mismatch` binds cell 2 to the `CLASS … count=` line
in `class-survey.txt`.

**Calibration finding (the one that matters for R71-C1).** The gate never parses cell 3. p2 shows a row
whose entire executed evidence is `zzz-no-counter` still prints `PREDICATE R63-C2 pass`. The frozen R63
predicate is about row set / census count / pointer resolution, so this is scope, not a defect — but it
means **the depth gate's pass is necessary and not sufficient for the `executed 3 of 8` → `executed 4 of 8`
move**. The witnesses for that move are the R71-C1 counting command (`grep -c 'executed 3 of 8' SKILL.md`
→ 0, `… 4 of 8 …` → 1) plus the hf probe receipt, exactly as the claims doc states. What the depth gate
*will* enforce at integration is that any new path token the row names (the round-71 hf receipt, the new
knowledge entry) exists on disk at the landed tip — strict equality, so one typo fails the gate. That is the
integration check to lean on, not a numerator check it cannot perform.

## Integration checklist handed to the L1

1. Re-run item 1 after the SKILL.md row edit; `ROWS n=16`, `count_mismatch=0`, `resolved == total`
   (expect `paths total` > 34 by the new hf tokens), `PREDICATE R63-C2 pass`.
2. Run item 2 on the new round-71 knowledge entry (trio keys `source`, `verified-at`, `recheck`, in that
   order, inside the first 12 lines and before the first `## ` heading — `TRIO_WINDOW=12`,
   `plans/round63_gate_checks.py:93-96`); the existing nginx entry's shape is the template.
3. Re-run the census: `rc=0`, `W04` should stay at 25 if S245/S246 carry fresh URLs, and the row count
   should become 238. A `W04` jump is a duplicate URL, not a pass.
4. Confirm the counter pair by grep, since the depth gate is blind to it (p2).

## Verdict

**PASS — both structural gates and the registry census reproduce green on the round-71 pre-entry tip.**
`PREDICATE R63-C2 pass` (`ROWS n=16 class_match=True count_mismatch=0 paths total=34 resolved=34 share=1.00`),
`TRIO pass` on the nginx entry, census `rc=0` with 25 unchanged `W04` warnings over 236 rows. Both gates
were shown to fail on adversarial bytes they are supposed to catch (dead pointer token, count drift,
trio order), and the depth gate was shown *not* to read the executed-counter cell — so the round's class-row
move must be witnessed by the R71-C1 counter and probe receipt, not by this gate.

## Risks / blockers

- No blocker. Pre-entry means these receipts validate the base state, not the landed move; item 1 must be
  repeated at integration (step 1 above).
- The seat spec's row-count command is broken as written (`(3,)`); using it verbatim yields `0`. I used the
  `{3,}` form and an independent `awk` count, both 236.
- I wrote only `corpus/evidence/round71/gates/{depth-gate,trio-nginx}.txt`, the byte-identical census
  reproduction, and this report; scratch stays under `/fast/scratch/hyaku/kengaku-r71/DepthGateRerun-2`.
