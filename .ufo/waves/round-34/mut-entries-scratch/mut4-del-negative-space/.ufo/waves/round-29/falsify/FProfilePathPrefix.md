writer: KengakuR29-2.FProfilePathPrefix-2

# FProfilePathPrefix — profile `path_prefix`, independent re-derivation and routing audit

Scope: the `path_prefix` profile of the round-29 instrument
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py` (sha256
`5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`): projected serialized-text
digest, `stimulus_observations`, `string_leaf_count`, the `stimulus_class` label against the profile
values and the README example shapes, and whether any stimulus effect reaches a FINDING or exit 1.
Read-only leaf. No production, fixture, corpus, SOURCES, SCORECARD or candidate file was written.
No tool install or upgrade (python3 3.14.8 stdlib only). Scratch and `/tmp` copies only.

## Independence and inputs

I did **not** open or read the text of `plans/config_projection.py`, did not copy or import it, and
did not inspect it with any parser. I only (i) ran `sha256sum` on it for identity, (ii) executed it
read-only (`--summary`, `--json`, `--selftest`, `--help`) and consumed stdout, and (iii) ran
`--root` against copies under `/tmp`. My derivation used: the round-29 prereg text
`plans/round-29-claims.md`; the generator bytes `plans/fixtures/r29/generate_test_data.py` (838
bytes, sha256 `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd`, lines 11–16
ordered `raw.replace`, line 20 `json.loads`, lines 21–23 `enumerate` filenames); the raw bytes
`plans/fixtures/r28/webarena/config_files/test.raw.json` (880776 bytes, 0 CR, all ASCII, sha256
`7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`); `plans/fixtures/r29/profiles.json`
(sha256 `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018`); manifest
`plans/fixtures/r29/manifest.json` (sha256 `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`);
the pinned README snapshot
`.ufo/waves/round-28/scratch/OpenTasks/pinned-README.md` (sha256
`081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287`); and the S072 row,
`corpus/SOURCES.md:94`.

Scratch: `.ufo/waves/round-29/scratch/falsify/FProfilePathPrefix-2/` — `reproject.py`,
`reproject.out`, `oracle.json`, `compare.py`, `compare.out`, `compare.json`, `compare2.out`,
`occ_check.out`, `live-summary.txt`, `label_check.out`, `root-copy-pristine.summary.txt`,
`root-copy-pathprefix-junction.summary.txt`, `root-copy-coherent-rebind.summary.txt`.

Commands (run from the lane root, read-only): `python3 plans/config_projection.py --summary`
(exit 0; 47 lines; `TOTAL findings=0 exit=0`; saved as `live-summary.txt`);
`python3 plans/config_projection.py --json` (exit 0; 3881050 bytes; sha256
`c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`);
`python3 plans/config_projection.py --selftest` (exit 0); `python3
.ufo/waves/round-29/scratch/falsify/FProfilePathPrefix-2/reproject.py` (`reproject.out`,
`oracle.json`); `python3 …/compare.py` (`compare.out`, `compare.json`); the stdlib scanner run
recorded in `occ_check.out`; `compare2.out` for bucket/per-task equality; `label_check.out` for the
label identity; and `python3 plans/config_projection.py --root /tmp/fpp_lane --summary` for the
three copy runs (exit 0 pristine, exit 2 on both tamper variants; the three `root-copy-*.summary.txt`
files).

## Attack

1. Re-implemented the generator on its bytes alone: UTF-8 text decode (inert: no CR, no non-ASCII),
   six `str.replace` calls in GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP order with the
   `path_prefix` values, `sha256(projected_text.encode("utf-8"))`, then `json.loads`.
2. Counted string **values** (not keys) in the parsed projection and compared every leaf
   raw-vs-projected by path, including category/template/token assignment.
3. Recomputed the stated observation exactly as: token occurrence whose replacement value ends with
   `/` and whose immediately following raw character is `/`. Cross-checked the same definition
   against the other two profiles (it must yield 697 for `trailing_slash_sensitivity`).
4. Wrote an independent JSON string-literal scanner over the raw text (path tuple, literal span,
   decoded value) to rebuild all 1435 occurrence records: token literal at codepoint offset,
   `json_pointer`, `task_index`, `path_template`, role.
5. Compared all 812 `projected_task` objects, all 1416 changed-leaf records (pointer, template,
   category, original, projected, tokens), `output_filename`, `index_equals_task_id`, and
   `would_be_file_sha256` (`json.dumps(item, indent=2)` UTF-8, upstream `json.dump` defaults) against
   the instrument's `--json`.
6. Checked the label against `profiles.json` values, the pinned README shape lines, and S072; then
   tested finding/exit routing, including negative controls on a `/tmp/fpp_lane` copy.

## Observed results — `path_prefix`

Mine (independent) vs instrument `profiles.path_prefix` (`--json`), and the corresponding
`--summary` lines 26/35/47 of `/tmp/r29_fpp_sum2.txt`:

| quantity | mine | instrument | match |
|---|---|---|---|
| `projected_text_sha256` (UTF-8 projected text) | `54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b` | same | yes |
| projected text size | 915216 bytes | not printed | — |
| `string_leaf_count` | 10869 | 10869 | yes |
| `parsed_task_count` | 812 | 812 | yes |
| `changed_leaf_count` | 1416 | 1416 | yes |
| `changed_task_count` | 812 | 812 | yes |
| `changed_leaves_with_multiple_occurrences` | 13 | 13 | yes |
| `applied_replacements` per step | 385, 336, 281, 300, 0, 133 | same (`steps[]`) | yes |
| `changed_leaves_by_token` | 385 / 323 / 275 / 300 / 0 / 133 | same | yes |
| `changed_tasks_by_token` | 204 / 128 / 192 / 182 / 0 / 128 | same | yes |
| `changed_leaves_by_category` | url 1355, non-url 61 | same | yes |
| `changed_leaves_by_path_template` | start_url 812, program_html url 338, reference_url 205, must_include 60, raw_annotation 1 | same | yes |
| `remaining_known_tokens_text` / `_decoded` | 0 each for all six | same | yes |
| `stimulus_observations.value_slash_then_raw_slash_junctions` | 0 | 0 | yes |
| per-task `projected_task` deep equality | 812/812 | 812/812 | yes |
| per-task `changed_leaves` (all fields incl. `tokens`, `category`) | 0 diffs / 1416 | — | yes |
| per-task `would_be_file_sha256` | 0 diffs / 812 | — | yes |
| `output_filename` / `index_equals_task_id` | `config_files/{i}.json`, true 812/812 | same | yes |
| occurrence records | 1435, multiset equal to instrument (offset, token, pointer, template, task, role) | 1435 | yes |

Supporting facts: raw task_ids are exactly `0..811` (int); every one of 812 tasks changes; union of
tasks carrying any token is 812; no token appears in a JSON key (18140 key literals scanned);
projected parsed values contain zero known tokens; every instrument occurrence offset satisfies
`raw[offset:offset+len(token)] == token` and its pointer resolves to a string containing the token
(1435/1435). `population.tokens_followed_by_slash` = 697, equal to my raw-only count; my junction
counts are 0 (`distinct_origins`), 0 (`path_prefix`), 697 (`trailing_slash_sensitivity`, per token
GITLAB 225, REDDIT 232, SHOPPING 110, SHOPPING_ADMIN 125, MAP 5, sum 697), so the observation is
profile-dependent, not a raw-only constant.

Independent execution checks: `--summary` exit 0, `--json` exit 0, `--selftest` exit 0
(`SELFTEST clean cases=20`). `--json` stdout sha256 is
`c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` on two runs (byte-identical),
equal to `corpus/evidence/round29-calibration/build-json-sha256.txt`. Current `--summary` is
identical to `build-summary.txt` except that receipt's appended final line `exit=0`.

The first ordered comparison of occurrence records reported 1435 positional differences; that was an
ordering artifact, not a value mismatch: the instrument lists occurrences grouped by replacement order
(first record offset 42249, `__GITLAB__`, `/44/start_url`), each group ascending by offset, whereas my
offset-sorted list starts at offset 172 (`__SHOPPING_ADMIN__`, `/0/start_url`). As a multiset the two
are exactly equal (`only mine: []`, `only theirs: []`), and no prereg line requires global offset
order.

## `stimulus_class` label against values and README shapes

Summary line 26 (now): `PROFILE path_prefix stimulus="synthetic '/prefix' path on all six values;
changes URL path structure by design"`; the JSON `profiles.path_prefix.stimulus_class` is the same
string (13 whitespace-delimited words, 80 chars; verified the summary line contains it exactly).

