import re
from pathlib import Path
def test_g1_startswith():
    assert Path("/app/g").read_text().startswith("#!/bin")
def test_g2_read_truthy():
    assert Path("/app/g").exists() and Path("/app/g").read_text()
def test_g3_re_match():
    assert re.match(r"^ok", Path("/app/g4").read_text())
