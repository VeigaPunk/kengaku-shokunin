"""Reproduce mutation-witness.txt's three mutants on a /tmp copy; never touches the lane."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
FILES = ["plans/config_projection.py", "plans/fixtures/r29/manifest.json", "plans/fixtures/r29/generate_test_data.py",
         "plans/fixtures/r29/profiles.json", "plans/fixtures/r28/webarena/config_files/test.raw.json",
         "plans/fixtures/r29/hand/cascade-order.case.json", "plans/fixtures/r29/hand/index-shuffled-ids.fixture.json",
         "plans/fixtures/r29/hand/url-only.fixture.json", "plans/fixtures/r29/hand/url-only.expected.json"]

PROJECT = '''    for name in ORDER:
        token = "__%s__" % name
        steps.append({"name": name, "token": token, "applied_replacements": text.count(token)})
        text = text.replace(token, values[name])
    return text, steps'''
MUTANTS = {
    "wrong_order_reversed": (PROJECT, PROJECT.replace("for name in ORDER:", "for name in reversed(ORDER):")),
    "url_only_substitution": (PROJECT, '''    import re as _re
    for name in ORDER:
        token = "__%s__" % name
        steps.append({"name": name, "token": token, "applied_replacements": text.count(token)})
        text = _re.sub(r'("(?:start_url|url|reference_url)":\\s*")([^"]*)"', lambda m: m.group(1) + m.group(2).replace(token, values[name]) + '"', text)
    return text, steps'''),
    "index_by_task_id": ('"output_filename": "config_files/%d.json" % i,',
                         '"output_filename": "config_files/%s.json" % (task.get("task_id", i) if isinstance(task, dict) else i),'),
}

for name, (old, new) in [("control", ("", ""))] + list(MUTANTS.items()):
    with tempfile.TemporaryDirectory(prefix="fcritclaimmet-") as tmp:
        root = Path(tmp)
        for rel in FILES:
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(LANE / rel, root / rel)
        tool = root / "plans/config_projection.py"
        if old:
            src = tool.read_text()
            assert src.count(old) == 1, name
            tool.write_text(src.replace(old, new))
        st = subprocess.run([sys.executable, str(tool), "--selftest"], capture_output=True, text=True)
        sm = subprocess.run([sys.executable, str(tool), "--summary"], capture_output=True, text=True)
        err = (st.stderr.strip().splitlines() or [""])[-1][:160]
        total = [l for l in sm.stdout.splitlines() if l.startswith("TOTAL")]
        finds = sorted({l.split('"id": "')[1].split('"')[0] for l in sm.stdout.splitlines() if l.startswith("FINDING")})
        print(f"{name}: selftest exit {st.returncode} {err or st.stdout.strip()[:60]} | summary exit {sm.returncode} {total} findings={finds}")
