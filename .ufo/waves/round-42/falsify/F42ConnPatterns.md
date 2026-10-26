# F42ConnPatterns — cross-claim patterns vs earlier lane instruments (kengaku round 42 wave 2)

Seat: `F42ConnPatterns` (connector, leaf). Scope: the four wave-1 shapes — (a) a counter whose sandbox
sentence was written from a command list while a `.git/config` key executes inside the tool run, (b)
attribution vacuous where the mutated line always runs, (c) a "content" check that is really a consistency
check (V9), (d) a grader that checks one path and executes another — mapped onto earlier lane instruments:
`plans/round3*_*.py`, `plans/round4*_*.py`, `plans/pkg_gate.py`, `plans/order_check.py`,
`plans/tip_receipts.py`. Source of record: the lane clone at 508434ad (docs commit at wave cut),
`/fast/scratch/hyaku/kengaku-r42/F42ConnPatterns/lane` (toplevel verified; nothing committed).

Method: analysis seat — no battery/counter/fixture was run. Every file:line below was read directly from the
clone (`grep`/`sed` outputs included); wave-1 facts are cited to their build reports. Receipt for my shell
work (reads/greps only, nothing written outside scratch and this report dir): `date +%T` `18:05:51`
before/after; `ls -A /home/vgpnk/.local/bin | sha256sum` `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52` (102 names) both times. No battery/counter/fixture run ⇒ no Q32 bwrap envelope required for a counter run; the envelope line is quoted in the anchor reports below.

---

## Shape (a) — sandbox sentence written from a command list; `.git/config` executes

Wave-1 anchor: `R42SentinelCounter` V1 (HIGH) — a fixture `.git/config` `[log] showSignature=true` +
`[gpg] program=<exe>` on a `gpgsig` claims commit runs `<exe>` inside the order tool's run
(`R42SentinelCounter.md`, `targeted.out`: `gpg+log.showSignature log --format=%H [B-runner] rc=0 exec=YES`);
frozen sentence `round42_c1_verify.py:30` "Both tools execute no fixture code (git plumbing only, hooks and
fsmonitor disabled)"; the run env pins exactly two keys (`round42_c1_verify.py:384-386` `GIT_CONFIG_COUNT=2`,
`core.fsmonitor=false`, `core.hooksPath=/dev/null`); `include.path` re-injects them.

| site | file:line | shape | one-line fixture |
|---|---|---|---|
| a1 | `plans/round40_c1_verify.py:56-57` (isolation claim) + `:365-367` (env pins `GIT_CONFIG_COUNT=2`, fsmonitor+hooksPath only) | the round-42 counter's ancestor sentence and pin pair, word-for-word the same two keys; its pinned order tool is byte-identical to round 42's (`round40_c1_verify.py:99` `948d5e1d…` == `order_check.py` PINS) | an order fixture repo whose `.git/config` carries `[log] showSignature = true` + `[gpg] program = <exe>` and a `gpgsig` claims commit → `<exe>` runs inside the reference and mutant runs (`order_check.py:97` executes twice per fixture) |
| a2 | `plans/round41_c1_verify.py:64-65` (isolation claim) + `:396-398` (same two-key pin) | same sentence shape; `sidechannel` is source-only (`:109-111` tokens; scan reads module source, never fixture text), so token-assembled key names pass | a receipts-tool fixture writes `"co"+"re.fsmonitor"` into its `.git/config` → `sidechannel=0`; no executing key is reachable for the receipts tool's command set (`ls-tree`/`show`/`rev-parse` only) [INFERENCE: per the SentinelCounter command matrix those commands trigger no config exec] |
| a3 | `plans/round42_c1_verify.py:29-30` + `:384-386` | the frozen target sentence/pin (wave-1 anchor) | same as a1, measured (`R42SentinelCounter` `targeted.out`) |
| a4 | `plans/order_check.py:97` — `git.out("log", "--reverse", "--diff-filter=A", "--format=%H", "--", path)` | the exact invocation where `gpg.program`+`log.showSignature` executes; present in rounds 40 and 42 at the identical digest `948d5e1d` | a claims commit carrying a `gpgsig` header built with `git hash-object -t commit -w --stdin --literally` → the gpg program runs (no gpg installed) |

## Shape (b) — attribution vacuous where the mutated line always runs

Wave-1 anchor: `R42CritAttribution` — 8/14 mutants have `span ∩ t_lines ≠ ∅` on every fixture; three are
structurally unconditional: XO6/XO7 span `order_check.py:53` (`GATE_P10 = re.compile`) and `:55`
(`CASE_LINE = re.compile`) — module-level, run once per process before any fixture byte is read; X13 spans
`anchor_digest_check.py:570` (`ap.add_argument("--evidence-ref", …, default="head")` in `main`, runs on
every invocation when fixtures pass only `--lane`). Leg f counts a kill when the span line executes, not
when the mutated value is observed.

