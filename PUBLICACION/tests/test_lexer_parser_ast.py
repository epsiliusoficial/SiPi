#!/usr/bin/env python3
"""
tests/test_lexer_parser_ast.py - Tests reales para lexer_sipi.py y
ast_sipi.py (fase 1 de los items #23-25 del feedback).

Ademas de probar el lexer/parser/AST por su cuenta, cruza resultados
contra 'Interprete.evaluar_expresion' del motor de produccion real
(sipi.py) para el subconjunto de expresiones donde ambos deberian
coincidir exactamente -- asi no es solo "el AST es internamente
consistente", sino "el AST calcula lo mismo que el interprete real que
la gente ya esta usando".
"""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from lexer_sipi import tokenizar, TipoToken, ErrorLexico
from ast_sipi import (
    parsear, evaluar_texto, evaluar, ErrorSintactico, ErrorEvaluacion,
    NumeroLiteral, Binario, Unario, Variable,
)

import importlib
sipi = importlib.import_module("sipi")


def _interprete_vacio():
    """Un Interprete real, construido de la forma NORMAL y soportada (a
    partir de un archivo .sipi real en disco), en vez de reconstruir a
    mano sus atributos internos con Interprete.__new__() -- ese approach
    resulto ser fragil (el Interprete real tiene bastante mas estado
    interno de lo que parecia a primera vista: 'entorno', 'pila_scopes',
    etc., todos relacionados entre si) y mas importante, no es como el
    interprete se usa de verdad en produccion. Instanciarlo desde un
    archivo real, aunque sea minimo, es la unica forma honesta de decir
    'esto es un Interprete real, tal cual lo ve un usuario'."""
    import tempfile
    tmp = tempfile.NamedTemporaryFile("w", suffix=".sipi", delete=False, encoding="utf-8")
    tmp.write('programa "vacio"\n')
    tmp.close()
    return sipi.Interprete(tmp.name)


class TestLexer(unittest.TestCase):
    def test_numeros_enteros_y_decimales(self):
        tokens = tokenizar("42 3.14")
        self.assertEqual([t.valor for t in tokens[:-1]], [42, 3.14])
        self.assertEqual(tokens[0].tipo, TipoToken.NUMERO)

    def test_texto_con_escapes(self):
        tokens = tokenizar(r'"hola\nmundo" "tab\tfin"')
        self.assertEqual(tokens[0].valor, "hola\nmundo")
        self.assertEqual(tokens[1].valor, "tab\tfin")

    def test_texto_sin_cerrar_da_error_con_columna(self):
        with self.assertRaises(ErrorLexico) as ctx:
            tokenizar('decir "sin cerrar')
        self.assertEqual(ctx.exception.columna, 6)  # posicion de la comilla de apertura

    def test_identificadores_y_alias_logicos_en_espanol(self):
        tokens = tokenizar("x y verdadero")
        tipos_valores = [(t.tipo, t.valor) for t in tokens[:-1]]
        self.assertEqual(tipos_valores, [
            (TipoToken.IDENTIFICADOR, "x"),
            (TipoToken.OPERADOR, "and"),  # 'y' se traduce a 'and' en el lexer
            (TipoToken.IDENTIFICADOR, "verdadero"),
        ])

    def test_operadores_de_dos_caracteres_no_se_confunden_con_uno(self):
        tokens = tokenizar("a >= b == c")
        operadores = [t.valor for t in tokens if t.tipo == TipoToken.OPERADOR]
        self.assertEqual(operadores, [">=", "=="])

    def test_caracter_desconocido_da_error_con_columna_exacta(self):
        with self.assertRaises(ErrorLexico) as ctx:
            tokenizar("variable x = 5 @ 2")
            # nota: '=' no esta soportado por este tokenizador (es de
            # asignacion de sentencia, no de expresion), asi que primero
            # explota ahi -- se prueba aparte con solo la expresion:
        with self.assertRaises(ErrorLexico) as ctx2:
            tokenizar("5 @ 2")
        self.assertEqual(ctx2.exception.columna, 2)

    def test_siempre_termina_en_eof(self):
        tokens = tokenizar("1 + 1")
        self.assertEqual(tokens[-1].tipo, TipoToken.EOF)


class TestParserYPrecedencia(unittest.TestCase):
    def test_precedencia_multiplicacion_sobre_suma(self):
        nodo = parsear("2 + 3 * 4")
        self.assertIsInstance(nodo, Binario)
        self.assertEqual(nodo.operador, "+")
        self.assertIsInstance(nodo.izquierda, NumeroLiteral)
        self.assertIsInstance(nodo.derecha, Binario)
        self.assertEqual(nodo.derecha.operador, "*")

    def test_parentesis_cambian_la_precedencia(self):
        nodo = parsear("(2 + 3) * 4")
        self.assertEqual(nodo.operador, "*")
        self.assertIsInstance(nodo.izquierda, Binario)
        self.assertEqual(nodo.izquierda.operador, "+")

    def test_unario_encadenado(self):
        nodo = parsear("- - 5")
        self.assertIsInstance(nodo, Unario)
        self.assertIsInstance(nodo.operando, Unario)

    def test_expresion_incompleta_da_error_sintactico(self):
        with self.assertRaises(ErrorSintactico):
            parsear("2 + ")

    def test_parentesis_sin_cerrar_da_error_sintactico(self):
        with self.assertRaises(ErrorSintactico):
            parsear("(2 + 3")


