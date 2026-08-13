#!/usr/bin/env python3
"""
lexer_sipi.py - Tokenizador real de SiPi (items #23-25 del feedback:
"Separar claramente: Codigo -> Lexer -> Parser -> AST -> Runtime").

IMPORTANTE - alcance de esta primera fase: el interprete de produccion
(sipi.py) sigue funcionando exactamente igual que siempre, linea por
linea, sin usar nada de este archivo -- no se toco ni una linea de
sipi.py para esto. Reescribir TODO el runtime para que use un
lexer/parser/AST formal es un proyecto en si mismo, demasiado grande y
riesgoso para meter a ciegas de una sola vez sobre un interprete de mas
de 9000 lineas que ya funciona bien y tiene gente usandolo. Este archivo
(junto con ast_sipi.py) es la base real y funcional de esa separacion,
construida y probada aparte, lista para que el runtime la empiece a usar
gradualmente en las proximas sesiones (por ejemplo: primero para dar
errores con columna exacta -- item #26 -- despues para reemplazar el
evaluador de expresiones basado en eval(), y asi sucesivamente) en vez
de todo de una.

Cubre el subconjunto de SiPi mas importante para expresiones: numeros,
texto, identificadores/palabras clave, y los operadores aritmeticos,
de comparacion y logicos (incluyendo los alias en español 'y'/'o'/'no').
"""
from dataclasses import dataclass
from enum import Enum, auto


class TipoToken(Enum):
    NUMERO = auto()
    TEXTO = auto()
    IDENTIFICADOR = auto()
    OPERADOR = auto()
    PARENTESIS_ABRE = auto()
    PARENTESIS_CIERRA = auto()
    COMA = auto()
    EOF = auto()


@dataclass
class Token:
    tipo: TipoToken
    valor: object
    columna: int  # posicion (0-based) del PRIMER caracter del token en la linea original

    def __repr__(self):
        return f"Token({self.tipo.name}, {self.valor!r}, col={self.columna})"


class ErrorLexico(Exception):
    """Se guarda 'columna' para que un consumidor (el parser, o el
    formateador de errores del item #26) pueda apuntar exactamente al
    caracter problematico, no solo a la linea entera."""
    def __init__(self, mensaje, columna):
        super().__init__(mensaje)
        self.columna = columna


# Palabras que, aunque son identificadores validos por forma, son en
# realidad operadores logicos en español (alias de and/or/not).
_ALIAS_OPERADOR_LOGICO = {"y": "and", "o": "or", "no": "not"}

_OPERADORES_DOS_CARACTERES = {"==", "!=", "<=", ">="}
_OPERADORES_UN_CARACTER = set("+-*/%<>")

_ESCAPES = {"n": "\n", "t": "\t", '"': '"', "\\": "\\", "'": "'"}


def tokenizar(texto):
    """Convierte una linea de codigo SiPi en una lista de Token, terminada
    siempre en un Token EOF. Lanza ErrorLexico con la columna exacta si
    encuentra un caracter que no reconoce o una cadena sin cerrar."""
    tokens = []
    i = 0
    n = len(texto)
    while i < n:
        c = texto[i]

        if c in " \t":
            i += 1
            continue

        if c == '"':
            inicio = i
            i += 1
            piezas = []
            while i < n and texto[i] != '"':
                if texto[i] == "\\" and i + 1 < n:
                    siguiente = texto[i + 1]
                    piezas.append(_ESCAPES.get(siguiente, siguiente))
                    i += 2
                else:
                    piezas.append(texto[i])
                    i += 1
            if i >= n:
                raise ErrorLexico("Cadena de texto sin cerrar (falta la comilla final '\"')", inicio)
            i += 1  # consume la comilla de cierre
            tokens.append(Token(TipoToken.TEXTO, "".join(piezas), inicio))
            continue

        if c.isdigit() or (c == "." and i + 1 < n and texto[i + 1].isdigit()):
            inicio = i
            tiene_punto = False
            while i < n and (texto[i].isdigit() or (texto[i] == "." and not tiene_punto)):
                if texto[i] == ".":
                    tiene_punto = True
                i += 1
            crudo = texto[inicio:i]
            valor = float(crudo) if tiene_punto else int(crudo)
            tokens.append(Token(TipoToken.NUMERO, valor, inicio))
            continue

        if c.isalpha() or c == "_":
            inicio = i
            while i < n and (texto[i].isalnum() or texto[i] == "_"):
                i += 1
            palabra = texto[inicio:i]
            if palabra in _ALIAS_OPERADOR_LOGICO:
                tokens.append(Token(TipoToken.OPERADOR, _ALIAS_OPERADOR_LOGICO[palabra], inicio))
            elif palabra in ("and", "or", "not"):
                tokens.append(Token(TipoToken.OPERADOR, palabra, inicio))
            elif palabra in ("verdadero", "true"):
                tokens.append(Token(TipoToken.IDENTIFICADOR, "verdadero", inicio))
            elif palabra in ("falso", "false"):
                tokens.append(Token(TipoToken.IDENTIFICADOR, "falso", inicio))
            elif palabra in ("nulo", "null"):
                tokens.append(Token(TipoToken.IDENTIFICADOR, "nulo", inicio))
            else:
                tokens.append(Token(TipoToken.IDENTIFICADOR, palabra, inicio))
            continue

        if texto[i:i + 2] in _OPERADORES_DOS_CARACTERES:
            tokens.append(Token(TipoToken.OPERADOR, texto[i:i + 2], i))
            i += 2
            continue

        if c in _OPERADORES_UN_CARACTER:
            tokens.append(Token(TipoToken.OPERADOR, c, i))
            i += 1
            continue

        if c == "(":
            tokens.append(Token(TipoToken.PARENTESIS_ABRE, "(", i))
            i += 1
            continue

        if c == ")":
            tokens.append(Token(TipoToken.PARENTESIS_CIERRA, ")", i))
            i += 1
            continue

        if c == ",":
            tokens.append(Token(TipoToken.COMA, ",", i))
            i += 1
            continue

        raise ErrorLexico(f"Caracter inesperado: '{c}'", i)

    tokens.append(Token(TipoToken.EOF, None, n))
    return tokens
