# Sealed mechanism notes

- `phantom_order.py`: `order` accepts a fixture whose `--lane` names a regular file rather than a repository; the fence validates path containment but does not require an existing directory/repository for the lane before admitting.
- `phantom_anchor.py`: `anchor` accepts a nonexistent lane; the fence does not require its lane target to exist or be a repository before admitting.
- `newline_anchor.py`: a newline-bearing lane token naming a nonexistent path is accepted as an argv value and an absent lane is admitted; this tests argv token-shape handling without shell interpolation.
