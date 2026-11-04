# ReviewerC1R81 — independent R81-C1 re-derivation (round 81 w1, reviewer seat)

Date 2026-11-04. Read-only review of committed bytes. Measured tip `git rev-parse master` =
`2fe3d8e6751fa055ac7912616e7fb83b7864360a`; base revision `4e833e9fee8022d24559535178c6fe32b2cd62f1`;
freeze commit `4d896e0daf8831ef7a0016bf3c944d11ba465f70`. All counter/gate executions named below ran
against my own scratch shared clone (`/fast/scratch/hyaku/kengaku-r81/ReviewerC1R81/clone`, HEAD =
`2fe3d8e6…`, `git status --porcelain` empty) or my own fixture copies — never with `--lane` pointing
at the real lane; the lane worktree itself was only read. The lane worktree currently has 4 untracked
`.ufo/waves/round-81` files (sibling-seat bookkeeping); excluded by measuring committed bytes in a
clean clone. No tools installed; no pacman transactions (paused per orchestrator ruling 2026-10-20).

## 1. Universe re-derived independently — matches the frozen claim and the counter

Method: my own script (`derive_universe.py`, re-written from the frozen sentence, not copied from the
counter) over `git show 4e833e9f…:plans/grader-population-ledger.json` (88 members) and base-rev
capture bytes from my clone.

- Step 1 — `status=="unexecuted"` AND `reason=="unattempted"` AND class set ⊆ {file-artifact,
  serialization-schema}: **n=16**.
- Step 2 — `corpus/evidence/round52/graders/<m>/tests/test_outputs.py` exists at BASE_REV and imports
  stdlib modules only (regex `^\s*(?:from X import|import X)`, roots checked against
  `sys.stdlib_module_names`): **n=11**.
- Assert count `^\s*assert\b`: **max = 5**, carried by exactly
  **{`log-summary-date-ranges`, `vulnerable-secret`}` → UNIVERSE n=2.**

Candidate table (asserts, member): 3 code-from-image, 1 count-dataset-tokens, 2 crack-7z-hash,
2 extract-moves-from-video, 2 fix-ocaml-gc, 2 gcode-to-text, **5 log-summary-date-ranges**,
3 mteb-leaderboard, 3 mteb-retrieve, 1 sqlite-db-truncat­e, **5 vulnerable-secret**.
Excluded at step 2 for non-stdlib imports: bn-fit-modify (pandas, scipy), fix-code-vulnerability
(bottle), multi-source-data-merger (pandas), regex-chess (chess), sparql-university (rdflib).

Counter's own print (run by me at base rev in my clone:
`python3 plans/round81_c1_new_members.py --lane <clone> --rev 4e833e9f… --work <scratch>`)
matches my derivation byte-for-byte on the member list:

```
CANDIDATES n=11 rule=stdlib-only-unattempted-max-asserts asserts=5 code-from-image,count-dataset-tokens,crack-7z-hash,extract-moves-from-video,fix-ocaml-gc,gcode-to-text,log-summary-date-ranges,mteb-leaderboard,mteb-retrieve,sqlite-db-truncate,vulnerable-secret
UNIVERSE members=2 log-summary-date-ranges,vulnerable-secret
DEFECT RECEIPT-UNTRACKED log-summary-date-ranges corpus/evidence/round81/log-summary-date-ranges-probe.txt
DEFECT RECEIPT-UNTRACKED vulnerable-secret corpus/evidence/round81/vulnerable-secret-probe.txt
DEFECTS n=2 / TARGET members=2 located=0 reproduced=0 ledger_flipped=0 defects=2 / PREDICATE R81-C1 fail
```

Frozen before-state confirmed (`DEFECTS n=2`, `RECEIPT-UNTRACKED` ×2, rc 1).

## 2. Receipts re-verified at the tip; instruments re-run in my own clone

Both receipts are tracked at tip, first lines match `^# tb2 <member> grader probe\b`, all 13 REQUIRED
stamps present, `WORKTREE clean`, `EXIT 0`, `MINTED_BY plans/round81_c1_remint.py`.
Recomputed with `sha256sum` in the clean clone (== committed bytes, `git status --porcelain` empty):

