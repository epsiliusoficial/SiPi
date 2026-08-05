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

## Nota sobre esta referencia

Las categorías de Ventanas/Juegos/Web cubren muchísimos parámetros propios de cada bloque (por ejemplo, las opciones exactas de `sprite` o `tarjeta`). La forma más confiable de ver la sintaxis exacta de cada uno es mirar los ejemplos ya funcionando en la carpeta `ejemplos/`, que están probados y corren tal cual.

Para cualquier duda puntual sobre un comando que no esté 100% claro en esta referencia, la forma más rápida de confirmar la sintaxis exacta es abrir `sipi.py` y buscar `if cmd == "nombre_del_comando"` — cada instrucción del lenguaje está implementada ahí mismo, en español, con su propia expresión regular de sintaxis.
