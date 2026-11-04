#!/usr/bin/env python3
"""Q1 / Q21 admission-bar rules for corpus/knowledge entries.

Operationalises the frozen R84-C2 sentences (plans/round-84-claims.md at
b12a9d46806cb8d69fe48fac0f4efff0b266e4c2, quoted here, never edited):

    Q1  -- its first three lines are `source:`, `verified-at:` and `recheck:`,
           and `recheck:` names an ISO date or cadence and a re-check action;
    Q21 -- its `source:` line carries a 40-hex commit pin and its `recheck:`
           line names that pin or the re-pin cadence.

This file is a mutation instrument for those two rules, not the round-84 C2
counter (plans/round84_c2_admission.py, which the L1 owns and which also
measures Q13).

Usage:
    rules.py ENTRY.md [--json]
    rules.py --selftest

Exit: 0 no defect, 1 defect(s) present, 2 could-not-evaluate.

Operationalisation decisions.  The frozen sentence under-determines the
mechanics, so every choice below is written out.  None of them may weaken a
mutant kill; the battery in mutants.md tests each one.

D1  Order clause: labels are matched at column 0 of lines 1, 2 and 3 exactly
    (`source:`, `verified-at:`, `recheck:`, each followed by a space or end of
    line).  A blank or other line inside the first three fails the order
    clause.  A `recheck:` line found later in the document still supplies the
    Q1/Q21 value (that is what "its recheck: line" says); it is the position
    that fails, not the content.
D2  Timing clause: either a calendar-valid ISO-8601 date YYYY-MM-DD (shape and
    datetime.date.fromisoformat, so 2027-02-31 is not a date) or a cadence
    term from CADENCE_TERMS, word-bounded and case-insensitive.
D3  Action clause: either (a) an argv-shaped invocation -- a token that is a
    known runner or that starts with a repo path prefix -- or (b) an action
    verb from ACTION_VERBS carrying at least one object token, i.e. a
    substantive token left after the timing phrase, the verb, connectives and
    cadence terms are removed.  A bare verb with no object is not an action:
    `monthly re-verify` names no observable re-check, so Q1 stays red (m3).
D4  Pin clause: the first standalone 40-hex token on the `source:` line, with
    hex boundaries on both sides, so a 64-hex sha256 digest and a longer hex
    run cannot supply one.
D5  Naming the pin: the exact 40-hex string must occur in the recheck value,
    hex-bounded.  A 7-char prefix, a one-digit variant and a 64-hex digest all
    fail (m5, m7, N2, N3).
D6  Re-pin cadence: the recheck value carries a re-pin token and a cadence
    term.  `re-pin when needed` carries no cadence and does not satisfy it
    (N1 -- a judgement call, recorded as such).
D7  No extra requirement is added: the date is not required to post-date
    `verified-at:`, because the frozen Q1 does not say so.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import re
import sys

HEADER_LABELS = ("source:", "verified-at:", "recheck:")

PIN_RE = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{40}(?![0-9a-fA-F])")
ISO_SHAPE_RE = re.compile(
    r"(?<!\d)(?:19|20)\d{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])(?!\d)"
)
TOKEN_RE = re.compile(r"[A-Za-z0-9_.\-/]+")

CADENCE_TERMS = (
    "on each upstream release",
    "on upstream release",
    "on upstream change",
    "on pin change",
    "semi-annual",
    "semiannual",
    "fortnightly",
    "every release",
    "each release",
    "per release",
    "every round",
    "each round",
    "per-round",
    "per round",
    "every wave",
    "each wave",
    "per-wave",
    "per wave",
    "quarterly",
    "biweekly",
    "biannual",
    "annually",
    "monthly",
    "weekly",
    "yearly",
    "daily",
    "annual",
)
_ALT = "|".join(re.escape(t) for t in sorted(CADENCE_TERMS, key=len, reverse=True))
CADENCE_RE = re.compile(r"(?<![A-Za-z0-9])(?:" + _ALT + r")(?![A-Za-z0-9])", re.I)

REPIN_RE = re.compile(r"(?<![A-Za-z0-9])re-?pin(?:ned|ning|s)?(?![A-Za-z0-9])", re.I)

RUNNERS = frozenset(
    {
        "python",
        "python3",
        "bash",
        "sh",
        "zsh",
        "uv",
        "node",
        "bun",
        "pytest",
        "make",
        "git",
        "jq",
        "rg",
        "awk",
    }
)
PATH_PREFIXES = ("plans/", "scripts/", "corpus/", "tools/", ".ufo/")

ACTION_VERBS = frozenset(
    {
        "replay",
        "replays",
        "replayed",
        "re-run",
        "rerun",
        "reruns",
        "re-read",
        "reread",
        "recheck",
        "re-check",
        "re-verify",
        "reverify",
        "verify",
        "verifies",
        "re-derive",
        "rederive",
        "re-execute",
        "reexecute",
        "recount",
        "recounts",
        "reconcile",
        "reconciles",
        "audit",
        "audits",
        "refresh",
        "refreshes",
        "reopen",
        "re-open",
        "check",
        "checks",
        "diff",
        "diffs",
        "read",
        "reads",
        "run",
        "runs",
    }
)

STOP = frozenset(
    {
        "a",
        "again",
        "and",
        "as",
        "at",
        "be",
        "by",
        "each",
        "every",
        "for",
        "from",
        "in",
        "into",
        "is",
        "it",
        "its",
        "must",
        "no",
        "not",
        "of",
        "on",
        "or",
        "out",
        "per",
        "recheck",
        "should",
        "so",
        "that",
        "the",
        "then",
        "this",
        "to",
        "up",
        "with",
    }
)


# --------------------------------------------------------------------------
# primitives
# --------------------------------------------------------------------------


def first_iso_date(value: str) -> str | None:
    """Return the first calendar-valid YYYY-MM-DD date in value, or None."""
    for match in ISO_SHAPE_RE.finditer(value):
        try:
            datetime.date.fromisoformat(match.group(0))
        except ValueError:
            continue
        return match.group(0)
    return None


def source_pin(source_value: str | None) -> str | None:
    """Return the first standalone 40-hex token, never a slice of a longer run."""
    if source_value is None:
        return None
    match = PIN_RE.search(source_value)
    return match.group(0) if match else None


def names_pin(recheck_value: str, pin: str) -> bool:
    """True only if the exact 40-hex pin occurs, hex-bounded, in recheck_value."""
    pattern = r"(?<![0-9a-fA-F])" + re.escape(pin) + r"(?![0-9a-fA-F])"
    return re.search(pattern, recheck_value) is not None


def repin_cadence(recheck_value: str) -> bool:
    """True only if a re-pin token and a cadence term are both present."""
    return REPIN_RE.search(recheck_value) is not None and (
        CADENCE_RE.search(recheck_value) is not None
    )


def _strip(value: str, regex: re.Pattern[str], *, keep: bool = False) -> str:
    out: list[str] = []
    last = 0
    for match in regex.finditer(value):
        out.append(value[last : match.start()])
        if keep:
            out.append(match.group(0))
        out.append(" ")
        last = match.end()
    out.append(value[last:])
    return "".join(out)


def action(value: str) -> tuple[bool, str]:
    """D3: argv-shaped invocation, or an action verb carrying an object."""
    rest = _strip(_strip(value, ISO_SHAPE_RE), CADENCE_RE)
    tokens = TOKEN_RE.findall(rest)
    for token in tokens:
        low = token.lower()
        if low in RUNNERS or low.startswith(PATH_PREFIXES):
            return True, f"argv-shaped command {token!r}"
    low_tokens = [(token, token.lower()) for token in tokens]
    verbs = [low for _, low in low_tokens if low in ACTION_VERBS]
    if not verbs:
        return False, "no re-check action: no argv-shaped command and no action verb"
    residual = [
        token
        for token, low in low_tokens
        if low not in ACTION_VERBS
        and low not in STOP
        and len(token) >= 3
        and any(ch.isalnum() for ch in token)
    ]
    if not residual:
        return (
            False,
            f"action verb {verbs[0]!r} carries no object: nothing observable is re-checked",
        )
    return True, f"action verb {verbs[0]!r} with object {residual[0]!r}"


def label_value(lines: list[str], label: str) -> str | None:
    """Value of the first line whose text starts with label at column 0."""
    for line in lines:
        if line.startswith(label):
            return line[len(label) :].strip()
    return None


# --------------------------------------------------------------------------
# rules
# --------------------------------------------------------------------------


def check_q1(text: str) -> dict[str, object]:
    lines = text.splitlines()
    order_ok = True
    order_why = "lines 1-3 are source:, verified-at:, recheck:"
    if len(lines) < 3:
        order_ok = False
        order_why = f"document has {len(lines)} line(s); three header lines are missing"
    else:
        for index, label in enumerate(HEADER_LABELS):
            if not lines[index].startswith(label):
                order_ok = False
                order_why = (
                    f"line {index + 1} is not {label!r} "
                    f"(got {lines[index][:48]!r})"
                )
                break

    recheck = label_value(lines, "recheck:")
    timing_ok = False
    timing_why = "no recheck: line"
    action_ok = False
    action_why = "no recheck: line"
    if recheck is not None:
        iso = first_iso_date(recheck)
        cadence = CADENCE_RE.search(recheck)
        if iso:
            timing_ok, timing_why = True, f"ISO date {iso}"
        elif cadence:
            timing_ok, timing_why = True, f"cadence {cadence.group(0)!r}"
        else:
            timing_why = "recheck value names neither an ISO date nor a cadence"
        action_ok, action_why = action(recheck)
    if recheck == "":
        timing_ok, timing_why = False, "recheck value is empty"
        action_ok, action_why = False, "recheck value is empty"

    passed = order_ok and timing_ok and action_ok
    reasons = [w for ok, w in ((order_ok, order_why), (timing_ok, timing_why), (action_ok, action_why)) if not ok]
    return {
        "pass": passed,
        "order": order_ok,
        "timing": timing_ok,
        "action": action_ok,
        "why": "ok" if passed else "; ".join(reasons),
        "detail": {"order": order_why, "timing": timing_why, "action": action_why},
    }


def check_q21(text: str) -> dict[str, object]:
    lines = text.splitlines()
    source = label_value(lines, "source:")
    recheck = label_value(lines, "recheck:")
    pin = source_pin(source)
    named = False
    cadence = False
    if source is None:
        why = "no source: line"
    elif pin is None:
        why = "source: line carries no standalone 40-hex commit pin"
    elif recheck is None:
        why = "no recheck: line"
    else:
        named = names_pin(recheck, pin)
        cadence = repin_cadence(recheck)
        if named:
            why = f"recheck names pin {pin}"
        elif cadence:
            why = "recheck names a re-pin cadence"
        else:
            why = f"recheck names neither pin {pin} nor a re-pin cadence"
    passed = bool(pin) and (named or cadence)
    return {
        "pass": passed,
        "pin": pin,
        "named": named,
        "repin_cadence": cadence,
        "why": why,
    }


def evaluate(path: str) -> dict[str, object]:
    with open(path, "rb") as handle:
        raw = handle.read()
    text = raw.decode("utf-8", "surrogateescape")
    q1 = check_q1(text)
    q21 = check_q21(text)
    defects = int(not q1["pass"]) + int(not q21["pass"])
    return {
        "path": path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "q1": q1,
        "q21": q21,
        "defects": defects,
        "result": "pass" if defects == 0 else "fail",
    }


# --------------------------------------------------------------------------
# selftest: the primitives, on synthetic strings, no filesystem
# --------------------------------------------------------------------------


def selftest() -> int:
    pin = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
    sha64 = "b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a"
    cases: list[tuple[str, bool, object, object]] = []

    def case(name: str, expected: object, observed: object) -> None:
        cases.append((name, expected == observed, expected, observed))

    case("iso valid", "2027-05-01", first_iso_date("recheck on 2027-05-01 please"))
    case("iso calendar-invalid (Feb 31)", None, first_iso_date("2027-02-31"))
    case("iso month-invalid", None, first_iso_date("2027-13-01"))
    case("pin from url", pin, source_pin("https://x/2fd12b88aafdd04a52c298e3940bcb189f9766d6/a.py"))
    case("pin absent in 64-hex sha256", None, source_pin("sha256 " + sha64))
    case("pin absent in 41-hex run", None, source_pin(pin + "0"))
    case("pin absent in 39-hex run", None, source_pin(pin[:-1]))
    case("names pin exact", True, names_pin("pin " + pin, pin))
    case("names pin prefix only", False, names_pin("pin " + pin[:7], pin))
    case("names pin one digit off", False, names_pin("pin " + pin[:-1] + "7", pin))
    case("names pin rejected inside longer hex, right", False, names_pin("sha256 " + pin + "ab", pin))
    case("names pin rejected inside longer hex, left", False, names_pin("sha256 ab" + pin, pin))
    case("cadence monthly", True, bool(CADENCE_RE.search("monthly re-verify")))
    case("cadence when-needed", False, bool(CADENCE_RE.search("re-pin when needed")))
    case("repin cadence yes", True, repin_cadence("quarterly; re-pin to the then-current commit"))
    case("repin cadence no cadence word", False, repin_cadence("re-pin when needed"))
    case("action argv", (True, True), (action("python3 plans/x.py --lane .")[0], True))
    case("action bare verb", False, action("monthly re-verify")[0])
    case("action date only", False, action("2027-05-01")[0])
    case("action verb+object", True, action("re-read the entry against upstream")[0])
    case(
        "q1 order green",
        True,
        check_q1("source: a\nverified-at: b\nrecheck: 2027-05-01 python3 plans/x.py\n")["pass"],
    )
    case(
        "q1 order blank line at 3",
        False,
        check_q1("source: a\nverified-at: b\n\nrecheck: 2027-05-01 python3 plans/x.py\n")["pass"],
    )
    case(
        "q1 timing missing",
        False,
        check_q1("source: a\nverified-at: b\nrecheck: python3 plans/x.py\n")["pass"],
    )
    case(
        "q21 green via cadence",
        True,
        check_q21(f"source: {pin}\nverified-at: b\nrecheck: quarterly python3 plans/x.py; re-pin\n")["pass"],
    )
    case(
        "q21 red no pin",
        False,
        check_q21("source: https://x/a.py\nverified-at: b\nrecheck: 2027-05-01 python3 plans/x.py\n")["pass"],
    )

    failures = 0
    for name, ok, expected, observed in cases:
        if not ok:
            failures += 1
            print(f"SELFTEST FAIL {name}: expected {expected!r} observed {observed!r}")
    print(f"SELFTEST cases={len(cases)} failures={failures}")
    print("SELFTEST pass" if failures == 0 else "SELFTEST fail")
    return 0 if failures == 0 else 1


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    args = list(argv)
    as_json = False
    if "--json" in args:
        as_json = True
        args.remove("--json")
    if "--selftest" in args:
        args.remove("--selftest")
        if args:
            print("rules.py: --selftest takes no path", file=sys.stderr)
            return 2
        return selftest()
    if len(args) != 1:
        print("usage: rules.py ENTRY.md [--json]\n       rules.py --selftest", file=sys.stderr)
        return 2
    try:
        result = evaluate(args[0])
    except OSError as exc:
        print(f"rules.py: cannot evaluate {args[0]}: {exc}", file=sys.stderr)
        return 2

    if as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["defects"] == 0 else 1

    q1 = result["q1"]
    q21 = result["q21"]
    print(
        "Q1={} order={} timing={} action={}".format(
            "pass" if q1["pass"] else "fail",
            "ok" if q1["order"] else "bad",
            "ok" if q1["timing"] else "bad",
            "ok" if q1["action"] else "bad",
        )
    )
    if not q1["pass"]:
        detail = q1["detail"]
        for span in ("order", "timing", "action"):
            if not q1[span]:
                print(f"Q1.{span}: {detail[span]}")
    print(
        "Q21={} pin={} named={} repin_cadence={}".format(
            "pass" if q21["pass"] else "fail",
            q21["pin"] or "none",
            "yes" if q21["named"] else "no",
            "yes" if q21["repin_cadence"] else "no",
        )
    )
    if not q21["pass"]:
        print(f"Q21.why: {q21['why']}")
    print(f"Q1.why: {q1['why']}")
    print(f"SHA256={result['sha256']} BYTES={result['bytes']}")
    print(f"DEFECTS={result['defects']}")
    print("RESULT=" + result["result"])
    return 0 if result["defects"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
