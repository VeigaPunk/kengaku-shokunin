#!/usr/bin/env python3
"""F40XMutLedgerOrder campaign driver (round 40 wave 2, falsify).

Runs >=10 near-variant mutants of plans/ledger_tip.py and plans/order_check.py -- none in the
frozen 21-mutant list of the C1 counter -- through the counter's own unedited machinery: same
sandboxed tool runs, same exhibits() kill rule, same battery40 fixtures, same survivor bookkeeping.
The counter module is imported from a byte-identical scratch copy (sha256 4d47800e... verified
against the lane tip); the ONLY override is the module-global MUTANTS list below.

Run inside the HOST-SAFETY sandbox:
  bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
        --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
        python3 xmut_driver.py --lane <scratch clone> --work <scratch run dir> \
        --only XL1,XL2,XL3,XL4,XL5,XL6,XL7,XO1,XO2,XO3,XO4,XO5,XO6,XO7
(--only makes the counter print `PREDICATE C1 n/a (non-default battery or mutant subset)`, which is
the honest label for a campaign that is not the frozen 21.)
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent

_spec = importlib.util.spec_from_file_location("c1_counter", str(HERE / "round40_c1_verify.py"))
c1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(c1)

L = "plans/ledger_tip.py"
O = "plans/order_check.py"

XMUT = [
    # -- ledger summary counters (the counter docstring names this class a limit: "text-only
    #    mutants (summary-line counts, labels) are not in the list because no direction here reads
    #    them"; claims freeze line 33 withdrew L08 for the same reason) --
    ("XL1", "ledger", "-", "rc-silence",
     f"{L}:249 'and then the summary line rows=<n> closed=<n> observed_pass=<n> mismatches=<n>' "
     "(total-line counters closed/observed_pass swapped)",
     "witness wit-xl1: summary line lies on every run; battery40 classes() reads only agree=NO row lines",
     '    print(f"rows={rows} closed={closed} observed_pass={passed} mismatches={mism}")',
     '    print(f"rows={rows} closed={passed} observed_pass={closed} mismatches={mism}")'),
    ("XL2", "ledger", "-", "rc-silence",
     f"{L}:245-246 'LEDGER <ledger> rows=<n> closed=<n> observed_pass=<n> mismatches=<n>' "
     "(per-ledger counters lclosed/lpassed swapped)",
     "witness wit-xl2: per-ledger summary line lies; not parsed by the counter",
     '                          f"observed_pass={lpassed} mismatches={lmism}")',
     '                          f"observed_pass={lmism} mismatches={lpassed}")'),
    # -- kind labels --
    ("XL3", "ledger", "-", "rc-silence",
     f"{L}:15-16 'kind=pin the check only pins closure bytes ... a pin failing means the closure "
     "evidence moved, not that the defect class came back' (r34_d2 relabelled kind=live)",
     "witness wit-xl3: R34-D2 row line prints kind=live; counter classes() ignores kind=",
     '    "r34_d2": "pin",',
     '    "r34_d2": "live",'),
    ("XL4", "ledger", "-", "rc-silence",
     f"{L}:233 unknown-check rows print kind=unknown (the KIND.get fallback); fallback relabelled "
     "kind=live so an unknown check masquerades as a behaviour check",
     "witness wit-xl4: unknown-check row prints kind=live on an r34_d6-flipped clone",
     '            kind = KIND.get(r.get("check"), "unknown")',
     '            kind = KIND.get(r.get("check"), "live")'),
    # -- REF AUDIT / REF BIND provenance lines --
    ("XL5", "ledger", "-", "rc-silence",
     f"{L}:37 'REF AUDIT ref=<ref> rev=<sha> tip=<sha> state=match - the ref resolves to the commit "
     "under audit; the body is bound to that sha' (line dropped)",
     "witness wit-xl5: on a clone with local master at the tip the reference prints REF AUDIT and "
     "the mutant does not; every battery40 ledger fixture clone is detached (REF BIND shape), so "
     "the branch is unreached there",
     '            print(f"REF AUDIT ref={ref} rev={rev} tip={tip} state=match")',
     '            pass  # REF AUDIT line suppressed'),
    ("XL6", "ledger", "-", "rc-silence",
     f"{L}:39,175 'REF BIND ref=<ref> rev=<sha> tip=<sha> source_ref=<sha|absent> why=clone-lacks-ref' "
     "(why label falsified to bound-anyway)",
     "witness wit-xl6: REF BIND line prints why=bound-anyway on the battery-shaped detached clone",
     '              f"why=clone-lacks-ref")',
     '              f"why=bound-anyway")'),
    # -- contrast probe (not one of the six axes): drop the buffered row statements; the row lines
    #    are the only ledger output the counter parses, so this one should be KILLED --
    ("XL7", "ledger", "NO:R34-D2", "silence",
     f"{L}:247 flush loop 'row and per-ledger lines are buffered and flushed only after every "
     "ledger has been evaluated' (statements flushed empty)",
     "contrast probe, expected killed by l_rows-open-row: proves the harness reports kills when the "
     "mutated bytes feed a parsed line",
     "    for line in statements:",
     "    for line in statements[:0]:"),
    # -- order_check.py clause 1: freeze-contains-receipt --
    ("XO1", "order", "-", "rc-silence",
     f"{O}:17,183 'FAIL when the freeze commit (the first commit adding <claims>) already contains "
     "<receipt>' (clause skipped)",
     "witness wit-xo1: repo whose freeze commit already carries the receipt (reference ORDER FAIL "
     "rc=1, mutant ORDER ok rc=0); no battery40 fixture has that shape",
     '        if git.rc("cat-file", "-e", f"{freeze}:{receipt}") == 0:',
     '        if False and git.rc("cat-file", "-e", f"{freeze}:{receipt}") == 0:'),
    ("XO2", "order", "-", "rc-mirror",
     f"{O}:17,183 (same clause, comparison inverted: rejects every honest two-commit repo)",
     "expected killed by o_gate-claims-gitlink (the only accept fixture; mutant exits 1 on it)",
     '        if git.rc("cat-file", "-e", f"{freeze}:{receipt}") == 0:',
     '        if git.rc("cat-file", "-e", f"{freeze}:{receipt}") != 0:'),
    # -- order_check.py clause 2: receipt-before-claims --
    ("XO3", "order", "-", "rc-silence",
     f"{O}:18,188 'FAIL when <receipt> was committed before <claims> (pre-registration inverted ...)' "
     "(clause skipped)",
     "witness wit-xo3: repo where the receipt commit is an ancestor of the freeze commit (reference "
     "ORDER FAIL rc=1, mutant ORDER ok rc=0); no battery40 fixture has that shape",
     '        if freeze != receipt_commit and git.rc("merge-base", "--is-ancestor", receipt_commit, freeze) == 0:',
     '        if False and freeze != receipt_commit and git.rc("merge-base", "--is-ancestor", receipt_commit, freeze) == 0:'),
    ("XO4", "order", "-", "rc-mirror",
     f"{O}:18,188 (same clause, comparison inverted: rejects every honest two-commit repo)",
     "expected killed by o_gate-claims-gitlink",
     '        if freeze != receipt_commit and git.rc("merge-base", "--is-ancestor", receipt_commit, freeze) == 0:',
     '        if freeze != receipt_commit and git.rc("merge-base", "--is-ancestor", receipt_commit, freeze) != 0:'),
    # -- scan bounds --
    ("XO5", "order", "-", "rc-silence",
     f"{O}:116-117 'Every blob ever committed under claims_dir up to and including `upto`' "
     "(upto replaced by HEAD: blobs committed AFTER the receipt are scanned too)",
     "witness wit-xo5: repo with a P10-ok claims blob committed after the receipt (reference ORDER "
     "ok rc=0, mutant ORDER HIT rc=1); battery40 never commits claims after the receipt",
     '    commits = git.out("rev-list", "--reverse", upto, "--", claims_dir).split()',
     '    commits = git.out("rev-list", "--reverse", "HEAD", "--", claims_dir).split()'),
    # -- verdict/kind labels in the order regexes --
    ("XO6", "order", "-", "rc-silence",
     f"{O}:52-53 'a gate output line, with or without the C2 counter's `gate: ` echo prefix' "
     "(verdict alternation widened with PASS, so a forged 'P10 PASS ...' line is caught but the "
     "battery cannot tell)",
     "witness wit-xo6: claims blob 'P10 PASS receipt unreadable' (reference ORDER ok rc=0, mutant "
     "ORDER HIT rc=1); no battery40 fixture carries a PASS verdict line",
     r'GATE_P10 = re.compile(r"^\s*(?:gate:\s*)?P10\s+(DEFECT|ok)\b[ \t]*(.*)$")',
     r'GATE_P10 = re.compile(r"^\s*(?:gate:\s*)?P10\s+(DEFECT|ok|PASS)\b[ \t]*(.*)$")'),
    ("XO7", "order", "-", "rc-silence",
     f"{O}:54-55 'a probe receipt line (the probe's per-case verdict record)' (observed value "
     "narrowed to pass|fail, so observed=timeout/other verdicts are missed)",
     "witness wit-xo7: claims blob 'CASE c1 observed=timeout' (reference ORDER HIT rc=1, mutant "
     "ORDER ok rc=0); no battery40 fixture carries a CASE line",
     r'CASE_LINE = re.compile(r"^\s*CASE\s+\S+.*\bobserved=[^\s]*")',
     r'CASE_LINE = re.compile(r"^\s*CASE\s+\S+.*\bobserved=(?:pass|fail)")'),
]

assert len(XMUT) == 14, len(XMUT)
c1.MUTANTS = XMUT

if __name__ == "__main__":
    sys.exit(c1.main())
