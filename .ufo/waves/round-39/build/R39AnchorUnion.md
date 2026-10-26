# R39AnchorUnion — bind each anchor token to a capture, not to the union of a row's captures (R5a)

Seat: `R39AnchorUnion` (executor, kengaku round 39 / wave 1 BUILD). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
tip `750473847af9c7a461487ba3a589b5519fac5ed8`. Object of the fix: the shipped round-38 D3 checker
`plans/anchor_digest_check.py`, sha256 `98847e8930304a23ab3e10dd27cfc3501738467b8871d8b725d24908e6c1f0b2`
(`sha256sum` in the lane and in the scratch clone, both identical, §0).

Assignment: round-38 closure item **R5a** (`corpus/lessons/round-38-verifier-spotcheck.md` §5 item 5), which cites
`F38AnchorFix` **F1** (`.ufo/waves/round-38/falsify/F38AnchorFix.md` §2). Deliverable, per the ticket: a fixed copy at
`.ufo/waves/round-39/build/R39AnchorUnion/anchor_digest_check.py` that binds each digest token to the capture its own
locator names, with red-before, red-after and no-false-red receipts.

Two axes named and walked (godspeed): **(1) calibration** — the copy must be red on the union shape and stay green on every
state the shipped tool is green on; **(2) operability** — one stdlib file, same argv/exit contract, a defect class that names
the capture that has no token, and a verbose line that shows the binding. Nothing in the lane was edited; the copy is for the
L1 to integrate.

## 0. Setup and baseline (commands and their output)

```
$ S=/fast/scratch/hyaku/kengaku-r39/R39AnchorUnion; git clone -q --shared <lane> "$S/lane"
$ git -C "$S/lane" rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r39/R39AnchorUnion/lane
$ git -C "$S/lane" rev-parse HEAD              -> 750473847af9c7a461487ba3a589b5519fac5ed8
$ sha256sum plans/anchor_digest_check.py corpus/SOURCES.md      (in $S/lane)
  98847e8930304a23ab3e10dd27cfc3501738467b8871d8b725d24908e6c1f0b2  plans/anchor_digest_check.py
  cec138692f48961da41b93f0a9dbab203443716619badbe961aad5c4f5ad089e  corpus/SOURCES.md
$ sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/anchor_digest_check.py
  98847e8930304a23ab3e10dd27cfc3501738467b8871d8b725d24908e6c1f0b2   (same file as the clone)
$ python3 plans/anchor_digest_check.py --lane .                 -> rows=109 tokens=17 defects=0   exit=0
$ python3 plans/anchor_digest_check.py --lane . --verbose       -> 19 BIND, 15 RESOLVED, 1 ABBREV, 1 EXEMPT,
                                                                   1 ERRATUM, last line rows=109 tokens=17 defects=0
$ python3 "$S/probe_bind.py" plans/anchor_digest_check.py .     -> rows=109 rows_with_multi_capture=0
                                                                   rows_with_multi_anchor_token=0
```

`probe_bind.py` imports the shipped module and reports, per row, the number of distinct captures `bind_row` returns. **No row
at the tip names more than one capture**, so any rule that treats a multi-capture row strictly cannot red the tip; the whole
question is whether the strictness is right. Fixed copy, same tip:

```
$ python3 .ufo/waves/round-39/build/R39AnchorUnion/anchor_digest_check.py --lane .                 -> rows=109 tokens=17 defects=0  exit=0
$ python3 .ufo/waves/round-39/build/R39AnchorUnion/anchor_digest_check.py --lane . --evidence-ref index
                                                                                                  -> rows=109 tokens=17 defects=0  exit=0
$ diff tip_verbose_current.txt tip_verbose_fixed.txt                                  -> 1 changed line (below)
$ git -C "$S/lane" status --porcelain | wc -l                                          -> 0 after every fixture
```

The only verbose-output change on the tip is the one intended: the ABBREV line now also names the capture the prefix bound
to (`tip_verbose_current.txt` vs `tip_verbose_fixed.txt`):

```
22c22
< ABBREV S036 prefix=afaae9dd matches=afaae9ddaf4deda0095c2e7ad39c6cb63236d72c812ca2fcd9ab18c42eef8131
---
> ABBREV S036 prefix=afaae9dd matches=afaae9ddaf4deda0095c2e7ad39c6cb63236d72c812ca2fcd9ab18c42eef8131 capture=corpus/evidence/attrib-r23-stream.log
```

