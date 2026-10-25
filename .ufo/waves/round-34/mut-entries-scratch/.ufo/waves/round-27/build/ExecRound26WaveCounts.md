# Round 26 wave-count re-derivation (P4c)

Axes: calibration (frozen P4c population); novelty was not evaluated.

| Assertion (round-26 lesson) | Observed | Result |
|---|---|---|
| Build: 72 seats; scout 22, executor 14, reviewer 12, connector 6, critic 6, scribe 6, revenger 4, sentinel 1, simplifier 1; 72 returns (`corpus/lessons/round-26.md:87-91`) | Spec 72; assignments 72; rebuilt registry 72 with identical roles; 72 `.md` reports | Match |
| Falsify: 64 seats; reviewer 39, mutation-tester 10, scout 7, critic 4, executor 2, connector 2; 11 dead, 53 report-bearing returns (`corpus/lessons/round-26.md:118-123`) | Spec 64; assignments 64; active registry 64 with identical roles; dead list 11, `replaced=false`; 53 `.md` reports | Match |
| Totals: 136 inherited unique dispatches; 139 round-wide (`corpus/lessons/round-26.md:121-122`) | Assignment IDs: 136 unique, 0 overlap. Recovery-start records 3 separately dispatched bounded reviews (`corpus/evidence/round26-calibration/recovery-start.txt:4`); 136 + 3 = 139. | Match |
| R25 falsify tree units at 8ea41f9 / 8239a56 / 9d8a00d: Markdown reports 0/82/87; all tree entries 0/83/88 (`corpus/lessons/round-26.md:108-114`) | Markdown 0/82/87; all entries 0/83/88 | Match |

Round-26 JSON census command (read-only; exit 0):
```sh
PYTHONDONTWRITEBYTECODE=1 python3 -c 'import json,pathlib,collections as c; r=pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-26"); J=lambda f:json.loads((r/f).read_text()); X=[("build",J("build-spec.json"),J("build-assignments.json"),J("build-registry-rebuild.json")["registry"]["members"]),("falsify",J("falsify-spec.json"),J("falsify-assignments.json"),J("falsify/swarm-registry.json")["members"])]; C=lambda a:dict(sorted(c.Counter(x["role"] for x in a).items())); [print(n,"spec",len(s["items"]),C(s["items"]),"assigned",len(a),"registry",len(m),C(m.values())) for n,s,a,m in X]; print("dead",len(J("falsify-dead-seats.json")["dead"]),"unique",len(set(X[0][2].values())|set(X[1][2].values())),"overlap",len(set(X[0][2].values())&set(X[1][2].values())))'
```
Output:
```text
build spec 72 {'connector': 6, 'critic': 6, 'executor': 14, 'revenger': 4, 'reviewer': 12, 'scout': 22, 'scribe': 6, 'sentinel': 1, 'simplifier': 1} assigned 72 registry 72 {'connector': 6, 'critic': 6, 'executor': 14, 'revenger': 4, 'reviewer': 12, 'scout': 22, 'scribe': 6, 'sentinel': 1, 'simplifier': 1}
falsify spec 64 {'connector': 2, 'critic': 4, 'executor': 2, 'mutation-tester': 10, 'reviewer': 39, 'scout': 7} assigned 64 registry 64 {'connector': 2, 'critic': 4, 'executor': 2, 'mutation-tester': 10, 'reviewer': 39, 'scout': 7}
dead 11 unique 136 overlap 0
```

Report-file count command (exit 0): `printf 'build='; printf '%s\n' /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-26/build/*.md | wc -l; printf 'falsify='; printf '%s\n' /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-26/falsify/*.md | wc -l` → `build=72`, `falsify=53`.

For each REV below, ran `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree -r --name-only REV -- .ufo/waves/round-25/falsify/ | PYTHONDONTWRITEBYTECODE=1 python3 -c 'import sys; n=sys.stdin.read().splitlines(); print("entries=%d markdown_reports=%d" % (len(n), sum(x.endswith(".md") for x in n)))'` (exit 0):

| REV | Command output (`entries`, `markdown_reports`) | Lesson assertion |
|---|---:|---:|
| `8ea41f9` | `0, 0` | `0, 0` |
| `8239a56` | `83, 82` | `83, 82` |
| `9d8a00d` | `88, 87` | `88, 87` |

All P4c counts re-derive; no mismatch / P4c finding. No installs; no tests, builds, linters or formatters run.

VERDICT: Round-26 seat, role, dead-seat, total and prior-report-unit assertions match retained evidence.
