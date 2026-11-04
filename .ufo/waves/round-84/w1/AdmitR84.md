# AdmitR84 — R84-C2 admission-bar counter

scope: the R84-C2 counter for `corpus/knowledge/tb2-code-from-image-offline.md`.
One instrument, one measured contract finding. No production file was written.

## Delivered

`round84_c2_admission.py`, sha256
`7558f3f4e10b849b0351cdd672ed66ba4f08c01a254704db6b4c2f6d67fa509e`, at
`.ufo/waves/round-84/w1/AdmitR84/round84_c2_admission.py`.
CLI `--lane DIR [--rev REV] [--work DIR]` plus `--selftest`, `--mutant q1|q21|q13`,
`--control-filler`, `--control-date-only`. Output lines:
`CHECK q1|q21|q13 ok|DEFECT <detail>`, `INFO writer=present|absent`,
`TARGET entries=1 q1=N q21=N q13=N defects=N`, `PREDICATE R84-C2 pass|fail`.
Exit 0 pass, 1 fail, 2 could-not-evaluate.

Rule definitions, regexes, measurement source and determinism notes are in the
script header and in `.ufo/waves/round-84/w1/AdmitR84/report.txt` §Rules.

## Evidence (all in `.ufo/waves/round-84/w1/AdmitR84/`)

| transcript | exit | result |
|---|---|---|
| `base.txt` (`--rev 4087b2f8…`) | 1 | q1=1 q21=1 q13=1 defects=3, fail |
| `selftest.txt` | 0 | 6 fixtures OK, 3/3 mutants killed |
| `mutant-q1.txt` / `-q21` / `-q13` | 0 / 0 / 0 | each rule relaxed to always-true is killed |
| `control-filler.txt` | 0 | BASE bytes stay defects=3, target not reached |
| `control-date-only.txt` | 0 | date-only repair keeps q21=1 q13=1 (defects=2) |
| `worktree.txt` | 1 | same BASE figures without `--rev` |
| `could-not-evaluate.txt` | 2 | unreadable revision |
| `probe-gate-layout.txt` | 0 | w1 citations rejected, falsify accepted, registry required |
| `probe-gate-contract.txt` | 0 | eight isolated Q13 evidence cases |
| `probe-repair-shape.txt` | 0 | compliant end state defects=0, `PREDICATE pass` |

BASE reproduces the frozen before-state exactly (`TARGET entries=1 q1=1 q21=1 q13=1
defects=3`, exit 1).

## Finding: the Q13 checker cannot admit the wave's own report layout

`plans/gate_timing_check.py` (sha256 `51c18a9e…`) accepts only `falsify` or
`wave2`/`wave-2`/`wave_2` directories and only `*.md` citations. Measured:

- `.ufo/waves/round-84/w1/ReviewerR84.md` (+ a w1 registry) → exit 1,
  `second-seat-reports=0`.
- `.ufo/waves/round-84/w1/ReviewerR84/report.txt` → no citation parsed at all.
- A registry outside a second-wave directory is never loaded.

So the successor Gate passes Q13 only if the cited re-read lives in
`.ufo/waves/round-84/falsify/` (or a `wave2`-named dir), is a nonempty `.md`, names the
FULL candidate path `corpus/knowledge/tb2-code-from-image-offline.md`, carries an
anchored `VERDICT:` line, and the directory's `swarm-registry.json` lists the seat with
an allowed role (`reviewer`/`scout`/`critic`/`sentinel`/`revenger`) and an `agentId`
other than `KengakuR84`. The entry must also carry a line-start `writer: KengakuR84`
(the checker fails without it: `candidate has no committed writer: field`).

Trap: the ReviewerR84 seat spec puts `writer: KengakuR84` in its report. Copied
verbatim into the cited `.md`, that line fails the check
(`report writer/author declaration equals candidate writer 'KengakuR84'`). The cited
report must declare its own identity another way (`re-read-by: ReviewerR84` works).

Recommendation: publish the round-84 re-read as
`.ufo/waves/round-84/falsify/ReviewerR84.md` plus
`.ufo/waves/round-84/falsify/swarm-registry.json`, and cite that path from the
round-84 Gate. That is a round-84 wave artifact, not a backdated landing-time review.
Editing the checker to accept `w1/` and `.txt` is the alternative; the counter follows
whichever checker the measured revision carries, so no counter change is needed either
way. This is a contract fact, not a frozen-claim change.

## Recommended repaired recheck line

Measured with the counter's own rules (`probe-repair-shape.txt`):

`recheck: re-verify weekly against pinned source 2fd12b88aafdd04a52c298e3940bcb189f9766d6 with python3 plans/round84_c2_admission.py --lane . --work DIR; next review 2026-12-04`

gives q1=0 and q21=0, and with the admissible Gate above q13=0 (defects=0, exit 0).
A date alone repairs Q1 only; a cadence alone (or `re-verify weekly` without the
literal word pin/re-pin) leaves q21=1. The pin above is the source-line pin, so the
line satisfies Q21 literally.

## Limits

No production bytes, MANIFEST, state file, sibling lane or domain tree touched. No
tool installed or upgraded. No build/lint/general suite run. Scratch was
`/fast/scratch/hyaku/kengaku-r84/AdmitR84`; receipts were copied into the output
directory before cleanup.
