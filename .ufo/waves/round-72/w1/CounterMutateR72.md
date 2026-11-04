# CounterMutateR72 — R72-C1 `check_receipt` counter-mutation: six of eight assigned clauses killed, two provably non-load-bearing

**Verdict in one line.** Six assigned clauses are load-bearing (M1, M2, M3, M4, M5, M7 all kill:
each mutant still accepts the genuine receipt and accepts a receipt the pristine checker refuses);
two are not — **M6** (the K9 case dropped from the case-set check) survives because `cases_ok`,
`case-digest-unique`, `case-digest` and the per-case vector loop independently refuse a K9-less
receipt, and **M8** (the `PROBE_BLOB`/`PROBE` equality) survives because it is implied by the two
independent blob bindings: the 3×3 value enumeration is 9/9 identical rc and identical defect codes.
Four residual witness gaps are reported, not edited: `env_cleared=True` is a generator literal, a
duplicated `PROVENANCE` line is accepted although the frozen kill rule names it a failure, three of
the five digests the receipt prints are never compared, and `allowlist_seen` counts presence rather
than exclusivity.

## Item attacked and scope

R72-C1's checker is `plans/round72_c1_hf_probe.py::check_receipt` (`:715-855`), scoped to the
provenance witness, the case set and the probe/blob binding. Nine single-clause mutants (M1–M8 plus
three attribution probes M3a/M3b/M6b) were built in
`/fast/scratch/hyaku/kengaku-r72/CounterMutateR72/mutants/`; the lane instrument was only read.
No predicate, case table, vector, digest, kill rule or target was edited; the two rules that look
wrong (F1/F2) are findings below.

Protocol, fixed before data: a mutant is **killed** when it (a) exits 0 on the genuine receipt and
(b) exits 0 on a receipt the pristine checker refuses with rc 1; **survived** when it still refuses
every pristine-refused receipt aimed at its clause; **invalid** when it fails the accept arm. Each
mutant is exactly one hunk in a scratch copy, anchored with a `count == 1` assertion.

## Pinned bytes

Lane `master` tip `b6336136e0e891522b113a94d8e0bd65e0eae8de`; host `python3` 3.14.8 (mutant driver),
`python3` 3.13.16 + bubblewrap 0.13.1 (battery), stdlib only.

| file | sha256 |
|---|---|
| `plans/round72_c1_hf_probe.py` (checker under test) | `99867c7f080179b44f30e7887c2f0a6c434217a1ec49cd2fbc1b23981faa637e` |
| `corpus/evidence/round72/hf/receipt.txt` (receipt of record) | `fa060b7fa2e4adbf8f0d4de180bea2d66bc7598ed5f13dbcfcf6093b7c224087` |
| this seat's own battery receipt | `fa060b7f…` — `cmp` against the record, **rc 0**, byte-identical |

The genuine baseline is therefore the receipt of record, not a hand-written stand-in: a nine-case
battery run of the same instrument at the same tip reproduced it byte-for-byte.

## Baselines

| receipt | pristine rc | defect codes |
|---|---|---|
| genuine (record) | **0** | `DEFECTS n=0` / `PREDICATE R72-C1 pass` |
| T1 `PROVENANCE` line dropped | 1 | `provenance-absent,predicate` |
| T2 `env_cleared=False` | 1 | `provenance-env,predicate` |
| T3a `distinct=2` | 1 | `provenance-distinct,predicate` |
| T3b `transformers_file=/work/…` | 1 | `provenance-path,predicate` |
| T4 `canary_seen=3` | 1 | `provenance-canary,predicate` |
| T5 `allowlist_seen=8/9` | 1 | `provenance-allowlist-seen,predicate` |
| T6 `CASE K9` line dropped | 1 | `case-set,case-digest,case-digest-unique,predicate` |
| T6b `CASE`+`LEGS`+`VECTOR K9` dropped | 1 | `case-set,case-digest,case-digest-unique,legs-line,summary,predicate` |
| T7 `LIBRARIES transformers=0.0.0` | 1 | `library-drift` |
| T8 `PROBE`+`PROBE_BLOB` equal but wrong | 1 | `probe-blob,probe-working-tree` |
| T8b `PROBE` line absent | 1 | `probe-working-tree,predicate` |

