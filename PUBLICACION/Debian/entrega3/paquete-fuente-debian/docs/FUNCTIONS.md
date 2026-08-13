# FUNCTIONS — Referencia de comandos de SiPi

Tabla completa de comandos del lenguaje, organizada por categoría. Para sintaxis general (bloques, expresiones, tipos), ver `SYNTAX.md` y `LANGUAGE_SPEC.md`. Para ver estos comandos en uso, ver `EXAMPLES.md` y la carpeta `ejemplos/`.

### Programa, variables y control de flujo
| Comando | Que hace |
|---|---|
| `programa "Nombre"` | Primera linea obligatoria de todo archivo `.sipi` |
| `variable x = expr` / `var x = expr` | Declara/reasigna una variable. Tipo opcional: `variable x: entero = expr` |
| `const x = expr` | Declara una constante (no se puede reasignar). Tambien admite tipo opcional |
| `sumar x expr` / `restar x expr` | Modifica una variable numerica existente (respeta el tipo si esta declarado) |
| `si ... sino ... fin` | Condicional |
| `mientras condicion ... fin` | Bucle mientras se cumpla la condicion |
| `repetir N veces ... fin` | Bucle de N iteraciones |
| `para_cada item en lista ... fin` | Recorre una lista |
| `romper` | Corta el bucle actual (break) |
| `continuar` | Salta a la siguiente iteracion (continue) |
| `funcion nombre(params) ... fin` | Define una funcion. Parametros y retorno con tipo opcional: `funcion suma(a: entero, b: entero) -> entero` |
| `devolver expr` | Devuelve un valor desde una funcion (se valida contra el tipo de retorno si esta declarado) |
| `llamar funcion(args)` | Llama a una funcion sin usar su resultado |
| `llamar_valor funcion(args) -> var` | Llama a una funcion y guarda el resultado |
| `lanzar_error "mensaje"` | Lanza una excepcion propia |
| `intentar ... capturar ... fin` | Manejo de errores (la variable `error` tiene el mensaje) |
| `importar "archivo.sipi"` | Importa otro archivo SiPi como modulo |
| `instalar_modulo "nombre_o_url"` | Descarga un `.sipi` suelto: por URL directa, o por nombre buscando en `SIPI_REGISTRO_MODULOS` |
| `instalar_repositorio "usuario/repo"` | Clona un repositorio completo de GitHub (varios `.sipi`) en `paquetes/<repo>/` |
| `buscar_paquete "tema"` | Busca repositorios reales en GitHub sobre un tema (API pública de GitHub, sin catalogo propio) y sugiere el `instalar_repositorio` para instalarlos |
| `listar_repositorios` | Muestra los paquetes de GitHub ya instalados con `instalar_repositorio` |
| `listar_modulos` / `desinstalar_modulo` | Lista o quita modulos instalados con `instalar_modulo` |
| `instalar_dependencias` | Lee `sipi_paquetes.json` en la carpeta del proyecto (equivalente a un `package.json`) e instala todos los modulos declarados de una sola vez. Ver `PACKAGES.md` |

### Listas, diccionarios, matrices y programacion funcional
| Comando | Que hace |
|---|---|
| `lista_crear nombre` | Crea una lista vacia. Tipada opcional: `lista_crear nombre: lista<entero>` |
| `lista_agregar lista valor` | Agrega un elemento (valida el tipo si la lista es tipada) |
| `lista_obtener lista indice -> var` | Obtiene un elemento por indice |
| `lista_eliminar lista indice` | Elimina un elemento |
| `lista_longitud lista -> var` | Cantidad de elementos |
| `lista_ordenar` / `lista_invertir` | Ordena/invierte una lista |
| `lista_contiene` | Verifica si un valor esta en la lista |
| `suma_lista` / `promedio_lista` / `minimo` / `maximo` | Estadisticas basicas |
| `lista_mapear lista con funcion -> var` | Aplica una funcion a cada elemento |
| `lista_filtrar lista con funcion -> var` | Filtra segun una funcion booleana |
| `lista_reducir lista con funcion desde inicial -> var` | Reduce a un solo valor |
| `lista_unir lista "separador" -> var` | Convierte a texto unido |
| `lista_aplanar lista -> var` | Aplana listas anidadas |
| `diccionario_crear` / `diccionario_asignar` / `diccionario_obtener` / `diccionario_tiene` / `diccionario_eliminar` / `diccionario_claves` | Diccionarios (clave-valor). Tipado opcional: `diccionario_crear nombre: diccionario<decimal>` |
| `matriz_crear` / `matriz_asignar` / `matriz_obtener` / `matriz_filas` / `matriz_columnas` | Matrices 2D |
| `enum Nombre ... fin` | Enumeraciones con valores automaticos |
| `estructura Nombre ... fin` / `instanciar` | Plantillas de datos reutilizables (como structs) |
| `clase Nombre [hereda_de Padre] [implementa Interfaz1, Interfaz2] ... fin` | Clase real con campos y metodos, con herencia e interfaces |
| `interfaz Nombre ... fin` | Declara metodos requeridos (sin implementarlos). Se verifica que la clase los tenga todos apenas se define (`implementa`), no recien al usarlos |
| `metodo nombre(params) ... fin` | Define un metodo dentro de una `clase` (usa `este` para el objeto) |
| `nuevo Clase(args) -> var` | Crea una instancia (llama a `constructor` si existe) |
| `llamar_metodo obj "nombre"(args) -> var` | Llama a un metodo de un objeto |
| `es_instancia_de obj Clase -> var` | Verifica el tipo de un objeto (incluyendo herencia) |

