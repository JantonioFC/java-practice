package com.jfranco.practice.exercises;

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
