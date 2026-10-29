import pytest
from pathlib import Path
def test_c0_prev_presence():
    assert Path("/app/x").exists()
@pytest.mark.parametrize("name", ["in.txt"])
def test_c_param_exists(name):
    assert (Path("/app") / name).exists()
