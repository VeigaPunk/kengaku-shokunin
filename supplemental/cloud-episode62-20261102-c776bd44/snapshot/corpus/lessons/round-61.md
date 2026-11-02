# Round 61 — kengaku lesson (hyaku run 14, 2026-11-02)

author: kengaku L1 (round 61, Windows host, WSL Ubuntu-24.04 instruments). Base `f97e5b7b`;
freeze `215a7029` (+ EOL repair `b9920576`); amendment `0e62b479`; measurements
`ddbb93ec`; landing = the round's last content commit. The round's shape: the seventeenth
grader read and executed as a NEW class (signal-propagated cancellation semantics), the
round-60 closure's D1 discharged with the byte-true mirror, and four author defects
caught by the round's own instruments — the honest fail of record committed before the
Q25 re-freeze.

## Gate

Sources opened this round (2026-11-02): **S224** — Terminal-Bench 2.0
`cancel-async-tasks` scoring predicate (`tests/test_outputs.py`) at pin `2fd12b88`,
https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/cancel-async-tasks/tests/test_outputs.py
— opened live via curl in WSL (the canonical environment), byte-compared to the committed
round-52 population capture (sha256 `d6f510b5…60ee7`, byte-identical); located quotes at
capture :75 ("This will fail e.g. if the agent tries to use threading.ThreadPoolExecutor
which", 12 words) and :144 ("This is a common gotcha in Python because asyncio.gather
doesn't properly cancel", 12 words). Tier A code for the narrow scope: the seventeenth
grader's decisive legs and the two traps the class prices. Grounds R61-C1 (the sourced
claim). **S225** — WHATWG Encoding Standard, windows-1252 index,
https://encoding.spec.whatwg.org/index-windows-1252.txt — opened live via curl in WSL
(sha256 `2c5fa192…60795`, dated 2024-09-18 in-file); located quotes at :7/:13/:25/:27/:105
(the cp1252 byte-to-codepoint mappings 0x80→U+20AC, 0x86→U+2020, 0x92→U+2019, 0x94→U+201D,
0xE2→U+00E2). Tier A docs for the narrow scope: why the round-60 mirror's defect is named
cp1252-double-encoded. Grounds R61-C2 (the sourced claim). Both adopted through
`plans/sources_adopt.py` (quote validation 7/7 located+bound; registry admission exit 0;
216 staged rows before; collisions=0, malformed=0, duplicates=0).

Flip check: S224 and S225 are new rows (216→218); no rejections this round; no flips of
existing rows. Census receipts (round start and end, exit codes) are in the round report.

