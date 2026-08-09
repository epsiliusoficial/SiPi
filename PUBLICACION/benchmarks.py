#!/usr/bin/env python3
"""
benchmarks.py - Benchmarks oficiales de SiPi (item #65 del feedback).

Mide el tiempo real de ejecucion del motor de SiPi (sipi.py) en varias
categorias representativas: bucles, funciones/recursion, strings, listas,
archivos y concurrencia (hilos). No son numeros inventados ni estimados:
cada benchmark es un programa .sipi real, generado y ejecutado con el
interprete real, cronometrado con time.perf_counter().

Uso:
    python benchmarks.py              corre todos los benchmarks
    python benchmarks.py --categoria loops    corre solo una categoria
    python benchmarks.py --json salida.json   ademas, guarda resultados en JSON

Pensado para poder correrse en CI y comparar version contra version (por
eso el --json: permite diffear numeros entre corridas, no solo leerlos).
"""
import argparse
import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))


def _cargar_motor():
    ruta = os.path.join(AQUI, "sipi.py")
    if not os.path.exists(ruta):
        ruta = os.path.join(AQUI, "sipi_protegido.py")
    spec = importlib.util.spec_from_file_location("motor_sipi_benchmark", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _correr_programa(motor, codigo_sipi, sin_cache=True):
    """Escribe 'codigo_sipi' a un archivo temporal real, lo ejecuta con el
    Interprete real del motor, y devuelve el tiempo transcurrido en
    segundos. Se corre CADA VEZ con --sin-cache (via los mismos hooks que
    usa sipi_cli.py) para medir el costo real de parseo + ejecucion, no
    solo la ejecucion con cache tibia -- si se quisiera medir el efecto de
    la cache aparte, es otro benchmark, no se mezclan ambas cosas en el
    mismo numero."""
    with tempfile.NamedTemporaryFile("w", suffix=".sipi", delete=False, encoding="utf-8") as f:
        f.write(codigo_sipi)
        ruta = f.name
    try:
        interprete = motor.Interprete(ruta)
        if sin_cache:
            interprete._ruta_cache_bytecode = lambda: None
            interprete._intentar_cargar_cache = lambda *a, **k: None
            interprete._guardar_cache_bytecode = lambda *a, **k: None
        inicio = time.perf_counter()
        # Los benchmarks miden tiempo de ejecucion, no generan un reporte
        # legible imprimiendo miles de lineas de 'decir'/'crear_archivo' a
        # la pantalla -- se silencia la salida real del programa (sigue
        # ejecutandose de verdad, solo no se muestra) para que el
        # resultado del benchmark sea lo unico que se ve.
        with contextlib.redirect_stdout(io.StringIO()):
            interprete.ejecutar()
        return time.perf_counter() - inicio
    finally:
        try:
            os.remove(ruta)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Definicion de cada categoria: nombre -> (codigo .sipi generado, repeticiones)
# ---------------------------------------------------------------------------

def _programa_loops(n=200000):
    return f'''programa "Benchmark bucles"
variable contador = 0
repetir {n} veces
    sumar contador 1
fin
'''


def _programa_funciones(n=20000):
    return f'''programa "Benchmark funciones"
funcion sumar_uno con x
    devolver x + 1
fin

variable total = 0
repetir {n} veces
    variable total = sumar_uno(total)
fin
'''


def _programa_strings(n=20000):
    return f'''programa "Benchmark strings"
variable texto = ""
repetir {n} veces
    variable texto = texto + "a"
fin
decir longitud(texto)
'''


def _programa_listas(n=50000):
    return f'''programa "Benchmark listas"
variable lista = lista_crear()
repetir {n} veces
    lista_agregar lista 1
fin
decir lista_longitud(lista)
'''


def _programa_archivos(n=500):
    return f'''programa "Benchmark archivos"
variable i = 0
repetir {n} veces
    crear_archivo "bench_tmp_archivo_sipi.txt" "contenido de prueba"
    variable contenido = leer_archivo "bench_tmp_archivo_sipi.txt"
fin
borrar_archivo "bench_tmp_archivo_sipi.txt"
'''


def _programa_concurrencia(n=8):
    return f'''programa "Benchmark concurrencia"
funcion trabajo(id)
    variable suma = 0
    repetir 100000 veces
        sumar suma 1
    fin
    devolver suma
fin

variable hilos = lista_crear()
repetir {n} veces
    hilo_crear trabajo(0) -> h
    lista_agregar hilos h
fin
para_cada h en hilos
    hilo_esperar h
fin
'''


CATEGORIAS = {
    "loops": ("Bucles (repetir/sumar)", _programa_loops),
    "funciones": ("Funciones (llamada + retorno)", _programa_funciones),
    "strings": ("Strings (concatenacion)", _programa_strings),
    "listas": ("Listas (agregar)", _programa_listas),
    "archivos": ("Archivos (crear + leer)", _programa_archivos),
    "concurrencia": ("Concurrencia (hilos reales)", _programa_concurrencia),
}


def correr_benchmarks(categorias_pedidas=None, repeticiones=3):
    motor = _cargar_motor()
    categorias = categorias_pedidas or list(CATEGORIAS.keys())
    resultados = {}
    print(f"[SiPi Benchmarks] Version del motor: {getattr(motor, 'VERSION', '?')}")
    print(f"[SiPi Benchmarks] Python: {sys.version.split()[0]} en {sys.platform}")
    print("-" * 70)
    for clave in categorias:
        if clave not in CATEGORIAS:
            print(f"[SiPi Benchmarks] Categoria desconocida: '{clave}' (omitida)")
            continue
        nombre, generador = CATEGORIAS[clave]
        codigo = generador()
        tiempos = []
        for _ in range(repeticiones):
            tiempos.append(_correr_programa(motor, codigo))
        promedio = sum(tiempos) / len(tiempos)
        mejor = min(tiempos)
        print(f"{nombre:38s} promedio: {promedio*1000:8.1f} ms   mejor: {mejor*1000:8.1f} ms")
        resultados[clave] = {"nombre": nombre, "promedio_ms": promedio * 1000,
                              "mejor_ms": mejor * 1000, "corridas_ms": [t * 1000 for t in tiempos]}
    print("-" * 70)
    return resultados


def main():
    parser = argparse.ArgumentParser(description="Benchmarks oficiales de SiPi")
    parser.add_argument("--categoria", action="append",
                         help="Corre solo esta categoria (repetible). Por defecto: todas.")
    parser.add_argument("--repeticiones", type=int, default=3,
                         help="Cuantas veces correr cada benchmark (default 3, se muestra promedio y mejor)")
    parser.add_argument("--json", help="Ademas, guarda los resultados en este archivo JSON")
    args = parser.parse_args()

    resultados = correr_benchmarks(args.categoria, args.repeticiones)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        print(f"[SiPi Benchmarks] Resultados guardados en {args.json}")


if __name__ == "__main__":
    main()
