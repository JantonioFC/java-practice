package com.jfranco.practice.exercises;

/**
 * Clase que contiene ejercicios sobre estructuras de decisión (condicionales).
 * Aprendé a usar `if-else` y la combinación de expresiones lógicas para
 * bifurcar el flujo de tu programa según distintas condiciones.
 */
public class Exercise03Conditionals {

    /**
     * ### Ejercicio 1 (Fácil): Determinar si un número es par o impar.
     *
     * **Explicación Clara y Detallada**:
     * Este método debe evaluar un número entero y retornar una cadena de texto
     * que indique si es "PAR" o "IMPAR". El objetivo es que practiques el uso
     * de una estructura condicional `if-else` básica y el operador módulo (`%`).
     * Un número es par si al dividirlo por 2, el resto es 0. De lo contrario,
     * es impar.
     *
     * **Lógica Paso a Paso**:
     * 1. Tomá el número entero de entrada.
     * 2. Calculá el resto de la división del número por 2 (usando el operador `%`).
     * 3. Si el resto es igual a 0, el número es par. Retorná la cadena "PAR".
     * 4. Si el resto no es igual a 0, el número es impar. Retorná la cadena "IMPAR".
     *
     * **Casos Borde a Considerar**:
     * - El número 0: ¿Es par o impar? Matemáticamente, se considera par.
     * - Números negativos: La lógica del operador módulo también funciona correctamente
     *   para números negativos. Por ejemplo, -2 % 2 es 0 (PAR), -3 % 2 es -1 (IMPAR).
     *
     * **Ejemplos Prácticos**:
     * - `esParOImpar(4)` debería retornar "PAR"
     * - `esParOImpar(7)` debería retornar "IMPAR"
     * - `esParOImpar(0)` debería retornar "PAR"
     * - `esParOImpar(-2)` debería retornar "PAR"
     */
    public String esParOImpar(int numero) {
        throw new UnsupportedOperationException("Implement esParOImpar");
    }

    /**
     * ### Ejercicio 2 (Medio): Evaluar la calificación académica de un alumno.
     *
     * **Explicación Clara y Detallada**:
     * Este método recibe una calificación numérica entera del 1 al 10 y debe
     * determinar el estado académico del alumno basándose en los siguientes criterios:
     * - Menos de 4: "DESAPROBADO"
     * - Entre 4 y 6 (inclusive): "REGULAR"
     * - 7 o más: "PROMOCIONADO"
     * El objetivo es que utilices la estructura `if-else if-else` para manejar
     * múltiples condiciones mutuamente excluyentes y definas un flujo claro
     * de evaluación.
     *
     * **Lógica Paso a Paso**:
     * 1. Evaluá la primera condición más restrictiva o inclusiva. Por ejemplo,
     *    podrías empezar preguntando si la calificación es mayor o igual a 7.
     *    Si es así, retorná "PROMOCIONADO".
     * 2. Si la primera condición no se cumple, pasá a la siguiente. Por ejemplo,
     *    preguntá si la calificación es mayor o igual a 4. Si es así (y sabés que
     *    es menor a 7 por la condición anterior), retorná "REGULAR".
     * 3. Si ninguna de las condiciones anteriores se cumplió, la calificación
     *    debe ser menor a 4. En este caso, retorná "DESAPROBADO".
     * Pensá en el orden de tus `if-else if` para que la lógica sea correcta y
     * eficiente.
     *
     * **Casos Borde a Considerar**:
     * - Los límites de cada rango: 3 (desaprobado), 4 (regular), 6 (regular), 7 (promocionado).
     * - Calificaciones mínimas y máximas: 1 y 10. Asegurate de que se manejen correctamente.
     *   Aunque el enunciado indica que la calificación es "del 1 al 10", es buena
     *   práctica pensar qué pasaría con valores fuera de ese rango (aunque para
     *   este ejercicio podés asumir que la entrada siempre será válida entre 1 y 10).
     *
     * **Ejemplos Prácticos**:
     * - `evaluarCalificacion(8)` debería retornar "PROMOCIONADO"
     * - `evaluarCalificacion(7)` debería retornar "PROMOCIONADO"
     * - `evaluarCalificacion(5)` debería retornar "REGULAR"
     * - `evaluarCalificacion(4)` debería retornar "REGULAR"
     * - `evaluarCalificacion(3)` debería retornar "DESAPROBADO"
     * - `evaluarCalificacion(1)` debería retornar "DESAPROBADO"
     */
    public String evaluarCalificacion(int calificacion) {
        throw new UnsupportedOperationException("Implement evaluarCalificacion");
    }