class TestEvaluador(unittest.TestCase):
    def test_aritmetica_basica(self):
        self.assertEqual(evaluar_texto("2 + 3 * 4"), 14)
        self.assertEqual(evaluar_texto("(2 + 3) * 4"), 20)
        self.assertEqual(evaluar_texto("10 / 4"), 2.5)
        self.assertEqual(evaluar_texto("10 % 3"), 1)

    def test_division_por_cero_da_error_evaluacion(self):
        with self.assertRaises(ErrorEvaluacion):
            evaluar_texto("5 / 0")

    def test_comparaciones(self):
        self.assertTrue(evaluar_texto("5 > 3"))
        self.assertFalse(evaluar_texto("5 < 3"))
        self.assertTrue(evaluar_texto("5 == 5"))
        self.assertTrue(evaluar_texto("5 != 3"))

    def test_logicos_con_cortocircuito(self):
        contador = {"llamadas": 0}

        def efecto():
            contador["llamadas"] += 1
            return True

        # 'or' con izquierda verdadera: la derecha (la llamada) NO deberia evaluarse
        resultado = evaluar_texto("verdadero or efecto()", funciones={"efecto": efecto})
        self.assertTrue(resultado)
        self.assertEqual(contador["llamadas"], 0)

    def test_variables(self):
        # Nota: 'y' y 'o' no sirven como nombre de variable en este lexer
        # porque son alias de 'and'/'or' (misma ambiguedad de fondo que
        # cualquier lenguaje con palabras clave en dos idiomas a la vez);
        # se usan nombres sin ese choque a proposito.
        self.assertEqual(evaluar_texto("x + b", variables={"x": 10, "b": 5}), 15)

    def test_variable_no_declarada_da_error_evaluacion(self):
        with self.assertRaises(ErrorEvaluacion):
            evaluar_texto("no_existe + 1")

    def test_concatenacion_de_texto(self):
        self.assertEqual(evaluar_texto('"hola " + nombre', variables={"nombre": "Mateo"}), "hola Mateo")

    def test_llamada_a_funcion(self):
        self.assertEqual(evaluar_texto("doble(21)", funciones={"doble": lambda x: x * 2}), 42)

    def test_negacion_logica_con_alias_espanol(self):
        self.assertEqual(evaluar_texto("no verdadero"), False)

    def test_limitacion_conocida_y_o_no_chocan_con_nombres_de_variable(self):
        # Documentado a proposito, no escondido: como 'y'/'o'/'no' son
        # alias de 'and'/'or'/'not' a nivel de LEXER (no de parser), un
        # programa que declare una variable literalmente llamada 'y' (por
        # ejemplo, una coordenada) no la va a poder usar como variable en
        # una expresion con este AST nuevo -- el lexer ya la convirtio en
        # operador antes de que el parser sepa que en este contexto es un
        # nombre. Resolver esto de verdad necesitaria desambiguacion
        # sensible al contexto, fuera del alcance de esta primera fase.
        # IMPORTANTE: verificado que el interprete de PRODUCCION (sipi.py)
        # no tiene esta limitacion -- 'variable y = 5 \n decir y + 1'
        # corre bien ahi. Es una diferencia real y pendiente entre esta
        # pieza nueva y el motor actual, no algo para asumir resuelto.
        with self.assertRaises(ErrorSintactico):
            evaluar_texto("y + 1", variables={"y": 5})


class TestCruzadoContraElInterpreteReal(unittest.TestCase):
    """El test mas importante de este archivo: confirma que el AST nuevo
    no es solo 'consistente consigo mismo', sino que da EXACTAMENTE los
    mismos resultados que 'Interprete.evaluar_expresion' del motor real
    para el mismo conjunto de expresiones."""

    EXPRESIONES_ARITMETICAS = [
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "10 - 4 / 2",
        "7 % 3",
        "5 > 3",
        "5 == 5",
        "5 != 3",
        "3 < 5",
    ]

    def test_coincide_con_evaluar_expresion_del_motor_real(self):
        interprete = _interprete_vacio()
        for expresion in self.EXPRESIONES_ARITMETICAS:
            with self.subTest(expresion=expresion):
                esperado = interprete.evaluar_expresion(expresion)
                obtenido = evaluar_texto(expresion)
                self.assertEqual(obtenido, esperado,
                                  f"'{expresion}': AST nuevo dio {obtenido!r}, motor real dio {esperado!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
