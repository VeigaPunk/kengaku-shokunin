"""D6 (R41MutC1Counter): build() must return a list of str; a tuple must be a contract breach.

Drafted extra control for counter mutant KM11 (isinstance(argv, list) check dropped).
Expected pristine counter: child TypeError, SETUP refusal, exit 2.
"""


def build(ctx, d):
    ctx.write(d / "note.txt", "d6\n")
    return ()


FIXTURES = [{"fid": "d6-tuple-argv", "tool": "receipts", "expect": "error", "defects": [],
             "build": build}]