| site | file:line | shape | one-line fixture |
|---|---|---|---|
| b1 | `plans/round37_c1_verify.py:23-25` — "mutant Mxx … killed iff some fixture's result differs from the reference" | no attribution leg at all: every kill is trivially "attributed" — the extreme ancestor of the vacuous leg (R37 wave 1 showed it gameable; `round37_c1_attribution.py:4-6`) | a battery37 fixture whose junk spec makes the gate exit 2 vs 0 kills any main-path mutant without exercising its branch |
| b2 | `plans/round38_c1_verify.py:29-38` (kill rule) + `:191-204` (`attributed()`) | attribution is clause-level only (silence/mirror/RUN/MAIN): the reference prints clause C, the mutant does not; no requirement that the mutated statement executed — a mutant whose clause prints unconditionally is attributed on any declaring fixture | a P9-class mutant of the "root is not a readable git worktree" return (`round37_c1_verify.py:139-140`): fixture over a non-git root dir, ref prints `P9 DEFECT` → killed; the mutated line runs on every invocation |
| b3 | `plans/round40_c1_verify.py:61-62` — freeze-named limit "a kill records a result difference in the declared direction, not the fixture's intent" | direction-only attribution; the exact XO6/XO7/X13 near-variants that are vacuous in round 42 cite round-40 origin in the frozen table (`round42_c1_verify.py:206-213`: "round-40 source: F40XMutLedgerOrder wit-xo6/wit-xo7", `:176-178`: "round-40 source: F40XMutAnchor W13") | a fixture whose result differs in the declared direction on an unconditional module-level regex mutant → killed, attributed, fixture intent unmeasured |
| b4 | `plans/round41_c1_verify.py:73-74` | the same limit sentence carried into round 41 (no executed-line check yet) | same as b3 |
| (target) | `plans/round42_c1_verify.py:26-29` (leg f) | closes only the shape half; 8/14 spans remain unconditional (measured by `R42CritAttribution` §2.1) | — |

## Shape (c) — a "content" check that is really a consistency/format check