### Texto
| Comando | Que hace |
|---|---|
| `mayusculas` / `minusculas` | Cambia capitalizacion |
| `texto_dividir` / `texto_reemplazar` / `texto_contiene` | Manipulacion de texto |
| `texto_recortar` | Quita espacios al principio/final (trim) |
| `texto_empieza_con` / `texto_termina_con` | Prefijo/sufijo |
| `texto_repetir` | Repite un texto N veces |
| `longitud` | Largo de un texto o lista |
| `hash_texto` | Genera un hash |
| `tipo_de expr -> var` | Devuelve el tipo (texto/numero/lista/diccionario/booleano) |

### Numeros
| Comando | Que hace |
|---|---|
| `redondear` / `raiz` / `potencia` | Operaciones matematicas |
| `azar_entre` / `elegir_al_azar` / `aleatorio` | Numeros/valores al azar |

### Fechas
| Comando | Que hace |
|---|---|
| `fecha_hora_actual -> var` | Fecha y hora actual (`AAAA-MM-DD HH:MM:SS`) |
| `fecha_sumar_dias fecha N -> var` | Suma (o resta con N negativo) dias a una fecha |
| `fecha_diferencia_dias f1 f2 -> var` | Dias entre dos fechas |
| `fecha_es_mayor f1 f2 -> var` | Compara dos fechas |
| `fecha_formatear fecha "patron" -> var` | Formatea con un patron estilo strftime (ej. `"%d/%m/%Y"`) |
| `fecha_dia_semana fecha -> var` | Nombre del dia de la semana en español |

### Imagenes (necesitan `pip install Pillow`)
| Comando | Que hace |
|---|---|
| `imagen_info "archivo" -> var` | Ancho, alto, formato y modo de una imagen |
| `imagen_redimensionar "in" ancho alto "out"` | Redimensiona y guarda una copia |
| `imagen_convertir "in" "out"` | Convierte de formato (ej. png a jpg) |

### Audio (sin dependencias externas)
| Comando | Que hace |
|---|---|
| `audio_duracion "archivo.wav" -> var` | Duracion en segundos de un .wav |
| `audio_generar_tono frecuencia duracion "archivo.wav"` | Genera un tono puro |

### Archivos, datos y base de datos
| Comando | Que hace |
|---|---|
| `crear_archivo` / `leer_archivo` / `borrar_archivo` / `copiar_archivo` | Archivos de texto |
| `crear_carpeta` / `listar_archivos` | Carpetas |
| `comprimir_carpeta` / `descomprimir_zip` | Compresion |
| `guardar_dato` / `obtener_dato` / `borrar_dato` | Base de datos simple JSON (clave-valor) |
| `json_crear` / `json_leer` / `json_guardar` / `json_texto` | JSON |
| `csv_leer` / `csv_guardar` | CSV |
| `sqlite_conectar "archivo.db" como db` | Abre/crea una base SQLite real |
| `sqlite_ejecutar db "SQL"` | Ejecuta INSERT/UPDATE/CREATE/DELETE |
| `sqlite_consultar db "SELECT ..." en var` | Ejecuta un SELECT y devuelve una lista de diccionarios |
| `sqlite_cerrar db` | Cierra la conexion |

