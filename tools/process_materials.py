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
import json
import os
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

import requests

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
    best_topic = None
    max_count = 0
    for topic in TOPICS:
        count = sum(haystack.count(keyword) for keyword in topic.keywords)
        if count > max_count:
            max_count = count
            best_topic = topic
    if best_topic and max_count > 0:
        return best_topic
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


def load_api_key() -> str | None:
    """Load GEMINI_API_KEY from environment or a local .env file."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    env_file = ROOT / ".env"
    if env_file.exists():
        try:
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() == "GEMINI_API_KEY":
                        val = v.strip()
                        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                            val = val[1:-1]
                        return val
        except Exception:
            pass
    return None


def get_next_exercise_index() -> int:
    """Determine the next sequential exercise number based on templates and src/."""
    highest = 1
    pattern = re.compile(r"Exercise(\d+)")
    
    templates_dir = ROOT / "tools" / "templates"
    if templates_dir.exists():
        for p in templates_dir.glob("Exercise*.java"):
            m = pattern.match(p.stem)
            if m:
                highest = max(highest, int(m.group(1)))
                
    main_dir = ROOT / "src" / "main" / "java" / "com" / "jfranco" / "practice" / "exercises"
    if main_dir.exists():
        for p in main_dir.glob("Exercise*.java"):
            m = pattern.match(p.stem)
            if m:
                highest = max(highest, int(m.group(1)))
                
    return highest + 1


def generate_java_exercises(api_key: str, next_num: int, topic: TopicSpec, extracted_text: str) -> tuple[str, str, str] | None:
    """Call the Gemini API using requests to generate new exercise skeletons and tests."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    system_instruction = (
        "Sos un profesor universitario experto de Java y un asistente de IA de elite.\n"
        "Tu tarea es analizar el texto extraído del PDF de estudio y diseñar un ejercicio de programación Java "
        "secuencial y una suite de pruebas JUnit 5.\n\n"
        "REQUISITOS CRÍTICOS:\n"
        "1. Debés responder únicamente con un objeto JSON que coincida exactamente con este esquema:\n"
        "{\n"
        "  \"exercise_name\": \"ExerciseXX[TopicName]\",\n"
        "  \"java_code\": \"package com.jfranco.practice.exercises;\\n\\n...\",\n"
        "  \"test_code\": \"package com.jfranco.practice.exercises;\\n\\n...\"\n"
        "}\n"
        "Reemplazá XX por el índice de ejercicio provisto y [TopicName] por la representación en inglés en formato camelCase (ej. '03' y 'Conditionals').\n"
        "2. La clase del ejercicio debe tener exactamente 3 métodos sin implementar que representen dificultades progresivas (Fácil, Medio, Difícil) sobre el tema en cuestión.\n"
        "3. CADA MÉTODO debe lanzar 'throw new UnsupportedOperationException(\"Implement [nombre_metodo]\");'.\n"
        "4. La documentación (JavaDoc) de cada método DEBE ser sumamente detallada, clara y con un enfoque fuertemente pedagógico. "
        "Debe estar en español rioplatense natural (usando voseo: 'Implementá', 'creá', 'retorná', 'evaluá', 'pensá'). "
        "Cada JavaDoc debe estructurarse obligatoriamente de la siguiente forma:\n"
        "   - **Explicación Clara y Detallada**: Qué debe hacer el método exactamente y cuál es el objetivo de aprendizaje.\n"
        "   - **Lógica Paso a Paso**: Guía o pista de cómo estructurar la solución mentalmente.\n"
        "   - **Casos Borde a Considerar**: Qué límites, valores extremos o comportamientos excepcionales hay que cuidar.\n"
        "   - **Ejemplos Prácticos**: Casos de prueba con entradas concretas y sus correspondientes retornos esperados.\n"
        "5. La clase de pruebas debe utilizar JUnit 5 y contener pruebas exhaustivas (al menos 3 tests por método cubriendo casos normales, bordes y excepciones si aplica).\n"
    )

    user_prompt = (
        f"Analizá el siguiente texto y generá el Ejercicio número {next_num:02d} sobre el tema '{topic.label}'.\n\n"
        f"Índice a utilizar en el nombre de la clase: {next_num:02d}\n"
        f"Tema: {topic.label}\n\n"
        f"Texto extraído del material de estudio:\n{extracted_text[:6000]}"
    )
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "exercise_name": {"type": "STRING"},
                    "java_code": {"type": "STRING"},
                    "test_code": {"type": "STRING"}
                },
                "required": ["exercise_name", "java_code", "test_code"]
            }
        },
        "systemInstruction": {
            "parts": [
                {"text": system_instruction}
            ]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        data = response.json()
        candidate = data["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(candidate)
        return parsed["exercise_name"], parsed["java_code"], parsed["test_code"]
    except Exception as exc:
        print(f"⚠️ Error al llamar a la API de Gemini: {exc}", file=sys.stderr)
        return None


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

    # Write Markdown notes
    note_path.write_text(note_markdown, encoding="utf-8")
    practice_path.write_text(practice_markdown, encoding="utf-8")
    
    # Try dynamic exercise generation using Gemini API
    api_key = load_api_key()
    if api_key:
        next_num = get_next_exercise_index()
        print(f"🤖 [IA] Conexión establecida. Generando ejercicio Java {next_num:02d} para el tema '{topic.label}'...")
        generation = generate_java_exercises(api_key, next_num, topic, extracted_text)
        if generation:
            ex_name, java_code, test_code = generation
            
            templates_dir = ROOT / "tools" / "templates"
            templates_dir.mkdir(parents=True, exist_ok=True)
            
            java_path = templates_dir / f"{ex_name}.java"
            test_path = templates_dir / f"{ex_name}Test.java"
            
            java_path.write_text(java_code, encoding="utf-8")
            test_path.write_text(test_code, encoding="utf-8")
            
            print(f"✅ [IA] ¡Desafío de código generado exitosamente! Guardado en {templates_dir.name}/{ex_name}.java")
        else:
            print("⚠️ [IA] No se pudieron generar las plantillas de código Java. Se preservan solo los apuntes teóricos.")
    else:
        print("⚠️ [IA] Saltando generación dinámica de código. GEMINI_API_KEY no encontrada en entorno ni en archivo .env.")
        print("💡 Para activar el modo inteligente, agregá GEMINI_API_KEY=tu_clave en un archivo .env en la raíz del proyecto.")

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
