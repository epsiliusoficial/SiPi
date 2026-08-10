# runtime_rust — Prototipo de runtime alternativo (item #70 del feedback)

## Que es esto

Un primer paso real y compilable hacia lo que el feedback describe como
"runtime alternativo" — la idea de que SiPi pueda tener distintas
implementaciones de ejecucion (Python, y eventualmente Rust) compartiendo
el mismo lenguaje y el mismo AST, sin que eso signifique crear "SiPi 2"
ni un lenguaje distinto.

## Que hace de verdad

Tokeniza y evalua **expresiones** de SiPi (aritmetica, comparaciones,
logica, texto, variables) — el mismo subconjunto que `lexer_sipi.py` /
`ast_sipi.py` en Python (carpeta padre), con la MISMA semantica.

```bash
cargo build
./target/debug/sipi_runtime_rust "2 + 3 * 4"     # -> 14
./target/debug/sipi_runtime_rust "(2 + 3) * 4"   # -> 20
```

## Que NO hace (todavia)

No ejecuta programas SiPi completos: sin `si`/`sino`/`fin`, sin
`funcion`, sin bucles, sin listas/diccionarios, sin ninguno de los ~170
comandos del motor real. Es deliberadamente solo expresiones — la pieza
mas chica y mas facil de verificar con certeza antes de escalar a algo
mas grande.

## Como se verifico

`cargo test` corre 17 tests unitarios en Rust (lexer + parser +
evaluador). Ademas, `tests/test_paridad_rust.py` (en la raiz del
proyecto, corre con `python3 tests/test_paridad_rust.py`) compara este
binario contra `ast_sipi.py` (Python) **y** contra
`Interprete.evaluar_expresion` del motor de produccion real
(`sipi.py`) para el mismo lote de expresiones, confirmando que las tres
implementaciones dan resultados identicos — no solo "deberian
coincidir", sino coinciden, verificado en cada corrida de la suite de
tests.

## Proximos pasos (no hechos todavia, para no prometer de mas)

1. Sentencias simples (`variable`, `decir`) sobre el mismo AST.
2. Control de flujo (`si`/`mientras`/`repetir`).
3. Funciones y llamadas reales (mas alla de una sola expresion).
4. Recien despues de eso tendria sentido evaluar seriamente si conviene
   compilar `.sipi` a este runtime como alternativa de rendimiento al
   interprete de Python, que es la motivacion original del item #70.