### Web (paginas y backend real)
| Comando | Que hace |
|---|---|
| `pagina_web ... fin` con `titulo`, `subtitulo`, `texto`, `enlace`, `lista_web`, `separador`, `tarjeta`, `tema`, `color`, `formulario`, `campo` | Genera una pagina HTML declarativa |
| `generar_pagina_web` | Guarda la pagina generada en disco |
| `iniciar_servidor_web "carpeta" puerto` | Levanta un servidor de archivos estaticos |
| `escuchar_ruta "/api/ruta" con funcion` | Registra una ruta de API |
| `iniciar_api_web puerto` | Levanta un backend HTTP real (GET/POST/PUT/DELETE) que despacha a funciones SiPi |
| `detener_api_web` | Apaga el servidor de API |

### Ventanas de escritorio (GUI)
| Comando | Que hace |
|---|---|
| `ventana ... fin` con `boton`, `etiqueta`, `entrada`, `imagen`, `cuadro`, `casilla`, `lista`, `barra_progreso`, `actualizar_barra`, `menu_desplegable`, `pestanias`/`pestana` | Interfaces graficas de escritorio (tkinter) |

### Juegos 2D
| Comando | Que hace |
|---|---|
| `crear_juego ... fin` con `sprite`, `sonido`, `tono`, `chocar`, `velocidad`, `puntaje_inicial`, `mostrar_puntaje`, `mover_aleatorio`, `gravedad`, `rebote`, `friccion`, `tamano_mundo`, `camara_seguir` | Motor de juegos 2D (pygame) |
| `ia`, `seguir`, `escapar`, `patrullar` | Comportamiento de IA para personajes/enemigos |
| `particulas`, `explosion`, `humo`, `fuego` | Efectos visuales |

### Sistema y utilidades
| Comando | Que hace |
|---|---|
| `ejecutar` / `esperar` | Ejecuta comandos del sistema / pausa |
| `reproducir_tono` | Sonido simple |
| `instalar_paquete` | Instala un paquete de Python (pip) que tu programa necesite |
| `obtener_url` | Peticion HTTP simple |
| `fecha_hora_actual` | Fecha y hora |
| `cada N segundos ... fin` / `detener_temporizador` | Temporizadores repetidos |
| `captura_pantalla` / `copiar_portapapeles` / `pegar_portapapeles` | Utilidades del sistema |
| `generar_app_android` / `generar_app_windows` | Empaquetado de apps |
| `modo_debug` | Activa impresion de cada linea ejecutada, para depurar |

## Concurrencia (hilos reales)

Threads reales de sistema operativo (`threading` de Python por dentro), no cooperativos. **Importante:** cada hilo trabaja con su propia copia de las variables globales tomada al momento de crearlo — no comparten estado en vivo con el resto del programa (ver `KNOWN_ISSUES.md` para el porqué). Comunicá resultados con `devolver`/`hilo_resultado`, no con variables globales.

| Comando | Qué hace |
|---|---|
| `hilo_crear funcion(args) -> id_hilo` | Corre una función en un hilo real, en paralelo, sin bloquear el resto del programa |
| `hilo_esperar id_hilo` | Bloquea hasta que ese hilo termine |
| `hilo_resultado id_hilo -> var` | Espera si hace falta y guarda lo que devolvió el hilo |
| `hilo_esta_vivo id_hilo -> var` | Revisa si sigue corriendo, sin bloquear |
| `hilo_esperar_todos` | Bloquea hasta que todos los hilos creados hasta ahora terminen |
| `bloqueo_crear nombre` | Crea un candado (lock) real para sincronizar acceso a un recurso compartido (archivo, conexión) |
| `con_bloqueo nombre ... fin` | Ejecuta el bloque con el candado tomado; se libera solo al salir, incluso si hay un error adentro |

```sipi
funcion descargar(url)
    peticion_http url -> respuesta
    devolver respuesta
fin

hilo_crear descargar("https://ejemplo.com/a") -> h1
hilo_crear descargar("https://ejemplo.com/b") -> h2
hilo_resultado h1 -> resultado_a
hilo_resultado h2 -> resultado_b
```

## Corrector automático y revisor de código (CLI)

Estos no son comandos dentro de un programa `.sipi`, son banderas de línea de comandos de `sipi.py`:

