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

### Tree mutant before/after sha256 (pristine T -> mutant)

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
