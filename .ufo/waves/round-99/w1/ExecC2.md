# ExecC2 — independent R99-C2 check (without relying on the round-99 counter)

Seat ExecC2, round 99. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
scratch `/fast/scratch/hyaku/kengaku-r99/ExecC2`, BASE `2233a66195e3d3d85856248fb8f66c1d8127cede`,
T `f72a8bc710b12473b5c768004e2581f980d924f4`.
Isolated `git clone --shared` checkouts detached at BASE (`cloneBASE`) and T (`cloneT`);
top-level verified with `git -C <clone> rev-parse --show-toplevel` before each checkout.
No production edits, no commits, no task calls. Pacman untouched, no installs.

## Verdicts

- S173: PASS — bound capture `corpus/evidence/round50/gitrepository-layout.adoc` sha256 equals row token and PROVENANCE sha column; exactly one PROVENANCE line names S173.
- S174: PASS — `corpus/evidence/round50/git-init.adoc`, same three-way equality, one line.
- S175: PASS — `corpus/evidence/round50/git-worktree.adoc`, same three-way equality, one line.
- S176: PASS — `corpus/evidence/round50/git-replace.adoc`, same three-way equality, one line.
- S177: PASS — `corpus/evidence/round50/git-fetch.adoc`, same three-way equality, one line.
- S180: PASS — `corpus/evidence/round79/sources/tb2-readme.md`, same three-way equality, one line. Gate detail differs from other rows: BASE `UNBOUND reason=no-capture-for-upstream-?/README.md-task=?` (not `row-carries-no-capture-locator`), no extra `anchor token` prefix ambiguity — token itself matches.
- S220: PASS — `corpus/evidence/round59/tb2-openssl-selfsigned-cert/solution/solve.sh` (`no-capture-for-upstream-openssl-selfsigned-cert/solution/solve.sh-task=solution` at BASE), three-way equality, one line.
- S225: PASS — `corpus/evidence/round61/whatwg-windows1252/index-windows-1252.txt`, three-way equality, one line.
- S270: PASS — `corpus/evidence/round82/fetch/candidate_pyproject.toml` (`no-capture-for-upstream-?/pyproject.toml-task=?` at BASE), three-way equality, one line.
- S285: PASS — `corpus/evidence/round92/graders/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_1.jsonl`, three-way equality, one line.
- S293: PASS — `corpus/evidence/round93/graders/schemelike-metacircular-eval/tests/test/01-factorial.scm`, three-way equality, one line.
- S306: PASS — `corpus/evidence/round95/graders/fix-code-vulnerability/upstream-bottle/bottle.py`, three-way equality, one line.
- PROVENANCE shape: PASS — all 8 new files are 3-column (`| row | file here | sha256 |`); `URL_HITS []`, no `http`/`://` substring; exactly 12 provenance data rows total (one per population row); every file is NEW at T (`git cat-file -e BASE:<path>` absent for all 8).
- BASE gate vs T gate (BASE gate bytes `git show 2233a661:plans/anchor_digest_check.py`, `--verbose`, `loc=` line numbers stripped): for rows present at BASE, exactly the 12 population rows change lines (`UNBOUND`+`DEFECT class=anchor-unbound` → `BIND ... by=provenance-row` + `RESOLVED`). Full-line diff also shows S334–S341 as new-at-T rows (BIND/RESOLVED at T only, no BASE line) — these are the R99-C1 additions (SOURCES diff shows pure `+` additions for S334–S341, no edits to the 12), not C2 population changes. Defects 45 → 33 (`rows=325→333 tokens=209→217`).
- Frozen counter at T: PASS, `PREDICATE R99-C2 pass`, rc 0, `pop=12 cleared=12 still=0 outside_rows=313 outside_removed=0 outside_added=0 outside_rebound=0 url_channel_files=0 rows_changed=0 captures_changed=0`.
- Census (read-only `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`): rc 0, `kengaku ok .../corpus/SOURCES.md` (W04 duplicate-url warnings are pre-existing scope notes, not failures).

## Commands run

```
mkdir -p /fast/scratch/hyaku/kengaku-r99/ExecC2
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin cloneT
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin cloneBASE
git -C cloneBASE checkout --detach 2233a66195e3d3d85856248fb8f66c1d8127cede
git -C cloneT checkout --detach f72a8bc710b12473b5c768004e2581f980d924f4
git -C cloneT show 2233a66195e3d3d85856248fb8f66c1d8127cede:plans/anchor_digest_check.py > gate_base.py
python3 independent_c2.py   # straight sha256/token/PROVENANCE comparison, no gate, no counter
cd cloneBASE && python3 ../gate_base.py --lane . --verbose > ../gate_base.txt 2>&1
cd cloneT && python3 ../gate_base.py --lane . --verbose > ../gate_t.txt 2>&1
cd cloneT && python3 plans/round99_c2_rowscoped_bind.py --lane . --rev f72a8bc710b12473b5c768004e2581f980d924f4 --work ../w2
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
```

## Evidence (under `.ufo/waves/round-99/w1/ExecC2/`)

- `independent_c2.py` — the no-counter checker (re-runnable from scratch root).
- `gate_base.py` — BASE gate bytes extracted via `git show`.
- `gate_base.txt` / `gate_t.txt` — full `--verbose` outputs (rc 1 both, defects 45/33).
- `gate_diff.txt` / `gate_unified.txt` — per-row diff (loc-stripped) and unified diff.
- `counter_t.txt` — frozen counter bytes at T (rc 0, predicate pass).
- `census.txt` — census validate output (rc 0).

## Risks / notes for L1

- S180 (and S220, S270, S285, S293, S306) use `no-capture-for-upstream-*` UNBOUND details rather than `row-carries-no-capture-locator`; the population rule "exactly ONE DEFECT line, class anchor-unbound" still holds per the 12-row check, but finding-class normalization in future counters should not over-specify the detail string.
- The naive per-row gate diff is 20 rows, not 12, because S334–S341 are new rows with T-only lines; scoping to "rows present at BASE" yields exactly 12. No other BASE-present row changed any DEFECT/BIND/RESOLVED/UNBOUND line.
