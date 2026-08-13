#!/usr/bin/env python3
"""
ast_sipi.py - Parser y AST reales de SiPi (continuacion de lexer_sipi.py,
items #23-25 del feedback).

Igual que lexer_sipi.py: esto NO reemplaza al interprete de produccion
(sipi.py) todavia -- es la base formal para hacerlo gradualmente en
sesiones futuras. Ver la nota grande al principio de lexer_sipi.py para
el porque de este alcance.

Gramatica implementada (precedencia de menor a mayor, tipica de
lenguajes con operadores infijos):

    expresion   := logico_or
    logico_or   := logico_and (('or') logico_and)*
    logico_and  := igualdad (('and') igualdad)*
    igualdad    := comparacion (('==' | '!=') comparacion)*
    comparacion := suma (('<' | '<=' | '>' | '>=') suma)*
    suma        := termino (('+' | '-') termino)*
    termino     := unario (('*' | '/' | '%') unario)*
    unario      := ('not' | '-' | '+') unario | llamada
    llamada     := primario ('(' argumentos? ')')*
    primario    := NUMERO | TEXTO | 'verdadero' | 'falso' | 'nulo'
                 | IDENTIFICADOR | '(' expresion ')'
"""
from dataclasses import dataclass, field

from lexer_sipi import tokenizar, TipoToken, ErrorLexico


# --------------------------------------------------------------------------
# Nodos del AST. Dataclasses simples: el arbol es solo datos, toda la
# logica de "que hacer con esto" vive aparte (en 'evaluar' de mas abajo),
# igual que en cualquier separacion lexer/parser/AST/runtime real -- el
# AST no sabe nada de como se ejecuta.
# --------------------------------------------------------------------------

@dataclass
class NumeroLiteral:
    valor: float


@dataclass
class TextoLiteral:
    valor: str


@dataclass
class BooleanoLiteral:
    valor: bool


@dataclass
class NuloLiteral:
    pass


@dataclass
class Variable:
    nombre: str


@dataclass
class Unario:
    operador: str
    operando: object


@dataclass
class Binario:
    izquierda: object
    operador: str
    derecha: object


@dataclass
class Llamada:
    nombre: str
    argumentos: list = field(default_factory=list)


class ErrorSintactico(Exception):
    def __init__(self, mensaje, columna):
        super().__init__(mensaje)
        self.columna = columna


