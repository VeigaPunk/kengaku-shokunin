"""Hand-expected synthetic extraction cases from the round-27 E0-E8 table.

These bounded research fixtures pin the policies' edge semantics. They are not a production
untrusted-input interface; the CLI admits only the pinned population before invoking policies.
Each row is (policy id, case name, raw response, expected parsed value).
"""

CASES = (
    # E0: last matched lane fence; a failing fence falls back to raw bare-last.
    ("E0", "last-valid-fence", '```json\n{"v": 1}\n```\n```json\n{"v": 2}\n```', {"v": 2}),
    ("E0", "bad-last-fence-fallback", '```json\n{"v": 1}\n```\n```json\nnot json\n```\n{"v": 3}', {"v": 3}),
    ("E0", "fallback-can-see-earlier-fence", '```json\n{"v": 1}\n```\n```json\nnot json\n```', {"v": 1}),
    ("E0", "valid-null-is-final", '```json\nnull\n```\n{"v": 4}', None),
    ("E0", "non-json-fence-is-bare-candidate", '```python\n{"v": 5}\n```', {"v": 5}),
    ("E0", "no-valid-candidate", 'nothing {broken}', None),

    # E1: first matched lane fence; one raw bare-last fallback, never later-fence retry.
    ("E1", "first-matched-fence", '```json\n{"v": 1}\n```\n```json\n{"v": 2}\n```', {"v": 1}),
    ("E1", "bad-first-does-not-retry-scalar-fence", '```json\n{bad}\n```\n```json\n"later"\n```', None),
    ("E1", "first-null-is-final", '```json\nnull\n```\n{"v": 4}', None),
    ("E1", "json-fence-after-ignored-python", '```python\n{"v": 1}\n```\n```json\n{"v": 2}\n```', {"v": 2}),
    ("E1", "no-fence-raw-bare-last", '{"v": 1} {"v": 2}', {"v": 2}),
    ("E1", "first-fence-beats-trailing-bare", '```json\n{"v": 1}\n```\n{"v": 2}', {"v": 1}),

    # E2: non-overlapping BARE_RE.findall over raw exactly as-is, including fences.
    ("E2", "bare-last-inside-fence", '```json\n{"v": 1}\n```\n{"v": 2}', {"v": 2}),
    ("E2", "findall-retains-nested-whole-object", '{"outer": {"inner": 1}}', {"outer": {"inner": 1}}),
    ("E2", "array-reference-is-last-candidate", '{"v": 1}\nSee [1].', [1]),
    ("E2", "malformed-later-skipped", '{"v": 1} {bad}', {"v": 1}),
    ("E2", "fence-straddling-candidate-not-stripped", '{"outer": "x", "note": ```json\n{"v": 1}\n```}', None),
    ("E2", "delimiter-straddling-json-is-not-cleaned", '{"outer": 1,\n```json\n"inner": 2}\n```', None),
    ("E2", "non-overlapping-array-candidate", '[{"v": 1}] {"last": 2}', {"last": 2}),

    # E3: first successful non-overlapping BARE_RE.findall candidate.
    ("E3", "bare-first", '{"v": 1} {"v": 2}', {"v": 1}),
    ("E3", "invalid-first-skipped", '{bad} {"v": 2}', {"v": 2}),
    ("E3", "first-array", '[1, 2] {"v": 3}', [1, 2]),
    ("E3", "nested-whole-candidate", '{"outer": {"inner": 1}} {"v": 2}', {"outer": {"inner": 1}}),
    ("E3", "fenced-candidate-is-not-excluded", '```json\n{"v": 1}\n```\n{"v": 2}', {"v": 1}),
    ("E3", "no-valid-candidate", '{bad} plain text', None),

    # E4: json.loads(raw.strip()), and nothing else.
    ("E4", "whole-object", ' \n{"v": 1}\t', {"v": 1}),
    ("E4", "strip-form-feed", '\x0c{"v": 2}\x0c', {"v": 2}),
    ("E4", "prose-rejected", 'answer: {"v": 3}', None),
    ("E4", "fence-rejected", '```json\n{"v": 4}\n```', None),
    ("E4", "json-scalar-number", '42', 42),
    ("E4", "json-scalar-string", '"text"', "text"),

    # E5: only the last matched lane fence; invalid/missing means None, no fallback.
    ("E5", "last-fence-parses", '```json\n{"v": 1}\n```', {"v": 1}),
    ("E5", "no-fence-no-fallback", '{"v": 1}', None),
    ("E5", "last-invalid-no-earlier-retry", '```json\n{"v": 1}\n```\n```json\n{"v":}\n```', None),
    ("E5", "invalid-fence-no-bare-fallback", '```json\ninvalid\n```\n{"v": 2}', None),
    ("E5", "last-null-is-none", '```json\nnull\n```\n{"v": 3}', None),
    ("E5", "python-fence-is-not-lane-fence", '```python\n{"v": 4}\n```', None),

    # E6: exact frozen one-token ASCII label regex plus E0's raw bare fallback.
    ("E6", "python-token-label", '```python\n{"v": 1}\n```', {"v": 1}),
    ("E6", "empty-label", '```\n{"v": 2}\n```', {"v": 2}),
    ("E6", "plus-label", '```c++\n{"v": 3}\n```', {"v": 3}),
    ("E6", "space-before-label-not-matched", '``` json\n"scalar"\n```', None),
    ("E6", "extended-info-not-matched", '```json title\n"scalar"\n```', None),
    ("E6", "tilde-fence-not-matched", '~~~json\n"scalar"\n~~~', None),
    ("E6", "invalid-recognized-fence-falls-back", '```text\ninvalid\n```\n{"v": 4}', {"v": 4}),
    ("E6", "two-distinct-any-label-fences", '```python\n{"v": 1}\n```\n```json\n{"v": 2}\n```', {"v": 2}),

    # E7: scan only { and [ positions, return first successful raw_decode.
    ("E7", "deep-nesting-outer-value", 'prefix {"a": {"b": {"c": 1}}} suffix', {"a": {"b": {"c": 1}}}),
    ("E7", "array-before-object", 'text [1, {"a": 2}] {"later": 3}', [1, {"a": 2}]),
    ("E7", "failed-opening-brace-skipped", '{bad {"a": 1}', {"a": 1}),
    ("E7", "only-scalar-is-not-started", '42 "text" true null', None),
    ("E7", "opening-brace-inside-quoted-prose", 'prose says {"a": 1}', {"a": 1}),
    ("E7", "leading-whitespace-scanned-through", '\n \t[2, 3] tail', [2, 3]),

    # E8: left-to-right successful spans; skip starts before each successful end.
    ("E8", "last-top-level-object", '{"v": 1} {"v": 2}', {"v": 2}),
    ("E8", "contained-span-skipped", '{"outer": {"inner": 1}}', {"outer": {"inner": 1}}),
    ("E8", "adjacent-boundary-is-next-span", '{}[]', []),
    ("E8", "crossing-span-start-skipped", '["[", ",1,"]"]', ["[", ",1,"]),
    ("E8", "scalar-after-object-is-not-a-start", '{} 42', {}),
    ("E8", "array-then-object-last", '[1] {"v": 3}', {"v": 3}),
    ("E8", "brace-in-quoted-prose", 'quoted {"a": 1} trailing', {"a": 1}),
    ("E8", "no-brace-or-bracket", 'plain text only', None),
)
