# Java Practice Workspace

Workspace personal para estudiar Java con ejercicios guiados, material de la universidad y tests automáticos.

## Recursos de instalación

Antes de arrancar, revisá el material de guía incluido en [`docs/media/`](docs/media/):

| Archivo | Tipo | Descripción |
| --- | --- | --- |
| [Entorno_Java_Automatizado.pdf](docs/media/Entorno_Java_Automatizado.pdf) | PDF | Guía de instalación del entorno |
| [Workspace_Práctica_Java.mp4](docs/media/Workspace_Práctica_Java.mp4) | Video | Recorrido del workspace y flujo de trabajo |
| [Convierte_tus_apuntes_PDF_en_retos_Java.m4a](docs/media/Convierte_tus_apuntes_PDF_en_retos_Java.m4a) | Audio | Explicación del flujo de materiales |

## Requisitos
- JDK 25 (LTS)
- Maven (o usar el wrapper incluido `./mvnw`)
- VS Code con Extension Pack for Java, **o** IntelliJ IDEA

## Abrir en IntelliJ IDEA
1. **File → Open** → seleccioná el archivo `pom.xml` → **Open as Project**.
2. IntelliJ importa todo automáticamente desde el POM.
3. Configurá el Project SDK: **File → Project Structure → SDK** → seleccioná JDK 25.
4. Corrés los tests con el botón ▶ en cualquier archivo de test, o desde el panel **Maven → Lifecycle → test**.

## Cómo usarlo
1. Abrí el proyecto en VS Code.
2. Subí el apunte o PDF del tema a `materials/inbox`.
3. Ejecutá `python3 tools/process_materials.py` para convertir el PDF a Markdown, clasificarlo y generar la hoja de práctica.
4. Revisá el resultado en `materials/topics/<tema>/notes` y `materials/topics/<tema>/practice`.
5. Empezá por `src/main/java/com/jfranco/practice/exercises/Exercise01Basics.java` o por el ejercicio que toque según el tema.
6. Implementá los métodos marcados como ejercicio.
7. Ejecutá la task de VS Code `practice: test and unlock next`.
8. Si el ejercicio actual está en verde, el siguiente se desbloquea automáticamente.

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
- Ejecutá la task `practice: test and unlock next`.
- Si falla, corregí según el mensaje y repetí.
- Cuando el ejercicio actual esté en verde, el siguiente se desbloquea automáticamente.
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
