#!/usr/bin/env python3
"""
proyecto.py - Scaffolding y verificación de proyectos SiPi multi-archivo,
para Claude.

Uso:
    python3 claude/proyecto.py verificar CARPETA
        Corre TODOS los .sipi de una carpeta y devuelve el estado de cada
        uno en una sola llamada -- para confirmar que un proyecto grande
        (varios archivos) sigue sano después de un cambio, sin gastar un
        tool-call por archivo.

    python3 claude/proyecto.py listar CARPETA
        Lista los .sipi de una carpeta con su tamaño y un vistazo rápido
        de qué define cada uno (funciones, clases) -- para orientarse en
        un proyecto grande sin tener que abrir archivo por archivo.

    python3 claude/proyecto.py crear CARPETA
        Crea la carpeta si no existe (scaffolding mínimo -- SiPi no tiene
        estructura de proyecto obligatoria más allá de los .sipi sueltos).

Todo en JSON compacto por stdout, sin llamadas a ninguna API -- es
puramente local (subprocess + análisis de texto), pensado para que
verificar un proyecto completo cueste lo mismo que verificar un archivo.
"""
import os
import sys
import json
import subprocess
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ_REPO = os.path.dirname(AQUI)

PATRON_FUNCION = re.compile(r"^\s*funcion\s+(\w+)\s*\(", re.MULTILINE)
PATRON_CLASE = re.compile(r"^\s*clase\s+(\w+)", re.MULTILINE)


def _ruta_motor():
    for candidato in (
        os.path.join(RAIZ_REPO, "src", "sipi.py"),
        os.path.join(RAIZ_REPO, "src", "sipi_protegido.py"),
        os.path.join(RAIZ_REPO, "sipi.py"),
    ):
        if os.path.exists(candidato):
            return candidato
    return None


def _archivos_sipi(carpeta):
    if not os.path.isdir(carpeta):
        return []
    return sorted(f for f in os.listdir(carpeta) if f.endswith(".sipi"))


def verificar_proyecto(carpeta, timeout=15):
    ruta_motor = _ruta_motor()
    if not ruta_motor:
        return {"ok": False, "error": "No se encontro el motor de SiPi (sipi.py).", "resultados": []}

    archivos = _archivos_sipi(carpeta)
    if not archivos:
        return {"ok": False, "error": f"No hay archivos .sipi en '{carpeta}'.", "resultados": []}

    resultados = []
    for nombre in archivos:
        ruta = os.path.join(carpeta, nombre)
        try:
            resultado = subprocess.run(
                [sys.executable, ruta_motor, ruta], capture_output=True, text=True, timeout=timeout,
            )
            ok = resultado.returncode == 0
            error = None
            if not ok:
                combinado = resultado.stdout + resultado.stderr
                error = (combinado[combinado.index("[SiPi] Error"):].strip()
                          if "[SiPi] Error" in combinado else combinado.strip()[-300:])
            resultados.append({"archivo": nombre, "ok": ok, "error": error})
        except subprocess.TimeoutExpired:
            resultados.append({"archivo": nombre, "ok": None, "error": "timeout (puede estar esperando 'preguntar')"})

    return {
        "ok": all(r["ok"] for r in resultados),
        "total": len(resultados),
        "resultados": resultados,
    }


def listar_proyecto(carpeta):
    archivos = _archivos_sipi(carpeta)
    if not archivos:
        return {"ok": False, "error": f"No hay archivos .sipi en '{carpeta}'.", "archivos": []}

    detalle = []
    for nombre in archivos:
        ruta = os.path.join(carpeta, nombre)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
        except OSError as e:
            detalle.append({"archivo": nombre, "error": str(e)})
            continue
        detalle.append({
            "archivo": nombre,
            "lineas": contenido.count("\n") + 1,
            "funciones": PATRON_FUNCION.findall(contenido),
            "clases": PATRON_CLASE.findall(contenido),
        })
    return {"ok": True, "carpeta": os.path.abspath(carpeta), "archivos": detalle}


def crear_proyecto(carpeta):
    try:
        os.makedirs(carpeta, exist_ok=True)
    except OSError as e:
        return {"ok": False, "error": str(e)}
    return {"ok": True, "carpeta": os.path.abspath(carpeta)}


