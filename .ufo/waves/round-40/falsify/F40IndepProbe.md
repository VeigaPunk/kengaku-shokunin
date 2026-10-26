# F40IndepProbe — independent re-run of the four non-frozen `db-wal` cases

Seat: critic, round 40 wave 2 (FALSIFY). **Attacks** the four results `R40CritProbe.md` derived from
non-frozen runs and that the entry is being asked to carry: §2 D3 (read-only decrypt+extract witness),
D4 (`truth` at the default path, and `truth` with both database files deleted), D5 (wrong-key read-only
isolation). Nothing was edited; the lane was cloned, not touched.

Axes named: (1) do the four cited results reproduce independently; (2) is each end state described
completely (files, sizes, digests); (3) is the proposed witness unique / what does it actually write;
(4) no host harm.

- Lane clone: `/fast/scratch/hyaku/kengaku-r40/F40IndepProbe/lane`, `git -C "$S/lane" rev-parse --show-toplevel`
  → `/fast/scratch/hyaku/kengaku-r40/F40IndepProbe/lane`; HEAD `ec1005a2a28bc5cfdde7723374368ed4cc956eed`;
  `git -C "$S/lane" status --porcelain` empty before and after; scratch removed at the end.
- Instrument: byte-identical copy of `plans/db_wal_probe.py`
  (`sha256sum "$S/probe_copy.py" "$S/lane/plans/db_wal_probe.py"` → both
  `69af65dfe4e2ecab9aec534c68a0bb2b071faf845f09b9ccff4a92e213e19ff3`, = `frozen_instruments`). The runner
  imports the probe's own `PINS`, `sandbox_argv`, `HARNESS_PY`, `MK_PY`, `DECRYPT`, `EXTRACT`, `RO`, `RW`,
  `Case`, `run_case` semantics and only *adds* case objects plus an end-state digest dump that runs after
  the sandbox exits (the probe itself deletes each work dir). Pins are re-checked against the captures at
  import; no case logic changed.
