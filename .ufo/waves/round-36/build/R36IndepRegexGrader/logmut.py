#!/usr/bin/env python3
"""Independent re-implementation of the pinned TB2 `regex-log` grader (round 36, C2 cross-check).

Written by seat R36IndepRegexGrader. It does NOT import the grader
(`corpus/evidence/round36/tb2-regex-log/test_outputs.py`) and does NOT import the probe's
`run_grader`. The sample log (25 lines) and the expected-date list were copied by hand from the
captured grader source into SAMPLE_LOGS / EXPECTED_DATES below; scoring uses only those constants
and a locally written `re.findall` comparison. Exactly one thing is imported from the probe:
`build_cases`, which supplies the 24 frozen candidate regexes, their modes and their predictions.

Layers:
  1. sha256 pin of the captured grader (refuses on drift, like the probe);
  2. transcription self-check: an ast.literal_eval of the grader's own `sample_logs` /
     `expected_dates` literals is compared to the hand-typed constants (proves the copy, without
     importing or executing the grader);
  3. scoring: each of the 24 cases is written to a file (or not written, for `absent`) and scored
     with an independently coded copy of the three assertions:
       - missing file  : the file does not exist
       - invalid regex : re.compile raises re.error
       - wrong matches : re.findall(pattern, log_text, re.MULTILINE) != expected dates
  4. comparison against `corpus/evidence/round36/regex-log-probe.txt`: verdict, failing-assertion
     class, and the normalised/truncated first-line assertion text;
  5. per-line decomposition: for each case whose assertion fired after findall, the exact set of
     (log line index, got-vs-expected) differences, plus an invariant that the concatenation of the
     per-line findalls equals the whole-text findall (no case regex can span a newline).

Run: python3 indep.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin
Exit 0 iff all 24 verdicts, classes and assertion texts agree with the receipt.
"""
import argparse
import ast
import hashlib
import pathlib
import re
import sys
import tempfile

PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
GRADER_REL = "corpus/evidence/round36/tb2-regex-log/test_outputs.py"
GRADER_SHA256 = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"
RECEIPT_REL = "corpus/evidence/round36/regex-log-probe.txt"

# --- hand-copied from test_outputs.py:32-56 (own reading, not imported) -----------------------
SAMPLE_LOGS = [
    "2025-01-09 User login from 192.168.0.1",
    "192.168.1.100 accessed on 2023-12-31 and 2024-11-01",
    "No IP here but 2022-05-05 appears",
    "Multiple IPs 10.0.0.1 10.0.0.2 with 2020-01-01",
    "Date before IP 2019-06-15 from 172.16.0.5",
    "IP with date before and after 2018-05-05 8.8.8.8 info 2018-06-06",
    "Invalid IP 256.100.50.25 with date 2021-01-01",
    "Another invalid 123.456.78.90 2020-12-12",
    "Edge case 0.0.0.0 and date 2017-03-04",
    "Broadcast 255.255.255.255 on 2016-12-31",
    "Broadcast 255.255.255.255 for user 1234-56-7890",
    "Error for user with code abc192.168.1.1 on 2023-01-01",
    "Connection from 192.168.0.10 on 2023-13-05",
    "Access from 10.0.0.5 at 2022-00-15",
    "Server 172.16.5.4 logged event on 1995-06-32",
    "Client 8.8.8.8 reported on 2001-09-00",
    "User 192.0.2.1 performed action 2020-07-15abc",
    "Backup abc2021-08-20 from 203.0.113.5 completed",
    "2024-11-11 login from 198.51.100.23 at start",
    "Routine check by 203.0.113.10 ended on 1999-03-05",
    "User login 192.168.1.1abc on 2021-12-01",
    "abc10.0.0.5 accessed system on 1999-07-20",
    "Login attempt 172.16.0.256 on 2000-05-10",
    "Login attempt 172.16.0.256 for user 2000-02-30",
    "Login attempt 172.16.0.256 for user 2000-04-31",
]

# indexes of SAMPLE_LOGS that the grader's expected_dates reflects, in log order
EXPECTED_DATES = [
    "2025-01-09",
    "2024-11-01",
    "2020-01-01",
    "2019-06-15",
    "2018-06-06",
    "2017-03-03",
    "2016-12-31",
    "2024-11-11",
    "1999-03-05",
]

