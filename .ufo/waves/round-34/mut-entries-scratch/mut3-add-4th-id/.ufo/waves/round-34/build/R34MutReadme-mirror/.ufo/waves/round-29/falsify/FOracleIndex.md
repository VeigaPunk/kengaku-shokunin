writer: KengakuR29-2.FOracleIndex-2

# FOracleIndex-2 — falsify integrated generated-config projection (round 29)

Item: for every profile and every task, output_filename == config_files/<enumerate index>.json,
index_equals_task_id true for all 812 frozen tasks, would_be_file_sha256 == sha256 of
json.dumps(task, indent=2) as upstream json.dump(item, f, indent=2) writes it; recomputed
independently from the instrument's --json projected_task and from my own text projection;
plus a shuffled-copy /tmp witness that pins block rebinding. Date 2026-10-21.

## Independence statement

I did NOT read or import plans/config_projection.py source (not even a range). I executed it
only as a CLI subprocess (--summary, --json, --selftest, and --root variants) from the lane
root and compared its stdout OUTPUT against an oracle derived solely from the prereg text
(plans/round-29-claims.md), the pinned generator bytes, and the pinned data. Python 3.14
(/usr/lib/python3.14), stdlib only. No tool installs: no pacman, no uv/cargo/npm (tooling
directive satisfied vacuously; nothing needed upgrading).

## Inputs (sha256sum, all match manifest.json and the prereg)

- plans/fixtures/r29/manifest.json f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87 (1061 bytes)
- plans/fixtures/r29/generate_test_data.py 45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd (838 bytes)
- plans/fixtures/r29/profiles.json 90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018 (1391 bytes)
- plans/fixtures/r28/webarena/config_files/test.raw.json 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 (880776 bytes)
Raw parses to a list of 812 tasks, all task_id int, ids [0..811] in file order. Oracle method
from generator bytes: six sequential str.replace over the whole raw text in manifest order
(GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP; tokens __TOK__), json.loads, then
enumerate position -> filename config_files/{idx}.json and json.dumps(task, indent=2) default
separators/ensure_ascii, no trailing newline.

## Instrument baseline (read-only runs)

- --summary rc=0, stdout 6914 bytes, ends "TOTAL findings=0 exit=0" (3 words, counted programmatically).
- --selftest rc=0, 20 clean cases listed, including cli_coherent_rebinding and cli_manifest_tampered.
- --json rc=0, stdout 3881050 bytes, findings=[].

## Row comparison (2436 rows x field classes = 21924 checks, instrument output vs my oracle)

Zero mismatches (0/2436 each):
1. output_index equals enumerate position (0-based, 0..811) for all rows, all 3 profiles.
2. output_filename == config_files/<output_index>.json, e.g. idx0 "config_files/0.json" (1 word), idx811 "config_files/811.json"; also equal to my oracle filename.
3. task_id equals the raw-file task at the same enumerate position (orig[i].task_id), all rows.
4. index_equals_task_id is true on every row AND internally consistent (task_id == output_index).
   Instrument index_mapping: {"index_equals_task_id": 812, "output_index_rule": "enumerate position", "violations": []}.
5. would_be_file_sha256 == my sha256(json.dumps(task, indent=2)) computed from my own text
   projection, 2436/2436. This is exactly what upstream json.dump(item, f, indent=2) writes
   (default ensure_ascii=True, no trailing newline). Example distinct_origins idx0:
   9533088e31781047e4c4f3b9cafe02f734aaaa3fb9c47ebc29176bd8d6a6e5e6.
6. projected_task deep-equals my parsed projected task (python ==), 2436/2436.

The single systematic observation (2436/2436 rows, exact values in scratch bundle):
- would_be_file_sha256 != sha256(json.dumps(<the projected_task object as emitted in --json>, indent=2)).
- Cause (observed, then [INFERENCE] for intent): the emitted projected_task carries keys sorted
  alphabetically, differing from raw-file key order in 812/812 rows per profile
  (row0 raw order starts sites, task_id, require_login...; emitted order starts eval, geolocation,
  instantiation_dict...). Sorting alone explains it: sorted-key dumps of emitted vs my object are
  byte-equal in 812/812 rows per profile, and deep equality holds. The claimed digest still
  matches the raw-ordered serialization on every row, i.e. what upstream would actually write.