# Esqueletos multi-archivo listos para arrancar proyectos grandes de una
# sola vez, en lugar de escribir main.sipi desde cero cada vez. Cada
# plantilla ya sigue las convenciones correctas del motor (verificadas
# contra sipi.py real), asi que lo unico que queda es llenar la logica.
PLANTILLAS = {
    "cli": {
        "main.sipi": (
            'programa "{nombre}"\n\n'
            '// Punto de entrada. Import manual no existe en SiPi todavia --\n'
            '// los proyectos multi-archivo se organizan por convencion de\n'
            '// carpeta (ver claude/proyecto.py listar) y se pegan/adaptan\n'
            '// fragmentos entre archivos, no se importan en tiempo de\n'
            '// ejecucion. Este archivo es el que se ejecuta con sipi.py.\n\n'
            'funcion principal()\n'
            '    decir "{nombre} arrancando..."\n'
            '    // TODO: logica principal aca\n'
            'fin\n\n'
            'llamar principal()\n'
        ),
        "utilidades.sipi": (
            'programa "{nombre} - utilidades (referencia, pegar funciones en main.sipi)"\n\n'
            'funcion validar_no_vacio(texto)\n'
            '    si longitud(texto) == 0\n'
            '        devolver falso\n'
            '    fin\n'
            '    devolver verdadero\n'
            'fin\n'
        ),
    },
    "juego": {
        "main.sipi": (
            'programa "{nombre}"\n\n'
            'crear_juego "{nombre}" ancho 800 alto 600\n'
            '    sprite "jugador" en 400 300 color "azul" tamano 32\n\n'
            '    al_iniciar\n'
            '        puntaje_inicial 0\n'
            '        mostrar_puntaje\n'
            '    fin\n\n'
            '    cada_cuadro\n'
            '        // TODO: logica de movimiento, colisiones, IA\n'
            '    fin\n'
            'fin\n'
        ),
    },
    "web": {
        "main.sipi": (
            'programa "{nombre}"\n\n'
            'funcion responder_estado(pedido)\n'
            '    variable r = diccionario_crear()\n'
            '    diccionario_asignar r "ok" verdadero\n'
            '    devolver r\n'
            'fin\n\n'
            'escuchar_ruta "/api/estado" con responder_estado\n\n'
            '// Descomentar para levantar el servidor de verdad (bloquea):\n'
            '// iniciar_api_web 8080\n'
        ),
    },
    "gui": {
        "main.sipi": (
            'programa "{nombre}"\n\n'
            'ventana "{nombre}" ancho 500 alto 400\n'
            '    etiqueta "Bienvenido a {nombre}" en 20 20\n'
            '    boton "Aceptar" en 20 60 al_hacer_clic accion_aceptar\n'
            'fin\n\n'
            'funcion accion_aceptar()\n'
            '    decir "Boton presionado"\n'
            'fin\n'
        ),
    },
}


def crear_plantilla(carpeta, tipo, nombre=None):
    if tipo not in PLANTILLAS:
        return {"ok": False, "error": f"Plantilla desconocida: '{tipo}'. Opciones: {sorted(PLANTILLAS)}"}
    nombre = nombre or os.path.basename(os.path.abspath(carpeta))
    try:
        os.makedirs(carpeta, exist_ok=True)
    except OSError as e:
        return {"ok": False, "error": str(e)}

    creados = []
    for nombre_archivo, contenido in PLANTILLAS[tipo].items():
        ruta = os.path.join(carpeta, nombre_archivo)
        if os.path.exists(ruta):
            continue  # nunca pisar un archivo existente
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido.format(nombre=nombre))
        creados.append(nombre_archivo)

    return {"ok": True, "carpeta": os.path.abspath(carpeta), "tipo": tipo, "creados": creados}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "ok": False,
            "error": "Uso: python3 proyecto.py <verificar|listar|crear|plantilla> CARPETA [tipo] [nombre]",
        }))
        sys.exit(1)

    accion, carpeta = sys.argv[1], sys.argv[2]
    if accion == "verificar":
        resultado = verificar_proyecto(carpeta)
    elif accion == "listar":
        resultado = listar_proyecto(carpeta)
    elif accion == "crear":
        resultado = crear_proyecto(carpeta)
    elif accion == "plantilla":
        tipo = sys.argv[3] if len(sys.argv) > 3 else "cli"
        nombre = sys.argv[4] if len(sys.argv) > 4 else None
        resultado = crear_plantilla(carpeta, tipo, nombre)
    else:
        resultado = {"ok": False, "error": f"Accion desconocida: '{accion}'. Usar verificar, listar, crear o plantilla."}

    print(json.dumps(resultado, ensure_ascii=False))
    sys.exit(0 if resultado.get("ok") else 1)


if __name__ == "__main__":
    main()
