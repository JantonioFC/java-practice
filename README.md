# Java Practice Workspace

Workspace pensado para practicar Java con ejercicios guiados, tests automáticos y feedback rápido.

## Requisitos
- JDK 17 o superior
- Maven
- VS Code con Extension Pack for Java

## Cómo usarlo
1. Abrí el proyecto en VS Code.
2. Empezá por `src/main/java/com/jfranco/practice/exercises/Exercise01Basics.java`.
3. Implementá los métodos marcados como ejercicio.
4. Corré los tests con:

```bash
mvn test
```

## Estructura
- `src/main/java`: código de ejercicios y soporte.
- `src/test/java`: tests que guían la práctica.
- `materials`: apuntes de la universidad, temas clasificados y plantilla para generar ejercicios.
- `.vscode`: configuración útil para ejecutar y testear.

## Flujo recomendado
- Leé el test antes de tocar el código.
- Implementá una solución pequeña.
- Corré los tests.
- Si falla, corregí según el mensaje y repetí.
- Subí primero los apuntes a `materials/inbox`.
- Mové cada tema a `materials/topics/<tema>` cuando ya esté clasificado.
- Generá los ejercicios a partir de ese material y guardá la fuente ya procesada en `materials/processed`.
