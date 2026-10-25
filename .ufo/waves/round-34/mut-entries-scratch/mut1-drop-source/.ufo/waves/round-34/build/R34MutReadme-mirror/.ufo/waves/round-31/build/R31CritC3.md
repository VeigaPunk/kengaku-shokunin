# R31CritC3 — C3 predicate falsification (kengaku round 31)

Seat: UFO-FSD critic, leaf. No production edits. Fixtures: `/tmp/r31-R31CritC3/`.
Read-only sources used: `plans/round-31-claims.md`, `plans/sources_adopt.py` (working tree), `git show
0883e72:plans/sources_adopt.py`, `corpus/QUALITY.md`, `corpus/lessons/round-30-verifier-spotcheck.md`,
`SCORECARD.md`, `.ufo/waves/round-31/claims/*`.

Bytes attacked. The lane file was moving while I read it (main agent mid-edit): first read 873 lines /
`cases=14`, final read 997 lines / md5 `02efe480f94eed1fef26c04530f5802e` / `cases=17`. All findings
below are reproduced against that final tip *and* against the frozen baseline, and F1/F2 hold against
the baseline, so they do not depend on the moving tip.

Target as measured, on the tip:

```
$ python3 plans/sources_adopt.py --selftest | tail -1
SELFTEST cases=17 failed=0
$ echo $?
0
```

---

## F1 — the predicate's observable is reachable with zero binding code (the predicate is not sufficient)

The frozen predicate's entire observable is `SELFTEST cases=17 failed=0` + exit 0
(`plans/round-31-claims.md:84`). The tally is produced by `print(f"SELFTEST cases={len(cases)}
failed={len(failed)}")` (`plans/sources_adopt.py:888`) over `cases: list[tuple[str, bool]]`, filled by
`case(name, passed)` (`:574`) from a caller-supplied boolean. Nothing in the harness requires a case to
call any function, name any exit code, or touch `bind_failure`.

Counterexample, built from the **frozen pre-change bytes** (`git show 0883e72:plans/sources_adopt.py`,
815 lines) plus three lines that assert nothing:

```
$ grep -c 'url_map\|EXIT_URL' /tmp/r31-R31CritC3/vacuous.py
0
$ python3 /tmp/r31-R31CritC3/vacuous.py --selftest | tail -1
SELFTEST cases=17 failed=0
$ echo $?
0
```

The three injected cases are literally `case("url-map-accepted", True)`,
`case("url-map-mismatch-refused", True)`, `case("url-map-unmapped-refused", True)`. The file contains
zero occurrences of `url_map` or `EXIT_URL`: no binding code, no exit 8, no exit 9, no `--url-map`
flag — and it prints the claim's exact target line and exits 0.

So the predicate cannot distinguish "the binding was implemented and works" from "three names were
appended to a list". The claim's own admission bar already measured this class: `corpus/QUALITY.md:221-223`
— "an exit-code-only criterion loses … **the detector is the PASS-line count, not the pinned integer**
… the integer detects shrinkage, not correctness (one check deleted → `n=732`; a tautologised assertion →
`n=733` PASS), so the gate diff still needs a reviewer". C3's predicate is that integer. It is a
calibration regression against Q20's recorded limit, not a new discovery.

Fair reading of the implementation: the three live cases are **not** vacuous. I mutated the binding
body and each new case is killed by at least one mutation (`/tmp/r31-R31CritC3/mut/`):

| mutation | selftest |
|---|---|
| `bind_failure` → `return ""` (always accept) | `cases=17 failed=2` (16, 17) |
| `bind_failure` → `return "unmapped"` | `cases=17 failed=2` (15, 16) |
| `bind_failure` → `return "url-mismatch"` | `cases=17 failed=2` (15, 17) |
| `if url_map is not None:` → `if False:` (map ignored) | `cases=17 failed=2` (16, 17) |
| `normalize_url` keeps the fragment | `cases=17 failed=1` (15) |
| **`bind_failure` cites-no-url checked before the map** | `cases=17 failed=0` — **survives** |
| **any-cited-URL match narrowed to `cited[0]`** | `cases=17 failed=0` — **survives** |
| **`locates` returns last match instead of first** | `cases=17 failed=0` — **survives** |

