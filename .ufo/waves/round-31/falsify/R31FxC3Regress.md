# R31FxC3Regress — the landed gate's pre-existing behaviour is unchanged (C3 regression)

Seat: `L1Kengaku31.R31FxC3Regress` (leaf, falsify wave 2). Date 2026-10-25.
Item: attack C3's regression surface — `plans/sources_adopt.py` before and after the round-31
landing. Nothing in the lane was edited; every fixture and output lives under
`/tmp/r31fx-C3Regress/`.

**VERDICT: the regression claim survived.** On all five pre-existing adoption shapes and the one
pre-existing quote shape, the landed gate (`dbb07364`) prints byte-identical stdout and the same
exit code as the baseline (`0883e72`); the three new `--url-map` shapes are unreachable on the
baseline (argparse exit 2) and return 0/8/9 on the landed gate, exactly as the frozen predicate
states. The unbound `QUOTE` summary line is byte-identical between baseline and landed, and
conforms field-for-field to the round-30 receipt `corpus/evidence/round30/quote-mode-six-rows.txt`.
Two deltas were found, neither reaching C3's predicate: (1) the committed CLI-evidence file
`corpus/evidence/round31/gate-cli-exits.txt` at `dbb07364` does **not** reproduce from the landed
code (summary-line field order and the no-map `urlmap=none` line are from an earlier printer); (2)
the working tree has drifted from the landed commit (67 lines, uncommitted) — adoption behaviour is
still identical, and quote-mode exits are unchanged, but bound-receipt bytes differ from both the
landed code and the committed evidence.

## 1. Bytes compared

| version | source | sha256 |
|---|---|---|
| baseline gate | `git show 0883e72:plans/sources_adopt.py` → `old_sources_adopt.py` | `47e60021966318c9f36d4cab8e1464a8cd333db114eca3c1689d206cdfef7922` |
| landed gate | `git show dbb07364:plans/sources_adopt.py` → `landed_sources_adopt.py` | `668fc6a20995e78c98f6f46f437044748aa92b42bbb9b4d230c1cdda8c942017` |
| working tree (drift, uncommitted) | `plans/sources_adopt.py` → `new_sources_adopt.py` | `38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0` |

Working tree is ahead of HEAD: `git diff --stat dbb07364 -- plans/sources_adopt.py` shows
67 changed lines (docstring, `bind_failure` now returns `(reason, bound)` tuple, receipts gain
`bound=<artifact>-><url>`, summary line re-ordered and gains `urlmap=<name> entries=N`). The
verdict below measures the **landed** file; §6 records the drift.

## 2. The five pre-existing adoption shapes (R30FxGateRegression §2, re-derived for round 31)

Fixtures (all under `/tmp/r31fx-C3Regress/`):

- `pre-registry.md` = `git show 0883e72:corpus/SOURCES.md` — 88 rows, byte pre-append registry.
- `package-real.md` = table header + separator + live rows S092/S093/S100 from
  `corpus/SOURCES.md` (each 11 cells, `status=mined`, `recheck=180d`, `used-by→`
  `corpus/knowledge/benchmark-verifier-execution-model.md`). sha256 `fd1efbed…`.
- `package-dup.md` = same with **S092 only** duplicated (`staged=4`). sha256 `28070fed…`.
- `package-pipe.md` = same with a literal ` \| ` inserted into S092's scope cell. sha256 `b042393a…`.
- Shared: `ENTRY=corpus/knowledge/benchmark-verifier-execution-model.md`,
  `--access-date 2026-10-25`, `--scope-to-admit` where R30's shape used it.

Run shape (old / landed):

