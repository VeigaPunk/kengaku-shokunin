# r10 documentation drafts — `grader.py` landing (kengaku-shokunin round 10, ExecutorDocs)

Draft-only. Nothing here has been written into the repo. Three blocks: (a) SKILL.md
new section + its anti-pattern entry, (b) corpus/README.md evidence-section addition,
(c) LOG.md round-10 entry. Every number quoted in the drafts was recomputed by this
lane from the committed bytes (commands + outputs in §Verification); the only
placeholder tokens are values that exist only after L1's fix runs.

## (a) SKILL.md — new section (insert before `## Production checklist — running an eval`, i.e. at `SKILL.md:362`)

```markdown
## Hermetic grader (operability gate) — `grader.py`

`grader.py` (repo root; stdlib only; no network, no endpoint) replays the two
committed probe trees against their own stored bytes and recomputes every
number their SUMMARYs assert. Deterministic and PYTHONHASHSEED-independent —
never iterate a set where the result is order-sensitive.

| Tree | Recomputed from committed bytes |
|---|---|
| `corpus/evidence/round8-horizon/` | `meta` regenerated from seeds `700 + pid*13` (incl. the `+977` retry chain) and matched field-for-field; each of the 258 non-meta `raw` strings re-parsed through the shipped `extract_json_block` and re-graded against `meta`'s `truth`; B cells re-scored to `outcome` ∈ {corrected, propagated, other}; C cells re-graded via `grade_c` (`square_valid`/`viol_ok`/`preserved`/`over_repair`); all 11 `run.log` SUMMARY lines (A-INC, A-MONO, A-CKPT, B-{corrupt,clean}-{plain,hint}, C-{conflict,benign,norule,MONO}) |
| `corpus/evidence/round9-replication/` | `meta` from seeds `2000 + pid*29`; the 4-cell table incl. mean final `nwrong` (A-INC 4/8 · 0.500, A-CKPT4710 2/8 · 0.875, A-CKPT710 2/8 · 1.375, A-MONO 0/8 · 2.250); the 284-record census (8 `meta` / 248 scored / 28 `filler`); ack compliance from the 80-char-truncated ack `raw` (CKPT4710 32/56 = 57.1%, CKPT710 48/64 = 75.0%) |

| Exit | Meaning |
|---|---|
| `0` | every recomputed value equals the stored one |
| `1` | ≥1 mismatch, each printed `MISMATCH <check-id>: stored=<x> recomputed=<y>` |
| `2` | a required input file is missing or unreadable |

Run `python3 grader.py` (defaults resolve beside the script); inputs overridable
via `--r8-jsonl/--r8-runlog/--r9-jsonl/--r9-md`. `--selftest` corrupts temp
copies only — one flipped stored `ok`, one edited `run.log` SUMMARY number, one
flipped byte inside a `raw` string — and exits 0 only if all three are caught
(exit 1 each): a gate that cannot fail on a deliberately broken copy is not a
gate.

Falsification (round 10): committed tree → **exit 0**; the same command on a
copy with one stored `ok` flipped → **exit 1** (both runs in `LOG.md` round 10).

Append to `## Benchmark anti-patterns` (the number continues the existing list,
which currently ends at 13):

14. **A stored SUMMARY no one can re-derive is a claim, not a measurement.**
    Round 8's SUMMARY spent a round un-recomputable from the repo — the run
    artifact was uncommitted and `raw`-stripped, so ack compliance could not be
    re-audited until round 9 re-landed the bytes. Commit the bytes, then commit
    the command that recomputes every number from them — and prove it can fail.
    (`python3 grader.py --selftest`;
    `corpus/evidence/round9-fleet/harness-mutation.md`)
