# Sealed module mechanism notes

- `info_redirect.py`: moves `.git/objects/info` outside the fixture and replaces it with a symlink. The fence's tree walk prunes `.git`; its explicit alternates probe sees no `alternates` entry, so the redirect remains unexamined.
- `pack_redirect.py`: repacks the committed objects, then moves `.git/objects/pack` outside and replaces it with a symlink. The fence's `.git`-pruned walk does not inspect this store member; the Git probes open pack data outside the fixture.
- `refs_redirect.py`: moves `.git/refs` outside and replaces it with a symlink after creating both required commits. Ref validation and object lookup open the redirected ref store outside the fixture.
