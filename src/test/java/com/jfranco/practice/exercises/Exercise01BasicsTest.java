package com.jfranco.practice.exercises;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class Exercise01BasicsTest {

    private final Exercise01Basics exercise = new Exercise01Basics();

    @Test
    void isEvenShouldReturnTrueForEvenNumbers() {
        assertTrue(exercise.isEven(8));
    }

    @Test
    void isEvenShouldReturnFalseForOddNumbers() {
        assertFalse(exercise.isEven(7));
    }

    @Test
    void sumShouldAddBothValues() {
        assertEquals(11, exercise.sum(5, 6));
    }

    @Test
    void reverseShouldInvertTheString() {
        assertEquals("cba", exercise.reverse("abc"));
    }
}
