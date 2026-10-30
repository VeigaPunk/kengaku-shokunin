SOURCE-URL: https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/main/harden_tests.py
import argparse
import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import yaml
from anthropic import Anthropic
from openai import OpenAI

from util import (
    get_container_contents,
    get_extra_test_files,
)


@dataclass
class HardenResult:
    challenge_name: str
    original_rating: int
    prompt: str
    new_tests: str
    full_response: str


def extract_code_block(response_text: str) -> str:
    """Extract Python code block from the response."""
    # Look for ```python ... ``` blocks
    pattern = r"```python\n(.*?)```"
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fallback: look for any ``` ... ``` block
    pattern = r"```\n?(.*?)```"
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def load_audit_feedback(audit_dir: Path, challenge_name: str) -> str:
    """Load the audit feedback for a specific challenge."""
    audit_file = audit_dir / "audit.txt"
    if not audit_file.exists():
        return ""

    with open(audit_file, "r") as f:
        content = f.read()

    # Parse the audit file to find the feedback for this challenge
    sections = content.split("=" * 60)
    for i, section in enumerate(sections):
        if f"Challenge: {challenge_name}" in section:
            # The feedback is in the next section
            if i + 1 < len(sections):
                return sections[i + 1].strip()
    return ""


def harden_challenge(
    challenge_dir: Path,
    client: OpenAI | Anthropic,
    provider: str,
    original_rating: int,
    audit_feedback: str,
) -> HardenResult | None:
    """Generate hardened test cases for a single challenge."""
    challenge_name = challenge_dir.name
    print(f"Hardening challenge: {challenge_name} (original rating: {original_rating})")

    eval_file = challenge_dir / "eval.yaml"
    if not eval_file.exists():
        print(f"  Challenge {challenge_name} is missing eval.yaml")
        return None

    with open(eval_file, "r") as f:
        eval_data: dict = yaml.safe_load(f)
        task = eval_data.get("variants").get("default").get("prompt")

    # Get container image name from compose.yaml
    compose_file = challenge_dir / "compose.yaml"
    container_contents = ""
    if compose_file.exists():
        with open(compose_file, "r") as f:
            compose_data = yaml.safe_load(f)
            image_name = (
                compose_data.get("services", {}).get("default", {}).get("image", "")
            )
            if image_name:
                container_contents = get_container_contents(image_name)
    else:
        print(f"  Challenge {challenge_name} is missing compose.yaml")

    test_file = challenge_dir / "tests" / "test_outputs.py"
    if not test_file.exists():
        print(f"  Challenge {challenge_name} is missing tests/test_outputs.py")
        return None

    with open(test_file, "r") as f:
        test_code = f.read()

    # Get extra test files (excluding test.sh and test_outputs.py)
    extra_test_files = get_extra_test_files(challenge_dir / "tests")

    solution_file = challenge_dir / "solution" / "solve.sh"
    if not solution_file.exists():
        print(f"  Challenge {challenge_name} is missing solution/solve.sh")
        return None

    with open(solution_file, "r") as f:
        solution_code = f.read()

    # Build extra test files section if present
    extra_test_section = ""
    if extra_test_files:
        extra_test_section = f"""

Extra test files (helper files used by the tests):
{extra_test_files}"""

    prompt = f"""You are a test case hardening expert. You will be given a task, the initial container state, existing test cases, an example solution, and feedback from an auditor about weaknesses in the test coverage.

Your job is to write improved test cases that address the weaknesses identified by the auditor.  However, you should also take care not to introduce any tests that would result in a correct submission failing.

Note that some tasks have lenient requirements, specified in the task description itself.  In such cases, ensure that your tests do not enforce stricter requirements than those stated in the task, even if the auditor suggests doing so.

Finally, in some cases, the auditor may request more test cases of a type that you cannot easily produce (e.g. requesting more sample videos for a task that processes videos). You should ignore such requests from the auditor.

Task:
{task}

Initial container state (files the agent starts with):
{container_contents}

Example solution:
{solution_code}

Current test cases (test_outputs.py):
{test_code}{extra_test_section}

Auditor feedback (explaining why coverage is weak):
{audit_feedback}

Original coverage rating: {original_rating}/5

Please write improved test cases that address the auditor's concerns. Output ONLY the complete Python test file content in a ```python code block. The tests should use pytest and follow the same patterns as the existing tests."""

    print("  Sending to LLM for hardening...")
    try:
        if provider == "anthropic":
            response = client.messages.create(
                model="claude-opus-4-5-20251101",
                max_tokens=16000,
                thinking={"type": "enabled", "budget_tokens": 10000},
                messages=[{"role": "user", "content": prompt}],
            )
            # Find the text block in the response
            response_text = ""
            for block in response.content:
                if block.type == "text":
                    response_text = block.text
                    break
        else:
            response = client.responses.create(
                model="gpt-5.2-2025-12-11",
                input=prompt,
                reasoning={"effort": "medium"},
            )
            response_text = response.output_text
    except Exception as e:
        print(f"  ERROR calling LLM for {challenge_name}: {e}")
        return None

    new_tests = extract_code_block(response_text)

    return HardenResult(
        challenge_name=challenge_name,
        original_rating=original_rating,
        prompt=prompt,
        new_tests=new_tests,
        full_response=response_text,
    )


