# MutC2 — mutation test of `plans/round100_c2_rowcensus_bind.py` at T

**Seat.** MutC2 (leaf, no dispatch). **Lane** `kengaku-shokunin`, round 100.
**Target** `plans/round100_c2_rowcensus_bind.py` @ T `dbe0cefa607cf57f7f58346fce64bcc127144ca0`
(pristine sha256 `e0eec212059b415fc4889c4e0e53bdd76b81736fcaf3275472ef017e46278bcc`, = the
`frozen-instruments` row at F `54df15ca`). **Claim** `plans/round-100-claims.md` §R100-C2.
**Scratch** `/fast/scratch/hyaku/kengaku-r100/MutC2` (removed after receipts were copied).

## Verdict

| | count |
|---|---|
| distinct mutants | 65 (34 counter single-point, 30 tree single-point, 1 no-op control) |
| counter x forgery combos | 22 |
| total runs | 87 |
| killed | 44 (28 tree, 5 counter on the positive control, 11 combos) |
| survived | 19 (1 tree, 7 counter clauses, 11 combos) |
| controls pass | 2 (M00 no-op, T20 allowed C1 receipt) |

One survivor is a real coverage gap in the round's contract (**T21**, a duplicated SOURCES row is
invisible to R100-C2 K8/K10 and to R100-C1 L10). Every other survivor is a *sole-detector* result
(the leg is the only check for that defect class and is present and correct), or a clause that is
vacuous / equivalent / unreachable on any candidate-only fixture. No survivor contradicts the
frozen predicate: the pristine T tree passes all ten legs, and every forgery the claim names is
killed by at least one leg.

## Method

