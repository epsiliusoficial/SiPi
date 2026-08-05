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


def correr(codigo_sipi, timeout=10):
    """Escribe 'codigo_sipi' en un archivo temporal y lo ejecuta con el
    motor real de SiPi. Devuelve (stdout, stderr, codigo_salida)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".sipi", delete=False, encoding="utf-8") as f:
        f.write(codigo_sipi)
        ruta = f.name
    try:
        resultado = subprocess.run(
            [sys.executable, MOTOR, ruta],
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
