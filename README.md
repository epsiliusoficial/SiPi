# SiPi v31.1.0

## Novedades de la version 31.1 — Bugs reales de control de flujo + excepciones propias

### Bug encontrado y corregido: 'romper'/'continuar' fuera de lugar
Se encontraron y corrigieron DOS bugs relacionados al agregar mas pruebas
sobre `romper`/`continuar` (introducidos en la v31.0):
1. Usar `romper` o `continuar` fuera de cualquier bucle terminaba en un
   **traceback crudo de Python** en vez de un error claro de SiPi. Ahora
   se valida en el momento exacto y se informa con un mensaje entendible.
2. Un `romper` (o `continuar`) ejecutado dentro de una funcion que NO
   tiene su propio bucle, pero que fue llamada desde dentro de un bucle
   del programa que la invoco, se **escapaba silenciosamente y rompia el
   bucle del que llamaba** — un bug de aislamiento real, no cosmetico.
   Se agrego un contador de profundidad de bucles (`profundidad_bucles`)
   que se resetea al entrar a una funcion y se restaura al salir, para
   que el control de flujo de una funcion nunca se filtre a quien la
   llama. Probado especificamente con este escenario.

### Excepciones propias reales: `lanzar_error`
Nuevo comando `lanzar_error "mensaje"` para lanzar un error personalizado
desde cualquier parte del programa (por ejemplo, validaciones dentro de
una funcion), capturable con la sintaxis existente `intentar` /
`capturar` (el mensaje queda disponible en la variable `error`). Antes
solo los errores internos del interprete generaban un `SiPiError`; ahora
el programador de SiPi puede definir sus propias reglas de validacion y
lanzar errores propios de la misma manera, como en cualquier lenguaje
grande (`throw`/`raise`).



## Novedades de la version 31.0 — Control de flujo real, funcional, y mas velocidad

### Bugs corregidos
- Al agregar `romper`/`continuar` se detecto y corrigio un bug donde el
  manejador generico de errores de `_ejecutar_bloque` envolvia esas
  senales de control de flujo en un `SiPiError` vacio en vez de dejarlas
  propagar hasta el bucle que las tiene que atrapar. Se agrego una
  excepcion explicita para `RomperBucle`/`ContinuarBucle` antes del
  `except Exception` generico.

### Control de flujo real: `romper` y `continuar`
Nuevos comandos `romper` (break) y `continuar` (continue), soportados
dentro de `mientras`, `repetir` y `para_cada`. Antes no habia forma de
cortar o saltear una iteracion sin reestructurar todo el bucle con
condicionales anidados. Probado con casos que combinan ambos dentro del
mismo bucle.

### Programacion funcional real sobre listas
Nuevos comandos que reciben el **nombre de una funcion SiPi** y la
aplican de verdad sobre una lista (no son simulaciones, ejecutan la
funcion definida por el usuario elemento por elemento):
- `lista_mapear lista con funcion -> variable`
- `lista_filtrar lista con funcion -> variable`
- `lista_reducir lista con funcion desde valor_inicial -> variable`
- `lista_unir lista "separador" -> variable`
- `lista_aplanar lista -> variable`

### Nuevas funciones de texto y utilidades
- `texto_recortar` (trim de espacios), `texto_empieza_con`,
  `texto_termina_con`, `texto_repetir`.
- `tipo_de expresion -> variable`: inspeccion de tipos en tiempo de
  ejecucion (`"texto"`, `"numero"`, `"lista"`, `"diccionario"`,
  `"booleano"`).

### Velocidad real (medida con benchmarks, no estimada)
- **Cache de `_encontrar_fin`**: antes, cada vez que se llamaba a una
  funcion que contiene un bucle o un `si`, el interprete volvia a
  escanear linea por linea para encontrar el `fin` correspondiente.
  Ahora ese resultado se memoiza (por identidad del bloque de lineas),
  asi que una funcion llamada miles de veces solo escanea su estructura
  una vez.
- **Cache propia de patrones regex (`_m()`)**: las ~126 llamadas a
  `re.match()` repartidas por todo el interprete (una por cada tipo de
  instruccion) ahora pasan por una cache directa en un diccionario,
  evitando el overhead de la cache interna de `re` (que hace un lookup
  con lock en cada llamada) en el camino mas caliente del interprete.
- **Resultado medido**: en un benchmark con una funcion de cuerpo largo
  llamada 3.000 veces, el tiempo bajo de **3.30s a 2.95s en promedio
  (~11-13% mas rapido)**, comparado directamente contra v29 corriendo el
  mismo programa. En bucles simples sin llamadas a funciones la mejora
  es marginal, porque el camino rapido de operaciones matematicas
  agregado en v29 ya cubria ese caso.



## Novedades de la version 30.0 — Ecosistema, datos reales y backend

Esta version se enfoca en cerrar los bugs de publicacion/distribucion
encontrados en v29 y en sumar tres sistemas nuevos pedidos para acercar
SiPi al nivel de un lenguaje/plataforma "grande":

### Bugs corregidos
- **`editor.exe` / `editor_sipi.py` con `ModuleNotFoundError: tkinter`**:
  ahora el import de tkinter esta protegido; si falta, se muestra un
  mensaje claro con instrucciones por sistema operativo, en vez de un
  traceback crudo.
- **`generar_exe.py` filtraba el codigo fuente dentro del .exe**: ahora
  usa automaticamente `sipi_protegido.py` (el motor ofuscado) si existe
  en la carpeta, y solo cae de vuelta a `sipi.py` con un aviso explicito
  si no se protegio el proyecto todavia.
- **Los `.bat` de la carpeta de publicacion apuntaban a los `.py`
  originales** (`sipi.py`, `editor_sipi.py`, `generar_exe.py`) que ya no
  existen ahi: se creo `publicar.py` / `publicar.bat`, que arma una
  carpeta `PUBLICACION/` limpia con los archivos protegidos y los `.bat`
  ya corregidos para apuntar a ellos (`sipi_protegido.py`,
  `editor_protegido.py`, `generar_exe_protegido.py`).
- **No existia una estructura oficial de publicacion**: `PUBLICACION/`
  ahora se genera siempre desde cero (se borra y se reconstruye), nunca
  mezcla archivos de desarrollo con archivos de distribucion, y nunca
  incluye `sipi.py`, `editor_sipi.py`, `generar_exe.py` ni
  `proteger_codigo.py`.
- **Verificacion de punta a punta**: se probo exactamente el escenario de
  un usuario final descargando el proyecto y ejecutandolo en una carpeta
  limpia y separada (simulando un `git clone`/descarga de ZIP), corriendo
  `sipi_protegido.py` directamente contra los ejemplos y confirmando
  salida identica a la version sin proteger.

### Sistema 1 — Administrador de paquetes (`instalar_modulo`)
Nuevo comando `instalar_modulo "nombre"` (o `instalar_modulo "https://.../modulo.sipi"`
para instalar directo desde cualquier URL, por ejemplo un repo de GitHub de
un tercero). Descarga real por HTTP el archivo `.sipi`, lo guarda en
`modulos_instalados/` y queda listo para `importar "modulos_instalados/nombre.sipi"`.
El registro por defecto se controla con la variable de entorno
`SIPI_REGISTRO_MODULOS` — cualquier comunidad puede publicar su propio
repositorio de modulos sin que SiPi tenga que cambiar.

