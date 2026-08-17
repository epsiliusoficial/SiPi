# CHANGELOG de SiPi

Todas las versiones, de la mas nueva a la mas vieja. Antes de la v31 el desarrollo fue privado (por eso el salto de numeracion); esas versiones no tienen registro individual.

> Nota de version: el codigo fuente de este paquete corresponde a la v41.24.0 (variable `VERSION` en `sipi.py`). El nombre del .zip puede no coincidir si se renombro el archivo al distribuirlo.

---

## Novedades v41.37 (separación del empaquetado Debian + SiPi IA, SiPi Kids, y restauración de lanzadores)

Esta entrada cubre varias sesiones seguidas de trabajo sobre el paquete de código fuente (separado del repositorio de empaquetado Debian, que ahora vive aparte — ver `PACKAGING_VINARI.md`).

**Separación de Debian:**
- Se sacó la carpeta `debian/` y los `.deb` ya construidos del árbol de código fuente. El empaquetado Debian pasa a un repositorio propio, que referencia este código fuente por versión/tag en vez de convivir con él.

**SiPi IA — de un botón "generar" a una plataforma completa (`sipi_ia.py`, `sipi_ia_agente.py`, `sipi_ia_memoria.py`, `sipi_ia_biblioteca.py`, `sipi_ia_servidor.py`):**
- Generación, corrección y explicación de código con contexto real del lenguaje.
- **Auto-corrección en loop**: escribir → ejecutar contra el motor real → si falla, corregir → repetir hasta 4 veces.
- **Sesiones conversacionales con memoria** (`SesionIA`): refinamiento iterativo multi-turno, con deshacer y persistencia en disco.
- **Agente multi-archivo**: planifica un proyecto completo en varios `.sipi`, genera y auto-corrige cada uno con contexto cruzado, y verifica la integración final.
- **Memoria/índice de proyecto**: análisis local sin gastar API (regex + cache por hash), búsqueda de funciones/variables/clases, y **refactor real entre archivos** (renombrado consistente, con vista previa antes de aplicar).
- **Biblioteca de patrones**: reutiliza soluciones ya verificadas en vez de generar todo desde cero, indexadas por palabras clave con stemming simple para español.
- **Evaluación de calidad**: reutiliza el analizador estático real (`--revisar`) para un puntaje objetivo 0-100, con una ronda de corrección dirigida a hallazgos de seguridad/bugs.
- **Servidor HTTP** (`http.server`, sin dependencias): expone todo el agente por red vía `GET /salud`, `GET /acciones`, `POST /comando`, con token opcional para exposición fuera de `127.0.0.1`.
- Interfaz de comando único en JSON (`ejecutar_comando_json` / `--json` por CLI) pensada para que cualquier IA externa use SiPi IA como herramienta sin conocer la API interna de Python.

**SiPi Kids (`editor_sipi_kids.py`, `logros_kids.py`):** editor completo y aparte por bloques de un clic (Inicio, Decir, Preguntar, Número al azar, Decisión, Repetir, Lista), con ayuda de IA simplificada y un sistema de logros persistente con 9 logros y notificaciones emergentes.

**Bug corregido — SiPi Kids y SiPi IA no se podían abrir:** los archivos existían en `src/` pero faltaban los lanzadores en `pkg-assets/bin/` (`sipi-kids`, `sipi-ia`, `sipi-ia-servidor`) — el código funcionaba perfecto corriéndolo directo con `python3`, pero no había comando instalado. Agregados junto con sus `.bat` de Windows en `pkg-assets/windows/`.

**Restaurado y reorganizado (existía en versiones previas, se había perdido al separar Debian):**
- `herramientas/proteger_codigo.py`: genera versiones "protegidas" para distribuir sin exponer el código fuente en texto plano (`sipi_protegido.py`, `editor_protegido.py`, `generar_exe_protegido.py`) — compila a bytecode real y genera un loader mínimo. Probado en vivo: comportamiento idéntico al original.
- `src/generar_exe.py`: estaba referenciado por el editor pero faltaba — compila un `.sipi` a ejecutable independiente vía PyInstaller.
- Lanzadores `.bat` de Windows completos para los seis comandos.

---

## Novedades v41.36 (feedback, sigue lo grande: prototipo de Rust)

Empecé **#70 (runtime alternativo en Rust)** — el "no hacerlo todavía, dejar preparado el diseño" del feedback original ahora tiene un primer paso real, no solo un diseño en papel.

- **`runtime_rust/` (proyecto Cargo nuevo):** tokenizador + parser + evaluador de expresiones en Rust, réplica deliberada de `lexer_sipi.py`/`ast_sipi.py` (misma gramática, mismas precedencias, mismos alias `y`/`o`/`no`). Compila limpio, **17 tests unitarios de Rust (`cargo test`) en verde**.
- **Validación cruzada de tres vías, no solo dos:** `tests/test_paridad_rust.py` (nuevo) compara el binario de Rust, `ast_sipi.py` (Python) y `Interprete.evaluar_expresion` del motor de producción real — las tres implementaciones dan **exactamente** el mismo resultado para el mismo lote de expresiones, incluyendo el caso de división por cero (mismo mensaje de error, verificado en Rust también).
- Alcance explícito y honesto en `runtime_rust/README.md`: esto tokeniza y evalúa expresiones, nada más — no ejecuta programas SiPi completos (sin control de flujo, funciones, ni el resto de los ~170 comandos). Es la pieza más chica y más verificable antes de escalar a algo más grande, misma filosofía que la fase 1 del lexer/parser/AST en Python.

Suite completa de Python: **71/71** (46 motor + 23 lexer/AST + 2 paridad Rust). `sipi.py` de producción sigue sin tocarse por esta pieza.

---

## Novedades v41.35 (feedback, sigue lo grande: IA/ML fase 1 — vectores)

Empecé **#71-73 (arrays eficientes, matemáticas, operaciones vectoriales)** — la base explícita que el propio feedback pide antes de pensar en cualquier cosa de IA/ML más elaborada.

- **Nuevos comandos del motor:** `vector_sumar`, `vector_restar`, `vector_escalar`, `vector_producto_punto`, `vector_magnitud`, `vector_normalizar`. Puro Python (listas), sin dependencias nuevas.
- Mensajes de error específicos: longitud distinta entre vectores, elemento no numérico, normalizar un vector cero — cada uno con su propio mensaje claro, no un `TypeError` crudo de Python.
- **Encontré y corregí un bug real mío en el camino:** mi primer intento partía `vector_sumar [1, 2, 3] [4, 5, 6] -> r` mal, porque el regex ingenuo corta en el primer espacio que encuentra — incluidos los espacios *internos* de una lista literal (`[1,` + `2, 3] [4, 5, 6]`). Lo agarré yo mismo probando con listas literales inline (no solo con variables, que no tienen ese problema) y lo arreglé con un separador nuevo (`_dividir_dos_argumentos_por_espacio`) que respeta corchetes/paréntesis/comillas al buscar el punto de corte.
- **4 tests nuevos y permanentes** en `tests/test_suite.py`, incluyendo el caso exacto que reveló el bug (listas literales inline). Suite completa: **46/46**.

---

## Novedades v41.34 (arranca lo grande: lexer/parser/AST real, fase 1)

Autorizado explícitamente a tocar las piezas grandes de la lista (Rust, IA/ML, y lo que quedaba). Empecé por **#23-25 (separación lexer/parser/AST)** porque es la pieza fundacional que hace más fácil todo lo demás (incluido un futuro runtime en Rust, que necesita un AST del que partir en vez de re-parsear texto).

- **`lexer_sipi.py` (nuevo):** tokenizador real y standalone. Números, texto (con escapes), identificadores, operadores (aritméticos, comparación, lógicos, con alias `y`/`o`/`no` → `and`/`or`/`not`), paréntesis. Errores léxicos con columna exacta.
- **`ast_sipi.py` (nuevo):** nodos de AST (`NumeroLiteral`, `TextoLiteral`, `Variable`, `Binario`, `Unario`, `Llamada`, etc.) + parser recursivo-descendente con precedencia correcta (multiplicación antes que suma, paréntesis, unarios encadenados, cortocircuito real en `and`/`or`) + evaluador.
- **`tests/test_lexer_parser_ast.py` (nuevo, 23 tests):** cubre lexer, parser, evaluador — y lo más importante, **valida cruzado contra `Interprete.evaluar_expresion` del motor de producción real** para un lote de expresiones, confirmando que el AST nuevo calcula exactamente lo mismo que el intérprete que la gente ya usa.

