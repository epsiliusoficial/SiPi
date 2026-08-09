# KNOWN ISSUES — Problemas conocidos

Lista honesta de limitaciones y problemas conocidos de SiPi, para que no pierdas tiempo reportando algo que ya sabemos. Si encontrás algo que no está acá, sí reportalo — ver [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Corregido recientemente (para que sepas si tu copia ya lo tiene)

- **Bug reportado por el tester en Windows: `can't open file ...\Temp\...\SiPi-main\sipi_protegido.py` / `[Errno 2] No such file or directory`.** Causa confirmada reproduciendo el escenario exacto: SiPi ejecutandose desde adentro de la carpeta temporal de Windows (típico de abrir el `.zip` descargado con doble clic sin extraerlo antes) — Windows puede borrar esa carpeta en cualquier momento. `editor_sipi.py` y `sipi_cli.py` ahora detectan esto al arrancar y avisan con causa y solución clara, antes de que se rompa nada. Además, cualquier error de "motor no encontrado" ahora muestra la carpeta exacta donde se buscó y la causa más probable, en vez de un traceback crudo.
- **F11 no hacía nada.** Confirmado por búsqueda en todo el código: no existía ningún `bind` para esa tecla. Se agregó pantalla completa real (`F11` alterna, `Escape` sale), verificado programáticamente.
- **Ejecutar exigía guardar primero.** Ahora "▶ Ejecutar" corre el contenido actual del editor aunque no esté guardado (usa un archivo temporal propio de la sesión, que no se borra hasta cerrar el editor — a diferencia de un temporal que se autodestruye antes de que el proceso hijo llegue a leerlo). Verificado ejecutando con y sin archivo guardado.
- **No había indicador de cambios sin guardar.** El título ahora muestra `nombre.sipi *` con cambios pendientes, y se limpia al guardar. Verificado programáticamente.
- **Sin atajos de teclado.** Se agregaron `Ctrl+S`, `Ctrl+Shift+S`, `Ctrl+Enter`/`F5` (ejecutar), `F11` (pantalla completa), `Ctrl+Y` (rehacer, además del `Ctrl+Z` que Tk ya traía), `Ctrl+F` (buscar) y `Ctrl+H` (buscar y reemplazar, nuevo).

- **`generar_exe.py` filtraba el código fuente completo del usuario en texto plano.** El motor (`sipi_protegido.py`) ya estaba protegido, pero el "wrapper" que PyInstaller compila tenía el programa `.sipi` entero embebido como un string de Python legible — cualquiera con una herramienta común de extracción de PyInstaller podía leerlo íntegro, aunque el lenguaje en sí estuviera protegido. Se corrigió aplicando la misma técnica de ofuscación (bytecode + marshal + base64) al wrapper también. Verificado corriendo el `.exe` real y buscando el código con `strings` — ya no aparece.
- **La combinación "motor protegido" generaba ejecutables rotos.** Al ofuscar el motor, PyInstaller dejaba de poder detectar sus propios `import` (`json`, `csv`, `sqlite3`, etc.) por análisis estático, y el `.exe` resultante crasheaba con `ModuleNotFoundError` en el primer uso — un bug que solo aparece al **ejecutar** el binario, no leyendo el código. Se corrigió declarando esos imports explícitamente. Verificado compilando y corriendo el `.exe` de punta a punta.
- **La carpeta `build_<nombre>/` que genera `generar_exe.py` quedaba en el disco para siempre**, con una copia en texto plano del wrapper (el programa completo del usuario) al lado del `.exe` "protegido" — una fuga más fácil de encontrar que cualquier cosa adentro del propio ejecutable. Ahora se borra sola en un build exitoso.
- **No había `.gitignore`**, así que `.sipic` (la caché — ver `CACHE.md`) se hubiera terminado versionando sin querer. `publicar.py` tampoco excluía archivos de caché al armar la distribución pública. Ambos corregidos.
- **`{variable}` no se interpolaba dentro de una concatenación con `+`.** `decir "hola {nombre}"` funcionaba, pero `decir "prefijo-" + "hola {nombre}"` mostraba literalmente `{nombre}` sin reemplazar. Corregido: ahora se interpola correctamente en ambos casos, incluyendo saltos de línea (`\n`) dentro del texto concatenado.
- **`crear_archivo` fallaba en total silencio con una expresión como contenido.** `crear_archivo "ruta" variable + "texto"` no hacía nada (ni error, ni escritura) porque el patrón de sintaxis solo aceptaba un texto literal completo o una única variable, no una expresión. Corregido: ahora acepta cualquier expresión válida como contenido, igual que `decir`.
- **`hilo_resultado` siempre devolvía `nulo`.** El resultado del hilo se guardaba en una copia del diccionario de estado interno en vez de la referencia real que el hilo iba actualizando. Corregido.

## Concurrencia (`hilo_crear`, `con_bloqueo`)

- **Cada hilo tiene su PROPIA copia de las variables globales, tomada en el momento de crearlo.** No es una limitación temporal, es la arquitectura elegida a propósito: el intérprete de SiPi no fue diseñado para que múltiples hilos muten el mismo estado interno de forma segura (varios atributos internos se reasignan temporalmente durante cada llamada a función). Compartir una variable de verdad entre hilos habría significado arriesgar corromper la pila de llamadas o el código que se está ejecutando. Si necesitás que un hilo devuelva algo al programa principal, usá el valor de `devolver` (leelo con `hilo_resultado`), no una variable global.
- `bloqueo_crear`/`con_bloqueo` sirven para sincronizar el acceso a recursos genuinamente compartidos entre hilos (un archivo, una conexión, la salida de consola) — no las variables de SiPi, que ya son independientes por diseño.

## Instalación

- **`buscar_paquete` puede fallar por límite de la API de búsqueda de GitHub.** Usa el endpoint de búsqueda de GitHub sin autenticación, que tiene un límite bajo (10 pedidos por minuto por IP, según la documentación de GitHub). Si hacés muchas búsquedas seguidas, puede empezar a devolver error hasta que se resetee el límite. `instalar_repositorio` con la URL/nombre exacto no tiene este problema, solo la búsqueda.
- **El instalador de Linux/Mac (`instalar.sh`) depende del gestor de paquetes de tu distro para `tkinter`.** Python por sí solo no lo instala vía `pip` (no es un paquete de PyPI en la mayoría de los sistemas) — el instalador te avisa con el comando exacto para tu distro (`apt`, `dnf`, `pacman`), pero no lo instala automáticamente porque requiere `sudo`.

## Editor visual (WYSIWYG)

- **Solo funciona sobre `ventana`, `pagina_web` y `crear_juego`.** Si tu programa no tiene ninguno de esos tres bloques, `editor_visual` no tiene nada para mostrar. Más tipos de bloque se van agregando con el tiempo.
- **Dentro de `crear_juego`, solo se pueden editar sprites con posición numérica literal** (`sprite jugador 100 200 ...`). Si la posición se calcula con una variable o fórmula, el editor visual no la muestra como arrastrable — para no pisar lógica dinámica escribiendo un número fijo encima sin que te des cuenta.

## LSP / extensión de VS Code

- **Valida la estructura de bloques (que todo `si`/`funcion`/etc. tenga su `fin`) y autocompleta nombres de comandos, pero todavía no valida la sintaxis interna de cada comando individual.** Un comando bien escrito de nombre pero con argumentos mal formados no se marca en rojo hasta que lo ejecutás.
- **No tiene "ir a la definición"** para funciones o variables todavía.

## Gestor de paquetes

- **No hay un índice curado de módulos recomendados.** `buscar_paquete` te muestra cualquier repositorio público de GitHub que matchee tu búsqueda, sin verificar calidad ni que el código sea seguro. Revisá el código de un paquete de terceros antes de instalarlo.

## Rendimiento

- **El techo de rendimiento es el de Python**, ya que SiPi es un intérprete escrito en Python puro. La caché de bytecode (`.sipic`) acelera reejecuciones del mismo archivo, pero no cambia esto de fondo. Para programas que necesitan procesar muchísimos datos o correr en tiempo real estricto, SiPi no es la herramienta indicada (ver "Cuándo NO conviene usar SiPi" en el `README.md`).

## Seguridad

- **`hash_texto` (SHA-256 simple, sin sal) no es apto para guardar contraseñas** — es rápido y vulnerable a fuerza bruta con GPU / tablas arcoíris. Para eso existe `hash_seguro_contrasena` (PBKDF2 con sal, ver `FUNCTIONS.md`). Esto no es un bug, es una elección de diseño de `hash_texto` (pensado para huellas digitales de datos, no contraseñas), pero se menciona acá porque es un error fácil de cometer si no se lee la documentación de cada comando.