Three surviving mutations, one of which (first-vs-last match) is the mechanism behind F2's false green.

## F2 — the disclosed gap is not closed: the gate binds the *first* artifact containing the sentence, not the capture the quote was read from

`locates` returns the first artifact in `load_artifact`'s sorted order whose normalised text contains
the needle (`plans/sources_adopt.py:387-396`); `quote_check` then binds that one name
(`:494-495`). A directory artifact is a documented, selftest-exercised mode
(`load_artifact` docstring; case 12 uses `artifact-dir`).

Fixture `/tmp/r31-R31CritC3/fx/dirA/`: two captures of two **different** documents, both containing the
sentence `the verifier shares the agent's container unless a task opts out`. Row cites
`https://example.invalid/docs/verifier.html`.

```
# map binds the REAL cited capture (b-real.txt) only
$ python3 plans/sources_adopt.py --quote-file row-ok.txt --artifact dirA --url-map m-real.json
QUOTE rows=1 spans=1 located=0 found=1 overlong=0 absent=0 mismatch=0 unmapped=1 malformed=0 ...
  REFUSED S900 unmapped words=11 at a-decoy.txt ...
EXIT=9                      # a correct map is a false RED

# map binds the DECOY (a capture of another document) to the cited URL
$ python3 plans/sources_adopt.py --quote-file row-ok.txt --artifact dirA --url-map m-decoy.json
QUOTE rows=1 spans=1 located=1 found=1 ... mismatch=0 unmapped=0 ...
  ok S900 words=11 at a-decoy.txt ...
EXIT=0                      # a wrong capture is GREEN

# rename a-decoy.txt -> z-decoy.txt, same bytes, same map: verdict flips
$ mv dirA/a-decoy.txt dirA/z-decoy.txt && python3 ... --url-map m-real.json
EXIT=0
```

The verdict is a function of filename sort order. Round 30's disclosure
(`SCORECARD.md:1024`) — "a capture of any document that contains the same string satisfies the gate, so
a row can be green while its quote was never read in the document it cites" — remains true after the
change whenever a second capture shares the sentence: the caller only has to name the decoy in the map.
The claim's surface sentence ("the adoption gate binds the capture to the row's cited URL",
`plans/round-31-claims.md:76`) overstates what the code does: it binds *the first artifact whose bytes
match* to *a caller-supplied assertion* about that artifact's URL.

Second, smaller, unbound: `bind_failure` accepts if **any** URL in the `source` cell matches
(`:412`, set membership). A row citing two documents is bound by the wrong one:

```
$ # row cites .../verifier.html AND .../unrelated.html; map points at the unrelated one
$ python3 plans/sources_adopt.py --quote-file row-two.txt --artifact capture.txt --url-map m-two.json
  ok S900 ... EXIT=0
```

## F3 — exit 8/9 are distinguishable from 2/4 by code, but 8 is not one verdict and 2 is now crowded

- 8 vs 9: separable both by code and by the summary counters `mismatch=` / `unmapped=`
  (`print_quote_report`, `:535`), verified: `mismatch=1 unmapped=0` exit 8; `mismatch=0 unmapped=1`
  exit 9. Good.