- Host-safety: every invocation below ran as
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 <script>`
  (the probe's per-case sandbox nests inside). No `systemd-run`, no writes outside scratch and my report
  dir; the two neutralized wave-1 shims were never executed.
- Host tools: sqlite3 3.54.0, Python 3.14.8, bubblewrap 0.13.1 — same stand-ins the probe states.

Receipts in `.ufo/waves/round-40/falsify/F40IndepProbe/`: `predictions.txt` (written **before** the first
run), `run1.txt`, `run2.txt` (`diff` → `BYTE-EQUAL-RERUN`), `ctl.txt`, `ctl2.txt`, `gt.txt`, `imm.txt`,
and the three scripts `runner.py`, `gt.py`, `imm.py`.

## 1. Pre-registered predictions (`predictions.txt`, before any run)

| case | recipe | predicted letters |
|---|---|---|
| P1 `truth-default-path` | `python3 /k/mk.py truth` (seeded `/app`) | `PPPPPPP` |
| P2 `truth-no-db` | `rm -f /app/main.db /app/main.db-wal` then the same | `PPPPPPP` |
| P3 `xor-42-RO` | XOR `0x42` in place, `EXTRACT` with `mode=ro` | `PPPPPPP` |
| P4 `xor-43-RO` | XOR `0x43` in place, `EXTRACT` with `mode=ro` | `PPPPFPF` |

Predicted artefacts were recorded too, including that P1's `main.db`/`main.db-wal` equal the captures,
`recovered.json` = `dd04f318…`, P3's WAL = `a00cfbf8…`/head `377f0682`, P4's WAL = `8a46e91e…`/head
`367e0783` and its 5-row JSON with values `100..500`.

## 2. Measured (four cases, `run1.txt` = `run2.txt` byte for byte)

| case | letters (pred → obs) | `/app` end state (size, sha256, first 4 bytes) | rows in `recovered.json` |
|---|---|---|---|
| P1 `truth-default-path` | `PPPPPPP` → `PPPPPPP` | `main.db` 8192 `68cb288e…d119` `53514c69`; `main.db-wal` 16512 `68753bdce26196a53194260d001544cc6bb8f9f38e2f2f6826d09798e31e6e26` `753d44c0`; `recovered.json` 472 `dd04f318daf77655ea9ae839f12e3d09b93661355c4fd5a946a9a9b338e910ef` | 11, ids 1–11, values `[150,250,300,…,1100]` |
| P2 `truth-no-db` | `PPPPPPP` → `PPPPPPP` | `/app/recovered.json` **only**, 472 `dd04f318…10ef`; `main.db` ABSENT, `main.db-wal` ABSENT, no `-shm` | 11, same rows |
| P3 `xor-42-RO` | `PPPPPPP` → `PPPPPPP` | `main.db` 8192 `68cb288e…d119`; **`main.db-shm` 32768 `cf857f02…f31e` `18e22d00`**; `main.db-wal` 16512 `a00cfbf891cb36157b7eca6df67f9920a0013769e446c2314ca204eef958c14c` `377f0682`; `recovered.json` 472 `dd04f318…10ef` | 11, values `[150,250,…,1100]` |
| P4 `xor-43-RO` | `PPPPFPF` → `PPPPFPF` | `main.db` 8192 `68cb288e…d119`; **`main.db-shm` 32768 `fd4c9fda…89eb` `18e22d00`**; `main.db-wal` 16512 `8a46e91ed1cca62f0cb0d4f1b37d7630d9e50ee2cdf766a5c7e44fcdf26801d6` `367e0783`; `recovered.json` 216 `dc514e5ed0589bb0476c134c5016654198f8ff16d34d38629ec7fa7cb975b69e` | 5, `[100,200,300,400,500]` |

P4 fails exactly `test_recovered_data_completeness` (`assert len(data) == 11`, `test_outputs.py:53`) and
`test_wal_was_decrypted` (`assert len(data) > 5`, `test_outputs.py:98`).

The non-frozen status is confirmed against the freeze itself: 28 `CASE` rows in
`corpus/evidence/round40/db-wal-dry-cases-freeze.txt`, and none is `truth` at the default path, a
read-only extraction, or a both-files-deleted export (`truth-wrong-path` writes to `/app/out/`).

Independent ground truth, derived from the two captures (`gt.txt`, not from the probe's `TRUTH`): base
alone → 5 rows `100..500`, JSON digest `dc514e5e…b69e`; XOR `0x42` → 11 rows `150,250,…,1100`, JSON
digest `dd04f318…10ef`; XOR `0x43` → WAL `8a46e91e…01d6`, head `367e0783`, 5 rows. Every digest in §2
matches this derivation, so P1/P3's `recovered.json` equals the true table exactly and P4's equals the
base table exactly.

## 3. One of my predictions was wrong, and the wave-1 text is silent about it

I predicted "no `-shm`" for P3/P4. Measured: both read-only extractions leave a 32,768-byte
`main.db-shm` whose first four bytes are `18e22d00` (little-endian `0x002de218` = wal-index version
3007000), i.e. a real wal-index header written into `/app`. Attribution (`ctl.txt`): with the same
decrypt step and **no** sqlite open, `decrypt-in-place-no-json` leaves `main.db` + repaired
`main.db-wal` and **no** `-shm`; and in `imm.txt` a clean copy opened with `mode=ro` creates
`main.db-shm` while `immutable=1` creates nothing. So the file is written by the extraction's
`mode=ro` connection, not by the decrypt or the seeding.

Consequence for the entry: P3 is a valid "WAL repaired, grader passes" witness, but any text calling
that pipeline clean or saying it leaves `/app` with only the database pair plus `recovered.json` is
false. `mode=ro` is read-only **for the database**, not for the directory
(`RO = "file:/app/main.db?mode=ro"`, `plans/db_wal_probe.py:146`).

## 4. Controls (frozen cases re-measured to support the two corrections the entry will carry)

| control | letters | end state |
|---|---|---|
| `ctl-decrypt-only` = frozen `decrypt-in-place-no-json` | `FFFFFFF` (predicted `FFFFFFF`) | `main.db` `68cb288e…d119`, `main.db-wal` `a00cfbf8…c14c` head `377f0682`, no `-shm`, no JSON |
| `ctl-xor-43-RW` = frozen `xor-wrong-key` | `PPPPFPF` (predicted `PPPPFPF`) | `main.db` `68cb288e…d119`, **`main.db-wal` ABSENT**, no `-shm`, `recovered.json` `dc514e5e…b69e` |

So both halves of D5's correction hold independently: the read-write extract **discards** the invalid
WAL (`so SQLite **discards** it — after the recipe there is no /app/main.db-wal at all`,
`R40CritProbe.md:113`), while the read-only read **keeps** it untouched (`8a46e91e…`, identical sha) and
still yields only 5 rows. My P4 is exactly the isolation run D5 asked for.

## 5. Does the D3 witness stay unique? (`imm.txt`, clean copies, WAL `a00cfbf8…` present)

| URI | rows | files created | WAL after |
|---|---|---|---|
| `?immutable=1` | 5 | none | `a00cfbf8…` unchanged |
| `?mode=ro&immutable=1` | 5 | none | unchanged |
| `?mode=ro` | **11** | `main.db-shm` | unchanged |

`immutable=1` makes SQLite ignore the WAL entirely, so `mode=ro` is the only shape among these that
applies the WAL *and* leaves it in place — D3's "This is the only shape that distinguishes \"the WAL file"
(`R40CritProbe.md:92`) survives, but only with the side-file caveat above. Note the same sentence is
the entry's licence to add a passing repaired-WAL case the frozen table lacks.

## 6. State of the three attacked claims after this run

1. **D3 — holds.** P3 passes `7 × P` with a genuinely repaired WAL (`377f0682`, `a00cfbf8…`) and no
   checkpointing of `main.db` (`68cb288e…`, byte-identical to the capture). Add: `main.db-shm` 32,768 B
   is part of that end state.
2. **D4 — holds, both halves.** P1 reproduces the wave-1 numbers exactly (`main.db`/`main.db-wal`
   bit-identical to the captures, `recovered.json` `dd04f318…`, `7 × P`), and P2 passes with **no
   database at all** — nothing but `recovered.json`
   (`No correct hand-typed export in the table; the grader passes with no database at all`,
   `R40CritProbe.md:95`). The entry may not claim the graded artefact requires a database.
3. **D5 — holds.** The wrong-key 5-row result is produced by the key *and* the destructive read; the
   read-only variant isolates the key (WAL survives, same sha) and still returns 5 rows.
4. **New constraint for the entry:** never describe P3 as leaving `/app` read-only or unmodified beyond
   the data; the `mode=ro` connection bootstraps `main.db-shm`. If the entry adopts P3 as its wave-2
   witness, it should print all four files (including the `-shm` digest) so the witness is checkable.

## Limits

Host sqlite3 3.54.0 / Python 3.14.8 / bwrap 0.13.1 stand in for the task image; the image was never
pulled; recipes run as the probing user. Four cases plus three controls; whether `-shm` would still be
created if `/app` were not writable was not tested (the extraction must write `recovered.json` there
anyway). `regrade=same` is an in-process second read (wave-1 D1), so it is not independent evidence and
I count nothing from it. My four-case runner adds cases only; the frozen 28-case receipt was neither
re-run nor re-pinned.

Agreement count: letters and every digest named by the four cited results matched on 4 of 4 cases; the
only divergence anywhere is the `-shm` file, which wave-1 did not claim absent (my prediction did).

VERDICT: indep-extra-agree-4/4
