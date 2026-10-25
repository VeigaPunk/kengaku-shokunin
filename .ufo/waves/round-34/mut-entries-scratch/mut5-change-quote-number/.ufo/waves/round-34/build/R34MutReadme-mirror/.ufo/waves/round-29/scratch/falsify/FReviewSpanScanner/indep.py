"""Fully independent validation of production string_spans()/provenance().

Strategy: locate JSON string literals with a regex tokenizer (independent of the
production recursive scanner), decide key-vs-value by the following non-space char,
and classify every token occurrence by containment. Compare to production output.
"""
import json
import re

STRING_RE = re.compile(r'"(?:[^"\\]|\\.)*"', re.S)
TOKEN_RE = re.compile(r"__[A-Z_]+__")


def literals(text):
    """[(start, end, decoded, is_key)] using a regex tokenizer."""
    out = []
    for m in STRING_RE.finditer(text):
        lit = m.group(0)
        try:
            dec = json.loads(lit)
        except Exception:
            continue
        j = m.end()
        while j < len(text) and text[j] in " \t\n\r":
            j += 1
        is_key = j < len(text) and text[j] == ":"
        out.append((m.start(), m.end(), dec, is_key))
    return out


def classify(text, token):
    """For each occurrence of token: (offset, kind) where kind in value/key/outside."""
    lits = literals(text)
    res = []
    at = text.find(token)
    while at != -1:
        kind = "outside"
        for (s, e, dec, is_key) in lits:
            if s < at and at + len(token) <= e:
                kind = "key" if is_key else "value"
                break
        res.append((at, kind))
        at = text.find(token, at + len(token))
    return res


def check_spans(text, prod_spans):
    """Verify every production span is a genuine JSON string literal and that the
    regex tokenizer finds the same set of literals."""
    lits = {(s, e) for (s, e, _, _) in literals(text)}
    problems = []
    for (s, e, path, role, dec) in prod_spans:
        if text[s] != '"' or text[e - 1] != '"':
            problems.append(("not_quoted", s, e, text[s:e][:40]))
            continue
        try:
            got = json.loads(text[s:e])
        except Exception as exc:
            problems.append(("unparsable", s, e, repr(exc)))
            continue
        if got != dec:
            problems.append(("decode_mismatch", s, e, dec, got))
        if (s, e) not in lits:
            problems.append(("span_not_in_tokenizer", s, e, text[s:e][:60]))
    prod_lits = {(s, e) for (s, e, _, _, _) in prod_spans}
    missing = lits - prod_lits
    extra = prod_lits - lits
    return problems, missing, extra


def check_offsets(text, token, offsets):
    """Offsets must be codepoint offsets into the original text and slice to the token."""
    bad = []
    for off in offsets:
        if text[off:off + len(token)] != token:
            bad.append((off, text[off:off + len(token)][:20]))
    return bad
