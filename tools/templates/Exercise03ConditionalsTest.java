package com.jfranco.practice.exercises;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Exercise03ConditionalsTest {

    private final Exercise03Conditionals exercise = new Exercise03Conditionals();

    @Test
    void testEsParNumeroPositivo() {
        assertEquals("PAR", exercise.esParOImpar(4), "4 debería ser PAR");
    }

    @Test
    void testEsImparNumeroPositivo() {
        assertEquals("IMPAR", exercise.esParOImpar(7), "7 debería ser IMPAR");
    }

    @Test
    void testEsParCero() {
        assertEquals("PAR", exercise.esParOImpar(0), "0 debería ser PAR");
    }

    @Test
    void testEsParNegativo() {
        assertEquals("PAR", exercise.esParOImpar(-2), "-2 debería ser PAR");
    }

    @Test
    void testEsImparNegativo() {
        assertEquals("IMPAR", exercise.esParOImpar(-3), "-3 debería ser IMPAR");
    }

    @Test
    void testCalificacionPromocionadoLimiteInferior() {
        assertEquals("PROMOCIONADO", exercise.evaluarCalificacion(7), "7 debería ser PROMOCIONADO");
    }

    @Test
    void testCalificacionPromocionadoMaximo() {
        assertEquals("PROMOCIONADO", exercise.evaluarCalificacion(10), "10 debería ser PROMOCIONADO");
    }

    @Test
    void testCalificacionRegularLimiteInferior() {
        assertEquals("REGULAR", exercise.evaluarCalificacion(4), "4 debería ser REGULAR");
    }

    @Test
    void testCalificacionRegularLimiteSuperior() {
        assertEquals("REGULAR", exercise.evaluarCalificacion(6), "6 debería ser REGULAR");
    }

    @Test
    void testCalificacionDesaprobadoLimiteSuperior() {
        assertEquals("DESAPROBADO", exercise.evaluarCalificacion(3), "3 debería ser DESAPROBADO");
    }

    @Test
    void testCalificacionDesaprobadoMinimo() {
        assertEquals("DESAPROBADO", exercise.evaluarCalificacion(1), "1 debería ser DESAPROBADO");
    }

    @Test
    void testAnioBisiestoDivisiblePor4NoPor100() {
        assertTrue(exercise.esAnioBisiesto(2004), "2004 debería ser bisiesto");
    }

    @Test
    void testAnioNoBisiestoNoDivisiblePor4() {
        assertFalse(exercise.esAnioBisiesto(2003), "2003 no debería ser bisiesto");
    }

    @Test
    void testAnioNoBisiestoDivisiblePor100NoPor400() {
        assertFalse(exercise.esAnioBisiesto(1900), "1900 no debería ser bisiesto");
    }

    @Test
    void testAnioBisiestoDivisiblePor400() {
        assertTrue(exercise.esAnioBisiesto(2000), "2000 debería ser bisiesto");
    }

    @Test
    void testAnioBisiestoOtroCaso() {
        assertTrue(exercise.esAnioBisiesto(1600), "1600 debería ser bisiesto");
    }

    @Test
    void testAnioNoBisiestoOtroCaso() {
        assertFalse(exercise.esAnioBisiesto(2019), "2019 no debería ser bisiesto");
    }

    @Test
    void testAnioBisiestoDivisiblePor4NoPor1002() {
        assertTrue(exercise.esAnioBisiesto(2024), "2024 debería ser bisiesto");
    }

    @Test
    void testAnioNoBisiestoDivisiblePor100NoPor4002() {
        assertFalse(exercise.esAnioBisiesto(1800), "1800 no debería ser bisiesto");
    }
}
