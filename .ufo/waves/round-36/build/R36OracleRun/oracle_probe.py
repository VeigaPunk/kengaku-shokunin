#!/usr/bin/env python3
"""R36OracleRun: run the pinned TB2 `regex-log` oracle (solution/solve.sh heredoc) through
(a) the real grader via plans/regex_log_probe.py:run_grader, and
(b) a 40-line hand-built probe table (re.findall per line, exactly as the grader applies it).

Nothing is hardcoded about the oracle: the pattern is extracted from the heredoc in
corpus/evidence/round36/tb2-regex-log/solve.sh. Mutants are whole-substring splices of that
extracted pattern, run through the same grader.
"""
import hashlib
import importlib.util
import pathlib
import re
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SOLVE = LANE / "corpus/evidence/round36/tb2-regex-log/solve.sh"
GRADER = LANE / "corpus/evidence/round36/tb2-regex-log/test_outputs.py"
PROBE = LANE / "plans/regex_log_probe.py"
START = "cat << 'EOF' > /app/regex.txt"
END = "EOF"


def extract_oracle(path):
    lines = path.read_text().splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.strip() == START]
    assert len(starts) == 1, starts
    i = starts[0] + 1
    body = []
    while lines[i] != END:
        body.append(lines[i])
        i += 1
    assert len(body) == 1, body
    return body[0], starts[0] + 1, i + 1  # pattern, heredoc-open line, heredoc-close line


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def grader_expected_dates(path):
    src = path.read_text()
    body = re.search(r"expected_dates = \[(.*?)\n    \]", src, re.S).group(1)
    return re.findall(r'"([^"]+)"', body)


