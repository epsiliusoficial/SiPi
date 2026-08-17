# EXAMPLES — Índice de ejemplos

Todos los archivos están en `ejemplos/` y corren tal cual: `sipi.bat ejemplos/nombre.sipi` (Windows) o `python3 sipi.py ejemplos/nombre.sipi` (Linux/Mac). Organizados por tema, de más simple a más avanzado dentro de cada uno.

## Básicos

| Archivo | Qué muestra |
|---|---|
| `hola_mundo.sipi` | Variables, condicionales, bucles y funciones simples — el punto de partida |
| `funciones_recursivas.sipi` | Recursión real: factorial y fibonacci |
| `funciones_nuevas_v11.sipi` | Repaso de funciones incorporadas del lenguaje |
| `producto_con_errores.sipi` | `intentar`/`capturar`/`lanzar_error` — manejo de errores propio |
| `enum_y_estructuras.sipi` | `enum` y `estructura` para modelar datos (sistema de personajes) |
| `estructuras_recursivas.sipi` | Listas enlazadas/árboles y scoping real por llamada |
| `interfaces_v41_5.sipi` | Interfaces (`interfaz`, `implementa`) |
| `pattern_matching_v41_20.sipi` | `seleccionar`/`caso`/`otro` |
| `pipe_operator_v41_22.sipi` | Operador pipe `\|>` |
| `navegacion_segura_v41_21.sipi` | `nulo` y navegación segura con `?` |
| `tipos_avanzados_v41_2.sipi`, `tipos_y_fechas_v41.sipi`, `listas_tipadas_v41_1.sipi` | Sistema de tipos opcional (variables, listas, fechas) |
| `indentacion_opcional_v41_15.sipi` | Cerrar bloques con indentación en vez de `fin` |
| `modulo_utilidades.sipi` + `usar_modulo.sipi` | Crear e importar un módulo propio con `importar` |
| `docstrings_v41_24.sipi` | Documentar funciones con docstrings |
| `tutorial_interactivo.sipi` | Tutorial guiado dentro del propio lenguaje |

## GUI de escritorio

| Archivo | Qué muestra |
|---|---|
| `calculadora_gui.sipi` | Ventana básica con botones y campos numéricos |
| `calculadora_con_cuadro.sipi` | Cuadro de color + campos numéricos |
| `formulario_completo.sipi` | Todos los widgets disponibles en una `ventana` |
| `panel_con_pestanias.sipi` | Pestañas (`pestanias`/`pestana`) y menú desplegable |
| `panel_coordenadas_dinamicas.sipi` | Widgets ubicados con coordenadas calculadas dinámicamente |
| `lista_dinamica_gui.sipi` | Lista de productos generada en tiempo real dentro de una ventana |
| `lista_menu_dinamicos.sipi` | Lista de tareas + selector con datos dinámicos |
| `galeria_imagenes.sipi` | Mostrar imágenes reales en una ventana |
| `agenda_contactos.sipi` | GUI + base de datos real combinadas (agenda de contactos) |

## Juegos 2D

| Archivo | Qué muestra |
|---|---|
| `juego_simple.sipi` | Mover un cuadrado con las flechas — el punto de partida para juegos |
| `juego_avanzado.sipi` | Meta, obstáculo y puntaje |
| `juego_obstaculos_moviles.sipi` | Obstáculos que se mueven solos |
| `plataformas_fisica.sipi` | Física real: gravedad, rebote, fricción |
| `sprites_posiciones_dinamicas.sipi` | Enemigos en posiciones aleatorias reales |
| `enemigos_ia_particulas.sipi` | Comportamiento de IA (`seguir`, `escapar`, `patrullar`) + partículas |
| `sonido_generado.sipi` | Generar tonos/sonido sin archivos de audio externos |
| `tres_en_raya.sipi` | Juego de tablero con matrices reales (`matriz_crear`, etc.) |
| `escena_3d_basica_v41_7.sipi` | Renderer 3D de wireframes básico |

## Web

| Archivo | Qué muestra |
|---|---|
| `crear_sitio_web.sipi` | Generar y publicar un sitio localmente con `pagina_web` |
| `tienda_sin_html.sipi` | Página tipo tienda online sin escribir HTML a mano |
| `formulario_contacto_web.sipi` | Formulario web con tema oscuro y color personalizado |

## Archivos y datos

| Archivo | Qué muestra |
|---|---|
| `procesar_archivos_con_variables.sipi` | Leer/escribir archivos usando variables, no solo rutas literales |
| `inventario_json_csv.sipi` | JSON y CSV reales, compatibles con Excel |
| `lista_tareas.sipi` | Lista de tareas con funciones avanzadas (`lista_mapear`, `lista_filtrar`, etc.) |

## Bases de datos

| Archivo | Qué muestra |
|---|---|
| `base_de_datos.sipi` | Sistema de puntajes con persistencia real |
| `agenda_contactos.sipi` | Ver arriba (GUI + base de datos) |

> Los ejemplos de **SQLite real** (`sqlite_conectar`/`sqlite_consultar`) y **backend con API web** (`escuchar_ruta` + `iniciar_api_web`) están documentados con código completo en `CHANGELOG.md`, bajo las entradas de la v30.0 ("Ecosistema, datos reales y backend").

## Automatización

| Archivo | Qué muestra |
|---|---|
| `automatizacion.sipi` | Automatización general (ejecutar comandos, esperar, etc.) |
| `automatizacion_escritorio.sipi` | Automatización de escritorio (capturas, portapapeles) |
| `temporizadores.sipi` | Cuenta regresiva real con `cada N segundos` |

## Empaquetado / apps

| Archivo | Qué muestra |
|---|---|
| `generar_apps.sipi` | Generar apps empaquetadas (Android/Windows) desde un programa SiPi |

Ver también `ejemplos/MiPrimeraApp_android/` (proyecto Android vía Kivy ya armado) y `ejemplos/MiPrimerPrograma_windows/` (compilación a `.exe`).