```sh
python3 <script> --registry pre-registry.md --package package-real.md                                        # (a)
python3 <script> --registry pre-registry.md --package package-real.md --admit-ids S092,S093,S100 \
  --entries $ENTRY --access-date 2026-10-25 --scope-to-admit --out block.txt                                 # (b)
python3 <script> --registry pre-registry.md --package package-real.md --admit-ids S092,S093,S100,S101 \
  --entries $ENTRY --access-date 2026-10-25 --scope-to-admit                                                 # (c)
python3 <script> --registry pre-registry.md --package package-dup.md --admit-ids S092,S093,S100 \
  --entries $ENTRY --access-date 2026-10-25 --scope-to-admit                                                 # (d)
python3 <script> --registry pre-registry.md --package package-pipe.md --admit-ids S092,S093,S100 \
  --entries $ENTRY --access-date 2026-10-25 --scope-to-admit                                                 # (e)
```

Results (`diff old-<x>.stdout landed-<x>.stdout` empty; `$?` identical):

| id | old exit | landed exit | stdout | block file |
|---|---|---|---|---|
| (a) real package, strict | 0 | 0 | identical (77 B): `registry=88 staged=3 collisions=0 malformed=0 duplicates=0 defects=0 prose=0` | n/a |
| (b) scoped to the three landed ids | 0 | 0 | identical (100 B) when both run `--out block.txt` from their own cwd | **identical** `sha256 01a732824b83b18cabdc5a9198f4e640e3a1ea80553bb60e0287a76f6482d578` (3018 B) |
| (c) missing requested id `S101` | 5 | 5 | identical (93 B): `  missing: S101` | none written |
| (d) duplicate staged id `S092` | 4 | 4 | identical (106 B): `staged=4 … duplicates=1`, `  duplicates: S092` | none written |
| (e) escaped-pipe row | 4 | 4 | identical (108 B): `staged=2 … malformed=1`, `  malformed: S092:escaped-pipe` | none written |

(b) also run with `--out` names differing only by script dir — stdout differs solely in the
`wrote <path>` string, the same artifact R30 recorded; with identical relative paths the stdout is
byte-identical and the two `block.txt` files hash identically, i.e. the append-block writer is
unchanged end to end.

## 3. The four quote-mode shapes (baseline vs landed)

Fixtures: `qfile.txt` = one S900 row whose anchor is `"the verifier shares the agent container"`
(6 words) and whose `source` cites `https://example.invalid/docs/verifier.html`; `cap.txt`
contains that sentence; `map-ok.json` = `{"cap.txt": "https://example.invalid/docs/verifier.html"}`;
`map-bad.json` = `{"cap.txt": "https://example.invalid/other.html"}`; `map-unmapped.json` = `{}`.

| id | invocation | old exit | landed exit | stdout |
|---|---|---|---|---|
| Q1 | `--quote-file qfile.txt --artifact cap.txt` | 0 | 0 | **identical** (173 B): `QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=cap.txt` + `ok S900` |
| Q2 | Q1 + `--url-map map-ok.json` | 2 (argparse) | 0 | control: old `unrecognized arguments: --url-map …`; landed adds `mismatch=0 unmapped=0 urlmap=entries=1` |
| Q3 | Q1 + `--url-map map-bad.json` | 2 (argparse) | 8 | landed: `mismatch=1`, `REFUSED S900 url-mismatch` |
| Q4 | Q1 + `--url-map map-unmapped.json` | 2 (argparse) | 9 | landed: `unmapped=1`, `REFUSED S900 unmapped` |

This is exactly the C3 control and the three failure-capable outcomes: the baseline rejects every
`--url-map` invocation at argparse exit 2 (matching committed control
`.ufo/waves/round-31/claims/gate-before.txt` line 8 `url_map_exit=2`), and the landed gate returns
0/8/9. `--selftest` also matches C3's comma: old prints `SELFTEST cases=14 failed=0` exit 0,
landed prints `SELFTEST cases=17 failed=0` exit 0, first ten case names identical order, new cases
11–17 = quote-overlong/absent/located/boundary-25 + quote-url-bound-accepted/mismatch-refused/
unmapped-refused. Landed selftest stdout is byte-identical to committed
`corpus/evidence/round31/gate-selftest-after.txt` (cases+summary lines).

