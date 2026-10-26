# F38AnchorFix — D3 anchor binding, falsified where it can be

Seat: F38AnchorFix (executor, wave 2 / FALSIFY). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Tip under attack: `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`. Object of attack: the round-38 D3 fix
`plans/anchor_digest_check.py` (rewritten by `R38AnchorBind`), its tip claim, and the round-37 tool it
replaced (`git show e0a37853:plans/anchor_digest_check.py`).

Receipts in `.ufo/waves/round-38/falsify/F38AnchorFix/` (each file is the raw, unfiltered run):

| receipt | content |
|---|---|
| `canonical.txt` | clone identity, both tool digests, tip and round-37 output on the pristine tip |
| `tip_verbose.txt` | tip `--verbose`: 19 `BIND` lines, 17 anchor tokens resolved, `defects=0` |
| `fixture_run.txt` | CONTROL, A, B, C, D × (tip, round-37) |
| `fixture_d.txt` | fixture D held open: tip `--verbose`, binding probe, round-37 |
| `fixture_extra.txt` | E, F, G, H, I × (tip, round-37) |
| `fixture_tail.txt` | J, K × (tip, round-37) |
| `fixture_l.txt` | anchor-token-removal probe |
| `fixture_m.txt` | erratum-laundering probe with the label the tool reads |
| `probe_pristine.txt` | rows with >1 pinned URL / >1 bound capture on the pristine tip: `0` |
| `probe_slugs.txt` | task-slug and anchor-token census: 4 slugs, 0 duplicates, 109 rows, 17 tokens on 17 rows |
| `probe_sums.txt` | accepted manifest view vs committed bytes: 31 captures, 0 disagreement |
| `q26_tree3ea.txt`, `q26_tree3ea_run.txt` | Q26 "shown able to fail" reproduction on a tree at `3ea9a1d9` |
| `cross_row_fixture.py`, `fixture_d_verbose.py`, `fixture_extra.py`, `fixture_tail.py`, `probe_bind.py`, `probe_sums.py` | the fixture drivers (re-run as `python3 <script> --lane <clone> --tip plans/anchor_digest_check.py --old <old copy>`) |

## 0. Setup — clone, digests, tip green

```
$ S=/fast/scratch/hyaku/kengaku-r38/F38AnchorFix; git clone -q --no-local <lane> "$S/lane" && \
  git -C "$S/lane" checkout -q 8c7422d7a646515d80af44844e8ecc8a1fc1d30a
$ git -C "$S/lane" rev-parse --show-toplevel        -> /fast/scratch/hyaku/kengaku-r38/F38AnchorFix/lane
$ git -C "$S/lane" rev-parse HEAD                    -> 8c7422d7a646515d80af44844e8ecc8a1fc1d30a
$ sha256sum plans/anchor_digest_check.py             -> 98847e8930304a23ab3e10dd27cfc3501738467b8871d8b725d24908e6c1f0b2
$ git show e0a37853:plans/anchor_digest_check.py | sha256sum
                                                     -> 6d7afcd56a95c59f835be04a16263d43db4840cc8a4b111350be4d7cb8d9a323
$ python3 plans/anchor_digest_check.py --lane .      -> rows=109 tokens=17 defects=0      exit=0
$ python3 <e0a37853 copy> --lane .                   -> rows=109 tokens=17 defects=0      exit=0
```

Both counters are green on the pristine tip — the round-37 tool's green here is expected (round 37 is
membership-only, and every tip token *is* some committed evidence digest). Note `3ea9a1d9` does not
contain the file at all: `git ls-tree 3ea9a1d9 -- plans/anchor_digest_check.py` is empty; the file first
lands in `c138da2` (`q26_tree3ea.txt`).

All fixtures below mutate **only the working tree** of the scratch clone (`corpus/SOURCES.md`, plus, for
M, a working-tree lesson line). The tip reads rows from the working tree and evidence from `HEAD`, so no
commit is needed and no git state was touched. After every fixture the pristine bytes are restored and
`git -C "$S/lane" diff --name-only` is empty (`canonical.txt`, `fixture_m.txt`).

## 1. The assigned falsification — cross-row substitution: CAUGHT at the tip, MISSED by round 37