- 8 vs 4: separable by code; ordering documented (2, 4, 6, 7, 8, 9) at `:433-440`.
- **8 vs 8**: `bind_failure` returns `"cites-no-url"` for a row whose `source` cell carries no URL
  (`:409-411`), and `quote_check` files every non-`"unmapped"` refusal in the mismatch bucket
  (`:496-497`). A row that simply has no URL is reported as exit 8 and counted as `mismatch=1`:

  ```
  $ python3 plans/sources_adopt.py --quote-file row-nourl.txt --artifact capture.txt --url-map map-ok.json
  QUOTE ... mismatch=1 unmapped=0 ...
    REFUSED S900 cites-no-url ...
  EXIT=8
  ```

  Only the per-row detail text separates them; the exit code and the counters do not. The repairs
  differ (fix the map vs fix the row's `source` cell), and the frozen predicate describes exit 8 as
  "mapped to a different URL" (`plans/round-31-claims.md:86`), which is narrower than the code.
- **2 vs argparse 2**: the change *adds* a producer of exit 2 — a malformed map returns
  `EXIT_QUOTE_UNREADABLE` (`:947-951`):

  ```
  $ python3 plans/sources_adopt.py --quote-file row-ok.txt --artifact capture.txt --url-map map-broken.json
  QUOTE problem=--url-map is unreadable: Expecting value: line 1 column 1 (char 0)
  EXIT=2
  ```

  `EXIT_QUOTE_UNREADABLE = 2` is commented "same class as argparse usage errors" (`:49`), so after this
  change a caller branching on 2 cannot tell a mistyped flag from a broken map. The claim's control
  line uses "argparse exit 2" as its evidence; that code is no longer unique to argparse in the
  post-change tool. The committed receipt survives only because it quotes stderr
  (`.ufo/waves/round-31/claims/gate-before.txt`: `error: unrecognized arguments: --url-map /tmp/z`).

## F4 — `--url-map` is silently ignored on the registry path (the round-30 silent-ignore class, reintroduced)

`main` consults `args.url_map` only inside the `if args.quote_file or args.artifact:` branch (`:941-953`).
The exclusivity guard the round-30 regression seat added covers `--quote-file/--artifact` vs
`--registry/--package` (`:944-945`) and does **not** cover the new flag:

```
$ python3 plans/sources_adopt.py --registry reg.md --package staged.md --url-map map-bad.json
registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
EXIT=0
```

A caller who believes the capture was bound gets a green registry append. The help text at `:921-923`
states the requirement the code does not enforce: "(needs --quote-file and --artifact)". Same shape as
the defect that produced the `:943` comment ("before this guard, a combined invocation silently ignored
the registry work and exited 0"). `--url-map` with `--selftest` is likewise accepted and ignored.

## F5 — the control line proves the flag did not exist, not that the target is unreachable

The frozen control is: pre-change bytes "reject the same invocation with argparse exit 2, i.e. the
control cannot reach the target" (`plans/round-31-claims.md:87-89`). Its receipt shows two things:

```
r31-gate-baseline.py: error: unrecognized arguments: --url-map /tmp/z
url_map_exit=2
SELFTEST cases=14 failed=0
selftest_exit=0
```

The second pair is the one that matters: **the pre-change tree's selftest already exits 0**. The only
delta the control establishes is the integer 14 → 17. The first pair establishes that `--url-map` was
not an argument. Neither establishes that `SELFTEST cases=17 failed=0` requires the binding — F1's
vacuous copy is a counterexample to exactly that claim, and it is a *stronger* control than the
committed one, because it holds the observable fixed and varies only the implementation. A control that
varies the flag's existence while the target's observable is reachable without the feature is
non-discriminating.

Also asymmetric: the control is CLI-level (`--url-map` rejected by argparse) while the three target
cases are function-level (`quote_check(..., url_map={...})`, `:845-851`). No selftest case goes through
`main(["--url-map", ...])`, so the flag's wiring, the map-load failure path, and exit propagation are
covered by no case at all — which is how F4 survived.

## F6 — what the claim still does not bind after the change

1. **Provenance of the map.** `--url-map` is a caller-authored JSON file. Nothing fetches, hashes, or
   records an HTTP status for the artifact. `{"capture.txt": "<cited url>"}` greens any bytes. The
   binding is artifact → *assertion about* URL, not artifact → URL. F2 shows the assertion can be made
   about the wrong capture.
2. **Which capture the quote was read from** — first-match, sort-order dependent (F2).
3. **Which cited URL** — existential over the `source` cell's URLs (F2).
4. **The CLI contract** — no case drives `main`; `--url-map` on the registry path is silently ignored
   (F4); the help text promises a pairing the code does not enforce.
5. **The `cites-no-url` verdict** — filed as exit 8 / `mismatch=1`, zero selftest coverage (F3; the
   surviving `bind-cites-before-map` mutation flips live `9` to mutated `8` and the selftest stays
   green — verified: live `EXIT=9`, mutated `EXIT=8`).
6. **Q20's out-of-band run.** Q20 (`corpus/QUALITY.md:196-212`) requires a commit touching `plans/*.py`
   to cite a run made in a tree extracted from the commit (`git archive <sha> | tar -x -C <tmp>`) with
   the exit code and pinned count line, committed as `.ufo/waves/round-<N>/gate-receipt.txt`. C3's
   counting command is a working-copy run and `.ufo/waves/round-31/gate-receipt.txt` does not exist.
   Q20 also requires the old→new count change to be explained in the same commit's diff (14 → 17).

---

## Direct answers

1. **Yes.** `SELFTEST cases=17 failed=0` + exit 0 is reached by the frozen baseline bytes plus three
   `case(name, True)` lines (F1); the file has zero binding code and still rejects `--url-map` with
   argparse 2. The case tuple passes trivially because `case()` accepts any boolean the caller writes
   and nothing re-derives the count from behaviour.
2. **Partly.** 8 vs 9 and 8/9 vs 4 are separable by code and by the `mismatch=`/`unmapped=` counters.
   8 is *not* one verdict: a row with no cited URL reports 8 and `mismatch=1` (F3). 2 is not
   separable from a usage error at all — by design, and the change adds a second producer of 2.
3. **Only that the option did not exist.** The control varies the flag's presence, not the target's
   reachability; the pre-change tree already satisfies "exit 0" and the vacuous copy satisfies the full
   target line (F1, F5).
4. **The map's provenance, the identity of the capture the quote was read from, which cited URL binds,
   the CLI wiring (silently ignored on the registry path), the `cites-no-url` verdict, and Q20's
   out-of-band receipt** (F2, F3, F4, F6).

## Impacted axes

- **operability** — the claim's axis. Two concrete defects: `--url-map` silently ignored on the
  registry path (F4) and the binding unsound for the documented directory mode (F2). Neither is
  disclosed; the claim's surface sentence overstates the result.
- **calibration** — the predicate re-adopts a shape `corpus/QUALITY.md:221-223` already measured as
  non-discriminating (tautologised assertion keeps `n` and PASS), and the control is non-discriminating
  (F5). If scored as-is, the round records an improvement its own bar says a count cannot see.
- **coverage** — not impacted by this claim (C1 owns it); F2 does not touch C1's counter.
- **novelty / depth / freshness / adjacency** — not impacted.

## Smallest safe correction

1. **Predicate (re-freeze before scoring, one added clause, no new tooling):** pair the tally with a
   discrimination run — the three new cases must be observed *failing* on a named mutation of
   `bind_failure` (e.g. body → `return ""` → `cases=17 failed=2`) with that output committed next to
   the selftest receipt, plus one case that drives `main(["--quote-file", …, "--artifact", …,
   "--url-map", …])` so the exit code is the process's, not a returned value. One command, two lines
   of receipt, and F1/F5 stop being satisfiable.
2. **Code (three small edits in `plans/sources_adopt.py`):**
   - extend the existing guard at `:944` — `if args.url_map and not (args.quote_file and args.artifact):
     parser.error("--url-map needs --quote-file and --artifact")` — closing F4 and making the help text
     at `:921` true;
   - `locates` → return *all* matching artifact names and bind on the set (accept if any containing
     artifact is mapped to a cited URL; 9 only if none is mapped; 8 only if all are mapped elsewhere),
     closing F2's false green and false red in the same change;
   - report `cites-no-url` under its own code (or as exit 8 with the predicate amended to say "cannot be
     bound"), so exit 8 names one verdict (F3).
3. **Disclosure (no code):** state in the C3 row that the binding is artifact → caller assertion, not
   artifact → fetch, and that the capture's provenance stays a reviewer's check. That is the honest
   bound round 30 already wrote and C3 currently overwrites.

Tool installs/upgrades: none (no pacman transaction; no network fetch; all fixtures generated locally).
Disk: `/tmp/r31-R31CritC3/` ≈ 400 KB.

VERDICT: REJECT as frozen — the predicate is reachable by three vacuous `case(…, True)` lines on the pre-change bytes (verified: `cases=17 failed=0`, exit 0, zero binding code), and the disclosed gap survives as a sort-order-dependent false green for directory artifacts while `--url-map` is silently ignored on the registry path; fixable by one predicate clause plus three small edits, and not scoreable as `improved` on the evidence the claim names.
