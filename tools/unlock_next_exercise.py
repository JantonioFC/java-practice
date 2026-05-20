#!/usr/bin/env python3
"""Unlock the next exercise only when the previous one passes.

This script keeps the learning flow sequential:
- validates the previous exercise test class is green
- creates the next exercise skeleton and its guiding tests
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_EXERCISES = ROOT / "src" / "main" / "java" / "com" / "jfranco" / "practice" / "exercises"
TEST_EXERCISES = ROOT / "src" / "test" / "java" / "com" / "jfranco" / "practice" / "exercises"


@dataclass(frozen=True)
class ExerciseTemplate:
    previous_test_class: str
    main_filename: str
    test_filename: str
    main_source: str
    test_source: str


TEMPLATES: tuple[ExerciseTemplate, ...] = (
    ExerciseTemplate(
        previous_test_class="Exercise01BasicsTest",
        main_filename="Exercise02Operators.java",
        test_filename="Exercise02OperatorsTest.java",
        main_source="""package com.jfranco.practice.exercises;

/**
 * Ejercicio 02 — Operadores
 *
 * Implementá cada método reemplazando el `throw` por la lógica correcta.
 * Usá solo operadores (aritméticos, relacionales, lógicos) — sin métodos de biblioteca.
 * Corré los tests para verificar tu solución: ./mvnw test
 */
public class Exercise02Operators {

    // Devuelve true si value está entre min y max (inclusive en ambos extremos).
    // Ejemplo: isWithinRange(5, 1, 10) → true  |  isWithinRange(11, 1, 10) → false
    public boolean isWithinRange(int value, int min, int max) {
        throw new UnsupportedOperationException(\"Implement isWithinRange\");
    }

    // Devuelve el mayor de los dos números.
    // Ejemplo: maxOfTwo(4, 9) → 9
    public int maxOfTwo(int left, int right) {
        throw new UnsupportedOperationException(\"Implement maxOfTwo\");
    }

    // Devuelve true si ambos números tienen el mismo signo (ambos positivos o ambos negativos).
    // El cero se considera positivo.
    // Ejemplo: sameSign(3, 8) → true  |  sameSign(-3, 8) → false
    public boolean sameSign(int left, int right) {
        throw new UnsupportedOperationException(\"Implement sameSign\");
    }
}
""",
        test_source="""package com.jfranco.practice.exercises;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class Exercise02OperatorsTest {

    private final Exercise02Operators exercise = new Exercise02Operators();

    @Test
    void isWithinRangeShouldReturnTrueForValueInsideBounds() {
        assertTrue(exercise.isWithinRange(5, 1, 10));
    }

    @Test
    void isWithinRangeShouldReturnFalseForValueOutsideBounds() {
        assertFalse(exercise.isWithinRange(11, 1, 10));
    }

    @Test
    void maxOfTwoShouldReturnTheGreatestValue() {
        assertEquals(9, exercise.maxOfTwo(4, 9));
    }

    @Test
    void sameSignShouldReturnTrueWhenBothArePositive() {
        assertTrue(exercise.sameSign(3, 8));
    }

    @Test
    void sameSignShouldReturnFalseWhenSignsDiffer() {
        assertFalse(exercise.sameSign(-3, 8));
    }
}
""",
    ),
)


def run_previous_test(test_class: str) -> bool:
    command = ["mvn", "-q", f"-Dtest={test_class}", "test"]
    result = subprocess.run(command, cwd=ROOT, check=False)
    return result.returncode == 0


def unlock(template: ExerciseTemplate) -> bool:
    main_path = MAIN_EXERCISES / template.main_filename
    test_path = TEST_EXERCISES / template.test_filename

    if main_path.exists() or test_path.exists():
        print(f"Exercise already unlocked: {template.main_filename}")
        return True

    print(f"Validating previous test class: {template.previous_test_class} ...")
    if not run_previous_test(template.previous_test_class):
        print("Cannot unlock next exercise.")
        print(f"Reason: {template.previous_test_class} is not passing yet.")
        print("Fix the previous exercise and run this command again.")
        return False

    main_path.write_text(template.main_source, encoding="utf-8")
    test_path.write_text(template.test_source, encoding="utf-8")

    print(f"Unlocked: {template.main_filename}")
    print(f"Unlocked: {template.test_filename}")
    print("Next step: implement the methods and run mvn test.")
    return True


def main() -> int:
    for template in TEMPLATES:
        main_exists = (MAIN_EXERCISES / template.main_filename).exists()
        test_exists = (TEST_EXERCISES / template.test_filename).exists()
        if not main_exists and not test_exists:
            return 0 if unlock(template) else 1

    print("No pending exercise templates to unlock.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
