# Referencia rápida de SiPi para Claude

SiPi ya tiene documentación de referencia completa en `docs/`. Este archivo
no la duplica -- señala qué leer según la necesidad, más lo mínimo
indispensable para arrancar sin abrir nada.

## Lectura según necesidad (de más a menos frecuente)

- **`docs/SYNTAX.md`** (151 líneas) -- referencia rápida de sintaxis:
  bloques, variables, condicionales, bucles, funciones, listas,
  diccionarios, manejo de errores, clases. **Leer esto primero** si hace
  falta refrescar sintaxis puntual.
- **`docs/FUNCTIONS.md`** -- catálogo de funciones/comandos built-in
  (matemáticas, texto, listas, archivos, bases de datos, web, GUI,
  juegos, seguridad, estadística, fechas). Consultar cuando se necesite
  un comando puntual que no se recuerda exacto.
- **`docs/LANGUAGE_SPEC.md`** -- especificación formal completa. Consultar
  solo para casos borde de precedencia/gramática, no para uso normal.
- **`docs/EXAMPLES.md`** y `examples/` (47 programas reales, 10 categorías)
  -- ejemplos completos y funcionando para copiar estructura.

## Lo mínimo para arrancar sin abrir nada

```sipi
programa "Nombre del programa"

variable x = 10                    // sin tipo
variable y: entero = 20            // con tipo (opcional)
const MI_CONSTANTE = 3.14159

decir "Texto con {x} interpolado"
variable y_respuesta = preguntar "Pregunta: "

si x > 5
    decir "mayor"
sino
    decir "menor"
fin

repetir 5 veces
    decir "hola"
fin

mientras x > 0
    variable x = x - 1
fin

variable milista = [1, 2, 3]
para_cada elemento en milista
    decir elemento
fin

funcion sumar(a, b)
    devolver a + b
fin

decir "Suma: {sumar(2, 3)}"

intentar
    // ...
capturar error
    decir "Error: {error}"
fin

clase Animal
    nombre = ""
fin

clase Perro hereda_de Animal
    metodo hacer_sonido()
        devolver "Guau!"
    fin
fin

nuevo Perro() -> rex
llamar_metodo rex "hacer_sonido"() -> sonido
decir "El perro dice: {sonido}"
```

Bloques abren con la palabra clave y cierran con **`fin` a secas** (NO
`fin si`, NO `fin funcion`, NO `fin repetir` -- esas formas con palabra
extra NO son válidas, el motor solo reconoce `fin` solo) -- o, alternativa,
solo con indentación consistente sin ningún `fin`. Las dos formas son
válidas y mezclables en el mismo archivo, pero nunca `fin <palabra>`.
**`si` NO lleva `entonces`** (`si x > 5` directo, sin conector). **`mientras`
NO lleva `hace`** (`mientras x > 0` directo). Estos son errores fáciles de
cometer por analogía con otros lenguajes/pseudocódigo en español -- SiPi
específicamente no los usa. **Asignación de resultado de un comando: `comando
argumentos -> variable`** (no `variable = comando(...)`) para los comandos
built-in que devuelven un valor (`nuevo`, `llamar_metodo`, `azar_entre`,
`leer_archivo`, `json_leer`, `diccionario_crear`, etc.) -- `devolver` dentro
de una función sí usa el valor directo, sin flecha.

## Comandos frecuentes que no siempre se recuerdan exactos

Fragmentos ilustrativos (no pensados para correr tal cual, `condicion` y
`funcion` son placeholders) -- mostrando la forma exacta de cada llamado:

```sipi
variable milista = [1, 2, 3]
variable valor = 4

lista_agregar milista valor
lista_ordenar milista
crear_archivo "ruta.txt" "contenido"
leer_archivo "ruta.txt" -> contenido
diccionario_crear -> dic
diccionario_asignar dic "clave" valor
azar_entre 1 10 -> numero

seleccionar valor
    caso 1
        decir "es uno"
    otro
        decir "otro caso"
fin
```

El motor tiene ~170 comandos en total (GUI con `ventana`/`boton`/...,
juegos con `crear_juego`/`sprite`/..., web con `iniciar_servidor_web`/...,
bases de datos con `sqlite_*`/`postgres_*`/..., seguridad con `hash_*`/...)
-- ninguno hace falta memorizar, `docs/FUNCTIONS.md` los tiene todos
categorizados.

## Directivas útiles al principio del archivo

```sipi
#idioma es        // (default) palabras clave en español
#idioma en         // palabras clave en inglés
#idioma ambos      // acepta ambos en el mismo archivo
#nivel principiante // mensajes de error mas simples (para SiPi Kids)
```
