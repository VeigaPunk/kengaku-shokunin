# R30 DefectFix — exact repair text for D1, D2, D3, D5

Seat `L1Kengaku30.R30DefectFix` (leaf, kengaku round 30, 2026-10-25). Claim C2
(`plans/round-30-claims.md`), routed-defect closure D1–D5 as recorded in
`corpus/lessons/round-29-verifier-spotcheck.md` §5.

Lane HEAD at the time of writing: `363a4eb` ("round-29 verifier spot-check (integrator, hyaku)").
**No lane file was edited by this seat.** Every `old_string` is byte-taken from committed bytes
(`git -C <lane> show HEAD:<path>`), every `new_string` was applied to a scratch tree at
`/tmp/r30-DefectFix/verify` (a `git archive HEAD` extraction) and re-derived there with the frozen
harness `plans/round30_defects.py` and the round-29 counter `plans/adoption_check.py`.

| item | file | status | proof command | observed |
|---|---|---|---|---|
| D1 | `corpus/evidence/round29-attempt2/control-nothing.txt` (new, 1852 bytes) | ready | `python3 plans/round30_defects.py --lane .` | `ok D1 receipt-at-cited-path: repaired` |
| D2 | `corpus/lessons/round-29.md` (HEAD lines 231–232) | ready | same | `ok D2 kappa-sweep-scope: repaired` |
| D3 | `corpus/lessons/round-29.md` (HEAD line 194, S078 cell) | ready | same | `ok D3 s078-line75-word-count: repaired` |
| D5 | `.ufo/waves/round-29/attempt2/adoption-expect.json` | ready | same + counter re-run | `ok D5 s091-usedby-asymmetry: repaired`; counter line unmoved |
| D4 | `.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md` | **not an edit** — a commit | `git -C <lane> commit -- .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md` | out of this seat's scope (lane bounds: no commits) |

The four checks were run together against the patched scratch tree (`plans/round30_defects.py`
imported and `check_d1`/`check_d2`/`check_d3`/`check_d5` called with that tree as `lane`):

```text
D1 -> ''
D2 -> ''
D3 -> ''
D5 -> ''
```

`''` is the harness's repaired sentinel. Over the live lane the same command prints
`ok D<N> <label>: repaired` per repaired item and keeps `DEFECT D4 … defects=1` until the
wave-evidence commit lands, because D4 is a git-state item.

---

## D1 — receipt at the path the report cites

**File:** `corpus/evidence/round29-attempt2/control-nothing.txt` — new file, 1852 bytes, LF endings,
trailing newline after `exit=1`, sha256 `0bc9834eef2cc8db1f66af197bf86d0ade4dbb3f775bc723b9083aaeeb2376a0`.

The defect: `.ufo/reports/round-29/kengaku.md:122-124` (fleet repo, read-only for this seat) cites this
path twice and no such path is committed; the bytes lived only at
`.ufo/waves/round-29/attempt2/control.nothing.txt`, whose field line carries an eighth field
(`verified_at=0`) that the report's quote omits.

**Exact bytes:**

```text
# receipt: round 29 attempt 2 - do-nothing control, frozen adoption counter (claim C1, before-state)
# command: python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json
#   run against a tree holding only `corpus/` extracted from the baseline (no --census: the control
#   line is census=skipped, as the frozen C1 expectation states)
# base:    1f3b0f1ec41ec297130e8944ff97968d32324632 (the round-29 baseline this control names; the
#   round-29 report places the control commit itself at the freeze 8c14a5d)
# re-derived: 2026-10-25 with corpus/ extracted at both revisions - the cited entry file is absent in
#   both trees, so the seven fields and the exit code agree - giving the seven-field line below,
#   exit 1
# provenance: round 30 (2026-10-25) re-commits these bytes at the path the round-29 report cites,
#   corpus/evidence/round29-attempt2/control-nothing.txt, which was absent when round 29 closed -
#   routed defect D1, corpus/lessons/round-29-verifier-spotcheck.md section 5. The values are the
#   control's own, first committed at .ufo/waves/round-29/attempt2/control.nothing.txt line 3; no
#   field was added, dropped or reordered.
# field note: the wave file's line carries `verified_at=0`, an eighth field the counter as frozen at
#   8c14a5d printed and the round-29 M99 repair removed; the report quotes the seven fields the
#   repaired counter prints. Both forms follow, verbatim, each under its own label.
# report quote, verbatim (.ufo/reports/round-29/kengaku.md:122-123, seven printed fields):
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped
# wave file line, verbatim (.ufo/waves/round-29/attempt2/control.nothing.txt:3, eight fields):
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 verified_at=0 census=skipped
exit=1
```

