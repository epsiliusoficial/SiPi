#!/usr/bin/env bash
# Instalador de SiPi para Linux/Mac (equivalente a instalar.bat en Windows).
# No usa 'set -e': un paquete opcional que falle (ej. kivy) no debe frenar
# el resto del instalador ni ocultar el resumen final.

echo "============================================"
echo "  SiPi - Instalador para Linux/Mac"
echo "============================================"
echo

# ---------- 1) Python ----------
PYTHON_BIN=""
for candidato in python3 python; do
    if command -v "$candidato" >/dev/null 2>&1; then
        PYTHON_BIN="$candidato"
        break
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    echo "ERROR: no se encontro Python instalado en este equipo."
    echo
    echo "Instalalo con el gestor de paquetes de tu sistema, por ejemplo:"
    echo "  Ubuntu/Debian:  sudo apt install python3 python3-pip python3-tk"
    echo "  Fedora:         sudo dnf install python3 python3-pip python3-tkinter"
    echo "  Arch/Manjaro:   sudo pacman -S python python-pip tk"
    echo "  macOS (brew):   brew install python-tk"
    exit 1
fi

VERSION_PY=$("$PYTHON_BIN" -c "import sys; print('%d.%d' % sys.version_info[:2])" 2>/dev/null)
echo "Python encontrado correctamente ($PYTHON_BIN, version $VERSION_PY)."
if [ -n "$VERSION_PY" ]; then
    "$PYTHON_BIN" -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "AVISO: SiPi esta pensado para Python 3.10 o mas nuevo. Con $VERSION_PY algunas cosas pueden fallar."
    fi
fi
echo

# ---------- 2) pip ----------
# A diferencia de la version anterior de este script, ahora se comprueba
# ESPECIFICAMENTE que pip exista antes de intentar usarlo -- en Arch Linux
# (y en instalaciones minimas de otras distros) Python no siempre viene con
# pip preinstalado, y usarlo sin chequear antes producia un error confuso
# a mitad de la instalacion en vez de un mensaje claro de que hacer.
if ! "$PYTHON_BIN" -m pip --version >/dev/null 2>&1; then
    echo "ERROR: no se encontro pip para $PYTHON_BIN."
    echo
    echo "Instalalo con el gestor de paquetes de tu sistema, por ejemplo:"
    echo "  Ubuntu/Debian:  sudo apt install python3-pip"
    echo "  Fedora:         sudo dnf install python3-pip"
    echo "  Arch/Manjaro:   sudo pacman -S python-pip"
    echo "  macOS (brew):   brew install python3   (pip ya viene incluido)"
    echo
    echo "Volve a correr este instalador despues de instalar pip."
    exit 1
fi
echo "pip encontrado correctamente."
echo

# ---------- 3) tkinter (para el editor visual) ----------
TKINTER_OK=0
if "$PYTHON_BIN" -c "import tkinter" >/dev/null 2>&1; then
    TKINTER_OK=1
else
    echo "AVISO: no se encontro el modulo 'tkinter' (necesario para el editor visual, editor_sipi.py)."
    echo "En Linux, instalalo con el gestor de paquetes de tu sistema, por ejemplo:"
    echo "  Ubuntu/Debian:  sudo apt install python3-tk"
    echo "  Fedora:         sudo dnf install python3-tkinter"
    echo "  Arch/Manjaro:   sudo pacman -S tk"
    echo "(En macOS, tkinter suele venir incluido con Python de python.org)"
    echo "El interprete (sipi.py) funciona igual sin tkinter; solo el editor visual lo necesita."
    echo
fi

# ---------- 4) Paquetes de Python ----------
echo "Instalando/actualizando componentes de SiPi..."
echo "  - pygame        (para juegos y escenas 3D)"
echo "  - pyinstaller   (para compilar a ejecutable)"
echo "  - Pillow        (para el manejo de imagenes)"
echo

"$PYTHON_BIN" -m pip install --upgrade pip --quiet 2>/dev/null || true

instalar_paquetes() {
    # En Debian/Ubuntu modernos y en Arch (ambos adoptaron PEP 668), pip
    # rechaza instalar en el Python del sistema con
    # "externally-managed-environment". Probamos primero de la forma normal
    # (mejor para venvs/pyenv/macOS/Windows) y si falla especificamente por
    # eso, reintentamos con --break-system-packages (razonable aca porque
    # son librerias que necesita SiPi para correr, no un paquete de sistema
    # critico).
    if "$PYTHON_BIN" -m pip install --user "$@" --quiet 2>/tmp/sipi_pip_error.log; then
        return 0
    fi
    if grep -qi "externally-managed-environment" /tmp/sipi_pip_error.log 2>/dev/null; then
        if "$PYTHON_BIN" -m pip install --user --break-system-packages "$@" --quiet 2>>/tmp/sipi_pip_error.log; then
            return 0
        fi
    fi
    return 1
}

instalar_paquetes pygame pyinstaller Pillow
FALLO_CORE=$?

echo
echo "(Opcional, puede tardar varios minutos) Instalando Kivy para apps Android..."
instalar_paquetes kivy >/dev/null 2>&1
KIVY_OK=$?

chmod +x sipi.py 2>/dev/null || true

# ---------- 5) Verificacion real: no confiar solo en el codigo de salida de pip ----------
# 'pip install' puede devolver exito y sin embargo el paquete no quedar
# importable (conflicto de version, instalado en un Python distinto, etc.),
# asi que la comprobacion real es: se puede importar de verdad.
echo
echo "Verificando que los componentes quedaron realmente instalados..."
FALLARON=""
"$PYTHON_BIN" -c "import pygame" >/dev/null 2>&1 || FALLARON="$FALLARON pygame"
"$PYTHON_BIN" -c "import PIL" >/dev/null 2>&1 || FALLARON="$FALLARON Pillow"
"$PYTHON_BIN" -c "import PyInstaller" >/dev/null 2>&1 || FALLARON="$FALLARON pyinstaller"

echo
echo "============================================"
if [ -z "$FALLARON" ]; then
    echo "  Instalacion completada correctamente."
    echo "  pygame, Pillow y pyinstaller quedaron instalados y verificados."
else
    echo "  Instalacion INCOMPLETA."
    echo "  No se pudieron instalar o verificar:$FALLARON"
    echo
    echo "  Proba instalarlos a mano, por ejemplo:"
    echo "    $PYTHON_BIN -m pip install --user$FALLARON"
    echo "  Si el error menciona 'externally-managed-environment', agregale --break-system-packages"
    echo "  al final de ese mismo comando."
fi
if [ "$TKINTER_OK" -eq 0 ]; then
    echo "  (tkinter tampoco esta instalado -- ver el aviso mas arriba si queres usar el editor visual)"
fi
echo
echo "  Ya podes usar SiPi con:"
echo "    $PYTHON_BIN sipi.py archivo.sipi"
if [ "$TKINTER_OK" -eq 1 ]; then
    echo "  o abrir el editor visual con:"
    echo "    $PYTHON_BIN editor_sipi.py"
fi
echo "============================================"

if [ -n "$FALLARON" ]; then
    exit 1
fi
exit 0