## 4. Unbound QUOTE summary line vs round-30 evidence

`corpus/evidence/round30/quote-mode-six-rows.txt` pins the unbound receipt line (e.g. line 6,
S081): `QUOTE rows=1 spans=3 located=3 found=3 overlong=0 absent=0 malformed=0 cap=25
artifacts=.git/COMMIT_EDITMSG,…`. A multi-span run of both gates

```sh
python3 <script> --quote-file qmulti.txt --artifact artdir
```

(a 1-row file with three quoted spans against a 5-file artifact directory) prints, byte-identical
on old and landed, exit 0:

```
QUOTE rows=1 spans=3 located=3 found=3 overlong=0 absent=0 malformed=0 cap=25 artifacts=a.git/COMMIT_EDITMSG,b.git/FETCH_HEAD,b.git/HEAD,b.git/ORIG_HEAD,b.git/config
```

— the same field order, counts and `artifacts=` comma-join as the pinned receipt. The unbound
summary line is unchanged by the round-31 change (the binding fields are appended only when
`--url-map` is given).

## 5. Finding — committed CLI evidence does not reproduce from the landed code

`git show dbb07364:corpus/evidence/round31/gate-cli-exits.txt` cannot be regenerated by
`landed_sources_adopt.py` with the same invocations. Exit codes reproduce exactly (0/8/9/0/2), but
the bytes differ:

- summary line field order — committed: `… overlong=0 absent=0 mismatch=0 unmapped=0
  malformed=0 cap=25 urlmap=entries=1 artifacts=cap.txt`; landed prints: `… overlong=0 absent=0
  malformed=0 cap=25 artifacts=cap.txt mismatch=0 unmapped=0 urlmap=entries=1`
  (my regeneration, e1: `QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0
  cap=25 artifacts=cap.txt mismatch=0 unmapped=0 urlmap=entries=1`);
- the committed no-map line prints binding fields and `urlmap=none`; the landed (and working-tree)
  code prints **no** binding fields without a map;
- the committed `url-map on registry path` line shows the error sentence only; the landed code
  prints the argparse usage block first.

So the evidence file at the landing commit was produced by an intermediate printer revision
(pre-landing) and does not describe the landed gate's output bytes. This is an evidence-fidelity gap
on the C3 surface, not a predicate failure: the frozen predicate counts `--selftest` output/exit and
the control exit, both of which reproduce.

## 6. Working-tree drift (observation)

`plans/sources_adopt.py` in the working tree ≠ `dbb07364` (67 changed lines, uncommitted; the
`git status` run also shows uncommitted edits to `corpus/evidence/round31/gate-cli-exits.txt` and
`gate-selftest-after.txt`, plus untracked `assimilation/`, `falsify/`, `gate-receipt.txt`,
`quote-mode-adopted-rows.txt`, `quote-mode-bound.txt`). On the working-tree gate, all five adoption
shapes still reproduce byte-identically (stdout and exits 0/0/5/4/4), and the four quote-mode exits
are unchanged (0/0/8/9); the bound-receipt bytes differ from both the landed code and the committed
evidence (`artifacts=cap.txt mismatch=0 unmapped=0 urlmap=map-ok.json entries=1`, detail lines gain
`bound=cap.txt->https://example.invalid/docs/verifier.html`). Flagged for the L1; not part of the
landed claim.

## 7. Scope statement

- Lane writes by this seat: this report only. All fixtures, scripts and captured outputs are under
  `/tmp/r31fx-C3Regress/` (well under the 60 MB cap; `/tmp` shared with peers).
- Tools installed: none. `python3` 3.14.8 (system). No package manager touched.
- Not run: no build/lint/formatter gate (the editing wave's gate is the parent's to execute); the
  only executions recorded are the CLI invocations and `--selftest` runs above.