Why this shape rather than a copy of the wave file: the receipt must reproduce **the report's quoted
line** *and* **the wave file's fields**. The report quotes the seven fields the repaired counter
prints (`entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped`, folded over report lines
122–123); the wave file's line 3 carries `verified_at=0`, printed by the counter as frozen at
`8c14a5d` and removed by the round-29 M99 repair. Both forms are carried verbatim, each directly
under its own label, behind a provenance header that names the source bytes, the base commit, the
re-derivation date and the routed-defect pointer.

**Proof (run by this seat, 2026-10-25):**

```text
$ git -C <lane> archive 8c14a5d corpus | tar -x -C /tmp/r30-DefectFix/base
$ python3 plans/adoption_check.py --lane /tmp/r30-DefectFix/base \
      --expect .ufo/waves/round-29/attempt2/adoption-expect.json
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped
exit=1

$ git -C <lane> archive 1f3b0f1 corpus | tar -x -C /tmp/r30-DefectFix/base1f
$ python3 plans/adoption_check.py --lane /tmp/r30-DefectFix/base1f \
      --expect .ufo/waves/round-29/attempt2/adoption-expect.json
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped
exit=1
```

Both runs reproduce the report's quoted line byte-for-byte (`1f3b0f1` is the base the wave file
records, `8c14a5d` the freeze the report names; the entry file is absent in both trees, so fields and
exit code agree). After writing the block above:

```text
$ grep -cF 'entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped' corpus/evidence/round29-attempt2/control-nothing.txt
1
$ python3 plans/round30_defects.py --lane . | grep '^ok D1 '
ok D1 receipt-at-cited-path: repaired
```

---

## D2 — narrow the kappa sentence to the scope its command measured

**File:** `corpus/lessons/round-29.md`, HEAD lines 231–232 (the `judge-calibration-thresholds.md`
bullet of §Rejected candidates). The defect: the sentence renders the sweep "0 hits in the lane"
while the scan's own command was scoped to `corpus/knowledge/*.md`; a lane-wide scan finds 65 files
at the round-29 tip.

**old_string** (2 lines, 2-space indent, U+2013 in `test–retest`, U+2192 before `0 hits`):

```text
  point duplicates `knowledge/llm-judge-calibration.md:7-13`. Only per-variable kappa and a
  test–retest ceiling are new (`grep kappa` → 0 hits in the lane).
```

**new_string:**

