#!/usr/bin/env python3
"""
tests/test_paridad_rust.py - Validacion cruzada de TRES vias (item #70
del feedback, prototipo de runtime en Rust): compara el binario Rust
('runtime_rust'), el AST nuevo en Python ('ast_sipi.py', fase 1 de los
items #23-25) y el motor de produccion real ('sipi.py') para el MISMO
conjunto de expresiones, confirmando que las tres implementaciones dan
resultados identicos.

Se salta automaticamente (no falla) si el binario de Rust no esta
compilado en esta maquina -- 'cargo build' en runtime_rust/ lo genera.
"""
import importlib
import os
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

import ast_sipi

sipi = importlib.import_module("sipi")

BINARIO_RUST = os.path.join(RAIZ, "runtime_rust", "target", "debug", "sipi_runtime_rust")


def _interprete_real():
    tmp = tempfile.NamedTemporaryFile("w", suffix=".sipi", delete=False, encoding="utf-8")
    tmp.write('programa "vacio"\n')
    tmp.close()
    return sipi.Interprete(tmp.name)


def _normalizar_para_comparar(valor_python):
    """El motor real de Python devuelve True/False/8.0; el binario de
    Rust imprime 'verdadero'/'falso'/'8' -- se normaliza al formato de
    texto de Rust para poder comparar como texto, sin asumir que ambos
    representan internamente los numeros de la misma forma (uno usa
    float de Python, el otro f64 de Rust)."""
    if valor_python is True:
        return "verdadero"
    if valor_python is False:
        return "falso"
    if isinstance(valor_python, float) and valor_python == int(valor_python):
        return str(int(valor_python))
    return str(valor_python)


EXPRESIONES = [
    "2 + 3 * 4", "(2 + 3) * 4", "10 - 4 / 2", "7 % 3",
    "5 > 3", "5 == 5", "5 != 3", "3 < 5", "10 / 4",
]


@unittest.skipUnless(os.path.exists(BINARIO_RUST),
                      "Binario de Rust no compilado -- correr 'cargo build' en runtime_rust/")
class TestParidadRustPythonMotorReal(unittest.TestCase):
    def test_las_tres_implementaciones_coinciden(self):
        interprete = _interprete_real()
        for expresion in EXPRESIONES:
            with self.subTest(expresion=expresion):
                esperado_motor_real = _normalizar_para_comparar(interprete.evaluar_expresion(expresion))
                esperado_ast_python = _normalizar_para_comparar(ast_sipi.evaluar_texto(expresion))
                resultado = subprocess.run([BINARIO_RUST, expresion], capture_output=True, text=True, timeout=5)
                obtenido_rust = resultado.stdout.strip()
                self.assertEqual(obtenido_rust, esperado_motor_real,
                                  f"'{expresion}': Rust dio '{obtenido_rust}', motor real dio '{esperado_motor_real}'")
                self.assertEqual(esperado_ast_python, esperado_motor_real,
                                  f"'{expresion}': AST Python dio '{esperado_ast_python}', motor real dio '{esperado_motor_real}'")

    def test_division_por_cero_da_error_en_rust_tambien(self):
        resultado = subprocess.run([BINARIO_RUST, "5", "/", "0"], capture_output=True, text=True, timeout=5)
        self.assertNotEqual(resultado.returncode, 0)
        self.assertIn("Division por cero", resultado.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