Against `plans/fixtures/r29/profiles.json:13-22`: `path_prefix` purpose (line 14, 8 words) is
"controlled synthetic text-substitution profile, not an observed deployment"; the six values
(lines 16–21) are `http://gitlab.invalid:10201/prefix`, `http://reddit.invalid:10202/prefix`,
`http://shopping.invalid:10203/prefix`, `http://shopping-admin.invalid:10204/prefix`,
`http://wikipedia.invalid:10205/prefix`, `http://map.invalid:10206/prefix`. Observed: all six end
`/prefix`; all six carry an `http://` scheme; all hosts are `.invalid`; ports are 10201–10206. The
label's two clauses are therefore literally true of the value map. The projected values confirm the
path effect: 1416 of 1416 changed leaves contain `/prefix`; of the 1435 token occurrences, 697 are
immediately followed by raw `/` (projected as `prefix/...`) and 738 by the closing `"`; no `//` is
created at a substitution boundary (junction 0). The naive `//` count in projected text (1458) is
scheme syntax only: 1435 value-internal `http://` plus 23 raw `://` in non-token text (5 `http://`,
8 `https://`, 10 `ssh://`); projected `http://` count is 1440, and `http://http://` count 0.

Against the README shape (`pinned-README.md:86-92`, sha256 `081c8264…9287`; S072 at
`corpus/SOURCES.md:94`): the README exports are scheme-less `origin:port` forms —
`export SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"` (2 words) at line 87 and
`export WIKIPEDIA="<your_wikipedia_domain>:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"`
(2 words) at line 91, with HOMEPAGE marked as a placeholder at line 92; S072 (3-word fragment
"SHOPPING_ADMIN adds /admin"). The profile deviates: it is scheme-qualified, puts `/prefix` on all
six values instead of `/admin` only on SHOPPING_ADMIN and a long path only on WIKIPEDIA, and
`__WIKIPEDIA__` has 0 raw occurrences so that value is never applied. The label does not assert
README conformance — it says "synthetic" and "by design"; the purpose line and summary LIMIT line 2
("their per-profile effects are stimulus observations, never model or task errors", 11 words) cover
the non-deployment status. No label statement is contradicted by the values or by S072, so I record
this as a disclosed synthetic deviation, not a label mismatch.

