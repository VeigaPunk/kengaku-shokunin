def selftest():
    """Suggested body to wire into plans/attrib_calibration.py --selftest."""
    import math
    from pathlib import Path

    fixture_dir = Path(__file__).resolve().parent / "fixtures" / "r25" / "attrib-cal"
    bar = 0.80

    def only_rows(name):
        blocks = parse_receipt(str(fixture_dir / name))
        assert len(blocks) == 1, (name, len(blocks))
        return blocks[0]["rows"]

    def row_signature(rows):
        # Frozen duplicate identity: trial id, prediction, GT and chain.
        return tuple((r[0], r[2], r[3], r[5]) for r in rows)

    # The zero-error CP lower endpoint is alpha/2 ** (1/n); this is also a
    # known-value guard against a numerically perturbed exact-interval routine.
    lo16, hi16 = clopper_pearson(16, 16)
    lo17, hi17 = clopper_pearson(17, 17)
    assert math.isclose(lo16, 0.025 ** (1 / 16), rel_tol=1e-10, abs_tol=1e-8)
    assert math.isclose(lo17, 0.025 ** (1 / 17), rel_tol=1e-10, abs_tol=1e-8)
    assert hi16 == 1.0 and hi17 == 1.0
    assert lo16 < bar <= lo17
    assert verdict(16, 16, bar) == "INDETERMINATE"
    assert verdict(17, 17, bar) == "PASS"

    # One changed GT field makes the retained 20/20 point summary stale.
    flip_path = fixture_dir / "gt-flip.log"
    flip_rows = only_rows("gt-flip.log")
    observed_k = sum(r[2] == r[3] for r in flip_rows)
    assert len(flip_rows) == 20 and observed_k == 19
    assert "ACCURACY: 20/20 = 1.000 (bar 0.80, min scored n 20) -> PASS" in flip_path.read_text(encoding="utf-8")
    assert verdict(observed_k, len(flip_rows), bar) == "INDETERMINATE"

    # Identical tables must contribute one n=16 sample, not n=32 (which passes).
    dup_blocks = parse_receipt(str(fixture_dir / "duplicate-block.log"))
    assert len(dup_blocks) == 2
    unique = {}
    for block in dup_blocks:
        rows = block["rows"]
        unique.setdefault(row_signature(rows), rows)
    assert len(unique) == 1
    dedup_rows = next(iter(unique.values()))
    dedup_k = sum(r[2] == r[3] for r in dedup_rows)
    assert len(dedup_rows) == 16 and dedup_k == 16
    assert verdict(dedup_k, len(dedup_rows), bar) == "INDETERMINATE"
    assert verdict(32, 32, bar) == "PASS"

    rows16 = only_rows("n16-all-correct.log")
    assert len(rows16) == 16 and all(r[2] == r[3] for r in rows16)
    rows17 = only_rows("n17-all-correct.log")
    assert len(rows17) == 17 and all(r[2] == r[3] for r in rows17)
    rows0 = only_rows("n0-untested.log")
    assert rows0 == [] and verdict(0, 0, bar) == "UNTESTED"

    wrong = only_rows("upper-below-bar.log")
    wrong_k = sum(r[2] == r[3] for r in wrong)
    _, upper = clopper_pearson(wrong_k, len(wrong))
    assert len(wrong) == 17 and wrong_k == 0
    assert math.isclose(upper, 1 - 0.025 ** (1 / 17), rel_tol=1e-10, abs_tol=1e-8)
    assert upper < bar and verdict(wrong_k, len(wrong), bar) == "FAIL"
    return True
