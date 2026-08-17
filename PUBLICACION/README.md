# SiPi - Código fuente (v41.24.0)

Este repositorio contiene **solo el código fuente de SiPi**: el
intérprete, el editor visual, la CLI, los ejemplos y la documentación.

## Qué NO está acá

El empaquetado Debian (`debian/`, reglas de `dpkg-buildpackage`, los
`.deb` ya construidos) se movió a un repositorio de empaquetado
aparte, para que este repo de código fuente no dependa de -ni se
mezcle con- un sistema de distribución en particular. Ver
`PACKAGING_VINARI.md` para el criterio de empaquetado, que sigue
siendo válido como referencia aunque los archivos `debian/` ya no
vivan acá.

## Lanzadores y herramientas de distribución (reorganizados, sin Debian)

Estos archivos existían en versiones anteriores del proyecto y se
habían perdido al separar el empaquetado Debian del código fuente —
quedan restaurados acá, **reorganizados fuera de cualquier carpeta
específica de un sistema de empaquetado**:

- **`pkg-assets/bin/`** — lanzadores para Linux/Mac (`sipi`,
  `sipi-editor`, `sipi-cli`, y los nuevos `sipi-kids`, `sipi-ia`,
  `sipi-ia-servidor`). Cualquier sistema de empaquetado (Debian,
  Flatpak, un `.pkg` de Mac, lo que sea) los puede instalar en
  `/usr/bin` o donde corresponda — no son específicos de ningún
  formato.
- **`pkg-assets/windows/`** — lanzadores `.bat` para Windows: `sipi.bat`,
  `sipi-editor.bat`, `sipi-cli.bat`, `sipi-kids.bat`, `sipi-ia.bat`,
  `sipi-ia-servidor.bat`. Cada uno busca primero el archivo fuente
  normal (`sipi.py`, `editor_sipi.py`) y si no lo encuentra (carpeta de
  publicación sin fuente) cae a la versión protegida
  (`sipi_protegido.py`, `editor_protegido.py`).
- **`pkg-assets/desktop/`** — entradas de escritorio Linux, ahora
  incluyendo `sipi-kids.desktop` además de `sipi-editor.desktop`.
- **`pkg-assets/man/`** — páginas de manual, ahora incluyendo
  `sipi-kids.1`, `sipi-ia.1`, `sipi-ia-servidor.1`.
- **`herramientas/proteger_codigo.py`** — genera las versiones
  "protegidas" para distribuir sin exponer el código fuente en texto
  plano (`sipi_protegido.py`, `editor_protegido.py`,
  `generar_exe_protegido.py`): compila cada archivo a bytecode real de
  Python y genera un loader mínimo que lo decodifica y ejecuta en
  tiempo real, con **comportamiento idéntico al original** — probado
  en vivo: mismo resultado exacto corriendo un programa con `sipi.py`
  y con el `sipi_protegido.py` generado. No es una protección
  criptográfica (alguien con un decompilador de bytecode puede
  reconstruir una aproximación del código), pero evita la copia/edición
  casual, que es el nivel de protección que tiene sentido para un
  lenguaje educativo. Vive fuera de `src/` para dejar claro que es una
  herramienta de build, no parte del lenguaje.
- **`src/generar_exe.py`** — estaba referenciado por el editor (botón
  "Compilar a ejecutable") pero faltaba en esta entrega; quedó
  restaurado: compila un `.sipi` puntual a un ejecutable independiente
  real vía PyInstaller, empaquetando el `.sipi` y el motor de SiPi como
  datos embebidos.

## Bug corregido: SiPi Kids y SiPi IA no se podían abrir

La causa: los archivos (`editor_sipi_kids.py`, `sipi_ia_agente.py`,
`sipi_ia_servidor.py`) existían en `src/`, pero nunca se habían creado
los lanzadores correspondientes en `pkg-assets/bin/` — solo estaban
los de `sipi`, `sipi-editor` y `sipi-cli`. Con eso, no había forma de
abrir SiPi Kids ni de usar SiPi IA por línea de comandos una vez
instalado el paquete, aunque el código funcionara perfecto corriéndolo
directo con `python3 archivo.py`. Ya están agregados los tres
lanzadores que faltaban (ver arriba).