| field | receipt stamp | recomputed | match |
|---|---|---|---|
| SUBJECT_SHA log-summary-date-ranges (`corpus/evidence/round52/graders/log-summary-date-ranges/tests/test_outputs.py`) | `2fc06a6c…9cb2b4` | `2fc06a6ce1944ad82f84fb437395fa75ed8c0eadd385b92e375c27e5bc9cb2b4` | ✓ |
| SUBJECT_SHA vulnerable-secret (`…/vulnerable-secret/tests/test_outputs.py`) | `f2b65f63…f0c753` | `f2b65f63ac81acd1e80e1ad4c59c1022131a0f9eb20f8ab3212c4ef8d8f0c753` | ✓ |
| TOOL_SHA `plans/round81_log_summary_probe.py` | `a983909a…9a046` | `a983909ac505374643f15ca8cca807a6799a71a70e72b8bda517268cbde9a046` | ✓ |
| TOOL_SHA `plans/round81_vulnerable_secret_probe.py` | `209b28bc…0dca` | `209b28bcd0a5060da41d9f44f8eaf56e5c19956a1370b9408695362812990dca` | ✓ |
| MINTED_BY_SHA `plans/round81_c1_remint.py` | `eb6297f6…5715d` | `eb6297f6b661fe54d4ca07d61bc89f07af379d7dac529da84d05d6fa84b5715d` | ✓ |

LANE_TIP: `git -C <clone> merge-base --is-ancestor 4ac8471b15a40cddc16e1c5cccbde2a087f12117
2fe3d8e6751fa055ac7912616e7fb83b7864360a` → rc 0 (receipt's `LANE_TIP 4ac8471b` is an ancestor of
the measured tip). Host pin re-runnable: this host is `Python 3.14.8` / `OpenSSL 3.6.5 29 Sep 2026`,
equal to both receipts' `HOST_PYTHON`/`HOST_OPENSSL`.

Replay (my clone, once per instrument, per the frozen argv):

```
cd <clone> && /usr/bin/python3 plans/round81_log_summary_probe.py --lane . --work $S/replay/log-summary-date-ranges.work --receipt $S/replay/log-summary-date-ranges.stdout.txt   → EXIT=0
cd <clone> && /usr/bin/python3 plans/round81_vulnerable_secret_probe.py --lane . --work $S/replay/vulnerable-secret.work --receipt $S/replay/vulnerable-secret.stdout.txt        → EXIT=0
```

Mechanical comparison under the frozen A2 projection (drops blank, `REV <hex>`, `cases=`,
`OBSERVED-U `, and CASE/case= lines whose predicted field contains `U`; implemented independently in
`projection_compare.py`):

```
== log-summary-date-ranges ==  receipt-block-lines=14 fresh-stdout-lines=15  projection-lines receipt=13 fresh=13
A2-PROJECTION log-summary-date-ranges: IDENTICAL
== vulnerable-secret ==        receipt-block-lines=14 fresh-stdout-lines=15  projection-lines receipt=13 fresh=13
A2-PROJECTION vulnerable-secret: IDENTICAL
```

Full 13-line projections (both members: 12 CASE lines + `PREDICATE R81-C1 pass`) are identical
line-for-line to the committed OBSERVATIONS blocks — e.g. log-summary: exact-15-rows P/P rc=0,
exact-no-trailing-newline, exact-crlf, exact-quoted-fields all P/P; missing-file F/F rc=1;
empty-file F/F violates=header,row-count; wrong-header, fourteen-rows, sixteen-rows,
one-count-changed, two-rows-swapped, extra-blank-row all F/F; mismatches=0. vulnerable-secret:
exact-flag / -trailing-newline / -surrounded-spaces / -crlf P/P; missing-file F/F; empty-file F/F
violates=content,prefix,suffix,length; wrong-flag F/F; prefix-only, short-flag,
flag-plus-second-line, truncated-flag, flag-case-lowered all F/F. The only replay-stdout extra is
the `REV 2fe3d8e6…` line, which the frozen projection drops. **Both receipts reproduce.**

## 3. Ledger rows and the round-79 population gate

Tip ledger (jq over `git show master:plans/grader-population-ledger.json`):

```
log-summary-date-ranges status=executed subject=tb2-header verdict=predicate round=81 receipt=corpus/evidence/round81/log-summary-date-ranges-probe.txt
vulnerable-secret       status=executed subject=tb2-header verdict=predicate round=81 receipt=corpus/evidence/round81/vulnerable-secret-probe.txt
{executed: 26, unlocated: 0, unexecuted: 62, rows: 88}
```

`verdict=predicate` is exactly `verdict_form` of each block (`^PREDICATE R\d+-C\d+ pass` present).
Tip ledger diff touches only these two rows (unexecuted/unattempted → executed/round 81/receipt/
subject/verdict); nothing else changed.