Each mutant is measured in its own `git clone --shared` fixture of the lane, never in the lane:
the fixture is checked out at P2 `5220b71d` (the counter's REF), overlaid with T's tree, mutated,
and committed as **two fixture commits** exactly as `.ufo/waves/round-100/L1/controls/run_controls.sh`
does:

* **F'** (fixture-only freeze): parent P2, tree = the mutant tree **minus** the three new
  `corpus/evidence/round{52,58,94}/PROVENANCE.md` files, carrying a rewritten
  `plans/round-100-claims.md` whose `frozen-instruments` block holds the instrument bytes **as
  mutated** (so K1's self leg resolves for a counter mutant) and whose `candidate-bytes` block
  holds the mutant candidate shas (so K10's `own_bad` resolves for a tree mutant).
* **rev** (the measured tree): parent F', tree = the mutant tree.

`git log --diff-filter=A rev -- plans/round-100-claims.md` therefore finds exactly one commit (F'),
`REF` resolves to P2 (the real REF), and `git diff F' rev` is exactly the C2 candidate bytes.
Counters run from the fixture root (`--lane . --rev HEAD`); the counter's own gate clones are
`--shared` clones of the fixture. TMPDIR was set to the scratch root throughout.

**Restoration.** No lane byte was written; the lane was read-only (`git clone --shared`). Every
fixture was deleted after its record was written (`driver.py` removes `mut/<id>` and `work/<id>`
unless `KEEP=1`), and the whole scratch tree was removed before this report was yielded. Before/after
hashes are recorded per mutant in `results/<id>.json` (`counter_sha`, `rev`, `fcommit`) and in
`results/tree_hashes.json` (pristine -> mutant sha256 of every touched path).

## Positive control

* **Pristine T, lane clone, direct run** (`baseline-T.txt`): `REV dbe0cefa…`, `REF 5220b71d…`,
  `GATE defects base=33 ref=32 rev=23`, `LEGS K1..K10=pass`, `TARGET pop=9 cleared=9 still=0 …`,
  `PREDICATE R100-C2 pass`, rc 0.
* **M00** (the same fixture construction with no mutation): all ten legs pass, rc 0. The fixture
  harness itself is therefore sound: F'/rev, the rewritten frozen table and the re-frozen candidate
  shas do not change the predicate.
* **T20** (the C1 probe receipt `corpus/evidence/round100/fdp-probe.txt` added *after* F'): passes,
  i.e. K10's `C1_RECEIPT` exemption is exercised in the positive direction. Paired with C33 it is
  killed (P18).

## Counter mutants

Each is one single-point text edit of the counter, run on the pristine tree (must pass if the edit
only removes a detector) and then, for the 22 that have one, paired with the forgery aimed at the
leg it removes. "pristine" is the mutant's verdict with no forgery; "combo verdict" is the verdict
with the forgery present.

### Counter mutants (single-point edits of `plans/round100_c2_rowcensus_bind.py`)


| id | edit (new text) | pristine | combo | combo verdict | failing leg | first DEFECT |
|---|---|---|---|---|---|---|
| C01 | `OWN_CLASSES = ("digest-wrong-capture",)` | killed | - | killed | K2 | DEFECT K2 derived=8 pop=9 only_derived=[] only_pop=['S300'] differ=[] |
| C02 | `if p.endswith(f"/{task}/") or p.endswith(f"/tb2-{task}/")` | killed | - | killed | K2 | DEFECT K2 derived=0 pop=9 only_derived=[] only_pop=['S210', 'S211', 'S219', 'S228', 'S232', 'S279', 'S281', 'S298', 'S300'] differ=[] |
| C03 | `if sid not in rows:` | SURVIVED | - | SURVIVED | - | - |
| C04 | `pop[sid] = (token, paths[-1], m_url.group(0))` | killed | - | killed | K2 | DEFECT K2 derived=9 pop=9 only_derived=[] only_pop=[] differ=['S210', 'S219'] |
| C05 | `if cls not in OWN_CLASSES:` | SURVIVED | - | SURVIVED | - | - |
| C06 | `terminal-bench-9/([0-9a-f]{40})` | killed | - | killed | K2 | DEFECT K2 derived=0 pop=9 only_derived=[] only_pop=['S210', 'S211', 'S219', 'S228', 'S232', 'S279', 'S281', 'S298', 'S300'] differ=[] |
| C07 | `task, rel = m_url.group(2), m_url.group(2)` | killed | - | killed | K2 | DEFECT K2 derived=0 pop=9 only_derived=[] only_pop=['S210', 'S211', 'S219', 'S228', 'S232', 'S279', 'S281', 'S298', 'S300'] differ=[] |
| C08 | `if len(line.strip().strip("|").split("|")) not in (3, 4):` | SURVIVED | P21 | SURVIVED | - | - |
| C09 | `url_files = []` | SURVIVED | P01 | killed | K4 | DEFECT K4 ids_not_in_pop=S180 |
| C10 | `changed_old = []` | SURVIVED | P20 | SURVIVED | - | - |
| C11 | `if len(hits) < 1:` | SURVIVED | P02 | killed | K5 | DEFECT K5 still_defective=- bind_resolve_or_other_wrong=S210 |
| C12 | `if not rd:` | SURVIVED | P03 | killed | K4,K5 | DEFECT K4 S210:binds=- |
| C13 | `if not cands:` | SURVIVED | P04 | killed | K5 | DEFECT K5 still_defective=S210 bind_resolve_or_other_wrong=S210 |
| C14 | `elif shas != [token]:` | SURVIVED | P05 | killed | K5,K6 | DEFECT K5 still_defective=S228 bind_resolve_or_other_wrong=S228 |
| C15 | `elif token not in shas or cap_sha != token:` | SURVIVED | P06 | SURVIVED | - | - |
| C16 | `extra_ids = []` | SURVIVED | P07 | SURVIVED | - | - |
| C17 | `if not binds or len(resolved) != 1 \` | SURVIVED | P08 | killed | K4,K5 | DEFECT K4 S210:binds=corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py |
| C18 | `or len(other_ref) != len(other_rev):` | SURVIVED | - | SURVIVED | - | - |
| C19 | `    still = []` | SURVIVED | P09 | killed | K4,K5 | DEFECT K4 S211:lines=0 |
| C20 | `caps_changed = []` | SURVIVED | P10 | killed | K4,K5 | DEFECT K4 S228:sha_col=['82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c'] capture=79a6ed58cbfb |
| C21 | `if bd != rd_:` | SURVIVED | - | SURVIVED | - | - |
| C22 | `row_missing = []` | SURVIVED | P11 | SURVIVED | - | - |
| C23 | `if len(live.get(s, [])) != 1 or live[s][0][0] != "200" or live[s][0][3] != url]` | SURVIVED | P12 | SURVIVED | - | - |
| C24 | `live_extra = []` | SURVIVED | P13 | SURVIVED | - | - |
| C25 | `if len(live.get(s, [])) < 1 or live[s][0][0] != "200"` | SURVIVED | P14 | SURVIVED | - | - |
| C26 | `outside_table = []` | SURVIVED | P15 | SURVIVED | - | - |
| C27 | `own_bad = []` | SURVIVED | P22 | SURVIVED | - | - |
| C28 | `k1_self = True` | SURVIVED | P16 | SURVIVED | - | - |
| C29 | `rev_files = set(ls(lane, BASE, "corpus/evidence"))` | SURVIVED | - | SURVIVED | - | - |
| C30 | `k7 = not moved` | SURVIVED | P19 | killed | K1,K7,K9,K10 | DEFECT K7 no freeze commit: census reference falls back to BASE |
| C31 | `k2 = bool(POP)` | SURVIVED | - | SURVIVED | - | - |
| C32 | `rows_changed = []` | SURVIVED | P17 | killed | K8 | DEFECT K8 base_rows_not_byte_equal=S210 |
| C33 | `outside_table = sorted(p for p in changed if p not in candidates)` | SURVIVED | P18 | killed | K10 | DEFECT K10 freeze=yes outside_table=['corpus/evidence/round100/fdp-probe.txt'] own_unbound=- |
| C34 | `if binds != [f"BIND {sid} capture={cap} by=provenance-row"] or len(resolved) < 0 \` | SURVIVED | - | SURVIVED | - | - |

## Tree mutants

One single-point edit of the fixture tree each, counter bytes pristine. "verdict" is the predicate
on that tree; the failing leg is the detector that fired.

### Tree mutants (single-point edits of the fixture tree)


| id | edit | verdict | failing leg | first DEFECT |
|---|---|---|---|---|
| T01 | SOURCES: silent outside row S001 rewritten (one extra space) | killed | K8 | DEFECT K8 base_rows_not_byte_equal=S001 |
| T02 | SOURCES: silent outside row S002 deleted | killed | K8 | DEFECT K8 base_rows_not_byte_equal=S002 |
| T03 | round52 PROVENANCE: fourth cell on the S228 line | killed | K3 | DEFECT K3 new_provenance_with_url=- not_three_cells=['corpus/evidence/round52/PROVENANCE.md'] old_provenance_changed=- |
| T04 | round52 PROVENANCE: fabricated id S999 line | killed | K4 | DEFECT K4 ids_not_in_pop=S999 |
| T05 | LIVE: S228 sha256 forged to zeros (frozen row re-frozen) | killed | K9 | DEFECT K9 receipt_frozen=True bad=S228 extra=- |
| T06 | round52 PROVENANCE: second binding line for S210 | killed | K4,K5 | DEFECT K4 S210:lines=2 |
| T07 | extra file corpus/evidence/round52/NOTES.md | killed | K10 | DEFECT K10 freeze=yes outside_table=['corpus/evidence/round52/NOTES.md'] own_unbound=- |
| T08 | round52 PROVENANCE: URL channel line for S180 | killed | K3,K4 | DEFECT K3 new_provenance_with_url=['corpus/evidence/round52/PROVENANCE.md'] not_three_cells=- old_provenance_changed=- |
| T09 | S210 binding moved from round52 to round58 | killed | K4,K5 | DEFECT K4 S210:file=corpus/evidence/round58/PROVENANCE.md |
| T10 | S210 binds the pypi-server capture instead of its own | killed | K4,K5 | DEFECT K4 S210:binds=corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py |
| T11 | POP capture round52/pypi-server bytes edited | killed | K4,K5,K6 | DEFECT K4 S228:sha_col=['82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c'] capture=79a6ed58cbfb |
| T12 | new PROVENANCE files identical F'..rev (pre-freeze commit) | killed | K10 | DEFECT K10 freeze=yes outside_table=- own_unbound=['corpus/evidence/round52/PROVENANCE.md', 'corpus/evidence/round58/PROVENANCE.md', 'corpus/evidence/ |
| T13 | frozen-instruments row for the counter removed | killed | K1 | DEFECT K1 gate_equal=True self=unfrozen |
| T14 | LIVE: extra id S999 line | killed | K9 | DEFECT K9 receipt_frozen=True bad=- extra=S999 |
| T15 | LIVE: S228 http=404 | killed | K9 | DEFECT K9 receipt_frozen=True bad=S228 extra=- |
| T16 | SOURCES: POP row S210 rewritten | killed | K6,K8 | DEFECT K6 rows_changed=['S210'] captures_changed=- |
| T17 | outside row S236 rebound by a round94 provenance line | killed | K4,K7 | DEFECT K4 ids_not_in_pop=S236 |
| T18 | S210 sha cell carries a second ticked sha | killed | K4 | DEFECT K4 S210:sha_col=['02bca54db4849b7c911253fb92f941e21db8b1eea13261a7e5a9871fca68b4ed', '000000000000000000000000000000000000000000000000000000000 |
| T19 | POP capture round52/pypi-server deleted | killed | K4,K5,K6 | DEFECT K4 S228:binds=- |
| T20 | C1 receipt added after the freeze (allowed change) | pass | - | - |
| T21 | SOURCES: silent outside row S001 duplicated | SURVIVED | - | - |
| T22 | round58 PROVENANCE: S211 line reduced to two cells | killed | K3,K4 | DEFECT K3 new_provenance_with_url=- not_three_cells=['corpus/evidence/round58/PROVENANCE.md'] old_provenance_changed=- |
| T23 | round52 PROVENANCE: S219 sha cell zeroed | killed | K4 | DEFECT K4 S219:sha_col=['0000000000000000000000000000000000000000000000000000000000000000'] capture=90970bb3c372 |
| T24 | round58 PROVENANCE emptied of table lines | killed | K4,K5 | DEFECT K4 S211:lines=0 |
| T25 | round58 PROVENANCE renamed to round59 | killed | K3,K4,K5,K7 | DEFECT K3 new_provenance_with_url=- not_three_cells=- old_provenance_changed=['corpus/evidence/round59/PROVENANCE.md'] |
| T26 | LIVE: second line for S228 | killed | K9 | DEFECT K9 receipt_frozen=True bad=S228 extra=- |
| T27 | POP capture round52/pypi-server replaced by another file's bytes | killed | K4,K5,K6 | DEFECT K4 S228:sha_col=['82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c'] capture=7f8d9ef66943 |
| T28 | round52 PROVENANCE: S210 line binds a path that does not exist | killed | K4,K5 | DEFECT K4 S210:binds=- |
| T29 | BASE provenance round50 gets a non-table comment line | killed | K3 | DEFECT K3 new_provenance_with_url=- not_three_cells=- old_provenance_changed=['corpus/evidence/round50/PROVENANCE.md'] |
| T30 | no freeze commit at all (claims file absent) | killed | K1,K7,K9,K10 | DEFECT K7 no freeze commit: census reference falls back to BASE |
## Combo matrix

The counter mutant is applied **and** the forgery it targets is present. `killed` means some other
leg still fails the predicate; `SURVIVED` means the whole predicate passes with that leg removed.

### Combo matrix (counter mutant x the forgery aimed at its leg)


| id | pairing | verdict | failing leg | first DEFECT |
|---|---|---|---|---|
| P01 | C09 (no :// scan) x URL-channel line | killed | K4 | DEFECT K4 ids_not_in_pop=S180 |
| P02 | C11 (zero-or-many lines) x duplicate S210 line | killed | K5 | DEFECT K5 still_defective=- bind_resolve_or_other_wrong=S210 |
| P03 | C12 (no round check) x S210 moved to round58 | killed | K4,K5 | DEFECT K4 S210:binds=- |
| P04 | C13 (no binds check) x S210 binds the wrong capture | killed | K5 | DEFECT K5 still_defective=S210 bind_resolve_or_other_wrong=S210 |
| P05 | C14 (no capture sha) x POP capture edited | killed | K5,K6 | DEFECT K5 still_defective=S228 bind_resolve_or_other_wrong=S228 |
| P06 | C15 (token membership) x second ticked sha | SURVIVED | - | - |
| P07 | C16 (no extra-id check) x fabricated S999 | SURVIVED | - | - |
| P08 | C17 (any BIND) x S210 binds the wrong capture | killed | K4,K5 | DEFECT K4 S210:binds=corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py |
| P09 | C19 (row may stay defective) x round58 emptied | killed | K4,K5 | DEFECT K4 S211:lines=0 |
| P10 | C20 (captures may change) x POP capture edited | killed | K4,K5 | DEFECT K4 S228:sha_col=['82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c'] capture=79a6ed58cbfb |
| P11 | C22 (no row equality) x silent row S001 rewritten | SURVIVED | - | - |
| P12 | C23 (no LIVE sha) x LIVE sha forged | SURVIVED | - | - |
| P13 | C24 (LIVE extra ids) x LIVE S999 | SURVIVED | - | - |
| P14 | C25 (duplicate LIVE) x second S228 line | SURVIVED | - | - |
| P15 | C26 (no outside-table) x post-freeze extra file | SURVIVED | - | - |
| P16 | C28 (self not frozen) x SELF frozen row removed | SURVIVED | - | - |
| P17 | C32 (POP rows may change) x S210 row rewritten | killed | K8 | DEFECT K8 base_rows_not_byte_equal=S210 |
| P18 | C33 (receipt not exempt) x receipt added after freeze | killed | K10 | DEFECT K10 freeze=yes outside_table=['corpus/evidence/round100/fdp-probe.txt'] own_unbound=- |
| P19 | C30 (no freeze needed) x claims file absent | killed | K1,K7,K9,K10 | DEFECT K7 no freeze commit: census reference falls back to BASE |
| P20 | C10 (BASE prov may change) x BASE provenance comment | SURVIVED | - | - |
| P21 | C08 (four cells allowed) x fourth cell | SURVIVED | - | - |
| P22 | C27 (own need not differ) x prov identical F'..rev | SURVIVED | - | - |

### Tree changes: before/after sha256 (pristine T -> mutant tree)

Rows are the tree leg of each tree mutant and of each combo (P*). T12/T20 change no file; T13 and
T30 change only the fixture claims file (see below); T21's added duplicate is listed under T21.

| id | path | before | after |
|---|---|---|---|
| P01 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `a1a11cc6e8a75ade…` |
| P02 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `4eb6a0d122d86eee…` |
| P03 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `52e66ee4ef54d291…` |
| P03 | `corpus/evidence/round58/PROVENANCE.md` | `a910b60a6deb82d8…` | `e947ae49ede1bde5…` |
| P04 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `5d1697c6edea325d…` |
| P05 | `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` | `82c6351722e9aa98…` | `79a6ed58cbfba356…` |
| P06 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `35c00d397cf8e46c…` |
| P07 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `43b3896ee32cfbcf…` |
| P08 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `5d1697c6edea325d…` |
| P09 | `corpus/evidence/round58/PROVENANCE.md` | `a910b60a6deb82d8…` | `85bff99501c7919c…` |
| P10 | `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` | `82c6351722e9aa98…` | `79a6ed58cbfba356…` |
| P11 | `corpus/SOURCES.md` | `1f4c2354b813eb82…` | `8244e1bcf4fed3ec…` |
| P12 | `.ufo/waves/round-100/L1/c2-live-refetch.txt` | `1399146ca8528822…` | `8fb928bebab26732…` |
| P13 | `.ufo/waves/round-100/L1/c2-live-refetch.txt` | `1399146ca8528822…` | `8ea83d80934f8a99…` |
| P14 | `.ufo/waves/round-100/L1/c2-live-refetch.txt` | `1399146ca8528822…` | `f132e49644169409…` |
| P17 | `corpus/SOURCES.md` | `1f4c2354b813eb82…` | `5434c521386e4fac…` |
| P20 | `corpus/evidence/round50/PROVENANCE.md` | `d52af96b1c35deaa…` | `00af1bc7880ca560…` |
| P21 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `0bb0c13c106f1efb…` |
| T01 | `corpus/SOURCES.md` | `1f4c2354b813eb82…` | `8244e1bcf4fed3ec…` |
| T02 | `corpus/SOURCES.md` | `1f4c2354b813eb82…` | `94cc787a7cd1aae1…` |
| T03 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `0bb0c13c106f1efb…` |
| T04 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `43b3896ee32cfbcf…` |
| T05 | `.ufo/waves/round-100/L1/c2-live-refetch.txt` | `1399146ca8528822…` | `8fb928bebab26732…` |
| T06 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `4eb6a0d122d86eee…` |
| T08 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `a1a11cc6e8a75ade…` |
| T09 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `52e66ee4ef54d291…` |
| T09 | `corpus/evidence/round58/PROVENANCE.md` | `a910b60a6deb82d8…` | `e947ae49ede1bde5…` |
| T10 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `5d1697c6edea325d…` |
| T11 | `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` | `82c6351722e9aa98…` | `79a6ed58cbfba356…` |
| T14 | `.ufo/waves/round-100/L1/c2-live-refetch.txt` | `1399146ca8528822…` | `8ea83d80934f8a99…` |
| T15 | `.ufo/waves/round-100/L1/c2-live-refetch.txt` | `1399146ca8528822…` | `67aaf5109c4765bd…` |
| T16 | `corpus/SOURCES.md` | `1f4c2354b813eb82…` | `5434c521386e4fac…` |
| T17 | `corpus/evidence/round94/PROVENANCE.md` | `974ba21db8703283…` | `9bc85a10d86768d4…` |
| T18 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `35c00d397cf8e46c…` |
| T19 | `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` | `82c6351722e9aa98…` | `absent…` |
| T21 | `corpus/SOURCES.md` | `1f4c2354b813eb82…` | `1854a6c877c0cc9d…` |
| T22 | `corpus/evidence/round58/PROVENANCE.md` | `a910b60a6deb82d8…` | `2e1e20e3f905f2a7…` |
| T23 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `8aaa0344d3ebbcc8…` |
| T24 | `corpus/evidence/round58/PROVENANCE.md` | `a910b60a6deb82d8…` | `85bff99501c7919c…` |
| T25 | `corpus/evidence/round58/PROVENANCE.md` | `a910b60a6deb82d8…` | `absent…` |
| T25 | `corpus/evidence/round59/PROVENANCE.md` | `7f3909f713db1e41…` | `a910b60a6deb82d8…` |
| T26 | `.ufo/waves/round-100/L1/c2-live-refetch.txt` | `1399146ca8528822…` | `f132e49644169409…` |
| T27 | `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` | `82c6351722e9aa98…` | `7f8d9ef66943f912…` |
| T28 | `corpus/evidence/round52/PROVENANCE.md` | `18be616be3826b51…` | `14dba330ef8ecb0b…` |
| T29 | `corpus/evidence/round50/PROVENANCE.md` | `d52af96b1c35deaa…` | `00af1bc7880ca560…` |

Fixture-claims hashes for the K1 mutants: `plans/round-100-claims.md` at T is
`018d213f20bd640c70f6a0e07bfa0ab5b1f9be76caa911ff7dc776a4f3bb329f`; T13 removes the one
`plans/round100_c2_rowcensus_bind.py` line from `frozen-instruments` ->
`e3ccb34d076f4d716533eaa15f98854e326773d57e3d859831c9009773edd790`; T30 deletes the file (absent).
## Findings (survivors) and repairs

### F1 — T21: a duplicated SOURCES row is invisible to both counters (real gap)

`corpus/SOURCES.md` with the S001 line duplicated verbatim (same id, same bytes) passes all ten
legs. K8 builds `row_lines()` with `setdefault`, so the duplicate is discarded and the surviving
line is still byte-equal; the membership test `line not in rev_set_lines` is satisfied. K10 cannot
see it either: `corpus/SOURCES.md` is a C1 candidate in `candidate-bytes`, and K10 compares shas
only for the C2-owned files (`own_bad` over `new_prov`). R100-C1's L10 does not see it either:
`new_row_defects()` diffs `set(rev_ids) - set(base_ids)`, and the duplicate adds no new id, so
"exactly 8 new SOURCES rows" still holds. The line gate does not see it either: with the S001 line
duplicated, `plans/anchor_line_check.py --lane .` prints the same 0 DEFECT lines as on the pristine
tree (`line-pristine.txt` / `line-dup.txt`, and SOURCES.md was restored byte-exactly to
`1f4c2354b813eb82c009591cd44b81fc1aa71a56c35471ef66c866af40f584ec`). The C2 claim's "no … SOURCES
row … changes", C1's "exactly 8" and the line gate are therefore all under-enforced for an *added
duplicate* row.
**Repair (route to round 101, not applied here):** K8 should compare the multiset of SOURCES row
lines (or the full line list) instead of membership, and C1's L10 should count row lines rather
than ids; alternatively K10 should sha-check every path in `candidate-bytes`, which alone would
turn any SOURCES byte change into a K10 failure.

### F2 — P11: K8 is the sole detector for outside-row byte equality

With C22 (`row_missing = []`) the silent-row rewrite T01 passes. K10 does not sha-check
`corpus/SOURCES.md` (it is a C1 candidate; only C2-owned candidates are sha-checked), so K8 is the
only leg standing between a rewritten outside row and a pass. The claim's K8 text is exactly this
check and it works; the finding is that there is no second line of defence.
**Repair:** extend K10's sha comparison from `own` to every path in `candidate-bytes` (SOURCES,
SKILL.md, the ledger). That is a detector change, not a contract change.

### F3 — sole-detector results (leg present, correct, and the only check)

These are killed mutants in the ordinary sense (the leg fires) but the *counter mutant* survives
because no other leg covers the same defect class. No repair is required for the predicate to hold;
each is listed so the redundancy budget is explicit.

| finding | mutant x forgery | sole detector | note |
|---|---|---|---|
| F3a | P06 C15 x second ticked sha | K4 `shas != [token]` | K5 checks the gate's BIND/RESOLVED lines, not the sha cell |
| F3b | P07 C16 x fabricated S999 | K4 `extra_ids` | K7 cannot see S999 (not a SOURCES row) |
| F3c | P12 C23 x forged LIVE sha | K9 `live[s][0][2] != token` | transitively equal to the capture sha via K4 `cap_sha == token` |
| F3d | P13 C24 x LIVE S999 | K9 `live_extra` | — |
| F3e | P14 C25 x duplicate LIVE line | K9 `len(live[s]) != 1` | — |
| F3f | P15 C26 x post-freeze extra file | K10 `outside_table` | — |
| F3g | P16 C28 x SELF row removed | K1 `k1_self` | — |
| F3h | P20 C10 x BASE provenance comment | K3 `changed_old` | T29 is a non-table comment; a table edit would also trip K4 |
| F3i | P21 C08 x fourth cell | K3 exactly-three-cells | — |
| F3j | P22 C27 x prov identical F'..rev | K10 `own_bad` | — |

### F4 — vacuous / equivalent / unreachable clauses (no fixture can distinguish them)

| finding | mutant | why it survives | evidence | repair |
|---|---|---|---|---|
| F4a | C03 drop the BASE-provenance `named` exclusion | vacuous: no POP row is named at BASE | `named` = 55 ids over 10 BASE PROVENANCE.md files, `POP ∩ named = ∅` | assert the invariant in the counter (or drop the clause); no contract change |
| F4b | C05 drop the 64-hex token guard | vacuous on this tree: `derived == POP` without it | C05 run: K2 pass, derived = POP = 9 | assert every POP token is 64-hex |
| F4c | C18 token SET relaxed to cardinality | unreachable: a POP row's other findings change only via SOURCES (K6/K8) or a capture (K6); S300's other token set is identical at REF and rev (only the class sharpens, `RECLASS`) | `baseline-T.txt` RECLASS line; T16/T11 runs | none — K6/K8 are the outer guards |
| F4d | C21 K7 ignores outside-row notes | masked: any outside-row note change also trips K4 (new provenance file naming an outside id) or K3 (BASE provenance changed) | P02/T17 runs | none |
| F4e | C29 resolving files looked up at BASE | equivalent: all 9 POP captures exist at BASE with the POP token, and a capture deleted at rev is caught by K4 `cap_sha != token` | 9/9 verified (`cap_at_base True`, `cap_sha_ok True`) | none |
| F4f | C31 K2 equality dropped | equivalent for candidate-only fixtures: `derive()` reads BASE (`ls(lane, BASE, …)`), so the derived set is immutable; K2 guards against *rule* drift, which C01/C02/C04/C06/C07 die on | C01/C02/C04/C06/C07 K2 failures | none |
| F4g | C34 RESOLVED line not required | unreachable: the gate emits exactly one `RESOLVED` per provenance-row binding; suppressing it needs a gate change (K1) or a binding change (K4/K5) | gate output at T (`RESOLVED S210…S300`, one each) | none |

### Killed mutants worth naming

* **K2 is load-bearing against rule drift**: five counter mutants that weaken the derivation
  (OWN_CLASSES, capture suffix, first-path choice, URL repo, task/rel grouping) fail K2 on the
  pristine tree — the frozen `POP` cannot be silently redefined.
* **K5 catches what K4's removal would let through**: P02 (duplicate line), P03 (wrong round),
  P04 (wrong capture path), P05 (edited capture), P08 (any BIND), P09 (emptied provenance) all fail
  K5 once the corresponding K4 sub-check is removed.
* **K7's BASE fallback is stricter, not weaker**: with C30 (no freeze required) and no claims file
  (T30/P19), K7 still fails because REF falls back to BASE and the pre-freeze P0 re-bind of S295
  moves an outside row. K1/K9/K10 also fail.
* **K10's candidate table is not a sha table**: P17 (C32 + POP row rewrite) is killed by K8, not
  K10, because SOURCES is a C1 candidate and only C2-owned candidates are sha-checked (same root
  cause as F2).

## Evidence inventory

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-100/w1/MutC2/`

| path | content |
|---|---|
| `baseline-T.txt` | pristine counter run at T (all legs pass, rc 0) |
| `gate-T.txt` | `anchor_digest_check.py --verbose` at T (23 DEFECT lines, 9 BIND/RESOLVED pairs) |
| `driver.py` | the fixture/mutant harness (one mutant per invocation) |
| `summarize.py`, `hash_evidence.py` | verdict roll-up; before/after tree hashes |
| `results/<ID>.json` | 87 records: rc, LEGS, DEFECT lines, counter sha, rev/F' hashes, full stdout |
| `results/tree_hashes.json` | pristine -> mutant sha256 for every touched tree path |
| `table.txt`, `tables-*.md` | the verdict tables reproduced above |
| `run.log`, `run2.log` | the two batch logs |

No tool was installed or upgraded for this seat (python3 3.x stdlib + git only).
