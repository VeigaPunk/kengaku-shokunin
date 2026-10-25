ATTACKS: fleet-root misroot sweep for untracked files naming kengaku round 25 (read-only)

Scope: `git -C /home/vgpnk/Projects/shokunin status --porcelain` (fleet root), then content scan of every untracked entry for kengaku round-25 naming.

Command 1: `git -C /home/vgpnk/Projects/shokunin status --porcelain`
- ` M .ufo/watchdog.log` (tracked, modified; not an untracked item, out of scope)
- `?? .ufo/state/{chousa,kagi,kaidoku,kake,kama,kasegi,kengaku,kumitate,mado,mori,souji,tabi,tameshi,tsukuroi}.report-baseline` (14 files)
- `?? .ufo/waves/round-35/` (directory; contains `build/FidCollectOmpNativeHandoffLibEve.md`)
- 15 untracked entries total.

Command 2: per-file scan for `kengaku` AND `round[ -]?25|round-25|r25` (case-insensitive). Result: no matches. The loop skipped directories (`-f` test), so the directory entry was covered separately.

Command 3: `grep -rIlE 'round[ -]?25|round-25|Round 25|kengaku round 25' .ufo/state/*.report-baseline .ufo/waves/round-35` -> no output.

Command 4: `grep -nIiE 'kengaku|round.?25|r25' .ufo/waves/round-35/build/FidCollectOmpNativeHandoffLibEve.md` -> no output.

Content of the 14 `.report-baseline` files: each is `<integer> e3b0c442...b855` (the integer is a count; the hash is the SHA-256 of empty input). `kengaku.report-baseline` = `25 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The integer `25` is a numeric baseline value, not a naming of kengaku round 25; treated as NOT a misroot, but flagged so the reader can judge.

Fleet-root path check: `ls /home/vgpnk/Projects/shokunin/.ufo/waves/round-25/` -> `No such file or directory`. No round-25 wave dir is misrooted at fleet root.

Lane-side state (read-only, for context): kengaku lane has `.ufo/waves/round-25/{build,falsify}/`; `falsify/` holds `swarm-registry.json` (mode 0600, not read, not in scope).

Misroot list: NONE.
Mutations: none. No files moved, deleted, or written at fleet root. Only this report was written, at the kengaku lane path.

Repo tips (read-only log): fleet root HEAD `f2e8cff`; kengaku lane HEAD `8ea41f9` (round-25 landed tip, as stated in the assignment).

Installs: none (no tools installed; `git`, `grep`, `find`, `ls`, `cat` only).

Limits: sweep covers `git status --porcelain` untracked entries only; ignored files (gitignored) were not scanned, and the round-35 build file was scanned only with the round-25 pattern, not read in full.

VERDICT: SURVIVES — no untracked fleet-root file names kengaku round 25; the only candidate (`kengaku.report-baseline` containing `25`) is a numeric baseline, not a misroot.
