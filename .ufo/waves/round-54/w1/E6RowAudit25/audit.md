# R54-C2 entry re-execution audit

Clone: `/fast/scratch/hyaku/kengaku-r54/E6RowAudit25/tmp.GDPgzAVZCI/clone` (shared clone of current lane tip). Runner imported `hermetic_env` from `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round54_c2_entrytruth.py`, gave each row its own scratch TMPDIR under `/fast/scratch/hyaku/kengaku-r54/E6RowAudit25/`, combined stderr/stdout, and used a 600-second subprocess timeout. All three declared argv were checked: no forbidden `--selftest`, `--help`, `--dry`, `--version` option; corresponding script path exists in clone.

Executed command: `python3 plans/scratch_guard.py check .` — declared exit 2, observed 1, fragment match yes; **MISMATCH**. Tail: `CHECK red reason=sentinel-missing` (preceded by root/sentinel/seat report).

Executed command: `python3 plans/sources_adopt.py --lane .` — declared exit 2, observed 2, fragment match yes; **CONFIRMED**. Tail: usage begins `usage: sources_adopt.py [-h] [--selftest] [--registry REGISTRY]`; argparse reports unrecognized arguments.

Executed command: `python3 plans/stage_scan.py --lane .` — declared exit 2, observed 2, fragment match yes; **CONFIRMED**. Tail: `ERROR unknown option --lane`.