    /**
     * ### Ejercicio 3 (Difícil): Determinar si un año es bisiesto.
     *
     * **Explicación Clara y Detallada**:
     * Este método debe recibir un año como número entero y retornar `true` si es
     * un año bisiesto, y `false` en caso contrario. La regla para determinar un
     * año bisiesto es un clásico desafío de condicionales y combina varias
     * expresiones lógicas. Un año es bisiesto si se cumplen las siguientes
     * condiciones:
     * 1. Es divisible por 4.
     * 2. PERO, si es divisible por 100, entonces NO es bisiesto.
     * 3. A MENOS QUE, también sea divisible por 400. En ese caso, SÍ es bisiesto.
     * La clave está en traducir estas reglas a una expresión lógica compuesta
     * utilizando operadores `&&` (AND), `||` (OR) y `!` (NOT).
     *
     * **Lógica Paso a Paso**:
     * 1. Un enfoque puede ser combinar las reglas en una única expresión booleana.
     * 2. Pensá en la condición principal: `(año % 4 == 0)`. Este es el punto de partida.
     * 3. Ahora, agregá la excepción: `&& (año % 100 != 0)`. Esto dice: "divisible por 4 Y NO divisible por 100".
     * 4. Finalmente, agregá la contra-excepción (la parte del "A MENOS QUE"). Esta es una
     *    condición `OR` con la anterior. Es decir, el año es bisiesto si cumple
     *    (divisible por 4 Y NO por 100) O (es divisible por 400).
     * 5. Estructurá todo dentro de paréntesis para asegurar el orden de evaluación correcto:
     *    `((año % 4 == 0) && (año % 100 != 0)) || (año % 400 == 0)`.
     *
     * **Casos Borde a Considerar**:
     * - Años que son divisibles por 4 pero no por 100 (ej: 2004, 2020).
     * - Años que son divisibles por 100 pero no por 400 (ej: 1900, 2100). Estos NO son bisiestos.
     * - Años que son divisibles por 400 (ej: 2000, 1600). Estos SÍ son bisiestos.
     * - Años que no cumplen ninguna de las condiciones (ej: 2003, 2019).
     * - Años negativos o el año 0: La definición del calendario gregoriano aplica a años positivos.
     *   Para este ejercicio, podés asumir años válidos > 0, o decidir cómo los manejas
     *   (por ejemplo, retornar false para años no positivos).
     *
     * **Ejemplos Prácticos**:
     * - `esAnioBisiesto(2000)` debería retornar `true` (Divisible por 400)
     * - `esAnioBisiesto(1900)` debería retornar `false` (Divisible por 100 pero no por 400)
     * - `esAnioBisiesto(2004)` debería retornar `true` (Divisible por 4 y no por 100)
     * - `esAnioBisiesto(2003)` debería retornar `false` (No divisible por 4)
     * - `esAnioBisiesto(1600)` debería retornar `true` (Divisible por 400)
     * - `esAnioBisiesto(2100)` debería retornar `false` (Divisible por 100 pero no por 400)
     */
    public boolean esAnioBisiesto(int anio) {
        throw new UnsupportedOperationException("Implement esAnioBisiesto");
    }
}
