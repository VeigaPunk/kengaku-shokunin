"""Pre-freeze witness (L1 KengakuR41): S10 — `check()`'s requested-id refusal (`if missing:` -> `if False:` at
plans/sources_adopt.py:237) — is rc-equivalent through the CLI: main()'s build_block refuses the same id with
exit 5. Runs reference and mutant on the requested-id-absent fixture; prints both exit codes."""
import pathlib, subprocess, sys, tempfile
lane = pathlib.Path(sys.argv[1]).resolve()
src = (lane / "plans/sources_adopt.py").read_text()
old = '        if missing:\n            report["missing"] = missing\n            return EXIT_REQUEST, report'
assert src.count(old) == 1
HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")
ROW = ("| S900 | fixture source — https://example.invalid/x | docs | A | fixture scope | anchor text | fixture "
       "teaches | mined | 2026-10-25 | 180d | corpus/knowledge/old.md |\n")
with tempfile.TemporaryDirectory(dir=sys.argv[2]) as t:
    t = pathlib.Path(t)
    (t / "reg.md").write_text(HEADER)
    (t / "pkg.md").write_text(HEADER + ROW)
    (t / "ref.py").write_text(src)
    (t / "mut.py").write_text(src.replace(old, old.replace("if missing:", "if False:")))
    argv = ["--registry", str(t / "reg.md"), "--package", str(t / "pkg.md"), "--admit-ids", "S901",
            "--entries", "corpus/knowledge/x.md", "--access-date", "2026-10-25"]
    rc = {v: subprocess.run([sys.executable, str(t / f"{v}.py"), *argv], capture_output=True).returncode
          for v in ("ref", "mut")}
print(f"S10 requested-id-absent ref_rc={rc['ref']} mut_rc={rc['mut']} "
      f"{'EQUIVALENT-BY-RC' if rc['ref'] == rc['mut'] else 'DIFFERS'}")
