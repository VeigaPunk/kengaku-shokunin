# LessonScribeR80 — lesson sections, report text only

Axes: coverage (held at L0 cap) and calibration (held at ceiling 10, exercised). No other axis or frozen predicate changed.

Freeze: `af51132d8919cedd14d3d3407ae5abc966d5d427`. Measured committed tip: `6669fe72e59718acc1a0f32a92849a544b0b2f1c`, obtained with `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master`. The receipt below stamps the earlier reachable mint tip `6250e94b2adaff8cd22d32f7ab45024f092e3235`; this is not a claim that its instrument was rerun by this scribe.

## Full proposed markdown

```markdown
## Gate

- **S258 admitted** as `own-work`, tier A only for the lane's located-replay instrument and its six frozen members, not independent evidence of benchmark-wide task success. Access date: 2026-11-04 UTC. Source bundle: `plans/round80_c1_located_replay.py`, `plans/round80_probes.json`, and the six `corpus/evidence/round80/<member>-probe.txt` receipts. Located quote, `corpus/evidence/round80/cancel-async-tasks-probe.txt:7`: **"LANE_TIP 6250e94b2adaff8cd22d32f7ab45024f092e3235"** (2 whitespace words). This receipt is 27 lines / 1,596 bytes, sha256 `7923b6dc39a1c201bd92ab3e4b6651a4c5ff83bc9a5606a1162a29bb6aa7f74e`, measured from committed bytes at `6669fe72e59718acc1a0f32a92849a544b0b2f1c`. Its subject is line 1, source/tool hashes and execution stamp are lines 3–10, and observations are lines 12–27. The frozen table has six member entries; its committed file is 43 lines / 1,944 bytes, sha256 `caa4333f2d3a12cc9d5755828937b24aa5ca22fa4f22798031aa7ce6b1520f22`. The counter is 625 lines / 28,550 bytes, sha256 `81bc451c210fbb36fd7c6e27621da68625b9976773e4aac036d3ad78e37e2ef8`. S258 already exists in the registry; this block documents that admission, not a second row. Status `mined`, recheck `90d`.
- **Reject candidate:** "A historical receipt's failed prediction must still be the current verdict, or its old observations can simply be copied under a new subject header." The round-59 OpenSSL receipt records two mismatches; the round-80 receipt instead records corrected predictions with zero mismatches and explicitly preserves the historical divergence. Neither age nor a header proves reproduction. **Flip:** a tracked subject-locating receipt with matching historical/tool hashes, an explicit divergence note when needed, and observations independently reproduced by the frozen argv at the measured tip. The frozen `--control-copy-observations` control must lose on `REPRODUCTION-MISMATCH`; an unnoted historical change must lose on `DIVERGENCE-UNNOTED`.

## Mistakes

- **M80-1 · class `historical-observation-drift` · evidence `corpus/evidence/round59/openssl-probe.txt:3–6,16–17` versus `corpus/evidence/round80/openssl-selfsigned-cert-probe.txt:12,15–16,26–27` · captured-by `R80-C1` historical-divergence comparison (`plans/round80_c1_located_replay.py:269–275`) · fix: preserve the original receipt and its sha256, re-mint the current instrument's actual stdout, and state `HISTORICAL-DIVERGENCE` rather than silently treating the old observations as current.** The historical receipt predicted `F/P/P/P/P/P` for both `perm-loose` and `key-1024` but observed `P/F/P/P/P/P`, ending `cases=12 legs=72 mismatches=2 setup=0 predicted_u=0` and `PREDICATE R59-C1 fail`. The current receipt predicts and observes `P/F/P/P/P/P` for both, ending `cases=12 legs=72 mismatches=0 setup=0 predicted_u=0` and `PREDICATE R59-C1 pass`. This is a corrected prediction derivation, not evidence that the grader changed. The new receipt stamps historical sha256 `ae89476cde80dfeb09106af53c8eab43a89afcde696d800ec0d0c60aa309b094` and current tool sha256 `6faf217c723efaf8d24bd15a9e8aeb873328af4a7f8e9c4ab4ca94b2465d4646`.
  **Fix can fail:** remove the divergence note while retaining the changed observations, then run `python3 plans/round80_c1_located_replay.py --lane <scratch-clone>`; the frozen rule returns a `DIVERGENCE-UNNOTED` defect and fails the claim. Existing committed sensitivity evidence is `corpus/evidence/round80/c1-selftest.txt:14–15`: `CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok`, followed by `CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok`. This scribe read those bytes; it did not execute the counter or recreate that mutation.

## Corrections

- **2026-11-04 · R79-V2:** W04 is **25 before, 26 after**, not “25 W04 … unchanged in both.” The additional line is S256's duplicate-URL warning. This corrects the round-79 census reading, not the frozen claim.
- **2026-11-04 · R79-V3:** **13 unquantified** rows means 12 bare `executed` rows plus one `recipe-unexecuted` row (`container-image`), not “13 bare executed.”
- **2026-11-04 · R79-V4:** S254's 15-word quote is anchored at **capture lines 2322–2326** in `corpus/evidence/round78/sources/git-status.html`: “Show untracked files.” is at 2322; “The mode parameter is used to specify the handling of untracked files.” is at 2326. The round-79 “capture line 2322 (one sentence)” wording was imprecise; these are two sentences across markup, not one sentence on one line.
- **2026-11-04 · R79-V5:** **S256 duplicate-URL kept**. The W04 warning is stated, not hidden: the same URL is retained for a distinct scope, the harness execution model versus the grader bytes. Contract legality does not erase the warning or license an unchanged census count.
```

