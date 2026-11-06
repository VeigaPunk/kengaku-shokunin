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