ROWS = [
    # id, log line, instruction verdict (Y/N/AMB), expected date, note
    ("A1", "from 01.2.3.4 at 2020-01-01", "N", None, "octet 01 has a leading zero (instr:4)"),
    ("A2", "from 192.168.0.01 at 2020-01-01", "N", None, "4th octet 01 leading zero (instr:4)"),
    ("A3", "from 192.168.001.1 at 2020-01-01", "N", None, "3-digit octet 001 (instr:4)"),
    ("A4", "from 00.0.0.0 at 2020-01-01", "N", None, "octet 00 (instr:4)"),
    ("A5", "from 010.1.2.3 at 2020-01-01", "N", None, "3-digit octet 010 (instr:4)"),
    ("A6", "from 192.168.01.1 at 2020-01-01", "N", None, "3rd octet 01 (instr:4)"),
    ("B1", "8.8.8.8 on 2020-02-29", "Y", "2020-02-29", "Feb 29 permitted in all years (instr:3)"),
    ("B2", "8.8.8.8 on 2019-02-29", "Y", "2019-02-29", "Feb 29 permitted even non-leap (instr:3)"),
    ("B3", "8.8.8.8 on 2000-02-30", "N", None, "Feb capped at 29 (instr:3)"),
    ("B4", "8.8.8.8 on 2020-04-31", "N", None, "Apr has 30 days (grader:66-68 comment; instr silent)"),
    ("B5", "8.8.8.8 on 2020-01-31", "Y", "2020-01-31", "31-day month"),
    ("B6", "8.8.8.8 on 2020-04-30", "Y", "2020-04-30", "30-day month"),
    ("B7", "8.8.8.8 on 2020-02-28", "Y", "2020-02-28", "Feb 28"),
    ("C1", "8.8.8.8 on 12345-06-07", "N", None, "year is YYYY (instr:1)"),
    ("C2", "8.8.8.8 on 999-06-07", "N", None, "3-digit year (instr:1)"),
    ("C3", "8.8.8.8 on 0000-01-01", "Y", "0000-01-01", "4-digit year, value unconstrained"),
    ("D1", "user 1134-12-1234 8.8.8.8", "N", None, "instr:6 example, digit-adjacent"),
    ("D2", "x2020-01-01 8.8.8.8", "N", None, "letter before date (instr:7)"),
    ("D3", "2020-01-012 8.8.8.8", "N", None, "digit after date (instr:7)"),
    ("D4", "_2020-01-01 8.8.8.8", "Y", "2020-01-01", "underscore is not alphanumeric"),
    ("D5", "2020-01-01. 8.8.8.8", "Y", "2020-01-01", "dot is not alphanumeric"),
    ("E1", "::1 on 2020-01-01", "N", None, "IPv6, no dotted quad"),
    ("E2", "2001:db8::1 on 2020-01-01", "N", None, "IPv6"),
    ("E3", "fe80::1ff:fe23:4567:890a 2020-01-01", "N", None, "IPv6, hex groups"),
    ("E4", "1.2.3.4.5 on 2020-01-01", "Y", "2020-01-01", "5-octet dotted string: 1.2.3.4 is not alnum-adjacent (literal instr:7)"),
    ("E5", "version 1.2.3 on 2020-01-01", "N", None, "3 octets only"),
    ("E6", "1.2.3.256 on 2020-01-01", "N", None, "octet > 255 (instr:1 'IPv4 address')"),
    ("E7", "255.255.255.255 on 2020-01-01", "Y", "2020-01-01", "broadcast"),
    ("E8", "0.0.0.0 on 2020-01-01", "Y", "2020-01-01", "zero address"),
    ("F1", "10.0.0.1 10.0.0.2 with 2020-01-01", "Y", "2020-01-01", "two IPs, one date"),
    ("F2", "2020-01-01 came from 172.16.0.5", "Y", "2020-01-01", "date before IP"),
    ("F3", "x 2020-01-01 y 2019-06-15 z 8.8.8.8", "Y", "2019-06-15", "last date (instr:2)"),
    ("F4", "8.8.8.8 2020-01-01 2019-06-15", "Y", "2019-06-15", "last date after IP"),
    ("F5", "2020-01-01 and 2019-06-15 then 8.8.8.8", "Y", "2019-06-15", "last date, IP last"),
    ("F6", "8.8.8.8 2020-01-01 then 2021-02-02abc", "AMB", None, "last date token is alnum-adjacent: instr:2 vs instr:7 conflict"),
    ("F7", "no ip 2020-01-01 at all", "N", None, "no IPv4"),
    ("F8", "8.8.8.8abc 2020-01-01", "N", None, "alnum after IP"),
    ("F9", "abc8.8.8.8 2020-01-01", "N", None, "alnum before IP"),
    ("F10", "8.8.8.8 2020-13-01", "N", None, "month 13"),
    ("F11", "8.8.8.8 2020-01-32", "N", None, "day 32"),
]

MUTANTS = [
    ("M0-unmodified-oracle", None, "control"),
    ("M1-strict-octets", ("1?\\d?\\d", "(?:1\\d\\d|[1-9]?\\d)"),
     "no leading-zero octets (instr:4)"),
    ("M2-feb-30", ("02-(?:0[1-9]|1\\d|2[0-9])", "02-(?:0[1-9]|1\\d|2\\d|30)"), "Feb 30 accepted"),
    ("M3-apr-31", ("(?:04|06|09|11)-(?:0[1-9]|[12]\\d|30)",
                   "(?:04|06|09|11)-(?:0[1-9]|[12]\\d|3[01])"), "Apr/Jun/Sep/Nov 31 accepted"),
    ("M4-year-width", ("\\d{4}-", "\\d{2,6}-"), "year width 2..6 (instr:1 YYYY)"),
    ("M5-left-boundary-letters-only", ("(?=$|[^0-9A-Za-z])).*(?:^|[^0-9A-Za-z])(",
                                       "(?=$|[^0-9A-Za-z])).*(?<![A-Za-z])("),
     "date left boundary blocks letters only"),
    ("M6-right-boundary-letters-only", ("))(?=$|[^0-9A-Za-z])", "))(?![A-Za-z])"),
     "date right boundary blocks letters only (digit adjacency allowed)"),
    ("M7-first-date-only", ("(?=$|[^0-9A-Za-z])).*(?:^|", "(?=$|[^0-9A-Za-z])).*?(?:^|"),
     "positive control: lazy .* must break the battery"),
]


