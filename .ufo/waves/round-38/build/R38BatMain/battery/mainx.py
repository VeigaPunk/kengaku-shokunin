"""Battery38 module mainx: ``main``'s exits, one fixture per frozen mutant N17 and N18.

Both fixtures are MAIN-shaped (``expect="error"``, ``defects=[]``): the reference gate exits 2 before
printing any clause line, so the declared clause set is empty and the kill is the exit code itself.

  mainx-root-not-a-directory   N17  ``main``'s ``if not args.root.is_dir():`` guard. ``--root`` names a
                                    path inside the fixture directory that exists nowhere; the reference
                                    prints ``setup: root not a directory: ...`` and returns 2. The mutant
                                    (``if False:``) falls through into ``cmd_package`` on a missing tree,
                                    whose clauses report DEFECT and exit 1.
  mainx-spec-invalid-json      N18  ``main``'s crash handler ``except Exception: ... return 2``. The
                                    fixture owns a spec that is not JSON, so ``json.loads`` raises
                                    ``JSONDecodeError`` inside the ``try``; the reference returns 2, the
                                    mutant returns 0 and prints nothing.

Neither fixture reuses the frozen round-35 package: N17 never reaches a clause, N18 never parses a spec.
The N18 fixture passes its own ``--spec`` inside the fixture directory (the counter accepts that only for
battery38 fixtures) and leaves ``--root`` on the directory itself; the resolution of the crash happens
before the root guard, so the ordering does not matter.

stdlib only; no import-time side effects.
"""


def _package_argv(d):
    return ["package", "--root", str(d), "--require-clean-tree"]


def _root_not_a_directory(ctx, d):
    """N17: root names a path under the fixture dir that does not exist; d stays empty on purpose."""
    missing = d / "absent-root"
    if missing.exists():
        raise RuntimeError(f"N17 fixture root unexpectedly exists: {missing}")
    return ["package", "--root", str(missing), "--require-clean-tree"]


def _spec_invalid_json(ctx, d):
    """N18: a fixture-owned spec whose bytes are not JSON; setup crashes before any clause runs."""
    spec = d / "spec-invalid.json"
    spec.write_text('{"rows": {\n')
    return _package_argv(d) + ["--spec", str(spec)]


FIXTURES = [
    {"fid": "mainx-root-not-a-directory", "expect": "error", "defects": [], "build": _root_not_a_directory},
    {"fid": "mainx-spec-invalid-json", "expect": "error", "defects": [], "build": _spec_invalid_json},
]