### Sistema 2 — Bases de datos reales (SQLite)
Comandos nuevos: `sqlite_conectar "archivo.db" como db`,
`sqlite_ejecutar db "SQL"`, `sqlite_consultar db "SELECT ..." en variable`
(devuelve una lista de diccionarios reales) y `sqlite_cerrar db`. Usa el
modulo `sqlite3` de la libreria estandar de Python: sin dependencias
externas, con datos reales persistidos en disco.

### Sistema 3 — API Web real (backend completo)
Comandos nuevos: `escuchar_ruta "/api/ruta" con nombre_funcion` para
registrar una ruta, e `iniciar_api_web puerto` para levantar un servidor
HTTP real (con la libreria estandar `http.server`) que recibe peticiones
GET/POST/PUT/DELETE desde cualquier lugar (apps moviles, webs externas,
`curl`, etc.), las despacha a la funcion SiPi registrada pasandole un
diccionario `peticion` (con `metodo`, `ruta`, `query` y `cuerpo` ya
parseado si es JSON), y devuelve como respuesta JSON real lo que la
funcion entregue con `devolver`. `detener_api_web` la apaga. Se probo con
peticiones reales via `curl` contra rutas existentes e inexistentes
(200 y 404 respectivamente).



**SiPi** es una herramienta con lenguaje propio, muy simple de aprender pero
muy abierta, para crear paginas web, aplicaciones, juegos, programas de
escritorio y automatizaciones. Pensada para que la use cualquiera: un chico
que arranca a programar, un profesional de cualquier carrera, una empresa
grande, o quien necesite prototipar rapido algo serio. Todo lo que hace es
**real y funcional** — no hay simulaciones, demos ni botones falsos.

## Verificacion adicional realizada en esta ronda (con pantalla real Xvfb)

Ademas de las pruebas de consola habituales, en esta ronda se instalo una
pantalla virtual real (Xvfb) para poder ejecutar y verificar de principio
a fin, con ventanas de verdad:

- ✅ El **Editor Visual** abre correctamente sin errores.
- ✅ El **Depurador visual** fue probado con un `mainloop()` real: se
  confirmo que un breakpoint pausa la ejecucion en la linea exacta, que
  cada clic en "Continuar" avanza una iteracion mostrando el valor real
  de las variables (`0 -> 1 -> 2 -> 3 -> 4 -> 5`), y que sin breakpoints
  "Continuar" corre el programa hasta el final, tal como se espera.
- ✅ Los ejemplos con **ventanas graficas** (`calculadora_gui.sipi`,
  `panel_con_pestanias.sipi`, `formulario_completo.sipi`,
  `agenda_contactos.sipi`) abren sin errores.
- ✅ Los ejemplos con **juegos de pygame** (`juego_simple.sipi`,
  `plataformas_fisica.sipi`, `enemigos_ia_particulas.sipi`) corren sin
  errores durante varios segundos reales de juego.
- ✅ El **servidor web** generado por `iniciar_servidor_web` fue probado
  con una peticion HTTP real (`curl`), confirmando una respuesta 200 con
  el HTML correcto.
- ✅ Se encontro y corrigio un **bug real de colisiones** (ver version
  20.0): las colisiones se disparaban en cada cuadro mientras los sprites
  seguian tocandose, en vez de una sola vez.

## Novedades de la version 29.0 — Velocidad real y proteccion de codigo fuente

- ✅ **Interprete mas rapido de verdad**: se identificaron los cuellos de
  botella reales con un perfilador (`cProfile`) y se optimizaron. Un
  benchmark de 50.000 iteraciones de un bucle con operaciones
  matematicas paso de **1.264 segundos a 0.719 segundos** (~43% mas
  rapido), con resultados identicos, verificado antes y despues del
  cambio. Los cambios: patrones de expresiones regulares precompilados
  (en vez de recompilarlos en cada linea), y un camino rapido para
  operaciones matematicas simples (`a + b`, `x * 2`, etc.) que evita
  pasar por el motor generico de evaluacion cuando no hace falta.
- ✅ **Sistema real de proteccion/ofuscacion de codigo fuente**
  (`proteger_codigo.py`, o el boton de un clic `proteger_codigo.bat`):
  genera versiones de `sipi.py`, `editor_sipi.py` y `generar_exe.py` que
  **no contienen codigo fuente legible** (compila a bytecode real de
  Python, lo serializa y lo codifica), para poder subir o distribuir el
  proyecto sin exponer el codigo, los nombres de variables ni los
  comentarios internos. Se verifico que el archivo protegido ejecuta
  **exactamente igual** que el original (mismos resultados en todos los
  ejemplos probados), y que no contiene ningun nombre de funcion o clase
  en texto plano.

**Nota honesta sobre la proteccion de codigo**: esta tecnica (bytecode
serializado y codificado) es la misma que usan muchas herramientas
simples de proteccion de Python. Impide que alguien abra el archivo con
un editor de texto y lea o copie tu codigo directamente. No es
"irrompible" ante alguien con conocimientos avanzados de ingenieria
inversa (ninguna proteccion de Python lo es), pero es una barrera real y
efectiva para el uso normal de distribucion de un proyecto.

## Novedades de la version 28.0 — Correccion profunda del ambito local (parte 2)

Al agregar el ambito local de variables en la version 27, se detecto que
la correccion habia quedado incompleta: solo `variable`, `sumar`, `restar`
y `llamar_valor` respetaban el nuevo ambito, pero **decenas de comandos**
que crean o leen variables (`lista_crear`, `lista_agregar`,
`diccionario_crear`, `diccionario_asignar`, `matriz_crear`, `preguntar`,
`leer_archivo`, `json_leer`, `csv_leer`, `hash_texto`, `azar_entre`, y
practicamente cualquier comando con `-> variable`) seguian escribiendo
directamente en el espacio global, sin pasar por el nuevo sistema de
ambitos.

- ✅ **Corregidos mas de 90 puntos del interprete** para que respeten el
  ambito local de forma consistente. Se verifico con un caso muy exigente:
  una funcion recursiva que crea un diccionario nuevo en cada llamada
  (`diccionario_crear nodo`) — antes, todas las llamadas recursivas
  terminaban compartiendo el mismo diccionario global sin darse cuenta,
  dando resultados incorrectos silenciosamente. Ahora cada llamada tiene
  su propio diccionario aislado, como corresponde.
- ✅ Se mantuvo a proposito el comportamiento de "variable persistente
  global" para los casos donde tiene sentido (acumuladores con
  `sumar`/`restar`, el puntaje de los juegos, la posicion de los sprites,
  y las variables ligadas a widgets de una ventana), para no romper
  patrones como `sumar puntaje 1` dentro de una funcion de colision.
- ✅ Nuevo ejemplo `estructuras_recursivas.sipi`: una lista y un arbol de
  diccionarios construidos con recursion real, aislados correctamente por
  llamada.

**Nota honesta**: si escribiste programas en versiones anteriores que
dependian (sin saberlo) del comportamiento anterior de variables
compartidas entre llamadas recursivas para "acumular" datos de forma
implicita, ese patron ya no funciona igual — ahora hay que pasar y
devolver los datos explicitamente (como en el ejemplo de arriba), que es
la forma correcta y esperada de trabajar con funciones en cualquier
lenguaje de programacion.