Fixture shape, verbatim from the assignment: *a row whose anchor carries another row's real committed
digest*, nothing else edited. The digest used is S108's, independently recomputed from the committed blob
(`RESOLVED S108 digest=345c3bd0…` in `tip_verbose.txt`; the same 64 hex appears in S108's own anchor).

**A — S111 keeps its configure-git-webserver URL and prose, its anchor is replaced by S108's digest:**

```
TIP exit=1
TIP | DEFECT S111 anchor token=345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72 \
      class=digest-wrong-capture detail=committed-capture-belonging-to-another-capture-\
      corpus/evidence/round36/tb2-regex-log/test_outputs.py-not-the-capture-this-row-names-\
      corpus/evidence/round37/tb2-git-webserver/test_outputs.py loc=corpus/SOURCES.md:126
TIP | rows=109 tokens=17 defects=1
OLD exit=0
OLD | rows=109 tokens=17 defects=0
```

The round-37 tool prints `defects=0`, exit 0 — the `F37A-1` hole (`.ufo/waves/round-37/falsify/F37AnchorRerun.md`
§4, mutants M4b/M5) reproduces exactly on the tip tree. Mechanism in the old copy: one global set,
`allowed = set(files) | set(manifests)` (`e0a37853:plans/anchor_digest_check.py:200`) tested at `:268`
(`elif tok not in allowed`); it has no `bind_row`, no `row_scope`, no `digest-wrong-capture` class
(`grep` over the old copy finds none of the three).

The same one-line substitution is caught at the tip on every binding route, and missed by the old tool on
every one (`fixture_run.txt`, `fixture_extra.txt`, `fixture_tail.txt`):

| # | row ← digest | the row binds by | tip | round-37 |
|---|---|---|---|---|
| A | S111 ← S108 (`345c…`) | `url-task` (round37/tb2-git-webserver) | exit 1, `digest-wrong-capture` | exit 0, `defects=0` |
| B | S115 ← S108 (round-38 row) | `url-task` (round38/tb2-build-pmars) | exit 1, `digest-wrong-capture` | exit 0 |
| C | S113 ← S111 (`526a…`), same task dir, other file | `url-task` | exit 1, `digest-wrong-capture` | exit 0 |
| G | S070 ← S105 (`44a0…`) | `provenance-row` | exit 1, `digest-wrong-capture` | exit 0 |
| J | S036 ← S105 | `row-path` | exit 1, `digest-wrong-capture` | exit 0 |
| K | S001 ← S108 (row binds nothing) | none | exit 1, `anchor-unbound detail=row-carries-no-capture-locator` | exit 0 |
| E | S111 ← S108's 8-hex prefix + `…` | `url-task` | exit 1, `abbrev-unresolved detail=no-digest-of-the-capture-this-row-names-starts-with-this-prefix` | exit 0 |
| H | S111 ← S108 uppercase | `url-task` | exit 1, `digest-uppercase` | exit 1, `digest-uppercase` |

K is the sharpest statement of the old hole: a row with no locator at all accepts any committed evidence
digest (`defects=0`), because the old tool never asks what the row is about. At the tip, a row that binds
nothing cannot carry a digest claim at all.

Erratum laundering is refused as documented (`fixture_m.txt`, anchor = S108's digest + an
`Erratum (round 37): S111 anchor sha256 …` line citing it as both wrong and correction):

```
ERRATUM S111 loc=corpus/lessons/round-38.md:79 cited_wrong=['345c…','345c…'] correction=[]
DEFECT S111 erratum token=- class=erratum-incomplete detail=no-64-hex-digest-of-the-capture-this-row-names
DEFECT S111 anchor token=345c… class=digest-wrong-capture …
rows=109 tokens=17 defects=2      exit=1
```

So the exemption inherits row scoping, as the docstring says. Fixture I (`fixture_extra.txt`) shows the
same erratum line labelled `Erratum (round 38):` producing only the anchor defect — `ERRATUM` is
`^ {0,3}Erratum \(round 37\): …` (`plans/anchor_digest_check.py:120`), so a future round's anchor erratum
is invisible to the tool unless it is written with the literal round-37 label that `corpus/QUALITY.md:386`
prescribes. Spec-consistent, but an operability trap for the next seat that needs one.

## 2. Finding F1 (residual, medium) — the binding is a union over locators, so a row that names two captures accepts either digest

The tip claim is `plans/anchor_digest_check.py:10` — "binds each token to the capture **the row itself
names**" — restated as **Closed** at `corpus/lessons/round-38.md:52`. `bind_row` returns *every* capture
the row's text resolves (one entry per matching pinned URL), and `check` unions their digests into
`row_scope`; the token is then accepted if it is in that union. Nothing prefers the capture the row's
`source` cell and prose are about. Consequence: append one extra pinned URL for another task and the
row's anchor may carry that other row's real digest, with the row's original URL and stated subject
untouched.

Fixture D (scope cell gains a regex-log URL; anchor ← S108's digest), held open in `fixture_d.txt`:

```
MUTATION S111 anchor '…; sha256 526aee3d…' -> '…; sha256 345c3bd0…' + second URL in scope cell
$ python3 plans/anchor_digest_check.py --lane . --verbose   exit=0
| BIND S111 capture=corpus/evidence/round37/tb2-git-webserver/test_outputs.py by=url-task
| RESOLVED S111 digest=345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72 \
           via=corpus/evidence/round36/tb2-regex-log/test_outputs.py bind=url-task listed=…
| rows=109 tokens=17 defects=0
$ probe_bind.py -> ROW S111 urls=2 caps=2 digests=2 anchor_tokens=1
$ python3 <e0a37853 copy> --lane .                          exit=0  rows=109 tokens=17 defects=0
```

Fixture F puts the extra URL in the **anchor cell** instead (`fixture_extra.txt`) and gets the same
`defects=0`, exit 0 — the bypass is not an artifact of which cell holds the URL.

What this does and does not falsify:

- It does not falsify the assignment's shape: A (and B/C/G/J/K/E) is one edit, the anchor only, and the
  tip catches all of them while the round-37 tool catches none.
- It does falsify the unqualified **Closed** wording at `corpus/lessons/round-38.md:52` and the sentence
  "What this copy closes is substitution that leaves the row's locator alone"
  (`plans/anchor_digest_check.py:106`). Fixture D leaves the row's locator — the URL and prose of the row's
  subject — alone, and substitutes another row's digest. The docstring's own limit paragraph (`:103-106`)
  names *rewriting* the locator ("points its URL at another task, or adds a provenance table line naming
  another capture") and therefore almost covers D; the additive second-URL variant is the same class but is
  not what the sentence says, and the lesson row drops the qualifier entirely.
- Both tools pass D, so D is not a regression introduced by D3 — it is the same class of hole that the
  round-37 report called out, surviving in a narrower form. The tip state itself is clean:
  `probe_pristine.txt` → `rows=109 rows_with_multi_url_or_multi_capture=0`, i.e. no real row has two
  locators today, so nothing in the lane is currently wrong.
- Cost of the bypass for a future author: one appended URL, no subject rewrite. Cost at round 37: one
  digest substitution, no URL edit at all. The fix raises the cost; it does not close the class.

Repair the next round should price (not applied — this seat writes reports only): treat a row's locator
set as *claims* of equal standing and require the row to carry one anchor token per distinct capture it
names (or bind the anchor to the capture the row's `source` cell names and report extra pinned URLs as
unresolved locators). Either change makes D a defect while keeping the pristine tip green.

## 3. Finding F2 (limit, low) — removing a digest claim silences the check

`defects=0` certifies that *present* claims resolve; it does not certify that an admitted row carries one.
Fixture L deletes S111's token and leaves everything else intact (`fixture_l.txt`):

```
BEFORE: commit 2fd12b8…, tests/test_outputs.py:9-13, :13 "assert "TEST PASSED" in result.stdout" …sha256 526aee3d…
AFTER : commit 2fd12b8…, tests/test_outputs.py:9-13 (no digest claim)
rows=109 tokens=16 defects=0      tip exit=0
RESTORED -> rows=109 tokens=17 defects=0
```

17 of 109 census rows carry an anchor token; the checker says nothing about the other 92, and nothing
about a row that sheds a token. Combined with `token-outside-anchor` (a token moved to the teaches cell is
a defect) this is coherent — the tool is a verifier of claims, not of their presence — but any statement
of the form "the registry's anchor digests are verified" must be read as "the 17 present ones are".

## 3b. Finding F3 (documentation calibration, low) — the criterion that governs the tool still advertises the hole the tool closed

`corpus/QUALITY.md:400-402` (Q26, unamended in round 38 — the round-38 section adds Q28 and Q29 only,
`grep -n "Round38 criterion" corpus/QUALITY.md` → `:453`, `:499`):

> "Limits: membership, not binding — a 64-hex token that is the digest of the wrong committed file passes, …
> the pin-to-capture binding stays with the counters that run the probe (`plans/pkg_gate.py` P5,
> `plans/round37_c2_verify.py` V3)"

That sentence is false at the tip: a 64-hex token that is the digest of the wrong committed file *fails* —
fixtures A/B/C/G/J are exactly that shape and the tip prints `digest-wrong-capture`, exit 1, where the old
tool printed `defects=0`. A reader who follows Q26 to decide whether a row-level digest check suffices is
told the opposite of what the shipped check now does, and the sentence names two other counters as the only
place the binding lives. This is the mirror of F1: the tool under-claims nowhere in its own docstring and
over-claims in one clause, while the criterion over-claims the hole and under-claims the tool. The next
round that prices D3 should amend Q26's Limits paragraph (append-only, per Q6) to state the binding, its
single-locator qualifier, and the two accepted views of a capture (F1's bypass belongs there too).

## 4. Adjacent calibration checks (attacks on the surrounding receipts, all reproduce)

- **Q26's "shown able to fail" numbers.** `corpus/QUALITY.md:393` says "on the lane at `3ea9a1d9` it prints
  `rows=103 tokens=11 defects=5`". The file does not exist at `3ea9a1d9` (first landed `c138da2`), so the
  claim's provenance is anachronistic; the numbers are right for the *tree* at `3ea9a1d9`
  (`q26_tree3ea_run.txt`, both tools): `rows=103 tokens=11 defects=5`, exit 1. Classes differ by tool —
  the tip says `anchor-unbound` for S070/S072/S073/S074 where the recorded run says `digest-unknown`, and
  both agree on S110 `digest-short detail=63-hex`. Any future re-quote of that line should name the tree,
  not the commit's own contents.
- **The two accepted views of a capture.** `capture_digests` accepts the committed file's sha256 *and* the
  `SHA256SUMS` entry for the same name. `probe_sums.txt`: `captures_listed_in_a_manifest=31 disagree=0
  manifest_entries=31 manifest_digests=30` — consistent today, so the union hides nothing now, but a stale
  manifest entry would make a wrong anchor green. Round 37 verified the same equality by hand; the tool
  does not enforce it.
- **Ambiguous task slugs.** `bind_row` refuses when two evidence dirs claim one `task.toml` slug, which
  would surface as `anchor-unbound`. Today `evidence_dirs_with_task_toml=4 task_slugs=4 duplicate_slugs=0`
  (`probe_slugs.txt`), so no row can hit it — noted because the refusal path is untested by any current
  fixture.

## 5. What I did not test (my own limits)

- No commit was made, in the lane or in the clone, so everything here exercises the working-tree-rows +
  `HEAD`-evidence path only. `--evidence-ref index` was not exercised.
- The bypass in F1 is demonstrated by construction; I did not look for a fixture that reaches it without
  editing the row at all (the pristine probe says none exists today).
- Byte-identical captures (two paths, one digest) and a conflicting manifest are reasoned about from the
  source, not fixtured.
- I did not re-run the whole round-38 gate battery; C1/C2 are other seats' objects.

## 6. Operability and no-harm

- Lane files untouched: every write went to the scratch clone or to
  `.ufo/waves/round-38/falsify/F38AnchorFix/`; final `git -C "$S/lane" diff --name-only` is empty and the
  pristine `corpus/SOURCES.md` (sha256 `cec138692f48961da41b93f0a9dbab203443716619badbe961aad5c4f5ad089e`)
  and `corpus/lessons/round-38.md` are byte-restored.
- Tooling: nothing installed or upgraded; `pacman` is paused host-wide and the task needed only `python3`
  (stdlib) and `git`.
- Scratch `/fast/scratch/hyaku/kengaku-r38/F38AnchorFix` (clone, `3ea9a1d9` tree, old-tool materialization,
  run logs) is deleted after the receipts above were copied out.
- Risk to the parent: the D3 milestone is real for single-locator rows and demonstrably red where the
  round-37 tool was green (A/B/C/G/J/K/E). The lesson/`STATUS` wording should gain "single-locator rows"
  before D3 is called closed, and the additive-URL case should be named in the docstring's limit paragraph
  rather than left to the reader.

VERDICT: anchor-cross-row-caught
