---
title: "Registry argv and flag audit — grounding command syntax against executable contracts"
branch: eval
category: craft
source_ids:
  - S250
last_compiled: 2026-11-04
verified-at: 2026-11-04 (L1 live fetch, HTTP 200; capture sha256 ad9095cdaa99c953046f510d6cd86cd6f7a1086c5aa35743c26e3fa41e4b5b8d)
recheck: on-release
writer: KengakuR74 (L1)
admission: hold
---

# Registry argv and flag audit — grounding command syntax against executable contracts

source: S250 (Python 3.15.2 argparse documentation, `https://docs.python.org/3/library/argparse.html#name-or-flags`, opened 2026-11-04 UTC; capture `corpus/evidence/round74/sources/argparse-docs.html`, sha256 `ad9095cdaa99c953046f510d6cd86cd6f7a1086c5aa35743c26e3fa41e4b5b8d`, line 908: “The add_argument() method must know whether an optional argument, like -f or --foo, or a positional argument, like a list of filenames, is expected.”)

## 1. Thesis

A gate/probe registry row that declares a runnable entry command (e.g. `python3 plans/my_tool.py --lane . --work <DIR>`) makes a falsifiable contract claim about the target script's command-line interface. In round 73, `plans/round73_c2_registry_audit.py` defined `command_flags` but never invoked it, allowing registry rows to advertise unbacked flags (such as `--strict` or unsupported subcommands) without detection (C2BlindSpotR73 case C14). Furthermore, table parsers that silently skip malformed rows (columns != 8) create blind spots where broken rows disappear from accounting entirely (cases C10 and C11).

Auditing registry rows against command-line contracts requires:
1. Exact column count validation (`columns == 8` on every table line, rejecting silent skips as named `MALFORMED-ROW` defects).
2. Flag extraction from entry command syntax (`command_flags`), verifying that every declared option string exists in the script's source.
3. Runner script existence validation for self-test specifications.
4. Errata revision consistency enforcement across all matching errata items.

## 2. Structural checks vs semantic acceptance

Per S250, optional arguments are attached via `add_argument()`. Merely matching option strings (e.g. `--strict`) against script text detects gross hallucinations (flags completely absent from source), but does not guarantee runtime parsing or execution validity without scoping and option configuration checks.

- Structural check (in-repo gate): verifies that the flag string appears in the script file, preventing phantom flag declarations in the registry.
- Runtime acceptance (reject flip): requires executing `python3 <script> --help` or AST verification of `parser.add_argument()`.

## 3. Admission boundary

This entry carries `admission: hold`. S250 grounds the definition of option strings and flags, but complete runtime certification requires an outside non-author spot-check and execution verification per Q13/Q14.