## Estructura

- `src/` - código fuente:
  - `sipi.py` - intérprete/motor del lenguaje
  - `editor_sipi.py` - editor visual (Tkinter), con tutorial
    interactivo, galería de ejemplos rápidos, buscar/reemplazar,
    zoom de fuente, depurador, terminal integrado y más
  - `editor_sipi_kids.py` - editor por bloques para chicos
  - `logros_kids.py` - sistema de logros de SiPi Kids
  - `sipi_ia.py` - generación, auto-corrección y sesiones conversacionales con IA
  - `sipi_ia_agente.py` - orquestador multi-archivo y CLI/JSON para otras IAs
  - `sipi_ia_memoria.py` - índice de proyecto, búsqueda y refactor
  - `sipi_ia_biblioteca.py` - biblioteca de patrones reutilizables
  - `sipi_ia_servidor.py` - servidor HTTP de SiPi IA
  - `generar_exe.py` - compila un `.sipi` a ejecutable independiente
  - `sipi_cli.py` - CLI de gestión de proyectos
  - `lexer_sipi.py` / `ast_sipi.py` - lexer/parser reales
  - `sipi_lsp.py` - soporte de Language Server
- `examples/` - 47 programas de ejemplo, organizados en 10 categorías
- `docs/` - documentación
- `herramientas/` - `proteger_codigo.py` (build tool, ver más abajo)
- `pkg-assets/` - íconos, `.desktop`, man pages, completions, lanzadores
  Linux/Mac (`bin/`) y Windows (`windows/`) — insumos reutilizables por
  cualquier sistema de empaquetado, no específicos de Debian

## Novedades del editor en esta entrega (parte 1)

- **Tutorial**: panel interactivo con 6 lecciones progresivas
  (programa básico, números, condicionales, bucles, funciones,
  listas), cada una con botón "Probar en el editor" que carga el
  código de la lección en una pestaña nueva.
- **Ejemplos**: galería de recetas cortas (entrada de datos,
  `mientras`, listas + funciones, manejo de errores) para insertar
  con un clic.
- **Buscar** / **Reemplazar**: ahora también como botones de la
  barra de herramientas (antes solo por atajo de teclado).
- **A- / A+**: zoom rápido del tamaño de letra sin entrar al panel de
  Configurar, con aviso temporal en la barra de estado.

## Novedades del editor en esta entrega (parte 2)

- **Iconos propios**: se reemplazaron todos los emojis de la barra de
  herramientas por íconos vectoriales propios (`src/iconos_editor/`,
  generados a medida, sin depender de fuentes de emoji del sistema
  operativo). Cada botón tiene tooltip con su nombre y atajo.
  Separadores visuales agrupan botones por función (archivo /
  ejecución / herramientas / búsqueda / zoom / aprendizaje-IA).
- **Más atajos de teclado**: `Ctrl+N` nuevo, `Ctrl+O` abrir, `Ctrl+D`
  depurar, `Ctrl+Shift+F` formatear, `Ctrl+= / Ctrl+-` zoom, `F1`
  tutorial, `Ctrl+I` SiPi IA, `Ctrl+PgUp/PgDn` cambiar de pestaña.
- **SiPi IA** (botón nuevo, ícono de chip): panel de asistencia con
  IA integrado al editor. Ver sección dedicada más abajo.

## SiPi IA

Nuevo módulo (`src/sipi_ia.py`) y panel integrado al editor
(botón **SiPi IA** / `Ctrl+I`) para programar más rápido y resolver
errores con ayuda de un modelo de IA (Anthropic). No agrega
dependencias externas: usa `urllib` de la biblioteca estándar.

Cuatro modos, todos con el código resultante listo para insertarse en
una pestaña nueva de un clic:

1. **Generar código nuevo** a partir de una descripción en lenguaje
   natural ("un programa que pida 3 números y diga el promedio").