## Novedades de la version 27.0 — Correccion critica: la recursion no funcionaba

Esta es la correccion mas importante de todas las realizadas hasta ahora.

- ✅ **Corregido un bug arquitectonico grave: las funciones recursivas
  daban resultados incorrectos**. `factorial(5)` devolvia `1` en vez de
  `120`, y `fibonacci(10)` devolvia `1` en vez de `55`. La causa: SiPi no
  tenia ambito local de variables — los parametros y las variables
  declaradas dentro de una funcion vivian en un unico espacio global
  compartido. Cuando una funcion se llamaba a si misma (recursion), la
  llamada mas profunda pisaba los parametros y variables de las llamadas
  anteriores, corrompiendo sus calculos silenciosamente. Peor aun, esto
  tambien afectaba a llamadas normales (no recursivas): si el programa
  principal tenia una variable con el mismo nombre que un parametro de
  una funcion, se corrompia al llamarla.
- ✅ **La solucion**: cada llamada a una funcion ahora tiene su propio
  ambito local real (como en cualquier lenguaje de programacion serio).
  Los parametros y las variables declaradas dentro de la funcion quedan
  aislados de esa llamada especifica. Las variables que ya existian antes
  de la llamada (como un contador global de puntaje) se siguen pudiendo
  modificar normalmente con `sumar`/`restar`, para no romper patrones
  como `sumar puntaje 1` dentro de una funcion de colision de un juego.
- ✅ Se verifico exhaustivamente: `factorial(10) = 3628800`, los primeros
  10 numeros de Fibonacci correctos, una variable global mutada
  correctamente desde una funcion, y una variable del programa principal
  que ya NO se corrompe al llamar una funcion con un parametro del mismo
  nombre.
- ✅ Nuevo ejemplo `funciones_recursivas.sipi`: factorial y Fibonacci
  calculados correctamente del 1 al 10.

**Como se encontro**: se probo el patron de programacion mas basico y
universal que existe — una funcion recursiva — algo que cualquier persona
aprendiendo a programar intenta hacer temprano. El resultado incorrecto
(pero sin ningun error visible) revelo que faltaba una pieza fundamental
del lenguaje.

## Novedades de la version 26.0 — Sprites y mundos con posiciones dinamicas

- ✅ **Corregido el mismo tipo de bug en `sprite` y `tamano_mundo`** dentro
  de `crear_juego`: no aceptaban variables para la posicion, el tamaño o
  el color de un sprite, solo numeros y texto literal. Esto rompia un
  patron muy natural en juegos: generar enemigos en posiciones
  **aleatorias** con `azar_entre` y pasarselas al sprite. Se confirmo con
  una prueba directa que un sprite creado con variables (`sprite enemigo
  px py 30 30 "rojo"`) toma exactamente los valores reales de esas
  variables.
- ✅ Nuevo ejemplo `sprites_posiciones_dinamicas.sipi`: un juego con dos
  enemigos que aparecen en posiciones aleatorias distintas cada vez que
  se ejecuta.

## Novedades de la version 25.0 — Coordenadas dinamicas en todos los widgets

- ✅ **Ultima ronda de esta serie de correcciones**: se generalizaron las
  coordenadas y tamaños (`x`, `y`, `ancho`, `alto`) de **todos** los
  widgets restantes (`imagen`, `casilla`, `barra_progreso`, `lista`,
  `menu_desplegable`) para aceptar variables y expresiones, no solo
  numeros literales. Se probo un caso integral con una ventana completa
  donde todas las posiciones se calculan con variables
  (`pos_x`, `pos_y`, `ancho_barra`), confirmando que cada widget se crea
  en el lugar correcto y responde con los valores reales esperados.

Con esta version, el motor de ventanas de SiPi acepta de forma consistente
variables y expresiones en practicamente todos sus argumentos —
texto, colores, posiciones y tamaños — en lugar de exigir literales fijos,
que era una limitacion real que afectaba a cualquier interfaz un poco mas
dinamica que un formulario estatico.

## Novedades de la version 24.0 — Listas y menus con datos dinamicos reales

- ✅ **Corregido el mismo tipo de bug en `lista` (listbox) y
  `menu_desplegable`**: hasta ahora solo aceptaban un texto literal fijo
  separado por `|` (`"Python|JavaScript|SiPi"`). Si querias mostrar el
  contenido de una lista real de SiPi (por ejemplo, construida con
  `lista_agregar` a partir de datos de un archivo o una base de datos),
  no habia forma de conectarla al widget. Ahora ambos aceptan
  directamente una lista de SiPi ademas de seguir aceptando el texto
  literal con `|` de siempre:
  `lista 20 40 35 6 tareas_pendientes -> tarea_elegida`
- ✅ Nuevo ejemplo `lista_menu_dinamicos.sipi`: una lista de tareas y un
  selector de pais, ambos construidos con datos reales en listas de SiPi
  en vez de texto fijo.

## Novedades de la version 23.0 — Bug importante: widgets dinamicos en bucles

- ✅ **Corregido un bug real que rompia un patron muy comun**: crear
  widgets (`etiqueta`, `boton`, `entrada`, `cuadro`) dentro de un
  `para_cada` o `repetir`, usando una variable para el texto o una
  posicion calculada (por ejemplo, `etiqueta producto 30 y_actual` para
  listar productos uno debajo del otro). Antes, estos comandos solo
  aceptaban texto literal entre comillas y numeros literales — si se
  usaba una variable, el widget **no se creaba y no avisaba ningun
  error**. Ahora `etiqueta`, `boton`, `entrada` y `cuadro` aceptan
  variables y expresiones tanto en el texto/color como en las
  coordenadas, ademas de seguir aceptando literales.
- ✅ Nuevo ejemplo `lista_dinamica_gui.sipi`: un catalogo de productos que
  genera una etiqueta por cada producto de una lista, con posiciones
  calculadas automaticamente.

**Como se encontro**: se probo el patron real de listar los elementos de
una lista SiPi como etiquetas en una ventana (algo que cualquiera
intentaria hacer para mostrar datos dinamicos), y se confirmo que no se
creaba ningun widget, sin ningun mensaje de error.

## Novedades de la version 22.0 — Dos bugs graves encontrados y corregidos

- ✅ **Corregido un crash real y grave**: el widget `cuadro` (un rectangulo
  de color dentro de una ventana) hacia que **todo el programa se cayera**
  si se usaba un nombre de color en español como `"azul"` o `"rojo"`,
  porque Tkinter solo entiende nombres de color en ingles o codigos
  hexadecimales. Se agrego una tabla de traduccion real de colores en
  español (`rojo`, `verde`, `azul`, `amarillo`, `morado`, `naranja`,
  `rosa`, `celeste`, `dorado`, etc.) compartida entre las ventanas y los
  juegos, para que nunca mas se rompa un programa por usar un color en
  español.
