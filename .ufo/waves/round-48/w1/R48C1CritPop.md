# R48C1CritPop — honest-population identity review

Axis named: **calibration**.

## Freeze and scope

Inspected the committed stage-1 tree at `REV a543d92083557dd9b33ee674e9b99b03411f80af` (commit time `2026-10-27T06:53:29-03:00`). The claims file exists there; `git diff a543d920..HEAD -- plans/round-48-claims.md` was empty. The freeze therefore predates this static inspection. I ran no counter, probe, or scored execution. No external sources were opened; source URLs/access dates are not applicable.

## Evidence

At the frozen base, `plans/round46_c1_verify.py` enumerates `*.py` under battery42/43/44 (line 536), expands builder output into fence rows (432), and computes `hrows` from observed `per` rows (597). A `BREACH` or `ERROR` contributes to `refused` (599); the predicate rejects a row-count or admission mismatch against `HONEST_TOTAL=104` (192, 621). Thus a refused built row is not silently removed by the existing rollup: it remains in the denominator and increments `refused`.

Population inventory: 22 module files expand statically to 104 literal `fid` entries; `uniq -d` found no repeated FID. All 22 module paths occur in the counter's PINS block; there were no symlinked modules and no byte-identical module files. FENCE-RUN output identifies each item as `module fid`; the module rollup prints only `f.name`, so `battery42/a_row.py` and `battery43/a_row.py` are ambiguous in rollup-only evidence. The 104 entries are distinct by FID, but FIDs alone do not establish semantic non-overlap with the nine later-described classes or future critic-authored classes.

Counterexample / remaining denominator hole: the builder wrapper accepts a successful `BUILT []` result: its loop over the decoded list emits no rows and raises no error. Then `build_errors` stays zero and the class is absent from `hrows`. A correctly independently frozen `<H>` catches the reduced count; but if stage 2 derives `<H>` from the same produced rows rather than the intended population, this omission is absorbed. Stage-1 text says stage 2 freezes `<H>` and inputs, but does not specify an independent expected-item manifest or a non-empty-per-module check.

The round-46 lesson describes the nine additions as packed refs after gc/pack-refs, annotated tags, detached HEAD, merge commit, `.gitignore`, 30-commit history, reflog gc, annotated-tag-plus-detached-HEAD, and ignored untracked file. Its located quote: “all nine are newly named modules in the counter's `--sealed` override” (`.ufo/waves/round-46/w2/R46W2C1HoHonest.md`, inspected 2026-10-27). The report records `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0` for the separate standing battery; it does not prove a deduplicated identity set for the nine additions, which were override modules.

## Commands and observed outputs

Commands were read-only except the required shared clone/checkout in my own scratch; no fixture writes or scored runs were made.

- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --format='%H %cI %an %s' -5` → stage-1 commit `a543d920...` at `06:53:29-03:00`, followed by dispatch/handoff commits.
- `git -C ... diff a543d920... HEAD --stat -- plans/round-48-claims.md corpus/lessons/round-46-verifier-spotcheck.md SCORECARD.md` → empty diff.
- `git clone --shared --no-checkout ... /fast/scratch/hyaku/kengaku-r48/R48C1CritPop/lane`; checkout `a543d920...`; `rev-parse HEAD` → `a543d920...`; `rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r48/R48C1CritPop/lane`.
- `find plans/battery42 plans/battery43 plans/battery44 -name '*.py' | wc -l` → `22`.
- `grep -hoE '"fid": "[^"]+"' plans/battery42/*.py plans/battery43/*.py plans/battery44/*.py | sort | ...` → `104`; duplicate FIDs: none.
- Sorted path comparison of battery files against paths extracted from PINS → `unpinned battery modules:` (empty).
- `find ... -type l -print` → empty; SHA-256 duplicate scan of module files → `0` duplicate hashes.
- Static source inspection only; no reports or receipts were produced. No receipt REV applies beyond the inspected revision above.

## Smallest safe correction

At stage 2, freeze an explicit expected-item manifest derived from authored inputs, not counter output: for every honest item record a stable class ID, source module/path, FID, and source digest; require unique IDs/FIDs and exactly one observed result per expected item. Derive `<H>` from that manifest, reject any module producing zero fixtures, and compare the observed identity set to the manifest before scoring. Give rollup rows a fully qualified module path. Explicitly review the nine and all wave-1 additions against the manifest for semantic overlap; do not treat unique FIDs as proof of distinct classes.

Limits: this is a static attack on the frozen base implementation and population. The round-48 counter and stage-2 manifest were not present at the frozen revision, and semantic equivalence among future authored classes cannot yet be measured.

VERDICT: **denominator accounting catches ordinary refused rows and the frozen 104 has unique FIDs; identity/overlap is not yet established for the added classes, and an empty-output module can disappear unless stage 2 independently freezes expected identities and rejects empty output.**