Round-79 gate print vs ledger's own count — **numbers match**:
gate `LEDGER rows=88 executed=26 unlocated=0 unexecuted=62` == jq `executed=26 unlocated=0`.

**FINDING F1 (major — R81-C1's gate clause is not met at the measured tip).** The claim requires
"the round-79 population gate still exits 0 with `executed=26 unlocated=0`". At tip `2fe3d8e6` the
gate prints the right tuple but **exits 1**:

```
python3 plans/round79_c1_population_ledger.py --lane <clone> --work $S/r79work  →  rc 1
LEDGER rows=88 executed=26 unlocated=0 unexecuted=62
DEFECT CLASS-K-MISMATCH file-artifact cell=16 of 76 ledger=18 of 76
TARGET classes=16 members=88 pairs=230 replayed=26 located=26 unlocated=0 unexecuted=62 …
PREDICATE R79-C1 fail
```

Cause, from committed bytes: tip commit `2fe3d8e6` touches only the two receipts + the ledger
(`git show --stat master`: 3 files). `SKILL.md` line 74 still reads `| file-artifact | 76 |
executed 16 of 76 | …` while the ledger's file-artifact executed count is now 18 (jq:
`[.members[] | select(.status=="executed" and (.classes|index("file-artifact")))] | length` → 18).
The gate exits 0 at both prior tips (`--rev 4e833e9f` and `--rev 4ac8471b`: `executed=24`,
`DEFECTS n=0`, `PREDICATE R79-C1 pass`), so the breakage is introduced by this round's ledger flip
without the SKILL census-cell bump. Consequently the C1 counter at the measured tip (clean clone,
worktree mode) ends:

```
LOCATED log-summary-date-ranges … / REPRODUCED … lines=13 / LOCATED vulnerable-secret … / REPRODUCED … lines=13
LEDGER-GATE rc=1 LEDGER rows=88 executed=26 unlocated=0 unexecuted=62
DEFECT LEDGER-GATE-FAIL rc=1 …
DEFECTS n=1 / TARGET members=2 located=2 reproduced=2 ledger_flipped=2 defects=1 / PREDICATE R81-C1 fail  (rc 1)
```

i.e. every receipt-level leg of R81-C1 verifies (located/reproduced/ledger_flipped 2/2/2, zero member
defects), but the claim as frozen — including "the round-79 population gate still exits 0" — is
**not satisfied at `2fe3d8e6`**. No `c1-after` receipt is committed at tip either (tracked round-81
evidence: `c1-before.txt`, `c1-selftest.txt`, `c1-mutants.txt`, `c1-control-*.txt`, the two probes,
plus C2 files). Repair path for L1: bump the SKILL.md census cell to `executed 18 of 76` (and mint
the after/gate receipt) so the clause can pass; without that commit the claim cannot reach
`DEFECTS n=0`.

## 4. Attack on the selection rule and the controls

**Derivable by one command?** Yes — my `derive_universe.py` re-derives the whole universe in one
command from git bytes alone (§1), and the counter prints `CANDIDATES n=11 …` + `UNIVERSE members=2
…` on every run, so a flattering cut cannot hide in code. Two rule-width notes:
- **F3 (low, latent):** the counter reads the ledger from BASE_REV but capture existence, imports and
  assert counts from the *checked tree* (`derive_universe(base_doc, tree)`), not from BASE_REV as the
  frozen sentence says. At this tip the round-52 capture tree is byte-identical to base
  (`git diff 4e833e9f…2fe3d8e6 -- corpus/evidence/round52/graders` is empty), so there is no present
  divergence — but a future capture edit would silently move the universe. Pinning capture bytes to
  BASE_REV would make the derivation revision-proof.