- ✅ **Corregido un bug real en los campos de entrada de las ventanas**:
  si el usuario escribia un numero en un campo `entrada` (por ejemplo
  para hacer una calculadora), SiPi lo guardaba como texto en vez de
  numero, asi que cualquier cuenta matematica con ese valor fallaba
  silenciosamente (el resultado quedaba como el texto de la formula sin
  calcular, en vez de un numero). Ahora los campos de entrada detectan
  automaticamente si lo que escribiste es un numero y lo convierten,
  igual que ya hacia el comando `preguntar`.
- ✅ Nuevo ejemplo `calculadora_con_cuadro.sipi`: una calculadora de total
  real (precio x cantidad) que ademas prueba que los colores en español
  ya no rompen el programa.

**Como se encontraron**: se probo la interaccion real con una calculadora
de ejemplo (escribiendo numeros en los campos y haciendo clic en
"Calcular"), en vez de solo revisar que la ventana abriera. El primer
intento crasheo por el color, y despues de arreglar eso, el segundo
intento revelo que el calculo daba un resultado incorrecto (texto sin
calcular en vez de 450). Ambos bugs afectaban un caso de uso central y
muy comun (una calculadora), asi que se les dio prioridad alta.

## Novedades de la version 21.0 — Tres bugs reales de GUI encontrados y corregidos

Siguiendo con las pruebas usando pantalla virtual real (Xvfb), esta vez se
probo la interaccion real con los widgets (escribir en campos, marcar
casillas, elegir de listas, hacer clic en botones) en vez de solo verificar
que las ventanas abren. Esto revelo tres bugs reales:

- ✅ **Corregido: el widget `imagen` dentro de una `ventana` no hacia nada**
  (bug silencioso, sin error visible). Estaba registrado como comando
  valido pero nunca se habia implementado. Ahora carga imagenes reales
  (PNG, JPG, etc.) con Pillow, con soporte opcional de redimensionado:
  `imagen "foto.png" x y` o `imagen "foto.png" x y ancho alto`.
- ✅ **Corregido: la `casilla` (checkbox) no actualizaba su variable si se
  marcaba de forma programatica**, solo con clics reales del mouse. Se
  unifico su mecanismo de actualizacion (usa `trace_add` como el resto de
  los widgets) para que sea mas robusto en todos los casos.
- ✅ **Corregido el mismo problema en `menu_desplegable`**: la variable no
  se actualizaba correctamente en algunos casos. Mismo arreglo aplicado.

Estos bugs se encontraron simulando interacciones reales (escribir texto,
marcar casillas, seleccionar de una lista, hacer clic en un boton) y
verificando que las variables de SiPi reflejaran los valores correctos
despues — no solo revisando que el codigo no lanzara errores.

- ✅ Nuevo ejemplo `galeria_imagenes.sipi`: muestra imagenes reales en una
  ventana, con y sin redimensionado.

## Novedades de la version 20.0 — Automatizacion de escritorio + correccion importante en juegos

- ✅ **Captura de pantalla real** (`captura_pantalla "archivo.png"`): guarda
  una imagen PNG real de lo que hay en la pantalla en ese momento.
- ✅ **Portapapeles real** (`copiar_portapapeles "texto"` /
  `pegar_portapapeles -> variable`): copia y lee el portapapeles real del
  sistema operativo, para integrar SiPi con cualquier otra aplicacion.
- ✅ **Corregido un bug importante en las colisiones de juegos**: hasta
  esta version, la funcion de `chocar` se disparaba en **cada uno de los
  60 cuadros por segundo** mientras dos sprites seguian superpuestos (por
  ejemplo, un enemigo tocando al jugador durante medio segundo generaba
  30 llamadas a la funcion en vez de 1). Ahora la funcion se dispara
  **una sola vez**, en el instante exacto en que empiezan a tocarse, tal
  como se espera en cualquier juego real. Se detecto probando el nuevo
  ejemplo de IA con Xvfb (pantalla virtual) y corriendo el juego de
  verdad, no solo revisando el codigo.
- ✅ Nuevo ejemplo `automatizacion_escritorio.sipi`: captura de pantalla y
  portapapeles reales en accion.

**Nota tecnica**: esta version se probo con una pantalla virtual real
(Xvfb) ademas de las pruebas de consola habituales, lo que permitio
ejecutar por primera vez los ejemplos con ventanas graficas y juegos de
principio a fin (no solo verificar que el codigo compila), y encontrar
el bug de colisiones arriba mencionado.

## Novedades de la version 19.0 — IA simple y particulas para juegos

- ✅ **IA real para enemigos** (`ia nombre_sprite comportamiento objetivo
  velocidad`):
  - `ia enemigo seguir jugador 1.5` — el sprite persigue al objetivo de
    verdad, calculando la direccion real hacia el cada frame.
  - `ia guardian escapar jugador 1.2` — el sprite huye del objetivo.
  - `ia patrulla patrullar x1 y1 x2 y2 velocidad` — el sprite camina de
    ida y vuelta entre dos puntos, cambiando de direccion solo.
- ✅ **Sistema de particulas real** (`explosion x y cantidad`,
  `humo x y cantidad`, `fuego x y cantidad`, o `particulas x y cantidad
  "tipo"`): genera un estallido real de particulas de colores que se
  dispersan y se desvanecen con el tiempo, usable desde cualquier funcion
  (por ejemplo, al chocar con un enemigo).
- ✅ **Posiciones de sprites accesibles como variables reales**
  (`nombre_x`, `nombre_y`): cualquier funcion (como una funcion de
  colision) puede leer `jugador_x` y `jugador_y` para saber donde esta
  el jugador en ese momento, por ejemplo para disparar una explosion
  justo en su posicion.
- ✅ Nuevo ejemplo `enemigos_ia_particulas.sipi`: un perseguidor que sigue
  al jugador, un guardian que lo esquiva, un sprite que patrulla solo, y
  explosiones reales al chocar.

## Novedades de la version 18.0 — Fisica real para juegos

- ✅ **Gravedad real** (`gravedad N` dentro de `crear_juego`): el jugador
  cae con aceleracion real en vez de moverse con las flechas arriba/abajo.
  Con gravedad activada, la barra espaciadora hace **saltar** al jugador
  de verdad (impulso proporcional a la gravedad).
- ✅ **Rebote real** (`rebote N`, de 0 a 1): al tocar el suelo, el jugador
  rebota con menos energia en cada bote, como una pelota real, hasta
  asentarse.
- ✅ **Friccion real** (`friccion N`): el jugador frena gradualmente al
  soltar las flechas, en vez de detenerse en seco.
- ✅ **Mundos mas grandes que la pantalla** (`tamano_mundo ANCHO ALTO`) y
  **camara que sigue al jugador** (`camara_seguir jugador`): para hacer
  niveles de plataformas que se desplazan mientras el jugador avanza, como
  un juego de verdad.
- ✅ Nuevo ejemplo `plataformas_fisica.sipi`: un nivel de plataformas de
  1600 pixeles de ancho (mas grande que la ventana) con salto, gravedad,
  rebote, friccion, camara que sigue al jugador, y monedas para recolectar.

**Nota**: si no usas `gravedad`, el juego sigue funcionando exactamente
igual que antes (movimiento clasico con las 4 flechas), para no romper
ningun proyecto existente.

## Novedades de la version 17.0 — Formularios y CSS automatico

