# Anchor captures for SOURCES rows S070, S072, S073, S074

Drafted by seat `R37AnchorSweep` (kengaku round 37) so that four anchor digests in `corpus/SOURCES.md`
resolve from committed bytes instead of only from a live fetch. Each file was fetched from the commit the
row itself pins, on 2026-10-26, and its digest equals the digest the row states — checked three ways: the
fetched bytes, the digest printed in the row, and (for S070/S072/S073) the byte-identical copy already
committed in round-29 scratch (`git ls-tree` + `git cat-file`).

| row | file here | pinned URL | commit | bytes | sha256 |
|---|---|---|---|---|---|
| S070 | `S070-generate_test_data.py` | `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/scripts/generate_test_data.py` | `dce04686a56253aefba7b18a4fa0937cf1dc987b` | 838 | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` |
| S072 | `S072-README.md` | `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/README.md` | `dce04686a56253aefba7b18a4fa0937cf1dc987b` | 9717 | `081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287` |
| S073 | `S073-prepare.sh` | `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/prepare.sh` | `dce04686a56253aefba7b18a4fa0937cf1dc987b` | 120 | `97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2` |
| S074 | `S074-task.py` | `https://raw.githubusercontent.com/ServiceNow/BrowserGym/4ccc72332ab9882bc9aed87264dbf60b16e426f0/browsergym/webarena/src/browsergym/webarena/task.py` | `4ccc72332ab9882bc9aed87264dbf60b16e426f0` | 8603 | `f996dfeef2bfb836fa79b20217cda36ecf428ed3965e3084e325626d7130fe67` |

`SHA256SUMS` beside this file lists those digests in `sha256sum -c` form.

Limit, stated: three of the four rows describe their digest as a "snapshot hash, not a manifest pin"
(S072 says so in the anchor cell). Retaining the bytes makes the claim re-checkable from the lane, which
`corpus/QUALITY.md` Q5 says a retained digest is *not* (a copy is not the original source); it does not
make the copy an independent observation of upstream — the fetch above is the independent observation.
