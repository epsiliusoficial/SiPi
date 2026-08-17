#!/usr/bin/env python3
"""
verificar.py - Verificación rápida de un archivo SiPi para Claude.

Uso: python3 claude/verificar.py archivo.sipi

Combina ejecución + análisis estático en UNA sola llamada de proceso,
para que confirmar que un programa funciona (y está bien escrito) cueste
un solo tool-call, no dos o tres. Sin dependencias de sipi_ia.py -- no
llama a ninguna API, todo es local e instantáneo (subprocess contra el
motor real).

Salida: JSON compacto por stdout, siempre, incluso ante errores propios
del verificador (nunca un traceback crudo). Campos:
  ok               true si el programa ejecutó sin errores
  salida           stdout real del programa
  error            stderr / mensaje de error real si lo hubo (o null)
  hallazgos        conteo por categoria del analizador estatico
                   (seguridad/bugs/estilo/sugerencias), o null si el
                   programa no llegó a ejecutar limpio (no tiene sentido
                   pedir estilo de algo que ni corre)
"""
import os
import sys
import json
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ_REPO = os.path.dirname(AQUI)


def _ruta_motor():
    for candidato in (
        os.path.join(RAIZ_REPO, "src", "sipi.py"),
        os.path.join(RAIZ_REPO, "src", "sipi_protegido.py"),
        os.path.join(RAIZ_REPO, "sipi.py"),
    ):
        if os.path.exists(candidato):
            return candidato
    return None


def _contar_hallazgos(salida_revisar):
    categorias = {"seguridad": 0, "bugs": 0, "estilo": 0, "sugerencias": 0}
    actual = None
    for linea in salida_revisar.splitlines():
        if "SEGURIDAD" in linea:
            actual = "seguridad"
        elif "POSIBLES BUGS" in linea:
            actual = "bugs"
        elif "ESTILO" in linea:
            actual = "estilo"
        elif "SUGERENCIAS" in linea:
            actual = "sugerencias"
        elif linea.strip().startswith("- ") and actual:
            categorias[actual] += 1
    return categorias


def verificar(ruta_archivo, timeout=15):
    if not os.path.exists(ruta_archivo):
        return {"ok": False, "salida": "", "error": f"No existe el archivo '{ruta_archivo}'.", "hallazgos": None}

    ruta_motor = _ruta_motor()
    if not ruta_motor:
        return {"ok": False, "salida": "", "error": "No se encontro el motor de SiPi (sipi.py).", "hallazgos": None}

    try:
        resultado = subprocess.run(
            [sys.executable, ruta_motor, ruta_archivo],
            capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {
            "ok": False, "salida": "",
            "error": f"Se agoto el tiempo de espera ({timeout}s). Si el programa usa 'preguntar', "
                     "correrlo asi no funciona para verificar -- probar con entrada de prueba redirigida.",
            "hallazgos": None,
        }

    ok = resultado.returncode == 0
    error_texto = None
    if not ok:
        # sipi.py imprime sus errores a stdout (con formato "[SiPi] Error...",
        # puntero de columna, y el mensaje), no a stderr -- se busca ahi.
        combinado = resultado.stdout + resultado.stderr
        if "[SiPi] Error" in combinado:
            error_texto = combinado[combinado.index("[SiPi] Error"):].strip()
        else:
            error_texto = (resultado.stderr.strip() or combinado.strip() or "El programa termino con error, sin mensaje detectado.")

    salida = {"ok": ok, "salida": resultado.stdout, "error": error_texto, "hallazgos": None}

    if ok:
        try:
            revision = subprocess.run(
                [sys.executable, ruta_motor, "--revisar", ruta_archivo],
                capture_output=True, text=True, timeout=timeout,
            )
            salida["hallazgos"] = _contar_hallazgos(revision.stdout)
        except subprocess.TimeoutExpired:
            pass  # el analisis estatico es un extra -- si tarda, no bloquea el resultado principal

    return salida


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "error": "Uso: python3 verificar.py archivo.sipi [archivo2.sipi ...]"}))
        sys.exit(1)

    archivos = sys.argv[1:]
    if len(archivos) == 1:
        # Caso comun: un solo archivo -- se mantiene la forma de salida
        # de siempre (objeto plano), para no romper nada que ya dependa
        # de este formato.
        resultado = verificar(archivos[0])
        print(json.dumps(resultado, ensure_ascii=False))
        sys.exit(0 if resultado["ok"] else 1)

    # Varios archivos en un solo tool-call: pensado para cuando se
    # termina de escribir/editar un proyecto de varios .sipi de una
    # sola vez y no tiene sentido pagar un tool-call por archivo solo
    # para confirmar que todos siguen corriendo bien.
    resultados = {}
    todos_ok = True
    for ruta in archivos:
        r = verificar(ruta)
        resultados[ruta] = r
        todos_ok = todos_ok and r["ok"]
    print(json.dumps({"ok": todos_ok, "archivos": resultados}, ensure_ascii=False))
    sys.exit(0 if todos_ok else 1)


if __name__ == "__main__":
    main()