- **F4 (info):** `imports_stdlib_only` returns True for a capture with zero import statements
  (vacuous `all([])`); no candidate or exclusion is affected today (my step-2 set equals the
  counter's exactly).

**Do-nothing controls.** Cheapest I could build (fixture = copy of the tip tree in my scratch,
`git rev-parse --show-toplevel` asserted equal to the fixture before committing):

1. *Delete the two receipts, keep the flipped ledger* (`do-nothing`):
   `DEFECT RECEIPT-UNTRACKED …` ×2, `DEFECTS n=3`, `PREDICATE R81-C1 fail` — **loses**.
2. *Zero-byte receipts* (`empty-receipts`): `DEFECT SUBJECT-ABSENT`, `DEFECT RECEIPT-MEMBER-COUNT
   names []`, `DEFECT STAMP-MISSING` ×13 — **loses**.
3. *Fabricated COMMAND with otherwise honest receipts* (`command-lie`; I first re-mint by running
   both instruments, then rewrite only the `COMMAND` line to
   `COMMAND echo plans/round81_<member>_probe.py --never-ran`):

```
CANDIDATES n=11 … / UNIVERSE members=2 log-summary-date-ranges,vulnerable-secret
LOCATED log-summary-date-ranges … verdict=predicate / REPRODUCED … lines=13
LOCATED vulnerable-secret … verdict=predicate / REPRODUCED … lines=13
DEFECT LEDGER-GATE-FAIL rc=1 …            ← only defect; caused by F1's stale SKILL cell, not the lie
DEFECTS n=1 / TARGET members=2 located=2 reproduced=2 ledger_flipped=2 defects=1 / PREDICATE R81-C1 fail (rc 1)
```

   **FINDING F2 (medium — claim wider than the counter can enforce).** The counter validates a
   receipt's `COMMAND` only by substring (`spec["tool"] in stamp["COMMAND"]`); `EXIT`/`WORKTREE`/
   `HOST_*` stamps are equality checks against constants or verdict-time state, not re-derivations of
   the mint run. A do-nothing adversary who runs the instruments once (the only way to obtain
   reproducing observations) can then narrate any `COMMAND` they like and pass **every member-level
   check** — on a tree where the r79 gate is green this fixture would have reached
   `PREDICATE R81-C1 pass`; it failed here only via F1. The observations themselves are genuinely
   pinned (fresh-run `REPRODUCTION-MISMATCH`/`REPRODUCTION-EXIT` and the env pins), so execution is
   real; what is not enforced is the receipt's provenance narration. Narrowing option: require the
   `COMMAND` line to re-appear verbatim in a counter-reconstructed argv (`render_argv`), or drop the
   free-text `COMMAND` stamp from the predicate.

The three frozen controls also lose as specified (`--control-flip-ledger-only` → `RECEIPT-UNTRACKED`;
`--control-header-only` → `STAMP-MISSING`/`SUBJECT-SHA-MISMATCH`/`TOOL-PATH`;
`--control-copy-observations` → `REPRODUCTION-MISMATCH`; committed battery receipts
`c1-control-*.txt`, `c1-selftest.txt` 11 cases, `c1-mutants.txt` 10/10 killed at tip).

## Findings by severity

- **F1 (major):** R81-C1's clause "the round-79 population gate still exits 0 with
  `executed=26 unlocated=0`" is false at the measured tip `2fe3d8e6`: gate exits 1 with
  `DEFECT CLASS-K-MISMATCH file-artifact cell=16 of 76 ledger=18 of 76` (`SKILL.md` line 74 not
  bumped; ledger file-artifact executed = 18). C1 counter at tip: `DEFECTS n=1`,
  `PREDICATE R81-C1 fail`, rc 1, with all 2/2/2 receipt legs green. Claim currently not landable
  without the SKILL census-cell fix (and a committed after/gate receipt; none is tracked yet).
- **F2 (medium):** receipt `COMMAND` narration is not verified beyond substring presence — a
  fabricated-COMMAND control passes all member-level checks (pasted above). Execution itself is
  still pinned by reproduction.
- **F3 (low, latent):** universe derivation reads capture bytes from the checked tree, not
  BASE_REV; equivalent today (captures unchanged base→tip), unguarded tomorrow.
- **F4 (info):** vacuous stdlib-only for zero-import captures; no effect on this universe.

## Residual risk and verification gaps

- I did not run the frozen `--selftest`/`--mutants` batteries myself; I read the committed battery
  receipts (`c1-selftest.txt`, `c1-mutants.txt`, `c1-control-*.txt`) and the code paths. Their
  pass/fail labels at tip are the executor's claim, not my measurement — flagged as the one
  unexercised leg.
- The C2 claim is outside my seat; the C2 files at tip were not judged beyond existence.
- F1's repair (SKILL cell bump) is L1's move; my verdict run of the C1 counter was on the committed
  tip, so a later commit that fixes the cell would also need a fresh gate receipt — not yet present.
- Scratch deleted before yield per seat rules; all evidence above is pasted command+output from
  committed bytes or my (deleted) scratch runs, reproducible from the lane at `2fe3d8e6`.