- Exact example: distinct_origins idx0 claimed 9533088e31781047e4c4f3b9cafe02f734aaaa3fb9c47ebc29176bd8d6a6e5e6;
  re-serialization of the emitted object gives 823a9a7fd4ca2b16ae5d6e0c7966f22584691845bdb675832ad56983085aebcd.
- Consumer caveat: anyone re-hashing the --json emitted projected_task with json.dumps(indent=2)
  will not reproduce would_be_file_sha256 (0/812 rows match); the digest is defined over the
  raw-ordered task, matching upstream. Presentation-only; not a projection or invariant finding.
- 31/812 distinct_origins rows contain non-ASCII content; ensure_ascii=True default is confirmed
  as the hashed serialization since my default-args dumps matched 2436/2436.

## Secondary agreement (my oracle vs instrument published aggregates, all equal)

- projected_text_sha256 per profile: 2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4 (distinct_origins), 54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b (path_prefix), 49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2 (trailing_slash_sensitivity).
- Original occurrences by token: GITLAB 385, REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133; tasks-with-token 204/128/192/182/0/128; string leaves 10869; changed leaves 1416; changed leaves by token 385/323/275/300/133.
- Remaining six known tokens in my projected texts: 0 across all 3 profiles.
- occurrence_provenance: all 1435 records verified — each codepoint offset slices exactly to its
  token in the raw text, and each json_pointer resolves into the claimed task_index's string leaf
  containing that token (0 failures, units kept distinct: occurrences vs changed leaves vs tasks).
- raw_text_sha256 field equals actual file digest; manifest_sha256 field equals the prereg pin.

## Pin-rebinding witness (all writes under /tmp/foracleindex2/; repo untouched)

1. Control: byte copy of the 4 pinned inputs into /tmp/foracleindex2/lane under the same
   relative layout, --root that lane --summary -> rc=0, findings=0 (structure accepted).
2. Shuffled raw, manifest untouched: json list shuffled with random.Random(29), written to
   /tmp/foracleindex2/lane_shuffled_raw -> rc=2, FINDING {"id": "snapshot_tampered", "path":
   "plans/fixtures/r28/webarena/config_files/test.raw.json"}, TOTAL findings=1 exit=2.
3. Coherent rebind (the requested case): copied the shuffled lane, re-pinned the manifest's raw
   sha256 to the shuffled file's true digest 10bcfaa726cc6b3ebc06b3be43fd0e44aa9e340beeb99f9925ca22366fd4bfea
   (manifest bytes then hash 8e22239e22d44b9bda50790bc7d2f1c194de8cf81eadb89a743e62b74cf8554d,
   i.e. manifest+input coherent) -> rc=2, FINDING {"id": "manifest_tampered"}, TOTAL findings=1 exit=2.
   The manifest pin persisted in the instrument (prereg: SHA256f6390b92... independently persisted)
   refuses coherent rebinding; no projections are emitted on any refusal path.

## Files touched by this seat

- Report: .ufo/waves/round-29/falsify/FOracleIndex.md (this file).
- Scratch: .ufo/waves/round-29/scratch/falsify/FOracleIndex-2/oracle-evidence.json (machine-readable results).
- /tmp/foracleindex2/ (instrument outputs, my projection, shuffled lanes; outside the repo).
No production, fixture, corpus, SOURCES, SCORECARD, candidate, git/jj state, or sibling files
written. No delegation, no subagents.

## Mismatches found

Exactly one class, presentation-layer and fully characterized above (2436/2436 rows: re-dump of
emitted projected_task != claimed sha; root cause observed as key-sorted emission; upstream-faithful
digest claim itself verified 2436/2436 against my independent serialization). Zero mismatches on
filename pattern, enumerate indexing, index==task_id, task_id-vs-raw, projected task content, all
published aggregates, and all 1435 provenance records.

[INFERENCE] The sorted-key emission is an intentional output canonicalization, not a projection
defect: deep equality and sorted-dump byte equality hold on every row, and the claimed digest
matches the upstream serialization everywhere.

Quoted strings used and their programmatic word counts: manifest_tampered (1), snapshot_tampered (1),
"TOTAL findings=0 exit=0" (3), "enumerate position" (2), config_files/0.json (1), index_equals_task_id (1).
All counts observed, none inferred; no counts promised.

VERDICT: PASS
