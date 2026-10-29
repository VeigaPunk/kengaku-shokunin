import sys
import pytest
from pathlib import Path
def test_h1_presence_only():
    assert Path("/app/h").exists()
@pytest.mark.skipif(sys.version_info < (3, 10), reason="needs 3.10")
def test_h2_compare():
    assert Path("/app/h").read_text() == "v"
