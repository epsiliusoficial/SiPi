#!/usr/bin/env python3
"""
sipi_cli.py - CLI profesional de SiPi.

Uso:
    sipi ejecutar archivo.sipi      Ejecuta un programa SiPi
    sipi crear nombre_proyecto      Crea un proyecto nuevo con estructura estandar
    sipi compilar archivo.sipi      Compila un programa a un ejecutable independiente
    sipi doc archivo.sipi           Genera documentacion HTML desde comentarios //! del codigo
    sipi instalar nombre_o_url      Instala un modulo .sipi (administrador de paquetes)
    sipi cache tamaño               Muestra cuanto ocupa la cache (.sipic) en esta carpeta
    sipi cache limpiar               Borra los .sipic encontrados (pide confirmacion, o --todo)
    sipi benchmarks                  Corre los benchmarks oficiales (loops, funciones, strings, listas, archivos, hilos)
    sipi publicar                   Genera la carpeta PUBLICACION/ lista para distribuir
    sipi tutorial                   Corre el tutorial interactivo para principiantes
    sipi test / sipi probar         Corre la bateria de pruebas automatizadas (regresion)
    sipi repl                       Abre la consola interactiva de SiPi
    sipi formato archivo.sipi       Reindenta el archivo (4 espacios por nivel)
    sipi corregir archivo.sipi      Corrige errores tipograficos chicos y guarda el archivo
    sipi analizar archivo.sipi      Revisa bugs, seguridad y estilo (sin ejecutar el programa)
    sipi depurar archivo.sipi       Ejecuta mostrando cada linea antes de correrla
    sipi ayuda                      Muestra esta ayuda
    sipi ayuda mostrar comando      Ver que hace un comando puntual, con ejemplo
    sipi ayuda buscar texto         Buscar comandos por palabra clave

(En Windows, "sipi" es el nombre del .bat que llama a este script; en
Linux/macOS se usa "python3 sipi_cli.py <subcomando> ...".)
"""
import os
import sys
import subprocess
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))


def _advertir_si_carpeta_volatil():
    """Misma deteccion que editor_sipi.py: si 'sipi_cli.py' se esta
    corriendo desde adentro de la carpeta temporal del sistema (tipico de
    abrir el .zip descargado con doble clic sin extraerlo antes), avisa
    con causa y solucion en vez de dejar que aparezca despues un
    '[Errno 2] No such file or directory' sin contexto."""
    try:
        temporal = os.path.normcase(os.path.abspath(tempfile.gettempdir()))
        actual = os.path.normcase(AQUI)
        if actual.startswith(temporal):
            print("=" * 70)
            print("[SiPi] Aviso: estas ejecutando SiPi desde una carpeta temporal:")
            print(f"       {AQUI}")
            print("       Es probable que hayas abierto el .zip descargado sin")
            print("       extraerlo primero. Extrae el .zip completo a una carpeta")
            print("       normal del disco y volve a correr SiPi desde ahi -- si no,")
            print("       Windows puede borrar estos archivos en cualquier momento,")
            print("       incluso a mitad de la ejecucion.")
            print("=" * 70)
    except OSError:
        pass


def _error_motor_no_encontrado(nombre_normal, nombre_protegido):
    print(f"[SiPi] No se encontro '{nombre_normal}' ni '{nombre_protegido}' en esta carpeta.")
    print(f"       Carpeta donde se busco: {AQUI}")
    print("       Causa mas probable: SiPi se esta ejecutando desde una copia")
    print("       incompleta (por ejemplo, un .zip sin extraer del todo) o un")
    print("       archivo fue borrado por un antivirus/limpiador de temporales.")
    print("       Extrae el proyecto completo a una carpeta normal e intenta de nuevo.")


def _ruta_motor():
    normal = os.path.join(AQUI, "sipi.py")
    protegido = os.path.join(AQUI, "sipi_protegido.py")
    if os.path.exists(normal):
        return normal
    if os.path.exists(protegido):
        return protegido
    _error_motor_no_encontrado("sipi.py", "sipi_protegido.py")
    sys.exit(1)


def _ruta_generar_exe():
    normal = os.path.join(AQUI, "generar_exe.py")
    protegido = os.path.join(AQUI, "generar_exe_protegido.py")
    if os.path.exists(normal):
        return normal
    if os.path.exists(protegido):
        return protegido
    _error_motor_no_encontrado("generar_exe.py", "generar_exe_protegido.py")
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


def cmd_repl(args):
    resultado = subprocess.run([sys.executable, _ruta_motor(), "--repl"])
    sys.exit(resultado.returncode)


def cmd_formato(args):
    if not args:
        print("Uso: sipi formato archivo.sipi")
        sys.exit(1)
    resultado = subprocess.run([sys.executable, _ruta_motor(), "--formatear"] + args)
    sys.exit(resultado.returncode)


def cmd_corregir(args):
    if not args:
        print("Uso: sipi corregir archivo.sipi")
        sys.exit(1)
    resultado = subprocess.run([sys.executable, _ruta_motor(), "--corregir"] + args)
    sys.exit(resultado.returncode)


