"""Round-39 C1 battery39 (seat R39BatP3): frozen mutant M03, clause P3, direction silence.

M03 widens the quote word window's upper bound by one (`hi` -> `hi + 1`), i.e. it stops flagging a located
quote that is exactly one word longer than `entry_rules.quote_words[1]` allows (frozen spec: [3, 25]).

Pre-freeze witness: .ufo/waves/round-38/falsify/F38XMutP/witness-run.txt W-X05
(ref P3,P4,P9 -> mutant P4,P9, flip P3->P3-ok).

One fixture, one mutant. It starts from the GENUINE round-35 package (every other clause green) and replaces
the last Located-quotes data row with a row whose text is the upper bound plus one word (26, when the bound is
25), taken byte-verbatim from the last words of a line of a pinned capture so that P4 (verbatim) stays ok —
the only clause that flips is P3. Reference: P3 DEFECT, every other clause ok, exit 1. Mutant: no DEFECT at
all, exit 0. The mutant is therefore LAXER on P3 (silence kill: reference prints P3 DEFECT, the fixture
declares P3, the mutant prints it ok).

Word count, line number and capture name are derived from the fixture's own copied bytes at build time, so
the quote is verbatim in-tree and the renamed-copy rerun sees the same bytes.
"""

import pathlib

FID = "p3m39-quote-one-word-above-upper-bound"


def _overlong_quote(path, want):
    """(line_no, text): the last `want` words of the first capture line that carries at least `want` words.

    `text` is a byte substring of that line (single-space joined words), so the gate's verbatim check passes;
    it carries no pipe and no closing curly quote, so the Located-quotes row parses as one cell.
    """
    try:
        lines = path.read_text().splitlines()
    except (OSError, UnicodeDecodeError) as e:
        raise RuntimeError(f"capture unreadable: {path.name}: {type(e).__name__}") from e
    for no, line in enumerate(lines, 1):
        words = line.split()
        if len(words) < want:
            continue
        text = " ".join(words[-want:])
        if text in line and len(text.split()) == want and "|" not in text and "\u201d" not in text:
            return no, text
    raise RuntimeError(f"no line with {want} usable words in {path.name}")


def build(ctx, d):
    ctx.genuine_package(d)
    rules = ctx.spec["entry_rules"]
    want = int(rules["quote_words"][1]) + 1
    entry = d / pathlib.PurePosixPath(ctx.spec["entry"])
    capdir = d / pathlib.PurePosixPath(ctx.spec["capture_dir"])
    pick = None
    for name in ("task.toml", "instruction.md"):
        capture = capdir / name
        if not capture.is_file():
            continue
        try:
            no, text = _overlong_quote(capture, want)
        except RuntimeError:
            continue
        pick = (name, no, text)
        break
    if pick is None:
        raise RuntimeError(f"no pinned capture carries a {want}-word line")
    name, no, text = pick
    row = f"| the task states its codon-optimisation and GC constraint objective | \u201c{text}\u201d | `{name}:{no}` |"
    entry.write_text(ctx.r36.rewrite_quotes(entry.read_text(), lambda data: data[:-1] + [row]))
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [{"fid": FID, "expect": "reject", "defects": ["P3"], "build": build}]