## Commands and observed outcomes

No counters, builds, probe runtimes, or mutation batteries were executed by this scribe. Commands below read committed artifacts; receipt-reported outcomes are not upgraded into fresh execution evidence.

Working directory for all shell commands: `/home/vgpnk/Projects/shokunin`. Let `L=/home/vgpnk/Projects/shokunin/kengaku-shokunin` and `T=6669fe72e59718acc1a0f32a92849a544b0b2f1c` in the compact command notation below; actual calls used the absolute path and literal hash.

1. `git -C "$L" rev-parse master && git -C "$L" status --porcelain | wc -l` → `6669fe72e59718acc1a0f32a92849a544b0b2f1c` and `5`; exit 0. This was an initial context observation, not a claim that the worktree was clean. No worktree mutation followed.
2. `S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r80/LessonScribeR80"; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT; printf 'scratch=%s\n' "$S"` → `scratch=/fast/scratch/hyaku/kengaku-r80/LessonScribeR80`; exit 0, shell EXIT trap removed scratch.
3. `git -C "$L" show master:corpus/evidence/round80/openssl-selfsigned-cert-probe.txt` → 28 receipt lines including `WORKTREE clean`, `EXIT 0`, the divergence note and the 12-case zero-mismatch observation block quoted above; exit 0. Preceded in the same call by `git -C "$L" rev-parse master`, which again printed T.
4. `git -C "$L" show master:plans/round80_probes.json | sha256sum` → `caa4333f2d3a12cc9d5755828937b24aa5ca22fa4f22798031aa7ce6b1520f22  -`; `... | wc -lc` → `43 1944`; exit 0.
5. `git -C "$L" show master:plans/round80_c1_located_replay.py | sha256sum` → `81bc451c210fbb36fd7c6e27621da68625b9976773e4aac036d3ad78e37e2ef8  -`; `git -C "$L" show "$T":plans/round80_c1_located_replay.py | wc -lc` → `625 28550`; exit 0.
6. `git -C "$L" show "$T":corpus/evidence/round59/openssl-probe.txt | sha256sum` → `ae89476cde80dfeb09106af53c8eab43a89afcde696d800ec0d0c60aa309b094  -`; exit 0.
7. `git -C "$L" show "$T":corpus/evidence/round80/openssl-selfsigned-cert-probe.txt | sha256sum` → `08c10b0d12e18e39daf834538da039c9e31474858a7b3ce3d6d2c393db7b8585  -`; exit 0.
8. `git -C "$L" show "$T":plans/round59_c1_openssl_probe.py | sha256sum` → `6faf217c723efaf8d24bd15a9e8aeb873328af4a7f8e9c4ab4ca94b2465d4646  -`; exit 0.
9. `git -C "$L" show "$T":corpus/evidence/round80/c1-selftest.txt` → 17 committed lines, including the exact two divergence cases quoted in the draft and `SELFTEST cases=16 red=14 failures=0`; exit 0. This command reads evidence, not runs the selftest.
10. `git -C "$L" show "$T":corpus/evidence/round59/openssl-probe.txt` → 17 historical lines, including both `MISMATCH` lines and `PREDICATE R59-C1 fail`; exit 0. This failure is historical receipt content, not a failed command in this seat.
11. `git -C "$L" show "$T":corpus/evidence/round80/cancel-async-tasks-probe.txt` → subject, stamp and observations reproduced in the draft; `... | sha256sum` → `7923b6dc39a1c201bd92ab3e4b6651a4c5ff83bc9a5606a1162a29bb6aa7f74e  -`; `... | wc -lc` → `27 1596`; exit 0.
12. `printf '%s\n' "Historical divergence (the historical receipt's observation lines differ from the block) is reported" | wc -w` → `13`; exit 0. Exploratory alternative quote only; final Gate uses the receipt's two-token stamp instead.