Wave-1 anchor: `R42CritClaims` D2 — V9 is labelled "V9 content" (`round42_c2_verify.py:36-42`, code
`:282-313`) but binds the entry's `## Case table` to the receipt as a triple `(cid, tests letters, observed)`
(`CASE_ROW` `:84`, Note column `.*`), substrings row ids, requires a PROVINCE line naming task+entry and a
README `## Frontier` naming the task; it reads no prose. An informed filler passes 9/9
(`R42CritClaims` §1; `lane-b-c2.txt`/`lane-c-c2.txt`). V7 labels are derived from the receipt's own
`violates=` tags (`R42CritClaims` §1.1 #6), so the requirement map mirrors the probe.

| site | file:line | shape | one-line fixture |
|---|---|---|---|
| c1 | `plans/pkg_gate.py:204-205` — P6 checks the teaches cell only by word count (`len(cells[6].split()) < rules["min_teaches_words"]`) | a content-bearing cell accepted on format alone: accepts a `teaches` cell saying "describing nothing that was read from the captured grader" (measured by `R42CritClaims`:117) | a registry row whose teaches cell is N≥min words of filler that states no finding → P6 ok |
| c2 | `plans/pkg_gate.py:229` — P7 requires only `(?i)falsifi(?:er|ed|es|ability)` inside `## Negative space` | accepts the sentence "Falsifiers are not named here; this is a mechanical filler control." (measured by `R42CritClaims`:118) | an entry whose Negative-space section contains exactly that sentence → P7 ok |
| c3 | `plans/round41_c2_verify.py:186-206` — v4: receipt ids == frozen dry-table ids; summary agrees with CASE lines; `match=NO` cases named in the entry | receipt-vs-freeze and receipt-internal consistency only; nothing reads the grader's content; the round-41 C2 predicate already passed a 43-line content-free filler 8/8 (`.ufo/waves/round-41/build/R41CritClaims.md:114`) | an informed filler copying the receipt's CASE lines and one summary line → v4 ok |
| c4 | `plans/round41_c2_verify.py:232-272` — v7: label `derive(set(violating.values()))` (lines 258,262-264) from the receipt's own `violates=` sets | the requirement-map labels mirror the probe's receipt rather than an independent reading of the grader | a receipt whose `violates=` tags align with the tag table → every map row derives without reading the grader |
| c5 | `plans/round37_c2_verify.py:129-136` — v4 ancestor: ids must equal the frozen dry-table ids (`NCASES`); same family at `round38_c2_verify.py:167-183`, `round39_c2_verify.py:169-192`, `round40_c2_verify.py:164-207` | the receipt-vs-freeze consistency check predates V9 by five rounds; V9's shape-half is its direct descendant | same as c3 against the round-37 dry table |
| (target) | `plans/round42_c2_verify.py:282-313` — V9 | consistency, not content; closes only the no-table filler shape (`control-c2-filler.txt` red) | an informed filler with a copied case table → V9 ok 9/9 (measured by `R42CritClaims`) |

## Shape (d) — a grader/instrument that checks one path and executes another

Wave-1 anchor: `R42CritProbe` §6.1 — `Dockerfile:8` invites editing `/app/sim.c`; the grader compiles
`/tests/sim.c` into the cwd (`test_outputs.py:66`) and runs `/app/sim` (`:119`); `sim.c` parses cwd-relative
`gates.txt` while the harness checks `/app/gates.txt`; the probe fixes cwd=/app (`fibsqrt_probe.py:239`),
making the split invisible to all 16 cases. (`R42CritProbe` D1-D5; `R42ConnPattern` A1/A2 same genus.)

| site | file:line | shape | one-line fixture |
|---|---|---|---|
| d1 | `plans/regex_log_probe.py:121-122` — `mod.Path = lambda _arg: real(p)  # the grader hard-codes /app/regex.txt` | pinned grader bytes (lines 139-142 digest-check) are executed against a substituted path: the hard-coded check path `/app/regex.txt` is redirected to the probe's tmp `regex.txt`/`absent-regex.txt` | case `regex-file-absent` (line 103) writes no `/app/regex.txt` yet the grader reads the tmp file via the patched `Path` |
| d2 | `plans/tb2_grader_probe.py:126` — `mod.Path = lambda _arg: real(p)  # the grader hard-codes /app/gblock.txt` | identical mechanism for `/app/gblock.txt` | a `gblock.txt` case whose `Path` patch feeds a scratch file, never `/app/gblock.txt` |
| d3 | `plans/constraints_probe.py:19-21` — "its `Path(__file__).resolve().parent.parent / "inputs"` is /inputs, which does not exist … the integrity check takes the sha256 branch, as in the task image (tests at /tests, no /inputs)" | the grader's checked path (`/inputs`) never exists in the probe sandbox; the executed branch depends on that absence — the checked form and the executed form are different paths | a case whose integrity-check branch is the `sha256` one because `/inputs` is absent, while a real image would have `inputs/` under `/app` |
| d4 | `plans/round37_c2_verify.py:58` + `:162` … `plans/round42_c2_verify.py:80` + `:218` — `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`; v6 runs it against `<lane>/corpus/SOURCES.md` | the checked subject lives in the clone; the executing tool lives at the fleet root, outside the lane, the clone and every pin (`pkg-spec-r4*.json` has no census token; `R42ConnPattern` A2) | drop a doctored `scripts/sources-census.sh` into the measured clone → v6 still passes because the host copy runs |

## Synthesis

One genus per shape, each with an unbroken successor chain from rounds 36-41 into round 42:

- **(a)** The isolation sentence has been written from the command list plus a two-key pin (`fsmonitor`,
  `hooksPath`) in rounds 40, 41 and 42 (a1-a3); the executing surface is the same pinned `order_check.py`
  `git log --diff-filter=A` in rounds 40 and 42 (a4). Round 41's tool command set (ls-tree/show/rev-parse)
  likely has no reaching key, so its sentence is the same *shape* with a narrower exploit surface.
- **(b)** The round-42 leg f is the first executed-line check; every ancestor (r37 no-attribution kill rule,
  r38-r41 clause/direction attribution) counts kills without any requirement that the mutated statement ran.
  The vacuous XO6/XO7/X13 spans are round-40 mutants (frozen table cites F40 sources), so their "always
  runs" character predates round 42; leg f was added but does not discriminate them.
- **(c)** "Content" checks in this lane have always been cross-artifact consistency: pkg_gate P6/P7 accept
  filler on word-count/regex (c1,c2), C2 v4/v7 compare receipt↔freeze and derive labels from the receipt
  itself (c3,c4), unchanged since round 37 (c5). V9 is the shape-closing descendant, not a content check.
- **(d)** Path-form splits are endemic to the probes: `mod.Path` redirection (d1,d2), the absent-`/inputs`
  integrity branch (d3), and the host-anchored census (d4) all run a checker that names one path while
  executing another — the same split the fibsqrt probe hides by pinning cwd=/app.

**Measured vs inferred.** Measured by wave-1 seats (cited above): gpg exec under the round-42 runner
(`R42SentinelCounter` `targeted.out`); 8/14 vacuous spans (`R42CritAttribution` §2.1); 9/9 filler pass and
V7 self-derivation (`R42CritClaims`); probe path split (`R42CritProbe`). Read/verified by this seat: the
pin lines, tool digests, module-level span lines, v4/v7 bodies, `mod.Path` patches, P6/P7 acceptance lines,
and the census lines in every C2 counter. Inferred (not separately executed): carrying the gpg vector to the
round-40 runner (same pinned tool bytes + same env pin pair; not re-run), and round-41 reachability.

Limits: no battery/counter/fixture was run by this seat (analysis); a site's "fixture" line is a proposed
demonstration, not a run. All file:line citations are from the clone at 508434ad.

VERDICT: patterns-17-sites