- ✅ **Formularios web reales** (`formulario "accion" / campo / boton / fin`):
  genera un `<form>` completo y funcional dentro de `pagina_web`, con
  distintos tipos de campo:
  - `campo "Nombre" texto` — campo de texto normal
  - `campo "Correo" email` — campo de email
  - `campo "Edad" numero` — campo numerico
  - `campo "Clave" clave` — campo de contraseña
  - `campo "Mensaje" area` — area de texto multilinea
  - `boton "Enviar"` — boton de envio del formulario
- ✅ **CSS automatico con temas** (`tema "oscuro"` / `tema "claro"` y
  `color "#3498db"` dentro de `pagina_web`): cambia toda la paleta de
  colores del sitio generado (fondo, texto, tarjetas, formularios) y el
  color de acento de botones y links, sin tocar una linea de CSS.
- ✅ Nuevo ejemplo `formulario_contacto_web.sipi`: una pagina de contacto
  real con tema oscuro, color personalizado y un formulario funcional.

## Novedades de la version 16.0 — HTML sin escribir HTML

- ✅ **Paginas web declarativas reales** (`pagina_web "Nombre" / ... / fin`):
  arma sitios web completos usando comandos simples en español, sin
  escribir una sola linea de HTML o CSS. SiPi genera el `index.html` y
  `estilo.css` reales, con un diseño limpio ya incluido.
  - `titulo "..."` / `subtitulo "..."` — encabezados
  - `texto "..."` — parrafos (soporta `{variables}`)
  - `boton "..."` — un boton estilizado
  - `imagen "ruta.png"` — una imagen
  - `enlace "Texto" "url"` — un link
  - `lista_web "item1|item2|item3"` — una lista con viñetas
  - `tarjeta "Titulo" "Texto"` — una tarjeta con sombra, al estilo de
    componentes modernos
  - `separador` — una linea divisoria
- ✅ Nuevo ejemplo `tienda_sin_html.sipi`: una landing page de tienda
  online completa, generada enteramente desde SiPi.

## Novedades de la version 15.0

- ✅ **Enumeraciones reales** (`enum Colores / ROJO / VERDE / AZUL / fin`):
  crea valores numerados automaticamente (`Colores_ROJO = 0`,
  `Colores_VERDE = 1`, etc.), ademas de un diccionario `Colores` completo.
  Son constantes: no se pueden modificar despues de creadas.
- ✅ **Estructuras reales** (`estructura Persona / nombre = "" / edad = 0 /
  fin`): define una plantilla con valores por defecto. El comando
  `instanciar Persona -> variable` crea una copia independiente de la
  plantilla (cada instancia es su propio diccionario, sin compartir datos
  entre si).
- ✅ **Formateador automatico de codigo** (como Black en Python): el boton
  "🪄 Formatear" del editor visual, o el comando
  `python sipi.py --formatear archivo.sipi` desde la consola, reindenta
  automaticamente cualquier programa `.sipi` con 4 espacios por nivel de
  anidamiento, sin importar lo desordenado que estuviera antes.
- ✅ Nuevo ejemplo `enum_y_estructuras.sipi`: un sistema simple de
  personajes con clases (enum) y una plantilla de personaje (estructura).

## Novedades de la version 14.0 — Depurador Visual

- ✅ **Depurador visual paso a paso real** (boton "🐞 Depurar" en el editor):
  ejecuta tu programa linea por linea en una ventana dedicada, mostrando
  el codigo con la linea actual resaltada y un panel con **todas las
  variables en vivo** (incluyendo listas y diccionarios completos) que se
  actualiza en cada paso.
  - **Breakpoints reales**: hace clic en el numero de una linea para
    poner o quitar un punto de interrupcion (se marca en rojo). La
    ejecucion se pausa automaticamente al llegar ahi.
  - **Controles**: "⏭ Paso" avanza una linea a la vez, "▶ Continuar" corre
    hasta el proximo breakpoint, "⏹ Detener" corta la ejecucion en el
    momento exacto en que estés.
  - Pensado para programas de consola y de logica (listas, diccionarios,
    matrices, funciones); los programas con `ventana` o `crear_juego`
    abren su propia ventana real y se depuran mejor con `modo_debug` por
    consola.

## Novedades de la version 13.0

- ✅ **Temporizadores reales** (`cada N segundos ... fin`): repite un bloque
  de codigo cada cierto tiempo. Soporta dos modos:
  - `cada 1 segundos 5 veces / fin` — se repite una cantidad fija de veces.
  - `cada 0.5 segundos / fin` — se repite indefinidamente hasta que el
    propio codigo use `detener_temporizador` para pararlo (por ejemplo, al
    cumplirse una condicion).
- ✅ Nuevo ejemplo `temporizadores.sipi`: una cuenta regresiva real y un
  temporizador que se detiene solo cuando se cumple una condicion.

## Novedades de la version 12.0

- ✅ **JSON real**: `json_crear`, `json_leer`, `json_guardar`, `json_texto`.
  Cualquier diccionario o lista de SiPi se puede guardar como un archivo
  `.json` real y volver a cargar despues, o convertir a texto legible.
- ✅ **CSV real, compatible con Excel**: `csv_leer`, `csv_guardar`. Una
  lista de diccionarios se guarda como un archivo `.csv` real con
  encabezados, listo para abrir directamente en Excel o Google Sheets, y
  tambien se puede leer un CSV existente como una lista de diccionarios.
- ✅ Nuevo ejemplo `inventario_json_csv.sipi`: un caso real de guardar un
  producto en JSON y una lista de ventas en CSV, y volver a leerlos.

## Novedades de la version 11.0

- ✅ **Constantes reales** (`const NOMBRE = valor`): una vez definida, SiPi
  impide modificarla con `variable`, `sumar` o `restar`, y avisa con un
  error claro si lo intentas.
- ✅ **Comentarios multilinea** (`/* ... */`): para documentar bloques
  completos de codigo, ademas de los comentarios de una linea (`//`).
- ✅ **Cadenas multilinea** (`"""..."""`): para textos largos, plantillas
  HTML, o mensajes de varias lineas, con interpolacion de `{variables}`
  incluida. Funciona igual en el archivo principal y en modulos
  importados.
- ✅ **Mensajes de error con sugerencias inteligentes**: si escribis mal un
  comando o el nombre de una funcion, SiPi te sugiere la opcion mas
  parecida ("¿Quisiste decir 'diccionario_asignar'?").
- ✅ **Pila de llamadas al fallar** (stack trace real): si un error ocurre
  dentro de una funcion llamada por otra funcion, SiPi te muestra la
  cadena completa de llamadas que llevo hasta ahi, para encontrar el
  problema mas rapido.
- ✅ Nuevo ejemplo `funciones_nuevas_v11.sipi` que muestra todo esto en
  conjunto.

### Sobre el resto de ideas propuestas (JSON, CSV, PDF, email, fisica de
juegos, IA simple, gestor de paquetes, autocompletado, depurador visual,
etc.)

Son una lista excelente y varias van a ir sumandose en las proximas
versiones. Para mantener cada entrega **real y probada** (sin prometer
botones que no funcionen), se van agregando de a bloques que se puedan
implementar y verificar de verdad, en lugar de simular todas de una vez.
Las de mayor impacto y viabilidad inmediata (JSON, CSV, temporizadores,
formateador de codigo) son las siguientes candidatas.

