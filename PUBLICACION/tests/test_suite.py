#!/usr/bin/env python3
"""
tests/test_suite.py - Pruebas automatizadas reales de SiPi.

No son simulaciones: cada test escribe un programa .sipi de verdad en un
archivo temporal, lo ejecuta con el motor real (sipi.py) en un
subproceso, y compara la salida real contra lo esperado. Sirven como
red de seguridad: si un cambio futuro rompe algo que ya funcionaba
(una regresion), estos tests lo detectan.

Uso:
    python3 tests/test_suite.py
    (o) sipi test          (desde la CLI profesional)

Requiere solo la libreria estandar (no pytest), para que corra en
cualquier maquina sin instalar nada extra.
"""
import os
import sys
import subprocess
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
MOTOR = os.path.join(RAIZ, "sipi.py") if os.path.exists(os.path.join(RAIZ, "sipi.py")) \
    else os.path.join(RAIZ, "sipi_protegido.py")


def correr(codigo_sipi, timeout=10, args=None):
    """Escribe 'codigo_sipi' en un archivo temporal y lo ejecuta con el
    motor real de SiPi. Devuelve (stdout, stderr, codigo_salida)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".sipi", delete=False, encoding="utf-8") as f:
        f.write(codigo_sipi)
        ruta = f.name
    try:
        resultado = subprocess.run(
            [sys.executable, MOTOR] + (args or []) + [ruta],
            capture_output=True, text=True, timeout=timeout, cwd=tempfile.gettempdir(),
        )
        return resultado.stdout, resultado.stderr, resultado.returncode
    finally:
        os.unlink(ruta)


class TestControlDeFlujo(unittest.TestCase):
    def test_romper_y_continuar(self):
        salida, _, codigo = correr('''programa "T"
variable i = 0
mientras i < 5
    sumar i 1
    si i == 2
        continuar
    fin
    si i == 4
        romper
    fin
    imprimir i
fin
''')
        self.assertEqual(codigo, 0)
        self.assertEqual(salida.strip(), "1\n3".replace("\n", "\n"))

    def test_romper_fuera_de_bucle_da_error_claro(self):
        salida, _, codigo = correr('programa "T"\nromper\n')
        self.assertNotEqual(codigo, 0)
        self.assertIn("fuera de un bucle", salida)

    def test_romper_dentro_de_funcion_no_rompe_el_bucle_del_llamador(self):
        # Bug historico: un 'romper' dentro de una funcion sin bucle propio
        # se filtraba y rompia el bucle de quien llamaba a esa funcion.
        salida, _, codigo = correr('''programa "T"
funcion romper_mal()
    romper
fin
repetir 3 veces
    llamar romper_mal()
fin
''')
        self.assertNotEqual(codigo, 0)
        self.assertIn("fuera de un bucle", salida)


class TestExpresiones(unittest.TestCase):
    def test_llamada_a_funcion_dentro_de_expresion(self):
        # Bug historico critico: 'variable r = doble(5)' devolvia el texto
        # crudo "doble(5)" en vez de llamar a la funcion.
        salida, _, codigo = correr('''programa "T"
funcion doble(x)
    devolver x * 2
fin
variable r = doble(21)
imprimir r
''')
        self.assertEqual(codigo, 0)
        self.assertEqual(salida.strip(), "42")

    def test_llamadas_anidadas(self):
        salida, _, codigo = correr('''programa "T"
funcion doble(x)
    devolver x * 2
fin
funcion mas_uno(x)
    devolver x + 1
fin
imprimir mas_uno(doble(3))
''')
        self.assertEqual(codigo, 0)
        self.assertEqual(salida.strip(), "7")

    def test_concatenacion_tres_partes(self):
        # Bug historico: "texto" + variable + "texto" se confundia con un
        # unico literal y no se evaluaba.
        salida, _, codigo = correr('''programa "T"
variable nombre = "Mateo"
variable r = "Hola " + nombre + " desde SiPi!"
imprimir r
''')
        self.assertEqual(codigo, 0)
        self.assertEqual(salida.strip(), "Hola Mateo desde SiPi!")

    def test_division_por_cero_da_error_claro(self):
        salida, _, codigo = correr('''programa "T"
variable a = 10
variable b = 0
variable r = a / b
imprimir r
''')
        self.assertNotEqual(codigo, 0)
        self.assertIn("Division por cero", salida)

    def test_variable_no_declarada_da_error_claro(self):
        salida, _, codigo = correr('programa "T"\nimprimir variable_que_no_existe\n')
        self.assertNotEqual(codigo, 0)
        self.assertIn("no declarada", salida)

    def test_recursion_profunda_real(self):
        salida, _, codigo = correr('''programa "T"
funcion contar(n)
    si n <= 0
        devolver 0
    fin
    devolver contar(n - 1) + 1
fin
imprimir contar(3000)
''', timeout=20)
        self.assertEqual(codigo, 0)
        self.assertEqual(salida.strip(), "3000")


class TestManejoDeErrores(unittest.TestCase):
    def test_lanzar_error_y_capturar(self):
        salida, _, codigo = correr('''programa "T"
funcion validar(edad)
    si edad < 0
        lanzar_error "Edad invalida"
    fin
    devolver edad
fin
intentar
    llamar_valor validar(-1) -> r
capturar
    imprimir "Capturado: {error}"
fin
''')
        self.assertEqual(codigo, 0)
        self.assertIn("Capturado: Edad invalida", salida)

    def test_const_no_se_puede_reasignar(self):
        salida, _, codigo = correr('programa "T"\nconst X = 5\nsumar X 1\n')
        self.assertNotEqual(codigo, 0)
        self.assertIn("constante", salida)


class TestListasYFuncional(unittest.TestCase):
    def test_lista_mapear_filtrar_reducir(self):
        salida, _, codigo = correr('''programa "T"
funcion doble(x)
    devolver x * 2
fin
funcion es_par(x)
    si x == 2
        devolver verdadero
    fin
    devolver falso
fin
funcion sumar_acc(acc, x)
    devolver acc + x
fin
lista_crear n
lista_agregar n 1
lista_agregar n 2
lista_agregar n 3
lista_mapear n con doble -> dobles
lista_filtrar n con es_par -> pares
lista_reducir n con sumar_acc desde 0 -> total
imprimir dobles
imprimir pares
imprimir total
''')
        self.assertEqual(codigo, 0)
        lineas = salida.strip().split("\n")
        self.assertEqual(lineas[0], "[2, 4, 6]")
        self.assertEqual(lineas[1], "[2]")
        self.assertEqual(lineas[2], "6")


class TestFormateador(unittest.TestCase):
    def test_formatear_indenta_pagina_web_y_formulario(self):
        # Bug historico: PALABRAS_APERTURA_BLOQUE del formateador no incluia
        # 'pagina_web' ni 'formulario', asi que --formatear no indentaba
        # esos bloques (quedaban todos al mismo nivel).
        sys.path.insert(0, RAIZ)
        import importlib
        motor = importlib.import_module("sipi") if os.path.exists(os.path.join(RAIZ, "sipi.py")) else None
        if motor is None:
            self.skipTest("Solo aplica en carpeta de desarrollo (con sipi.py)")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".sipi", delete=False, encoding="utf-8") as f:
            f.write('programa "T"\npagina_web "X"\ntitulo "Y"\nformulario "c"\ncampo "n"\nfin\nfin\n')
            ruta = f.name
        try:
            resultado = motor.formatear_codigo(ruta)
        finally:
            os.unlink(ruta)
        lineas = resultado.split("\n")
        self.assertTrue(lineas[2].startswith("    titulo"))
        self.assertTrue(lineas[3].startswith("    formulario"))
        self.assertTrue(lineas[4].startswith("        campo"))


class TestSQLite(unittest.TestCase):
    def test_sqlite_real(self):
        salida, _, codigo = correr('''programa "T"
sqlite_conectar "test_suite_temporal.db" como db
sqlite_ejecutar db "CREATE TABLE IF NOT EXISTS t (id INTEGER, val TEXT)"
sqlite_ejecutar db "DELETE FROM t"
sqlite_ejecutar db "INSERT INTO t VALUES (1, 'hola')"
sqlite_consultar db "SELECT * FROM t" en filas
imprimir filas
sqlite_cerrar db
''')
        self.assertEqual(codigo, 0)
        self.assertIn("'val': 'hola'", salida)
        ruta_db = os.path.join(tempfile.gettempdir(), "test_suite_temporal.db")
        if os.path.exists(ruta_db):
            os.unlink(ruta_db)


class TestConcatenacionTextoYNumero(unittest.TestCase):
    def test_concatenar_texto_con_numero(self):
        # Bug historico: "texto" + numero (o numero + "texto") tiraba un
        # TypeError de Python y se devolvia el texto crudo sin evaluar.
        salida, _, codigo = correr('''programa "T"
variable nombre = "Rex"
variable vida = 100
variable r = nombre + " tiene " + vida + " de vida"
imprimir r
''')
        self.assertEqual(codigo, 0)
        self.assertEqual(salida.strip(), "Rex tiene 100 de vida")


class TestProgramacionOrientadaAObjetos(unittest.TestCase):
    def test_clases_herencia_y_polimorfismo(self):
        salida, _, codigo = correr('''programa "T"
clase Animal
    nombre = "sin nombre"
    metodo constructor(nombre_inicial)
        diccionario_asignar este "nombre" nombre_inicial
    fin
    metodo hacer_sonido()
        devolver "..."
    fin
fin
clase Perro hereda_de Animal
    metodo hacer_sonido()
        devolver "Guau!"
    fin
fin
nuevo Perro("Rex") -> rex
diccionario_obtener rex "nombre" -> n
llamar_metodo rex "hacer_sonido"() -> sonido
imprimir n
imprimir sonido
es_instancia_de rex Animal -> es_animal
imprimir es_animal
''')
        self.assertEqual(codigo, 0)
        lineas = salida.strip().split("\n")
        self.assertEqual(lineas[0], "Rex")
        self.assertEqual(lineas[1], "Guau!")
        self.assertEqual(lineas[2], "verdadero")

    def test_campo_con_nombre_igual_a_palabra_reservada_no_rompe_el_conteo_de_fin(self):
        # Bug historico: agregar 'clase' como palabra reservada (para el
        # sistema de POO) rompia cualquier programa que ya tuviera un campo
        # o variable llamado literalmente 'clase' (ej. dentro de una
        # 'estructura'), porque el detector de bloques lo confundia con la
        # apertura de un bloque de clase real.
        salida, _, codigo = correr('''programa "T"
estructura Personaje
    nombre = "Sin nombre"
    clase = 0
fin
instanciar Personaje -> p
diccionario_obtener p "clase" -> c
imprimir c
''')
        self.assertEqual(codigo, 0)
        self.assertEqual(salida.strip(), "0")


class TestREPL(unittest.TestCase):
    """REPL interactivo (sipi.py --repl). Se prueba alimentando stdin como
    si fuera una sesion real tipeada a mano, igual que un usuario haria."""

    def _correr_repl(self, entrada_stdin, timeout=15):
        proceso = subprocess.run(
            [sys.executable, os.path.join(RAIZ, "sipi.py"), "--repl"],
            input=entrada_stdin, capture_output=True, text=True, timeout=timeout,
        )
        return proceso.stdout

    def test_mantiene_estado_entre_lineas_y_evalua_expresiones(self):
        salida = self._correr_repl('variable x = 5\n2 + 2\ndecir x\nsalir\n')
        self.assertIn("4", salida)
        self.assertIn("5", salida)

    def test_soporta_bloques_multilinea(self):
        salida = self._correr_repl(
            'funcion doble(n)\n    devolver n * 2\nfin\ndoble(21)\nsalir\n'
        )
        self.assertIn("42", salida)

    def test_sobrevive_a_un_error_y_sigue_manteniendo_el_estado(self):
        salida = self._correr_repl(
            'variable x = 1\ndecir variable_que_no_existe\ndecir "sigo vivo"\ndecir x\nsalir\n'
        )
        self.assertIn("ERROR", salida)
        self.assertIn("sigo vivo", salida)
        self.assertIn("1", salida)

    def test_autocorrige_un_comando_mal_escrito_sin_romper_la_linea(self):
        # Regresion de un bug real encontrado durante el desarrollo: la
        # correccion automatica se decidia ANTES de intentar autocorregir,
        # asi que 'decid "x"' terminaba mal-envuelto como
        # 'decir decid "x"' en vez de corregirse a 'decir "x"'.
        salida = self._correr_repl('decid "mensaje correcto"\nsalir\n')
        self.assertIn("mensaje correcto", salida)
        self.assertNotIn('decid "mensaje correcto"', salida)


class TestBanderaDepurar(unittest.TestCase):
    def test_depurar_muestra_cada_linea_y_ejecuta_normal(self):
        salida, _, codigo = correr('programa "T"\nvariable x = 1\ndecir "x={x}"\n', args=["--depurar"])
        self.assertEqual(codigo, 0)
        self.assertIn("DEBUG", salida)
        self.assertIn("x=1", salida)


class TestInterpolacionEnConcatenacion(unittest.TestCase):
    """Bug real encontrado y corregido en esta revision: '{variable}' solo
    se interpolaba cuando el string era un literal SUELTO (ej. decir "hola
    {x}"). Si el string formaba parte de una concatenacion con '+' (ej.
    'algo + "hola {x}"'), las llaves quedaban sin reemplazar. El fix
    tambien tuvo que preservar la decodificacion de escapes de Python
    (\\n, \\t) en ese mismo camino, que se habia roto en un primer intento."""

    def test_interpola_variable_dentro_de_una_concatenacion(self):
        salida, _, codigo = correr(
            'programa "T"\nvariable id_hilo = "X"\ndecir "prefijo-" + "hilo-{id_hilo}"\n'
        )
        self.assertEqual(codigo, 0)
        self.assertIn("prefijo-hilo-X", salida)
        self.assertNotIn("{id_hilo}", salida)

    def test_interpola_dentro_de_parametro_de_funcion_concatenado(self):
        salida, _, codigo = correr(
            'programa "T"\n'
            'funcion probar(id)\n'
            '    devolver "valor: " + "{id}"\n'
            'fin\n'
            'llamar_valor probar("Y") -> r\n'
            'decir r\n'
        )
        self.assertEqual(codigo, 0)
        self.assertIn("valor: Y", salida)

    def test_decodifica_saltos_de_linea_dentro_de_una_concatenacion(self):
        salida, _, codigo = correr(
            'programa "T"\nvariable x = "a"\ndecir x + "b\\nc"\n'
        )
        self.assertEqual(codigo, 0)
        self.assertIn("ab\nc", salida)


class TestCrearArchivoConExpresion(unittest.TestCase):
    """Bug real encontrado y corregido en esta revision: 'crear_archivo'
    solo aceptaba un literal completo o una unica variable como contenido.
    Una expresion como 'variable + "texto"' no matcheaba el regex viejo y
    el comando fallaba en TOTAL SILENCIO (sin ningun error ni escritura),
    el peor tipo de bug para alguien que recien esta aprendiendo."""

    def test_acepta_una_expresion_como_contenido(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = os.path.join(tmp, "salida.txt").replace("\\", "/")
            salida, _, codigo = correr(
                f'programa "T"\n'
                f'variable base = "hola"\n'
                f'crear_archivo "{ruta}" base + " mundo"\n'
                f'leer_archivo "{ruta}" -> r\n'
                f'decir r\n'
            )
            self.assertEqual(codigo, 0)
            self.assertIn("hola mundo", salida)


class TestHilosReales(unittest.TestCase):
    """Concurrencia real (threading.Thread de verdad, no cooperativa). Ver
    _clonar_para_hilo en sipi.py para el diseño (cada hilo tiene su propia
    copia de variables, para evitar condiciones de carrera)."""

    def test_hilo_crear_y_hilo_resultado_devuelven_el_valor_correcto(self):
        # Regresion de un bug real: el resultado se guardaba en una COPIA
        # del diccionario de estado en vez de la referencia compartida con
        # el hilo, asi que 'hilo_resultado' siempre devolvia 'nulo'.
        salida, _, codigo = correr(
            'programa "T"\n'
            'funcion doble(n)\n    devolver n * 2\nfin\n'
            'hilo_crear doble(21) -> h\n'
            'hilo_resultado h -> r\n'
            'decir r\n'
        )
        self.assertEqual(codigo, 0)
        self.assertIn("42", salida)

    def test_hilos_corren_en_paralelo_de_verdad(self):
        import time
        inicio = time.time()
        salida, _, codigo = correr(
            'programa "T"\n'
            'funcion tardar(s)\n    esperar s\n    devolver s\nfin\n'
            'hilo_crear tardar(1) -> h1\n'
            'hilo_crear tardar(1) -> h2\n'
            'hilo_esperar h1\nhilo_esperar h2\n'
            'decir "listo"\n',
            timeout=8,
        )
        duracion = time.time() - inicio
        self.assertEqual(codigo, 0)
        self.assertLess(duracion, 1.8)  # si fuera secuencial tardaria ~2s

    def test_con_bloqueo_sincroniza_escrituras_a_un_archivo_compartido(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = os.path.join(tmp, "log.txt").replace("\\", "/")
            _, _, codigo = correr(
                f'programa "T"\n'
                f'bloqueo_crear candado\n'
                f'crear_archivo "{ruta}" ""\n'
                f'funcion escribir(n)\n'
                f'    variable i = 0\n'
                f'    mientras i < 20\n'
                f'        con_bloqueo candado\n'
                f'            leer_archivo "{ruta}" -> actual\n'
                f'            crear_archivo "{ruta}" actual + "x"\n'
                f'        fin\n'
                f'        sumar i 1\n'
                f'    fin\n'
                f'    devolver 1\n'
                f'fin\n'
                f'hilo_crear escribir(1) -> h1\n'
                f'hilo_crear escribir(2) -> h2\n'
                f'hilo_esperar_todos\n',
                timeout=15,
            )
            self.assertEqual(codigo, 0)
            with open(ruta, encoding="utf-8") as f:
                contenido = f.read()
            # Sin el candado, escrituras concurrentes pisandose entre si
            # perderian caracteres -- con el candado, tienen que ser
            # exactamente 40 ('x' x 20 escrituras x 2 hilos).
            self.assertEqual(len(contenido), 40)


class TestAutocorrector(unittest.TestCase):
    """El corrector automatico de errores tipograficos (ver FUNCTIONS.md,
    seccion 'Corrector automatico y revisor de codigo')."""

    def test_corrige_espacios_dobles_comillas_curvas_punto_suelto_y_typo(self):
        salida, _, codigo = correr(
            'programa "T"\n'
            'variable  nombre = "Mateo"\n'
            'decid "Hola " + nombre.\n'
        )
        self.assertEqual(codigo, 0)
        self.assertIn("Hola Mateo", salida)
        self.assertIn("se corrigieron autom", salida.lower())

    def test_no_toca_espacios_dentro_de_un_string(self):
        # Los espacios de mas DENTRO de un texto entre comillas son una
        # decision del usuario, no un error -- nunca deben colapsarse.
        salida, _, codigo = correr('programa "T"\ndecir "a    b"\n')
        self.assertEqual(codigo, 0)
        self.assertIn("a    b", salida)

    def test_no_autocorrige_comando_ambiguo(self):
        # 'intentar' y 'mientras' estan a la misma distancia de 'mientars':
        # con mas de una opcion razonable, el corrector no debe adivinar.
        _, _, codigo = correr('programa "T"\nmientars verdadero\nfin\n')
        self.assertNotEqual(codigo, 0)


class TestRevisorDeCodigo(unittest.TestCase):
    """El analizador estatico (--revisar), ver sipi.py:_analizar_codigo_estatico."""

    def test_detecta_credencial_hardcodeada_y_sql_injection_y_capturar_vacio(self):
        import sipi
        contenido = (
            'programa "T"\n'
            'variable api_key = "sk-secreto123"\n'
            'sqlite_conectar "d.db" como db\n'
            'sqlite_consultar db "SELECT * FROM t WHERE n = \'{nombre}\'" en filas\n'
            'intentar\n'
            '    variable x = 1\n'
            'capturar\n'
            'fin\n'
        )
        hallazgos = sipi._analizar_codigo_estatico(contenido)
        self.assertTrue(any("api_key" in h for h in hallazgos["seguridad"]))
        self.assertTrue(any("inyecci" in h.lower() for h in hallazgos["seguridad"]))
        self.assertTrue(any("capturar" in h and "vac" in h for h in hallazgos["bugs"]))

    def test_no_da_falsos_positivos_en_codigo_limpio(self):
        import sipi
        contenido = 'programa "T"\nvariable x = 1\ndecir "{x}"\n'
        hallazgos = sipi._analizar_codigo_estatico(contenido)
        total = sum(len(v) for v in hallazgos.values())
        self.assertEqual(total, 0)


class TestGenerarExeProtegeElProgramaDelUsuario(unittest.TestCase):
    """Bug real encontrado y corregido en esta revision: generar_exe.py
    embebia el programa del usuario en TEXTO PLANO dentro del wrapper que
    PyInstaller compila (el motor podia estar protegido, pero el programa
    del usuario -- la razon de compilar a .exe -- no). No corre PyInstaller
    de verdad aca (demasiado pesado/lento para el test suite normal); en
    cambio valida directamente que la funcion de ofuscacion del wrapper
    (_ofuscar_wrapper) hace lo que promete: el archivo resultante en disco
    no contiene el codigo fuente en texto plano, y sigue ejecutando
    exactamente lo mismo que el original al importarlo/ejecutarlo."""

    def test_wrapper_ofuscado_no_contiene_el_codigo_en_texto_plano_y_ejecuta_igual(self):
        sys.path.insert(0, RAIZ)
        import generar_exe

        secreto = "ESTO_NO_DEBERIA_APARECER_EN_TEXTO_PLANO_XYZ"
        with tempfile.TemporaryDirectory() as tmp:
            original = os.path.join(tmp, "original.py")
            protegido = os.path.join(tmp, "protegido.py")
            with open(original, "w", encoding="utf-8") as f:
                f.write(f'CODIGO_SIPI = "{secreto}"\nprint(CODIGO_SIPI)\n')

            generar_exe._ofuscar_wrapper(original, protegido)

            with open(protegido, "r", encoding="utf-8") as f:
                contenido_protegido = f.read()
            self.assertNotIn(secreto, contenido_protegido)

            resultado = subprocess.run([sys.executable, protegido], capture_output=True, text=True, timeout=10)
            self.assertEqual(resultado.returncode, 0)
            self.assertIn(secreto, resultado.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
