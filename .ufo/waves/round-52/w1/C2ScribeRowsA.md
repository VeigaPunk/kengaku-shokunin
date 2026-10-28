# R52 wave 1 — seat C2ScribeRowsA (scribe): five gate/probe registry rows

Round 52 / hyaku run 11, wave 1 (build), lane `kengaku-shokunin`, base tip
`30801b479e3418c11089b8586178b6960216f364`. Claim served: **R52-C2** (operability 8 → 9), the
`MISSING 28` leg. I am the scribe seat for five of the twenty-eight advertised-but-unregistered
instruments.

## Behaviour

Five registry rows, one per instrument, eight non-empty cells each, written to

- `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsA/rows.md` (deliverable; a copy is committed to this
  report directory as `rows.md`)

| instrument | row name | kind |
|---|---|---|
| `plans/adoption_check.py` | `adoption-check` | **gate** |
| `plans/attrib_probe.py` | `attrib-probe` | **probe** |
| `plans/catalog_probe.py` | `catalog-probe` | **probe** |
| `plans/defect_ledger.py` | `defect-ledger` | **gate** |
| `plans/gate_flip_check.py` | `gate-flip-check` | **gate** |

No row was left unfilled. Every cell states something I either read in the script or measured by
running it; where a fact is code-derived and not executed I say so below.

## Provenance of the facts

The sibling seats' artefacts were **absent** when I started, so I derived every fact myself:

```
$ ls -la /fast/scratch/hyaku/kengaku-r52/C2ExecRowFacts/        # empty (no facts.json)
$ ls -la /fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/         # only empty lane/ and tmp/
```

I read each of the five scripts in full (`adoption_check.py` 168 lines, `defect_ledger.py` 145,
`catalog_probe.py` 378, `gate_flip_check.py` 747, `attrib_probe.py` 1172 — docstring, argparse
block, every `return` and every `open(..., "a")`/`write_bytes` site) and then ran every entry I
cite, so the numbers below are measurements, not inferences.

## Exact commands and measured numbers

All runs from `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, `TMPDIR` set to my scratch.
Nothing in this list writes into the lane.

### The base-tip counter (unchanged, for reference)

```
$ python3 plans/round52_c2_registry.py --lane .
ADVERTISED total=72
REGISTERED total=44 rows=46
MISSING 28      (… including plans/adoption_check.py, plans/attrib_probe.py, plans/catalog_probe.py,
                 plans/defect_ledger.py, plans/gate_flip_check.py …)
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 1     (`order-check`)
PREDICATE R52-C2 fail        exit=1
```

### `plans/adoption_check.py`

```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok        rc=0

$ python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=skipped    rc=1

$ python3 plans/adoption_check.py --lane .
usage: adoption_check.py [-h] [--lane LANE] --expect EXPECT [--census]
adoption_check.py: error: the following arguments are required: --expect                 rc=2

$ python3 plans/adoption_check.py --expect /nonexistent.json --census
FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent.json'               rc=1

$ python3 plans/adoption_check.py --expect <scratch>/empty-expect.json --census
entries=0 cited_rows=0 required=0 -> empty expectation is not a pass                      rc=1
```

`--expect` is required and `--census` is required for a pass: the `ok` conjunction contains
`args.census and census_code == 0` (`plans/adoption_check.py:155-164`), so the seven printed fields
alone never buy a green. Unprinted gating legs: `verified-at: <access_date>`, exact id-set equality,
no duplicate ids, exactly one shaped index row (`:112-152`). Writes nothing; the census leg is
`subprocess.run([...sources-census.sh, "validate", "--root", lane.parent, lane_name])`, fixed argv,
no shell (`:132-140`).

### `plans/attrib_probe.py`

```
$ python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r23-frozen.md
FREEZE-CHECK: reads=1 block_sha=1b2d6a01bfa431ec pinned=1b2d6a01bfa431ec stable=True -> OK   rc=0

$ python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r21-frozen.md
FREEZE-CHECK: reads=1 block_sha=9f0244bb0aa4463c pinned=9f0244bb0aa4463c stable=True -> OK   rc=0

$ python3 plans/attrib_probe.py block-sha --frozen plans/attrib-r23-frozen.md
1b2d6a01bfa431ec4e78bf89fd989f9ad500d10bb78634362a3c0e3bce794f87

$ python3 plans/attrib_probe.py                                              rc=2   (required subparser)

$ python3 plans/attrib_probe.py force-trials --shim glm --out <s>/o.jsonl --receipt <s>/r.log
force-trials: leg forcing is defined for the ds cascade only (alibaba->hyper->opencode-go);
refusing shim 'glm' (exit 2)                                                 rc=2   no file created

$ python3 plans/attrib_probe.py force-trials --shim ds --frozen plans/attrib-r21-frozen.md \
      --out <s>/o.jsonl --receipt <s>/r.log
