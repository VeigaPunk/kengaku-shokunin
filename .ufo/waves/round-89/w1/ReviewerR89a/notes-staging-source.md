Review-side staging + confirmation driver.
Bind copies the probe's argv shape; inside the namespace it chowns nothing
and asks only for the four toolchain steps the captured grader performs.

Staging rule: the case tree must be owned by a uid NOT mapped in the sandbox's
uid_map (mapping is identity "0 0 1"), so the sandboxed python (uid 0 == host 0)
must see the tree readable+searchable but the compiler temp-dir writes fail
unless the dir is uid-0-owned AND 0777... which is what the probe avoids:
the probe stages under a TemporaryDirectory owned by the CALLER (uid 0), inside
an unshare-all namespace whose uid_map is "0 0 1" → tree is uid==0, writable.
Re-derivation: use a staging dir owned by uid 0 (the caller), the tree must be
actual host-uid-0 owned to be writable inside the minimally mapped uid-ns.

For the blind derivation though, the mapping does not matter: whether or not the
compilers can write temp files does not change the P/F/E classification, since
any compile failure routes through FileNotFoundError exactly as a missing binary,
which is the honest-limit note (b) in the claims file. My confirmation driver
therefore stages owned-by-0 with world-write, which restores every case's
intended semantics:
  - exact, padded-output: compile succeeds, exec works, outputs compared strimmed
  - extra-file: listdir fails first, identical regardless of write perms
  - off-by-one-rust: compile succeeds both sides; F requires Rust output mismatch
  - cpp-exits-nonzero: compiles ok, exit 1 raises CalledProcessError -> E
  - rust-only: g++ fails, cmain absent -> FileNotFoundError
  - cpp-only: rustc fails, main absent -> FileNotFoundError
  - neither-compiles: both absent -> FileNotFoundError
"""
