# condicionales_java

        - Source: condicionales_java.pdf
        - Topic: Condicionales
        - Status: auto-converted from PDF

        ## Auto summary
        Decision making with if, else, else if, ternary expressions, and switch statements.

        ## Extracted text
        Universidad de Ciencias de la

Computación

Cátedra de Programación I - Lenguaje Java



Clase 3: Estructuras de Decisión

(Condicionales)

Las estructuras condicionales permiten bifurcar el flujo de ejecución de un

programa en base al resultado de evaluar una expresión lógica (booleana).



1. La estructura if-else
Es la forma más básica de tomar decisiones. Si la condición lógica se evalúa

como verdadera (true), se ejecuta el bloque de código correspondiente al if.

De lo contrario, opcionalmente se ejecuta el bloque del else.




  int temperatura = 25;



  if (temperatura > 30) {



       System.out.println("Hace calor");



  } else if (temperatura < 15) {
      System.out.println("Hace frío");



  } else {



      System.out.println("El clima está agradable");



  }




2. La estructura switch
Cuando tenemos múltiples caminos mutuamente excluyentes basados en el

valor de una misma variable (que puede ser entera, caracter, string o un enum),

es preferible usar un switch en lugar de muchos if-else encadenados.




  int dia = 3;



  switch (dia) {



      case 1:



           System.out.println("Lunes");



           break;



      case 2:



           System.out.println("Martes");
               break;



        case 3:



               System.out.println("Miércoles");



               break;



        default:



               System.out.println("Otro día");



 }




3. Retos de Código Sugeridos (Ejercicios Prácticos)
     • Reto 1 (Fácil): Crear un método que determine si un número entero es

       par o impar.

     • Reto 2 (Medio): Escribir una función que reciba una calificación numérica

       del 1 al 10 y devuelva el estado académico del alumno: "DESAPROBADO"

       (menos de 4), "REGULAR" (entre 4 y 6), o "PROMOCIONADO" (7 o más).

     • Reto 3 (Difícil): Implementar un método que determine si un año

       determinado es bisiesto o no (recordando que un año es bisiesto si es

       divisible por 4, pero no por 100, a menos que también sea divisible por

       400).
