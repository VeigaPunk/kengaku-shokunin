# R39QualityQ30 — QUALITY.md Q30 drafted (round 39, wave 1)

Target file: `corpus/QUALITY.md` (L1 integrates; this seat wrote nothing outside its own report dir).
Insertion point: **append after `corpus/QUALITY.md:518`** (Q29's closing line `Supersedes: none.`), as
`## Round39 criterion — …` then the one bullet, matching Q24–Q29's shape (bold rule → evidence with
pointers → `Check (executable, round-<N> instance)` → `Shown able to fail` → `Limits:` → `Lesson:` /
`Supersedes:`).

Axes this moves: **quality** (the class that recurred twice becomes a command, not a paragraph) and
**calibration** (the criterion's own evidence is red-on-both-occurrences, green-on-this-round, plus
three synthetic legs). No axis harmed: no lane file touched, no frozen byte read as writable.

## 1. The draft, ready to paste

```markdown
## Round39 criterion — a class that recurs twice is closed by a gate over committed history

- **Q30 — a mistake class that recurs twice is closed by a gate that reads committed history — red on
  both occurrences and green on the round that lands it — never by a second prose rule.** A forward
  rule leaves nothing to observe. The order-of-operations class (a skip-control that runs the frozen
  instrument before the round's first recorded run) was recorded with a forward fix in
  `corpus/lessons/round-37.md:42` ("the discarded run cannot become evidence … the write-up must not be
  the only artefact") and recurred in round 38 (`corpus/lessons/round-38.md:36`), where the artefact was
  again only the claims header; round 37's stated fix "does not prevent the ordering, it only makes the
  discarded run harmless" (same row). The round-38 closure named the shape the class needed —
  "Append a correction and turn the lint into a gate with a red-before state"
  (`corpus/lessons/round-38-verifier-spotcheck.md:162-165`, routed item R3) — and the recurrence is the
  case `considerthese/2026-10-25.md:42-44`, proposal 2(b), predicted. The gate is
  `plans/order_check.py`: it reads commits only (working tree and index ignored) and FAILS when a file
  committed under `.ufo/waves/round-<N>/claims/` at or before the first commit adding the receipt shows
  the frozen probe executed (a `P10` line whose detail is anything but `receipt unreadable`, or a
  receipt-shaped `CASE … observed=` line), when the freeze commit already contains the receipt, and when
  the receipt was committed before the claims file; exit 2 on setup errors, never a silent pass.
  Measured at the criterion's creation (2026-10-26, before the tool landed): `ls plans/order_check.py` →
  `No such file or directory`; `grep -c 'order-of-operations' corpus/lessons/round-37.md
  corpus/lessons/round-38.md` → `1` and `2` (one row, one cross-reference to it); every occurrence was
  closed in prose.
  Check (executable, round-39 instance) — the pair that makes this a gate rather than a rule:
  `python3 plans/order_check.py --lane . --claims plans/round-38-claims.md --receipt
  corpus/evidence/round38/build-pmars-probe.txt` prints `ORDER HIT
  .ufo/waves/round-38/claims/control-c2-skip.txt@e0a378539a45:11 kind=gate-p10`, quoting the control
  line `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`, then `ORDER RESULT FAIL`,
  exit 1; and the same
  command with `--claims plans/round-39-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt`
  prints `ORDER scanned commits=1 file_entries=7 distinct_blobs=7`, `ORDER RESULT PASS`, exit 0 — round
  39's only `P10` line is the exempt `P10 DEFECT receipt unreadable`
  (`.ufo/waves/round-39/claims/control-c2-nothing.txt:11`).
  Shown able to fail: the recurrence's origin is red as well — `--claims plans/round-37-claims.md
  --receipt corpus/evidence/round37/git-webserver-probe.txt` → `ORDER HIT
  .ufo/waves/round-37/claims/control-c2-skip.txt@ca790460e9b7:12`, `ORDER RESULT FAIL`, exit 1 — and
  three synthetic two-commit repos make each leg bite alone: claims+receipt in one commit → `ORDER FAIL
  freeze-contains-receipt`, exit 1; receipt committed first → `ORDER FAIL freeze-contains-receipt
  receipt-before-claims`, exit 1; clean freeze-then-receipt → `ORDER RESULT PASS`, exit 0 (the tool is
  not always red).
  Limits: commits only — an executed probe whose output was never committed is invisible, and round 38
  is red only because its skip control kept one `P10` line; the `receipt unreadable` exemption is
  textual, so an instrument that prints that detail after executing would be excused; `CASE …
  observed=` binds the probe's line shape, so another instrument needs its own pattern; the gate detects
  and does not block, so 2(b)'s "blocks pre-registration" half stays unimplemented, and Q23's limit line
  (`corpus/QUALITY.md:291`) is named here, not amended (R1); the `recurrence=2` ledger row is written by
  the integrator and is not read by the gate; and a gate that only ever runs on the round that
  introduces it proves nothing, which is why the red pair is part of the check.
  Lesson: routed item R3, `corpus/lessons/round-38-verifier-spotcheck.md` §5 item 3; occurrences
  `corpus/lessons/round-37.md:42`, `corpus/lessons/round-38.md:36`; proposal
  `considerthese/2026-10-25.md:42-44`. Supersedes: none.
```

