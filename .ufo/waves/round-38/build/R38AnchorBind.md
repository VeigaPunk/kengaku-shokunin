# R38AnchorBind — row-scoped anchor binding: the checker now catches cross-row digest substitution

Seat `R38AnchorBind` (executor, kengaku round 38 wave 1, routed item D3). Target: `plans/anchor_digest_check.py` as
landed on lane tip `2c5f4e0` absorbing round 37's finding: the tool accepted a row whose anchor carries **another
row's real committed digest** (`.ufo/waves/round-37/falsify/F37AnchorRerun.md` §4 `F37A-1`; its mutants M4b and M5
printed `defects=0`, `EXIT=0`).

Artifact (this seat's, not integrated): `.ufo/waves/round-38/build/R38AnchorBind/anchor_digest_check.py`,
`sha256 98847e8930304a23ab3e10dd27cfc3501738467b8871d8b725d24908e6c1f0b2`, 534 lines vs 308 in the lane file
(`+273 / -47` against `sha256 6d7afcd56a95c59f835be04a16263d43db4840cc8a4b111350be4d7cb8d9a323`; full `diff -u` in
`receipts/diff-old-new.txt`). CLI, exit codes (0/1/2), defect line shape
`DEFECT <sid> anchor token=<hex> class=<cls> detail=<why> loc=corpus/SOURCES.md:<line>`, the summary line
`rows= tokens= defects=`, and the verbose `EVIDENCE/BIND/RESOLVED/ABBREV/EXEMPT/ERRATUM` prefixes are kept; one
class is added (`digest-wrong-capture`) and one is new for locator-less claims (`anchor-unbound`).
Fixture harness also retained: `run_fixtures.py`, `sha256 5983297db5f851165c72499a33ea6accd5b44c1cff96245a4621d0d0d2d3975a`.
Environment: `python3 -V` → `Python 3.14.8` (receipt `receipts/provenance.txt`); nothing was installed and no
package-manager transaction was run — nothing was needed. Scratch `/fast/scratch/hyaku/kengaku-r38/R38AnchorBind/` (clone + lane-tip checker copy)
deleted before this seat finished; `TMPDIR` pointed there. Lane, fleet root, jj state untouched.

## 1. What binds what

Each `sha256 <hex>` token must now be a digest of **the capture the row itself names**, not a member of the global
set of every committed evidence digest. Three locator sources, first one that yields a capture winning:

| # | source | rule | rows it binds at tip |
|---|---|---|---|
| 1 | provenance row | committed `PROVENANCE.md` under `corpus/evidence/` whose table line carries this sid and a filename resolving beside it | S070, S072, S073, S074 |
| 2 | upstream URL | `raw.githubusercontent.com/<o>/<r>/<sha>/<subpath>` or `github.com/<o>/<r>/blob/<sha>/<subpath>`: the deepest `<subpath>` component a committed `task.toml` gives as `name = "<org>/<task>"` selects the evidence dir; capture = dir + URL basename | S105–S113 |
| 3 | explicit lane path | a `corpus/evidence/…` path written in the row, bound only if it is a committed file (a directory binds nothing) | S036, S114 |

A capture's accepted digests are the two views of that one named file — sha256 of its committed blob and the digest
a `SHA256SUMS*` beside it lists for that filename — since the assignment sanctions either ("or the capture manifest
entry for that file"). Both views agree at tip for every manifest entry in the lane (receipt
`receipts/manifest-drift.txt`). Set A survives only to label a failure: a 64-hex token in A but not in the row's capture is
`digest-wrong-capture` (detail names both captures), a token in no committed capture is `digest-unknown`. The
erratum exemption inherits the same scoping: its "correction" digest must be the captured digest of the row it names,
so the exemption door no longer opens with a sibling's real digest.

## 2. Lane at tip → defects=0 (no true defects to list)

Clone of `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e` (`git -C <clone> rev-parse --show-toplevel` verified as the
scratch clone), lane files copied in unmodified:

```
$ python3 <fixed> --lane .
rows=107 tokens=15 defects=0
EXIT=0
```

Same tree, round-37 checker (`plans/anchor_digest_check.py`, byte-identical copy, `cmp` clean): `rows=107 tokens=15
defects=0`, `EXIT=0` (`receipts/run-tip-old.txt`, `receipts/run-tip-new-plain.txt`). `--evidence-ref index` on the
clean tree: `rows=107 tokens=15 defects=0`, `EXIT=0` (`receipts/run-tip-new-index.txt`). Two `--verbose` runs are
byte-identical (`sha256 cab851b8…`, `receipts/determinism.txt`).

Every row that carries an anchor token is bound — `rows_with_anchor_tokens=15 unbound=0` (`receipts/coverage.txt`)
— and the verbose run reports all 15 resolutions / exemptions (`receipts/run-tip-new.txt`, `receipts/bindings-tip.txt`):

```
EVIDENCE ref=head files=418 manifest_digests=30 rows=107 paths=485 bound_rows=17 unbound_rows=90
BIND S036 capture=corpus/evidence/attrib-r23-stream.log by=row-path
BIND S070 capture=corpus/evidence/round37/anchor-captures/S070-generate_test_data.py by=provenance-row
BIND S105 capture=corpus/evidence/round35/tb2-eval/test_outputs.py by=url-task
BIND S111 capture=corpus/evidence/round37/tb2-git-webserver/test_outputs.py by=url-task
BIND S114 capture=corpus/evidence/round37/prior-art/tb21-issue-133-body.md by=row-path
```

(five of the 15 `BIND` lines quoted verbatim; the receipt carries all of them, S072/S073/S074/S106–S113 elided).
`bound_rows=17` counts
every row whose text names a resolvable capture, including S025/S047 which carry no sha256 token; `unbound_rows=90`
are rows that make no digest claim, so an empty binding costs them nothing. The 15 token rows are exactly 14
`RESOLVED` plus S110 `EXEMPT` by the round-37 erratum, whose correction `4f7ac05e…96f9c` is now required to be the
digest of `round36/tb2-regex-log/instruction.md` — the capture S110's own URL names.

Independently of the tool, three captures equal their upstream bytes at the row's pinned commit
(`receipts/upstream-identity.txt`, `curl` of `raw.githubusercontent.com/…/2fd12b88…`):

```
configure-git-webserver/tests/test_outputs.py row=526aee3d…6b37 upstream=526aee3d…6b37 MATCH
regex-log/tests/test_outputs.py            row=345c3bd0…8f72 upstream=345c3bd0…8f72 MATCH
configure-git-webserver/tests/verify.sh    row=1dc44c92…3d05 upstream=1dc44c92…3d05 MATCH
```

So the bindings are not merely internally consistent: the captures are the upstream files the rows claim.

## 3. Falsifiers — M4b/M5 rebuilt, plus 3 more cross-capture shapes, 4 locator/erratum controls, 3 round-37 recall checks

All in the scratch clone, one edit at a time, `git -C <clone> diff --stat` recorded per mutant (each shows exactly
`1 file changed, 1 insertion(+), 1 deletion(-)` or `1 insertion(+)`), file bytes restored after each run and the
tree verified clean at the end (`receipts/fixtures-all.txt`). "old" = lane `plans/anchor_digest_check.py`,
"new" = this seat's copy; both run on the identical tree (`receipts/mutant-<id>.txt`).

| # | fixture (edit) | old | new | new class |
|---|---|---|---|---|
| M4b | S111 anchor gains a **second** token = S108's real committed digest (round-37 M4b rebuild) | `tokens=16 defects=0` EXIT 0 | `tokens=16 defects=1` EXIT 1 | `digest-wrong-capture` |
| M5 | S111's digest **replaced** by S108's real committed digest (round-37 M5 rebuild) | `tokens=15 defects=0` EXIT 0 | `defects=1` EXIT 1 | `digest-wrong-capture` |
| M6 | S111's digest replaced by **verify.sh of the same capture dir** | `defects=0` EXIT 0 | `defects=1` EXIT 1 | `digest-wrong-capture` |
| M7 | S070's digest replaced by S073's (same capture dir, provenance-bound) | `defects=0` EXIT 0 | `defects=1` EXIT 1 | `digest-wrong-capture` |
| M9 | S114's digest (row-path bound) replaced by S113's task-capture digest | `defects=0` EXIT 0 | `defects=1` EXIT 1 | `digest-wrong-capture` |
| M8 | S111's digest replaced by a **fabricated** 64-hex token (control: must stay caught) | `defects=1` EXIT 1 | `defects=1` EXIT 1 | `digest-unknown` |
| M10 | S111 keeps its digest but **loses its URL** (control: locator-less claim) | `defects=0` EXIT 0 | `defects=1` EXIT 1 | `anchor-unbound` |
| M12 | S114 names an evidence **directory** instead of a capture file | `defects=0` EXIT 0 | `defects=1` EXIT 1 | `anchor-unbound` |
| M11 | **insert** an erratum for S111 whose only 64-hex token is S108's digest (erratum door) | `defects=0` EXIT 0 | `defects=1` EXIT 1 | `erratum-incomplete` |
| R1 | delete the S110 erratum (round-37 M1 recall) | `defects=1` | `defects=1` | `digest-short` |
| R2 | flip the erratum's last correction digit `96f9c→96f9d` (round-37 M2 recall) | `defects=3` | `defects=3` | `erratum-digest-unresolved`, `erratum-incomplete`, `digest-short` |
| R3 | shorten S108's anchor by one digit (round-37 M3 recall) | `defects=1` | `defects=1` | `digest-short` |

Exact M5 line (`receipts/mutant-M5.txt:23`, one line, quoted in full):

```
DEFECT S111 anchor token=345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72 class=digest-wrong-capture detail=committed-capture-belonging-to-another-capture-corpus/evidence/round36/tb2-regex-log/test_outputs.py-not-the-capture-this-row-names-corpus/evidence/round37/tb2-git-webserver/test_outputs.py loc=corpus/SOURCES.md:126
```

Score under the assigned reading (M4b and M5 are the round-37 survivors, rebuilt verbatim): **2/2 caught**, old
checker **0/2** on the same trees. Recall of the three round-37 mutants the old tool already caught is preserved
(3/3, same classes, same counts). No mutant regressed: old-green → new-red for exactly the 8 cross-capture /
locator / erratum cases (M4b, M5, M6, M7, M9, M10, M11, M12), old-red → still-red for the 4 digest-shape cases
(M8, R1, R2, R3).

## 4. Mechanism notes (why the fix is narrow)

* One capture, not one directory: M6 and M7 fail because the bound digest set is the row's own filename, not the
  dir's contents; S111 may carry `test_outputs.py`'s digest only.
* `task.toml` identity rather than lexical guessing: the deepest URL path component a committed `name =
  "terminal-bench/<task>"` names selects the dir (`configure-git-webserver` → `round37/tb2-git-webserver`,
  `regex-log` → `round36/tb2-regex-log`, `protein-assembly` → `round35/tb2-eval` — a name pair no substring rule
  would guess). Two dirs claiming one task slug, or a task dir holding no file of the URL's basename, bind nothing
  and the row surfaces as `anchor-unbound` instead of silently passing.
* Provenance table is row-keyed: `anchor-captures/PROVENANCE.md` names S070/S072/S073/S074 beside their pinned URL
  and digest, so those four rows bind without a task dir.
* The tool stays read-only: the only subprocesses are `git ls-tree`, `git ls-files`, `git cat-file --batch`
  (`receipts/provenance.txt`), no write path, no network.
* Old behaviour preserved for output consumers: same summary line, same defect grammar, same exit codes; `files=`
  keeps its old meaning (distinct committed evidence digests, 418) with `paths=485` added.

## 5. Limits and open holes (stated, not repaired)

1. **Locator rewriting is out of reach.** A row that rewrites its URL *and* digest together, or adds a provenance
   table line naming another capture, passes: the lane keeps no independent record of which upstream file the row is
   about. What is now caught is substitution that leaves the locator alone — exactly the S110/M5 family.
2. **Round-37 `F37A-2` (index mode is self-certifying) is inherited unchanged.** A staged `SHA256SUMS` line naming a
   fabricated digest still resolves in `--evidence-ref index` because manifest listings are not tied to blob bytes.
   The binding makes the *row* select which manifest entry must carry the digest, which narrows the blast radius to
   the row's own capture name but does not close it. Fix shape remains: in `ref=index`, accept a manifest digest only
   if a staged/committed blob of that digest exists.
3. **An erratum can legitimise a wrong token** if it cites that token as the row's wrong token *and* carries the row's
   real captured digest as correction — append-only semantics, unchanged from round 37; it is now confined to the
   row's own capture family (M11 shows the cross-row variant refused).
4. **Multi-capture rows take the first locator source only.** A row naming both a provenance line and a different
   explicit path binds the provenance line; the checker does not arbitrate which one the anchor "means". No tip row
   is in that state.
5. Not attempted: fetching every capture to prove upstream identity (only 3 of 15 probed, section 2); running the
   C1/C2 counters or any battery (out of this seat's remit); a `plans/round37_c2_verify.py` census-regex cross-check.

## 6. For the L1 (integration is yours)

`plans/anchor_digest_check.py` in the lane was **not** touched — the fixed copy and its receipts are here only.
Replacing the lane file is a byte copy of `anchor_digest_check.py`; its docstring documents the binding rules,
`digest-wrong-capture`, `anchor-unbound` and the limits above, so `corpus/QUALITY.md`-style claims stay accurate.
Suggested post-integration gate: run it on the lane at the integration commit and expect `rows=… tokens=15
defects=0` plus the M4b/M5 fixtures red.

Receipt inventory under `.ufo/waves/round-38/build/R38AnchorBind/receipts/` (24 files, every number above has one):
`run-tip-new.txt` (verbose), `run-tip-new-plain.txt`, `run-tip-old.txt`, `run-tip-new-index.txt`, `bindings-tip.txt`,
`coverage.txt`, `determinism.txt`, `manifest-drift.txt`, `upstream-identity.txt`, `provenance.txt`, `diff-old-new.txt`,
`fixtures-all.txt`, and `mutant-{M4b,M5,M6,M7,M8,M9,M10,M11,M12,R1,R2,R3}.txt`.

VERDICT: anchor-bind-cross-row-caught-yes
