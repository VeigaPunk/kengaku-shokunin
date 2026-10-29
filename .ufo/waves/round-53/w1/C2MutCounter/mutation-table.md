| id | group | mutant | predicted | pristine selftest | augmented selftest | killer / note |
|---|---|---|---|---|---|---|
| M00 | NL | null: comment appended, no behaviour change | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | SURVIVED (rc=0, SELFTEST cases=41 failures=0) | null: not killable by design |
| M01 | SL | ledger absent: missing list emptied | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: ledger-absent |
| M02 | SL | argv length floor 2 -> 1 | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: argv-one-element |
| M03 | SL | argv length floor 2 -> 3 | K | KILLED (rc=1, SELFTEST cases=12 failures=7) | KILLED (rc=1, SELFTEST cases=41 failures=22) | pristine fixture |
| M04 | SL | argv all-str check disabled | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: argv-nonstring-element |
| M05 | SL | script-None guard removed | E | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | SURVIVED (rc=0, SELFTEST cases=41 failures=0) | equivalent |
| M06 | SL | entry-script membership inverted | K | KILLED (rc=1, SELFTEST cases=12 failures=8) | KILLED (rc=1, SELFTEST cases=41 failures=25) | pristine fixture |
| M07 | SL | exit bool exclusion removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: exit-is-bool |
| M08 | SL | state domain check removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: state-outside-domain |
| M09 | SL | state/exit consistency test removed | K | KILLED (rc=1, no cases line) | KILLED (rc=1, no cases line) | pristine: crash (KeyError 'evidence' in state-exit-inconsistent) |
| M10 | SL | state/exit consistency operator != -> == | K | KILLED (rc=1, no cases line) | KILLED (rc=1, no cases line) | pristine: crash (KeyError 'evidence') plus truthful row flagged BAD-DECL |
| M11 | SL | kind domain check removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: kind-outside-domain |
| M12 | SL | red-reason branch keyed on green | K | KILLED (rc=1, SELFTEST cases=12 failures=2) | KILLED (rc=1, SELFTEST cases=41 failures=11) | pristine fixture |
| M13 | SL | reason word floor < -> <= | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: reason-exactly-10-words |
| M14 | SL | MIN_REASON_WORDS 10 -> 9 | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: reason-9-words |
| M15 | SL | MIN_REASON_WORDS 10 -> 17 | K | KILLED (rc=1, SELFTEST cases=12 failures=1) | KILLED (rc=1, SELFTEST cases=41 failures=5) | pristine fixture |
| M16 | SL | MIN_REASON_WORDS 10 -> 1 | K | KILLED (rc=1, SELFTEST cases=12 failures=1) | KILLED (rc=1, SELFTEST cases=41 failures=2) | pristine fixture |
| M17 | SL | evidence floor 6 -> 5 | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: evidence-5-chars |
| M18 | SL | evidence floor 6 -> 9 | K | KILLED (rc=1, SELFTEST cases=12 failures=1) | KILLED (rc=1, SELFTEST cases=41 failures=5) | pristine fixture |
| M19 | SL | evidence strip() dropped | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: evidence-padded-short |
| M20 | SL | evidence str-type check removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | SURVIVED (rc=0, SELFTEST cases=41 failures=0) | crash-equivalent: pristine and mutant both exit 1 via uncaught exception (TypeError at evaluate vs AttributeError at static_legs) |
| M21 | SL | help limit <= -> < | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: help-at-exact-limit |
| M22 | SL | MAX_HELP_FRACTION 0.10 -> 0.50 | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: help-fraction-quarter |
| M23 | EV | help count reads entry kind | K | KILLED (rc=1, SELFTEST cases=12 failures=2) | KILLED (rc=1, SELFTEST cases=41 failures=8) | pristine fixture |
| M24 | EV | kind-count guard removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, no cases line) | new fixture: kind-outside-domain (crash) |
| M25 | EV | static_ok: missing term removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: dry-missing-row |
| M26 | EV | static_ok: extra term removed | K | KILLED (rc=1, SELFTEST cases=12 failures=1) | KILLED (rc=1, SELFTEST cases=41 failures=1) | pristine fixture |
| M27 | EV | static_ok: entry_mismatch term removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: dry-entry-mismatch |
| M28 | EV | static_ok: bad_decl term removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: dry-bad-decl |
| M29 | EV | static_ok: bad_reason term removed | K | KILLED (rc=1, SELFTEST cases=12 failures=1) | KILLED (rc=1, SELFTEST cases=41 failures=3) | pristine fixture |
| M30 | EV | static_ok: dups term removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: duplicate-row-name |
| M31 | EV | static_ok: ledger_err term removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: ledger-absent-no-rows |
| M32 | EV | static_ok: help_ok and -> or | K | KILLED (rc=1, SELFTEST cases=12 failures=3) | KILLED (rc=1, SELFTEST cases=41 failures=11) | pristine fixture |
| M33 | EV | static_ok: help_ok dropped | K | KILLED (rc=1, SELFTEST cases=12 failures=1) | KILLED (rc=1, SELFTEST cases=41 failures=2) | pristine fixture |
| M34 | SL | extra computed as intersection | K | KILLED (rc=1, SELFTEST cases=12 failures=2) | KILLED (rc=1, SELFTEST cases=41 failures=8) | pristine fixture |
| M35 | SL | missing computed as intersection | K | KILLED (rc=1, SELFTEST cases=12 failures=2) | KILLED (rc=1, SELFTEST cases=41 failures=9) | pristine fixture |
| M36 | RV | row entry cell index 2 -> 1 | K | KILLED (rc=1, SELFTEST cases=12 failures=7) | KILLED (rc=1, SELFTEST cases=41 failures=22) | pristine fixture |
| M37 | RV | entry regex loses corpus/grader prefixes | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: corpus-entry-script |
| M38 | RV | duplicate names not recorded | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: duplicate-row-name |
| M39 | RV | duplicate names: first-wins | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | SURVIVED (rc=0, SELFTEST cases=41 failures=0) | verdict-equivalent (predicate fails either way; only the validated duplicate line changes) |
| M40 | RV | ledger schema check removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: ledger-schema-foreign |
| M41 | EV | dry-run exit inverted | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=4) | new fixture: dry-truthful |
| M42 | EV | predicate fail exit 1 -> 2 | K | KILLED (rc=1, SELFTEST cases=12 failures=11) | KILLED (rc=1, SELFTEST cases=41 failures=29) | pristine fixture |
| M43 | EV | help limit max(1,n_reg) -> n_reg | E | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | SURVIVED (rc=0, SELFTEST cases=41 failures=0) | equivalent |
| M44 | EV | clean test rewritten as is-not-False | E | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | SURVIVED (rc=0, SELFTEST cases=41 failures=0) | equivalent |
| M45 | EV | clean test widened to admit dirty clone | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: git-dirty |
| M46 | EV | executed == n_reg relaxed to >= | E | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | SURVIVED (rc=0, SELFTEST cases=41 failures=0) | equivalent |
| M47 | EV | executed == n_reg dropped | E | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | SURVIVED (rc=0, SELFTEST cases=41 failures=0) | equivalent under static_ok and only-None |
| M48 | EV | tmo == 0 dropped | K | KILLED (rc=1, SELFTEST cases=12 failures=1) | KILLED (rc=1, SELFTEST cases=41 failures=2) | pristine fixture |
| M49 | EV | mism == 0 dropped | K | KILLED (rc=1, SELFTEST cases=12 failures=2) | KILLED (rc=1, SELFTEST cases=41 failures=2) | pristine fixture |
| M50 | EV | evmiss == 0 dropped | K | KILLED (rc=1, SELFTEST cases=12 failures=1) | KILLED (rc=1, SELFTEST cases=41 failures=1) | pristine fixture |
| M51 | EV | only-is-None term dropped | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: only-every-row |
| M52 | EV | only-is-None inverted | K | KILLED (rc=1, SELFTEST cases=12 failures=1) | KILLED (rc=1, SELFTEST cases=41 failures=7) | pristine fixture |
| M53 | EV | only filter disabled | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: only-one-row-count |
| M54 | EV | entry_mismatch filter dropped from names | S-diag | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: entry-mismatch-not-executed |
| M55 | EV | bad_decl filter dropped from names | K | KILLED (rc=1, no cases line) | KILLED (rc=1, no cases line) | pristine: crash (KeyError 'evidence' on a bad_decl row) |
| M56 | EV | TIMEOUT branch disabled | K | KILLED (rc=1, SELFTEST cases=12 failures=1) | KILLED (rc=1, SELFTEST cases=41 failures=2) | pristine fixture |
| M57 | EV | timeout ignores per-row timeout_s | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: timeout-default-ignored |
| M58 | EV | evidence containment inverted | K | KILLED (rc=1, SELFTEST cases=12 failures=2) | KILLED (rc=1, SELFTEST cases=41 failures=5) | pristine fixture |
| M59 | EV | evidence gate keyed on green | K | KILLED (rc=1, no cases line) | KILLED (rc=1, no cases line) | pristine: crash (KeyError 'evidence' on a green row) |
| M60 | EV | rc mismatch test inverted | K | KILLED (rc=1, SELFTEST cases=12 failures=4) | KILLED (rc=1, SELFTEST cases=41 failures=9) | pristine fixture |
| M61 | EV | observed-green counter inverted | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: tally-two-green-one-red |
| M62 | EV | declared-green count reads red | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: tally-two-green-one-red |
| M63 | EV | executed counter not incremented | K | KILLED (rc=1, SELFTEST cases=12 failures=1) | KILLED (rc=1, SELFTEST cases=41 failures=7) | pristine fixture |
| M64 | SX | selftest: want_out check removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: neg-want-out |
| M65 | SX | selftest: want_in check removed | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: neg-want-in |
| M66 | SX | selftest exit always 0 | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | SURVIVED (rc=0, SELFTEST cases=41 failures=0) | survives default run; killed only by the env-gated poison child |
| M67 | SX | selftest cases line constant changed | K | KILLED (rc=0, SELFTEST cases=112 failures=0) | KILLED (rc=0, SELFTEST cases=141 failures=0) | trivial: cases line text changed (not a fixture) |
| M68 | SX | selftest: rc check made vacuous | S | SURVIVED (rc=0, SELFTEST cases=12 failures=0) | KILLED (rc=1, SELFTEST cases=41 failures=1) | new fixture: neg-want-rc |
