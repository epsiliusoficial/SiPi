#!/usr/bin/env python3
"""
sipi_cli.py - CLI profesional de SiPi.

Uso:
    sipi ejecutar archivo.sipi      Ejecuta un programa SiPi
    sipi crear nombre_proyecto      Crea un proyecto nuevo con estructura estandar
    sipi compilar archivo.sipi      Compila un programa a un ejecutable independiente
    sipi doc archivo.sipi           Genera documentacion HTML desde comentarios //! del codigo
    sipi instalar nombre_o_url      Instala un modulo .sipi (administrador de paquetes)
    sipi publicar                   Genera la carpeta PUBLICACION/ lista para distribuir
    sipi tutorial                   Corre el tutorial interactivo para principiantes
    sipi test                       Corre la bateria de pruebas automatizadas (regresion)
    sipi ayuda                      Muestra esta ayuda
    sipi ayuda mostrar comando      Ver que hace un comando puntual, con ejemplo
    sipi ayuda buscar texto         Buscar comandos por palabra clave

(En Windows, "sipi" es el nombre del .bat que llama a este script; en
Linux/macOS se usa "python3 sipi_cli.py <subcomando> ...".)
"""
import os
import sys
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))


def _ruta_motor():
    normal = os.path.join(AQUI, "sipi.py")
    protegido = os.path.join(AQUI, "sipi_protegido.py")
    if os.path.exists(normal):
        return normal
    if os.path.exists(protegido):
        return protegido
    print("[SiPi] Error: no se encontro 'sipi.py' ni 'sipi_protegido.py' en esta carpeta.")
    sys.exit(1)


def _ruta_generar_exe():
    normal = os.path.join(AQUI, "generar_exe.py")
    protegido = os.path.join(AQUI, "generar_exe_protegido.py")
    if os.path.exists(normal):
        return normal
    if os.path.exists(protegido):
        return protegido
    print("[SiPi] Error: no se encontro 'generar_exe.py' ni 'generar_exe_protegido.py' en esta carpeta.")
    sys.exit(1)