FREEZE-CHECK: reads=1 block_sha=9f0244bb0aa4463c pinned=9f0244bb0aa4463c stable=True -> OK
force-trials: table version 'attrib-feature-table-v1' is not attrib-feature-table-v2
— no request sent (exit 2)                                                   rc=2   no file created
```

Six subcommands (`block-sha`, `freeze-check`, `trials`, `force-trials`, `stream-trials`, `score`);
**no self-test switch**. `freeze-check` returns 2 (not 1) when the pin fails, which is why the row's
refusal leg is `2`. The only writes are the caller-named `--out` and `--receipt`, both opened `"a"`
(`:545-546`, `:642-643`, `:766-767`, `:1109-1113`). `score` is the single ground-truth read:
`journalctl --user -u <unit>` (`:884-886`).

**Declared limit:** the `score` verdict path (`0` on `PASS`, `1` on `FAIL`, `plans/attrib_probe.py:1115`)
is code-read, not executed — it needs live shim traffic plus a unit journal I will not drive from
this seat. Everything else in that row is measured.

### `plans/catalog_probe.py`

```
$ python3 plans/catalog_probe.py --selftest
… CASE verify-entry-block-red PASS
SELFTEST checks=13 failed=0                                                   rc=0

$ python3 plans/catalog_probe.py --verify --lane .
raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok
HF missing fields: author, sha, lastModified, gated                             rc=0
```

No exit-2 path exists in the script (argparse only); `--diff` is accepted and referenced nowhere
(`grep -n "args.diff\|\.diff" plans/catalog_probe.py` → no hit), which is what the row says.
`--capture` is the only writing mode (`corpus/evidence/round33/catalogs/`: `hf.raw.json`,
`or.raw.json`, `SHA256SUMS`, `after.txt`, `:83-113`); `--verify` re-derives offline (`:139-210`).

### `plans/defect_ledger.py`

```
$ python3 plans/defect_ledger.py --lane .
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass                                                             rc=0

$ python3 plans/defect_ledger.py --lane /nonexistent                          rc=1   (uncaught read)
```

`--lane` is the only flag; no self-test; writes nothing; `git -C <lane> ls-files / ls-tree` as
fixed argv (`:34-35`); a raising check is an observed failure, never a pass (`:127-129`).

### `plans/gate_flip_check.py`

```
$ python3 plans/gate_flip_check.py --selftest
SELFTEST ok=27/27                                                             rc=0

$ python3 plans/gate_flip_check.py --lesson corpus/lessons/round-51.md
FLIP line=19 flip_line=19 item=https://huggingface.co/docs/hub/en/models-commits shapes=flip: resolution=unresolved:no-line
FLIP-DETAIL lesson=corpus/lessons/round-51.md lesson_round=51 refused_rows=4 malformed_resolutions=0
FLIPS total=1 unresolved=1
FLIP-CITE entries=served-endpoint-identity-pin.md missing=README.md not_fired=0 red=0   rc=1

$ python3 plans/gate_flip_check.py --lesson README.md
SETUP no '## Gate' section                                                    rc=2