def verdict_line(pattern, line):
    return re.findall(pattern, line, re.MULTILINE)


def main():
    pattern, open_ln, close_ln = extract_oracle(SOLVE)
    print(f"oracle=corpus/evidence/round36/tb2-regex-log/solve.sh sha256="
          f"{hashlib.sha256(SOLVE.read_bytes()).hexdigest()}")
    print(f"oracle_heredoc=solve.sh:{open_ln}..{close_ln} body_line={open_ln + 1} "
          f"chars={len(pattern)} whitespace_tokens={len(pattern.split())}")
    print(f"oracle_pattern={pattern!r}")
    print(f"grader=corpus/evidence/round36/tb2-regex-log/test_outputs.py sha256="
          f"{hashlib.sha256(GRADER.read_bytes()).hexdigest()}")
    print(f"probe=plans/regex_log_probe.py sha256={hashlib.sha256(PROBE.read_bytes()).hexdigest()}")
    probe = load_module("r36_probe", PROBE)

    # (a) real grader, through the pinned probe's run_grader
    a_verdict, a_msg = probe.run_grader(GRADER, pattern, "file")
    print(f"\n[A] run_grader(oracle) verdict={a_verdict} assertion={a_msg!r}")
    a2, _ = probe.run_grader(GRADER, pattern + "\n", "file")
    print(f"[A] run_grader(oracle + trailing newline as the heredoc writes it) verdict={a2}")

    # independent re.findall against the fixture's own expected list
    src = GRADER.read_text()
    block = re.search(r"sample_logs = \[(.*?)\n    \]", src, re.S).group(1)
    logs = re.findall(r'"([^"]*)"', block)
    expected = grader_expected_dates(GRADER)
    got = re.findall(pattern, "\n".join(logs), re.MULTILINE)
    print(f"[A] fixture_lines={len(logs)} expected_count={len(expected)} got={got}")
    print(f"[A] findall_matches_expected={got == expected}")

    # (b) 40-line table
    print("\n[B] id | verdict | oracle | instruction | note")
    viol = []
    amb = []
    for rid, line, want, want_date, note in ROWS:
        m = verdict_line(pattern, line)
        obs = "Y:" + (m[0] if m else "") if m else "N"
        if want == "AMB":
            amb.append((rid, line, m, note))
            tag = "AMB"
        else:
            ok = (want == "Y" and m == [want_date]) or (want == "N" and m == [])
            tag = "ok" if ok else "VIOLATION"
            if not ok:
                viol.append((rid, line, want, want_date, m, note))
        print(f"{rid} | {tag} | {obs} | {want}{':' + want_date if want_date else ''} | {note}")

    print(f"\n[B] rows={len(ROWS)} violations={len(viol)} ambiguous={len(amb)}")
    for v in viol:
        print(f"[B] VIOLATION {v[0]} line={v[1]!r} instruction={v[2]} oracle={v[4]} note={v[5]}")
    for v in amb:
        print(f"[B] AMBIGUOUS {v[0]} line={v[1]!r} oracle={v[2]} note={v[3]}")

    # exhaustive octet acceptance sweep against the oracle itself
    cands = set()
    for i in range(0, 1000):
        cands.add(str(i))
    for i in range(0, 100):
        cands.add("%02d" % i)
    for i in range(0, 1000):
        cands.add("%03d" % i)
    def instruction_valid(o):
        return re.fullmatch(r"0|[1-9]\d{0,2}", o) is not None and int(o) <= 255
    pos = {0: [], 1: [], 2: [], 3: []}
    for o in sorted(cands):
        if instruction_valid(o):
            continue
        for k in range(4):
            octs = ["9", "9", "9", "9"]
            octs[k] = o
            if re.findall(pattern, ".".join(octs) + " on 2020-01-01", re.MULTILINE):
                pos[k].append(o)
    print(f"\n[OCT] candidates={len(cands)} instruction-invalid octets accepted by the oracle, "
          f"by octet position 1..4: {[pos[k] for k in range(4)]}")
    print(f"[OCT] accepted sets identical across positions="
          f"{all(pos[k] == pos[0] for k in range(4))} count={len(pos[0])}")
    allfour = ".".join([pos[0][1] if len(pos[0]) > 1 else "01"] * 4)
    print(f"[OCT] all-four leading-zero case {allfour!r} matches="
          f"{bool(re.findall(pattern, allfour + ' on 2020-01-01', re.MULTILINE))}")
    rejected_valid = []
    for o in sorted(cands):
        if not instruction_valid(o):
            continue
        if not re.findall(pattern, f"9.9.9.{o} on 2020-01-01", re.MULTILINE):
            rejected_valid.append(o)
    print(f"[OCT] instruction-valid octets the oracle rejects: {rejected_valid}")

    # mutant sweep through the real grader
    print("\n[M] mutant -> grader verdict (pass means the requirement is unenforced by the fixture)")
    for name, sub, why in MUTANTS:
        mut = pattern if sub is None else pattern.replace(sub[0], sub[1])
        changed = mut != pattern
        mv, mm = probe.run_grader(GRADER, mut, "file")
        print(f"{name} mutated={changed} verdict={mv} requirement={why}")
        if sub is not None and not changed:
            print(f"[M] WARNING splice missed for {name}")

    # [F] why the fixture cannot see the violations
    print("\n[F] fixture coverage holes")
    lz = [ln for ln in logs if re.search(r"(?:^|[^\d])(?:0\d)\.", ln)]
    print(f"[F] fixture_lines={len(logs)} lines_with_a_leading_zero_octet={len(lz)} {lz}")
    print(f"[F] fixture_negative_ip_markers="
          f"{[ln for ln in logs if '256' in ln or '456' in ln]}")
    feb = next(ln for ln in logs if "2000-02-30" in ln)
    apr = next(ln for ln in logs if "2000-04-31" in ln)
    print(f"[F] feb30_line={feb!r} invalid_ip_present={'172.16.0.256' in feb}")
    print(f"[F] apr31_line={apr!r} invalid_ip_present={'172.16.0.256' in apr}")
    m2 = pattern.replace("02-(?:0[1-9]|1\\d|2[0-9])", "02-(?:0[1-9]|1\\d|2\\d|30)")
    m3 = pattern.replace("(?:04|06|09|11)-(?:0[1-9]|[12]\\d|30)",
                         "(?:04|06|09|11)-(?:0[1-9]|[12]\\d|3[01])")
    m1 = pattern.replace("1?\\d?\\d", "(?:1\\d\\d|[1-9]?\\d)")
    print(f"[F] feb30 line as-is: oracle={re.findall(pattern, feb, re.M) or 'N'}")
    print(f"[F] feb30 line with 172.16.0.256->172.16.0.25: "
          f"M2={re.findall(m2, feb.replace('172.16.0.256', '172.16.0.25'), re.M) or 'N'}")
    print(f"[F] apr31 line as-is: oracle={re.findall(pattern, apr, re.M) or 'N'}")
    print(f"[F] apr31 line with 172.16.0.256->172.16.0.25: "
          f"M3={re.findall(m3, apr.replace('172.16.0.256', '172.16.0.25'), re.M) or 'N'}")
    synth = "from 01.2.3.4 with 2020-01-01"
    print(f"[F] synthetic negative line {synth!r}: oracle={re.findall(pattern, synth, re.M) or 'N'} "
          f"M1-strict={re.findall(m1, synth, re.M) or 'N'} "
          f"(fixture cannot separate them: it has no such line)")

    # spans for the leading-zero counterexamples: the IP in the match really is the bad one
    print("\n[SPAN] leading-zero counterexamples, whole-match spans")
    for rid, line, _, _, _ in [r for r in ROWS if r[0] in ("A1", "A2", "A4", "A6")]:
        for m in re.finditer(pattern, line, re.MULTILINE):
            print(f"{rid} line={line!r} span={m.span()} text={m.group(0)!r} capture={m.groups()}")

    # [G] multi-line probes (the grader joins lines with \n, no DOTALL)
    print("\n[G] multi-line probes (a line's own IP is the instruction's condition, instr:1)")
    gl = {
        "G1-date-at-start-of-IP-less-line": ("1.2.3.4\n2020-01-01", "N", None),
        "G2-date-on-line-then-IP-starts-next": ("2020-01-01\n1.2.3.4", "N", None),
        "G3-last-date-crosses-to-IP-less-line": ("1.2.3.4 2020-01-01\n2020-01-02", "Y", "2020-01-01"),
        "G4-both-lines-qualify": ("1.2.3.4 2020-01-01\n5.6.7.8 2021-02-03", "Y2", "2020-01-01,2021-02-03"),
        "G5-ip-less-line-then-IP-start": ("x 2020-01-01\n1.2.3.4 2021-02-03", "Y", "2021-02-03"),
        "G6-date-then-next-line-starts-with-date": ("1.2.3.4 2020-01-01\n2021-02-03 more", "Y", "2020-01-01"),
    }
    gl_viol = 0
    for k, (log, want, want_dates) in gl.items():
        ms = [m.group(1) for m in re.finditer(pattern, log, re.MULTILINE)]
        spans = [m.span() for m in re.finditer(pattern, log, re.MULTILINE)]
        exp = [] if want == "N" else want_dates.split(",")
        ok = ms == exp
        gl_viol += not ok
        print(f"{k} log={log!r} instruction={exp} oracle={ms} spans={spans} "
              f"{'ok' if ok else 'VIOLATION'}")
    print(f"[G] rows={len(gl)} violations={gl_viol}")

    # [X] fragility: the pinned fixture never puts an IP or a date at the very start of a
    # line that follows an unrelated one, so the leak above is invisible. Move one IP to the
    # start of fixture line 3 and the same oracle fails its grader.
    print("\n[X] fragility of the pinned fixture (modified grader copy under this scratch dir)")
    orig = logs[3]
    mod_line = "10.0.0.1 " + orig.replace("Multiple IPs 10.0.0.1 10.0.0.2", "Multiple IPs 10.0.0.2")
    src2 = src.replace(f'"{orig}"', f'"{mod_line}"')
    assert src2 != src
    copyp = pathlib.Path(__file__).with_name("test_outputs_ip_at_line_start.py")
    copyp.write_text(src2)
    print(f"[X] fixture_line4_rewrite={mod_line!r}")
    xv, xm = probe.run_grader(copyp, pattern, "file")
    print(f"[X] run_grader(oracle, modified copy) verdict={xv} assertion={xm!r}")
    logs2 = list(logs)
    logs2[3] = mod_line
    got2 = re.findall(pattern, "\n".join(logs2), re.MULTILINE)
    print(f"[X] modified-copy log findall={got2}")
    print(f"[X] extra={[d for d in got2 if d not in expected]} missing={[d for d in expected if d not in got2]}")
    print(f"[X] fixture line starts with an IP: "
          f"{[i for i, ln in enumerate(logs) if re.match(r'\d{1,3}\.', ln)]}; "
          f"line starts with a date: {[i for i, ln in enumerate(logs) if re.match(r'\d{4}-', ln)]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