class Parser:
    """Recursive-descent / precedence-climbing clasico. Cada metodo de
    'nivel de precedencia' llama al de precedencia inmediatamente mayor
    para sus operandos, lo que hace que el arbol resultante ya respete la
    precedencia sin necesitar ningun paso de reordenamiento posterior."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _actual(self):
        return self.tokens[self.pos]

    def _avanzar(self):
        token = self.tokens[self.pos]
        if token.tipo != TipoToken.EOF:
            self.pos += 1
        return token

    def _coincide_operador(self, *operadores):
        token = self._actual()
        return token.tipo == TipoToken.OPERADOR and token.valor in operadores

    def parsear_expresion(self):
        nodo = self._logico_or()
        if self._actual().tipo != TipoToken.EOF:
            raise ErrorSintactico(
                f"Se esperaba el final de la expresion, se encontro '{self._actual().valor}'",
                self._actual().columna,
            )
        return nodo

    def _logico_or(self):
        nodo = self._logico_and()
        while self._coincide_operador("or"):
            operador = self._avanzar().valor
            nodo = Binario(nodo, operador, self._logico_and())
        return nodo

    def _logico_and(self):
        nodo = self._igualdad()
        while self._coincide_operador("and"):
            operador = self._avanzar().valor
            nodo = Binario(nodo, operador, self._igualdad())
        return nodo

    def _igualdad(self):
        nodo = self._comparacion()
        while self._coincide_operador("==", "!="):
            operador = self._avanzar().valor
            nodo = Binario(nodo, operador, self._comparacion())
        return nodo

    def _comparacion(self):
        nodo = self._suma()
        while self._coincide_operador("<", "<=", ">", ">="):
            operador = self._avanzar().valor
            nodo = Binario(nodo, operador, self._suma())
        return nodo

    def _suma(self):
        nodo = self._termino()
        while self._coincide_operador("+", "-"):
            operador = self._avanzar().valor
            nodo = Binario(nodo, operador, self._termino())
        return nodo

    def _termino(self):
        nodo = self._unario()
        while self._coincide_operador("*", "/", "%"):
            operador = self._avanzar().valor
            nodo = Binario(nodo, operador, self._unario())
        return nodo

    def _unario(self):
        if self._coincide_operador("not", "-", "+"):
            operador = self._avanzar().valor
            return Unario(operador, self._unario())
        return self._llamada()

    def _llamada(self):
        nodo = self._primario()
        while self._actual().tipo == TipoToken.PARENTESIS_ABRE:
            if not isinstance(nodo, Variable):
                raise ErrorSintactico("Solo se puede 'llamar' a un nombre de funcion", self._actual().columna)
            self._avanzar()  # '('
            argumentos = []
            if self._actual().tipo != TipoToken.PARENTESIS_CIERRA:
                argumentos.append(self._logico_or())
                while self._actual().tipo == TipoToken.COMA:
                    self._avanzar()
                    argumentos.append(self._logico_or())
            self._esperar(TipoToken.PARENTESIS_CIERRA, "Falta cerrar ')'")
            nodo = Llamada(nodo.nombre, argumentos)
        return nodo

    def _primario(self):
        token = self._actual()
        if token.tipo == TipoToken.NUMERO:
            self._avanzar()
            return NumeroLiteral(token.valor)
        if token.tipo == TipoToken.TEXTO:
            self._avanzar()
            return TextoLiteral(token.valor)
        if token.tipo == TipoToken.IDENTIFICADOR:
            self._avanzar()
            if token.valor == "verdadero":
                return BooleanoLiteral(True)
            if token.valor == "falso":
                return BooleanoLiteral(False)
            if token.valor == "nulo":
                return NuloLiteral()
            return Variable(token.valor)
        if token.tipo == TipoToken.PARENTESIS_ABRE:
            self._avanzar()
            nodo = self._logico_or()
            self._esperar(TipoToken.PARENTESIS_CIERRA, "Falta cerrar ')'")
            return nodo
        raise ErrorSintactico(f"Se esperaba un valor, se encontro '{token.valor}'", token.columna)

    def _esperar(self, tipo, mensaje_si_falta):
        if self._actual().tipo != tipo:
            raise ErrorSintactico(mensaje_si_falta, self._actual().columna)
        return self._avanzar()


def parsear(texto):
    """Atajo: tokeniza y parsea una expresion en un solo paso, devolviendo
    la raiz del AST."""
    return Parser(tokenizar(texto)).parsear_expresion()


class ErrorEvaluacion(Exception):
    pass


def evaluar(nodo, variables=None, funciones=None):
    """Recorre el AST y calcula su valor real. 'variables' es un dict
    nombre->valor; 'funciones' un dict nombre->callable, para poder
    evaluar 'Llamada' sin que este modulo sepa nada de los builtins de
    SiPi (los inyecta quien lo use)."""
    variables = variables or {}
    funciones = funciones or {}

    if isinstance(nodo, NumeroLiteral):
        return nodo.valor
    if isinstance(nodo, TextoLiteral):
        return nodo.valor
    if isinstance(nodo, BooleanoLiteral):
        return nodo.valor
    if isinstance(nodo, NuloLiteral):
        return None
    if isinstance(nodo, Variable):
        if nodo.nombre not in variables:
            raise ErrorEvaluacion(f"Variable no declarada: '{nodo.nombre}'")
        return variables[nodo.nombre]
    if isinstance(nodo, Unario):
        valor = evaluar(nodo.operando, variables, funciones)
        if nodo.operador == "-":
            return -valor
        if nodo.operador == "+":
            return +valor
        if nodo.operador == "not":
            return not _es_verdadero(valor)
        raise ErrorEvaluacion(f"Operador unario desconocido: {nodo.operador}")
    if isinstance(nodo, Binario):
        return _evaluar_binario(nodo, variables, funciones)
    if isinstance(nodo, Llamada):
        if nodo.nombre not in funciones:
            raise ErrorEvaluacion(f"Funcion no reconocida: '{nodo.nombre}'")
        argumentos = [evaluar(a, variables, funciones) for a in nodo.argumentos]
        return funciones[nodo.nombre](*argumentos)
    raise ErrorEvaluacion(f"Tipo de nodo desconocido: {type(nodo).__name__}")


def _es_verdadero(valor):
    if isinstance(valor, bool):
        return valor
    if valor is None:
        return False
    if isinstance(valor, (int, float)):
        return valor != 0
    if isinstance(valor, str):
        return valor != ""
    return bool(valor)


def _evaluar_binario(nodo, variables, funciones):
    operador = nodo.operador
    # Cortocircuito real para 'and'/'or': el lado derecho ni se evalua si
    # ya no hace falta (importante si tiene efectos secundarios via una
    # llamada a funcion).
    if operador == "and":
        izq = evaluar(nodo.izquierda, variables, funciones)
        return izq if not _es_verdadero(izq) else evaluar(nodo.derecha, variables, funciones)
    if operador == "or":
        izq = evaluar(nodo.izquierda, variables, funciones)
        return izq if _es_verdadero(izq) else evaluar(nodo.derecha, variables, funciones)

    izq = evaluar(nodo.izquierda, variables, funciones)
    der = evaluar(nodo.derecha, variables, funciones)

    if operador == "+":
        # Concatenacion si cualquiera de los dos lados es texto (misma
        # convencion que ya usa el interprete de produccion).
        if isinstance(izq, str) or isinstance(der, str):
            return _texto(izq) + _texto(der)
        return izq + der
    if operador == "-":
        return izq - der
    if operador == "*":
        return izq * der
    if operador == "/":
        if der == 0:
            raise ErrorEvaluacion(f"Division por cero al evaluar la expresion '{izq} / {der}'.")
        return izq / der
    if operador == "%":
        if der == 0:
            raise ErrorEvaluacion(f"Division por cero al evaluar la expresion '{izq} % {der}'.")
        return izq % der
    if operador == "==":
        return izq == der
    if operador == "!=":
        return izq != der
    if operador == "<":
        return izq < der
    if operador == "<=":
        return izq <= der
    if operador == ">":
        return izq > der
    if operador == ">=":
        return izq >= der
    raise ErrorEvaluacion(f"Operador desconocido: {operador}")


def _texto(valor):
    if isinstance(valor, bool):
        return "verdadero" if valor else "falso"
    if valor is None:
        return "nulo"
    if isinstance(valor, float) and valor == int(valor):
        return str(int(valor))
    return str(valor)


def evaluar_texto(texto, variables=None, funciones=None):
    """Atajo de punta a punta: tokeniza, parsea y evalua una expresion en
    un solo llamado."""
    return evaluar(parsear(texto), variables, funciones)
