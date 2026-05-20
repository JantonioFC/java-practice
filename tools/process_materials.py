#!/usr/bin/env python3
"""Process university PDFs into topic notes and practice sheets.

Workflow:
- read every PDF in materials/inbox
- classify it by filename and extracted text
- convert it to Markdown using pdftotext
- archive the original PDF under materials/topics/<topic>/source
- generate a study note and a practice sheet in Markdown
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INBOX = ROOT / "materials" / "inbox"
DEFAULT_TOPICS = ROOT / "materials" / "topics"
UNCLASSIFIED_FOLDER = "99-no-clasificado"


@dataclass(frozen=True)
class TopicSpec:
    folder: str
    label: str
    keywords: tuple[str, ...]
    summary: str
    exercises: tuple[str, ...]
    common_mistakes: tuple[str, ...]


TOPICS: tuple[TopicSpec, ...] = (
    TopicSpec(
        folder="01-variables",
        label="Variables",
        keywords=("variable", "variables"),
        summary="Declaring values, assigning data, choosing types, and reading state from memory.",
        exercises=(
            "Declare three variables with different primitive types and explain why each type fits.",
            "Given a short code snippet, identify the value stored in each variable after every line.",
            "Refactor a block of repeated literals into named variables and justify the names you chose.",
        ),
        common_mistakes=(
            "Confusing declaration with assignment.",
            "Choosing a type that is too small or too specific for the value.",
            "Using vague names that hide the purpose of the value.",
        ),
    ),
    TopicSpec(
        folder="02-operadores",
        label="Operadores",
        keywords=("operador", "operadores", "operaciones matematicas", "operaciones aritmeticas"),
        summary="Arithmetic, relational, logical, and assignment operators plus precedence rules.",
        exercises=(
            "Predict the result of an expression that mixes arithmetic and relational operators.",
            "Rewrite a boolean expression using parentheses so the evaluation order is explicit.",
            "Write a method that returns true only when a number is inside a given range.",
        ),
        common_mistakes=(
            "Forgetting operator precedence.",
            "Mixing logical and bitwise operators without knowing the difference.",
            "Assuming an expression returns the same type as its inputs.",
        ),
    ),
    TopicSpec(
        folder="03-condicionales",
        label="Condicionales",
        keywords=("condicional", "condicionales", "if", "else", "switch"),
        summary="Decision making with if, else, else if, ternary expressions, and switch statements.",
        exercises=(
            "Classify a student grade into approved, recovery, or failed.",
            "Implement a menu handler using switch for at least four options.",
            "Convert a nested if structure into a clearer version with early returns.",
        ),
        common_mistakes=(
            "Writing conditions that overlap or leave gaps.",
            "Using nested if statements when a simpler branch is enough.",
            "Ignoring edge cases such as equal limits or empty input.",
        ),
    ),
    TopicSpec(
        folder="04-iteraciones",
        label="Iteraciones",
        keywords=("iteracion", "iteraciones", "while", "for", "do while", "loop"),
        summary="Repetition with while, for, do-while, and the ability to stop or continue a loop.",
        exercises=(
            "Sum the numbers from 1 to N using a loop.",
            "Count how many even numbers appear in a list or range.",
            "Write a loop that stops when a sentinel value is reached.",
        ),
        common_mistakes=(
            "Forgetting the loop update and creating an infinite loop.",
            "Choosing the wrong loop structure for the problem.",
            "Not handling empty or boundary values before iterating.",
        ),
    ),
    TopicSpec(
        folder="05-funciones-y-modularidad",
        label="Funciones y modularidad",
        keywords=("funcion", "funciones", "modularidad", "metodo", "metodos"),
        summary="Breaking logic into methods, keeping responsibilities small, and making code reusable.",
        exercises=(
            "Extract repeated validation logic into a method and define its contract.",
            "Split a long procedure into three methods with clear responsibilities.",
            "Design a method that receives input and returns a computed result without printing anything.",
        ),
        common_mistakes=(
            "Creating methods that do too many things at once.",
            "Choosing names that hide the method's responsibility.",
            "Printing inside methods that should only compute values.",
        ),
    ),
)


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = "".join(char for char in normalized if not unicodedata.combining(char))
    return ascii_text.lower()


def slugify(value: str) -> str:
    normalized = normalize_text(value)
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    return normalized or "material"


def extract_pdf_text(pdf_path: Path) -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = Path(temp_dir) / f"{pdf_path.stem}.txt"
        command = [
            "pdftotext",
            "-layout",
            "-nopgbrk",
            "-enc",
            "UTF-8",
            str(pdf_path),
            str(output_path),
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path.read_text(encoding="utf-8", errors="ignore")


def classify_topic(pdf_path: Path, extracted_text: str) -> TopicSpec:
    haystack = normalize_text(f"{pdf_path.name}\n{extracted_text[:4000]}")
    for topic in TOPICS:
        if any(keyword in haystack for keyword in topic.keywords):
            return topic
    return TopicSpec(
        folder=UNCLASSIFIED_FOLDER,
        label="No clasificado",
        keywords=tuple(),
        summary="Material that did not match the known topic rules.",
        exercises=(
            "Read the material and define the main concept in one sentence.",
            "Extract three key ideas that should become exercises.",
            "Choose the correct topic folder once the content becomes clear.",
        ),
        common_mistakes=(
            "Leaving the material without review.",
            "Trying to generate exercises before understanding the topic.",
            "Forgetting to classify the document after reading it.",
        ),
    )


def build_note_markdown(pdf_path: Path, topic: TopicSpec, extracted_text: str) -> str:
    return dedent(
        f"""\
        # {pdf_path.stem}

        - Source: {pdf_path.name}
        - Topic: {topic.label}
        - Status: auto-converted from PDF

        ## Auto summary
        {topic.summary}

        ## Extracted text
        {extracted_text.strip()}
        """
    ).strip() + "\n"


def build_practice_markdown(pdf_path: Path, topic: TopicSpec) -> str:
    exercises = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(topic.exercises))
    mistakes = "\n".join(f"- {item}" for item in topic.common_mistakes)
    return dedent(
        f"""\
        # Practice sheet: {pdf_path.stem}

        ## What this topic should reinforce
        {topic.summary}

        ## Exercises
        {exercises}

        ## How to review your answer
        - Start from the tests or expected outcome.
        - Keep the solution small and focused.
        - Explain what changed and why it works.

        ## Common mistakes to watch for
        {mistakes}
        """
    ).strip() + "\n"


def ensure_topic_layout(topic_root: Path) -> dict[str, Path]:
    paths = {
        "root": topic_root,
        "source": topic_root / "source",
        "notes": topic_root / "notes",
        "practice": topic_root / "practice",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def process_pdf(pdf_path: Path, topics_root: Path, dry_run: bool = False) -> str:
    extracted_text = extract_pdf_text(pdf_path)
    topic = classify_topic(pdf_path, extracted_text)
    topic_root = topics_root / topic.folder
    layout = ensure_topic_layout(topic_root)

    slug = slugify(pdf_path.stem)
    note_path = layout["notes"] / f"{slug}.md"
    practice_path = layout["practice"] / f"{slug}.md"
    archived_pdf_path = layout["source"] / pdf_path.name

    note_markdown = build_note_markdown(pdf_path, topic, extracted_text)
    practice_markdown = build_practice_markdown(pdf_path, topic)

    if dry_run:
        return f"DRY-RUN: {pdf_path.name} -> {topic.folder}"

    note_path.write_text(note_markdown, encoding="utf-8")
    practice_path.write_text(practice_markdown, encoding="utf-8")
    shutil.move(str(pdf_path), str(archived_pdf_path))

    return f"{pdf_path.name} -> {topic.folder}"


def process_inbox(inbox: Path, topics_root: Path, dry_run: bool = False) -> list[str]:
    pdf_files = sorted(inbox.glob("*.pdf"))
    if not pdf_files:
        return []

    results: list[str] = []
    for pdf_file in pdf_files:
        try:
            results.append(process_pdf(pdf_file, topics_root, dry_run=dry_run))
        except subprocess.CalledProcessError as exc:
            print(f"Failed to convert {pdf_file.name}: {exc}", file=sys.stderr)
            raise

    return results


def watch_inbox(inbox: Path, topics_root: Path, dry_run: bool = False, interval_seconds: int = 5) -> int:
    print(f"Watching {inbox} for PDFs... Press Ctrl+C to stop.")
    try:
        while True:
            results = process_inbox(inbox, topics_root, dry_run=dry_run)
            for line in results:
                print(line)
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("Stopped watching inbox.")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert PDFs from materials/inbox into Markdown notes and practice sheets.",
    )
    parser.add_argument("--inbox", type=Path, default=DEFAULT_INBOX, help="Inbox folder with incoming PDFs.")
    parser.add_argument("--topics", type=Path, default=DEFAULT_TOPICS, help="Target topic folder.")
    parser.add_argument("--dry-run", action="store_true", help="Show the planned actions without writing files.")
    parser.add_argument("--watch", action="store_true", help="Keep watching inbox and process new PDFs automatically.")
    parser.add_argument(
        "--interval-seconds",
        type=int,
        default=5,
        help="Polling interval used with --watch.",
    )
    args = parser.parse_args()

    inbox = args.inbox
    topics_root = args.topics

    if not inbox.exists():
        print(f"Inbox folder not found: {inbox}", file=sys.stderr)
        return 1

    if args.watch:
        return watch_inbox(inbox, topics_root, dry_run=args.dry_run, interval_seconds=args.interval_seconds)

    results = process_inbox(inbox, topics_root, dry_run=args.dry_run)
    if not results:
        print("No PDFs found in inbox.")
        return 0

    for line in results:
        print(line)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
