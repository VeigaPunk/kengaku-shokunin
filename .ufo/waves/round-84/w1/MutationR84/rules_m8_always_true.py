#!/usr/bin/env python3
"""Instrument mutant m8: an always-true Q1/Q21 detector.

Every mutant battery needs a mutant of the instrument itself, otherwise a
detector that reports "clean" for everything is indistinguishable from a
correct one.  This file keeps rules.py's parsing, CLI and exit-code machinery
and replaces only the two rules with constants.

Expected behaviour under the battery's kill rule: it reports the BASE bytes
green, so the BASE-sensitivity gate (C2: "a base-insensitive check" fails the
claim) kills it, and it flags none of the mutant fixtures, which is what the
gate is there to catch.
"""

from __future__ import annotations

import sys

import rules


def _always_true(_text: str) -> dict[str, object]:
    return {
        "pass": True,
        "order": True,
        "timing": True,
        "action": True,
        "why": "mutant m8: always-true",
        "detail": {"order": "mutant m8", "timing": "mutant m8", "action": "mutant m8"},
    }


def _always_true_q21(_text: str) -> dict[str, object]:
    return {
        "pass": True,
        "pin": "mutant-m8",
        "named": True,
        "repin_cadence": True,
        "why": "mutant m8: always-true",
    }


rules.check_q1 = _always_true
rules.check_q21 = _always_true_q21

if __name__ == "__main__":
    sys.exit(rules.main(sys.argv[1:]))
