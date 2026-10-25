# DupR22Scout — r22 scored blocks: same sample? (resolves P2)

Read-only. Parsed every `{"kind": "record"}` line and every `## GT + scoring at close` table in the
three receipts; hashed the 20-row table bodies; converted the blocks' journal `@epoch` windows
exactly. `plans/attrib_calibration.py` is absent at read time (`ls`: No such file), so no code was
verified — this is the dedup decision that instrument must implement.

## File shapes (python parse of the three files)

- `attrib-r22-legs.log`: 40 records = two full runs, blocks at `:260` (run-1) and `:312` (run-2);
  frozen last-block rule ⇒ authoritative = `:312`.
- `attrib-r22-opencode-trials.log`: 20 records, one block at `:204`.
- `attrib-r22-legs-hyper.log`: 20 records, **zero** scored blocks (`grep -c 'GT + scoring at close'` = 0; `grep -c '^| T'` = 0).

## Pair table (five-key test requested)

| pair | trial ids | request UTC | predictions | GT | chains | answer |
|---|---|---|---|---|---|---|
| legs↔opencode | SAME labels T01–T20 | DIFFERENT | SAME | SAME | SAME | **PARTIAL** |
| legs↔hyper | SAME labels | DIFFERENT | SAME | ABSENT | ABSENT | **DIFFERENT** |
| opencode↔hyper | SAME labels | DIFFERENT | SAME | ABSENT | ABSENT | **DIFFERENT** |

## Decisive line pairs

legs↔opencode — table identical, sample disjoint:
- `attrib-r22-legs.log:319-339` vs `attrib-r22-opencode-trials.log:211-231`: all 20 tuples equal,
  `sha256(rows)[:16] = 54c7888cd056490c` for both; T03 (`legs:322` vs `opencode:214`) same
  pred=hyper / GT=hyper / `1/alibaba-token-plan FAIL 400; 2/hyper OK 200`.
- `legs:313` window `@1792151616–@1792151737` = 11:53:36–11:55:37Z vs `opencode:205`
  `@1792151440–@1792151562` = 11:50:40–11:52:42Z — disjoint.
- `legs:143` T01 `t0_utc` 11:53:41.144Z vs `opencode:87` T01 11:50:45.244Z; `legs:257` T20
  11:55:07.542Z vs `opencode:201` 11:52:12.302Z — disjoint request sets.
- `opencode:204` block stamped 11:52:23Z, 78 s BEFORE run-2's first request (`legs:143`,
  11:53:41.144Z) ⇒ it cannot have scored run-2.
- `legs:315` pin 77b8d4a0 (freeze-3) vs `opencode:207` pin 3d7861f8 (freeze-2).
- `legs:349` `loo:hdr_tells 19/20` vs `opencode:241` `18/20` — identical 20 predictions cannot give
  different LOO unless the feature samples differ.
- Body level: all 80 records across the three files carry unique `features.id_value`; 0 cross-file
  duplicates (python set test) ⇒ no scored trial is a copy of another file's trial.

legs↔hyper and opencode↔hyper — hyper has no scored block:
- `attrib-r22-legs-hyper.log:129`: `# force-trials done ... journal GT intentionally NOT read`;
  `:222`: `The score phase ... was NOT run by this seat.`
- Its 20 records are a third run: `hyper:14` T01 11:50:58.065Z → `hyper:128` T20 11:52:26.186Z;
  predictions hyper×10 / alibaba×10, but no GT or chain cells exist to compare.

## Consequences

- The frozen dedup key (trial ids, predictions, GT, chains) FIRES on `legs:312` vs `opencode:204`;
  request UTC proves they are distinct populations. A table-shape dedup would collapse 20 real
  trials and understate n. Identity must key on the run (journal window + the block's `t0_utc` set
  or response-id set), so P2's literal predicate is true while its gloss "same sample" is false.
- `legs:260` (run-1, 11:50:06–11:51:49Z) is a third scored sample whose window `legs:261` =
  11:50:01–11:52:19Z encloses the opencode run and most of hyper's; the seats disclose the
  shared-window hazard (`hyper` addendum item 3: per-seat rid provenance "NOT separable";
  opencode triple-traffic amendment). Its table differs from block2 only at T03 (`legs:270`,
  pred/GT opencode-go, 3-leg chain), so it duplicates neither.

VERDICT: PARTIAL for legs↔opencode (identical 20-row table, disjoint request-UTC samples); DIFFERENT for legs↔hyper and opencode↔hyper (hyper has no scored block).
Installs: none.