```

## (b) corpus/README.md — evidence-section addition (insert after `corpus/README.md:57`)

```markdown
In-repo gate (round 10): `grader.py` (repo root) replays both run trees above
offline and recomputes every stored number — `python3 grader.py` → exit 0
(all-match), exit 1 per mismatch (`MISMATCH <check-id>: stored=… recomputed=…`),
exit 2 when an input is missing/unreadable; `python3 grader.py --selftest`
corrupts temp copies and exits 0 only if all three seeded corruptions (flipped
`ok`, edited SUMMARY number, flipped `raw` byte) are caught. Stdlib only, no
endpoint, deterministic.
```

## (c) LOG.md — round-10 entry (append after `LOG.md:16`)

```markdown
- 2026-09-28 — round 10: **operability axis-move** — landed the repo's first in-repo gate: `grader.py` (repo root, stdlib-only, no endpoint, deterministic) replays both committed probe trees against their stored bytes and recomputes every number their SUMMARYs assert — r8: `meta` regenerated from seeds `700 + pid*13` incl. the `+977` retry chain (10/10), all 258 non-meta `raw` re-parsed through the shipped `extract_json_block` and re-graded against `meta`'s `truth`, B-cell `outcome` re-scored, C-cell `grade_c` flags re-derived, all 11 `run.log` SUMMARY lines recomputed; r9: `meta` from seeds `2000 + pid*29` (8/8), the 4-cell table incl. mean final `nwrong` (4/8 · 0.500, 2/8 · 0.875, 2/8 · 1.375, 0/8 · 2.250), the 284-record census (8 `meta` / 248 scored / 28 `filler`) and ack compliance (CKPT4710 32/56 = 57.1%, CKPT710 48/64 = 75.0%). Evidence: `python3 grader.py` → exit `{{EXIT_COMMITTED}}` on the committed tree; the same command on a working copy with one stored `ok` flipped → exit `{{EXIT_CORRUPTED}}` with `{{MISMATCH_COUNT}}` `MISMATCH <check-id>: stored=… recomputed=…` line(s); `python3 grader.py --selftest` → {{SELFTEST_OUTPUT}} (all three seeded corruptions detected — flipped `ok`, edited SUMMARY number, flipped `raw` byte); runnable-file count `find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' | wc -l` → `{{RUNNER_FILES}}` (was 11), closing `SCORECARD.md`'s operability falsifiable target (≥12 runnable files **and** the exit-0-committed / exit-1-corrupted pair); `SCORECARD.md` operability row 4 → 5 under the rubric's ±1. Freshness: endpoint re-verified — `curl -s http://127.0.0.1:34113/v1/models` → `Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`, `/health` → `200`; evidence md5s re-checked (`df154cb5…` `results.jsonl`, `fc3b232f…` `run.log`, `f3c58218…` `results-r9.jsonl`; `replicate.py` is byte-identical to `horizon.py`, md5 `1c157e2a…`), so no claim in this entry rests on `/tmp` or on the live endpoint beyond that probe.
```

## Pattern-matched anchors (in-repo line ranges)

| Draft | Pattern source | Matched |
|---|---|---|
| (a) section body | `SKILL.md:310-361` (`## Planning-horizon & transcript-shape probes`) — heading, one-sentence framing, pipe tables with exact cells, closing scope/limit sentence, citations as backticked paths | section shape, table grammar, "never iterate…" style clause |
| (a) exit table + gate semantics | `corpus/evidence/round9-fleet/harness-mutation.md` (exit-0 self-verifying battery), `SCORECARD.md` §Planned ("exit 1 on a wrong SUMMARY", "`--selftest`" contrast with `../kagi-shokunin/corpus/drift-pins.sh`) | exit-code 0/1/2 table, `--selftest` wording |
| (a) anti-pattern 14 | `SKILL.md:47-113` (`## Benchmark anti-patterns`; entries `1.` at `:49` … `13.` at `:107-113`): `N. **Bold title.**` + observed-numbers sentence + parenthesised citation | numbering continues 13 → 14, bold-title + cited-evidence form |
| (b) note | `corpus/README.md:45-57` (`### \`evidence/\`` heading, 3-row table `:52-54`, prose sentence + inline command at `:56-57`) | prose-note form after the table, command inline in backticks |
| (c) entry | `LOG.md:3-16`, e.g. `:14` (round 9) — single dense paragraph `- 2026-09-28 — round N: **label** — … Evidence: …` with commands, hashes and counts inline | prefix, bold label, "Evidence:" pivot, per-claim command citations |

