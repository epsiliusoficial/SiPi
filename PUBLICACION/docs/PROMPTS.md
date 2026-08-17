# PROMPTS — Prompts listos para pedir código SiPi a una IA

Copiá y pegá estos prompts en ChatGPT, Claude o cualquier otro asistente, junto con los archivos de contexto que se indican (adjuntándolos o pegando su contenido). Cuantos más archivos de contexto le des, más preciso va a ser el código generado.

## Prompt base (recomendado para cualquier pedido)

```
Vas a escribir código en SiPi, un lenguaje de programación en español.
Antes de escribir nada, leé los archivos adjuntos AI_GUIDE.md, SYNTAX.md
y FUNCTIONS.md — son la referencia completa del lenguaje. No inventes
comandos que no aparezcan en FUNCTIONS.md. Todo bloque que abre (si,
funcion, mientras, clase, ventana, crear_juego, etc.) tiene que cerrar
con "fin". Los strings van entre comillas dobles y se interpolan con
{variable}, nunca con f-strings de Python.

Mi pedido:
[DESCRIBÍ ACÁ QUÉ QUERÉS QUE HAGA EL PROGRAMA]
```
**Adjuntar:** `AI_GUIDE.md`, `SYNTAX.md`, `FUNCTIONS.md`

## Para un programa básico (variables, lógica, funciones)

```
Escribí un programa en SiPi que [describir la lógica]. Usá solo los
comandos de la sección "Programa, variables y control de flujo" y
"Listas, diccionarios, matrices y programacion funcional" de
FUNCTIONS.md. Mostrá el resultado con "decir". Seguí exactamente el
estilo de ejemplos/hola_mundo.sipi.
```
**Adjuntar:** `FUNCTIONS.md`, `ejemplos/hola_mundo.sipi`

## Para una interfaz gráfica de escritorio

```
Escribí un programa en SiPi que abra una ventana con [describir los
elementos: botones, campos, listas, etc.] y que [describir el
comportamiento al interactuar]. Basate en la estructura del bloque
"ventana ... fin" que aparece en estos ejemplos adjuntos, y no inventes
parámetros de widgets que no veas usados en ellos.
```
**Adjuntar:** `ejemplos/calculadora_gui.sipi`, `ejemplos/formulario_completo.sipi`, `FUNCTIONS.md`

## Para un juego 2D

```
Escribí un juego 2D en SiPi usando "crear_juego ... fin" que [describir
mecánica: personaje, obstáculos, puntaje, física, etc.]. Basate en la
estructura y los parámetros usados en estos ejemplos adjuntos (sprite,
velocidad, chocar, gravedad, etc.) sin inventar parámetros nuevos.
```
**Adjuntar:** `ejemplos/juego_simple.sipi`, `ejemplos/plataformas_fisica.sipi`, `ejemplos/enemigos_ia_particulas.sipi`

## Para una página web

```
Escribí un programa en SiPi que genere una página web con
"pagina_web ... fin" que tenga [describir: título, secciones, formulario,
etc.]. Basate en la estructura de estos ejemplos adjuntos.
```
**Adjuntar:** `ejemplos/crear_sitio_web.sipi`, `ejemplos/formulario_contacto_web.sipi`

## Para trabajar con archivos, JSON/CSV o SQLite

```
Escribí un programa en SiPi que [describir: guardar datos, leer un CSV,
consultar una base SQLite, etc.]. Usá los comandos de la sección
"Archivos, datos y base de datos" de FUNCTIONS.md exactamente como
están documentados ahí, incluyendo la sintaxis "-> variable" para los
comandos que devuelven un valor.
```
**Adjuntar:** `FUNCTIONS.md`, `ejemplos/inventario_json_csv.sipi`, `ejemplos/base_de_datos.sipi`

## Para programación orientada a objetos

```
Modelá [describir el dominio] en SiPi usando "clase", herencia con
"hereda_de" e interfaces con "implementa" si corresponde. Recordá que
dentro de un metodo el objeto se llama "este", y que una instancia se
crea con "nuevo Clase(args) -> variable".
```
**Adjuntar:** `LANGUAGE_SPEC.md` (sección 8), `ejemplos/enum_y_estructuras.sipi`, `ejemplos/interfaces_v41_5.sipi`

## Para revisar/corregir código SiPi ya escrito

```
Revisá este programa SiPi y corregí cualquier error de sintaxis. Prestá
especial atención a: bloques sin su "fin" correspondiente, comandos que
no existan en FUNCTIONS.md, uso de "=" en vez de "-> variable" para
comandos que devuelven un valor, y comillas dobles escapadas con \"
(no funcionan en SiPi).

Código a revisar:
[PEGAR CÓDIGO]
```
**Adjuntar:** `FUNCTIONS.md`, `SYNTAX.md`