## 1. The hole, located in the shipped code

The shipped tool builds one digest→capture map per row by unioning the digests of **every** capture `bind_row` returns
(`plans/anchor_digest_check.py:392-399`), then accepts a token by membership in that map (`:486`):

```
392:    bound, unbound = {}, {}
399:                    digs.setdefault(dig, (path, how, label))
...
486:            elif tok not in row_scope:
```

`row_scope` is that union (`:449`). Consequence, exactly as `F38AnchorFix` §2 recorded: a row that names two captures
accepts *either* capture's digest, and no locator is preferred. `F38AnchorFix` measured this with fixture D
(`S111` keeps its configure-git-webserver URL and prose, gains a regex-log URL, and its anchor is replaced by S108's
digest of that other capture) and the shipped tool printed `defects=0`. I reproduced that here from scratch, §3.

## 2. The fix (what changed, and why this rule)

**Rule.** The row's locator set is treated as a set of claims of equal standing; every anchor token is bound to the capture
whose bytes (or whose `SHA256SUMS` entry) it is the digest of. When a row names **N>1** distinct captures it must carry an
anchor token for each of them, and a capture that none of the row's tokens resolves is a defect:

```
545:        # round 39: a token binds to a capture, not to the union of the row's captures. When the row
546:        # names more than one capture, every one of them must be resolved by one of the row's tokens.
547:        if per and not ex and len(per) > 1:
...
554:                    defects.append(f"DEFECT {sid} anchor token=- class=capture-unanchored "
555:                                   f"detail=row-names-{len(per)}-captures-{ntok}-anchor-token-"
556:                                   f"none-resolves-capture-{p} loc=corpus/SOURCES.md:{lineno}")
```

Supporting changes in the copy (all in `.ufo/waves/round-39/build/R39AnchorUnion/anchor_digest_check.py`):

| line(s) | change |
|---|---|
| `94-103` | docstring: the round-39 rule, its class, and its limits |
| `125-135` | docstring limits paragraph: the additive-URL variant is named as closed; presence and provenance-rewrite limits restated |
| `420-433` | `captures[sid]` = `{capture path: {how, {digest: label}}}` beside the existing union `bound[sid]` (kept for the erratum path and for `digest-wrong-capture` wording) |
| `440-448` | verbose `BIND+` line for the 2nd..Nth capture of a row (single-capture rows print exactly as before) |
| `502-519` | an abbreviation token now resolves to the captures its prefix matches, not only to "the union starts with it" |
| `538-543` | a full 64-hex token records which of the row's captures it binds to |
| `545-556` | the coverage leg: `capture-unanchored` per unclaimed capture, plus a verbose `CAPTURES` line |

Two properties keep it honest: a token that resolves to *several* of the row's captures is not a defect (those captures have
identical bytes, so the one digest is the true digest of each), and single-capture rows fall through to exactly the round-38
behaviour (`409+` rows with one capture: the union of one set is that set). The alternative repair `F38AnchorFix` also offered —
bind only to the capture the row's `source` cell names and report other URLs as unresolved — was rejected because it re-opens
the same class the moment the second URL is added to the *source* cell instead; the coverage rule is cell-independent, and
fixture F proves it (§5).

Diff against the shipped file: `diff-vs-plans.patch`, 80 changed lines in 8 hunks, `ast.parse` ok, 591 lines vs 534.

## 3. Red-before (shipped tool green) and red-after (copy red) on the union fixture