Two integration notes the L1 owns:

1. **Land the tool at the path the criterion names.** At drafting it sits at
   `.ufo/waves/round-39/build/R39OrderGate/order_check.py` (executor seat `R39OrderGate`; sha256
   `313f17b301b91bf63d6dfa4ebef9b79018df5ba92bce2a17aafffa7a3d0520d5`, 210 lines,
   `.ufo/waves/round-39/build/R39OrderGate.md` not yet written when this was drafted). The criterion's
   command path is `plans/order_check.py`; the run below used the artifact copy, and every number here
   is from that copy at that digest. If the executor's landed bytes differ, re-run the three commands —
   the criterion is safe either way because it quotes the command, not a digest.
2. **`corpus/defects.jsonl` has no row for this class** — 5 rows, `R34-D1`…`R34-D5`, none of them the
   order class (`json.loads` over the file, printed id/class/recurrence/status). The `recurrence=2` row
   in the claims text (`plans/round-39-claims.md:99-101`) is still the L1's to write; Q30's check does
   not read the ledger and does not pretend to.

## 2. The three inputs, with locations

| input | location | what it says (quoted ≤25 words) |
|---|---|---|
| round-37 lesson row 3 | `corpus/lessons/round-37.md:42` | fix cell: "the discarded run cannot become evidence and the disclosure is the right shape, but the write-up must not be the only artefact" |
| round-38 lesson row 2 (recurrence) | `corpus/lessons/round-38.md:36` | "round 37's fix (re-pin and re-run every counter run) does not prevent the ordering, it only makes the discarded run harmless" |
| round-38 closure R3 | `corpus/lessons/round-38-verifier-spotcheck.md:162-165` | "Append a correction and turn the lint into a gate with a red-before state." |

`grep -c 'order-of-operations' corpus/lessons/round-37.md corpus/lessons/round-38.md` → `corpus/lessons/round-37.md:1`,
`corpus/lessons/round-38.md:2`.

## 3. Check grounding — commands and outputs

Tool: `.ufo/waves/round-39/build/R39OrderGate/order_check.py` (sha256 `313f17b3…520d5`). Receipt:
`.ufo/waves/round-39/build/R39QualityQ30/order-gate-runs.txt` (50 lines). All runs read-only, on a
`git clone -q --shared` of the lane at `/fast/scratch/hyaku/kengaku-r39/R39QualityQ30/lane`
(`rev-parse --show-toplevel` → that path; `rev-list --count HEAD` → 202), `TMPDIR` set into the same
scratch root.

| run | command | observed |
|---|---|---|
| recurrence origin | `order_check.py --lane . --claims plans/round-37-claims.md --receipt corpus/evidence/round37/git-webserver-probe.txt` | `ORDER HIT .ufo/waves/round-37/claims/control-c2-skip.txt@ca790460e9b7:12 kind=gate-p10`, `ORDER FAIL probe-executed-before-receipt hits=1`, `ORDER RESULT FAIL`, **exit=1** |
| second occurrence | `--claims plans/round-38-claims.md --receipt corpus/evidence/round38/build-pmars-probe.txt` | `ORDER HIT .ufo/waves/round-38/claims/control-c2-skip.txt@e0a378539a45:11 kind=gate-p10`, `ORDER RESULT FAIL`, **exit=1** |
| introducing round | `--claims plans/round-39-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt` | `ORDER scanned commits=1 file_entries=7 distinct_blobs=7`, `ORDER ok …`, `ORDER RESULT PASS`, **exit=0** |
| leg 1 alone | fixture A (claims + receipt in one commit) | `ORDER FAIL freeze-contains-receipt`, **exit=1** |
| leg 2 alone | fixture B (receipt committed first) | `ORDER FAIL freeze-contains-receipt receipt-before-claims`, **exit=1** |
| negative control | fixture C (clean freeze, then receipt) | `ORDER RESULT PASS`, **exit=0** |

