# F38CritTags — the frozen `violates=` tags, adjudicated against `instruction.md`

Round 38, wave 2 (falsify). Attacked: `corpus/evidence/round38/build-pmars-dry-cases-freeze.txt`
(sha256 `93b4b60c…f4df0`, the V5 pin) and, through it, the C2 map in
`corpus/knowledge/tb2-build-pmars-grader.md` §Requirement map. Lane tip `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`.
Work done in `git clone --no-local` under `/fast/scratch/hyaku/kengaku-r38/F38CritTags/lane`
(`git -C … rev-parse --show-toplevel` = that path; `HEAD` = the tip); scratch deleted at the end. **No lane file,
tag, probe, counter or map row was edited.** The frozen tags stay; this is a limit report plus a priced alternative.

Every number below comes from a receipt in this directory:

| receipt | produced by |
|---|---|
| `tag-contest.txt` | `python3 tag_contest.py --lane <clone>` (reuses the counter's own `derive`/`MAP_ROW` and the frozen probe's `CASES`) |
| `adjudication.json` | the per-pair verdicts the script itself cross-checks against its computed edits (`ADJUDICATION_EDITS_MATCH_ALT=True`, `tag-contest.txt:47`) |
| `cases.json` | the frozen probe module's 22 `Case` objects (staged `/app` trees, artefacts, texts) |
| `v7-probes.txt` | `plans/round38_c2_verify.py::v7` run against a scratch copy of the entry/dry table |
| `dlopen.strace`, `dlopen.stdout` | `strace -f -e trace=openat` on the probe's own `dlopen-x11` artefact |
| `probe-dry.stdout/.stderr` | `plans/build_pmars_probe.py --dry`; `diff` against the frozen table is empty (`DRY_BYTE_EQUAL=yes`) |

Frozen inputs verified before any interpretation: dry table `93b4b60c…`, probe `32f0771c…`,
`sha256sum -c corpus/evidence/round38/tb2-build-pmars/SHA256SUMS` → five `OK`, and the counter's own
`V7 ok rows=7 tags=7 bad=0` on the clone.

## 1. Shape of the frozen table (what the labels can and cannot say)

`tag-contest.txt:18` — `charged_pairs=100 of 154 case-tag slots`; `tag-contest.txt:6-12` — with the counter's own
`derive()` rule every one of the seven rows derives `partly`, and the entry says `partly` for all seven.

The load-bearing structural fact this seat adds: **four tags carry the identical 22-case carrier set**.

```
tag-contest.txt:15  DEGENERATE identical_set_and_label label=partly n=22
                    tags=['debian-source', 'debugger-works', 'extract-to-app', 'from-source']
tag-contest.txt:16  distinct_carrier_sets=4 of 7 tags
```

So the map has 7 rows but 4 distinguishable rows. `from-source`, `debian-source`, `extract-to-app` and
`debugger-works` are charged to *every* case, including all 7 passing ones; their labels are algebraically the same
number. The entry's headline (`tb2-build-pmars-grader.md:151`) — "no line of the instruction is fully enforced" — is
therefore entailed by the tagging, not independent evidence: any tag charged to all 22 cases is `partly` by
construction, because 7 of the 22 pass.

The null case is not load-bearing for any label (`tag-contest.txt:17`, `NULLCASE empty-tree dropped:
labels_moved=0 none`), so the "all partly" result rests entirely on the 21 substantive cases. Removing
`empty-tree` from an over-broad tag does not help a row; the over-charge is not a null-case artefact.

## 2. Clause reading — what each tag names

