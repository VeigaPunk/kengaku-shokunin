# S250 — Python 3.15.2 argparse documentation

- URL: https://docs.python.org/3/library/argparse.html#name-or-flags
- Opened: 2026-11-04 UTC (L1 KengakuR74, round 74)
- Local capture: `corpus/evidence/round74/sources/argparse-docs.html`
- Size: 334994 bytes
- SHA256: `ad9095cdaa99c953046f510d6cd86cd6f7a1086c5aa35743c26e3fa41e4b5b8d`
- Section: `<section id="name-or-flags">`
- Anchor quote located at capture lines 908–910:
  “The add_argument() method must know whether an optional argument, like -f or --foo, or a positional argument, like a list of filenames, is expected.” (24 words).
- Secondary located quote (lines 910–912):
  “The first arguments passed to add_argument() must therefore be either a series of flags, or a simple argument name.” (19 words).
- Admission scope: Tier A for Python command-line flag and argument specification contracts. Grounds the entry flag validation leg in `plans/round74_c2_registry_audit.py` and knowledge entry `corpus/knowledge/registry-argv-and-flag-audit.md`.
- Reject candidate: “Presence of a flag string in a script body proves `argparse` acceptance.”
  Reason: String presence in source or comments does not prove the argument parser configures or accepts the option.
  Flip: AST validation of `add_argument()` calls or controlled subprocess execution with `--help` / `--<flag>`.