def append_result(result: HardenResult, run_dir: Path) -> None:
    """Append a single hardening result to the output files."""
    # Append to summary.txt
    summary_file = run_dir / "summary.txt"
    with open(summary_file, "a") as f:
        f.write(f"Challenge: {result.challenge_name}\n")
        f.write(f"Original rating: {result.original_rating}/5\n")
        f.write(f"New tests generated: {'Yes' if result.new_tests else 'No'}\n")
        f.write("-" * 40 + "\n\n")

    # Append to responses.txt
    responses_file = run_dir / "responses.txt"
    with open(responses_file, "a") as f:
        f.write(f"{'=' * 60}\n")
        f.write(f"Challenge: {result.challenge_name}\n")
        f.write(f"Original rating: {result.original_rating}/5\n")
        f.write(f"{'=' * 60}\n\n")
        f.write(result.full_response)
        f.write("\n\n")

    # Append to prompts.txt
    prompts_file = run_dir / "prompts.txt"
    with open(prompts_file, "a") as f:
        f.write(f"{'=' * 60}\n")
        f.write(f"Challenge: {result.challenge_name}\n")
        f.write(f"{'=' * 60}\n\n")
        f.write(result.prompt)
        f.write("\n\n")

    # Write individual hardened test file
    if result.new_tests:
        tests_dir = run_dir / "hardened_tests"
        tests_dir.mkdir(exist_ok=True)
        test_file = tests_dir / f"{result.challenge_name}_test_outputs.py"
        with open(test_file, "w") as f:
            f.write(result.new_tests)


def write_final_summary(results: list[HardenResult], run_dir: Path) -> None:
    """Write final summary to console."""
    print(f"\n{'=' * 60}")
    print("HARDENING SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total challenges processed: {len(results)}")
    successful = sum(1 for r in results if r.new_tests)
    print(f"Successfully generated new tests: {successful}")
    print(f"\nResults saved to: {run_dir}")
    print("  - summary.txt")
    print("  - responses.txt")
    print("  - prompts.txt")
    print("  - hardened_tests/")