def cmd_analizar(args):
    if not args:
        print("Uso: sipi analizar archivo.sipi")
        sys.exit(1)
    resultado = subprocess.run([sys.executable, _ruta_motor(), "--revisar"] + args)
    sys.exit(resultado.returncode)


def cmd_depurar(args):
    if not args:
        print("Uso: sipi depurar archivo.sipi")
        sys.exit(1)
    resultado = subprocess.run([sys.executable, _ruta_motor(), "--depurar"] + args)
    sys.exit(resultado.returncode)


def _buscar_archivos_cache(carpeta_raiz):
    """Recorre 'carpeta_raiz' buscando todos los '.sipic' (ver CACHE.md:
    son archivos chicos, uno por cada '.sipi', al lado del original -- no
    existe una carpeta central de cache). Se salta '.git', 'node_modules'
    y carpetas ocultas para no tardar de mas en proyectos grandes."""
    encontrados = []
    for actual, carpetas, archivos in os.walk(carpeta_raiz):
        carpetas[:] = [c for c in carpetas if c not in (".git", "node_modules") and not c.startswith(".")]
        for nombre in archivos:
            if nombre.endswith(".sipic"):
                encontrados.append(os.path.join(actual, nombre))
    return encontrados


def cmd_cache(args):
    """Items 37/38/39 del feedback: 'sipi cache tamaño', 'sipi cache
    limpiar' (con confirmacion) y 'sipi cache limpiar --todo' (sin
    preguntar, para scripts/CI). Busca desde el directorio actual hacia
    abajo, ya que la cache de SiPi no vive en una carpeta central sino
    repartida junto a cada '.sipi' (documentado en CACHE.md)."""
    accion = args[0] if args else None
    raiz = os.getcwd()
    if accion == "tamaño" or accion == "tamano":
        archivos = _buscar_archivos_cache(raiz)
        total = sum(os.path.getsize(a) for a in archivos)
        print(f"[SiPi] {len(archivos)} archivo(s) .sipic encontrados bajo {raiz}")
        print(f"[SiPi] Tamaño total: {total / 1024:.1f} KB")
        return
    if accion == "limpiar":
        archivos = _buscar_archivos_cache(raiz)
        if not archivos:
            print("[SiPi] No hay archivos .sipic para limpiar.")
            return
        total = sum(os.path.getsize(a) for a in archivos)
        forzar = "--todo" in args
        if not forzar:
            respuesta = input(
                f"[SiPi] Se van a borrar {len(archivos)} archivo(s) .sipic "
                f"({total / 1024:.1f} KB). ¿Confirmar? (s/n): "
            ).strip().lower()
            if respuesta != "s":
                print("[SiPi] Cancelado, no se borro nada.")
                return
        borrados = 0
        for archivo in archivos:
            try:
                os.remove(archivo)
                borrados += 1
            except OSError as error:
                print(f"[SiPi] No se pudo borrar {archivo}: {error}")
        print(f"[SiPi] {borrados} archivo(s) .sipic borrados ({total / 1024:.1f} KB liberados).")
        print("[SiPi] Se regeneraran solos en la proxima ejecucion de cada .sipi -- no rompe nada.")
        return
    print("Uso:")
    print("    sipi cache tamaño            Muestra cuanto ocupa la cache (.sipic) en esta carpeta")
    print("    sipi cache limpiar           Borra los .sipic encontrados (pide confirmacion)")
    print("    sipi cache limpiar --todo    Borra los .sipic sin preguntar")
    sys.exit(1)


def cmd_benchmarks(args):
    """Item #65 del feedback: benchmarks oficiales. Delega en
    benchmarks.py (motor + generador de programas .sipi reales), pasando
    los argumentos tal cual para no duplicar el parser de opciones."""
    ruta_benchmarks = os.path.join(AQUI, "benchmarks.py")
    if not os.path.exists(ruta_benchmarks):
        print("[SiPi] No se encontro 'benchmarks.py' en esta carpeta.")
        sys.exit(1)
    resultado = subprocess.run([sys.executable, ruta_benchmarks] + args)
    sys.exit(resultado.returncode)


SUBCOMANDOS = {
    "ejecutar": cmd_ejecutar,
    "crear": cmd_crear,
    "compilar": cmd_compilar,
    "doc": cmd_doc,
    "instalar": cmd_instalar,
    "cache": cmd_cache,
    "benchmarks": cmd_benchmarks,
    "publicar": cmd_publicar,
    "tutorial": cmd_tutorial,
    "test": cmd_test,
    "probar": cmd_test,
    "repl": cmd_repl,
    "formato": cmd_formato,
    "corregir": cmd_corregir,
    "analizar": cmd_analizar,
    "depurar": cmd_depurar,
    "ayuda": cmd_ayuda,
    "help": cmd_ayuda,
    "-h": cmd_ayuda,
    "--help": cmd_ayuda,
}


def main():
    _advertir_si_carpeta_volatil()
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