## Novedades de la version 10.0 — correccion importante de usabilidad

- ✅ **Corregido bug grave**: los comandos de archivos y datos
  (`leer_archivo`, `crear_archivo`, `borrar_archivo`, `crear_carpeta`,
  `copiar_archivo`, `listar_archivos`, `comprimir_carpeta`,
  `descomprimir_zip`, `guardar_dato`, `obtener_dato`, `borrar_dato`,
  `obtener_url`) solo aceptaban nombres de archivo o claves escritos
  literalmente entre comillas. Si guardabas el nombre en una variable (algo
  muy comun, por ejemplo al recorrer una lista de archivos con
  `para_cada`), el comando fallaba silenciosamente. Ahora todos estos
  comandos aceptan tanto texto literal (`"archivo.txt"`) como una variable
  (`nombre_archivo`) indistintamente.
- ✅ **Corregido bug de aliasing en listas y diccionarios**: si agregabas la
  misma variable (un diccionario o una lista) a distintos elementos de una
  lista, una matriz, u otro diccionario, todos terminaban compartiendo el
  mismo objeto por error. Ahora cada asignacion crea una copia
  independiente, evitando cambios inesperados entre datos que deberian ser
  distintos.
- ✅ Nuevo ejemplo: `procesar_archivos_con_variables.sipi`, que muestra el
  patron real (muy comun) de recorrer una lista de nombres de archivo y
  procesarlos uno por uno.

## Novedades de la version 9.0 — correcciones importantes de estabilidad

- ✅ **Proteccion contra importaciones circulares**: si el archivo A importa
  a B y B importa de vuelta a A, SiPi ya no se cuelga ni se cae — detecta
  el ciclo y continua normalmente. Ademas, importar el mismo modulo dos
  veces desde el mismo archivo ya no lo vuelve a ejecutar innecesariamente.
- ✅ **Corregido bug de aliasing en matrices**: si creabas una matriz usando
  un diccionario o una lista como valor inicial, todas las celdas
  compartian el mismo objeto por error — modificar una celda modificaba
  todas las demas. Ahora cada celda tiene su propia copia independiente,
  como corresponde.
- ✅ Verificado que los generadores de apps Android y Windows funcionan
  correctamente incluso con nombres de proyecto que tienen espacios o
  caracteres especiales.

## Novedades de la version 8.0

- ✅ **Sonido generado sin archivos externos** (`reproducir_tono`, y `tono`
  dentro de `crear_juego`): SiPi genera ondas de sonido reales (senoidales)
  al momento, para que no dependas de conseguir un archivo `.wav` para
  tener efectos de sonido. Util para juegos, notificaciones o melodias
  simples.
- ✅ **Correccion real de bug**: el sonido de las colisiones (`chocar`) no
  se reproducia correctamente porque buscaba el sonido con el nombre
  equivocado. Ahora `chocar` acepta un nombre de sonido opcional:
  `chocar sprA sprB funcion() nombre_del_sonido`.

## Novedades de la version 7.0

- ✅ **Matrices reales (arrays 2D)**: `matriz_crear`, `matriz_asignar`,
  `matriz_obtener`, `matriz_filas`, `matriz_columnas`. Perfecto para
  tableros de juegos (tres en raya, buscaminas, ajedrez), hojas de calculo
  simples, o cualquier dato en forma de grilla.
- ✅ **Obstaculos con movimiento real en los juegos** (`mover_aleatorio`):
  los sprites pueden moverse solos por la pantalla y rebotar en los bordes,
  para juegos mas dinamicos con enemigos que se mueven.
- ✅ Nuevos ejemplos: un **Tres en raya** completo usando matrices y
  funciones, un **juego con obstaculos moviles**, y una **agenda de
  contactos** que combina GUI real con base de datos persistente real.

## Novedades de la version 6.0

- ✅ **Sistema de modulos real** (`importar "archivo.sipi"`): organiza tus
  proyectos grandes en varios archivos y reutiliza funciones y variables
  entre ellos, como en cualquier lenguaje serio.
- ✅ **Modo debug paso a paso** (`modo_debug`): activalo al principio de tu
  programa y SiPi te muestra cada linea antes de ejecutarla, para encontrar
  errores facilmente.
- ✅ **Pestañas reales en ventanas** (`pestanias` / `pestana "Nombre" / fin`):
  organiza tu interfaz grafica en varias pestañas, como cualquier app
  profesional.
- ✅ **Menu desplegable real** (`menu_desplegable`): un combobox real para
  elegir una opcion de una lista desplegable.
- ✅ Corregido: los valores booleanos y las funciones importadas desde
  modulos ahora funcionan de forma coherente en todos los casos.

## Novedades de la version 5.0

- ✅ **Diccionarios reales** (clave -> valor): `diccionario_crear`,
  `diccionario_asignar`, `diccionario_obtener`, `diccionario_tiene`,
  `diccionario_eliminar`, `diccionario_claves`. Ideal para fichas de
  productos, perfiles de usuario, configuraciones, etc.
- ✅ **Manejo de errores real**: bloques `intentar / capturar / fin` para que
  tu programa no se caiga ante un error (archivo faltante, dato invalido,
  etc.) y en cambio reaccione de forma controlada. La variable `error`
  queda disponible con el mensaje real dentro del bloque `capturar`.
- ✅ **Texto avanzado**: `texto_dividir`, `texto_reemplazar`, `texto_contiene`.
- ✅ **Listas mas potentes**: `lista_ordenar`, `lista_invertir`,
  `lista_contiene`, `suma_lista`, `promedio_lista`.
- ✅ **Matematica adicional**: `minimo`, `maximo`, `redondear`, y las
  constantes predefinidas `PI` y `E`.
- ✅ **Registro de eventos real** (`registrar_evento`): guarda logs con
  fecha y hora reales en un archivo, util para auditorias o depuracion.
- ✅ **Nuevos widgets de interfaz**: `barra_progreso` (barra de progreso
  real) con el comando `actualizar_barra` para moverla dinamicamente.
- ✅ Los valores booleanos ahora se muestran como `verdadero` / `falso` en
  vez de `True` / `False`, para que todo el lenguaje sea consistente.

## Todo lo que ya traia SiPi

- **Editor Visual** con vista previa en vivo del resultado mientras escribis,
  resaltado de sintaxis, panel de configuracion (temas de colores, tamaño de
  letra, color de texto personalizado), y botones para ejecutar y compilar.
- **Funciones con retorno real** (`devolver`, `llamar_valor`).
- **Bucles** `repetir`, `mientras`, y `para_cada elemento en lista`.
- **Operadores logicos** `y`, `o`, `no` en condiciones.
- **Generador de sitios web reales** (HTML/CSS/JS) y servidor web local.
- **Base de datos local persistente real** (JSON).
- **Peticiones HTTP reales**.
- **Auto-instalacion real** de componentes que falten, e instalacion de
  paquetes bajo demanda.
- **Interfaces graficas reales**: ventanas, botones, etiquetas, campos de
  texto, checkboxes, listas, barras de progreso.