| tag | line | the clause it names (quoted) | verdict on the line |
|---|---|---|---|
| `from-source` | 1 | "Build pMARS (http://www.koth.org/pmars/) from source with no X server." | fine |
| `no-x11` | 3 | "Extract the source to `/app` and build without X11 support." | fine (L1 "no X server" and L9 "no X11 dependencies" are equally available; the line cell is pinned by V7 but moves no label) |
| `debian-source` | 3 | "get the source from Debian packages instead" | fine |
| `extract-to-app` | 3 | "Extract the source to `/app`" | **contest: destination vs identity** |
| `install-path` | 3 | "Install the binary to `/usr/local/bin/pmars`." | fine for the path, over-charged once (silent-binary), under-charged once (canned-script) |
| `results-format` | 7 | "This should output "Results: X Y Z" where X, Y, Z are integers." | **contest: prefix vs full line; "integer" includes negatives** |
| `debugger-works` | 9 | "… and that the debugger works properly." | fine (a transcript is not a debugger) |

The probe's own comment for `extract-to-app` reads `# extract the source to /app`
(`plans/build_pmars_probe.py:70`), i.e. it is named for a **destination**; the frozen table charges it, on 20 cases,
for the **identity** of the tree — the same defect `debian-source` and `from-source` already charge. That is the
whole of the contest that moves labels.

## 3. Per-case adjudication

Of the 100 charged pairs: **77 defensible as filed, 23 over-charges, 1 under-charge**; 6 further contests were
examined and the tag **upheld** (`tag-contest.txt:80`, `contested_deletions=23 contested_additions=1
upheld_contests=6 weak=0`). Full matrix (`tag-contest.txt:78-100`; `C`=charged-but-contested, `+`=contested add,
`d`=charged and defensible, `.`=not charged):

```
CASE                 obs   from no-x debi extr inst resu debu
empty-tree           fail  d    d    d    d    d    d    d
canned-shape         pass  d    .    d    C    .    .    d
canned-script        fail  d    .    d    C    +    .    d
canned-static        fail  d    .    d    C    .    .    d
canned-x11-linked    fail  d    d    d    C    .    .    d
canned-x11-dlopen    pass  d    d    d    C    .    .    d
results-two-ints     fail  d    .    d    C    .    d    d
results-trailing-text pass d    .    d    C    .    C    d
results-not-last     fail  d    .    d    C    .    d    d
results-negative     fail  d    .    d    C    .    C    d
one-address          fail  d    .    d    C    .    .    d
four-digit-address   fail  d    .    d    C    .    .    d
canned-exit-nonzero  pass  d    .    d    C    .    .    d
nonexec-binary       fail  d    .    d    C    d    .    d
silent-binary        fail  d    .    d    C    C    .    d
path-split           pass  d    .    d    C    d    .    d
no-debian-dir        fail  d    .    d    C    .    .    d
debian-is-file       pass  d    .    d    C    .    .    d
src-no-c             fail  d    .    d    C    .    .    d
c-is-dir             pass  d    .    d    C    .    .    d
no-src-dir           fail  d    .    d    C    .    .    d
pmars-dir-elsewhere  fail  d    .    d    d    .    .    d
```

The 20 `C` cells in the `extr` column are the over-charge argued below; the two `d` cells there (`empty-tree`,
`pmars-dir-elsewhere`) are the destination violations this seat keeps. Every `d` in the other columns is a charge
re-read against its clause and kept (the 6 hardest are re-argued in §6).

