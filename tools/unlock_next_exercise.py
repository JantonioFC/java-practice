#!/usr/bin/env python3
"""Unlock the next exercise only when the previous one passes.

This script keeps the learning flow sequential:
- scans tools/templates for dynamic exercise structures
- validates the previous exercise test class is green
- creates the next exercise skeleton and its guiding tests
- provides a reset option to clear practice state
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_EXERCISES = ROOT / "src" / "main" / "java" / "com" / "jfranco" / "practice" / "exercises"
TEST_EXERCISES = ROOT / "src" / "test" / "java" / "com" / "jfranco" / "practice" / "exercises"
TEMPLATES_DIR = ROOT / "tools" / "templates"


@dataclass(frozen=True)
class Exercise:
    number: int
    name: str
    main_filename: str
    test_filename: str
    previous_test_class: str | None
    is_template_only: bool


def get_exercise_list() -> list[Exercise]:
    """Dynamically scan both active files and templates to build a sequential list."""
    exercises_map: dict[int, dict] = {}

    # 1. Scan templates
    if TEMPLATES_DIR.exists():
        for p in TEMPLATES_DIR.glob("Exercise*.java"):
            if p.name.endswith("Test.java"):
                continue
            match = re.match(r"Exercise(\d+)([A-Za-z0-9_]+)", p.stem)
            if match:
                num = int(match.group(1))
                exercises_map[num] = {
                    "number": num,
                    "name": p.stem,
                    "main_filename": p.name,
                    "test_filename": f"{p.stem}Test.java",
                    "is_template_only": True,
                }

    # 2. Scan active files in MAIN_EXERCISES
    if MAIN_EXERCISES.exists():
        for p in MAIN_EXERCISES.glob("Exercise*.java"):
            if p.name.endswith("Test.java"):
                continue
            match = re.match(r"Exercise(\d+)([A-Za-z0-9_]+)", p.stem)
            if match:
                num = int(match.group(1))
                # Active files override template status or establish the base
                if num in exercises_map:
                    exercises_map[num]["is_template_only"] = False
                else:
                    exercises_map[num] = {
                        "number": num,
                        "name": p.stem,
                        "main_filename": p.name,
                        "test_filename": f"{p.stem}Test.java",
                        "is_template_only": False,
                    }

    # Sort sequentially by exercise number
    sorted_numbers = sorted(exercises_map.keys())
    exercises_list: list[dict] = [exercises_map[n] for n in sorted_numbers]

    # Assign previous test class dynamically based on sequence
    final_list: list[Exercise] = []
    for i, ex in enumerate(exercises_list):
        prev_test = f"{exercises_list[i-1]['name']}Test" if i > 0 else None
        final_list.append(
            Exercise(
                number=ex["number"],
                name=ex["name"],
                main_filename=ex["main_filename"],
                test_filename=ex["test_filename"],
                previous_test_class=prev_test,
                is_template_only=ex["is_template_only"],
            )
        )

    return final_list


def run_previous_test(test_class: str) -> bool:
    """Run Maven test for the specified class and check if it passes."""
    command = ["./mvnw", "-q", f"-Dtest={test_class}", "test"]
    print(f"Ejecutando pruebas de validación para {test_class}...")
    result = subprocess.run(command, cwd=ROOT, check=False)
    return result.returncode == 0


def unlock(exercise: Exercise) -> bool:
    """Copy the dynamic templates to active source and test directories."""
    main_path = MAIN_EXERCISES / exercise.main_filename
    test_path = TEST_EXERCISES / exercise.test_filename

    # Safety double check
    if main_path.exists() or test_path.exists():
        print(f"El ejercicio ya se encuentra desbloqueado: {exercise.name}")
        return True

    # Validate previous exercise tests if applicable
    if exercise.previous_test_class:
        print(f"Validando ejercicio anterior: {exercise.previous_test_class}...")
        if not run_previous_test(exercise.previous_test_class):
            print("\n❌ NO SE PUEDE DESBLOQUEAR EL SIGUIENTE NIVEL.")
            print(f"Razón: Los tests de {exercise.previous_test_class} no están pasando todavía.")
            print("Corregí tu solución actual y volvé a intentar.")
            return False

    # Read templates and write to source
    template_main = TEMPLATES_DIR / exercise.main_filename
    template_test = TEMPLATES_DIR / exercise.test_filename

    if not template_main.exists() or not template_test.exists():
        print(f"❌ Error: Archivos de plantilla no encontrados en {TEMPLATES_DIR}")
        return False

    MAIN_EXERCISES.mkdir(parents=True, exist_ok=True)
    TEST_EXERCISES.mkdir(parents=True, exist_ok=True)

    main_path.write_text(template_main.read_text(encoding="utf-8"), encoding="utf-8")
    test_path.write_text(template_test.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"\n🎉 ¡EJERCICIO DESBLOQUEADO CON ÉXITO!")
    print(f"  👉 Creado: src/main/java/.../exercises/{exercise.main_filename}")
    print(f"  👉 Creado: src/test/java/.../exercises/{exercise.test_filename}")
    print("\n¡A trabajar! Implementá los métodos pendientes y corré los tests con la task de VS Code.")
    return True


def reset_workspace() -> int:
    """Delete all unlocked exercises greater than Exercise01Basics."""
    print("🧹 Iniciando limpieza y reinicio del workspace...")
    exercises = get_exercise_list()
    
    deleted_count = 0
    for ex in exercises:
        if ex.number > 1:
            main_path = MAIN_EXERCISES / ex.main_filename
            test_path = TEST_EXERCISES / ex.test_filename
            
            if main_path.exists():
                main_path.unlink()
                print(f"  🗑️  Eliminado ejercicio: {ex.main_filename}")
                deleted_count += 1
            if test_path.exists():
                test_path.unlink()
                print(f"  🗑️  Eliminado test: {ex.test_filename}")
                
    if deleted_count > 0:
        print(f"\n✅ Workspace reiniciado con éxito. Se eliminaron {deleted_count} ejercicio(s).")
        print("Tu lección activa ahora vuelve a ser: Exercise01Basics.")
    else:
        print("\nEl workspace ya se encuentra en su estado inicial (solo Exercise01Basics activo).")
        
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gestiona el desbloqueo secuencial y el estado de la práctica de Java."
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Limpia el workspace eliminando los ejercicios desbloqueados mayores a 01."
    )
    args = parser.parse_args()

    if args.reset:
        return reset_workspace()

    exercises = get_exercise_list()
    
    # Find the first exercise that is still "template only" (not in src/main/java)
    pending_exercise = None
    for ex in exercises:
        if ex.is_template_only:
            pending_exercise = ex
            break

    if not pending_exercise:
        print("🎉 ¡Excelente! No quedan más ejercicios pendientes por desbloquear.")
        print("Si cargás un PDF nuevo en materials/inbox, se generarán nuevos desafíos automáticamente.")
        return 0

    return 0 if unlock(pending_exercise) else 1


if __name__ == "__main__":
    raise SystemExit(main())
