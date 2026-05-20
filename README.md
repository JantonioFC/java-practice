# Java Practice Workspace

Workspace personal para estudiar Java con ejercicios guiados, material de la universidad y tests automáticos.

## Requisitos
- JDK 17 o superior
- Maven
- VS Code con Extension Pack for Java

## Cómo usarlo
1. Abrí el proyecto en VS Code.
2. Subí el apunte o PDF del tema a `materials/inbox`.
3. Ejecutá `python3 tools/process_materials.py` para convertir el PDF a Markdown, clasificarlo y generar la hoja de práctica.
4. Revisá el resultado en `materials/topics/<tema>/notes` y `materials/topics/<tema>/practice`.
5. Empezá por `src/main/java/com/jfranco/practice/exercises/Exercise01Basics.java` o por el ejercicio que toque según el tema.
6. Implementá los métodos marcados como ejercicio.
7. Corré los tests con:

```bash
mvn test
```

## Estructura
- `src/main/java`: código de ejercicios y soporte.
- `src/test/java`: tests que guían la práctica.
- `materials`: apuntes de la universidad, temas clasificados y plantilla para generar ejercicios.
- `materials/inbox`: entrada rápida para material nuevo.
- `materials/topics`: material ordenado por tema o unidad.
- `materials/topics/<tema>/source`: PDFs originales archivados.
- `materials/topics/<tema>/notes`: versiones en Markdown extraídas del PDF.
- `materials/topics/<tema>/practice`: hojas de práctica generadas desde el material.
- `materials/processed`: material ya usado para generar ejercicios.
- `.vscode`: configuración útil para ejecutar y testear.
- `Escritorio/Ejercicios-Java`: acceso directo a `materials` desde el escritorio.

## Flujo recomendado
- Leé primero el apunte o el enunciado del tema.
- Recoré los tests antes de tocar el código.
- Implementá una solución pequeña y concreta.
- Corré los tests.
- Si falla, corregí según el mensaje y repetí.
- Subí primero los apuntes a `materials/inbox`.
- Corré el script de procesamiento para convertir, clasificar y generar el material de estudio.
- Generá los ejercicios a partir de la hoja de práctica y guardá la fuente ya procesada en `materials/processed`.

## Objetivo del workspace
La idea es que cada tema de la universidad tenga su propia traducción a práctica:
- material de estudio
- ejercicios cortos
- tests que te corrijan
- feedback para aprender del error

Si querés seguir el ritmo de la cursada, cargá el tema actual y armamos una tanda de ejercicios alineada a ese contenido.