assert len(SAMPLE_LOGS) == 25, len(SAMPLE_LOGS)
assert len(EXPECTED_DATES) == 9, len(EXPECTED_DATES)
LOG_TEXT = "\n".join(SAMPLE_LOGS)
LINE_OF_EXPECTED = (0, 1, 3, 4, 5, 8, 9, 18, 19)  # derived by reading each line's comment
LINE_EXPECTED = {}
for _i, _d in zip(LINE_OF_EXPECTED, EXPECTED_DATES):
    LINE_EXPECTED.setdefault(_i, []).append(_d)


class MissingFile(Exception):
    """the grader's `assert regex_file.exists()` fired"""


class InvalidRegex(Exception):
    """the grader's `re.compile` try/except fired"""


class WrongMatches(Exception):
    """the grader's final `matches == expected_dates` assert fired"""


def score(regex, mode, tmpdir):
    """Independent copy of test_regex_matches_dates; returns None on pass, else raises."""
    p = pathlib.Path(tmpdir) / ("regex.txt" if mode == "file" else "absent-regex.txt")
    if mode == "file":
        p.write_text(regex)
    if not p.exists():
        raise MissingFile(f"Regex file {p} does not exist")
    text = p.read_text().strip()
    try:
        re.compile(text)
    except re.error as e:
        raise InvalidRegex(f"Regex in {p} is invalid: {e}")
    got = re.findall(text, LOG_TEXT, re.MULTILINE)
    if got != EXPECTED_DATES:
        raise WrongMatches(f"Expected {EXPECTED_DATES}, but got {got}")


def assertion_line(exc, tmpdir):
    """First line, tmp dir -> <tmp>, truncated exactly like the probe's run_grader."""
    txt = (str(exc).splitlines() or [type(exc).__name__])[0].replace(str(tmpdir), "<tmp>")
    return txt if len(txt) <= 160 else txt[:157] + "..."


def klass(name):
    return {"MissingFile": "missing-file",
            "InvalidRegex": "invalid-regex",
            "WrongMatches": "wrong-matches"}.get(name, "ok")


def klass_of_text(a):
    if a == "-":
        return "ok"
    if a.startswith("Regex file ") and a.endswith(" does not exist"):
        return "missing-file"
    if a.startswith("Regex in ") and " is invalid: " in a:
        return "invalid-regex"
    if a.startswith("Expected ") and "], but got " in a:
        return "wrong-matches"
    return "unknown"


def ast_literals(grader_path):
    """Pull the two list literals out of the grader's AST without importing it."""
    tree = ast.parse(grader_path.read_text())
    got = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in ("sample_logs", "expected_dates"):
                    try:
                        got[t.id] = ast.literal_eval(node.value)
                    except Exception:
                        pass
    return got


def parse_receipt(path):
    """case -> (predicted, observed, match, assertion) from the committed receipt."""
    rows, summary = {}, None
    for line in path.read_text().splitlines():
        if line.startswith("cases=") and "mismatches=" in line:
            summary = line
            continue
        m = re.match(r"^case=(\S+) predicted=(\S+) observed=(\S+) match=(\S+) "
                     r"assertion=(.*?) requirement=", line)
        if not m:
            continue
        name, pred, obs, mt, raw = m.groups()
        try:
            a = ast.literal_eval(raw)
        except Exception:
            a = raw.strip("'\"")
        rows[name] = (pred, obs, mt, a)
    return rows, summary


def per_line(regex):
    """[(line index, got, expected)] for every line whose findall disagrees with the line table."""
    bad = []
    for i, line in enumerate(SAMPLE_LOGS):
        got = re.findall(regex, line, re.MULTILINE)
        exp = LINE_EXPECTED.get(i, [])
        if got != exp:
            bad.append((i, got, exp))
    return bad