| Comando | Qué hace |
|---|---|
| `python sipi.py archivo.sipi` | Ejecuta el programa normalmente. Si encuentra errores tipográficos chicos (espacios de más, comillas curvas, un punto suelto, un comando mal escrito por poco como `decid`→`decir`), los corrige **en memoria** para esa corrida y te dice exactamente qué corrigió — el archivo en disco no cambia. |
| `python sipi.py --corregir archivo.sipi` | Corre el mismo corrector, pero **guarda** la versión corregida de vuelta en el archivo. Te lista todo lo que cambió antes de guardar. |
| `python sipi.py --revisar archivo.sipi` | Analiza el código (sin ejecutarlo) y da un reporte de seguridad, posibles bugs, estilo y sugerencias — ver detalle abajo. |
| `python sipi.py --formatear archivo.sipi` | Reindenta el archivo con 4 espacios por nivel (ya existía, ver `DOCUMENTACION.md`). |
| `python sipi.py --repl` (o `python sipi.py` sin argumentos) | Abre una consola interactiva: escribís código SiPi línea por línea y se ejecuta al toque, manteniendo variables/funciones/clases entre líneas. Soporta bloques multilínea (`si`/`funcion`/etc. se completan solos hasta su `fin`) y evalúa expresiones sueltas automáticamente (`2 + 2` imprime `4`, sin necesitar `decir`). También corrige y avisa errores tipográficos como en una ejecución normal. Salís con `salir`, `exit` o Ctrl+D. |
| `python sipi.py --depurar archivo.sipi` | Ejecuta el programa mostrando cada línea antes de correrla (igual que poner `modo_debug` como primera línea, pero sin editar el archivo). Combinable con `--sin-cache`. |

Todo esto también está disponible desde `sipi_cli.py` (o el comando `sipi` si lo tenés instalado así): `sipi repl`, `sipi corregir archivo.sipi`, `sipi analizar archivo.sipi`, `sipi depurar archivo.sipi`, `sipi formato archivo.sipi`, `sipi probar` (alias de `sipi test`).

### ¿Qué corrige el corrector automático?

- Espacios dobles/triples entre palabras (nunca dentro de un texto entre comillas — ahí el espacio es una decisión tuya).
- Comillas "curvas" (las que pone Word o el teclado del celular) cambiadas por comillas rectas, las únicas válidas en SiPi.
- Un punto suelto al final de una línea, que no forma parte de ningún texto.
- Espacios/tabs sobrantes al final de una línea.
- Un comando mal escrito por muy poco (ej. `decid` en vez de `decir`), **solo** cuando hay una única opción razonable — si es ambiguo, no toca nada y te deja el error normal de "comando desconocido" para que decidas vos.

### ¿Qué mira `--revisar`?

- **🔒 Seguridad:** credenciales escritas directo en el código (usar `variable_entorno` en su lugar), `hash_texto` usado sobre algo que parece una contraseña (usar `hash_seguro_contrasena`), consultas SQL armadas interpolando una variable directo en el texto (riesgo de inyección SQL).
- **🐛 Posibles bugs:** bloques `capturar` vacíos (un error que se atrapa pero no se hace nada con él), variables declaradas y nunca usadas, funciones definidas y nunca llamadas.
- **🎨 Estilo:** funciones muy largas, bloques anidados muchos niveles, comentarios `TODO`/`FIXME` que quedaron pendientes.
- **💡 Sugerencias:** operaciones riesgosas (archivos, red, bases de datos) sin ningún `intentar`/`capturar` en todo el programa; programas grandes sin ninguna prueba automatizada (`afirmar`).

Es un análisis básico y honesto sobre su propio alcance: agarra los problemas más comunes y más caros de cometer, no reemplaza revisar el código con atención vos mismo.

## Nota sobre esta referencia

Las categorías de Ventanas/Juegos/Web cubren muchísimos parámetros propios de cada bloque (por ejemplo, las opciones exactas de `sprite` o `tarjeta`). La forma más confiable de ver la sintaxis exacta de cada uno es mirar los ejemplos ya funcionando en la carpeta `ejemplos/`, que están probados y corren tal cual.

Para cualquier duda puntual sobre un comando que no esté 100% claro en esta referencia, la forma más rápida de confirmar la sintaxis exacta es abrir `sipi.py` y buscar `if cmd == "nombre_del_comando"` — cada instrucción del lenguaje está implementada ahí mismo, en español, con su propia expresión regular de sintaxis.