$ python3 plans/gate_flip_check.py --lesson /nonexistent.md
SETUP unreadable lesson: [Errno 2] No such file or directory: '/nonexistent.md'  rc=2
```

The self-test count is **27**, not the 19 the pre-existing SKILL.md row claims — the round-44
citation leg (`--entry`, `FLIP-CITE`) added eight cases. My row states 27/27 as measured.

## What I attacked, and whether the attack landed

I attacked my own deliverable with the frozen counter rather than trusting a read-through. Fixture:
a real (non-hardlinked) copy of the lane's `SKILL.md`, `SCORECARD.md`, `LOG.md`, `grader.py`,
`corpus/README.md`, `corpus/knowledge/*.md`, `plans/*.py` and `corpus/evidence/*/*.py` at
`/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsA/lane/` (4.8 MB); the malformed `gate-flip-check` row
at `SKILL.md:609` replaced by my five rows; then

```
$ python3 plans/round52_c2_registry.py --lane /fast/scratch/hyaku/kengaku-r52/C2ScribeRowsA/lane
ADVERTISED total=72
REGISTERED total=49 rows=51
MISSING 23        (28 − 5; the five named instruments are gone from the list)
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 1     (`order-check`, not mine)
PREDICATE R52-C2 fail   exit=1   (correct: the other 23 seats' rows are still absent)
```

| attack | mutation | expected | observed |
|---|---|---|---|
| blank a cell | emptied the pinned-values cell of `defect-ledger` | `INCOMPLETE 1` on that row | `INCOMPLETE 1`, `INCOMPLETE-ROW \`defect-ledger\`` — **landed** |
| false self-test | rewrote `--selftest` to `--no-such-flag` in the `gate-flip-check` self-test cell | `SELFTEST-UNBACKED 2` | `SELFTEST-UNBACKED 2` (`order-check`, `gate-flip-check`) — **landed** |
| restore | pristine splice re-applied | back to `INCOMPLETE 0`, `SELFTEST-UNBACKED 1` | as expected — the cells are non-vacuous, not merely present |

So the two legs that would falsify my rows both fire against my rows when the rows are wrong, and
both stay quiet when they are right.

## Findings the integrator needs

1. **`gate-flip-check` is MISSING because its existing row is unparseable, not because it has no
   row.** `SKILL.md:609` holds a 9-cell row: the verdict map writes `fired\|not fired`, and the
   frozen counter splits on *every* pipe including the escaped one
   (`plans/round52_c2_registry.py:56-57`, `parse_rows`). A census over the registry block finds
   exactly one malformed row and it is this one. **My row must replace line 609, not sit beside
   it** — a second row for the same script would leave a duplicate name (round-51 D3 lists
   duplicate id as a C2-gate survivor class) and `reg.setdefault` would keep whichever parses first.
2. **No cell of my five rows contains a `|` character.** Verified by asserting exactly 8 cells per
   row after the split. Any later edit that adds a pipe (even escaped) silently drops the row.
3. **A truthful "no self-test" cell must not name one script plus one `--flag`.** The counter's
   `selftest_unbacked` counts a cell as unbacked when it finds exactly one `.py` name and at least
   one `--flag` and *none* of the flags occur in the script body (`:74-84`). So for
   `adoption-check`, `attrib-probe` and `defect-ledger` I wrote "none declared — no self-test
   switch…" with **no flag token**: naming `--selftest` there in the negative would be read as a
   claim and flagged. This is the one place where the counter's rule and plain prose pull apart;
   the integrator should keep those three cells flag-free.
4. `attrib-probe` is typed **probe** even though its `score` subcommand carries a threshold verdict:
   the row's entry is the pin check (`freeze-check`), the trial modes measure, and the PASS/FAIL
   lives in the verdict map where a reader can see it. `catalog-probe` is a probe for the same
   reason. `adoption-check`, `defect-ledger` and `gate-flip-check` are gates: each admits or refuses
   a frozen expectation set.

## Files produced (absolute paths)

- `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsA/rows.md` — the five rows (deliverable)
- `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsA/skill-with-rows.md` — the spliced scratch `SKILL.md`
  the counter was run against (shows the rows in place, line 609 replaced)
- `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsA/counter-after-5rows.txt` — counter output above
- `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsA/empty-expect.json` — the empty-expectation fixture
- `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsA/lane/` — the 4.8 MB scratch lane copy
- copied into this directory before cleanup: `rows.md`, `skill-with-rows.md`, `counter-after-5rows.txt`,
  `empty-expect.json`

## Out of scope / not done

- I did not touch the lane tree, `.ufo/state/`, `.ufo/watchdog.log`, `templates/`, `scripts/`,
  `MANIFEST.json`, `.scratch/`, or any git/jj state. No commit, add, push, stash, checkout, reset,
  pull. The only lane-path writes are none at all; the counter and all five instruments were run
  read-only from the lane.
- I did not draft the other 23 missing rows (other seats own them) and did not edit
  `SKILL.md` itself — the L1 is the integration owner.
- No tool was installed or upgraded (pacman is paused host-wide; nothing was needed).
- One declared non-executed leg: `attrib_probe.py score`'s `PASS`/`FAIL` exit path (code-read only,
  see above). Everything else cited in the rows is measured.

## Cleanup

`/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsA/` is removed after the receipts above were copied
here; this seat leaves no tree on disk.

Alias: the seat spec names two report paths; `.ufo/waves/round-52/w1/C2ScribeRowsA.md` carries the
same bytes as `.ufo/waves/round-52/w1/C2ScribeRowsA/report.md`.

## Measurement tip (provenance)

Every command above ran against lane HEAD `07ea2084053f5112ea797a653e6a3a96e8cf4a64`, not the
claims file's base tip `30801b479e3418c11089b8586178b6960216f364`. `30801b4` is an ancestor
(`git merge-base --is-ancestor` → true); the two commits between them add only the round-52
artefacts (`plans/round-52-claims.md`, `plans/round52-tasks.json`, both counters, the wave-1 spec
and registry) and touch neither `SKILL.md` nor any of the five instruments. The counter at this tip
reproduces the claims file's frozen before-numbers exactly (`ADVERTISED 72`, `REGISTERED 44 rows=46`,
`MISSING 28`, `SELFTEST-UNBACKED 1`), which is the check that the row work is measured against the
same surface the claim froze. `git status --porcelain` at the end of the seat shows 22 untracked
paths, all wave-1 artefacts of other seats plus my own report directory; no tracked lane file was
modified by this seat.