def concat_matches(regex):
    """Per-line concat of a case regex must equal its whole-text findall (no regex spans \\n)."""
    joined = []
    for line in SAMPLE_LOGS:
        joined.extend(re.findall(regex, line, re.MULTILINE))
    return joined == re.findall(regex, LOG_TEXT, re.MULTILINE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--receipt", default=RECEIPT_REL, help="receipt to compare against (for mutants)")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    grader = lane / GRADER_REL
    receipt = lane / a.receipt

    digest = hashlib.sha256(grader.read_bytes()).hexdigest()
    print(f"grader={GRADER_REL} sha256={digest} pin={PIN} pin_ok={'yes' if digest == GRADER_SHA256 else 'NO'}")
    if digest != GRADER_SHA256:
        print("REFUSE grader digest drift")
        return 2

    lits = ast_literals(grader)
    log_ok = lits.get("sample_logs") == SAMPLE_LOGS
    exp_ok = lits.get("expected_dates") == EXPECTED_DATES
    print(f"handtyped_log_lines={len(SAMPLE_LOGS)} ast_lines={len(lits.get('sample_logs') or [])} "
          f"handtyped_equals_grader={'yes' if log_ok and exp_ok else 'NO'} "
          f"log={'yes' if log_ok else 'NO'} expected={'yes' if exp_ok else 'NO'}")
    print(f"handtyped_log_sha256={hashlib.sha256(LOG_TEXT.encode()).hexdigest()}")

    sys.path.insert(0, str(lane / "plans"))
    from regex_log_probe import build_cases  # the only import: the 24 frozen cases

    cases = build_cases()
    rows, summary = parse_receipt(receipt)
    print(f"probe_cases={len(cases)} receipt_cases={len(rows)} receipt_summary={summary!r}")

    agree = 0
    vmis = cmis = amis = 0
    missing_receipt = []
    diffs = {}
    cat_ok = []
    verdicts = {}
    for name, regex, pred, req, mode in cases:
        with tempfile.TemporaryDirectory() as d:
            try:
                score(regex, mode, d)
                obs, cls, text = "pass", "ok", "-"
            except Exception as e:  # noqa: BLE001 - the three grader assertion classes
                obs, cls, text = "fail", klass(type(e).__name__), assertion_line(e, d)
        verdicts[name] = obs
        if regex is not None:
            try:
                re.compile(regex.strip())
            except re.error:
                pass  # invalid-regex: no findall happens, by construction
            else:
                cat_ok.append((name, concat_matches(regex)))
                if obs == "fail" and cls == "wrong-matches":
                    diffs[name] = per_line(regex)
        r = rows.get(name)
        if r is None:
            missing_receipt.append(name)
            print(f"case={name} mode={mode} observed={obs} class={cls} "
                  f"receipt=MISSING verdict_match=NO assertion_match=NO")
            vmis += 1
            continue
        rpred, robs, rmatch, rtext = r
        v_ok = (robs == obs and rpred == pred)
        c_ok = klass_of_text(rtext) == cls
        a_ok = (rtext == text)
        agree += v_ok and c_ok and a_ok
        vmis += not v_ok
        cmis += not c_ok
        amis += not a_ok
        print(f"case={name} mode={mode} predicted={pred} observed={obs} class={cls} "
              f"receipt_observed={robs} receipt_class={klass_of_text(rtext)} "
              f"verdict_match={'yes' if v_ok else 'NO'} class_match={'yes' if c_ok else 'NO'} "
              f"assertion_match={'yes' if a_ok else 'NO'}")
        if not a_ok:
            print(f"  mine    ={text!r}")
            print(f"  receipt ={rtext!r}")

    print(f"observed_pass={sum(1 for k in verdicts if verdicts[k] == 'pass')}/{len(cases)} "
          f"observed_fail={sum(1 for k in verdicts if verdicts[k] == 'fail')}/{len(cases)} "
          f"perline_concat_equals_wholtext={sum(ok for _, ok in cat_ok)}/{len(cat_ok)}")
    print("--- per-line differences (16 failing cases) ---")
    for name, _, _, _, mode in cases:
        if mode == "absent":
            print(f"DIFF case={name} class=missing-file no_findall=yes")
            continue
        if name == "invalid-regex":
            print(f"DIFF case={name} class=invalid-regex no_findall=yes")
            continue
        if name not in diffs:
            continue
        rowsd = diffs[name]
        print(f"DIFF case={name} lines_differ={len(rowsd)} line_indexes={[i for i, _, _ in rowsd]}")
        for i, got, exp in rowsd:
            g = repr(got) if len(repr(got)) <= 120 else f"<{len(got)} items> {got[:3]!r}..."
            print(f"  L{i} got={g} expected={exp!r}")

    print(f"agree={agree}/{len(cases)} verdict_mismatches={vmis} class_mismatches={cmis} "
          f"assertion_mismatches={amis}")
    ok = agree == len(cases) and len(cases) == 24 and not missing_receipt and log_ok and exp_ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