```text
  point duplicates `knowledge/llm-judge-calibration.md:7-13`. At the sweep's own scope,
  `grep -rn kappa corpus/knowledge/*.md` → 0 hits; only per-variable kappa and a test–retest
  ceiling are new. A lane-wide `git grep -li kappa` covers more than `corpus/knowledge/*.md` —
  65 files at tip `2ff4b6f`, 63 at the freeze `8c14a5d` — mostly the round-12 Greek-letter token
  vocabulary, which is why the sweep is stated at the scope its command measured.
```

The surrounding prose is untouched: the bullet head
(`- \`judge-calibration-thresholds.md\` — reject, narrow, on premise (Q3/Q6): …`) and the next
bullet (`benchmark-grader-semantics.md`) are outside the pair. The sentence keeps its own words
("only per-variable kappa and a test–retest ceiling are new") and gains the measured scope plus the
two file counts, so the reject's measurement is stated where it was taken.

**Proof (run by this seat, 2026-10-25):**

```text
$ grep -rn kappa corpus/knowledge/*.md | wc -l
0
$ git -C <lane> grep -li kappa 2ff4b6f | wc -l
65
$ git -C <lane> grep -li kappa 8c14a5d | wc -l
63
```

`2ff4b6f` is the round-29 tip and `8c14a5d` the freeze, so both counts re-derive from commits the
lesson's own references name. After the pair is applied,
`python3 plans/round30_defects.py --lane .` prints `ok D2 kappa-sweep-scope: repaired`; the check
requires every line containing `kappa` to name `corpus/knowledge/*.md` and none to say "in the lane",
which the new text satisfies — the lane-wide clause carries the scope on its own line and the
sentence never repeats the token on a scope-free line.

---

## D3 — correct the S078 line-75 word count

**File:** `corpus/lessons/round-29.md`, HEAD line 194 (the S078 row of §Sources opened this round).

**old_string:**

```text
"The verifier never runs in the agent's sandbox." — 9 words, line 75;
```

**new_string:**

```text
"The verifier never runs in the agent's sandbox." — 8 words, line 75;
```

One cell changes, `9` → `8`. The row's other quote ("731 -> 642 tasks: 89 dropped after review." —
8 words, line 99) and the `v2/GATE.md` clause are outside the pair. The registry already agrees:
`corpus/SOURCES.md:101` carries `"The verifier never runs in the agent's sandbox." (8 words)`, so only
the lesson moves.

**Proof (run by this seat, 2026-10-25):**

```text
$ printf '%s' "The verifier never runs in the agent's sandbox." | wc -w
8
$ printf '%s' "The verifier never runs in the agent's sandbox." | wc -c
47
```

`wc -w` = 8 over the exact quoted bytes (47 bytes, no newline fed to `wc`), so 8 is correct and the
lesson's 9 was wrong. After the pair is applied, `python3 plans/round30_defects.py --lane .` prints
`ok D3 s078-line75-word-count: repaired`; the check compares both the lesson cell and the registry
cell against `len(QUOTE.split())`.

---

## D5 — record the S091 used-by asymmetry in the frozen expectation file

**File:** `.ufo/waves/round-29/attempt2/adoption-expect.json`.

**Exact key and value to add** — one new top-level key. `usedby_notes` is never read by
`plans/adoption_check.py`, which reads only `access_date` and `entries`, so the printed fields cannot
move:

```json
"usedby_notes": {
  "S091": "asymmetry, not a citation: corpus/SOURCES.md lists S091 as used-by corpus/knowledge/benchmark-task-validity-checklist.md, while the entry carries no `source: S091` line - it quotes S091 in its Prior art section as the priced prior instrument. The registry relation is kept as the record of that quote, and the counter's seven printed fields are unchanged (cited_rows=5, the S077-S080 plus S090 rows). Documentation only: plans/adoption_check.py reads access_date and entries, never usedby_notes. Routed defect D5, corpus/lessons/round-29-verifier-spotcheck.md section 5, 2026-10-25."
}
```

**old_string** (the committed tail of the file):

```text
      "sources": ["S077", "S078", "S079", "S080", "S090"]
    }
  ]
}
```

**new_string:**

```text
      "sources": ["S077", "S078", "S079", "S080", "S090"]
    }
  ],
  "usedby_notes": {
    "S091": "asymmetry, not a citation: corpus/SOURCES.md lists S091 as used-by corpus/knowledge/benchmark-task-validity-checklist.md, while the entry carries no `source: S091` line - it quotes S091 in its Prior art section as the priced prior instrument. The registry relation is kept as the record of that quote, and the counter's seven printed fields are unchanged (cited_rows=5, the S077-S080 plus S090 rows). Documentation only: plans/adoption_check.py reads access_date and entries, never usedby_notes. Routed defect D5, corpus/lessons/round-29-verifier-spotcheck.md section 5, 2026-10-25."
  }
}
```

The `entries` array is not touched, and that is the point: `cited_rows` is the count of distinct
`source: S###` lines found in the entry's bytes, while the pass predicate compares it against
`sum(len(entry["sources"]))`; appending `S091` to that `sources` list would print `cited_rows=5` and
then fail on `5 != 6`. The note records the asymmetry in the file the closure named without entering
the counted set.

**Proof (run by this seat, 2026-10-25, against the real lane bytes, read-only):**

```text
$ python3 plans/adoption_check.py --lane <lane> \
      --expect /tmp/r30-DefectFix/expect-before.json --census
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
exit=0
$ python3 plans/adoption_check.py --lane <lane> \
      --expect /tmp/r30-DefectFix/expect-after.json --census
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
exit=0
```

The two printed lines are byte-identical and both equal
`corpus/evidence/round29-attempt2/adoption-measured.txt`, so round 29's frozen line does not move
(`cited_rows=5` held). After the pair is applied, `python3 plans/round30_defects.py --lane .` prints
`ok D5 s091-usedby-asymmetry: repaired`; the check requires the `usedby_notes.S091` key, the
registry's `used-by` cell still naming the entry, and *no* `source: S091` line in the entry — the
entry holds none, its five `source:` lines are S077–S080 and S090, and S091 appears only in §Prior
art.

---

## Retained measurements (all run by this seat)

| command | observed |
|---|---|
| `python3 plans/round30_defects.py --lane .` on the live lane | `ok D1 … ok D2 … ok D3 … DEFECT D4 … ok D5 … defects=1` |
| `check_d1/2/3/5` on `/tmp/r30-DefectFix/verify` after the four pairs | `''`, `''`, `''`, `''` |
| `printf '%s' "<S078 line-75 quote>" \| wc -w` | `8` |
| `grep -rn kappa corpus/knowledge/*.md \| wc -l` | `0` |
| `git grep -li kappa 2ff4b6f \| wc -l` / `8c14a5d` | `65` / `63` |
| counter on the `8c14a5d` corpus and on the `1f3b0f1` corpus | seven-field control line, `exit=1` both |
| counter `--census`, expectation file before vs after the D5 key | identical line, `exit=0` both |

## Risks, divergences, blockers

1. **The live worktree already holds a different D1 receipt.** `corpus/evidence/round29-attempt2/control-nothing.txt`
   exists as a 699-byte untracked sibling write (sha256 `4b478db4…e4bd`). It carries only the
   eight-field wave line — `grep -cF` for the seven-field report quote on it returns `0` — so it does
   not reproduce the report's quoted line, which is the D1 requirement as stated. Adopting the bytes
   above means replacing that file. Both versions satisfy `check_d1`, which only requires the path,
   `entries=0` and `exit=1`.
2. **Anchoring.** The `old_string` pairs are exact against HEAD `363a4eb`. The worktree lesson and
   expectation file were already patched by sibling seats this round, so the pairs will not match the
   worktree as it stands: apply them to the committed bytes, or accept the sibling repairs for D2/D3/D5
   and take only the D1 receipt bytes from this document.
3. **D2 phrasing is line-sensitive by construction.** `check_d2` is line-scoped — every line holding
   the token must name `corpus/knowledge/*.md` — which is why the count sentence does not repeat the
   token on a scope-free line. A later rewrite must keep token and scope on the same line, or the
   check must be relaxed.
4. **Nothing here is unproven.** All four items are byte-exact and re-derived; no item is named as
   non-reproducible. D4 is a commit, not an edit, and this seat holds no commit scope: it stays open
   until the lane commits the critic addendum.
5. No tool was installed or upgraded by this seat, and no network fetch was needed — every byte quoted
   is committed lane or fleet bytes plus `git`-local extraction of lane trees. PACMAN was not used.
