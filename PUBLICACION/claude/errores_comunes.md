# Errores que Claude ya cometió antes escribiendo SiPi

Este archivo existe por una razón concreta: en sesiones anteriores,
Claude generó SiPi con sintaxis inventada (parecida a otros lenguajes,
pero que el motor real no entiende) de forma sistemática, durante
mucho tiempo, antes de que se detectara y corrigiera. Cada entrada acá
es un error real que pasó, verificado contra el motor, no una
advertencia teórica.

**Antes de escribir SiPi, leer esta lista una vez.** Cuesta pocos
tokens y evita el patrón más caro que existe: escribir 200 líneas con
un error sistemático repetido en cada bloque, y tener que reescribir
todo.

## 1. Cierre de bloques: SIEMPRE `fin`, nunca `fin si` / `fin funcion` / etc.

❌ Incorrecto (inventado, mezcla con otros lenguajes):
```
si condicion
    decir "hola"
fin si
```

✅ Correcto:
```
si condicion
    decir "hola"
fin
```

`fin` cierra CUALQUIER bloque abierto (si, funcion, clase, repetir,
mientras, para_cada, intentar, etc.) -- no lleva la palabra del bloque
que cierra. Esto vale para absolutamente todos los bloques del
lenguaje, sin excepción.

## 2. `si` no lleva `entonces`

❌ Incorrecto:
```
si edad >= 18 entonces
    decir "mayor"
fin
```

✅ Correcto:
```
si edad >= 18
    decir "mayor"
fin
```

## 3. `para_cada` es UNA palabra con guion bajo, no dos palabras

❌ Incorrecto: `para cada elemento en lista`
✅ Correcto: `para_cada elemento en lista`

## 4. `azar_entre` es una sentencia con flecha, no una función que se llama

❌ Incorrecto (estilo función, como en Python):
```
variable n = azar_entre(1, 10)
```

✅ Correcto (sentencia propia, con `->` para guardar el resultado):
```
azar_entre 1 10 -> n
```

## 5. Repetir: `repetir N veces`, no `repetir(N)` ni `para i en rango(N)`

❌ Incorrecto: `repetir(5)` / `para i en rango(5)`
✅ Correcto:
```
repetir 5 veces
    decir "hola"
fin
```

## 6. No hay `entonces`/`then`/`do` en ningún lado del lenguaje

Si en algún momento parece natural escribir una palabra de enlace tipo
"then"/"do"/"entonces" copiando la sensación de otro lenguaje (Lua,
Ruby, BASIC), es casi seguro que SiPi no la usa. La lista completa de
palabras clave reales está en `referencia_rapida.md` y
`docs/LANGUAGE_SPEC.md` -- si una palabra no aparece ahí, no existe.

## 7. Comentarios: `//`, no `#` (excepto la directiva de nivel)

❌ Incorrecto: `# esto es un comentario`
✅ Correcto: `// esto es un comentario`

La única excepción real es la directiva `#nivel principiante` /
`#nivel intermedio` / `#nivel avanzado`, que sí usa `#` porque es una
directiva del motor, no un comentario.

## 8. No hay `import`/`from ... import` entre archivos `.sipi`

SiPi no tiene un sistema de módulos con `import` entre archivos `.sipi`
todavía. Un proyecto de varios archivos se organiza por convención de
carpeta (ver `proyecto.py` en esta misma carpeta), no importando
funciones de un archivo a otro en tiempo de ejecución. Si la tarea
"necesita" import, la solución real es: escribir todo el programa en
el archivo que se va a ejecutar, o usar los patrones de
`patrones/proyecto_cli.sipi` como referencia de organización.

## Cómo se corrigió esto la vez pasada (y cómo evitar que vuelva a pasar)

Cada patrón en `patrones/*.sipi` fue **ejecutado de verdad** contra
`sipi.py` antes de guardarse acá -- no son ejemplos "de memoria". Si
hace falta escribir algo que no está cubierto por ningún patrón
existente, el flujo correcto es:

1. Escribir el programa.
2. Correr `python3 claude/verificar.py archivo.sipi` ANTES de darlo
   por terminado (un solo tool-call, ver `SKILL.md`).
3. Si el error es de sintaxis rara ("no se esperaba X", "token
   inesperado"), es casi siempre uno de los patrones de esta lista --
   revisar acá antes de adivinar una segunda vez.
