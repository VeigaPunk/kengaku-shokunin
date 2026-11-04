# C1CriticR73 — frozen R73-C1 counterexamples

Axes: coverage (advertised command discovery), calibration (frozen predicate identity and controls).
Authority: claims read in full before commands; base d96c3e62, freeze gate extracted from 255c261d. No predicate, registry, or lane implementation edits made by this seat. Live lane changed during review; deterministic results below use extracted frozen bytes, except the explicitly labelled live comparison.

## 1. Frozen predicate is impossible; the subsequent replacement is gameable

Counterexample: 111 existing one-line `pass` scripts, 111 distinct eight-cell registry rows, and one plans/claims.md line naming already-registered `plans/tool_0.py`. The threshold is true and MISSING 0, but the FROZEN gate exits 1: plans_only=0 and PREDICATE R73-C1 fail. Thus the suggested single-line padding does NOT satisfy the complete frozen sentence. Adding a second line naming nonexistent plans/not_present.py changes neither tally nor missing: existence filtering silently discards it.

Stronger defect: every registry key is extracted with CMD from a row in SKILL.md. SKILL.md is also scanned for advertisements. Consequently every registered existing script is advertised by SKILL.md. MISSING 0 therefore implies every advertised script has SKILL.md in its provenance, hence plans_only=0. Frozen r73 requires plans_only>=1: MISSING 0 and R73-C1 pass are mutually exclusive. The stock selftest still reports cases=4 failures=0 because it never tests this conjunction.

During review, the live gate changed to plans_seen>=1 (see exact read-only diff below). On the IDENTICAL 111-script fixture, a single plans-doc line naming an already-registered script now yields ADVERTISED total=111, MISSING 0, PREDICATE R73-C1 pass, rc=0. No new instrument enters the universe through plans/. This is a counterexample to the replacement's coverage meaning, not a fabricated pass of the original frozen gate. The freeze gate cannot pass this or any clean registry fixture.

Calibration note: first live observation before row landing was total=113, registered=105, MISSING 8, plans_only=3; later observation had total=113, registered=113, MISSING 0. The documented exact target 112 is not demonstrated by either observation. These moving-tree observations do not establish a landing commit.

Smallest safe correction: preserve this round's frozen failure; do not substitute a post-score predicate. A separately authorized freeze could compare the pre-row full-minus-legacy advertised set against final registry membership, keeping provenance independent of the registry text. Merely replacing only with seen permits the single-line padding attack demonstrated here.

## 2. Command-form sweep: four missed lane-owned commands