Every baseline was taken with `--work` (the claim's counting-command shape), so the staged-digest
clause was active; `DEFECTS n=0` on the genuine receipt there re-derives all nine case digests.
The same twelve receipts were also run without `--work` for the cross matrix.

## Result matrix

| # | clause neutered | kill receipt | pristine rc | mutant rc | verdict |
|---|---|---|---|---|---|
| M1 | `PROVENANCE` absent branch (`prov_ok=False` + defect) | T1 | 1 | **0** | **KILLED** |
| M2 | `env_cleared != "True"` | T2 | 1 | **0** | **KILLED** |
| M3 | `distinct` + `/venv/` path (both sites) | T3a, T3b | 1, 1 | **0, 0** | **KILLED** |
| M4 | `canary_seen != "0"` | T4 | 1 | **0** | **KILLED** |
| M5 | `allowlist_seen != 9/9` | T5 | 1 | **0** | **KILLED** |
| M6 | K9 no longer required by the case-set check | T6, T6b | 1, 1 | 1, 1 | **SURVIVED** |
| M7 | `LIBRARIES` drift | T7 | 1 | **0** | **KILLED** |
| M8 | `blob_ok` (PROBE_BLOB sha == PROBE sha) | T8, T8b | 1, 1 | 1, 1 | **SURVIVED** |
| M3a | `distinct` only | T3a | 1 | **0** | killed (attribution) |
| M3b | `/venv/` prefix only | T3b | 1 | **0** | killed (attribution) |
| M6b | K9 dropped from case-set **and** `cases_ok` | T6, T6b | 1, 1 | 1, 1 | **SURVIVED** (attribution) |

Accept arms: every listed mutant exits 0 with `DEFECTS n=0` / `PREDICATE R72-C1 pass` on the
genuine receipt **with and without** `--work` (M1–M8 all clean; the derived-baseline arm agrees).
Specificity: the cross matrix shows each killed mutant accepts exactly the genuine receipt plus the
tamper(s) aimed at its own clause — `M1 {GENUINE,T1}`, `M2 {GENUINE,T2}`, `M3 {GENUINE,T3a,T3b}`,
`M4 {GENUINE,T4}`, `M5 {GENUINE,T5}`, `M7 {GENUINE,T7}`; `M6`, `M6b`, `M8` accept `{GENUINE}` only,
and `PRISTINE` accepts `{GENUINE}` only.

## The two clauses that are not load-bearing

**F1 — M6, the K9 case-set membership, is a duplicate detector.** The case-set clause is
`sorted(r["CASE"]) != sorted(ids)`; `cases_ok` contains the same conjunct
(`sorted(r["CASE"]) == sorted(ids)`) and feeds the recomputed `PREDICATE` line. Therefore any
receipt that trips `case-set` also forces `predicate == "fail"`, and the final return refuses it
either way (predicate defect when the receipt says `pass`; `predicate == "pass"` false when it says
`fail`). Empirically, the K9-less receipt T6 is still refused by M6 through `case-digest-unique`
(eight distinct digests ≠ `len(CASES)=9`), `case-digest` under `--work` (the K9 stage is absent, so
`None != want`), and the per-case vector loop; T6b adds `legs-line` and `summary`. M6b, which also
relaxes `cases_ok`, still refuses both through `case-digest`/`case-digest-unique`. So the K9 case is
enforced by at least four independent clauses and the named one can never be the deciding clause.
*Consequence:* the claim's K9 coverage is real, but the `case-set` line's K9 membership is dead
weight — the count-based `case-digest-unique` and the per-case digest re-stage are what price it.

**F2 — M8, the `PROBE_BLOB`/`PROBE` equality, is implied.** `probe-blob` fires when
`PROBE_BLOB.sha256 != blob`; `probe-working-tree` fires when `PROBE.sha256 != blob`. If neither
fires then `PROBE_BLOB.sha == PROBE.sha == blob`, so `blob_ok` is never the deciding conjunct.
Enumeration over `PROBE`×`PROBE_BLOB` ∈ {committed blob, `0`×64, absent}: **9/9 pairs identical rc
and identical defect codes** between pristine and M8 (e.g. `blob/zero` → `probe-blob,predicate`
under both; `zero/zero` → `probe-blob,probe-working-tree` under both; `absent/absent` →
`probe-blob,probe-blob-rev,probe-working-tree,predicate` under both). No receipt can isolate it.

## Residual findings (reported, not edited)

**F3 — `env_cleared=True` is a generator literal, not a witness.** `battery_lines` writes
`f"PROVENANCE env_cleared=True …"` with no field of the sandbox payload feeding it (`run_case`
returns `env_keys`, `canary`, `transformers_file` — never a cleared flag). The clause is
enforceable against a forged receipt (M2 is killed; removing the token is refused,
`provenance-env,predicate`), but no genuine battery can ever print `False`, so the clause cannot
detect a real environment leak. The leak detectors that *are* derived are `canary_seen` (M4),
`allowlist_seen` (M5) and `transformers_file` (M3).

**F4 — a duplicated `PROVENANCE` line is accepted.** The checker reads `prov_lines[0]` and never
checks the count, although the frozen kill rule lists "a `PROVENANCE` line that is
absent/**duplicated**/outside `/venv/`" as a failure. Probes: identical duplicate → rc 0,
`DEFECTS n=0` (P2); first line good, second line `canary_seen=7` → rc 0, `DEFECTS n=0` (P3), with
and without `--work`. Absent and outside-`/venv/` are enforced; duplicated is not.

**F5 — three of the five printed digests are unbound.** The receipt's `GRADER`, `INSTRUCTION` and
`MODEL` sha lines and its `SANDBOX` line are never compared to lane-derived values; replacing all
four with zeros/`bwrap=no port=1 net=host cleared_env=False` still exits 0 with `DEFECTS n=0`
(P1, both arms). The lane files themselves are re-derived against the constants, so the predicate
stays true of the artifact, but the receipt's printed header is decorative (carried from round 71's
`unbound-receipt-digests`, still open).

