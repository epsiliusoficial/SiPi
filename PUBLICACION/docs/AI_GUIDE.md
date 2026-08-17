# AI_GUIDE — Guía para asistentes de IA (ChatGPT, Claude, etc.)

Este documento está escrito para que un modelo de lenguaje lea SiPi y genere código correcto en el primer intento, sin necesitar ver el intérprete. Si sos un asistente de IA leyendo este archivo porque un usuario pidió código SiPi: leé este documento entero antes de escribir código, y preferí `FUNCTIONS.md`/`SYNTAX.md`/`LANGUAGE_SPEC.md` como fuente de verdad si hay conflicto.

## Qué es SiPi, en una frase

Un lenguaje interpretado, con palabras clave en español, para lógica general, GUI de escritorio, juegos 2D y páginas web — pensado para principiantes, con tipado dinámico y anotaciones de tipo opcionales.

## Reglas duras (no romper nunca)

1. **Todo archivo empieza con** `programa "Nombre"` como primera línea.
2. **Todo bloque que abre debe cerrar con `fin`** (o, alternativamente, con indentación consistente sin `fin` — pero no mezclar ambos estilos dentro del *mismo* bloque). Ante la duda, usá siempre `fin` explícito: es más seguro y es el estilo usado en el 100% de los ejemplos oficiales.
3. **Los strings van con comillas dobles** `"..."`. Nunca uses `\"` para escapar comillas dentro de un string — no funciona. Si necesitás una comilla dentro de un texto, usá comillas simples `'` para ese fragmento.
4. **La interpolación de variables es `{variable}` dentro de un string con `decir`** u otros comandos de texto, no f-strings de Python ni `${}`.
5. **Los comandos que devuelven un valor lo hacen con `-> variable`**, no con `=`. Ejemplo correcto: `lista_longitud mi_lista -> total`. Incorrecto: `total = lista_longitud(mi_lista)`.
6. **No inventes comandos.** Si necesitás una operación que no está en `FUNCTIONS.md`, resolvela combinando los comandos existentes (variables, condicionales, bucles, funciones) en vez de inventar un nombre de comando que suene plausible. SiPi no tiene una librería estándar tan grande como Python: muchas cosas hay que armarlas a mano con lo básico.
7. **`sumar`/`restar` son para modificar una variable existente**, no para sumar dos valores nuevos (para eso usá `+` directamente en una expresión).
8. **Dentro de una `clase`, el objeto propio se llama `este`**, no `self` ni `this`.
9. **Los comentarios son `//` (línea) y `/* */` (bloque)**, igual que en C/JS, no `#` como en Python.

## Plantilla mínima que siempre compila

Cuando no estés seguro de qué generar, esta plantilla es un punto de partida seguro:

```sipi
programa "Nombre del programa"

variable x = 0
decir "Programa iniciado"

funcion hacer_algo(param)
    decir "Parametro recibido: {param}"
fin

llamar hacer_algo("prueba")
```

## Checklist antes de entregar código SiPi

- [ ] ¿Empieza con `programa "..."`?
- [ ] ¿Cada bloque abierto (`si`, `funcion`, `mientras`, `clase`, `ventana`, `crear_juego`, etc.) tiene su `fin`?
- [ ] ¿Todos los comandos usados existen en `FUNCTIONS.md`? (si no estás seguro, elegí una alternativa más básica y verificada)
- [ ] ¿Los strings usan comillas dobles y `{variable}` para interpolar, sin `\"` interno?
- [ ] ¿Los comandos que calculan algo usan `-> variable`, no `=`?
- [ ] Si hay una `clase`, ¿usa `este` para referirse al objeto?
- [ ] Si hay tipos anotados (`variable x: entero`), ¿son consistentes con el valor asignado?

## Errores comunes que un modelo de lenguaje comete al "adivinar" SiPi

| Error típico (mal) | Correcto |
|---|---|
| `total = suma_lista(numeros)` | `suma_lista numeros -> total` |
| `print(f"Hola {nombre}")` | `decir "Hola {nombre}"` |
| `def funcion(x):` | `funcion nombre(x) ... fin` |
| `for item in lista:` | `para_cada item en lista ... fin` |
| `self.campo = valor` | `diccionario_asignar este "campo" valor` (dentro de un método) |
| `# comentario` | `// comentario` |
| Mezclar `fin` e indentación en el mismo bloque | Elegir un solo estilo por bloque, `fin` por defecto |
| Usar `try/except` | `intentar ... capturar ... fin` (la variable de error se llama `error`) |

## Cuándo pedir contexto en vez de adivinar

Los bloques `ventana`, `crear_juego` y `pagina_web` tienen mini-lenguajes internos con muchos parámetros específicos (opciones de `sprite`, de `tarjeta`, de `boton`, etc.) que no están 100% formalizados fuera del código fuente. Si el pedido usa alguno de estos bloques con una funcionalidad no cubierta claramente en `FUNCTIONS.md` o en un ejemplo de `EXAMPLES.md`, la respuesta más confiable es basarse en el ejemplo más parecido de `ejemplos/` y adaptarlo, en vez de inventar parámetros nuevos.

## Dónde mirar para más detalle

- Sintaxis básica y patrones: `SYNTAX.md`
- Lista completa de comandos por categoría: `FUNCTIONS.md`
- Reglas formales de tipos, bloques y POO: `LANGUAGE_SPEC.md`
- Código real funcionando, organizado por tema: `EXAMPLES.md` + carpeta `ejemplos/`
- Prompts ya armados para pedir código SiPi: `PROMPTS.md`
