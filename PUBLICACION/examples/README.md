# Ejemplos de SiPi

47 programas de ejemplo, organizados por categoría (antes estaban todos
sueltos en una sola carpeta):

| Carpeta | Contenido |
|---|---|
| `01_Fundamentos/` | Lo básico: hola mundo, funciones, recursión, módulos, manejo de errores, tutorial interactivo |
| `02_Funciones_Del_Lenguaje/` | Demos de features específicas del lenguaje por versión: tipos, enums, pattern matching, pipe operator, navegación segura, docstrings |
| `03_Interfaces_Graficas/` | Calculadoras, listas dinámicas, formularios y paneles con ventanas reales (Tkinter) |
| `04_Videojuegos/` | Juegos completos: tres en raya, plataformas con física, enemigos con IA, sprites |
| `05_Graficos_3D/` | Renderer de wireframe 3D |
| `06_Audio/` | Generación de sonido |
| `07_Web/` | Sitios y formularios generados con SiPi |
| `08_Apps_Moviles_Y_Escritorio/` | Generación de apps para Android/escritorio |
| `09_Bases_De_Datos_Y_Archivos/` | SQLite, JSON, CSV, agendas |
| `10_Automatizacion/` | Automatización de archivos y de escritorio |

## Nota sobre archivos generados

Algunos ejemplos (`automatizacion.sipi`, `agenda_contactos.sipi`,
`base_de_datos.sipi`, `procesar_archivos_con_variables.sipi`,
`producto_con_errores.sipi`, y los de `07_Web`/`08_Apps_Moviles...`)
CREAN sus propios archivos y carpetas de salida la primera vez que se
corren (`sipi_datos.json`, `historial.log`, `documentos/`, `salida/`,
sitios web generados, proyectos Android generados). Esos archivos NO
se incluyen en esta colección -- se generan solos al ejecutar el
ejemplo correspondiente, en el directorio desde el que lo corras.

## Cómo correr un ejemplo

```sh
sipi 04_Videojuegos/tres_en_raya.sipi
```