Command: read-only `git -C <lane> ls-tree -r --name-only 255c261d`, then `git -C <lane> show 255c261d:<file>` for exactly 57 plans/*.md and SCORECARD.md, SKILL.md, LOG.md, corpus/README.md; Python re.finditer with the category expressions below. Driver rc=0.

Definite lane-owned misses, all four committed paths exist:
- SCORECARD.md:74 — python3 corpus/evidence/round9-fleet/test_harness.py
- SKILL.md:592 — python3 corpus/evidence/round13-coverage/coverage_census.py
- LOG.md:521 — python3 plans/fixtures/r28/acceptance.py
- SKILL.md:599 — python3 plans/fixtures/r29/mutation_witness.py

Two are hyphenated evidence directories (CMD permits only alphanumerics/underscores); two are deeper plans paths (explicitly excluded fixture helpers, a stated depth tradeoff rather than an undisclosed implementation error). Four occurrences in three files. No hyphenated plans-stem occurrence found.

Other forms: two python -m occurrences in two plans docs are pip installs, not lane verdict instruments. Three uv-wrapped python3 occurrences in LOG.md, SCORECARD.md, SKILL.md are NOT invisible: unanchored CMD finds their inner python3 plans/tb2_grader_probe.py. Zero npx, zero python3 ./, zero python plans/ forms. Five genuine absolute-path command occurrences across three files describe task/container execution, not lane-owned registry instruments. One additional broad-regex hit is a false positive (`uv venv --python /usr/bin/python3`), excluded from the five. Full sweep output below retains it transparently.

Impact: coverage; calibration if wrapper occurrences or upstream grader commands are incorrectly counted as missing lane instruments. Smallest safe correction: retain current-round finding; in an authorized future freeze, support hyphens in lane evidence directories and explicitly enumerate exclusions. Do not inflate the missed-instrument count with installs, wrappers already seen, or upstream task commands.

## 3. Base-byte control is valid on a plans-only fixture

Command: `git -C <lane> show d96c3e62:plans/round52_c2_registry.py` to own scratch (rc=0), and the equivalent show from freeze 255c261d (rc=0). Fixture has registered plans/tool_0.py and existing plans/unregistered.py named ONLY in plans/claims.md. Running base gate on this fixture prints ADVERTISED total=1, MISSING 0, PREDICATE R52-C2 pass, rc=0. Running freeze gate on the same fixture prints total=2, plans_only=1, MISSING 1 with plans/unregistered.py, R73-C1 fail, rc=1.

The requested control behavior is confirmed. This does not validate the separate exact legacy-real-lane receipt against an immutable base-tree replay; that broader replay was not run. Smallest correction: none for this control; preserve its narrow meaning. It proves discovery, not satisfiability of the combined landing predicate.

R73-C1 falsified

Decisive evidence: frozen MISSING 0 implies plans_only=0, whereas frozen r73 requires plans_only>=1; deterministic 111-instrument fixture demonstrates MISSING 0 + threshold true + R73-C1 fail, while selftest remains green. The live plans_seen replacement is a different, demonstrably pad-able predicate.

## Fixture construction and commands

All fixture files were created under /fast/scratch/hyaku/kengaku-r73/C1CriticR73. Each tool_i.py contains `pass\n`. SKILL.md has heading `## Gate/probe registry`, the standard eight-cell table header/separator, and for each i: `| ti | gate | python3 plans/tool_i.py | 0 ok | none | none | read-only | kengaku |` (entry enclosed in backticks). plans/claims.md initially contains just `python3 plans/tool_0.py` enclosed in backticks. Control has one registered tool and a plans doc naming existing unregistered.py. No git fixture mutations or commits were performed. The parser counts the header as a row, hence rows=112 for 111 registered scripts; it does not affect the counterexample.

## Exact gate/control transcript

```text
$ python3 /fast/scratch/hyaku/kengaku-r73/C1CriticR73/gate_base.py --lane /fast/scratch/hyaku/kengaku-r73/C1CriticR73/control
ADVERTISED total=1
REGISTERED total=1 rows=2
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 pass
rc=0

$ python3 /fast/scratch/hyaku/kengaku-r73/C1CriticR73/gate_freeze.py --lane /fast/scratch/hyaku/kengaku-r73/C1CriticR73/control
UNIVERSE mode=full files=2 plans_only=1
ADVERTISED total=2
REGISTERED total=1 rows=2
MISSING 1
  MISSING plans/unregistered.py
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 fail
PREDICATE R73-C1 fail
rc=1

$ python3 /fast/scratch/hyaku/kengaku-r73/C1CriticR73/gate_freeze.py --lane /fast/scratch/hyaku/kengaku-r73/C1CriticR73/padding
UNIVERSE mode=full files=2 plans_only=0
ADVERTISED total=111
REGISTERED total=111 rows=112
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 pass
PREDICATE R73-C1 fail
rc=1

$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c2_registry.py --lane /fast/scratch/hyaku/kengaku-r73/C1CriticR73/padding
UNIVERSE mode=full files=2 plans_seen=1 plans_only=0
ADVERTISED total=111
REGISTERED total=111 rows=112
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 pass
PREDICATE R73-C1 pass
rc=0

$ python3 /fast/scratch/hyaku/kengaku-r73/C1CriticR73/gate_freeze.py --lane /fast/scratch/hyaku/kengaku-r73/C1CriticR73/padding
UNIVERSE mode=full files=2 plans_only=0
ADVERTISED total=111
REGISTERED total=111 rows=112
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 pass
PREDICATE R73-C1 fail
rc=1

$ TMPDIR=/fast/scratch/hyaku/kengaku-r73/C1CriticR73 python3 gate_freeze.py --lane /fast/scratch/hyaku/kengaku-r73/C1CriticR73/padding --selftest
SELFTEST ok clean-fixture
SELFTEST ok missing-fixture
SELFTEST ok incomplete-fixture
SELFTEST ok plans-fixture
SELFTEST cases=4 failures=0
rc=0

$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff 255c261d -- plans/round52_c2_registry.py
diff --git c/plans/round52_c2_registry.py w/plans/round52_c2_registry.py
index e5953ed3..736ae5ca 100755
--- c/plans/round52_c2_registry.py
+++ w/plans/round52_c2_registry.py
@@ -130,10 +130,12 @@ def collect(lane: Path, universe: str = PLANS_UNIVERSE):
 
 def verdict(lane: Path, universe: str = PLANS_UNIVERSE) -> int:
     adv, rows, reg, missing, incomplete, entry_missing, unbacked, duplicate = collect(lane, universe)
+    plans_seen = sorted(p for p, files in adv.items()
+                        if any(x.startswith("plans/") for x in files))
     plans_only = sorted(p for p, files in adv.items()
                         if files and all(x.startswith("plans/") for x in files))
     print(f"UNIVERSE mode={universe} files={len(self_assessment_files(lane, universe))} "
-          f"plans_only={len(plans_only)}")
+          f"plans_seen={len(plans_seen)} plans_only={len(plans_only)}")
     print(f"ADVERTISED total={len(adv)}")
     print(f"REGISTERED total={len(reg)} rows={len(rows)}")
     print(f"MISSING {len(missing)}")
@@ -153,7 +155,10 @@ def verdict(lane: Path, universe: str = PLANS_UNIVERSE) -> int:
         print(f"  DUPLICATE-ROW {r}")
     ok = not (missing or incomplete or entry_missing or unbacked or duplicate)
     print(f"PREDICATE R52-C2 {'pass' if ok else 'fail'}")
-    r73 = ok and universe == "full" and len(plans_only) >= 1
+    # Amendment A1 (round 73): the arm is `plans_seen`, not `plans_only` — a registered
+    # instrument is advertised by SKILL.md too, so `plans_only` is 0 in every tree where the
+    # rows exist.  The observable the widening adds is "the plans/ leg sees instruments".
+    r73 = ok and universe == "full" and len(plans_seen) >= 1
     print(f"PREDICATE R73-C1 {'pass' if r73 else 'fail'}")
     return 0 if r73 else 1
 
rc=0
```

## Sweep patterns and output

```text
hyphenated_lane_path = python3 (?:plans/|corpus/evidence/)[^\s`]*-[^\s`]*\.py
nested_lane_path = python3 plans/[^\s`]+/[^\s`]+\.py
module = \bpython(?:3)? -m [^`\n]+
uv_python3 = uv run[^`\n]*python3 [^`\n]+
npx = \bnpx\s+[^`\n]+
absolute_python_path = (?:\bpython(?:3)? /[^`\n ]+|/usr/bin/python3 /[^`\n ]+)
dot_relative = python3 \./[^`\n ]+
python_lane = \bpython plans/[^`\n ]+
SNAPSHOT 255c261d: 57 plans/*.md + four self-assessment files = 61 files.
hyphenated_lane_path: 2 matches
  SCORECARD.md:74 python3 corpus/evidence/round9-fleet/test_harness.py
  SKILL.md:592 python3 corpus/evidence/round13-coverage/coverage_census.py
nested_lane_path: 2 matches
  LOG.md:521 python3 plans/fixtures/r28/acceptance.py
  SKILL.md:599 python3 plans/fixtures/r29/mutation_witness.py
module: 2 matches
  plans/round-63-claims.md:34 python -m pip install --index-url http://localhost:8080/simple vectorops==0.1.0
  plans/round-68-claims.md:64 python -m pip install --index-url http://localhost:8080/simple vectorops==0.1.0
uv_python3: 3 matches
  LOG.md:1000 uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .
  SCORECARD.md:564 uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .
  SKILL.md:665 uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .
npx: 0 matches
absolute_python_path: 6 matches
  corpus/README.md:79 python3 /app/polyglot/main.py.c
  corpus/README.md:87 python /app/check_cert.py
  plans/round-59-claims.md:57 python /app/check_cert.py
  plans/round-67-claims.md:11 python /usr/bin/python3
  plans/round-67-claims.md:47 /usr/bin/python3 /ctl/driver.py"
  plans/round-67-claims.md:51 /usr/bin/python3 /ctl/driver.py"
dot_relative: 0 matches
python_lane: 0 matches
```

## Scope and self-evaluation

No tool installation/update. No canonical judging, admission, integration or shipping. Required command experiments only; no general verification suite. An early shell used set -e and stopped at the expected fixture rc=1; the complete controlled replay above captures both arms. Initial sweep interpretation was corrected after concurrent lane edits were discovered; final sweep uses immutable freeze bytes. Scratch is removed after writing this evidence and the seat report.

Self-evaluation: accuracy 4 (live observations are explicitly separated from immutable fixtures); completeness 4 (all three assigned findings covered, not an independent replay of every preexisting receipt); clarity 4 (proof and transcripts separated); actionability 4 (safe correction requires a new authorized freeze); conciseness 4 (full transcript retained for provenance). Overall 4.0. Highest-impact improvement applied: distinguish the frozen unsatisfiable predicate from the live gameable replacement. User-agreement self-check: evidence supports the scoped findings, not an admission decision.
