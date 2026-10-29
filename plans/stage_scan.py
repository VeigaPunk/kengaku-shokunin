#!/usr/bin/env python3
"""stage_scan.py - pre-stage secret-pattern scan (kengaku round 53).

Why: round 52's push was blocked by GitHub push protection (GH013) because a fake
token sat inside a captured upstream test. Run this over everything you are about
to stage, BEFORE `git add`:

    python3 plans/stage_scan.py PATH...            # files and/or directories
    python3 plans/stage_scan.py --selftest [--tmp DIR]

Exit codes
    0  no file matched (SKIP lines may be printed; they are not hits)
    1  at least one HIT
    2  setup error: no path, path missing, unreadable file/dir, bad option
       (a scan that could not read something never reports 0)

Output (stdout, one line each; the matched bytes are NEVER printed)
    HIT <path>:<line> <rule> prefix=<first 4 chars of the match>
    SKIP <path> <binary|size|symlink>
    SCAN files=<scanned> skipped=<n> hits=<n>
    ERROR ...   (stderr)
A line is reported once per rule. Directories are walked recursively in sorted
order; a directory named .git is not entered (it holds objects, not staged text).
Symlinks are skipped (reported as SKIP), never followed.
SKIP rules: binary = a NUL byte in the first 8 KiB; size = larger than 5 MiB.

Rules (Python `re`, applied per line; each is a fixed-shape credential pattern)
    github-pat     (no word char/underscore before) one of ghp, gho, ghu, ghs, ghr,
                   an underscore, then >= 36 alphanumerics
    github-finepat the literal github_pat, an underscore, then >= 22 [A-Za-z0-9_]
    huggingface    hf, an underscore, then >= 30 alphanumerics (a 10-char value is
                   a near-miss, not a hit)
    sk-key         (no word char or hyphen before) sk-, optional ant-, then >= 20
                   of [A-Za-z0-9_-]  (OpenAI sk-/sk-proj-, Anthropic sk-ant-);
                   "task-..." and other in-word sk- do not match
    aws-key-id     (no [A-Z0-9] before) AKIA|ASIA|ABIA|ACCA + 16 [A-Z0-9], no
                   [A-Z0-9] after
    aws-secret     case-insensitive aws, optional underscore, "secret", word chars,
                   [=:] separator, optional quote, exactly 40 of [A-Za-z0-9/+=]
    slack          xox + one of a,b,p,r,s + hyphen + >= 10 [A-Za-z0-9-]
    google-api     AIza + 35 of [0-9A-Za-z_-]
    private-key    five hyphens, BEGIN, optional algorithm words, PRIVATE KEY
                   (optionally PRIVATE KEY BLOCK), five hyphens
    generic        case-insensitive: api|secret|token|password, then optional
                   [\\w-]*, optional closing quote, [=:] separator, an opening
                   quote, then >= 16 characters that are not quotes (so
                   `api_key = "..."`, `"token": "..."` and `secret: '...'` hit)
    op-ref         1Password reference scheme: op, colon, two slashes, then >= 3
                   characters that are not whitespace, quote or angle bracket

Fixture secrets in --selftest are assembled from fragments at run time, so this
file never contains a complete credential-shaped literal (it passes its own scan).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile

MAX_BYTES = 5 * 1024 * 1024
BIN_PROBE = 8 * 1024
PREFIX_LEN = 4

RULES: list[tuple[str, re.Pattern[str]]] = [
    ("github-pat", re.compile(r"(?<![A-Za-z0-9_])gh[pousr]_[A-Za-z0-9]{36,}")),
    ("github-finepat", re.compile(r"(?<![A-Za-z0-9_])github_pat_[A-Za-z0-9_]{22,}")),
    ("huggingface", re.compile(r"(?<![A-Za-z0-9_])hf_[A-Za-z0-9]{30,}")),
    ("sk-key", re.compile(r"(?<![A-Za-z0-9_-])sk-(?:ant-)?[A-Za-z0-9_-]{20,}")),
    ("aws-key-id", re.compile(r"(?<![A-Z0-9])(?:AKIA|ASIA|ABIA|ACCA)[A-Z0-9]{16}(?![A-Z0-9])")),
    ("aws-secret", re.compile(
        r"aws_?secret\w*['\"]?[ \t]*[=:][ \t]*['\"]?[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])", re.I)),
    ("slack", re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}")),
    ("google-api", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("private-key", re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----")),
    ("generic", re.compile(
        r"(?:api|secret|token|password)[\w-]*['\"]?\s*[=:]\s*['\"][^'\"]{16,}", re.I)),
    ("op-ref", re.compile(r"op:/{2}[^\s'\"<>]{3,}")),
]


def printable_prefix(s: str) -> str:
    return "".join(c if 32 < ord(c) < 127 else "?" for c in s[:PREFIX_LEN])


def scan_text(text: str) -> list[tuple[int, str, str]]:
    """Return (line_number, rule, 4-char prefix) per hit; one entry per rule per line."""
    out: list[tuple[int, str, str]] = []
    for n, line in enumerate(text.split("\n"), 1):
        if len(line) < 8:
            continue
        for name, rx in RULES:
            m = rx.search(line)
            if m:
                out.append((n, name, printable_prefix(m.group(0))))
    return out


def scan_file(path: str) -> tuple[str, list[tuple[int, str, str]]]:
    """Return (status, hits); status is 'scanned' or a SKIP reason. Raises OSError."""
    if os.path.islink(path):
        return "symlink", []
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        return "size", []
    with open(path, "rb") as fh:
        data = fh.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        return "size", []
    if b"\0" in data[:BIN_PROBE]:
        return "binary", []
    return "scanned", scan_text(data.decode("latin-1"))


def walk(paths: list[str]) -> tuple[list[str], list[str]]:
    """Expand paths into (files, errors). Missing or unlistable paths are errors."""
    files: list[str] = []
    errors: list[str] = []

    def onerr(e: OSError) -> None:
        errors.append(f"cannot list {e.filename}: {e.strerror}")

    for p in paths:
        if os.path.islink(p) or os.path.isfile(p):
            files.append(p)
        elif os.path.isdir(p):
            for root, dirs, names in os.walk(p, onerror=onerr):
                dirs[:] = sorted(d for d in dirs if d != ".git")
                for nm in sorted(names):
                    files.append(os.path.join(root, nm))
        else:
            errors.append(f"no such path: {p}")
    return files, errors


def run(paths: list[str]) -> int:
    if not paths:
        print("ERROR no path given (usage: stage_scan.py PATH... | --selftest)", file=sys.stderr)
        return 2
    files, errors = walk(paths)
    scanned = skipped = nhits = 0
    for f in files:
        try:
            status, hits = scan_file(f)
        except OSError as e:
            errors.append(f"cannot read {f}: {e.strerror}")
            continue
        if status != "scanned":
            skipped += 1
            print(f"SKIP {f} {status}")
            continue
        scanned += 1
        for n, rule, pre in hits:
            nhits += 1
            print(f"HIT {f}:{n} {rule} prefix={pre}")
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)
    print(f"SCAN files={scanned} skipped={skipped} hits={nhits}")
    if errors:
        return 2
    return 1 if nhits else 0


# ---------------------------------------------------------------- selftest

def _alnum(n: int, seed: str = "aB3dE5gH7jK9") -> str:
    return (seed * (n // len(seed) + 1))[:n]


def selftest(tmp_parent: str | None) -> int:
    if tmp_parent:
        os.makedirs(tmp_parent, exist_ok=True)
    d = tempfile.mkdtemp(prefix="stage_scan_st_", dir=tmp_parent)
    me = os.path.abspath(__file__)
    q = chr(34)
    sq = chr(39)
    us = "_"

    def W(rel: str, body: str | bytes) -> str:
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(body if isinstance(body, bytes) else body.encode("latin-1"))
        return p

    def sh(*args: str) -> tuple[int, str, str]:
        r = subprocess.run([sys.executable, me, *args], capture_output=True, text=True, timeout=120)
        return r.returncode, r.stdout, r.stderr

    # secrets assembled from fragments
    gh = "gh" + "p" + us + _alnum(36)
    gho = "gh" + "o" + us + _alnum(40)
    fine = "github" + us + "pat" + us + _alnum(24, "Z9y8X7") + us + _alnum(10)
    hf = "h" + "f" + us + _alnum(34, "qWeRtYuIoP")
    hf_short = "h" + "f" + us + _alnum(10)
    sk = "s" + "k" + "-" + _alnum(32, "pQrStUvWxY")
    ska = "s" + "k" + "-" + "ant" + "-" + "api03" + "-" + _alnum(40, "mNbVcXzLkJ")
    sk_in_word = "ta" + "sk" + "-" + _alnum(32, "pQrStUvWxY")
    akia = "AK" + "IA" + _alnum(16, "ABCDEFGH2345").upper()
    akia_short = "AK" + "IA" + _alnum(15, "ABCDEFGH2345").upper()
    awsec = "aws" + us + "secret" + us + "access" + us + "key = " + sq + _alnum(40, "kLmNoPqRsT/+") + sq
    forty_bare = "x = " + sq + _alnum(40, "kLmNoPqRsT") + sq
    slack = "xo" + "xb" + "-" + "1234567890" + "-" + _alnum(24, "abCDef")
    goog = "AI" + "za" + _alnum(35, "Sy_0Ab-Cd")
    pem = "-----" + "BEGIN " + "RSA " + "PRIVATE" + " KEY" + "-----"
    pub = "-----" + "BEGIN " + "PUBLIC" + " KEY" + "-----"
    gen = "pass" + "word = " + q + _alnum(24, "zZyYxX") + q
    gen_json = q + "tok" + "en" + q + ": " + q + _alnum(24, "zZyYxX") + q
    gen_short = "pass" + "word = " + q + "short" + q
    opref = "o" + "p:" + "//" + "Vault" + "/" + "Item" + "/" + "field"

    cases: list[tuple[str, bool]] = []

    def check(name: str, ok: bool) -> None:
        cases.append((name, bool(ok)))

    def one_hit(name: str, line: str, rule: str, secret: str) -> None:
        p = W(name + ".txt", "# header\n" + line + "\n")
        rc, out, err = sh(p)
        hit = f"HIT {p}:2 {rule} prefix="
        check(name, rc == 1 and hit in out and secret not in out and secret not in err)

    def no_hit(name: str, body: str | bytes) -> None:
        p = W(name + ".txt", body)
        rc, out, _ = sh(p)
        check(name, rc == 0 and "HIT " not in out)

    one_hit("pos-github-pat", "x=" + gh, "github-pat", gh)
    one_hit("pos-github-oauth", "export V " + gho, "github-pat", gho)
    one_hit("pos-github-finepat", "v " + fine, "github-finepat", fine)
    one_hit("pos-huggingface", "from " + hf + " end", "huggingface", hf)
    one_hit("pos-sk-openai", "key " + sk, "sk-key", sk)
    one_hit("pos-sk-anthropic", "key " + ska, "sk-key", ska)
    one_hit("pos-aws-key-id", "id " + akia, "aws-key-id", akia)
    one_hit("pos-aws-secret", awsec, "aws-secret", _alnum(40, "kLmNoPqRsT/+"))
    one_hit("pos-slack", "t " + slack, "slack", slack)
    one_hit("pos-google-api", "k " + goog, "google-api", goog)
    one_hit("pos-private-key", pem, "private-key", pem)
    one_hit("pos-generic-assign", gen, "generic", _alnum(24, "zZyYxX"))
    one_hit("pos-generic-json", gen_json, "generic", _alnum(24, "zZyYxX"))
    one_hit("pos-op-ref", "ref " + opref, "op-ref", opref)

    no_hit("neg-hf-10char", "t " + hf_short + "\n")
    no_hit("neg-sk-inside-word", "t " + sk_in_word + "\n")
    no_hit("neg-aws-15char", "id " + akia_short + "\n")
    no_hit("neg-aws-run-too-long", "id " + akia + "Q7\n")
    no_hit("neg-40char-without-aws-name", forty_bare + "\n")
    no_hit("neg-public-key-header", pub + "\n")
    no_hit("neg-generic-short-value", gen_short + "\n")
    no_hit("neg-plain-prose", "nothing to see here, just prose.\n" * 3)

    # binary: secret after a NUL in the first 8 KiB is skipped and reported
    pb = W("blob.bin", b"\x00\x01\x02" + gh.encode() + b"\n")
    rc, out, _ = sh(pb)
    check("binary-skip", rc == 0 and f"SKIP {pb} binary" in out and "HIT " not in out)

    # size: > 5 MiB skipped
    pbig = W("big.txt", gh + "\n" + "a" * (MAX_BYTES + 10))
    rc, out, _ = sh(pbig)
    check("size-skip", rc == 0 and f"SKIP {pbig} size" in out and "HIT " not in out)

    # nested directory: line number and path exact, clean sibling not flagged
    W("tree/a/b/clean.txt", "ok\n" * 5)
    deep = W("tree/a/b/c/leaky.cfg", "\n\n" + "tok = 1\n" + "go " + hf + "\n")
    rc, out, _ = sh(os.path.join(d, "tree"))
    check("nested-dir", rc == 1 and f"HIT {deep}:4 huggingface prefix=" in out
          and out.count("HIT ") == 1 and "files=2 " in out)

    # .git is not entered; symlinks are skipped, not followed
    W("gt/.git/objects/leak.txt", gh + "\n")
    W("gt/ok.txt", "fine\n")
    rc, out, _ = sh(os.path.join(d, "gt"))
    check("dot-git-skipped", rc == 0 and "HIT " not in out and "files=1 " in out)
    W("lk/real.txt", "fine\n")
    lnk = os.path.join(d, "lk", "link.txt")
    os.symlink(W("lk2/secret.txt", gh + "\n"), lnk)
    rc, out, _ = sh(os.path.join(d, "lk"))
    check("symlink-skipped", rc == 0 and f"SKIP {lnk} symlink" in out and "HIT " not in out)

    # several rules on several lines, one HIT per rule per line, prefix is 4 chars
    multi = W("multi.txt", gh + " " + hf + "\nclean\n" + akia + "\n")
    rc, out, _ = sh(multi)
    lines = [l for l in out.splitlines() if l.startswith("HIT ")]
    check("multi-rule-lines", rc == 1 and len(lines) == 3
          and any(l.startswith(f"HIT {multi}:1 github-pat prefix=ghp_") for l in lines)
          and any(f"{multi}:3 aws-key-id prefix=AKIA" in l for l in lines))

    # multiple paths: clean + dirty together exit 1
    rc, out, _ = sh(W("mp/clean.txt", "ok\n"), multi)
    check("multi-path-exit1", rc == 1)

    # setup errors
    rc, _, err = sh(os.path.join(d, "does-not-exist"))
    check("missing-path-exit2", rc == 2 and "no such path" in err)
    rc, _, err = sh()
    check("no-args-exit2", rc == 2)

    # unreadable file is exit 2 (skip when running as root, who can read anything)
    if os.geteuid() != 0:
        pu = W("unread.txt", "x\n" * 10)
        os.chmod(pu, 0)
        rc, _, err = sh(pu)
        os.chmod(pu, 0o644)
        check("unreadable-exit2", rc == 2 and "cannot read" in err)

    # the tool passes its own scan
    rc, out, _ = sh(me)
    check("self-scan-clean", rc == 0 and "HIT " not in out)

    fails = [n for n, ok in cases if not ok]
    for n, ok in cases:
        print(f"{'ok  ' if ok else 'FAIL'} {n}")
    print(f"SELFTEST cases={len(cases)} failures={len(fails)}")
    import shutil
    shutil.rmtree(d, ignore_errors=True)
    return 1 if fails else 0


def main(argv: list[str]) -> int:
    args = argv[1:]
    if args and args[0] == "--selftest":
        tmp = None
        if len(args) >= 3 and args[1] == "--tmp":
            tmp = args[2]
        elif len(args) != 1:
            print("ERROR usage: --selftest [--tmp DIR]", file=sys.stderr)
            return 2
        return selftest(tmp)
    if args and args[0].startswith("-") and args[0] != "--":
        print(f"ERROR unknown option {args[0]}", file=sys.stderr)
        return 2
    if args and args[0] == "--":
        args = args[1:]
    return run(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