- **Juegos 2D reales** con colisiones, sonido y puntaje.
- **Compilador real** de programas `.sipi` a `.exe` de Windows.
- **Generadores de proyectos reales y compilables** para Android (Kivy +
  Buildozer) y Windows (Tkinter + PyInstaller).
- **Compresion/descompresion real de archivos** (`comprimir_carpeta`,
  `descomprimir_zip`).

## Sobre la promesa de "instalar automaticamente" apps de Android

Compilar un APK real requiere el SDK de Android, NDK, Java y varios GB de
herramientas del sistema — cosas que no pueden vivir dentro de un archivo
`.sipi` ni de un `.zip`. Por eso SiPi es honesto: en vez de fingir un boton
magico, **genera el proyecto completo y funcional** para que lo compiles con
un solo comando (`buildozer android debug`), explicado paso a paso en el
`LEEME.txt` que se crea junto al proyecto.

## Requisitos (Windows 10)

- Python 3.10 o superior. Si no lo tenes, ejecuta `instalar.bat` y te va a
  guiar para descargarlo (recorda marcar "Add Python to PATH" al instalar).
- Todo lo demas se instala solo, ya sea con `instalar.bat` o
  automaticamente la primera vez que tu programa lo necesite.

## Como usar

1. Descomprimí este ZIP en cualquier carpeta.
2. Ejecutá `instalar.bat` una sola vez.
3. Opciones para trabajar:
   - `ejecutar_ejemplo.bat` — menu con todos los ejemplos, incluido el editor.
   - `editor.bat` — abre el Editor Visual de SiPi (con vista previa en vivo).
   - `sipi.bat mi_programa.sipi` — corre un programa `.sipi` por consola.
   - `compilar_programa.bat mi_programa.sipi` — genera un `.exe` real.

## El lenguaje SiPi — guia completa

```
programa "Nombre de mi programa"

// Variables, matematica y constantes
variable edad = 15
decir "PI vale {PI} y E vale {E}"
sumar edad 1
restar edad 1
raiz 16 -> raiz_de_16
potencia 2 10 -> dos_a_la_diez
azar_entre 1 100 -> numero_aleatorio
minimo 3 7 -> el_menor
maximo 3 7 -> el_mayor
redondear 4.7 -> valor_redondeado

// Texto
longitud "Hola" -> cuantas_letras
mayusculas "hola" -> en_mayusculas
minusculas "HOLA" -> en_minusculas
texto_dividir "a,b,c" "," -> partes
texto_reemplazar "hola mundo" "mundo" "SiPi" -> nuevo_texto
texto_contiene "hola mundo" "mundo" -> lo_contiene

// Condicionales con operadores logicos
si edad >= 18 y lo_contiene == verdadero
    decir "Cumple ambas condiciones"
fin
si edad < 10 o lo_contiene == verdadero
    decir "Cumple al menos una"
fin
si no lo_contiene == falso
    decir "El operador 'no' funciona"
fin

// Bucles
repetir 3 veces
    decir "Esto se repite"
fin
variable contador = 0
mientras contador < 5
    sumar contador 1
fin

// Listas reales
lista_crear numeros
lista_agregar numeros 5
lista_agregar numeros 2
lista_ordenar numeros
lista_invertir numeros
lista_contiene numeros 5 -> tiene_el_5
suma_lista numeros -> total
promedio_lista numeros -> promedio
para_cada n en numeros
    decir "Numero: {n}"
fin

// Diccionarios reales
diccionario_crear persona
diccionario_asignar persona "nombre" "Ana"
diccionario_obtener persona "nombre" -> nombre_persona
diccionario_tiene persona "nombre" -> existe
diccionario_claves persona -> claves

// Funciones (con y sin retorno)
funcion saludar(persona)
    decir "Hola, {persona}!"
fin
llamar saludar("Mundo")

funcion sumar_dos(a, b)
    devolver a + b
fin
llamar_valor sumar_dos(4, 5) -> resultado

// Manejo de errores real
intentar
    leer_archivo "puede_no_existir.txt" -> contenido
capturar
    decir "Hubo un error: {error}"
fin

// Entrada del usuario por consola
preguntar "Como te llamas?" -> nombre_usuario

// Archivos y automatizacion real
crear_carpeta "datos"
crear_archivo "datos/nota.txt" "Esto es una nota real"
leer_archivo "datos/nota.txt" -> contenido
copiar_archivo "datos/nota.txt" "datos/copia.txt"
borrar_archivo "datos/copia.txt"
listar_archivos "datos" -> archivos
comprimir_carpeta "datos" "datos_respaldo.zip"
descomprimir_zip "datos_respaldo.zip" "datos_restaurados"
registrar_evento "Se hizo una automatizacion" "eventos.log"
ejecutar "dir"
esperar 2

// Base de datos local persistente real
guardar_dato "puntaje_maximo" 9500
obtener_dato "puntaje_maximo" -> mejor_puntaje

// Utilidades varias
fecha_hora_actual -> ahora
hash_texto "clave secreta" -> hash_resultado
elegir_al_azar "rojo|verde|azul" -> color_elegido

// Peticiones web reales
obtener_url "https://api.ejemplo.com/datos" -> respuesta

// Instalar cualquier paquete de Python bajo demanda
instalar_paquete "requests"

// Ventanas reales (interfaz grafica completa)
ventana "Mi Ventana" 420 380
    etiqueta "Hola desde una ventana real" 50 20
    entrada mi_variable 50 60
    casilla "Aceptar terminos" 50 100 acepto
    lista 50 130 30 5 "Opcion A|Opcion B|Opcion C" -> opcion_elegida
    barra_progreso mi_barra 50 300 200 50
    boton "Presioname" 50 320 mi_funcion()
fin

// Juegos reales con colisiones, sonido y puntaje
funcion ganar_punto()
    sumar puntaje 1
fin
crear_juego "Mi Juego" 640 480
    sprite jugador 300 220 40 40 "cian"
    sprite meta 50 400 30 30 "verde"
    velocidad 6
    puntaje_inicial 0
    mostrar_puntaje
    chocar jugador meta ganar_punto()
fin

// Modulos: organiza tu proyecto en varios archivos
importar "mi_modulo.sipi"

// Modo debug: muestra cada linea antes de ejecutarla
modo_debug

// Pestañas y menu desplegable en ventanas
ventana "Panel" 450 380
    pestanias 20 20 400 300
        pestana "Perfil"
            etiqueta "Nombre:" 20 20
            entrada campo_nombre 100 18
            menu_desplegable 20 60 20 "Argentina|Chile|Uruguay" -> pais
        fin
        pestana "Configuracion"
            casilla "Notificaciones" 20 20 notificaciones
        fin
    fin
fin

// Paginas web declarativas: HTML sin escribir HTML
pagina_web "Mi Tienda"
    titulo "Bienvenido a Mi Tienda"
    subtitulo "Los mejores productos"
    texto "Encontra de todo un poco"
    tarjeta "Envio gratis" "En compras mayores a $50000"
    lista_web "Item 1|Item 2|Item 3"
    boton "Comprar ahora"
    enlace "Contacto" "contacto.html"
    separador
fin

// Generar y publicar un sitio web real (plantilla simple, no declarativa)
generar_pagina_web "MiSitio"
iniciar_servidor_web "MiSitio_web" 8000

// Generar proyectos reales de apps nativas
generar_app_android "MiApp"
generar_app_windows "MiPrograma"
```