Integrator notes on the drafts:

- Anti-pattern 14 assumes the list stays numbered; if L1 renumbers or houses the
  rule inside the new section instead, keep the bold title and citation and drop
  the numeral.
- (b) is a note, not a table row, because the existing table's left column is
  keyed by `evidence/` subdirectory and `grader.py` sits at repo root. Row
  variant if preferred: ``| `../grader.py` (repo root) | in-repo gate: replays both run trees offline, `python3 grader.py` → exit 0/1/2 |``.
- (c) placeholders are only L1-owned post-run values: exit codes observed
  (`{{EXIT_COMMITTED}}`, `{{EXIT_CORRUPTED}}`), mismatch counts
  (`{{MISMATCH_COUNT}}`), selftest output (`{{SELFTEST_OUTPUT}}`), file counts
  (`{{RUNNER_FILES}}`). Literal numbers in (a)/(b)/(c) come from the committed
  bytes and were reproduced below.

## Verification (this lane; read-only; commands and observed output)

```
$ python3 -c "…gen_problem from horizon.py, compare to meta…"      # exec of defs only (module import is unsafe: horizon.py:15-16 opens /tmp/bench-r8/results.jsonl)
r8 meta regenerated from seed 700+pid*13: (10, 10, [])
r9 meta regenerated from seed 2000+pid*29: (8, 8, [])

$ md5sum corpus/evidence/round8-horizon/{horizon.py,run.log,results.jsonl} corpus/evidence/round9-replication/replicate.py corpus/evidence/round9-replication/results-r9.jsonl
1c157e2a5f5cd3b8516d30c3d4a9c01d  corpus/evidence/round8-horizon/horizon.py
fc3b232ffc532717e50c1d06e0549acc  corpus/evidence/round8-horizon/run.log
df154cb524bf210782fb0f4a46fd1bdc  corpus/evidence/round8-horizon/results.jsonl
1c157e2a5f5cd3b8516d30c3d4a9c01d  corpus/evidence/round9-replication/replicate.py
f3c58218da27cc6b05dca5a4e10d7f52  corpus/evidence/round9-replication/results-r9.jsonl

$ grep -c '^[A-Z][A-Za-z0-9-]*: [0-9]*/[0-9]*$' corpus/evidence/round8-horizon/run.log
11

$ python3 - <<'PY'   # per-record recomputation from the committed JSONL
r8: 268 records = 10 meta + 258 non-meta, raw on 258/258 non-meta
    cells: A-INC 100, A-CKPT 30, A-CKPT-ack 70, A-MONO 10, B-* 8×4, C-* 4×4, meta 10
r9: 284 records = 8 meta + 276 non-meta, raw on 276/276 non-meta
    cells: A-INC 80, A-CKPT4710 24 (+56 ack), A-CKPT710 16 (+64 ack), A-MONO 8, filler 28, meta 8
final-turn means: A-INC 4/8 0.500 · A-CKPT4710 2/8 0.875 · A-CKPT710 2/8 1.375 · A-MONO 0/8 2.250
ack compliance (raw.lstrip().lower().startswith('ok')): 32/56 = 57.1% · 48/64 = 75.0%
PY

$ curl -s -m 5 http://127.0.0.1:34113/v1/models ; curl -s -m 5 -o /dev/null -w 'health=%{http_code}\n' http://127.0.0.1:34113/health
{"models":[{"name":"/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf",…}]}
health=200
```

Recompute citations used above: `corpus/evidence/round9-replication/replication.md`
(table "A-INC 4/8 / 0.500 … A-MONO 0/8 / 2.250"; "Ack compliance audit … 32/56 =
57.1% … 48/64 = 75.0%") — both reproduced 1:1 from the JSONL by this lane.
`run.log` SUMMARY key list reproduced from `run.log:-40`. UNVERIFIED by this
lane: the post-fix `grader.py` run itself (file does not exist at this HEAD —
`ls grader.py` → No such file or directory), so the placeholder tokens in draft
(c) and the "exit 0 / exit 1" falsification sentence in draft (a) are
L1-fillable claims, not measurements of mine.
