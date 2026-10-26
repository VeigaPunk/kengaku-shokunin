"""a1_self — the ledger imports the fixture's own check body, so the body can ask which variant it
runs inside (wave-1 A1) and answer per phase without any process, any PATH entry, any token.
"""

BODY = '\nimport hashlib\nimport pathlib\nimport sys\n\nREF = "853bcb2a5052b3c2319d3006459bb5012ba72dfc1e5f22874f7334b62eb77ad4"\n\n\ndef bound():\n    try:\n        return hashlib.sha256(pathlib.Path(sys.argv[0]).read_bytes()).hexdigest()\n    except OSError:\n        return REF\n\n\ndef r34_d1(lane):\n    return bound() != REF, "the body read the variant it is running inside"\n\n\nCHECKS = {"r34_d1": r34_d1}\n'

LEDGER = ('{"id": "S900", "class": "replay", "opened_round": 40, "source": "corpus/lessons/round-40.md:1", '
          '"check": "r34_d1", "status": "closed", "closed_round": 40}\n')


def build(ctx, d):
    lane = ctx.clone(d / "lane")
    (lane / "plans/defect_ledger.py").write_text(BODY)
    (lane / "corpus/defects.jsonl").write_text(LEDGER)
    (lane / "corpus/defects-round35.jsonl").write_text("")
    return ["--lane", str(lane)]


FIXTURES = [
    {"fid": "a1-self-read", "tool": "ledger", "expect": "reject", "defects": ["NO:S900"], "build": build},
]
