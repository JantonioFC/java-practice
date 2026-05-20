# Manual de uso - Java Practice Workspace

Este manual explica el flujo completo de estudio en este workspace: desde cargar material de la universidad hasta resolver ejercicios con tests y desbloqueo secuencial.

## 1) Objetivo

El objetivo es practicar Java de forma incremental:

- cada ejercicio tiene tests que guian la implementacion
- el siguiente ejercicio se habilita solo cuando el anterior esta aprobado
- el material teorico se transforma en notas y hojas de practica

## 2) Requisitos

- JDK 25 (LTS)
- Maven (o usar el wrapper incluido `./mvnw`)
- VS Code con Extension Pack for Java, **o** IntelliJ IDEA
- utilitario pdftotext disponible en el sistema (lo usa el procesamiento de PDF)

## 2b) Script de configuración de entorno

Antes de empezar, verificá que tu máquina tiene todo lo necesario ejecutando:

```bash
bash tools/setup.sh
```

El script revisa y reporta el estado de cada requisito:

| Componente | Qué verifica | Qué hace si falta |
| --- | --- | --- |
| **JDK 25+** | Versión de `java` en PATH | Muestra el comando de instalación |
| **Maven Wrapper** | Presencia de `./mvnw` en el proyecto | Indica cómo regenerarlo |
| **Build rápido** | Compila el proyecto con `./mvnw clean test-compile` | Reporta el error de compilación |
| **pdftotext** | Disponibilidad del utilitario | Muestra comando de instalación (solo necesario para PDFs) |
| **Python 3** | Disponibilidad de `python3` | Advierte si falta (necesario para los scripts de herramientas) |

Salida esperada cuando todo está bien:

```
✅ JDK 25 detectado
✅ mvnw encontrado en el proyecto
✅ Compilación exitosa
✅ pdftotext disponible
✅ Python 3.x

✅ Entorno listo. Podés empezar con:
   ./mvnw clean test
```

Si algún componente falla, el script imprime el comando exacto para instalarlo y termina con código de salida distinto de cero.

## 2c) Abrir en IntelliJ IDEA

1. **File → Open** → seleccioná el archivo `pom.xml` → **Open as Project**.
2. IntelliJ importa la estructura, dependencias y configuración del compilador automáticamente.
3. Configurá el SDK del proyecto: **File → Project Structure → Project → SDK** → seleccioná JDK 25.
4. Para correr los tests: botón ▶ junto a cualquier clase de test, o desde **Maven → Lifecycle → test**.
5. Para correr el flujo completo desde terminal integrada:

   ```bash
   ./mvnw clean test
   ```

> El proyecto incluye Maven Wrapper (`./mvnw`). No necesitás tener Maven instalado globalmente.

## 3) Estructura principal

- src/main/java/com/jfranco/practice/exercises: ejercicios a implementar
- src/test/java/com/jfranco/practice/exercises: tests guia
- materials/inbox: entrada de PDFs nuevos
- materials/topics: material clasificado por tema
- tools/process_materials.py: convierte y clasifica PDFs
- tools/unlock_next_exercise.py: desbloqueo secuencial de ejercicios
- .vscode/tasks.json: tareas de VS Code (incluye el flujo recomendado)

## 4) Flujo rapido (recomendado)

1. Abri el proyecto en VS Code.
2. Carga un PDF de la facultad en materials/inbox.
3. Procesa el material con:

   ```bash
   python3 tools/process_materials.py
   ```

4. Revisa los archivos generados en `materials/topics/{tema}/notes` y `materials/topics/{tema}/practice`.
5. Resuelve el ejercicio actual en `src/main/java/com/jfranco/practice/exercises`.
6. Ejecuta la task de VS Code:
   - practice: test and unlock next
7. Si los tests del ejercicio actual pasan, el siguiente ejercicio se desbloquea automaticamente.

## 5) Que hace la task principal

La task practice: test and unlock next hace dos pasos en cadena:

1. Ejecuta todos los tests con Maven.
2. Si el estado permite avanzar, ejecuta el desbloqueo secuencial.

Resultado esperado:

- si todo esta bien, se crea la siguiente clase de ejercicio y su test guia
- si no, no se crea nada nuevo y el flujo se detiene para que corrijas

## 6) Flujo de estudio sugerido por ejercicio

1. Lee primero el test del ejercicio.
2. Implementa lo minimo para pasar un test.
3. Ejecuta la task principal.
4. Repite hasta dejar verde el ejercicio.
5. Al quedar verde, se habilita el siguiente.

## 7) Flujo de materiales (PDF -> practica)

Cuando ejecutas tools/process_materials.py:

1. Toma cada PDF de materials/inbox.
2. Extrae texto con pdftotext.
3. Clasifica por tema (por ejemplo variables, operadores, condicionales, iteraciones, funciones).
4. Genera:
   - nota en Markdown (notes)
   - hoja de practica (practice)
5. Mueve el PDF original a la carpeta source del tema.

## 8) Resolucion de problemas

### 8.1 La task falla en tests

Significa que el ejercicio actual todavia no esta aprobado.
Accion: corregi implementacion en src/main y volve a ejecutar la task.

### 8.2 No se desbloquea el siguiente ejercicio

Causas comunes:

- el test del ejercicio previo no pasa
- el siguiente ejercicio ya fue desbloqueado antes

Verificacion rapida:

- revisa el output de la task en Terminal
- confirma si ya existen los archivos ExerciseXX en src/main y src/test

### 8.3 El procesamiento de PDF no genera archivos

Causas comunes:

- no hay PDFs en materials/inbox
- falta pdftotext

Accion:

- agrega un PDF valido a inbox
- instala pdftotext y reintenta

## 9) Tareas de VS Code

En .vscode/tasks.json ya estan definidas las tareas principales:

- practice: test and unlock next (flujo recomendado)
- watch materials inbox (procesamiento continuo de PDFs)
- maven test (ejecucion manual de tests)
- unlock next exercise (ejecucion manual del desbloqueo)

## 10) Buenas practicas

- No saltees ejercicios: la progresion esta pensada para aprendizaje incremental.
- Mantene cada solucion simple y legible.
- Usa los tests como especificacion del comportamiento esperado.
- Si agregas un ejercicio nuevo, agrega siempre su test guia correspondiente.

## 11) Siguiente mejora sugerida

Para ampliar la escalera de ejercicios, agrega nuevas entradas en TEMPLATES dentro de tools/unlock_next_exercise.py (definiendo test previo, archivo main y archivo test de cada nuevo nivel).