Independent cross-check of the same facts without the tool (plain git, read-only in the lane):
`git log --diff-filter=A -- plans/round-38-claims.md` → freeze `e0a378539a45…` at 02:38:28;
`… -- corpus/evidence/round38/build-pmars-probe.txt` → `e95cf5500b6c…` at 02:38:41;
`git cat-file -e e0a37853:corpus/evidence/round38/build-pmars-probe.txt` → rc 128 (receipt absent at the
freeze, so leg 1/2 are green and the red is leg 3 only). Round 39: freeze `088f7c36e94c…` at 03:40:24,
receipt `6a1eb5e1da4a…` at 03:40:45, `git cat-file -e 088f7c36:corpus/evidence/round39/git-leak-probe.txt`
→ rc 128; `grep -rnE '^ *gate: P10' .ufo/waves/round-39/claims/` → one line, `control-c2-nothing.txt:11
gate: P10 DEFECT receipt unreadable` (the exemption).

## 4. Round-38 spot-check §3 — scanned for a disagreement needing a criterion

Read `corpus/lessons/round-38-verifier-spotcheck.md:121-136`. The §3 table has **5 rows and 5 `agree`**:
`knowledge/tb2-build-pmars-grader.md` (admit), S115, S116 (mined admits), TB2 issue #59 (refused),
`JonathanGabor/terminal-bench-2-audit` (refused) — `grep` over the §3 block returns 6 lines matching
`agree|disagree`, one of which is the table header. The conclusion line reads "3/3 sampled admits and
2/2 sampled refusals agree" (`:132`). **Confirmed: 0 disagreements, so no additional criterion is
needed from §3** — nothing here is a second witness for a criterion this seat would have to draft.

The one caveat in that same paragraph (`:133-135`) is not a §3 disagreement; it is already routed as R3
("the order-of-operations mistake recurred although `round-37.md:42` carried a rule forward … routed
(R3)") and is exactly what Q30 above converts from prose into a gate. That is the correct disposition:
Q28 and Q29 each consumed the previous round's own disagreement, and Q30 consumes the recurrence the
closure flagged as the counterweight to "discernment improved".

## 5. Findings and out-of-scope

- **Finding (for the L1):** `plans/order_check.py` does not exist yet; until it lands, Q30's command is a
  promise. The criterion is written to survive that (it quotes the command and its expected output, and
  names the artifact digest it was measured on), but a QUALITY row whose command cannot run is the shape
  Q21/Q22 call stale debt — land the tool in the same commit as the row, or the row opens red.
- **Finding (calibration):** the gate's two non-hit legs (`freeze-contains-receipt`, `receipt-before-claims`)
  were never exercised by real round history — round 37/38/39 all froze before their receipts — so their
  red evidence here is synthetic (fixtures A/B, one commit each). The criterion states this rather than
  presenting all three legs as historical.
- **Out of scope, not touched:** `corpus/QUALITY.md` (L1 integrates), `plans/order_check.py` (executor
  seat), `corpus/defects.jsonl` (L1), round-38 wave-2 reports (other seats), the frozen claims/counters/
  probe/spec/dry table/captures/receipt named in the assignment. No frozen byte was read as writable and
  nothing frozen changed.
- **Scratch:** `/fast/scratch/hyaku/kengaku-r39/R39QualityQ30/` held the lane clone and the three
  fixture repos; the receipt was copied into this seat's dir first and the tree removed at exit.
- **Tooling:** no installs or upgrades this seat (nothing was needed; pacman is paused host-wide and no
  `uv tool` / `npx` / binary install was proposed).

VERDICT: q30-drafted
