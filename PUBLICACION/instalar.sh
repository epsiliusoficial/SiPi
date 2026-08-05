#!/usr/bin/env bash
# Instalador de SiPi para Linux/Mac (equivalente a instalar.bat en Windows).
set -e

echo "============================================"
echo "  SiPi - Instalador para Linux/Mac"
echo "============================================"
echo

PYTHON_BIN=""
for candidato in python3 python; do
    if command -v "$candidato" >/dev/null 2>&1; then
        PYTHON_BIN="$candidato"
        break
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    echo "No se encontro Python instalado en este equipo."
    echo
    echo "Instalalo con el gestor de paquetes de tu sistema, por ejemplo:"
    echo "  Ubuntu/Debian:  sudo apt install python3 python3-pip python3-tk"
    echo "  Fedora:         sudo dnf install python3 python3-pip python3-tkinter"
    echo "  macOS (brew):   brew install python-tk"
    exit 1
fi

echo "Python encontrado correctamente ($PYTHON_BIN)."
echo

if ! "$PYTHON_BIN" -c "import tkinter" >/dev/null 2>&1; then
    echo "AVISO: no se encontro el modulo 'tkinter' (necesario para el editor visual)."
    echo "En Linux, instalalo con el gestor de paquetes de tu sistema, por ejemplo:"
    echo "  Ubuntu/Debian:  sudo apt install python3-tk"
    echo "  Fedora:         sudo dnf install python3-tkinter"
    echo "  Arch:           sudo pacman -S tk"
    echo "(En macOS, tkinter suele venir incluido con Python de python.org)"
    echo
fi

echo "Instalando/actualizando componentes de SiPi..."
echo "  - pygame        (para juegos y escenas 3D)"
echo "  - pyinstaller   (para compilar a ejecutable)"
echo "  - Pillow        (para el manejo de imagenes)"
echo

"$PYTHON_BIN" -m pip install --upgrade pip --quiet 2>/dev/null || true

instalar_paquetes() {
    # En Debian/Ubuntu modernos (PEP 668), pip rechaza instalar en el
    # Python del sistema con "externally-managed-environment". Probamos
    # primero de la forma normal (mejor para venvs/pyenv/macOS/Windows) y
    # si falla especificamente por eso, reintentamos con
    # --break-system-packages (razonable aca porque son librerias que
    # necesita SiPi para correr, no un paquete de sistema critico).
    if "$PYTHON_BIN" -m pip install --user "$@" --quiet 2>/tmp/sipi_pip_error.log; then
        return 0
    fi
    if grep -qi "externally-managed-environment" /tmp/sipi_pip_error.log 2>/dev/null; then
        "$PYTHON_BIN" -m pip install --user --break-system-packages "$@" --quiet 2>/dev/null || return 1
        return 0
    fi
    return 1
}

instalar_paquetes pygame pyinstaller Pillow || echo "AVISO: no se pudieron instalar algunos componentes automaticamente; instalalos a mano con pip."

echo
echo "(Opcional, puede tardar varios minutos) Instalando Kivy para apps Android..."
instalar_paquetes kivy || true

chmod +x sipi.py 2>/dev/null || true

echo
echo "============================================"
echo "  Instalacion completada."
echo "  NOTA: SiPi tambien auto-instala componentes"
echo "  que falten la primera vez que los necesites,"
echo "  asi que si te salteaste algo no hay problema."
echo
echo "  Ya podes usar SiPi con:"
echo "    $PYTHON_BIN sipi.py archivo.sipi"
echo "  o abrir el editor visual con:"
echo "    $PYTHON_BIN editor_sipi.py"
echo "============================================"