### Referencia rapida de comandos

| Categoria | Comandos |
|---|---|
| Variables y matematica | `variable`, `sumar`, `restar`, `raiz`, `potencia`, `azar_entre`, `minimo`, `maximo`, `redondear`, constantes `PI`/`E` |
| Texto | `longitud`, `mayusculas`, `minusculas`, `texto_dividir`, `texto_reemplazar`, `texto_contiene` |
| Control de flujo | `si/sino/fin` (con `y`/`o`/`no`), `repetir...veces`, `mientras`, `para_cada...en` |
| Funciones | `funcion`, `llamar`, `devolver`, `llamar_valor` |
| Listas | `lista_crear`, `lista_agregar`, `lista_obtener`, `lista_longitud`, `lista_eliminar`, `lista_ordenar`, `lista_invertir`, `lista_contiene`, `suma_lista`, `promedio_lista` |
| Diccionarios | `diccionario_crear`, `diccionario_asignar`, `diccionario_obtener`, `diccionario_tiene`, `diccionario_eliminar`, `diccionario_claves` |
| Manejo de errores | `intentar`, `capturar`, `fin` (variable `error` disponible) |
| Archivos | `crear_archivo`, `leer_archivo`, `borrar_archivo`, `copiar_archivo`, `crear_carpeta`, `listar_archivos`, `comprimir_carpeta`, `descomprimir_zip` |
| Sistema | `ejecutar`, `esperar`, `instalar_paquete`, `registrar_evento` |
| Datos persistentes | `guardar_dato`, `obtener_dato`, `borrar_dato` |
| Web | `obtener_url`, `generar_pagina_web`, `iniciar_servidor_web` |
| Paginas declarativas | `pagina_web / titulo / subtitulo / texto / boton / imagen / enlace / lista_web / tarjeta / separador / tema / color / fin` |
| Formularios web | `formulario "accion" / campo "Etiqueta" tipo / boton / fin` |
| Interfaz grafica | `ventana`, `etiqueta`, `boton`, `entrada`, `casilla`, `lista`, `barra_progreso`, `actualizar_barra`, `menu_desplegable`, `pestanias`, `pestana`, `cuadro`, `imagen` (con redimensionado opcional) |
| Juegos | `crear_juego`, `sprite`, `velocidad`, `chocar`, `sonido`, `tono`, `puntaje_inicial`, `mostrar_puntaje`, `mover_aleatorio` |
| Fisica de juegos | `gravedad`, `rebote`, `friccion`, `tamano_mundo`, `camara_seguir` |
| IA y particulas | `ia nombre seguir/escapar objetivo vel`, `ia nombre patrullar x1 y1 x2 y2 vel`, `explosion`, `humo`, `fuego` |
| Automatizacion de escritorio | `captura_pantalla`, `copiar_portapapeles`, `pegar_portapapeles` |
| Apps nativas | `generar_app_android`, `generar_app_windows` |
| Utilidades | `fecha_hora_actual`, `hash_texto`, `elegir_al_azar`, `reproducir_tono` |
| JSON y CSV | `json_crear`, `json_leer`, `json_guardar`, `json_texto`, `csv_leer`, `csv_guardar` |
| Temporizadores | `cada N segundos [M veces] / fin`, `detener_temporizador` |
| Enum y estructuras | `enum Nombre / valores / fin`, `estructura Nombre / campos / fin`, `instanciar` |
| Modulos y depuracion | `importar "archivo.sipi"`, `modo_debug` |
| Matrices (2D) | `matriz_crear`, `matriz_asignar`, `matriz_obtener`, `matriz_filas`, `matriz_columnas` |

## El Editor Visual de SiPi

Abrilo con `editor.bat`. Tiene resaltado de sintaxis en vivo, un panel de
vista previa que corre tu programa en segundo plano y te muestra el
resultado apenas dejas de escribir, un boton de configuracion (temas de
colores, tamaño de letra, color de texto), y botones para ejecutar el
programa completo (incluidas ventanas y juegos reales) o compilarlo a
`.exe` con un clic.

## Publico pensado

El lenguaje esta diseñado para que lo pueda usar literalmente cualquiera:
desde un chico que recien empieza a programar, hasta un profesional de
cualquier area, una startup, o un equipo tecnico de una empresa grande que
necesite automatizar tareas, montar un sitio, prototipar una app o un juego
rapido, o armar una herramienta interna sin fricciones. El motor de abajo es
Python real, asi que todo lo que corre en SiPi es codigo real ejecutandose
en tu maquina, sin cajas negras.

## Estructura del ZIP

```
SiPi/
├── sipi.py                     <- el interprete (motor real del lenguaje)
├── sipi.bat                     <- ejecutar archivos .sipi facilmente
├── editor_sipi.py                <- editor visual (vista previa + config)
├── editor.bat                     <- abre el editor visual
├── generar_exe.py                  <- compilador real de .sipi a .exe
├── compilar_programa.bat            <- compilar con un clic
├── instalar.bat                      <- instala Python/dependencias
├── ejecutar_ejemplo.bat                <- menu de ejemplos
├── README.md
└── ejemplos/
    ├── hola_mundo.sipi
    ├── calculadora_gui.sipi
    ├── juego_simple.sipi
    ├── juego_avanzado.sipi
    ├── formulario_completo.sipi
    ├── automatizacion.sipi
    ├── generar_apps.sipi
    ├── crear_sitio_web.sipi
    ├── base_de_datos.sipi
    ├── lista_tareas.sipi
    ├── producto_con_errores.sipi
    ├── modulo_utilidades.sipi
    ├── usar_modulo.sipi
    ├── panel_con_pestanias.sipi
    ├── tres_en_raya.sipi
    ├── juego_obstaculos_moviles.sipi
    ├── agenda_contactos.sipi
    ├── sonido_generado.sipi
    ├── procesar_archivos_con_variables.sipi
    ├── funciones_nuevas_v11.sipi
    ├── inventario_json_csv.sipi
    ├── tienda_sin_html.sipi
    ├── formulario_contacto_web.sipi
    ├── plataformas_fisica.sipi
    ├── enemigos_ia_particulas.sipi
    ├── automatizacion_escritorio.sipi
    ├── galeria_imagenes.sipi
    ├── calculadora_con_cuadro.sipi
    ├── lista_dinamica_gui.sipi
    ├── lista_menu_dinamicos.sipi
    ├── panel_coordenadas_dinamicas.sipi
    ├── sprites_posiciones_dinamicas.sipi
    ├── funciones_recursivas.sipi
    ├── estructuras_recursivas.sipi
    ├── temporizadores.sipi
    └── enum_y_estructuras.sipi
```

## Roadmap (proximas versiones)

- Mas widgets (pestañas, menus desplegables).
- Empaquetado automatico de proyectos Android dentro de un contenedor Linux
  incluido, para no depender de WSL manual.
- Depurador paso a paso integrado en el editor visual.
- Libreria de sprites y sonidos de ejemplo incluida en el ZIP.
- Publicacion directa de sitios generados a internet (hosting con un clic).
- Modulos/importaciones entre archivos `.sipi`.

— NovaLab Corporation