def main():
    parser = argparse.ArgumentParser(
        description="Harden test cases based on audit results"
    )
    parser.add_argument(
        "--audit-dir",
        type=str,
        required=True,
        help="Path to the audit results directory (e.g., audit_results/20260119_114803)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
        help="Harden challenges with rating at or below this threshold (default: 3)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of challenges to process",
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=1,
        help="Number of parallel workers (default: 1)",
    )
    parser.add_argument(
        "--challenge",
        type=str,
        default=None,
        help="Process a specific challenge by name (ignores threshold)",
    )
    parser.add_argument(
        "--provider",
        type=str,
        choices=["openai", "anthropic"],
        default="anthropic",
        help="LLM provider to use (default: openai)",
    )
    args = parser.parse_args()

    base = Path(__file__).parent / "challenges"
    output_dir = Path(__file__).parent / "harden_results"

    # Load audit results
    audit_dir = Path(args.audit_dir)
    if not audit_dir.is_absolute():
        audit_dir = Path(__file__).parent / args.audit_dir

    ratings_file = audit_dir / "ratings.json"
    if not ratings_file.exists():
        print(f"Ratings file not found: {ratings_file}")
        return

    with open(ratings_file, "r") as f:
        ratings: dict[str, int] = json.load(f)

    # Filter challenges based on threshold or specific challenge
    if args.challenge:
        if args.challenge not in ratings:
            print(f"Challenge {args.challenge} not found in audit results")
            print("Available challenges:")
            for name in sorted(ratings.keys()):
                print(f"  - {name}: {ratings[name]}/5")
            return
        challenges_to_harden = [(args.challenge, ratings.get(args.challenge, 0))]
        print(f"Processing specific challenge: {args.challenge}")
    else:
        challenges_to_harden = [
            (name, rating)
            for name, rating in ratings.items()
            if rating is not None and rating <= args.threshold
        ]
        challenges_to_harden.sort(
            key=lambda x: (x[1], x[0])
        )  # Sort by rating, then name
        print(
            f"Found {len(challenges_to_harden)} challenges with rating <= {args.threshold}"
        )

    if args.limit:
        challenges_to_harden = challenges_to_harden[: args.limit]
        print(f"Limiting to {args.limit} challenges")

    if not challenges_to_harden:
        print("No challenges to harden")
        return

    print(f"Using provider: {args.provider}")

    # Create output directory at the start
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = output_dir / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"Saving results to: {run_dir}")

    # Write header to summary file
    summary_file = run_dir / "summary.txt"
    with open(summary_file, "w") as f:
        f.write("TEST HARDENING SUMMARY\n")
        f.write("=" * 60 + "\n\n")

    # Lock for thread-safe file writes
    write_lock = threading.Lock()

    def create_client() -> OpenAI | Anthropic:
        if args.provider == "anthropic":
            return Anthropic()
        return OpenAI()

    results: list[HardenResult] = []

    if args.parallel > 1:
        print(f"Running with {args.parallel} parallel workers")

        def harden_with_client(
            challenge_info: tuple[str, int],
        ) -> HardenResult | None:
            challenge_name, rating = challenge_info
            challenge_dir = base / challenge_name
            if not challenge_dir.exists():
                print(f"  Challenge directory not found: {challenge_name}")
                return None
            client = create_client()
            audit_feedback = load_audit_feedback(audit_dir, challenge_name)
            return harden_challenge(
                challenge_dir, client, args.provider, rating, audit_feedback
            )

        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            futures = {
                executor.submit(harden_with_client, c): c for c in challenges_to_harden
            }
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                    with write_lock:
                        append_result(result, run_dir)
        results.sort(key=lambda r: r.challenge_name)
    else:
        client = create_client()
        for challenge_name, rating in challenges_to_harden:
            challenge_dir = base / challenge_name
            if not challenge_dir.exists():
                print(f"  Challenge directory not found: {challenge_name}")
                continue
            audit_feedback = load_audit_feedback(audit_dir, challenge_name)
            result = harden_challenge(
                challenge_dir, client, args.provider, rating, audit_feedback
            )
            if result:
                results.append(result)
                append_result(result, run_dir)

    if results:
        write_final_summary(results, run_dir)
    else:
        print("No challenges were successfully hardened.")


if __name__ == "__main__":
    main()