def _cargar_motor_como_modulo():
    """Carga el motor de SiPi (sipi.py o sipi_protegido.py) como modulo de
    Python, sin depender de que se llame literalmente 'sipi', para poder
    reutilizar su logica interna (instalar modulos, etc.) sin duplicarla."""
    import importlib.util
    ruta = _ruta_motor()
    spec = importlib.util.spec_from_file_location("motor_sipi_cli", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def cmd_ejecutar(args):
    if not args:
        print("Uso: sipi ejecutar archivo.sipi")
        sys.exit(1)
    archivo = args[0]
    if not os.path.exists(archivo):
        print(f"[SiPi] Error: no se encontro el archivo '{archivo}'")
        sys.exit(1)
    resultado = subprocess.run([sys.executable, _ruta_motor(), archivo] + args[1:])
    sys.exit(resultado.returncode)


def cmd_compilar(args):
    if not args:
        print("Uso: sipi compilar archivo.sipi")
        sys.exit(1)
    archivo = args[0]
    if not os.path.exists(archivo):
        print(f"[SiPi] Error: no se encontro el archivo '{archivo}'")
        sys.exit(1)
    resultado = subprocess.run([sys.executable, _ruta_generar_exe(), archivo])
    sys.exit(resultado.returncode)


def cmd_doc(args):
    if not args:
        print("Uso: sipi doc archivo.sipi")
        sys.exit(1)
    archivo = args[0]
    if not os.path.exists(archivo):
        print(f"[SiPi] Error: no se encontro el archivo '{archivo}'")
        sys.exit(1)
    ruta_generador = os.path.join(AQUI, "generar_docs.py")
    resultado = subprocess.run([sys.executable, ruta_generador, archivo])
    sys.exit(resultado.returncode)


def cmd_instalar(args):
    if not args:
        print('Uso: sipi instalar "nombre_o_url"')
        print("     sipi instalar --dependencias   (instala todo lo declarado en sipi_paquetes.json)")
        sys.exit(1)
    motor = _cargar_motor_como_modulo()
    interp = motor.Interprete(os.path.join(os.getcwd(), "_sipi_cli_temporal.sipi"))
    interp.entorno = motor.Entorno()
    if args[0] in ("--dependencias", "-d", "dependencias"):
        interp._instalar_dependencias()
        return
    for nombre_o_url in args:
        try:
            interp._instalar_modulo(nombre_o_url)
        except motor.SiPiError as e:
            print(f"[SiPi] Error instalando '{nombre_o_url}': {e}")
            sys.exit(1)


def cmd_publicar(args):
    ruta_publicar = os.path.join(AQUI, "publicar.py")
    if not os.path.exists(ruta_publicar):
        print("[SiPi] Error: no se encontro 'publicar.py' en esta carpeta (esta es una carpeta de desarrollo?).")
        sys.exit(1)
    resultado = subprocess.run([sys.executable, ruta_publicar])
    sys.exit(resultado.returncode)


PLANTILLA_MAIN = '''programa "{nombre}"

// Punto de entrada de tu proyecto. Corre con: sipi ejecutar main.sipi
decir "Hola desde {nombre}!"
'''

PLANTILLA_PAQUETES = '''{
  "modulos": {}
}
'''

PLANTILLA_README = '''# {nombre}

Proyecto creado con `sipi crear`.

## Estructura

- `main.sipi` — punto de entrada del programa.
- `ejemplos/` — programas de ejemplo o pruebas sueltas.
- `modulos_instalados/` — modulos de terceros (administrados con `sipi instalar`).
- `sipi_paquetes.json` — dependencias del proyecto (instalar todas con `sipi instalar --dependencias`).

## Como correrlo

```
sipi ejecutar main.sipi
```
'''


def cmd_crear(args):
    if not args:
        print("Uso: sipi crear nombre_proyecto")
        sys.exit(1)
    nombre = args[0]
    if os.path.exists(nombre):
        print(f"[SiPi] Error: ya existe una carpeta o archivo llamado '{nombre}'.")
        sys.exit(1)
    os.makedirs(nombre)
    os.makedirs(os.path.join(nombre, "ejemplos"))
    os.makedirs(os.path.join(nombre, "modulos_instalados"))
    with open(os.path.join(nombre, "main.sipi"), "w", encoding="utf-8") as f:
        f.write(PLANTILLA_MAIN.format(nombre=nombre))
    with open(os.path.join(nombre, "sipi_paquetes.json"), "w", encoding="utf-8") as f:
        f.write(PLANTILLA_PAQUETES)
    with open(os.path.join(nombre, "README.md"), "w", encoding="utf-8") as f:
        f.write(PLANTILLA_README.format(nombre=nombre))
    print(f"[SiPi] Proyecto '{nombre}' creado.")
    print("[SiPi] Para empezar:")
    print(f"         cd {nombre}")
    print("         sipi ejecutar main.sipi")


def cmd_ayuda(args):
    if args and args[0] in ("mostrar", "ver"):
        if len(args) < 2:
            print('Uso: sipi ayuda mostrar nombre_comando')
            sys.exit(1)
        nombre_comando = args[1]
        motor = _cargar_motor_como_modulo()
        ayuda_comandos = getattr(motor, "AYUDA_COMANDOS", {})
        if nombre_comando in ayuda_comandos:
            resumen, ejemplo = ayuda_comandos[nombre_comando]
            print(f"{nombre_comando}: {resumen}\n")
            print("Ejemplo:")
            print(ejemplo)
        elif nombre_comando in getattr(motor, "COMANDOS_CONOCIDOS", []):
            print(f"'{nombre_comando}' es un comando valido de SiPi, pero todavia no tiene una ficha corta.")
            print("Buscalo en DOCUMENTACION.md para ver su sintaxis completa.")
        else:
            import difflib
            candidatos = list(ayuda_comandos.keys()) + list(getattr(motor, "COMANDOS_CONOCIDOS", []))
            sugerencia = difflib.get_close_matches(nombre_comando, candidatos, n=1, cutoff=0.6)
            if sugerencia:
                print(f"No encontre el comando '{nombre_comando}'. ¿Quisiste decir '{sugerencia[0]}'?")
            else:
                print(f"No encontre el comando '{nombre_comando}'.")
        return
    if args and args[0] in ("buscar",):
        if len(args) < 2:
            print("Uso: sipi ayuda buscar texto_a_buscar")
            sys.exit(1)
        texto = " ".join(args[1:]).lower()
        motor = _cargar_motor_como_modulo()
        ayuda_comandos = getattr(motor, "AYUDA_COMANDOS", {})
        encontrados = [
            nombre for nombre, (resumen, _) in ayuda_comandos.items()
            if texto in nombre.lower() or texto in resumen.lower()
        ]
        if encontrados:
            print(f"Comandos que coinciden con '{texto}':")
            for nombre in sorted(encontrados):
                print(f"  - {nombre}: {ayuda_comandos[nombre][0]}")
        else:
            print(f"No encontre ningun comando relacionado con '{texto}'.")
        return
    print(__doc__)
    try:
        motor = _cargar_motor_como_modulo()
        comandos = sorted(getattr(motor, "COMANDOS_CONOCIDOS", []))
        print(f"El lenguaje SiPi tiene {len(comandos)} comandos. Referencia completa en DOCUMENTACION.md.")
        print("Tambien podes usar:")
        print("  sipi ayuda mostrar nombre_comando   Ver que hace un comando y un ejemplo")
        print("  sipi ayuda buscar texto             Buscar comandos por palabra clave")
    except Exception:
        pass


def cmd_tutorial(args):
    ruta_tutorial = os.path.join(AQUI, "ejemplos", "tutorial_interactivo.sipi")
    if not os.path.exists(ruta_tutorial):
        print("[SiPi] No se encontro el tutorial interactivo (ejemplos/tutorial_interactivo.sipi).")
        sys.exit(1)
    resultado = subprocess.run([sys.executable, _ruta_motor(), ruta_tutorial])
    sys.exit(resultado.returncode)


def cmd_test(args):
    ruta_tests = os.path.join(AQUI, "tests", "test_suite.py")
    if not os.path.exists(ruta_tests):
        print("[SiPi] No se encontro tests/test_suite.py en esta carpeta.")
        sys.exit(1)
    resultado = subprocess.run([sys.executable, ruta_tests] + args)
    sys.exit(resultado.returncode)


SUBCOMANDOS = {
    "ejecutar": cmd_ejecutar,
    "crear": cmd_crear,
    "compilar": cmd_compilar,
    "doc": cmd_doc,
    "instalar": cmd_instalar,
    "publicar": cmd_publicar,
    "tutorial": cmd_tutorial,
    "test": cmd_test,
    "ayuda": cmd_ayuda,
    "help": cmd_ayuda,
    "-h": cmd_ayuda,
    "--help": cmd_ayuda,
}


def main():
    if len(sys.argv) < 2:
        cmd_ayuda([])
        sys.exit(1)
    subcomando = sys.argv[1]
    resto = sys.argv[2:]
    funcion = SUBCOMANDOS.get(subcomando)
    if funcion is None:
        print(f"[SiPi] Subcomando desconocido: '{subcomando}'")
        cmd_ayuda([])
        sys.exit(1)
    funcion(resto)


if __name__ == "__main__":
    main()
