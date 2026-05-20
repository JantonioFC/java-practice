# Materials

Drop university materials here and turn them into practice exercises.

## Automated flow
1. Put the PDF in `inbox/`.
2. Run `python3 tools/process_materials.py` from the workspace root.
3. The script converts the PDF to Markdown, classifies it, archives the original PDF under `topics/<tema>/source/`, and generates a note plus a practice sheet.

## Folders
- `inbox/`: raw notes, PDFs converted to text, slides, and ad-hoc material waiting to be reviewed.
- `topics/`: material organized by subject or chapter.
- `topics/<tema>/source/`: original PDFs kept for reference.
- `topics/<tema>/notes/`: Markdown version extracted from the PDF.
- `topics/<tema>/practice/`: generated exercises and explanations.
- `processed/`: material already used to generate exercises.
- `templates/`: prompts and formats used to turn material into exercises.

## Suggested flow
1. Put new material in `inbox/`.
2. Let the automation convert and classify it into `topics/<subject>/<chapter>/`.
3. Use the generated practice sheet to create or extend exercises in `src/main/java/com/jfranco/practice/exercises/` and tests in `src/test/java/com/jfranco/practice/exercises/`.
4. Move the source material to `processed/` when the exercises are created.

## Naming suggestion
Use short, stable names such as:
- `algoritmos`
- `poo`
- `estructuras-de-datos`
- `concurrencia`