**F6 — `allowlist_seen` counts presence, not exclusivity.** It is `sum(1 for n in allow_names if
all_allow)` where `all_allow` asks whether the sandbox's `env_keys` is a superset of the nine
allowlisted names; extra inherited variables are not counted, and the `PROVENANCE` line records no
total key count. `--clearenv` is real in `bwrap_argv`, so this is a witness-strength bound, not a
known leak: the canary is the only field that would catch a specific inherited variable.

## Commands run (exact)

1. `python3 plans/round72_c1_hf_probe.py --lane <lane> --work <S>/battery --receipt <S>/receipt.txt
   --port-lock /fast/scratch/hyaku/kengaku-r72/port5000.lock` — nine cases,
   `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`, `SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=2`,
   `PREDICATE R72-C1 pass`, **rc 0**, 143 s. `cmp` against
   `corpus/evidence/round72/hf/receipt.txt` → **rc 0**.
2. `python3 plans/round72_c1_hf_probe.py --lane . --check-receipt <S>/receipt.txt --work
   <S>/receipt-check` — `DEFECTS n=0` / `PREDICATE R72-C1 pass`, **rc 0**, 1.22 s.
3. `python3 <S>/mutate.py` — builds the 11 measured mutants, 12 receipts, pristine baselines,
   diagonal with `--work`, cross matrix, M8 enumeration; **rc 0**, 4 m 04 s
   (log: `CROSS PRISTINE accepts=GENUINE` … `EQUIV-M8 … same=True`).
4. `python3 <S>/extra_probes.py` — P1 `rc 0`, P2 `rc 0`, P3 `rc 0`, P4 `rc 1 (predicate)`,
   P5 `rc 1 (provenance-env,predicate)`; **rc 0**, 12 s.

**Calibration note (why the accept arm matters).** The first mutant build was discarded before any
verdict was recorded: M1's neuter moved the `else:` branch onto `if False:` so the T1 receipt
crashed with `IndexError` (rc 1, no `DEFECTS` line) — an apparent "survived" that was a broken
mutant; M6's first form rejected the *genuine* receipt (K9 present) and was invalid. Both were
rewritten (M1 keeps the `else` reachable, M6 makes K9 optional) and re-run; only the corrected run
is reported. This is the protocol working: a mutant that fails its accept arm is invalid, not a
kill.

## Unrun rows (declared)

Built but **not executed** — the wave was wrapped up before the consolidated rerun:
`M6c` (case-set clause deleted outright), `M9` (allowlist names), `M10` (LEG-COVERAGE), `M11`
(SUMMARY), `M12` (case-digest under `--work`). Their receipt tampers are in the scratch driver but
have no measured verdict; they are listed as `UNRUN` in
`corpus/evidence/round72/c1-counter-mutants.txt` and must not be read as passes. The eight assigned
clauses are fully measured.

## Evidence and restoration

- Matrix, baselines, mutant shas, per-target outputs, cross matrix, M8 enumeration and probe
  results: `corpus/evidence/round72/c1-counter-mutants.txt` (written before scratch removal).
- Lane instrument sha256 re-read at run time = `99867c7f…`; no lane file was written, so no restore
  was required. No git/jj mutation was run. No tool was installed or upgraded (pacman untouched).
- Scratch `/fast/scratch/hyaku/kengaku-r72/CounterMutateR72` holds every clone, mutant, receipt and
  work tree; it is removed after the evidence file, and the removal is verified (path absent).
- Port 5000: the battery took `/fast/scratch/hyaku/kengaku-r72/port5000.lock`; all checker and
  mutant runs bind nothing.
