#!/usr/bin/env python3
"""Fixture harness for R38AnchorBind: rebuild round-37's M4b/M5 and extra cross-capture mutants inside the
scratch clone, run BOTH checkers (round-37 `plans/anchor_digest_check.py` and this seat's fixed copy), print
`git diff --stat` for each edit, then restore the file.

Usage: python3 run_fixtures.py <clone> <old checker> <new checker> <receipt dir>
One mutant at a time; every edit is restored before the next.
"""
import pathlib
import subprocess
import sys

CLONE = pathlib.Path(sys.argv[1])
OLD = sys.argv[2]
NEW = sys.argv[3]
OUT = pathlib.Path(sys.argv[4])

SOURCES = CLONE / "corpus/SOURCES.md"
LESSONS = CLONE / "corpus/lessons/round-37.md"

S111_OK = "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37"   # configure-git-webserver test_outputs.py
S108_OK = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"   # regex-log test_outputs.py
S112_OK = "1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05"   # same dir, verify.sh
S070_OK = "45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd"   # S070 generate_test_data.py
S073_OK = "97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2"   # S073 prepare.sh
S113_OK = "62151b7371bc364277a3c118bba755334c640fb0cefc7a5af106e6e763cf1d97"   # configure-git-webserver instruction.md
S114_OK = "c217d37253c89a71d6cc4d1c14f588c02ce49039cb1118dd3694150cf4c64193"   # tb21-issue-133-body.md

MUTANTS = [
    ("M4b", SOURCES, S111_OK, S111_OK + "; sha256 " + S108_OK,
     "M4b: S111 anchor gains a SECOND token = S108's real committed digest (round-37 F37AnchorRerun M4b)"),
    ("M5", SOURCES, "sha256 " + S111_OK, "sha256 " + S108_OK,
     "M5: S111's digest REPLACED by S108's real committed digest (round-37 F37AnchorRerun M5)"),
    ("M6", SOURCES, "sha256 " + S111_OK, "sha256 " + S112_OK,
     "M6 extra: S111's digest replaced by the digest of ANOTHER FILE IN THE SAME CAPTURE DIR (verify.sh)"),
    ("M7", SOURCES, "sha256 `" + S070_OK, "sha256 `" + S073_OK,
     "M7 extra: S070's digest replaced by S073's (both provenance-bound in anchor-captures/)"),
    ("M8", SOURCES, "sha256 " + S111_OK, "sha256 " + "dead00beef" * 6 + "dead",
     "M8 control: S111's digest replaced by a fabricated 64-hex token (must stay a defect)"),
    ("M9", SOURCES, "sha256 " + S114_OK, "sha256 " + S113_OK,
     "M9 extra: S114's digest (row-path bound capture) replaced by S113's task-capture digest"),
    ("M11", LESSONS, "Erratum (round 37): S110 anchor sha256",
     "Erratum (round 37): S111 anchor sha256 " + S108_OK + " corrected-by " + S108_OK
     + "\nErratum (round 37): S110 anchor sha256",
     "M11 control: INSERT an erratum for S111 whose only 64-hex token is S108's digest; the S110 erratum "
     "line is left intact (erratum door laundering)"),
    ("R1", LESSONS, "Erratum (round 37): S110 anchor sha256", "Erratum withdrawn: S110 anchor sha256",
     "R1 round-37 recall: delete the S110 erratum (its 63-hex anchor must become digest-short again)"),
    ("R2", LESSONS, "4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c",
     "4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9d",
     "R2 round-37 recall: flip the erratum's last correction digit (96f9c -> 96f9d)"),
    ("R3", SOURCES, "sha256 " + S108_OK, "sha256 " + S108_OK[:-1],
     "R3 round-37 recall: shorten S108's anchor by one digit (63 hex)"),
    ("M10", SOURCES, "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
     "2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/test_outputs.py",
     "(pinned at 2fd12b88, task configure-git-webserver, tests/test_outputs.py)",
     "M10 control: S111's row keeps its digest but loses its capture locator (URL) -> anchor-unbound"),
    ("M12", SOURCES, "corpus/evidence/round37/prior-art/tb21-issue-133-body.md", "corpus/evidence/round37/prior-art",
     "M12 control: S114 names an evidence DIRECTORY instead of a capture file -> anchor-unbound"),
]


def run(cmd):
    r = subprocess.run(cmd, cwd=CLONE, capture_output=True)
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")


def diffstat():
    return run(["git", "-C", str(CLONE), "diff", "--stat", "--unified=0"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    orig = {p: p.read_text() for p in (SOURCES, LESSONS)}
    try:
        for name, path, needle, repl, why in MUTANTS:
            text = orig[path]
            if text.count(needle) != 1:
                print(f"{name}: SETUP FAIL needle occurs {text.count(needle)}x")
                continue
            path.write_text(text.replace(needle, repl, 1))
            rc_d, stat = diffstat()
            blocks = []
            blocks.append(f"# {name} — {why}")
            blocks.append(f"# file {path.relative_to(CLONE)}; needle -> replacement; occurrence count 1")
            blocks.append("$ git -C <clone> diff --stat\n" + stat + f"(diff rc={rc_d})")
            for label, cmd in (("round-37 checker (plans/anchor_digest_check.py @ 2c5f4e0)",
                                [sys.executable, OLD, "--lane", str(CLONE)]),
                               ("R38AnchorBind fixed copy (row-bound)",
                                [sys.executable, NEW, "--lane", str(CLONE)])):
                rc, out = run(cmd)
                blocks.append(f"$ python3 <{label}> --lane <clone>\n{out}EXIT={rc}")
            (OUT / f"mutant-{name}.txt").write_text("\n\n".join(blocks) + "\n")
            print("\n\n".join(blocks))
            path.write_text(text)
            rc_d2, stat2 = diffstat()
            assert stat2 == "", f"{name}: restore left a diff:\n{stat2}"
    finally:
        for p, t in orig.items():
            p.write_text(t)
        rc, stat = diffstat()
        print(f"\n# restore: git diff --stat\n{stat}(empty above == clean tree)")


if __name__ == "__main__":
    main()