## Finding / exit routing

Observed on the frozen tree: `--summary` prints `TOTAL findings=0 exit=0` (line 47) and exits 0;
`--json` has top-level `"findings": []` and exits 0. The profile object has no findings/effect key;
its keys are `changed_leaf_count`, `changed_leaves_by_category`, `changed_leaves_by_path_template`,
`changed_leaves_by_token`, `changed_leaves_with_multiple_occurrences`, `changed_task_count`,
`changed_tasks_by_token`, `parsed_task_count`, `projected_text_sha256`, `purpose`,
`remaining_known_tokens_decoded`, `remaining_known_tokens_text`, `steps`, `stimulus_class`,
`stimulus_observations`, `string_leaf_count`, `tasks`, `values`. No summary line other than the TOTAL
line contains "finding", and no line contains "FINDING".

A nonzero stimulus in the same observation field does not route to a finding either: line 46 reports
`value_slash_then_raw_slash_junctions=697` for `trailing_slash_sensitivity` while line 47 remains
`TOTAL findings=0 exit=0`.

Negative controls on `/tmp/fpp_lane` (copy of `plans/fixtures`, production untouched):
- pristine copy with `--root /tmp/fpp_lane`: exit 0, summary byte-identical to the live summary;
- `path_prefix` values edited to end `/` (which would make 697 substitution-boundary junctions under
  this profile name): `FINDING
  {"id": "snapshot_tampered", "path": "plans/fixtures/r29/profiles.json"}`, `TOTAL findings=1
  exit=2` — a could-not-evaluate integrity exit, not exit 1;
- coherent rebinding after updating the manifest's `profiles.json` hash (new profiles sha
  `dbb4d6904d228794e9b92c3e9b7758b6caf0e197b8b382aac13a80e8d01d4c04`, manifest sha
  `938c6d33dc7f57f6d83b37784a3ab4eb72176f4150c14c38d361d527c628373f`): `FINDING
  {"id": "manifest_tampered"}`, exit 2.
On the tested CLI surface (`--root` copies), both routes that would change this profile's stimulus
are rejected as exit 2, and no observed stimulus effect — zero or 697 junctions — produced a
projection FINDING or exit 1.

## Mismatches and non-defects

Value mismatches in the assigned quantities: **none**. Three presentation facts were checked and
are not contradictions:
(a) occurrence list order is token-group order, not global offset order (details above; multiset
equal, 1435/1435).
(b) `--summary` abbreviates the JSON key `stimulus_class` as `stimulus=`; the quoted value is
identical.
(c) For `path_prefix` the sole reported observation is structurally 0 because no value ends `/`;
that metric measures `//` junctions and says nothing about the `/prefix` insert, which is evidenced
by the digest and the 1416 changed leaves. [INFERENCE] Reading `0` as "no path effect" would be a
misinterpretation of the metric, not a contradiction of the label.

Units stay distinct and verified: occurrences 1435, changed leaves 1416, changed tasks 812,
task/profile projections 2436, output ordinals 812 with `task_id` 0–811 in order.

Residual unknowns: actual `env_config` values and any README-conformant deployment were not observed
(out of scope per prereg); no runtime/evaluator claim was tested. [INFERENCE] Nothing else bearing on
this profile's projection is unresolved by the pinned bytes.

VERDICT: PASS