Admit/reject spot-check (LEARNING.md discernment), sampled for the outside closure: ADMIT
S224 (tier A code; the quotes byte-locate in the committed capture; the word counts are
derived and gate-checked) and ADMIT S225 (tier A spec index; the five byte-mapping lines
are the mis-decode table that names the mirror defect). REJECT-equivalent decisions
sampled: (1) the failed first scored run was NOT re-rolled or quietly repaired — its
receipt of record was committed AS-IS and the re-freeze declared per Q25 (both instrument
digests named); (2) the freeze's wrong before-anchor was NOT silently fixed — Amendment 1
addendum 2 dates the correction and the measurements receipt carries the measured counts.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| windows-text-mode write — the freeze commit's SOURCES.md append went through a Windows text-mode write and flipped the whole registry's line endings (273 lines rewritten CRLF; the diff showed 546 changed lines for a 2-row append) | `b9920576` (the repair: parent blob bytes restored, the two rows re-inserted as a pure byte append; net diff vs base +2/0/0-CR) | my own append-only verification of the freeze diff | registry/append-only file edits happen ONLY through WSL-native tooling (python in WSL or shell appends) — a Windows-side `write_text` never touches an append-only registry again; the repair class is byte-restoration from the parent blob, not an in-place rewrite |
| builder-property unwired — the simulator never read the declared `handler` property (the signal-handler branch was gated only on ignore_sigint), so a case declared as "no handler" installed the cancelling handler and passed legs it was built to fail | `.ufo/waves/round-61/recon/c1-first-run-FAIL.txt` (the kbdint-no-handler row: predicted F at above, observed P) | the round's own probe — the designed capture, on the first scored run | every declared candidate property is keyed in the simulator by construction (the amended sim branches directly off the SPEC field it declares); the claims freeze states the builder-honors-declarations rule explicitly |
| freeze-transcription recurrence — ONE table row (no-max-enforcement) hand-transcribed into the freeze doc with two legs swapped, the exact r59 class, ONE round after its mined fix | `.ufo/waves/round-61/recon/table-identity.txt` (freeze block vs the tool's own table output: exactly that row differs) | the table-identity receipt — measured before the re-freeze landed | the fix is now MECHANICAL, not a habit: the amendment's table block is the literal `--render-table` output inserted by script (verified byte-identical); no future freeze embeds a hand-typed table |
| model else-branch blind spot — predict_legs' asyncio else-branch asserted "asyncio + handler" in its comment without checking handler, so the model's below/at legs were blind to the same property the above formula priced (the first run's mismatch shape — predicted F only at above — was this bug colliding with the builder bug) | the first run's kbdint row + Amendment 1 addendum (the model fix, named) | the round's own probe (the above formula disagreed with the else-branch on the same case) | a predicate's comment is a contract: every condition the comment names must appear in the code; the amended else-chain checks handler explicitly |
| asserted before-anchor — the freeze claimed a base count of 0 for the frontier anchor without measuring it; the planned text's own sentence already contained the token (count 1) | `.ufo/waves/round-61/measurements.txt` controls section (measured: the word counts 1 at base; the correct frontier anchor counts 0 at base, 1 at landing) | the measured controls run (after the scored run, before the landing) | before-anchors are MEASURED against base bytes, never asserted from memory; the controls section is part of the measurement receipt, and a wrong anchor is dated-corrected (Amendment 1 addendum 2), never silently repaired |
| environment: /tmp wipes between wsl.exe invocations and /mnt/c clones — two runner take were lost to a wiped /tmp work dir and one clone landed on /mnt/c (not the native-fs counter environment) before being re-taken | the scratch transcripts (selftest re-run after re-mkdir; scored_run vs scored_run2) | my own runner scripts | single-script WSL runners that create their own work dirs; measured clones live in ~/$ (native ext4), never /mnt/c — the r59/r60 canonical-environment rule, re-learned twice in one round |

## Carried → closed this round

- The round-60 closure's routed defect D1 (mirror byte-fidelity): CLOSED — the byte-true
  mirror landed (cmp-identical, receipt-priced), the dated erratum names the encoding
  defect and the surplus blank line, the round-60 file is downgraded to the
  content-mirror of record, and the byte-mirror of record is the round-61 file. The
  fleet-root landing stays the orchestrator's (the append re-verified intact at
  measurement).
- The round-60 closure's D2 (report mistake-row undercount): a precision nit on the
  round-60 REPORT (fleet-root file, orchestrator-owned); named in the round-61 report;
  no lane artifact edited.
- Standing opens routed/closed with evidence: the r50-c1 root cause and the R56-F1
  checker repair were closed at round 58 (the SCORECARD round-58 rows) and re-verified
  green in the round-60 final receipts — evidence cited, nothing re-opened. The three L0
  questions `kengaku | round-25/33/51` (coverage cap; decision packet; absent surfaces)
  and the `kengaku | round-56` pair (L2 surface; ledger host column): STILL OPEN,
  nothing assumed answered — coverage is claimed predicate-met this round with the score
  held at 7; the L2 surface routed around again. The `kengaku | round-52`
  push-protection question is already disposed by operator decision
  (`corpus/evidence/round52/graders/EXCLUDED.md`, 2026-10-28).

The close rule for every future round: tables are embedded from the tool's own output by
script; before-anchors are measured; declared properties are wired by construction; and
append-only registries are never touched by Windows text-mode writes.

## Precision erratum — round62, 2026-11-02

This corrects the earlier Mistakes rows and the round61 review's D3, without
rewriting either historical record. Evidence and commands:
`.ufo/waves/round-62/recon/precision-before.txt`;
`corpus/evidence/round62/manual-answers.md` §C2.

- R61-D1: the freeze-transcription row's ONE-row assertion and “exactly that
  row differs” are inaccurate. The preserved table-identity diff has THREE
  changed lines: the separator, sequential-sync, and no-max-enforcement.
  That is TWO data rows, not one. The amended table itself is not changed by
  this correction; the first-run failure remains historical.
- R61-D2: S225's pointer226 gloss is inaccurate: index line105 is pointer98,
  corresponding to byte0xE2 (226 decimal). S230 corrects the source row by
  succession; S225 remains untouched.
- R61-D3: the registry byte counts are base272 LF/0CR → freeze274 LF/274CR
  (274CRLF) → repaired274 LF/0CR, not273 lines. On this cloud host,
  `git diff --numstat f97e5b7b 215a7029 -- corpus/SOURCES.md` is +274/-272,
  total546; base→b9920576 is +2/-0. Thus the original546 diff-line total
  reproduces here; the old review's +274/-237=511 does not. The precise cause
  of that review discrepancy is not established. Literal blob SHA256s and full
  commit IDs are in precision-before.txt, and the independent round62 reviewer
  separately confirms these counts. This is a correction of author AND reviewer
  precision, not a retroactive re-scoring of round61.

Manual precision correction is not perpetual automated closure: Q23's executable
ledger extension has not been implemented/run under this host's blocked envelope.
