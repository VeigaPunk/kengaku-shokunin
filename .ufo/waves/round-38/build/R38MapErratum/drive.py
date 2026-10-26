import pathlib, sys
lane = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(lane / "plans"))
import round37_c2_verify as r37
import round38_c2_verify as r38
print("r37.v7 ->", r37.v7(lane))
print("r38.v7 ->", r38.v7(lane))
print("r38.derive fail-set ->", r38.derive({"fail"}),
      "| pass-set ->", r38.derive({"pass"}),
      "| mixed ->", r38.derive({"fail", "pass"}))
row9 = [l for l in (lane/"corpus/knowledge/tb2-git-webserver-grader.md").read_text().splitlines()
        if l.startswith("| `instruction.md:9`")][0]
print("r38.MAP_ROW on the round-37 row-9 line ->", r38.MAP_ROW.match(row9))
print("r37 row-9 bytes ->", row9)