Fixture D, verbatim from the assignment and from `F38AnchorFix` §2: one extra pinned URL appended to **S111's scope cell**
(nothing else in the row's text touched) and the anchor's digest replaced by S108's — the real committed digest of the capture
that second URL names. Exact word-level deltas from `fixture_deltas.txt` (script `fixture_union.py`, pristine row is
`corpus/SOURCES.md:126`):

```
CASE D:
  insert: pristine='' -> mutant='https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py'
  replace: pristine='526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37' -> mutant='345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72'
```

Receipt `fixture_all.txt`, CASE D (the row was mutated in the working tree only; restore verified after the run):

```
$ python3 fixture_union.py --lane . --tool TIP=plans/anchor_digest_check.py --tool FIXED=<copy>   (case D block)
==== CASE D ====
TIP exit=0
TIP | rows=109 tokens=17 defects=0
FIXED exit=1
FIXED | DEFECT S111 anchor token=- class=capture-unanchored detail=row-names-2-captures-1-anchor-token-none-resolves-capture-corpus/evidence/round37/tb2-git-webserver/test_outputs.py loc=corpus/SOURCES.md:126
FIXED | rows=109 tokens=17 defects=1
RESTORED corpus/SOURCES.md sha256=cec138692f48961da41b93f0a9dbab203443716619badbe961aad5c4f5ad089e git status --porcelain lines=0
```

`--verbose` on the same fixture (`fixture_d_verbose.txt`, S111 lines and the surrounding bindings):

```
TIP | BIND S111 capture=corpus/evidence/round37/tb2-git-webserver/test_outputs.py by=url-task
TIP | RESOLVED S111 digest=345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72 via=corpus/evidence/round36/tb2-regex-log/test_outputs.py bind=url-task listed=corpus/evidence/round36/tb2-regex-log/test_outputs.py
TIP | rows=109 tokens=17 defects=0                      exit=0
FIXED | BIND S111 capture=corpus/evidence/round37/tb2-git-webserver/test_outputs.py by=url-task
FIXED | BIND+ S111 capture=corpus/evidence/round36/tb2-regex-log/test_outputs.py by=url-task
FIXED | RESOLVED S111 digest=345c3bd0… via=corpus/evidence/round36/tb2-regex-log/test_outputs.py bind=url-task …
FIXED | CAPTURES S111 n=2 claimed=corpus/evidence/round36/tb2-regex-log/test_outputs.py paths=corpus/evidence/round36/tb2-regex-log/test_outputs.py,corpus/evidence/round37/tb2-git-webserver/test_outputs.py
FIXED | DEFECT S111 anchor token=- class=capture-unanchored detail=row-names-2-captures-1-anchor-token-none-resolves-capture-corpus/evidence/round37/tb2-git-webserver/test_outputs.py loc=corpus/SOURCES.md:126
FIXED | rows=109 tokens=17 defects=1                     exit=1
```

Read the two lines together: the shipped tool *resolves* S111's token to the **other** capture
(`via=corpus/evidence/round36/tb2-regex-log/test_outputs.py`) and calls it green; the copy shows both captures it bound, the
one the token claims, and the row's own capture sitting unclaimed. The verbosity difference is the whole finding: "which
capture does this row's digest belong to" was never printed, so it was never asked.

## 4. Green at the lane tip — no false red

Run against the **real lane working tree** (read-only; the tool writes no file) and against the scratch clone, both at
`7504738`, `corpus/SOURCES.md` sha256 `cec1386…` (clean, `git status --porcelain -- corpus/SOURCES.md | wc -l` → 0):

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && date -u +%FT%TZ && git rev-parse HEAD
  2026-10-26T06:56:33Z
  750473847af9c7a461487ba3a589b5519fac5ed8
$ python3 plans/anchor_digest_check.py --lane .                     -> rows=109 tokens=17 defects=0  exit=0
$ python3 .ufo/waves/round-39/build/R39AnchorUnion/anchor_digest_check.py --lane .
                                                                    -> rows=109 tokens=17 defects=0  exit=0
$ python3 .ufo/waves/round-39/build/R39AnchorUnion/anchor_digest_check.py --lane . --verbose | tail -2
  RESOLVED S116 digest=16068505…  via=corpus/evidence/round38/tb2-build-pmars/instruction.md bind=url-task …
  rows=109 tokens=17 defects=0
```

Lane status at that moment: 4 untracked round-39 paths (`.ufo/waves/round-39/{build.ready,build/,integrate/}`,
`corpus/lessons/round-39.md`) — all pre-existing wave-1 state, none written by this seat.

## 5. Controls — regressions, false-red guards, and a mutant that proves the leg is load-bearing

Full receipt `fixture_all.txt` (all eight cases, both tools, restore checked after each). Summary:

| case | edit to the S111 row | shipped `TIP` | `FIXED` copy |
|---|---|---|---|
| CONTROL | none | `rows=109 tokens=17 defects=0` exit 0 | `rows=109 tokens=17 defects=0` exit 0 |
| D | +regex-log URL in scope cell, anchor ← its digest | **`defects=0` exit 0** (the red-before) | `defects=1` `capture-unanchored` exit 1 |
| F | same URL in the **anchor** cell, anchor ← its digest | `defects=0` exit 0 | `defects=1` `capture-unanchored` exit 1 |
| D2 | both locators, **one token each** (coherent multi-capture row) | `rows=109 tokens=18 defects=0` exit 0 | `rows=109 tokens=18 defects=0` exit 0 — no false red |
| DUP | both locators, both tokens are the row's own digest | `defects=0` exit 0 | `defects=1` `capture-unanchored` (regex-log unclaimed) exit 1 |
| A | anchor ← S108's digest, no second locator | `defects=1` `digest-wrong-capture` | identical |
| L | anchor token deleted | `tokens=16 defects=0` exit 0 | identical |
| M | A + `Erratum (round 37): S111 anchor sha256 <S108 digest>` in a working-tree lesson | `defects=2` (`erratum-incomplete` + `digest-wrong-capture`) | identical |

The parts of the receipt that carry the calibration:

```
==== CASE F ====
TIP exit=0
TIP | rows=109 tokens=17 defects=0
FIXED exit=1
FIXED | DEFECT S111 anchor token=- class=capture-unanchored detail=row-names-2-captures-1-anchor-token-none-resolves-capture-corpus/evidence/round37/tb2-git-webserver/test_outputs.py loc=corpus/SOURCES.md:126
FIXED | rows=109 tokens=17 defects=1
==== CASE D2 ====
TIP | rows=109 tokens=18 defects=0          FIXED | rows=109 tokens=18 defects=0        (both exit 0)
==== CASE DUP ====
TIP exit=0
TIP | rows=109 tokens=18 defects=0
FIXED exit=1
FIXED | DEFECT S111 anchor token=- class=capture-unanchored detail=row-names-2-captures-2-anchor-token-none-resolves-capture-corpus/evidence/round36/tb2-regex-log/test_outputs.py loc=corpus/SOURCES.md:126
FIXED | rows=109 tokens=18 defects=1
==== CASE A ====
TIP exit=1    TIP | DEFECT S111 anchor token=345c3bd0… class=digest-wrong-capture …   TIP | rows=109 tokens=17 defects=1
FIXED exit=1  FIXED | DEFECT S111 anchor token=345c3bd0… class=digest-wrong-capture … FIXED | rows=109 tokens=17 defects=1
==== CASE L ====
TIP | rows=109 tokens=16 defects=0          FIXED | rows=109 tokens=16 defects=0
==== CASE M ====
TIP | DEFECT S111 erratum token=- class=erratum-incomplete … / DEFECT S111 anchor … class=digest-wrong-capture … / rows=109 tokens=17 defects=2
FIXED | DEFECT S111 erratum token=- class=erratum-incomplete … / DEFECT S111 anchor … class=digest-wrong-capture … / rows=109 tokens=17 defects=2
```

D2 and DUP are the pair that matters: D2 has the same two locators as D/DUP and stays green because it really does carry a
digest for each capture, while DUP carries two copies of one capture's digest and reds for the other. The rule is "one token
per capture", not "multi-locator rows are suspicious".

**Mutant R39-M1 (coverage leg disabled)** — proves the new `defects=1` is caused by this change and nothing else. One-line
mutant of the copy (`sed 's/if per and not ex and len(per) > 1:/if False:/'`, line 547):

```
$ python3 mutant_m1.py --lane .                              -> rows=109 tokens=17 defects=0   exit=0   (tip unchanged)
$ python3 fixture_union.py --lane . --tool M1=mutant_m1.py --tool FIXED=<copy> --cases CONTROL,D
==== CASE CONTROL ====
M1 exit=0     M1 | rows=109 tokens=17 defects=0             FIXED exit=0  FIXED | rows=109 tokens=17 defects=0
==== CASE D ====
M1 exit=0     M1 | rows=109 tokens=17 defects=0             FIXED exit=1  FIXED | DEFECT S111 … class=capture-unanchored … FIXED | rows=109 tokens=17 defects=1
```

So the red on D is attributable to the coverage leg alone (`mutant_m1.txt`).

## 6. Adjacent observation (not part of R5a, both tools): a URL glued to `;` is not bound

When the extra URL is written with no separating space before a semicolon, `URL_RAW`'s subpath group
`([^\s|`)\]]+)` (`plans/anchor_digest_check.py:126-127`) swallows the `;`, so the basename becomes `test_outputs.py;`, no
capture matches, and that locator silently binds nothing (`quirk_glue.txt`):

```
==== CASE GLUE ====      (the D/F edit with "url;" instead of "url ;")
TIP exit=1
TIP | DEFECT S111 anchor token=345c3bd0… class=digest-wrong-capture …   TIP | rows=109 tokens=17 defects=1
FIXED exit=1
FIXED | DEFECT S111 anchor token=345c3bd0… class=digest-wrong-capture … FIXED | rows=109 tokens=17 defects=1
```

Both tools lose the second capture and judge the token against the single remaining one. The direction is false-red (the tool
gets stricter, not looser: the capture count is under-counted, never over-counted), so it does not reopen the union hole — but
it is the same "which capture did that URL name" question, and a future row that writes its *only* locator that way would be
`anchor-unbound`. My fixture F therefore writes `url ;`. I did not change the scanner: the fix belongs with whoever next
touches `URL_RAW`, and it is not on R5a's path.

## 7. Limits of the fix, stated as limits

- **Presence is unchanged.** A row with no anchor token claims nothing and raises nothing; 92 of 109 rows carry none at
  `7504738` (`tokens=17`, `L` fixture). `defects=0` certifies the tokens present. The coverage leg only applies to a row that
  carries at least one token (a multi-locator row with no claim stays green).
- **Provenance rewrite is unchanged.** A row that rewrites locator set *and* tokens consistently is still green — the row is
  the only witness, as the shipped docstring already said.
- **Policy consequence to price before integration.** A future row that *mentions* a second capture (prose, URL, provenance
  line) and carries a digest only for its subject becomes `capture-unanchored`. That is the intended strictness — the row is
  claiming two subjects — but it is a new authoring rule, and it is why this is a routed copy rather than an edit: the L1
  should land it together with a one-line note in `corpus/QUALITY.md`'s Q26 limits (which `F38AnchorFix` §3b shows still
  advertises the round-37 hole) so writers know the rule exists. No row at the tip is affected (0 multi-capture rows).
- **Erratum path unchanged.** A valid `Erratum (round 37)` exemption still bypasses every anchor class including coverage, so a
  two-capture row under a valid erratum need not anchor both. Fixture M shows the exemption refusing to launder (2 defects,
  same lines, same classes).

## 8. Operability and no-harm

- Invocation, exit codes and stdout contract are the shipped tool's: `python3 <copy> [--lane DIR] [--evidence-ref head|index]
  [--verbose]`, exit 0/1/2, final line `rows=… tokens=… defects=…`. Stdlib only; writes no file (it only reads git objects).
- New output is additive: one new class name (`capture-unanchored`) whose `detail` names the capture and the token count, one
  verbose line (`BIND+`) for extra captures, one verbose line (`CAPTURES`) showing claimed vs named captures, and the ABBREV
  line's `capture=` suffix.
- Writes by this seat: `.ufo/waves/round-39/build/R39AnchorUnion/` (copy, driver, receipts) and
  `.ufo/waves/round-39/build/R39AnchorUnion.md`; plus scratch `/fast/scratch/hyaku/kengaku-r39/R39AnchorUnion/` (clone,
  mutant, receipts) deleted before this report was filed. No lane file, index or jj state touched: every fixture mutated only
  the scratch clone's working tree and every case ends with `RESTORED … sha256=cec1386… git status --porcelain lines=0`.
  `plans/anchor_digest_check.py` is byte-unchanged (`98847e89…`).
- Tooling: nothing installed, nothing upgraded; `python3` (stdlib) and `git` only. `pacman` was not run.
- Unverified by me, named: `--evidence-ref index` was exercised only on a clean clone (identical to HEAD by construction), not
  on a tree with staged-only captures; a row whose `PROVENANCE.md` line names two captures was not fixtured (none exists).

Receipts in `.ufo/waves/round-39/build/R39AnchorUnion/`: `anchor_digest_check.py` (the copy, sha256 `11bb2cad…`),
`diff-vs-plans.patch`, `fixture_union.py` (driver, sha256 `5ae644da…`), `probe_bind.py`, `fixture_all.txt`, `fixture_deltas.txt`,
`fixture_d_verbose.txt`, `mutant_m1.txt`, `quirk_glue.txt`, `tip_verbose_current.txt`, `tip_verbose_fixed.txt`.

VERDICT: anchor-union-red-before-yes-tip-defects-0