**`extract-to-app` on 20 cases** (`tag-contest.txt:33`) — over-charge, and this is executed evidence, not a reading.
Both shape tests assert the same one-level glob (`test_outputs.py:62`, `:75`: `source_dirs = list(Path("/app").glob("pmars-*"))`;
`:63`, `:76` `assert source_dirs`), so a `P` in test position 3 or 4 is a receipt-backed witness that a tree exists at
`/app/pmars-*`. All 20 cases this seat drops the tag from show such a `P`
(`tag-contest.txt:20`, `destination_satisfied=20/20`), and the two cases it keeps — `empty-tree:FFFF`,
`pmars-dir-elsewhere:PPFF` — are exactly the two where both shape tests fail (`tag-contest.txt:21`). The instruction's
destination clause held in those 20 states; what failed there is the source's identity (`debian-source`) or the build
(`from-source`). The entry itself reads the tag this way in Finding 7 (`tb2-build-pmars-grader.md:261`: "the one place
the map's `extract-to-app` label is enforced in the failing direction"), so the map row's `canned-shape` citation
contradicts the entry's own finding.

**`results-format` on two cases** (`tag-contest.txt:35`) — `results-trailing-text` and `results-negative`. L7 states a
three-integer prefix, and `-1` is an integer. `Results: 12 34 78 forged` still carries X, Y, Z as integers; the
grader's `re.match` accepting it is the behaviour the instruction's own test command (`instruction.md:5`, ending
`| tail -n 1`) invites, so the case is a **lenience control**, not a violated requirement. `results-negative` is the
mirror: `\d+` rejecting a sign is grader **strictness**, not a fact about three integers. Note the load-bearing pair
here is `results-trailing-text`, not `results-negative`: the entry's wave-1 contest
(`tb2-build-pmars-grader.md:189-190`) names the latter as contestable and says "No label moves without them", which
is true for the neighbour but misses that dropping the former moves the row.

**`install-path`** — one over-charge, one under-charge (`tag-contest.txt:34`): `silent-binary` has an executable
compiled file at the instruction's path (its silence is a `from-source`/`results-format`/`debugger-works` defect),
while `canned-script`'s `/usr/bin/bash` script at that path is not "the binary" at all. Both are label-neutral.

## 4. Strongest alternative, and the recomputed labels

Alternative rule this seat argues for (script: ALT-LOCATION + ALT-LITERAL + destination-only `install-path`):

1. `extract-to-app` = the L3 destination clause only (`# extract the source to /app`, `build_pmars_probe.py:70`):
   violated iff no `/app/pmars-*` tree exists.
2. `results-format` = L7 read literally: violated iff the piped command's last line does not carry three integers
   (`-?\d+`); trailing words after the third integer do not violate a prefix requirement.
3. `install-path` = the destination clause ("Install **the binary** at that path"): `silent-binary` keeps the file at
   the path (drop), `canned-script` installs a script (add).

Recomputed with the counter's own `derive()` (`tag-contest.txt:24-30`):

| row | frozen | alternative | carriers under the alternative |
|---|---|---|---|
| `extract-to-app` | partly | **enforced** | `empty-tree` fail, `pmars-dir-elsewhere` fail |
| `results-format` | partly | **enforced** | `empty-tree` fail, `results-two-ints` fail, `results-not-last` fail |
| other five | partly | partly (unchanged) | — |

`tag-contest.txt:37` — `ALT labels_change=2 rows=['extract-to-app', 'results-format']`.

Three consequences, all checkable:

- **Rows that change:** `instruction.md:3 | extract-to-app` → `enforced`; `instruction.md:7 | results-format` →
  `enforced`. Under the alternative the entry's map-level sentence at `tb2-build-pmars-grader.md:151` is false for two
  of seven lines: the one-level `/app/pmars-*` glob and the three-integer prefix *are* fully enforced on the frozen
  table.
- **Citations that break** (`tag-contest.txt:38`): `extract-to-app` cites `canned-shape`, `install-path` cites
  `silent-binary`, `results-format` cites `results-trailing-text` — all three stop being violating cases, so V7's
  citation rule (`cited ⊆ violating`) would reject the rows as filed.
- **Both `enforced` rows lose their pass carrier by construction** (no violating case passes any more), so the map's
  "violating, both directions" citation style cannot be kept for them: the alternative is expressible only with
  fail-only citations. That is the price of the alternative and the reason it remains a limit, not an edit.

## 5. Why the counter cannot see any of this — the calibration defect

`V7`'s label rule is self-referential: it derives the label from the frozen `violates=` sets, so any tag table yields
a green map. Probed on a scratch copy (`v7-probes.txt`):

```
P0 frozen tags, frozen labels: (True, 'rows=7 tags=7 bad=0')
P1 entry relabelled to the ALT labels, tags untouched: (False, "… bad=['extract-to-app: labelled enforced,
   receipt derives partly', 'results-format: labelled enforced, receipt derives partly']")
P2 one frozen tag dropped in the dry table: raised ValueError: dry table not at its freeze digest
```

P1 shows the labels are a function of the tags, not of the receipt's evidence; P2 shows the counter is **pinned to
the frozen tags and cannot price an alternative at all** (`dry()` refuses a perturbed table). Tag quality is therefore
outside V7's reach by design: `checks=7 defects=0` certifies internal consistency and says nothing about whether a
charge is defensible. That is the calibration gap this seat exists to name.

**Smallest safe correction (no edit to tags, probe, counter or labels):** in `tb2-build-pmars-grader.md` §Requirement
map, state beside the table that (a) four of the seven rows share one 22-case carrier set and are not independently
informative; (b) the labels are derived from the frozen tags and the frozen tags are pinned in the counter, so the
"no line fully enforced" sentence is a tagging statement, not an execution result; (c) under the destination reading
of `extract-to-app` (the reading Finding 7 uses) and the literal L7 reading, those two rows derive `enforced`, and the
cases that would then stop being violations are `canned-shape`‑class, `results-trailing-text` and `results-negative`
(lenience/strictness controls). One paragraph, no relabel, no counter change.

## 6. Contests examined and upheld (with receipts)

- **`canned-x11-dlopen` → `no-x11` (upheld).** The wave-1 objection (`tb2-build-pmars-grader.md:183-186`) is that the
  rig "calls no X11 symbol". True and irrelevant to L9's "no X11 dependencies": the process opens the library.
  `strace -f -e trace=openat ./pmars -b` (artefact built by the probe's own `build_art` with `link="dlopen-x11"`)
  gives `openat(AT_FDCWD, "/usr/lib/libX11.so.6", O_RDONLY|O_CLOEXEC) = 3` (`dlopen.strace`, one hit). A run-time load
  of `libX11.so.6` is an X11 dependency; the tag stands. Priced anyway: dropping it makes `no-x11` `enforced`
  (`tag-contest.txt:42-43`, labels change 3) — so the row *is* one tag away from flipping, which is worth saying, but
  the flip is not text-justified.
- **`debugger-works` charged to the canned cases (upheld).** A canned program printing two literal address lines is not
  a debugger that "works properly" (`instruction.md:9`). The behaviour-only alternative (keep the tag only where the
  debug text is defective) derives `enforced` from `{empty-tree, one-address, four-digit-address}`
  (`tag-contest.txt:44-45`, labels change 3) and is rejected: it would let a transcript claim a property of the build,
  and the entry's Finding 1 depends on the identity charge.
- **`path-split` → `install-path` (upheld).** The artefact answering the instruction's own command is at
  `/usr/local/sbin/pmars`; the named path holds a silent file. The binary the instruction names is not at the path it
  names.
- **`results-not-last` → `results-format` (upheld).** L5's documented command ends in `tail -n 1`; the case's last line
  is `end of battle`.
- **`canned-shape` → `from-source`** and **`debian-is-file` → `debian-source` (upheld).** C_SRC is a 21-line
  transcription program with no pMARS code; a zero-byte regular file named `debian` is not source obtained from
  Debian packages.

## 7. Axis impact

- **calibration:** the map's labels were the one C2 product V7 could not scrutinise; this seat turns "all partly" from
  a finding into a tagging consequence, prices the strongest alternative (2 rows, 3 citations), and supplies executed
  witnesses for the destination clause (the receipt's own test letters) instead of a reading. The frozen predicate
  is untouched: `V7 ok rows=7 tags=7 bad=0` on the clone at the start, and again on a fresh scratch copy at the end
  (`v7-probes.txt` P0).
- **coverage:** no new source, no score move — an anti-overclaim on C2's map-level sentence, which is the honest
  direction for a falsification wave.

## 8. Tooling

Nothing installed or upgraded: `python3` (3.14), `gcc`, `bwrap`, `strace` were already present; pacman was not
touched. Scratch removed (`rm -rf` of `/fast/scratch/hyaku/kengaku-r38/F38CritTags`) after the receipts were copied.

VERDICT: tags-contestable-24-labels-change-2