Specialized reads: frozen `plans/round-80-claims.md` in full before shell work; `corpus/lessons/round-79.md:12–49,69–86,119–135`; `corpus/lessons/round-79-verifier-spotcheck.md:160–190`; historical/current OpenSSL receipts; counter `:9–22,269–275,495–540`; `corpus/evidence/round78/sources/git-status.html:2322–2326`; `corpus/SOURCES.md:274`; and routed rows R79-V2–V5. These establish shape, exact correction literals and source location; the correction facts otherwise inherit the frozen plan and routed spot-check rather than a new census run.

## Gates, findings, touched surfaces, limits

- Gates: read committed divergence sensitivity evidence only. No fresh C1/C2 pass or census count claimed. Main should integrate the lesson and run the frozen C1/C2 tip gates and C2 rollback sensitivity checks.
- Findings: historical OpenSSL predictions demonstrably differ from the current receipt; preserving both plus a divergence note avoids presenting corrected predictions as unchanged historical evidence. S258 already occupies registry line 274; do not append another S258 row.
- Touched surface: only `.ufo/waves/round-80/w1/LessonScribeR80.md`; transient own scratch created and removed by EXIT trap. No product lesson, code, judge, plan, registry or fleet file edited. No clone, commit, push, publish, deploy, installation or other runtime invoked.
- Out of scope: integrating the lesson, restamping receipts, rerunning instruments, source-registry edits, assimilation/proposal disposition and round verdict. No failures were produced by this seat's shell commands; initial search reported a missing peer report path, after which direct committed bytes were used.
- Known limit: this draft is measured at T; a later integration tip needs its own main-agent gate run. The quoted old receipt failure and committed selftest result are provenance, not this seat's independent execution.
- Protocol conflict recorded: generic godspeed text asks parallel subagents, but the canonical seat assignment explicitly requires a leaf; no dispatch was made.
- Self-evaluation: accuracy 4 (execution versus receipt evidence explicitly separated; not all correction facts independently recounted); completeness 4 (all requested sections and fail command present, integration intentionally excluded); clarity 4 (long command provenance retained for audit); actionability 4 (paste-ready text, main must integrate); conciseness 4 (evidence ledger necessarily longer than lesson). Overall 4.0. Improvement priority: main runs the frozen sensitivity gates after integration; do not promote this draft into execution evidence. User-agreement self-check: yes, provided report-only scope is retained.

Artifact: `.ufo/waves/round-80/w1/LessonScribeR80.md`.