2. **Completar/extender lo que ya tengo**: toma el código actual del
   editor + una instrucción puntual ("agregale validación de que no
   sea negativo") y devuelve el programa completo ya integrado.
3. **Corregir el último error**: ejecuta el código actual en modo
   diagnóstico para conseguir el error real del motor, se lo pasa al
   modelo junto con el código, y devuelve el programa corregido con
   una explicación breve del bug.
4. **Explicar el código actual** en español simple, útil para
   aprender o para entender código ajeno.

La clave de API se pide una sola vez (o se toma de la variable de
entorno `ANTHROPIC_API_KEY`) y se guarda con permisos restringidos
(`0600`) en `~/.config/sipi/sipi_ia_config.json` — separada de la
configuración general del editor. `sipi_ia.py` también se puede usar
suelto desde la línea de comandos:

```sh
python3 src/sipi_ia.py "un programa que simule un cajero automático"
```

### Auto-corrección en loop (escribir → ejecutar → verificar → corregir)

Quinto modo del panel SiPi IA: **"Generar y auto-corregir (loop)"**.
En vez de confiar en que la IA acertó a la primera, el sistema:

1. Genera (o parte de) un programa.
2. Lo **ejecuta de verdad** contra el motor real de `sipi.py` (en un
   archivo temporal, con timeout).
3. Si tira error, se lo pasa al modelo junto con el código para que lo
   corrija.
4. Repite hasta 4 veces o hasta lograr una ejecución limpia.

El panel muestra el progreso intento por intento (qué código se probó,
si funcionó o no, y el error real si lo hubo), no solo el resultado
final — para que se vea el proceso de corrección, no una caja negra.
Implementado en `generar_con_auto_correccion()` dentro de
`sipi_ia.py`, reutilizable fuera del editor (mismo patrón que ya usás
en PiCi: escribir → ejecutar → corregir).

## SiPi IA Agente — para que otras IAs construyan software complejo en SiPi

Módulo nuevo: `src/sipi_ia_agente.py`. Es la capa que convierte a SiPi
IA en **herramienta principal para otras IAs** (Claude Code, cualquier
agente, cualquier script) que quieran construir software real y
complejo en minutos, no solo generar un archivo suelto.

**Por qué hace falta esta capa además de `sipi_ia.py`:** un pedido
complejo casi nunca es un archivo — es varios módulos con un plan
detrás. La forma de resolver la complejidad no es pedirle a un modelo
que genere todo de una sola pasada (ahí es donde a la mayoría de las
IAs se les complica y empiezan a alucinar sintaxis o perder el
contexto), sino **descomponerla**: planificar, generar cada parte por
separado con su propia auto-corrección, y verificar la integración al
final.

**Flujo completo (`construir_proyecto`):**

1. **Planificación** (`crear_plan`): antes de escribir código, le pide
   al modelo un plan de qué archivos hacen falta y qué hace cada uno
   — igual que un desarrollador senior diseña antes de programar.
   Como SiPi no tiene sistema de `importar` entre archivos, el plan
   está pensado para eso: dividir por responsabilidad, con
   `principal.sipi` siempre como punto de entrada.
2. **Construcción multi-archivo**: genera y auto-corrige cada archivo
   del plan contra el motor real (reutilizando
   `generar_con_auto_correccion` de `sipi_ia.py`), pasándole a cada
   archivo nuevo el contexto de los que ya se generaron, para mantener
   consistencia de estilo y nombres.
3. **Verificación de integración**: al terminar, corre el
   `principal.sipi` una vez más con todos los archivos del proyecto
   ya en su lugar.
4. Deja todo organizado en una carpeta de proyecto real, lista para
   abrir en el editor.

**Interfaz de herramienta para otras IAs** (`ejecutar_comando_json` /
modo CLI `--json`): cualquier agente externo puede invocar SiPi IA sin
conocer la API interna de Python, con comandos estructurados y
respuestas estructuradas — siempre JSON, nunca un traceback crudo:

```sh
python3 src/sipi_ia_agente.py --json '{
  "accion": "construir_proyecto",
  "objetivo": "un sistema de biblioteca con prestamos, devoluciones y multas por atraso",
  "carpeta": "/ruta/al/proyecto"
}'
```

Acciones soportadas: `generar_codigo`, `corregir_error`,
`auto_corregir`, `construir_proyecto`, `optimizar_codigo`,
`generar_pruebas`, `diagnosticar_error`, `crear_plan`. Cada una
devuelve `{"ok": true/false, ...}` con el detalle correspondiente.

**Capacidades adicionales** pensadas para que programar en SiPi con
ayuda de IA sea más completo, no solo más rápido:

- `optimizar_codigo`: reescribe un programa que ya funciona para que
  quede más prolijo (nombres claros, sin repetición), sin tocar el
  comportamiento.
- `generar_pruebas`: como SiPi no tiene framework de testing propio,
  genera un segundo programa SiPi que ejercita al primero con varios
  casos y reporta "OK"/"FALLO" comparando resultado esperado vs.
  obtenido.
- `diagnosticar_y_explicar_error`: separa diagnóstico de corrección —
  para cuando lo que hace falta es entender la causa del error, no
  necesariamente reescribir código todavía.

**Panel en el editor grande**: botón "Construir proyecto completo
(multi-archivo)" dentro del panel de SiPi IA (`Ctrl+I`), con el plan,
el progreso de cada archivo (intentos de auto-corrección incluidos) y
la verificación de integración mostrados en vivo.

## SiPi IA — sesiones conversacionales con memoria

Nueva clase `SesionIA` en `sipi_ia.py`: hasta ahora cada pedido a la
IA era una unidad aislada (descripción → código). Programar de verdad
es iterativo — "hacelo", después "agregale esto", después "cambiale el
nombre a esa variable" — y cada pedido nuevo necesita el CONTEXTO
COMPLETO de lo que se discutió antes, no solo el último mensaje.

- `sesion.pedir(mensaje)` manda el historial completo de la
  conversación (hasta 20 mensajes de contexto) en cada vuelta, y
  siempre devuelve el programa completo actualizado, no un fragmento.
- `auto_verificar=True` ejecuta el resultado contra el motor real y,
  si falla, pide una corrección extra antes de devolverlo.
- `sesion.deshacer()` vuelve a la versión de código anterior sin
  perder la memoria de la conversación (la IA sigue sabiendo que el
  usuario decidió volver atrás).
- `sesion.exportar()` / `SesionIA.desde_exportado()`: la conversación
  se puede guardar y continuar después — no se pierde al cerrar el
  editor.
- Integrada en `sipi_ia_agente.py` como acción `sesion_pedir`, con
  persistencia automática en disco (`.sipi_sesion_<id>.json` dentro de
  la carpeta del proyecto), así una IA externa puede mantener una
  conversación de refinamiento a lo largo de varias invocaciones
  separadas del CLI, cada una un comando JSON independiente.

## SiPi IA — memoria e índice de proyecto (`sipi_ia_memoria.py`)

Para que el agente maneje proyectos grandes sin tener que reenviar
todo el código de todos los archivos en cada pedido (caro, lento, y en
proyectos grandes ni siquiera entra en el contexto):

- **`IndiceProyecto`**: analiza todos los `.sipi` de una carpeta con
  regex livianas (sin gastar API) para extraer funciones, clases y
  variables globales de cada archivo, con cache en disco por hash de
  contenido — solo se re-analiza lo que cambió de verdad. Opcionalmente
  puede pedirle a la IA un resumen de una línea por archivo, también
  cacheado.
- **`contexto_resumido()`**: versión compacta del índice para pasarle
  a un prompt en vez del código completo — suficiente para que el
  modelo sepa qué hay en el proyecto antes de tocar un archivo puntual.
  `construir_proyecto` deja el proyecto indexado automáticamente al
  terminar.
- **`buscar(termino)`**: responde preguntas tipo "¿en qué archivo está
  la función que calcula el descuento?" sin mandarle el proyecto
  entero al modelo — busca en funciones, clases, variables globales,
  resúmenes y contenido de texto.
- **`renombrar_en_proyecto()`**: refactor real entre archivos —
  renombra una variable/función de forma consistente en todos los
  `.sipi` del proyecto a la vez, con reemplazo de palabra completa.
  Soporta **vista previa** (`aplicar=False`) antes de tocar nada.
- **`verificar_proyecto_completo()`**: corre todos los archivos del
  proyecto contra el motor real y devuelve el estado de cada uno — útil
  después de un refactor o un cambio grande, para saber de un vistazo
  si algo se rompió sin abrir archivo por archivo.
- Todo esto también expuesto como acciones del comando JSON del
  agente: `indexar_proyecto`, `buscar_en_proyecto`,
  `renombrar_en_proyecto`, `verificar_proyecto`.
- **Panel nuevo en el editor**: botón "Buscar / Refactor en el
  proyecto" dentro del panel de construcción multi-archivo, con
  pestañas de Buscar y Renombrar (esta última con vista previa
  obligatoria antes de aplicar, y confirmación explícita).

## SiPi IA — biblioteca de patrones (`sipi_ia_biblioteca.py`)

Acelera la generación y mejora la consistencia reutilizando soluciones
que **ya se verificaron que funcionan**, en vez de generar todo desde
cero cada vez:

- Cuando `construir_proyecto` genera un archivo con éxito, lo guarda
  automáticamente en una biblioteca compartida (persistente en
  `~/.config/sipi/sipi_ia_biblioteca.json`, entre proyectos distintos,
  no solo dentro de uno).
- Antes de generar un archivo nuevo, busca soluciones parecidas por
  palabras clave (coeficiente de Jaccard) — con un **stemming simple
  por truncamiento** para que conjugaciones distintas de una misma
  raíz matcheen entre sí (`validar`/`valida`/`validando` → `valid`),
  sin depender de ningún modelo de embeddings ni librería externa.
- Si encuentra una coincidencia fuerte, la usa como punto de partida
  para que el modelo la **adapte** al pedido nuevo, en vez de
  reinventar la rueda — más rápido, más barato, y con estilo
  consistente entre programas parecidos.
- Poda automática: si se acumulan más de 300 soluciones, descarta
  primero las menos usadas y más viejas, no solo por antigüedad.
- Expuesta como acciones `buscar_patrones` y `estadisticas_biblioteca`
  en el comando JSON del agente.

## SiPi IA — evaluación de calidad de código

`evaluar_calidad()` y `generar_con_calidad_garantizada()` en
`sipi_ia_agente.py`. `generar_con_auto_correccion` solo garantiza que
un programa **corra** sin error — pero correr sin error no significa
estar bien escrito. Este sistema reutiliza el **analizador estático
real que ya trae SiPi** (`sipi.py --revisar`, con categorías
seguridad/bugs/estilo/sugerencias) para calcular un puntaje objetivo
de 0 a 100 (ponderado: los hallazgos de seguridad penalizan mucho más
que uno de estilo), sin gastar ninguna llamada a la API — es análisis
estático local e instantáneo.

`generar_con_calidad_garantizada()` combina ambos mundos: primero
logra que el programa corra (auto-corrección de ejecución), y si el
puntaje de calidad queda por debajo de un mínimo configurable, le pide
al modelo que resuelva específicamente los hallazgos de seguridad y
bugs (no los de estilo, esos quedan a criterio) — revalidando siempre
contra el motor real antes de aceptar el arreglo, para que "mejorar la
calidad" nunca rompa "que funcione". `construir_proyecto` ya calcula y
reporta el puntaje de calidad de cada archivo que genera.

Acciones nuevas en el comando JSON: `evaluar_calidad`,
`generar_con_calidad`.

## SiPi IA — servidor HTTP (`sipi_ia_servidor.py`)

Todo lo anterior también accesible por **red**, no solo por CLI —
pensado para el caso en que quien va a usar SiPi IA como herramienta
principal es un agente de IA remoto o un panel que habla HTTP en vez
de lanzar procesos. Implementado con `http.server` de la biblioteca
estándar — sin Flask, sin dependencias:

```sh
python3 src/sipi_ia_servidor.py --puerto 8420
```

- `GET /salud` — chequeo simple de que el servidor está arriba.
- `GET /acciones` — catálogo de acciones disponibles con descripción,
  para que un agente que recién se conecta pueda "descubrir" qué puede
  pedir sin leer el código fuente.
- `POST /comando` — el mismo formato JSON del CLI del agente; devuelve
  HTTP 200 si `ok: true`, 422 si `ok: false` (nunca un traceback
  crudo).
- Por defecto escucha solo en `127.0.0.1` (esta misma computadora). Si
  se expone a la red con `--host 0.0.0.0`, exige (y avisa si falta) un
  `--token` que el cliente manda en el header `X-SiPi-Token` — sin
  eso, cualquiera en esa red podría gastar la clave de API configurada.
- **Panel en el editor**: botón "Servidor para otras IAs" en el panel
  de SiPi IA, para prender/apagar el servidor sin salir de la app, con
  generación automática de un token seguro (`secrets.token_hex`)
  cuando se habilita el acceso desde la red.

Probado en vivo end-to-end: `/salud`, `/acciones`, y `/comando` con y
sin clave de API configurada — responde siempre JSON estructurado con
el código HTTP correcto.

## SiPi Kids

Editor nuevo y completamente aparte: `src/editor_sipi_kids.py`.
Pensado para chicos o para cualquiera que recién arranca, sin tener
que memorizar sintaxis:

- **Paleta de bloques** (panel izquierdo, con íconos propios en
  `src/iconos_kids/`): Inicio, Decir algo, Preguntar y guardar, Número
  al azar, Si pasa esto..., Repetir varias veces, Lista de cosas. Cada
  bloque es un botón grande y colorido que inserta el fragmento de
  código SiPi correcto justo donde está el cursor, dejando el cursor
  listo en el lugar donde el chico tiene que completar el dato (el
  texto, la condición, la cantidad de veces).
- El área de código sigue siendo texto real y editable — no es un
  simulador aparte — y corre con el mismo motor `sipi.py` que el
  editor grande.
- Botón **¡Ejecutar!** gigante: en Linux/Mac corre el programa
  capturando la salida y mostrándola directo en un panel de
  "Resultado" al costado (sin tener que abrir una terminal aparte); si
  hay un error, se explica con un tono simple y se sugiere probar de
  nuevo o pedir ayuda a la IA.
- **Ayuda de la IA** simplificada: una sola caja de texto ("contá qué
  querés que haga tu programa") + un botón. Reutiliza `sipi_ia.py`
  con un prompt adaptado a alguien que recién empieza (código simple
  y comentado).
- El nivel de dificultad queda fijo en `#nivel principiante` (la
  directiva real que ya entiende `sipi.py`), así el propio intérprete
  avisa con mensajes claros si se usa algo más avanzado, en vez de un
  error técnico.
- Tipografía grande (Comic Sans MS), colores vivos, sin atajos de
  teclado que aprender ni menús escondidos.

Se abre como programa aparte:

```sh
python3 src/editor_sipi_kids.py
```

## Sistema de logros (SiPi Kids)

Módulo nuevo y separado, `src/logros_kids.py` — gamificación real y
persistente, no cosmética:

- **Progreso persistente**: se guarda en
  `~/.config/sipi/sipi_kids_progreso.json`, así los logros y
  estadísticas sobreviven entre sesiones.
- **9 logros** en el catálogo inicial, cada uno con una condición
  declarativa (una función que mira las estadísticas acumuladas, no un
  contador hardcodeado disperso por el código): primer programa,
  primer guardado, uso de cada tipo de bloque, 5 ejecuciones seguidas
  sin error, 10 programas en total, primer pedido a la IA, 25 usos de
  bloques, y la colección completa de tipos de bloque.
- **API independiente de la interfaz** (`registrar_evento(tipo,
  **datos)` devuelve la lista de logros nuevos desbloqueados), para
  poder reusarse si el editor grande o algún otro front-end quiere
  engancharse más adelante.
- **Notificaciones emergentes**: ventanita sin bordes arriba a la
  derecha que aparece 4 segundos al desbloquear un logro, sin
  interrumpir al chico en medio de escribir el programa.
- **Botón "Mis logros"**: vitrina con el catálogo completo — los
  logros ya conseguidos se muestran en color con su descripción; los
  que faltan se muestran en gris con ícono de candado y "???", para
  que se note que hay más por descubrir sin arruinar la sorpresa.
- Eventos ya enganchados en `editor_sipi_kids.py`: usar un bloque,
  ejecutar (con o sin error, incluyendo la racha), guardar un archivo,
  y pedirle algo a la Ayuda de la IA.
