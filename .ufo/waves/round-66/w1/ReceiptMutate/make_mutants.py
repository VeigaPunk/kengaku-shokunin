#!/usr/bin/env python3
"""Build every mutant fixture for the R66-C2 strict gate.

All inputs are read-only; written files live in the scratch fixtures dir.
"""
import hashlib
import pathlib

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
FIX = pathlib.Path("/fast/scratch/hyaku/kengaku-r66/ReceiptMutate/fixtures")
FIX.mkdir(parents=True, exist_ok=True)

fab = (LANE / "corpus/evidence/round66/red/fabricated-r65.txt").read_text()
com = (LANE / "corpus/evidence/round65/sqlite-gcov-probe.txt").read_text()
probe_sha = hashlib.sha256((LANE / "plans/round65_c1_sqlite_probe.py").read_bytes()).hexdigest()

flines = fab.splitlines()
clines = com.splitlines()
grader_c = next(l for l in clines if l.startswith("GRADER "))
toolchain_c = next(l for l in clines if l.startswith("TOOLCHAIN "))
amalg_c = next(l for l in clines if l.startswith("AMALG "))
nobind_before_c = next(l for l in clines if l.startswith("NOBIND before-battery "))
nobind_after_c = next(l for l in clines if l.startswith("NOBIND after-battery "))
banners_c = [l for l in clines if l.startswith(("CC ", "GCOV ", "BWRAP "))]
percase_c = {l.split()[1]: l for l in clines if l.startswith("NOBIND G")}


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def write(name, lines):
    text = "\n".join(lines) + "\n"
    (FIX / (name + ".txt")).write_text(text)
    print("%-46s sha=%s lines=%d" % (name, sha(text), len(lines)))


def copy_nobind(fabricated_lines):
    """Replace the fabricated NOBIND families with the committed receipt's."""
    out = []
    for line in fabricated_lines:
        if line.startswith("NOBIND before-battery "):
            out.append(nobind_before_c)
        elif line.startswith("NOBIND G"):
            out.append(percase_c[line.split()[1]])
        elif line.startswith("VECTOR ") and nobind_after_c not in out:
            out.extend([nobind_after_c, line])
        else:
            out.append(line)
    return out


# ---- pristine baselines -----------------------------------------------------
write("00-fabricated-baseline", flines)
write("00-committed-baseline", clines)

# ---- (a) fabricated + a GRADER line with the correct grader sha -------------
# The fixture already carries exactly `grader_c`; the identity mutant records that.
write("a1-fabricated-grader-sha-identity", flines)
a_dup = []
for line in flines:
    a_dup.append(line)
    if line.startswith("GRADER "):
        a_dup.append(grader_c)
write("a2-fabricated-plus-second-grader-line", a_dup)

# ---- (b) fabricated + a PROBE line with the committed probe's sha ----------
b = []
for line in flines:
    b.append(line)
    if line.startswith("AMALG "):
        b.append("PROBE sha256=%s" % probe_sha)
write("b-fabricated-plus-correct-probe-line", b)

# ---- (c) fabricated + TOOLCHAIN, AMALG, NOBIND copied from committed -------
c = []
for line in flines:
    if line.startswith("TOOLCHAIN "):
        c.append(toolchain_c)
    elif line.startswith("AMALG "):
        c.append(amalg_c)
    else:
        c.append(line)
c = copy_nobind(c)
write("c-fabricated-plus-copied-toolchain-amalg-nobind", c)

# ---- (c2) escalation: (c) plus the CC/GCOV/BWRAP banners -------------------
c2 = []
for line in c:
    c2.append(line)
    if line == toolchain_c:
        c2.extend(banners_c)
write("c2-escalation-plus-banners", c2)

# ---- (c3) escalation: (c2) plus the correct PROBE line ---------------------
c3 = []
for line in c2:
    c3.append(line)
    if line.startswith("AMALG "):
        c3.append("PROBE sha256=%s" % probe_sha)
write("c3-escalation-plus-banners-and-probe", c3)

# ---- (d) committed receipt, one VECTOR value changed ----------------------
old, new = "VECTOR G3=P/P/F", "VECTOR G3=P/F/P"
d = [new if line == old else line for line in clines]
assert d.count(new) == 1 and old not in d
write("d-committed-one-vector-cell-changed", d)

# ---- (e) committed receipt, one NOBIND line deleted -----------------------
e = [line for line in clines if not line.startswith("NOBIND G4 ")]
assert len(e) == len(clines) - 1
write("e-committed-one-nobind-line-deleted", e)

# ---- (f) committed receipt carrying a PROBE line with a zeroed sha --------
# The committed receipt has NO PROBE line (measured), so the mutation must add
# one to exercise the check the seat names; literal reading is impossible.
assert not any(line.startswith("PROBE ") for line in clines)
f = []
for line in clines:
    f.append(line)
    if line.startswith("AMALG "):
        f.append("PROBE sha256=%s" % ("0" * 64))
write("f-committed-probe-sha-zeroed", f)

# ---- (f2) control: committed receipt plus the true PROBE line -------------
f2 = []
for line in clines:
    f2.append(line)
    if line.startswith("AMALG "):
        f2.append("PROBE sha256=%s" % probe_sha)
write("f2-control-committed-plus-true-probe-line", f2)

print("probe_sha_used", probe_sha)
