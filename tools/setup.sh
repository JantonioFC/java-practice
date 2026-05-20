#!/usr/bin/env bash
# setup.sh — Verifica e instala los requisitos del workspace java-practice
set -euo pipefail

PASS="✅"
FAIL="❌"
WARN="⚠️ "
MIN_JAVA=25

ok()   { echo "  $PASS $*"; }
fail() { echo "  $FAIL $*"; ERRORS=$((ERRORS + 1)); }
warn() { echo "  $WARN $*"; }

ERRORS=0

echo ""
echo "================================================"
echo " java-practice — verificación de entorno"
echo "================================================"
echo ""

# ── 1. Java ──────────────────────────────────────────
echo "[ Java ]"
if command -v java &>/dev/null; then
  JAVA_VER=$(java -version 2>&1 | grep -oP '(?<=version ")[\d]+' | head -1)
  if [ "${JAVA_VER:-0}" -ge "$MIN_JAVA" ]; then
    ok "JDK $JAVA_VER detectado ($(command -v java))"
  else
    fail "JDK $JAVA_VER detectado — se requiere JDK $MIN_JAVA o superior"
    echo ""
    echo "     Instalá JDK $MIN_JAVA con:"
    echo "       sdk install java ${MIN_JAVA}-open     # si usás SDKMAN"
    echo "       sudo apt install openjdk-${MIN_JAVA}-jdk  # Debian/Ubuntu"
  fi
else
  fail "Java no encontrado en PATH"
  echo ""
  echo "     Instalá JDK $MIN_JAVA con:"
  echo "       sdk install java ${MIN_JAVA}-open     # si usás SDKMAN"
  echo "       sudo apt install openjdk-${MIN_JAVA}-jdk  # Debian/Ubuntu"
fi
echo ""

# ── 2. Maven Wrapper ─────────────────────────────────
echo "[ Maven Wrapper ]"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -f "$SCRIPT_DIR/mvnw" ]; then
  ok "mvnw encontrado en el proyecto (no necesitás Maven global)"
else
  fail "mvnw no encontrado — regeneralo con: mvn wrapper:wrapper -Dmaven=3.9.9"
fi
echo ""

# ── 3. Build rápido ──────────────────────────────────
echo "[ Build ]"
if [ -f "$SCRIPT_DIR/mvnw" ]; then
  if "$SCRIPT_DIR/mvnw" -f "$SCRIPT_DIR/pom.xml" clean test-compile -q 2>/dev/null; then
    ok "Compilación exitosa"
  else
    fail "La compilación falló — revisá la versión de JDK o ejecutá: ./mvnw clean test-compile"
  fi
else
  warn "Saltando build (mvnw no disponible)"
fi
echo ""

# ── 4. pdftotext ─────────────────────────────────────
echo "[ pdftotext (procesamiento de material) ]"
if command -v pdftotext &>/dev/null; then
  ok "pdftotext disponible ($(pdftotext -v 2>&1 | head -1))"
else
  warn "pdftotext no encontrado — solo necesario para procesar PDFs"
  echo "     Instalalo con: sudo apt install poppler-utils"
fi
echo ""

# ── 5. Python ────────────────────────────────────────
echo "[ Python (scripts de herramientas) ]"
if command -v python3 &>/dev/null; then
  PY_VER=$(python3 --version 2>&1)
  ok "$PY_VER"
else
  warn "python3 no encontrado — necesario para process_materials.py y unlock_next_exercise.py"
  echo "     Instalalo con: sudo apt install python3"
fi
echo ""

# ── Resultado final ──────────────────────────────────
echo "================================================"
if [ "$ERRORS" -eq 0 ]; then
  echo " $PASS Entorno listo. Podés empezar con:"
  echo ""
  echo "   ./mvnw clean test"
else
  echo " $FAIL Se encontraron $ERRORS problema(s). Revisá los mensajes anteriores."
fi
echo "================================================"
echo ""

exit "$ERRORS"
