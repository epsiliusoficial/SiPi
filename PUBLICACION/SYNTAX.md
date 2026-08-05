# SYNTAX — Referencia rápida de sintaxis de SiPi

Guía de consulta rápida. Para la explicación completa con ejemplos progresivos, ver `DOCUMENTACION.md` (sección "Tutorial desde cero"). Para el detalle formal, ver `LANGUAGE_SPEC.md`.

## Estructura mínima

```sipi
programa "Nombre"
decir "Hola, mundo!"
```

Toda anotación de tipo, en variables, listas, diccionarios o funciones, es **opcional**: podés escribir SiPi sin tipos y agregarlos después a medida que el proyecto crece.

## Bloques

Se cierran con `fin`, o con indentación consistente (sin `fin`) — mezclables libremente en el mismo archivo:

```sipi
si edad >= 18
    decir "Mayor de edad"
sino
    decir "Menor de edad"
fin
```

Abren bloque: `si`/`sino`, `mientras`, `repetir N veces`, `funcion`, `para_cada`, `intentar`/`capturar`, `enum`, `estructura`, `clase`, `interfaz`, `ventana`, `crear_juego`, `pagina_web`, `formulario`, `pestanias`/`pestana`, `cada N segundos`, `seleccionar`/`caso`.

## Comentarios

```sipi
// comentario de una línea
/* comentario
   de varias líneas */
```

## Variables y constantes

```sipi
variable nombre = "Mateo"
variable edad: entero = 20
const PI = 3.1416
sumar edad 1
restar edad 1
```

## Texto e interpolación

```sipi
decir "Hola {nombre}, tenés {edad} años"
```
No se puede escapar `"` con `\"` dentro de un string; para texto con comillas, usar `'` en ese fragmento.

## Condicionales

```sipi
si condicion
    ...
sino
    ...
fin
```

## Pattern matching

```sipi
seleccionar valor
    caso 1
        decir "uno"
    caso 2
        decir "dos"
    otro
        decir "otro valor"
fin
```

## Bucles

```sipi
mientras condicion
    ...
fin

repetir 5 veces
    ...
fin

para_cada item en lista
    ...
fin
```
`romper` corta el bucle actual, `continuar` salta a la siguiente iteración.

## Funciones

```sipi
funcion suma(a: entero, b: entero) -> entero
    devolver a + b
fin

llamar_valor suma(2, 3) -> resultado
llamar imprimir_algo()   // sin usar el resultado
```
Las llamadas a función se pueden anidar dentro de expresiones: `suma_uno(doble(3))`.

## Manejo de errores

```sipi
intentar
    lanzar_error "mensaje de error"
capturar
    decir "Error: {error}"
fin
```

## Clases

```sipi
clase Animal
    campo nombre = ""
    metodo hacer_sonido()
        decir "..."
    fin
fin

clase Perro hereda_de Animal implementa PuedeCorrer
    metodo hacer_sonido()
        decir "Guau"
    fin
fin

nuevo Perro() -> p
llamar_metodo p "hacer_sonido"()
es_instancia_de p Animal -> var
```

## Asignación de resultado con `->`

Patrón general de comandos que producen un valor:

```sipi
comando argumentos -> variable
lista_mapear numeros con doble -> dobles
sqlite_consultar db "SELECT * FROM tabla" en filas
```

## Errores con sugerencias

Si escribís mal un comando, SiPi sugiere el correcto:
```
Comando desconocido: 'imprimr'. ¿Quisiste decir 'imprimir'?
```