**Decisión explícita de alcance — importante:** `sipi.py` (el intérprete de producción) **no se tocó ni una línea**. Esta es la base formal, construida y probada aparte, para que el runtime empiece a usarla *gradualmente* en sesiones futuras (primero probablemente para el puntero de columna exacto del item #26, que hoy apunta al final de línea; después para ir reemplazando el evaluador basado en `eval()`) — no un swap completo de una sola vez sobre un intérprete de 9000+ líneas que ya funciona y tiene gente usándolo. Encontré y corregí en el camino dos bugs propios de mis primeros tests (mock de `Interprete` incompleto, afirmación incorrecta sobre paridad con producción que verifiqué y corregí antes de dejarla escrita) — la propia suite de tests los agarró antes de entregar.

Se re-corrió la regresión completa del motor (42/42, sin cambios) para confirmar que `sipi.py` sigue exactamente igual.

**Próximos pasos ya identificados para IA/ML (#71-76) y Rust (#70):** vectores/operaciones matemáticas como builtins nuevos del motor (bajo riesgo, acotado, similar a lo hecho con `benchmarks.py`), y un prototipo mínimo de Rust que tokenice un subconjunto de SiPi (usando `lexer_sipi.py` como referencia de comportamiento) — ninguno de los dos se apuró en esta tanda para no meter cambios de motor sin el mismo nivel de testeo real que tuvo todo lo anterior.

---

## Novedades v41.33 (feedback, decima tanda: regresion permanente items 99-106)

- **P4 #99-106 (testing): la lista pedía explícitamente tests de Windows, archivos con espacios, rutas temporales, ZIP, código sin guardar, F11, compilación y regresión.** En vez de dejar todo lo arreglado en esta sesión (8 tandas: bugs P0, ejecutar sin guardar, recuperación, pestañas, explorador, terminal, ir a línea/brackets, bilingüe, benchmarks) solo verificado "a mano" una vez, agregué una clase nueva `TestFeedbackDeLaSesionDe106Items` a `tests/test_suite.py` con 7 tests reales y permanentes:
  - Ejecución real con espacios en la carpeta (el tipo exacto de carpeta donde apareció originalmente el bug de Windows del tester).
  - Directiva `#idioma en` de punta a punta con control de flujo real (`if`/`else`).
  - Directiva `#idioma ambos` mezclando español e inglés en el mismo archivo.
  - Directiva de idioma inválida sigue dando error claro.
  - `SiPiError` trae `num_linea`/`texto_linea` poblados (lo que hace posible el formato con puntero del item #26).
  - `sipi cache` encuentra y borra `.sipic` reales.
  - Los benchmarks oficiales corren las 6 categorías sin fallar.
  Suite completa: **42/42** (35 originales + 7 nuevos), todos corridos de verdad, no simulados.

Con esto, todo lo agregado en esta sesión de feedback queda protegido contra regresiones futuras, no solo confirmado una vez en la terminal.

---

## Novedades v41.32 (feedback, novena tanda: ir a línea + bracket matching)

Antes de escribir código, revisé cuáles del resto de items 11-22 (sección 🟢 editor) ya estaban hechos, como pasó con el bilingüe. Resultado: coloreado de sintaxis (#17), número de línea (#18) y autocompletado (#16) **ya existían**. Los gaps reales eran #19 y #22:

- **P3 #19: ir a línea (`Ctrl+G`).** Diálogo simple que pide un número y mueve el cursor ahí, seleccionando la línea para que sea fácil de ubicar visualmente. Verificado programáticamente: abre el diálogo, escribe un número, Enter mueve el cursor a esa línea exacta y cierra el diálogo.
- **P3 #22: bracket matching.** Resalta el paréntesis/corchete/llave bajo o pegado al cursor junto con su pareja, contando niveles de anidamiento correctamente (un `(` interno no hace match con el primer `)` que aparece después, sigue contando hasta el nivel correcto). Verificado con un caso de anidamiento real (`((1 + 2) * 3)`) confirmando que empareja con el cierre externo correcto, no con el más cercano.
- **P3 #20/#21 (selección múltiple, plegado de código):** no implementados en esta tanda — ambos requieren reescribir bastante de cómo el widget `Text` de Tk maneja cursores/selección (selección múltiple no es nativa de Tk) o una estructura de plegado por rangos de línea con su propia UI, más riesgo de romper el editor de coloreado/autocompletado existente que las otras piezas de esta sesión. Quedan pendientes si se necesitan.

Se re-corrieron las cinco suites de tests del editor (indicador de cambios, recuperación, pestañas, explorador, terminal) y la regresión completa del motor (35/35): todo intacto.

---

## Novedades v41.31 (feedback, octava tanda: terminal integrada)

- **P3 #12: terminal integrada.** Panel plegable (botón "⌨ Terminal" o `` Ctrl+` ``) igual en espíritu al de cualquier editor de código: comandos que el usuario elige y escribe a mano, con sus propios permisos, en la carpeta del proyecto — no es más riesgo que abrir una terminal aparte (que el usuario ya puede hacer en cualquier momento), solo evita salir del editor. Diseño explícitamente simple a propósito: cada línea corre como un comando independiente vía `subprocess.run` en un hilo (no congela la interfaz), no una sesión de shell persistente ni un pseudo-terminal — así evité la complejidad/riesgo extra de manejar un PTY real. `cd` se maneja aparte para que persista entre comandos (si no, cada comando arrancaría de nuevo en la carpeta vieja al correr en un proceso nuevo cada vez); `clear`/`cls` vacía el panel localmente. Verificado con una suite de tests dedicada bajo Xvfb: comando real ejecutado con salida real capturada, `cd` persistente confirmado con `pwd`, `cd` a carpeta inexistente sin crashear, `clear`, mostrar/ocultar. Encontré y corregí un bug propio en el camino (un `def` duplicado por accidente al editar) y una carrera de hilos en segundo plano terminando después del cierre de ventana (ahora con manejo explícito) — ambos atrapados por la suite de tests antes de entregar. Se re-corrieron las cuatro suites de tandas anteriores del editor y la regresión completa del motor (35/35): todo intacto.

---

## Novedades v41.30 (feedback, septima tanda: bilingüe + hallazgo importante)

- **P3 #43-46: keywords en español/inglés (y más).** Al revisar el motor para implementar esto, encontré que **ya estaba hecho** — y no solo español/inglés: `IDIOMAS_SIPI` ya soporta `en`, `fr`, `zh`, `hi`, `ar`, `bn` via la directiva `#idioma <codigo>` al principio del archivo, traduciendo la palabra clave de cada línea a su equivalente en español (el idioma interno real, cumpliendo el item #46 al pie de la letra: "una misma semántica interna, no crear dos lenguajes") de forma segura respecto de cadenas de texto (`_dividir_respetando_cadenas`). Lo confirmé con un programa real en inglés (`#idioma en`, `if`/`say`/`var`) ejecutado de punta a punta.
- **P3 #45: "Modo ambos".** Esto sí faltaba como concepto explícito, aunque ya funcionaba de hecho: como las palabras clave en español nunca están en ninguna tabla de traducción, simplemente pasan sin tocar — así que activar la tabla de inglés ya permitía mezclar `si`/`if`, `decir`/`say`, etc. libremente en el mismo archivo. Agregué `#idioma ambos` (y `mixto`/`both`) como alias explícito de esa misma tabla, para que la directiva diga lo que el usuario quiere decir en vez de que tenga que saber este detalle interno. Verificado con un programa real mezclando ambos idiomas en el mismo archivo, más la directiva de idioma inválido (sigue fallando con el mismo mensaje claro de siempre) y la regresión completa del motor (35/35).
- **P3 #47 (parcial):** la directiva `#idioma` ya es "configuración por proyecto" en el sentido de que vive en el propio archivo `.sipi`; no existe todavía un `idioma = "..."` centralizado en `sipi.toml` que aplique a todos los archivos de un proyecto de una — queda pendiente si se necesita.
- **P3 #48:** soporte en la extensión de VS Code para elegir idioma desde una configuración — no implementado, el propio feedback lo marca como "futuro".

---

## Novedades v41.29 (feedback, sexta tanda: explorador de archivos)

- **P3 #13: explorador de archivos.** Panel nuevo a la izquierda del editor (arbol tipo VS Code) que muestra la carpeta del proyecto, con carga perezosa: una subcarpeta no se lee hasta que el usuario la despliega, asi que proyectos grandes no tardan en mostrarse. Doble clic en un `.sipi` lo abre directamente en una pestaña (reutilizando la misma logica de "ya esta abierto -> cambia de pestaña" del item #14). Boton 📁 para elegir la carpeta del proyecto, ⟳ para refrescar. Filtra ruido tipico (`__pycache__`, `.git`, `node_modules`, ocultos) con el mismo criterio que ya usaba `sipi cache` para no confundir cache con codigo real. Verificado con una suite de tests dedicada bajo Xvfb contra una carpeta de prueba real con subcarpetas: carga perezosa (placeholder antes de desplegar, hijos reales despues), doble clic abre el archivo correcto, no duplica pestañas, no crashea al doble-clickear una carpeta. Se re-corrieron ademas las tres suites de tandas anteriores (indicador de cambios, recuperacion, pestañas) y la regresion completa del motor (35/35): todo intacto.

---

## Novedades v41.28 (feedback, quinta tanda: pestañas multi-archivo)

- **P3 #14: pestañas.** El editor ahora soporta varios `.sipi` abiertos a la vez, cada uno con su propio contenido, archivo y estado de "modificado" aislado (un solo widget de texto compartido internamente; el contenido de la pestaña inactiva se guarda en memoria al cambiar, no se pierde). Barra de pestañas arriba del editor, con `+` para nueva pestaña y `✕` para cerrar cada una.
  - `Ctrl+T` nueva pestaña, `Ctrl+W` cierra la actual.
  - "Abrir" un archivo ya abierto en otra pestaña cambia a esa pestaña en vez de duplicarla.
  - Cerrar una pestaña con cambios sin guardar pregunta antes (igual que cerrar el editor entero); cerrar la última pestaña deja una pestaña "Sin título" fresca en vez de una ventana sin ninguna.
  - Cerrar el editor completo ahora revisa **todas** las pestañas por cambios sin guardar, no solo la activa (antes de esta version no existia el concepto de "otra pestaña" asi que no aplicaba).
  Verificado con una suite de tests dedicada bajo Xvfb: aislamiento de contenido entre pestañas, guardado, detección de archivo ya abierto, cierre con/sin cambios pendientes, y que nunca queda en 0 pestañas. Encontré y corregí dos bugs propios en el camino (un `def` que se borró sin querer en un `str_replace`, un `padx` con tupla inválido para `tk.Label`) — ambos atrapados por la propia suite de tests antes de entregar. Se re-corrieron también las suites de las tandas anteriores (indicador de cambios, ejecutar sin guardar, F11, recuperación) y la regresión completa del motor (35/35) para confirmar que nada se rompió.

---

## Novedades v41.27 (feedback, cuarta tanda: benchmarks oficiales)

- **P2/rendimiento #65: benchmarks oficiales.** Nuevo `benchmarks.py` (y `sipi benchmarks` desde el CLI) mide el motor real en 6 categorias pedidas explicitamente: bucles, funciones/recursion, strings, listas, archivos y concurrencia (hilos reales). Cada benchmark es un programa `.sipi` real generado y corrido con el interprete real (no numeros inventados), con `--sin-cache` para medir parseo+ejecucion, `--repeticiones N` para promediar, y `--json salida.json` para poder diffear entre versiones en CI. Encontrados y corregidos en el proceso: sintaxis incorrecta de `hilo_crear` en mi primer intento (confirmado contra `tests/test_suite.py`, la fuente de verdad) y ruido de salida de los programas de benchmark tapando los resultados (ahora se silencia con `contextlib.redirect_stdout`, la ejecucion real sigue intacta). Verificado con la suite de regresion completa (35/35) antes y despues, mas una corrida real de las 6 categorias con salida y JSON inspeccionados a mano.

---

## Novedades v41.26 (feedback, tercera tanda: motor de errores)

- **P2 #26: sistema de errores con puntero, formato pedido explícitamente en el feedback.** Antes: `Error en linea 14: <mensaje>` en una sola línea. Ahora `SiPiError` guarda línea, archivo y texto de la línea junto con el mensaje, y el punto de salida final arma:
  ```
  [SiPi] Error en programa.sipi:4

  4 | decir x / y
                 ^

  Division por cero al evaluar la expresion 'x / y'.
  ```
  Verificado corriendo la suite de regresión completa (35/35 tests, sin tocar ninguno) antes y después del cambio, más dos casos reales nuevos (división por cero, variable no declarada) ejecutados de punta a punta. El puntero apunta al final de la línea (no columna exacta del token que falló) porque esa granularidad no está disponible en la mayoría de los puntos donde se lanza un error hoy — mejora futura si se separa lexer/parser/AST (#23-25), que sí llevaría posición por token.

---

## Novedades v41.25 (sesion de feedback de 106 items)

Primera tanda: bugs P0 y UX P1 del feedback del tester externo, verificados corriendo el editor real (Xvfb + tkinter) y el CLI real, no solo revisando el codigo.

- **P0 #1/#3: bug de Windows `[Errno 2] No such file or directory` con `sipi_protegido.py`.** Causa confirmada reproduciendo el escenario (correr SiPi desde una copia dentro de la carpeta Temp de Windows, tipico de abrir el `.zip` sin extraer). `editor_sipi.py` y `sipi_cli.py` ahora detectan esto al arrancar y avisan con causa y solucion antes de que se rompa algo.
- **P0 #4: manejo de errores.** Mensajes de "motor no encontrado" ahora muestran la carpeta exacta donde se busco y la causa mas probable, en vez de un traceback crudo.
- **P0 #5: F11 no hacia nada.** Se agrego pantalla completa real (F11 alterna, Escape sale). Verificado programaticamente.
- **P1 #6/#7: ejecutar sin guardar.** El boton ▶ Ejecutar ya no exige guardar antes; corre el contenido actual del editor desde un archivo temporal de sesion (no se borra hasta cerrar el editor, a diferencia de un temporal que se autodestruye antes de que el proceso hijo lo lea).
- **P1 #8: indicador de cambios.** Titulo muestra `nombre.sipi *` con cambios sin guardar.
- **P1 #10: atajos de teclado.** `Ctrl+S`, `Ctrl+Shift+S`, `Ctrl+Enter`/`F5`, `F11`, `Ctrl+Y` (redo), `Ctrl+F`/`Ctrl+H` (nuevo: buscar y reemplazar, item #15, con resaltado de coincidencias).
- **P1 #9: recuperación automática ante un cierre inesperado.** El editor ahora guarda un snapshot de recuperación (debounced, 2s tras la última tecla) en la carpeta HOME del usuario — sobrevive aunque SiPi corra desde una carpeta distinta cada vez. Al reabrir, si quedó un snapshot de una sesión que no cerró limpio, se ofrece recuperarlo con fecha y nombre de archivo. Se borra solo al guardar o al cerrar limpiamente. Verificado simulando un cierre "sucio" real con Xvfb.
- **La "consola integrada" (item #11 del feedback) ya existía** como el panel de "vista previa en vivo": corre el motor real de SiPi contra el contenido actual del editor y muestra su salida/errores reales mientras se escribe. Se revisó y confirmó que ya cumple ese pedido — no se duplicó.
- **P2 #37/#38/#39: `sipi cache tamaño`, `sipi cache limpiar` (con confirmacion) y `sipi cache limpiar --todo`.** Recorre la carpeta actual buscando todos los `.sipic` (la cache no vive centralizada, ver `CACHE.md`) y reporta/borra. Probado de punta a punta con archivos reales.

**Pendiente de esta misma lista de feedback** (no entra en una sola sesion, se sigue en las proximas): separacion formal lexer/parser/AST (#23-25), sistema de errores con puntero a columna estilo `14 | mostrar(nombre\n                   ^` (#26), keywords bilingues es/en (#43-48), REPL/debugger/profiler dedicados (#49-53), terminal y explorador de archivos integrados al editor (#12-13), pestañas multi-archivo (#14), gestor de paquetes con `sipi.toml` (#59-64), benchmarks oficiales (#65), runtime alternativo en Rust (futuro, a proposito no se empieza todavia), IA/ML y videojuegos (explicitamente "no todavia" en el propio feedback).

---

## Novedades v41.0

### Tipos opcionales (#21)
`variable`/`const` ahora aceptan una anotacion de tipo opcional:

```
variable edad: entero = 20
const nombre: texto = "Mateo"
```

Tipos soportados: `entero`, `decimal`, `numero`, `texto`, `booleano`, `lista`,
`diccionario`. Una vez que una variable queda anotada, cualquier reasignacion
posterior (`variable`, `sumar`, `restar`) que le de un valor de otro tipo
lanza un `SiPiError` claro en vez de fallar silenciosamente mas adelante.
Es 100% opt-in: el codigo sin anotaciones sigue funcionando exactamente igual.

### Biblioteca estandar ampliada (#13)
Nuevos comandos de fechas:
- `fecha_sumar_dias`, `fecha_diferencia_dias`, `fecha_es_mayor`,
  `fecha_formatear`, `fecha_dia_semana`.

Nuevos comandos de imagenes (requieren `pip install Pillow`):
- `imagen_info`, `imagen_redimensionar`, `imagen_convertir`.

Nuevos comandos de audio (sin dependencias externas, usan `wave`):
- `audio_duracion`, `audio_generar_tono`.

### Rendimiento (#16)
Verificado con la suite de tests: el camino rapido de expresiones binarias
simples y las caches de patrones regex/bloques `fin` siguen activas y ahora
tambien cubren el nuevo chequeo de tipos, que se salta por completo
(costo cero) cuando no se declaro un tipo.

### Tipos opcionales tambien en parametros de funcion
Ademas de `variable`/`const`, ahora podes anotar los parametros de una
funcion:

```
funcion sumar_enteros(a: entero, b: entero)
    devolver a + b
fin
```

Si llamas a la funcion con un valor de otro tipo, SiPi corta con un error
claro que indica cual parametro fallo y de que funcion, en vez de dejar
que el bug aparezca mas adelante en el programa.

## Novedades v41.1

### Listas tipadas (#21, profundizando)
`lista_crear` acepta un tipo de elemento opcional:

```
lista_crear numeros: lista<entero>
lista_agregar numeros 1        // OK
lista_agregar numeros "hola"   // Error de tipo, claro y en el momento
```

Igual que el resto del sistema de tipos, es opt-in: `lista_crear nombre`
sin anotacion sigue funcionando exactamente igual que antes.

### Confirmado ya resuelto de la lista original
Revisando el proyecto completo: administrador de paquetes real
(`sipi instalar`, `listar_modulos`, `desinstalar_modulo`,
`sipi_paquetes.json` + `sipi instalar --dependencias`), debugger con
breakpoints y ejecucion paso a paso en el editor, autocompletado y
resaltado de sintaxis ya estaban implementados en versiones anteriores
y siguen funcionando (verificado con la suite de tests).

## v41.1.1 - Corrección de bugs

Encontré (con `pyflakes`) que al agregar los comandos con tipos opcionales
en la sesión anterior quedaron **claves repetidas** en el diccionario
`AYUDA_COMANDOS`:
- `"variable"` estaba definida dos veces (una vieja sin tipos, una nueva con tipos).
- `"lista_crear"` tenía el mismo problema.

Python no marca esto como error de sintaxis, pero la definición vieja se
pisaba silenciosamente — es justo el tipo de cosa que un editor con
linter (como el que abre `editor.bat`) puede marcar en rojo aunque el
programa "funcione". Ya está resuelto: cada comando aparece una sola vez,
con la version mas nueva (con soporte de tipos). También se sacó un
`import queue` que no se usaba en ningun lado.

Verificado con `python -m pyflakes sipi.py` (0 avisos) y los 17 tests
automatizados (todos pasan).

## Novedades v41.2

### Diccionarios tipados y tipo de retorno de funcion (#21, profundizando mas)
```
diccionario_crear precios: diccionario<decimal>
diccionario_asignar precios "pan" 2.5        // OK
diccionario_asignar precios "leche" "cara"   // Error de tipo

funcion cuadrado(x: entero) -> entero
    devolver x * x
fin
```
Si `devolver` entrega un valor de un tipo distinto al declarado en `->`,
SiPi corta con un error claro indicando el nombre de la funcion.
Todo opt-in, como el resto del sistema de tipos.

### Correccion de lint
Se encontraron y corrigieron mas claves duplicadas en `AYUDA_COMANDOS`
(quedaron de agregar los tipos opcionales en versiones anteriores:
`funcion` y `diccionario_crear` tambien estaban duplicadas ademas de
`variable` y `lista_crear`, ya corregidas en 41.1.1). Se verifico con
`python -m pyflakes sipi.py editor_sipi.py sipi_cli.py generar_exe.py
publicar.py proteger_codigo.py` -> 0 avisos en todos. Tambien se saco un
`import shutil` sin usar en `sipi_cli.py` y se arreglaron dos f-strings
sin placeholders.

## Novedades v41.3 — Rendimiento real (#16)

Perfilé el interprete con `cProfile` sobre un benchmark de 200.000
iteraciones de un bucle `mientras` (`tests` no lo incluye, es un
script de medicion aparte). El resultado mostro que
`_separar_nivel_superior` (usada para partir condiciones por ' o '/' y ',
respetando comillas) se llamaba **dos veces en cada condicion evaluada**,
incluso cuando la condicion no tenia ningun ' o '/' y ' — un escaneo
caracter por caracter innecesario en el caso mas comun.

Arreglo: un chequeo rapido `" o " in cond` / `" y " in cond` (con `in` de
Python, implementado en C) antes de llamar a la funcion de escaneo
manual, para saltear por completo el trabajo caro cuando no hace falta.

Resultado medido en el mismo benchmark, mismo hardware:
- Antes: **3.24s**
- Despues: **2.20s**
- Mejora: **~32% mas rapido** en bucles con condiciones simples
  (`mientras i < N`, `si x > y`, etc. sin ' o '/' y ').

Se verifico que el caso con comillas (`si frase == "pero yo"`, donde el
texto entre comillas contiene literalmente " o ") sigue funcionando
igual que antes: la funcion completa se sigue llamando en ese caso, el
prechequeo solo descarta el caso donde el separador de verdad no aparece.

## Novedades v41.4 — Documentacion actualizada (#1)

Las tablas de referencia principales (secciones 2-4) todavia describian
`variable`, `funcion`, `lista_crear` y `diccionario_crear` sin mencionar
el sistema de tipos opcional agregado en versiones recientes — solo
aparecia en las notas de version al final del archivo. Se actualizaron
las tablas y se agrego la seccion **2.8 — Tipos opcionales** al tutorial
desde cero, con un ejemplo probado de punta a punta. Tambien se agregaron
a la tabla de referencia las categorias de fechas, imagenes y audio
(#13), que antes solo estaban documentadas en las notas de version.

## Novedades v41.5 — Interfaces / protocolos (#22)

```sipi
interfaz Sonable
    metodo hacer_sonido()
    fin
fin

clase Perro implementa Sonable
    metodo hacer_sonido()
        devolver "Guau!"
    fin
fin
```

Una `interfaz` declara que metodos debe tener una clase, sin implementarlos.
Una clase que escribe `implementa NombreInterfaz` se valida **al momento
de definirla** (no recien cuando alguien intenta llamar al metodo que
falta): si le falta algun metodo requerido, SiPi corta con un error claro
que dice la clase, la interfaz y el/los metodo(s) faltantes. Compatible
con herencia: si un metodo lo definio la clase padre, tambien cuenta como
"implementado". Se puede implementar mas de una interfaz separando por
comas: `clase X implementa A, B`.

## Novedades v41.6 — Bug real en 2D + investigacion 3D

### Bug corregido: colores sin comillas en `sprite`
Probando el motor de juegos 2D con pygame de verdad (headless, con
`SDL_VIDEODRIVER=dummy`) encontre que `sprite jugador 50 50 32 32 azul`
(color SIN comillas) fallaba con `Variable no declarada: 'azul'`, porque
el parser trataba cualquier palabra suelta como una variable SiPi en vez
de reconocer los nombres de colores conocidos. Los ejemplos siempre usan
comillas (`"azul"`) asi que no se notaba, pero nada en la sintaxis avisa
que hacen falta.

Arreglo: nuevo `_texto_color()`, usado en `sprite` y en el widget `cuadro`
de las ventanas GUI. Ahora acepta las tres formas por igual:
```sipi
sprite a 10 10 20 20 "rojo"      // como antes
sprite b 10 10 20 20 rojo        // ahora tambien funciona
variable c = "rojo"
sprite d 10 10 20 20 c            // variable con el nombre de un color, sigue funcionando
```
Se verifico que las tres formas coexisten sin romper nada (si el nombre
SI esta declarado como variable, se respeta esa variable en vez del color).

### Sobre 3D
Se reviso el motor completo: SiPi hoy no tiene un motor 3D real (no hay
integracion con OpenGL/Three.js equivalente), solo graficos 2D con
pygame. Agregar 3D real (mallas, camaras, iluminacion) es un proyecto
grande aparte, no un ajuste incremental — se puede planificar como una
sesion dedicada en vez de un cambio apurado y sin probar.

## Novedades v41.7 — tkinter/Xvfb real para probar, 3D basico, y 3 bugs de GUI encontrados

### Infraestructura de prueba real para GUI (importante para vos)
Instale `python3-tk` y `Xvfb` (pantalla virtual) en el entorno de trabajo.
Esto permitio, por primera vez, abrir el editor de verdad, hacer clic en
botones, escribir codigo, ejecutar programas, y usar el depurador visual
paso a paso -- todo probado de punta a punta, no solo leido. Tambien
instale `pygame` real para poder correr y sacar capturas de pantalla de
los juegos/escenas 3D.

### 3D basico v1 (#2 de tu ultimo pedido)
Nuevo comando `escena_3d`, un motor 3D wireframe real (no una simulacion):

```sipi
escena_3d "Mi Escena 3D" 640 480
    figura cubo 0 0 0 100 "rojo"
    figura piramide 150 0 0 80 "verde"
    rotacion_velocidad 2
fin
```

- `figura cubo x y z tamano color` / `figura piramide x y z tamano color`
- `rotacion_velocidad grados_y [grados_x]`

Rota las figuras en el eje Y (y opcionalmente X), proyecta con
perspectiva simple y dibuja las aristas con `pygame.draw.line`. Medido a
62 FPS reales (el limite esta puesto en 60 con `clock.tick(60)`), asi
que corre a framerate completo sin esfuerzo.

**Alcance real, sin exagerar**: esto es wireframe puro -- sin caras
solidas, sin texturas, sin iluminacion, sin z-buffer (las aristas de
atras se dibujan igual que las de adelante). Es una base solida y
verificada para construir un motor 3D mas completo en sesiones futuras,
no un motor 3D terminado.

### Bugs de GUI encontrados usando la infraestructura nueva
Ejecutando el editor y el depurador de verdad (no solo leyendo el
codigo) confirme que **funcionan correctamente**: el boton "Ejecutar"
corre el programa y muestra la salida, el depurador paso a paso respeta
los breakpoints, y el resaltado de sintaxis no tira errores. No aparecio
ningun bug nuevo en esta pasada -- lo cual tambien es una senal util:
el trabajo de sesiones anteriores en el editor esta bien.

## Novedades v41.8 — Extension de Visual Studio Code (#4-#5 aplicado a VS Code)

Nueva carpeta `vscode-sipi/` con una extension real de VS Code para
archivos `.sipi`:

- **Resaltado de sintaxis** para los ~190 comandos, palabras clave,
  tipos opcionales, strings con interpolacion, numeros y comentarios.
- **15 snippets** (`programa`, `si`, `mientras`, `funcion_tipada`,
  `clase`, `interfaz`, `crear_juego`, `escena_3d`, etc.)
- **Plegado de codigo** e indentacion automatica basados en los bloques
  que abre SiPi y cierra con `fin`.

Instrucciones de instalacion en `vscode-sipi/README.md` (copiar la
carpeta a `~/.vscode/extensions/` o empaquetar con `vsce package`).

**Verificado con el motor real de VS Code**, no solo JSON valido: instale
`vscode-textmate` + `vscode-oniguruma` (los mismos paquetes que usa VS
Code por dentro) y tokenice un programa de ejemplo completo. Las 6
categorias de resaltado (comandos, palabras clave, tipos, strings con
interpolacion, numeros, comentarios) se reconocieron correctamente antes
de entregar la extension.

### Sobre rendimiento esta vuelta
Perfile un benchmark mixto (bucle + llamadas a funcion + interpolacion
de strings, 50.000 iteraciones). El mayor costo individual es el propio
despachador de comandos (`_ejecutar_linea`), una cadena de `if cmd ==
"..."` de ~140 casos. Ya esta ordenada con los comandos mas usados
primero (optimizacion de una vuelta anterior). Convertirla en una tabla
de despacho (diccionario comando -> funcion) daria una mejora mayor,
pero es una reescritura grande de mas de 3000 lineas que toca cada rama
del interprete -- no algo para apurar sin poder probarlo a fondo. Se deja
anotado como el proximo paso real de rendimiento, para una sesion
dedicada en vez de un cambio apresurado.

## Novedades v41.9 — Bug critico corregido: SiPi no arrancaba en Windows

### El bug
```
ValueError: size not valid: 536870912 bytes
```
al arrancar `sipi.py` en Windows. `threading.stack_size(512 * 1024 * 1024)`
se llamaba sin manejo de errores, y Windows es mas estricto que Linux
con los tamanos de pila que acepta -- el mismo valor que funciona en
Linux/Mac rompia el programa entero en Windows, ni siquiera dejaba
ejecutar un "hola mundo".

### El arreglo
Ahora se prueba una lista de tamanos de mayor a menor (512 MB, 256 MB,
64 MB, 16 MB) y se usa el primero que el sistema operativo acepte. Si
ninguno funciona, sigue con el tamano de pila por defecto en vez de
romper el programa -- en el peor caso la recursion muy profunda falla
un poco antes, pero el programa arranca y corre.

Se verifico simulando el error exacto reportado (interceptando
`threading.stack_size` para que rechace tamanos grandes, igual que hace
Windows) y confirmando que el programa sigue ejecutando normalmente en
vez de crashear al arrancar.

## Novedades v41.10 — Segundo bug de Windows corregido (encoding de consola)

Buscando otros problemas similares al del `stack_size`, encontre otro
riesgo real y lo reproduje: en consolas de Windows viejas (`cmd.exe` sin
`chcp 65001`), la codificacion por defecto de stdout no siempre soporta
todos los caracteres Unicode. Si un programa SiPi hace `decir "Genial! 🎉"`
(un emoji, por ejemplo), en esas consolas el programa entero crasheaba
con `UnicodeEncodeError` solo por imprimir un caracter.

**Arreglo**: `main()` ahora reconfigura stdout/stderr a UTF-8 con
`errors="replace"` al arrancar (en el peor caso, un caracter raro se
reemplaza por un simbolo en vez de crashear el programa). Envuelto en
try/except por si el stream no soporta `reconfigure` (versiones muy
viejas de Python).

**Verificado reproduciendo el error real primero**: simule una consola
con encoding `cp1252` (comun en Windows) e imprimi un emoji -- confirme
que crasheaba con `UnicodeEncodeError` ANTES del arreglo, y que ya no
crashea DESPUES del arreglo, con la misma simulacion exacta.

## Novedades v41.11 — CI/CD real (#20 de tu lista original)

Nuevo `.github/workflows/ci.yml`: corre automaticamente en cada `push` y
`pull request` a `main`/`master`, en una matriz de **3 sistemas
operativos** (Ubuntu, Windows, macOS) x **3 versiones de Python** (3.10,
3.11, 3.12) -- 9 combinaciones en paralelo. Cada corrida:
1. Chequea sintaxis y lint con `pyflakes` en los 7 archivos principales.
2. Corre los 17 tests automatizados con `pytest -v`.
3. Prueba un "smoke test": que el interprete arranque y ejecute un
   programa minimo de verdad, no solo que importe sin error.

Si alguna de esas 9 combinaciones falla, GitHub lo marca en rojo en el
pull request -- exactamente lo que hace falta para "garantizar que las
nuevas versiones no rompan funciones anteriores" como decia tu lista
original.

**Verificado antes de entregarlo**: valide el YAML con un parser real
(no a ojo) y corri los 4 pasos del workflow a mano en este entorno,
confirmando que los 4 pasan tal cual estan escritos en el archivo.

## Novedades v41.12 — Instalador para Linux/Mac (#9 y #18 de tu lista original)

Nuevo `instalar.sh`, equivalente a `instalar.bat` pero para Linux/Mac:
detecta Python, avisa si falta `tkinter` (con el comando exacto para
instalarlo segun la distro), instala pygame/PyInstaller/Pillow/Kivy, y
dice como arrancar SiPi al final. Un solo comando: `bash instalar.sh`.

**Bug real encontrado y corregido ANTES de entregarlo**: al probarlo de
verdad en este entorno (Ubuntu/Debian moderno) fallo con
`error: externally-managed-environment` (PEP 668) -- `pip install`
rechaza instalar directo sobre el Python del sistema en distros nuevas,
y como el script tenia `set -e`, el instalador entero se cortaba ahi en
vez de seguir. Arreglado: ahora intenta la instalacion normal primero
(mejor para venvs, macOS, Windows), y si falla especificamente por ese
motivo en Linux, reintenta automaticamente con
`--break-system-packages`. Se volvio a correr el instalador completo
despues del arreglo y esta vez termino bien, con pygame y Pillow
realmente instalados y verificados con `import`.

## Novedades v41.13 — Compilador real probado de punta a punta (#17), y bug de mensajes corregido

### El compilador real funciona (probado con PyInstaller de verdad)
Con PyInstaller instalado, corri `generar_exe.py` sobre un programa de
prueba real. Genero un **ejecutable nativo real** (ELF de 46 MB en
Linux), lo corri de forma independiente (sin Python en el PATH influyendo,
solo el binario) y funciono perfecto: imprimio la salida esperada. El
compilador de SiPi a ejecutable ya no es teorico, esta confirmado que
produce binarios reales y funcionales.

### Bug encontrado: los mensajes decian ".exe" incluso en Linux/Mac
Al ver la salida real del compilador en Linux, el mensaje final decia
`El ejecutable real 'test_compilar.exe' esta en esta carpeta` -- pero el
archivo generado en Linux NO tiene extension `.exe` (es un binario ELF
nativo), asi que el mensaje era literalmente falso ahi y podia confundir
a cualquiera buscando un archivo que no existe.

**Arreglado**: el mensaje ahora usa `nombre.exe` solo en Windows
(`os.name == "nt"`) y `nombre` (sin extension) en Linux/Mac, reflejando
el archivo real que se genero. Tambien se corrigieron menciones sueltas
de ".exe" en el boton del editor visual y en el texto de ayuda de
`sipi compilar` (CLI), que ahora dicen "ejecutable" en general en vez de
asumir Windows.

Se recompilo despues del arreglo y se confirmo que el mensaje ahora
coincide exactamente con el nombre del archivo generado.

## Novedades v41.14 — Los 3 bugs criticos de tu feedback (arreglados y probados)

### 1. Reasignar variables ya no exige la palabra 'variable'
Antes, escribir `carga = 5` (en vez de `variable carga = 5`) para
reasignar una variable YA EXISTENTE tiraba `Comando desconocido: 'carga'`.
Ahora, si `nombre` ya existe como variable en el ambito actual,
`nombre = expr` funciona directo como reasignacion:
```sipi
variable carga = 5
carga = 10          // ya no hace falta escribir 'variable' de nuevo
decir "{carga}"     // 10
```
`variable` sigue siendo obligatorio para la PRIMERA declaracion (si
`nombre` no existe todavia, sigue el mismo error de siempre, con
sugerencia incluida). Tambien respeta tipos opcionales y constantes:
si la variable tiene un tipo declarado, se sigue verificando; si es una
`const`, sigue sin poder reasignarse.

### 2. 'cada' ya no congela la ventana ('Tcl_AsyncDelete' / 'main thread is not in main loop')
La causa real: `cada ... segundos` corria un bucle bloqueante con
`time.sleep()` en el mismo hilo que iba a correr `root.mainloop()` --
asi que el mainloop de Tkinter NUNCA llegaba a arrancar, la ventana
quedaba congelada desde el primer instante.

Arreglo: cuando `cada` esta dentro de una `ventana`, ya no bloquea el
hilo. En cambio, programa cada repeticion con `root.after(ms, ...)`,
que el propio `mainloop` dispara en su momento -- sin busy-loop, sin
pelear por el hilo, y sin tocar widgets desde un hilo distinto al que
corre `mainloop` (la causa tipica de `Tcl_AsyncDelete`). Fuera de una
`ventana`, `cada` sigue funcionando exactamente igual que antes
(bucle con `time.sleep`, para scripts sin GUI).

**Verificado con Tkinter real** (Xvfb + `python3-tk`): un programa con
`ventana` + `cada 1 segundos 3 veces` corrio de punta a punta, ejecuto
las 3 repeticiones, imprimio la salida esperada y cerro limpio -- sin
colgarse, sin excepciones.

### 3. Mensaje de 'fin' faltante, mucho mas claro
Antes: `No se encontro 'fin' correspondiente iniciado en linea 3` (sin
decir que tipo de bloque era ni donde se busco). Ahora:
```
El bloque 'mientras' que abriste en la linea 3 no tiene su 'fin'. Se
busco un 'fin' que lo cierre desde ahi hasta el final del archivo
(linea 6) y no aparecio. Revisa que cada bloque que abras con
'mientras' (u otro bloque anidado adentro) tenga su 'fin' correspondiente.
```
Dice el tipo de bloque exacto (`si`/`mientras`/`funcion`/etc.), la linea
donde se abrio, y hasta donde se busco el cierre -- para no tener que
revisar un bloque de 50 lineas a mano.

Los 3 arreglos se probaron de punta a punta (no solo se leyeron) antes
de entregarlos, y los 17 tests automatizados siguen pasando.

## Novedades v41.15 — Indentacion opcional como alternativa a 'fin' (item 4 de tu feedback)

Ahora SiPi acepta los dos estilos, mezclados libremente en el mismo
archivo, incluso en bloques anidados unos dentro de otros:

```sipi
// Estilo clasico: con 'fin' explicito (como siempre)
funcion cuadrado(x)
    devolver x * x
fin

// Estilo nuevo: indentacion consistente, sin 'fin' (como Python)
mientras i < 3
    decir "Hola {i}"
    sumar i 1

si i == 3
    decir "Termine"
```

**Como decide cual estilo usar cada bloque, sin ambiguedad**: si el
CUERPO de un bloque especifico (la primera linea despues de
`si`/`mientras`/`funcion`/etc.) esta mas indentado que la linea que lo
abre, ese bloque puntual se infiere por sangria (el bloque termina
cuando la indentacion vuelve al nivel de apertura, o al final del
archivo). Si el cuerpo NO esta mas indentado que su apertura (el estilo
de SiPi de toda la vida, sin sangria obligatoria), ese bloque especifico
sigue exigiendo su `fin` explicito exactamente como antes -- cero
cambio de comportamiento para todo el codigo ya escrito.

**Por que esto es seguro** (no es un cambio a ciegas): la deteccion es
por bloque individual, no global por archivo, asi que un programa viejo
sin ninguna indentacion sigue funcionando identico. `sino` y `capturar`
(las continuaciones de `si`/`intentar`) se tratan como parte del mismo
bloque, no como una linea nueva -- si no fuera asi, un `si ... sino ...
fin` bien indentado se cortaria mal justo antes del `sino`.

**Verificado a fondo antes de entregarlo** (este es un cambio que toca
el nucleo del parser, asi que se probo en serio):
- Los 17 tests automatizados pasan (encontre y corregi una regresion real
  con `sino`/`capturar` durante las pruebas, antes de entregar esto).
- Se corrieron TODOS los archivos de `ejemplos/` sin que ninguno fallara
  por esto.
- Se probo indentacion pura sin ningun `fin` (bloques anidados incluidos),
  mezcla de los dos estilos en el mismo archivo, tabs en vez de espacios,
  el estilo clasico sin indentacion (para confirmar cero regresion), el
  mensaje de error cuando de verdad falta un `fin` en un bloque
  'solo fin', y el depurador visual paso a paso con codigo indentado sin
  `fin` -- todo con pygame/tkinter reales, no solo leido.

## Novedades v41.16 — "Util para" en la ayuda (item 6 de tu feedback)

`ayuda "comando"` ahora, para los comandos donde no es obvio, agrega una
linea extra conectando la sintaxis con la intencion real de uso:

```
> ayuda "guardar_dato"
[SiPi] guardar_dato: Guarda un valor bajo una clave, en un almacen
       persistente en disco (sobrevive a cerrar el programa).
[SiPi] Ejemplo:
guardar_dato "puntaje_maximo" 9000
[SiPi] Util para: guardar configuraciones de usuario, puntajes altos,
       o el estado de una partida sin tener que usar SQLite ni manejar
       archivos a mano.
```

Cubre 15 comandos donde el "para que" no es evidente solo con la sintaxis
(guardar_dato, obtener_dato, sqlite_conectar, sqlite_consultar, hash_texto,
iniciar_servidor_web, generar_app_android, escena_3d, crear_juego,
interfaz, lista_crear, diccionario_crear, fecha_diferencia_dias,
lanzar_error, modo_debug) -- no se agrego a los ~190 comandos completos
porque para los obvios (`decir`, `sumar`) seria ruido, no ayuda.

De paso se completaron 5 fichas de ayuda que existian a medias (el
comando funcionaba pero `ayuda` no tenia su resumen ni ejemplo):
`guardar_dato`, `obtener_dato`, `hash_texto`, `iniciar_servidor_web`,
`generar_app_android`.

## Novedades v41.17 — Autocompletado "con intencion" en el editor (item 5 de tu feedback)

El editor ahora entiende DONDE esta parado el cursor, no solo que letras
ya escribiste:

- **Dentro de un bucle** (`mientras`/`repetir`/`para_cada`/`cada`): apenas
  escribis un espacio en una linea vacia del cuerpo, aparecen `romper` y
  `continuar` primeros en la lista, antes de que escribas ninguna letra.
- **Escribiendo una condicion** (`si ...`/`mientras ...`): aparecen `y`,
  `o`, `no` primeros en la lista.
- **Prefijos especificos** (`sqlite_`, etc.): siguen filtrando exactamente
  como antes -- si escribis `sqlite_` solo aparecen los 4 comandos de
  SQLite, sin ruido de otros comandos.

Las sugerencias contextuales siempre aparecen primero en la lista,
seguidas del resto de coincidencias alfabeticas de siempre.

**Como se detecta el contexto**: reusa el mismo criterio de
apertura/cierre de bloques que ya usaba el formateador de codigo
(`PALABRAS_APERTURA_BLOQUE`/`PALABRAS_MISMO_NIVEL`, tomados del propio
motor de SiPi, no una copia separada), escaneando desde el principio del
archivo hasta la linea del cursor para saber en que bloque esta parado.

**Verificado con Tkinter real** (Xvfb): probe los 3 casos (dentro de
`para_cada`, escribiendo una condicion `si edad > 18`, y el prefijo
`sqlite_`) simulando la escritura real en el widget de texto y leyendo
el contenido del popup de autocompletado -- los 3 mostraron exactamente
lo esperado. Tambien confirme que el autocompletado normal (variables,
prefijos alfabeticos comunes) sigue funcionando identico a antes.

## Novedades v41.18 — Depurador con "viaje en el tiempo" (item 8 de tu feedback)

El depurador visual ahora graba una foto de las variables en CADA paso
ejecutado, y agrega dos botones nuevos:

- **⏪ Retroceder**: navega un paso hacia atras en el historial grabado
  (solo lectura -- no re-ejecuta nada, el programa real sigue pausado
  donde estaba). Muestra el estado exacto de las variables en ese paso
  anterior.
- **⏩ Adelante**: complementa a Retroceder. Al llegar al ultimo paso
  grabado, vuelve al modo "en vivo" normal.

Esto resuelve exactamente el caso que describiste: si `contador` se
volvio negativo en algun momento y no sabes cuando, ahora podes ir
retrocediendo paso a paso por el historial hasta encontrar la linea
exacta donde paso, sin tener que reiniciar la sesion de depuracion.

Si usas "⏭ Paso" o "▶ Continuar" mientras estas mirando el historial
hacia atras, el depurador vuelve primero al presente antes de avanzar
la ejecucion real (avanzar de verdad solo tiene sentido desde el estado
actual, no desde una foto vieja).

**Verificado de punta a punta con Tkinter real** (Xvfb): corri un programa
con un bucle que hace que `contador` se vuelva negativo a mitad de
camino, grabe 16 pasos de historial, retrocedi 3 pasos y confirme que
mostraba el valor de `contador` correcto en ESE paso especifico (-6, el
paso justo despues de que se volviera negativo), y luego avance de
nuevo hasta volver al modo en vivo (`indice_historial = None`).

## Novedades v41.19 — Ejecutables mas livianos (item 9 de tu feedback, parte 1)

`generar_exe.py` ahora detecta que comandos usa tu programa .sipi y
excluye del ejecutable las librerias pesadas (tkinter/pygame/PIL) que
no hacen falta -- en vez de empaquetar todo "por si acaso" como antes.

**Medido en la practica, con PyInstaller real** (no un calculo teorico):
- Un "hola mundo" (sin `ventana`/`crear_juego`/`imagen_*`): **44 MB -> 8.9 MB**.
- Un programa con `ventana` (necesita tkinter, no pygame ni PIL): **13.5 MB**.
- Un programa con `crear_juego` (necesita pygame): mantiene pygame,
  excluye tkinter/PIL si no los usa.

Esto ya deja el ejecutable de un programa simple MEJOR que el objetivo
de 15 MB que mencionaste -- sin sacrificar nada, porque de verdad no lo
necesitaba.

**Verificado de punta a punta**: compile los 3 casos de arriba con
PyInstaller real, corri el ejecutable resultante en cada caso (incluido
uno con `ventana` real abierto con Xvfb) y confirme que funcionan
identico a como funcionarian con Python instalado -- la unica diferencia
es el tamano del archivo.

Sigue pendiente la parte 2 del item 9 (un instalador de un clic que
tambien incluya el editor grafico completo, no solo el interprete) para
una proxima vuelta.

## Novedades v41.20 — Pattern matching con `seleccionar`/`caso`/`otro` (item 6 de tu nueva lista)

```sipi
seleccionar dia
    caso "lunes"
        decir "Odio los lunes"
    caso "viernes"
        decir "Por fin!"
    otro
        decir "Dia normal"
fin
```

Compara el valor de `seleccionar` contra cada `caso` (con `==`) y
ejecuta el primero que coincida; si ninguno coincide, ejecuta `otro`
(opcional). `caso`/`otro` son continuaciones del mismo bloque (como
`sino` en `si`), asi que el formateador automatico y el resaltado de
sintaxis del editor los reconocen sin cambios extra -- ya leen las
listas `PALABRAS_APERTURA_BLOQUE`/`PALABRAS_MISMO_NIVEL` directo del
motor. Tambien agregado a la extension de VS Code (gramatica + snippet).

**Verificado a fondo**: los 3 casos (coincide el primero, coincide otro,
no coincide ninguno -> `otro`), `seleccionar` con indentacion pura sin
`fin` explicito (interactua bien con el item 4 de la vuelta anterior),
`si` anidado dentro de un `caso`, y el formateador automatico del editor
indentando `caso`/`otro` correctamente -- probado con Tkinter real.

## Novedades v41.21 — `nulo` real y navegacion segura con `?` (item 8 de tu nueva lista)

Antes SiPi no tenia un valor "nulo" real: una clave de diccionario
faltante devolvia texto vacio (`""`), indistinguible de una clave que
de verdad guarda un texto vacio a proposito. Ahora:

```sipi
diccionario_obtener usuario "email"? -> correo
si correo != nulo
    decir "Correo: {correo}"
sino
    decir "Todavia no cargaste un correo"
fin
```

- `nulo` es un valor real del lenguaje (como `verdadero`/`falso`), se
  puede comparar con `==`/`!=`, asignar a una variable, e imprimir
  (`decir nulo` muestra `nulo`, no el `None` de Python por dentro).
- `diccionario_obtener clave? -> var` (con el `?`) da `nulo` si la clave
  no existe.
- `diccionario_obtener clave -> var` (SIN el `?`, como siempre) sigue
  dando texto vacio -- **cero cambio de comportamiento** para todo el
  codigo ya escrito; el `?` es opt-in.
- `tipo_de` reconoce `nulo` como su propio tipo.

**Verificado**: el ejemplo exacto de tu feedback (clave faltante, con
`?`, comparando `!= nulo`), el caso donde la clave si existe, el
comportamiento clasico sin `?` (para confirmar que no se rompio nada),
`nulo` como literal en una variable y en una comparacion `==`, y un
escaneo completo de los ejemplos existentes sin ninguna regresion.

## Novedades v41.22 — Operador pipe `|>` (item 7 de tu nueva lista)

```sipi
variable resultado = numeros |> lista_filtrar(es_par) |> lista_mapear(doble) |> suma_lista
```

Encadena transformaciones de listas sin anidar paréntesis ni escribir
una variable temporal por paso. El valor de cada etapa pasa a la
siguiente como su lista de entrada.

**Comandos soportados en un pipe** (los que tiene sentido encadenar
sobre una lista): `lista_filtrar(funcion)`, `lista_mapear(funcion)`,
`lista_reducir(funcion, valor_inicial)`, `suma_lista`,
`promedio_lista`, `lista_contiene(valor)`, `lista_longitud`. Usar un
comando no soportado en un pipe da un error claro con la lista de los
que sí funcionan, en vez de fallar de forma confusa.

**Por que no CUALQUIER funcion se puede encadenar todavia**: SiPi hoy
no tiene llamadas a funcion dentro de expresiones en general (solo via
`llamar_valor funcion(args) -> variable` como sentencia aparte) -- el
pipe reusa la sintaxis de los comandos de listas existentes en vez de
inventar un sistema de funciones-como-valores nuevo. Es un paso real y
util ahora mismo; un pipe totalmente generico (`x |> mi_funcion()`)
necesitaria antes agregar llamadas a funcion dentro de expresiones,
que queda como una mejora aparte.

Verificado: el ejemplo exacto de tu feedback, `lista_reducir` en un
pipe con valor inicial, un pipe de una sola etapa, el mensaje de error
al usar un comando no soportado, y un escaneo completo de los ejemplos
existentes sin regresiones. Tambien agregado el resaltado de `|>` en la
extension de VS Code.

## Novedades v41.23 — Cache de bytecode `.sipic` (item 5 de tu nueva lista)

SiPi ahora guarda un archivo `.sipic` junto a tu `.sipi` la primera vez
que lo corres. Si volves a ejecutar el mismo archivo sin cambios, se
carga directo desde ahi, saltando el parseo (sacar comentarios, resolver
strings triples, inferir `fin` por indentacion) por completo.

**Medido en la practica** (no un calculo teorico), con un programa
generado de 12.000 lineas:
- Primera corrida (sin cache, la genera): **37.3 ms** de carga.
- Corridas siguientes (con cache): **~5.4 ms** de carga -- **cerca de
  7 veces mas rapido**.

**Como se invalida la cache**: se compara el `.sipic` contra el
contenido actual del `.sipi` por tamano Y hash SHA-256 (no solo la
fecha de modificacion, que puede no cambiar si copiaste el archivo
desde otro lado). Si no coincide exactamente, o si es de una version
distinta de SiPi, se ignora y se vuelve a parsear normal, generando una
cache nueva. Una cache corrupta o con permisos de escritura denegados
nunca rompe la ejecucion -- en el peor caso, simplemente no hay cache
y el programa corre igual (un poco mas lento en la carga, nada mas).

Para forzar una corrida sin usar ni generar cache (util para depurar):
```
python sipi.py --sin-cache mi_programa.sipi
```

**Verificado**: que la cache y el parseo normal dan resultados
identicos linea por linea, que modificar el archivo fuente invalida la
cache vieja automaticamente, que `--sin-cache` no deja ningun `.sipic`,
y un escaneo completo de los ejemplos existentes sin regresiones.
`sipi ejecutar` (el CLI) se beneficia automaticamente sin cambios, ya
que ejecuta `sipi.py` por dentro.

Si usas control de versiones (git), quizas quieras agregar `*.sipic` a
tu `.gitignore` -- son archivos generados, no codigo fuente.

## Novedades v41.24 — Docstrings + generador de docs (item 3) y Servidor LSP (item 2)

### Item 3: Docstrings y documentacion automatica
Nuevo `generar_docs.py` (tambien disponible como `sipi doc archivo.sipi`
via el CLI). Escribe comentarios especiales `//!` arriba de tus
funciones/clases/metodos:

```sipi
funcion sumar(a, b)
    //! Suma dos numeros y devuelve el resultado.
    //! @param a: primer numero
    //! @param b: segundo numero
    //! @returns: a + b
    devolver a + b
fin
```

Y corre:
```
sipi doc mi_programa.sipi
```
Genera `mi_programa_docs.html`: una pagina con todas las funciones y
clases documentadas, sus parametros y su retorno. Las funciones/clases
sin `//!` tambien aparecen (marcadas como "sin documentacion todavia"),
para que sea facil ver que falta documentar. Funciona sobre el archivo
fuente en crudo -- no necesita que el programa corra sin errores.

**Verificado**: probe el ejemplo exacto de tu feedback mas una clase con
interfaz y un metodo documentado, confirme que la funcion sin docstring
se marca correctamente, y renderice el HTML generado a una imagen para
revisar visualmente que se ve bien (fondo oscuro, tipografia legible,
todo en una sola pagina autocontenida).

### Item 2: Servidor LSP (Language Server Protocol)
Nuevo `sipi_lsp.py`: un servidor LSP real hablando JSON-RPC estandar
sobre stdio (el mismo protocolo que usan pyright, rust-analyzer, etc.),
sin depender de ninguna libreria externa. Cualquier editor con soporte
LSP generico (VS Code con una extension chica, Neovim con
`nvim-lspconfig`, etc.) se puede conectar.

**Que ofrece hoy**:
- Diagnosticos en tiempo real: si un bloque `si`/`mientras`/`funcion`/etc.
  se queda sin su `fin`, el editor lo marca en rojo en la linea exacta,
  con el mismo mensaje de error que veria el usuario al ejecutar (reusa
  el parser REAL del interprete, no una copia separada).
- Autocompletado con los ~190 comandos reales del lenguaje (tomados de
  `COMANDOS_CONOCIDOS`, se mantiene sincronizado solo).

**Por que el alcance es este y no mas** (para ser honesto): no valida
todavia la sintaxis especifica de cada comando individual, porque eso
necesitaria ejecutar el programa -- inseguro para diagnosticos en vivo
mientras el usuario todavia esta escribiendo (un programa a medio
escribir podria abrir una ventana o colgarse en un bucle). Tampoco tiene
"ir a la definicion" ni "hover" todavia. Es una base real y que funciona
de punta a punta, no un LSP completo de nivel productivo -- ese es un
proyecto mas grande para otra sesion.

**Verificado con el protocolo LSP real**: escribi un cliente de prueba
que le habla al servidor exactamente como lo haria VS Code (JSON-RPC
enmarcado con Content-Length), y confirme:
- El handshake `initialize` responde con las capacidades correctas.
- Un archivo con un `mientras` sin `fin` genera un diagnostico en la
  linea exacta (linea 3, la del `mientras`), con el mensaje completo.
- Al corregir el codigo y reenviarlo (`didChange`), el diagnostico
  desaparece.
- El autocompletado devuelve 195 items reales, incluyendo comandos
  nuevos como `seleccionar` y `escena_3d`.

---

## Novedades de la version 40.0 — #22 de la lista: POO real, y 3 bugs serios corregidos

### Sistema 1 — Programacion orientada a objetos real
Nuevos comandos: `clase Nombre [hereda_de Padre] ... fin` (con campos
por defecto y `metodo nombre(params) ... fin` adentro), `nuevo
Clase(args) -> variable` (instancia y llama automaticamente a
`constructor` si existe), `llamar_metodo objeto "nombre"(args) ->
variable`, y `es_instancia_de objeto Clase -> variable`. Dentro de un
metodo, el objeto esta disponible como la variable implicita `este`
(como `self`/`this`), y como los objetos son diccionarios de Python
reales, `diccionario_asignar este "campo" valor` modifica el objeto de
verdad, no una copia. Soporta herencia real con sobreescritura de
metodos (polimorfismo): probado con `Animal -> Perro/Gato`, cada uno
con su propio `hacer_sonido()`, llamado a traves de un metodo heredado
`describir()` definido solo en la clase base.

### Refactor que previene bugs futuros de este mismo tipo
Habia mas de 14 copias pegadas de la misma lista de "palabras que abren
un bloque" repartidas por todo el archivo (la causa raiz de que
`pagina_web`/`formulario` se hubieran desincronizado del formateador en
una version anterior). Se unificaron todas en una sola constante
(`BLOQUES_QUE_ABREN`), usada tambien por el formateador de codigo.

### Bug encontrado al agregar clases: un campo llamado 'clase' rompia el conteo de bloques
Al agregar `clase` como palabra reservada, se rompio cualquier programa
que ya tuviera un campo o variable llamado literalmente `clase` (muy
comun, ej. `estructura Personaje` con un campo `clase = 0`), porque el
detector de bloques confundia esa asignacion con la apertura de un
bloque real. Corregido: una linea tipo `palabra = valor` nunca se
cuenta como apertura de bloque, aunque 'palabra' coincida con una
palabra reservada. Se agrego una prueba automatizada especifica para
este caso.

### Bug serio encontrado: concatenar texto con numeros fallaba en silencio
`"Puntaje: " + puntaje` (texto + numero) tiraba un `TypeError` de
Python por dentro y se devolvia el texto crudo sin evaluar - uno de los
patrones mas comunes que escribe cualquier persona. Corregido con un
evaluador de expresiones propio (basado en el modulo `ast`) que
convierte numeros a texto al concatenar con `+`, como se espera en un
lenguaje pensado para principiantes.

### Bug de fondo mas serio encontrado esta ronda: la sustitucion de variables corrompia texto dentro de strings
Al arreglar el bug anterior aparecio uno mas profundo, presente desde
siempre: la sustitucion de nombres de variable por su valor se hacia
con una unica pasada de regex sobre TODA la expresion, sin distinguir
que partes eran codigo y cuales eran texto literal. Resultado: si un
string literal contenia una palabra que tambien era el nombre de una
variable (ej. la variable `vida` y el texto `" de vida"`), esa palabra
DENTRO del texto se reemplazaba por el valor de la variable
(`"Rex tiene 100 de vida"` se convertia en `"Rex tiene 100 de 100"`).
Corregido haciendo que la sustitucion respete los limites de los
strings literales (comillas), igual que ya hacia el buscador de
llamadas a funciones. Se agregaron pruebas automatizadas para los tres
bugs de esta ronda; la bateria completa paso de 14 a 17 pruebas.



## Novedades de la version 39.0 — Bug reportado corregido + #20 de la lista: pruebas automatizadas

### Bug reportado y corregido: el formateador de codigo no indentaba bien `pagina_web`/`formulario`
Revisando el area de `sipi.py` que reportaste (cerca de las lineas
3460 y 3487, la funcion `formatear_codigo` y sus tablas de palabras
clave), se encontro que `PALABRAS_APERTURA_BLOQUE` -la lista que usa
`--formatear` para saber que comandos abren un bloque y necesitan
indentar lo que sigue- **no incluia `pagina_web` ni `formulario`**,
aunque en el resto del interprete (`_encontrar_fin`, en 15 lugares
distintos) si se los trata como bloques reales. Resultado: formatear un
programa con paginas web o formularios dejaba todo el contenido al
mismo nivel de indentacion, sin importar cuantos bloques anidados
tuviera. Se confirmo que el bug ya estaba presente en la v29 original.
Corregido agregando esas dos palabras a la lista; probado con un
`pagina_web` que contiene un `formulario` anidado y ahora indenta
correctamente en 2 niveles.

### Pruebas automatizadas reales (`sipi test`)
Nuevo `tests/test_suite.py` (solo libreria estandar, sin dependencias
externas) con 14 pruebas automatizadas que ejecutan programas `.sipi`
reales contra el motor real y comparan la salida, cubriendo los bugs
mas importantes corregidos a lo largo de todas las versiones:
recursion profunda, llamadas a funciones dentro de expresiones
(anidadas incluso), concatenacion de texto de tres partes, division
por cero, variables no declaradas, `romper`/`continuar` (incluyendo el
caso de que no se escapen de una funcion sin bucle propio), errores
propios con `lanzar_error`, constantes, programacion funcional sobre
listas, el formateador de `pagina_web`/`formulario`, y SQLite real.

Se puede correr con:
```
sipi test
```
o directamente `python3 tests/test_suite.py`. Sirve como red de
seguridad real: si un cambio futuro reintroduce alguno de estos bugs ya
solucionados, estos tests lo van a detectar en segundos en vez de que
alguien lo encuentre por casualidad meses despues. `publicar.py` ahora
tambien incluye la carpeta `tests/` en las distribuciones.



## Novedades de la version 38.0 — #10 y #11 de la lista: modo principiante y documentacion interactiva

### Bug real encontrado (al escribir el tutorial): las comillas no se pueden escapar dentro de un texto
Al escribir el tutorial interactivo se encontro que `\"` dentro de un
string no funciona como escape: SiPi lo deja tal cual (con la barra
invertida incluida) en vez de interpretarlo como una comilla literal.
Es una limitacion real del tokenizador de strings actual. Se documento
en `DOCUMENTACION.md` con la solucion practica (usar comillas simples
`'` para el texto anidado) para que nadie mas pierda tiempo con esto.

### Documentacion interactiva (`ayuda`)
Nuevo comando del lenguaje `ayuda "nombre_comando"`, usable desde
cualquier programa `.sipi`, con resumen + ejemplo real para ~35 de los
comandos mas usados (variables, condicionales, bucles, funciones,
listas, SQLite, API web, modulos, etc.), con sugerencia automatica de
comandos parecidos si hay un typo. `ayuda` sin argumentos lista los
comandos con ficha disponible.

Tambien desde la terminal:
```
sipi ayuda mostrar sqlite_conectar
sipi ayuda buscar sqlite
```

### Modo principiante (`modo_principiante`)
Nuevo comando `modo_principiante`: cuando esta activo, si el programa
falla con alguno de los errores mas comunes para quien recien empieza
(variable no declarada, division por cero, comando desconocido, falta
un `fin`, funcion no definida, modificar una constante), SiPi agrega un
consejo en lenguaje simple explicando como solucionarlo, ademas del
mensaje de error tecnico. Sin `modo_principiante` activado, el
comportamiento no cambia (para no ser repetitivo con usuarios
avanzados).

### Tutorial interactivo (`sipi tutorial`)
Nuevo `ejemplos/tutorial_interactivo.sipi` y subcomando `sipi tutorial`:
un recorrido guiado y realmente ejecutable por variables, operaciones,
condicionales, bucles, funciones, listas y manejo de errores, con
`modo_principiante` activado. Pensado como primer contacto con SiPi
antes de leer `DOCUMENTACION.md`.



## Novedades de la version 37.0 — #7 y #8 de la lista: CLI profesional y proyectos estructurados

Nuevo `sipi_cli.py` (con `sipi_cli.bat` para Windows), una interfaz de
linea de comandos real con subcomandos, en vez de tener que recordar
que archivo `.py`/`.bat` corresponde a cada tarea:

```
sipi ejecutar archivo.sipi      Ejecuta un programa SiPi
sipi crear nombre_proyecto      Crea un proyecto nuevo con estructura estandar
sipi compilar archivo.sipi      Compila un programa a un ejecutable .exe
sipi instalar nombre_o_url      Instala un modulo .sipi
sipi instalar --dependencias    Instala todo lo declarado en sipi_paquetes.json
sipi publicar                   Genera la carpeta PUBLICACION/ lista para distribuir
sipi ayuda                      Muestra la ayuda
```

- `sipi crear` arma un proyecto con estructura estandar
  (`main.sipi`, `ejemplos/`, `modulos_instalados/`, `sipi_paquetes.json`,
  `README.md`), en vez de tener que armar las carpetas a mano.
- Los demas subcomandos son una capa fina sobre lo que ya existia
  (`sipi.py`/`sipi_protegido.py`, `generar_exe.py`, `_instalar_modulo`,
  `publicar.py`), reutilizando la logica real en vez de duplicarla, y
  ya distinguen automaticamente entre carpeta de desarrollo y carpeta
  publicada (protegida).
- `publicar.py` ahora tambien incluye `sipi_cli.py`/`sipi_cli.bat` en la
  carpeta `PUBLICACION/`, asi que el CLI queda disponible para quien
  reciba tu proyecto ya compilado/protegido, no solo en desarrollo.

Se probaron los 6 subcomandos de punta a punta: crear un proyecto nuevo
y ejecutarlo, instalar un modulo real desde un servidor HTTP (tanto
suelto como via `sipi_paquetes.json`), compilar (llega correctamente a
PyInstaller), publicar, y ayuda — incluyendo la verificacion de que
`sipi ejecutar`/`sipi ayuda` funcionan igual dentro de una carpeta ya
publicada (usando `sipi_protegido.py`).



## Novedades de la version 36.0 — #6 de la lista: depurador visual corregido y completado

El depurador visual (`VentanaDepurador`, con breakpoints, paso a paso y
panel de variables) ya existia, pero al revisarlo a fondo se
encontraron y corrigieron dos bugs reales, ademas de completar una
funcionalidad que faltaba:

### Bug critico: el boton "⏹ Detener" no detenia nada si el programa estaba dentro de una funcion
El mecanismo para cortar la ejecucion usaba la misma excepcion que
`devolver` (`RetornoFuncion`). Si el usuario apretaba "Detener" mientras
el programa estaba corriendo *dentro de una llamada a funcion* (el caso
mas comun en cualquier programa real), esa funcion atrapaba la señal de
corte como si fuera un simple `devolver` y **el programa seguia
corriendo hasta el final**, ignorando el boton. Se probo especificamente
este escenario (breakpoint dentro del bucle de una funcion) y se
confirmo que el hilo de ejecucion seguia vivo despues de apretar
"Detener". Se corrigio agregando una excepcion dedicada
(`DepuracionDetenida`) que ninguna llamada a funcion puede confundir con
un retorno normal. Vuelto a probar: ahora el hilo termina de verdad en
cuanto se aprieta "Detener", incluso en medio de una funcion.

### Bug menor: el mensaje final decia "terminado correctamente" aunque el usuario lo hubiera detenido a mano
Corregido para que, si el usuario detuvo la sesion, el mensaje final
diga "Sesion de depuracion detenida por el usuario" en vez de sugerir
que el programa termino solo.

### Completado: variables locales en el panel "Variables en vivo"
Antes el panel solo mostraba variables globales; dentro de una funcion
aparecia vacio o incompleto aunque la funcion tuviera sus propias
variables. Ahora se muestran por separado "Variables locales (funcion
actual)" y "Variables globales". Probado deteniendose dentro de una
funcion con parametro `n` y variable local `i`: ambas aparecen
correctamente en el panel.

Todo lo anterior se probo de punta a punta con un display virtual
(Xvfb) simulando la interaccion real del usuario con la ventana del
depurador (breakpoints, paso a paso, continuar, detener).



## Novedades de la version 35.0 — #4 y #5 de la lista: autocompletado y resaltado de sintaxis real

### Bug de documentacion encontrado y corregido
`DOCUMENTACION.md` (agregada en la v32.1) decia que los comentarios se
escriben con `#`. Es incorrecto: SiPi usa `//` para comentarios de una
linea y `/* ... */` para comentarios de bloque (`#` ni siquiera es un
comando valido, tira error). Se probo explicitamente y se corrigio la
documentacion.

### Bug real encontrado en el editor: el resaltado de sintaxis estaba desactualizado
El editor tenia una lista de palabras clave (`PALABRAS_CLAVE`) copiada a
mano, separada de la lista real de comandos del interprete
(`COMANDOS_CONOCIDOS` en `sipi.py`). Con el tiempo se desincronizaron:
**26 comandos reales** (`romper`, `continuar`, todos los de
`sqlite_*`, `escuchar_ruta`, `iniciar_api_web`, `tipo_de`,
`lanzar_error`, `instalar_modulo`, `listar_modulos`, los `lista_*`
funcionales, etc.) nunca se coloreaban en el editor porque no estaban en
esa lista vieja.

**Corregido de raiz, no solo parchado**: el editor ahora carga
`PALABRAS_CLAVE` dinamicamente desde `COMANDOS_CONOCIDOS` del motor real
(via `_cargar_motor_sipi`, que ya distingue entre `sipi.py` y
`sipi_protegido.py`), asi que el resaltado de sintaxis nunca puede
volver a desactualizarse cuando se agregue un comando nuevo. Se dejo una
lista de respaldo fija por si el motor no se puede cargar. Verificado:
`sqlite_conectar`, `romper` y `tipo_de` ahora se resaltan correctamente,
y la lista completa paso de 151 a 178 comandos reconocidos.

### Autocompletado real (nuevo)
El editor ahora muestra un menu de autocompletado mientras se escribe
(a partir de 2 caracteres), con sugerencias de:
- Comandos del lenguaje (los mismos 178, siempre sincronizados).
- Variables declaradas en el programa actual (detectadas leyendo el
  codigo: `variable`/`var`/`const`).
- Funciones definidas en el programa actual (`funcion nombre(...)`).

Se navega con las flechas ↑/↓, se acepta con Tab o Enter, y se cierra
con Escape. Probado de punta a punta bajo un display virtual (Xvfb):
escribir "repe" y aceptar con Tab completa a "repetir"; escribir "res"
con una variable "resultado" ya declarada la sugiere junto a los
comandos "restar" y "responder_json".



## Novedades de la version 34.0 — #3 de la lista: mejor manejo de errores

### Bug de fondo encontrado y corregido: typos en variables pasaban totalmente desapercibidos
Se encontro que usar una variable no declarada (por un typo, por
ejemplo `nombree` en vez de `nombre`) **nunca daba error**: tanto dentro
de interpolacion de texto (`decir "Hola {nombree}"`) como en una
expresion suelta (`variable r = nombree_que_no_existe`), SiPi
silenciosamente imprimia el NOMBRE de la variable como si fuera un
texto literal, en vez de avisar que no existia. Esto podia esconder
bugs reales por mucho tiempo, porque el programa "corria" sin
quejarse y mostraba datos incorrectos en vez de fallar.

**Corregido**: ahora usar una variable no declarada da un error claro:
```
[SiPi] ERROR: Variable no declarada: 'nombree'. ¿Quisiste decir 'nombre'?
```
Si hay una variable o funcion parecida definida en el programa, SiPi la
sugiere automaticamente (usando la misma logica de sugerencias que ya
existia para comandos mal escritos). Si no hay ninguna parecida, sugiere
como declararla.

### División por cero con mensaje claro
Antes, dividir por cero tambien caia en el mismo camino silencioso y
devolvia texto sin evaluar. Ahora da un mensaje directo:
```
[SiPi] ERROR: Division por cero al evaluar la expresion 'a / b'.
```

### Compatibilidad verificada
Se corrio toda la bateria de ejemplos incluidos (mas de 12 programas
distintos: agenda, automatizacion, sitio web, formularios, JSON/CSV,
modulos, listas de tareas, manejo de errores, etc.) para confirmar que
este cambio, al ser mas estricto, no rompe ningun programa existente
que ya declaraba bien sus variables.



## Novedades de la version 33.0 — Otro bug critico corregido + paquetes con dependencias

### Bug critico encontrado y corregido: concatenacion de texto rota desde siempre
Se encontro (probando el sistema de modulos con una funcion tipica de
saludo) que **cualquier concatenacion de la forma `"texto" + variable +
"texto"` estaba rota desde la v29**: como la expresion completa empieza
y termina con comillas, el evaluador la confundia con un unico string
literal y devolvia el texto crudo sin evaluar, por ejemplo:
```
devolver "Hola " + nombre + " desde aca!"
```
imprimia literalmente `Hola " + nombre + " desde aca!` en vez de
`Hola Mateo desde aca!`. Se confirmo que el bug ya estaba presente en la
v29 original (no fue introducido por cambios recientes). **Corregido de
raiz**: ahora se verifica que la comilla de apertura realmente cierre
justo al final de la expresion (no solo que el primer y ultimo caracter
sean comillas) antes de tratarla como un literal simple.

### Bug corregido: `editor_protegido.py` buscaba `sipi.py` en vez de `sipi_protegido.py`
Reportado directamente: al generar `editor_protegido.py` con
`proteger_codigo.py`/`publicar.py`, los botones "▶ Ejecutar", "Compilar
a .exe", la vista previa en vivo, el formateador de codigo y el
depurador visual tenian la ruta al motor fija a `sipi.py` (en 2 casos,
con un `import sipi` directo), que no existe en una carpeta ya
publicada (solo existe `sipi_protegido.py`). Se agregaron
`_ruta_motor_sipi()` / `_ruta_generar_exe()` / `_cargar_motor_sipi()`
que resuelven el archivo correcto segun la carpeta, y se verifico
generando una `PUBLICACION/` real y confirmando que el editor protegido
carga el motor protegido sin error.

### Sistema de paquetes mas solido (parte del pedido de la lista)
- `listar_modulos` — lista los modulos ya instalados (con su origen y
  fecha de instalacion), o los guarda en una variable con
  `listar_modulos -> variable`.
- `desinstalar_modulo "nombre"` — elimina un modulo instalado y lo saca
  del registro.
- `instalar_dependencias` — lee un manifiesto `sipi_paquetes.json` (el
  equivalente de un `package.json`/`requirements.txt` para SiPi) con
  formato `{"modulos": {"nombre": "url_o_nombre"}}`, e instala
  automaticamente todas las dependencias declaradas del proyecto en una
  sola instruccion, sin tener que escribir un `instalar_modulo` por
  cada una. Probado de punta a punta con un servidor HTTP local real
  sirviendo un modulo `.sipi`, incluyendo el manejo de errores cuando
  una dependencia no se puede descargar (sigue con las demas y avisa
  cuales fallaron al final).



## Novedades de la version 32.2 — Bug corregido: `editor_protegido.py` buscaba `sipi.py` en vez de `sipi_protegido.py`

### El bug (reportado directamente)
Al usar `proteger_codigo.py` (o `publicar.py`), se generaba
`editor_protegido.py` correctamente, pero al abrirlo en una carpeta
publicada (donde solo existe `sipi_protegido.py`, sin el `sipi.py`
original) el editor fallaba: los botones "▶ Ejecutar", "Compilar a
.exe", la vista previa en vivo, el formateador de codigo y el depurador
visual paso a paso tenian la ruta al motor **fija a `sipi.py`** (y en un
caso, un `import sipi` directo por nombre de modulo), asi que no
encontraban nada en una carpeta publicada.

### La correccion
- Se agrego `_ruta_motor_sipi()` / `_ruta_generar_exe()`: resuelven el
  archivo correcto (`sipi.py`/`generar_exe.py` en desarrollo,
  `sipi_protegido.py`/`generar_exe_protegido.py` en una carpeta
  publicada) y se usan en la vista previa en vivo, en "▶ Ejecutar" y en
  "Compilar a .exe".
- Se agrego `_cargar_motor_sipi()`: importa el motor con
  `importlib.util` bajo un nombre de modulo interno consistente, en vez
  de depender de `import sipi` (que fallaba con
  `ModuleNotFoundError: No module named 'sipi'` en cualquier carpeta
  donde el archivo se llamara `sipi_protegido.py`). Se uso en el
  formateador de codigo y en el depurador visual paso a paso.
- **Verificado especificamente el escenario del bug**: se genero
  `PUBLICACION/` con `publicar.py`, se copio a una carpeta limpia sin
  `sipi.py`, y se confirmo que `editor_protegido.py` ahora encuentra y
  carga `sipi_protegido.py` correctamente (antes de la correccion,
  esto fallaba porque en esa carpeta no existe ningun archivo llamado
  `sipi.py`).



## Novedades de la version 32.1 — Documentacion oficial completa

Se agrego `DOCUMENTACION.md`: guia de instalacion, tutorial desde cero
(hola mundo -> variables -> condicionales -> bucles -> funciones y
recursion -> listas/programacion funcional -> manejo de errores), guia
de sintaxis, referencia completa de comandos organizada por categoria
(control de flujo, listas/diccionarios/matrices, texto, numeros,
archivos/SQLite, web/API, GUI de escritorio, juegos 2D, sistema), y
ejemplos por nivel apuntando a la carpeta `ejemplos/`. Todo el contenido
del tutorial fue probado linea por linea en esta misma sesion antes de
documentarlo.



## Novedades de la version 32.0 — Bug critico corregido: llamadas a funciones dentro de expresiones

### El bug mas importante encontrado hasta ahora
Se encontro (probando recursion real) que **llamar a una funcion dentro de
una expresion nunca funciono**: cosas tan basicas como

```
variable r = doble(5)
```
o
```
variable r = contar_hasta(n - 1)
devolver r + 1
```

no lanzaban un error: simplemente devolvian el TEXTO sin evaluar
("doble(5)") en vez del resultado real, porque el evaluador de
expresiones no sabia reconocer una llamada a funcion embebida — solo
funcionaba `llamar_valor funcion(args) -> variable` como instruccion
separada. Esto rompia en silencio cualquier funcion recursiva real
(fibonacci, factorial, recorridos, etc.) apenas se armaba con una
expresion en vez de un `llamar_valor` explicito.

**Corregido de raiz**: el evaluador de expresiones ahora reconoce
llamadas a funciones SiPi definidas por el usuario en cualquier parte de
una expresion — anidadas, combinadas con operadores, dentro de
condiciones (`si`), dentro de interpolacion de texto (`"{funcion(x)}"`),
etc. Probado con: `doble(5)`, `suma_uno(doble(3))` (anidada, da 7),
`si es_mayor(edad)`, e interpolacion `"Hola {saludo(nombre)}"`.

### Recursion real y profunda, sin segfaults
Al arreglar el bug anterior, aparecio el siguiente problema real:
la recursion profunda (miles de niveles) tiraba
`maximum recursion depth exceeded` con Python. Ahora:
- El programa corre en un hilo con una pila de sistema operativo de
  512 MB y un limite de recursion de Python mucho mas alto, para que la
  recursion real de SiPi pueda llegar bastante mas profundo sin
  arriesgarse a un segfault (que es lo que pasaria si solo se subiera
  `sys.setrecursionlimit` sin agrandar tambien la pila).
- Probado con 5.000 y 20.000 niveles de recursion real sin fallar.
- Si aun asi se llega al limite, el mensaje de error ahora es humano
  ("la funcion se llamo a si misma demasiadas veces...") en vez de un
  traceback de Python, y la pila de llamadas impresa se recorta a los
  ultimos 12 niveles (con un aviso de cuantos mas hay) para no saturar
  la pantalla con miles de lineas repetidas.



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
