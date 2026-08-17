# CACHE — El sistema de caché de SiPi (`.sipic`)

Documento pedido explícitamente: qué guarda exactamente la caché, cuándo se crea/usa/actualiza/borra, y qué medidas de seguridad tiene (o no tiene).

## ¿Qué es?

Al ejecutar `programa.sipi`, SiPi parsea el archivo (saca comentarios, resuelve strings triples, infiere los `fin` por indentación si corresponde — ver `LANGUAGE_SPEC.md`). Ese parseo es barato para un programa chico, pero se nota en cada ejecución de un proyecto de miles de líneas. `programa.sipic` guarda el resultado YA parseado, para saltarse ese trabajo en la próxima corrida.

## ¿Qué guarda exactamente? (sé preciso, no lo asumas)

Un `.sipic` es un archivo **JSON en texto plano**, no bytecode binario ni nada ofuscado, con esta forma:

```json
{
  "version_sipi": "41.24.0",
  "tamano": 1234,
  "hash": "sha256 del contenido fuente completo",
  "lineas": [[1, "programa \"Mi programa\""], [2, ""], [3, "decir \"hola\""], ...]
}
```

`"lineas"` es la lista completa de `(número_de_línea, línea_ya_procesada)` — es decir, **tu código fuente, sin los comentarios, y con los `fin` inferidos por indentación ya agregados explícitamente.** No es una forma comprimida ni ilegible: si abrís un `.sipic` con un editor de texto, vas a poder leer el programa casi entero.

**Esto es intencional y honesto de nuestra parte decirlo así de claro:** la caché no fue diseñada para ocultar nada, es puramente una optimización de velocidad. Si tu objetivo es que el código no sea legible, la herramienta correcta es `proteger_codigo.py` / `generar_exe.py` (ver `KNOWN_ISSUES.md` y el propio código de esos dos, que fueron auditados y corregidos en esta misma revisión), no la caché.

## ¿Qué NO guarda?

- No guarda valores de variables, estado de ejecución, ni nada de "memoria en vivo" del programa mientras corre. La caché existe solo entre ejecuciones distintas, nunca durante una.
- No guarda datos temporales de la ejecución (archivos abiertos, conexiones de red/base de datos, etc.) — eso vive únicamente en memoria del proceso mientras el programa corre, y se descarta al terminar (ver la sección de gestión de memoria en `KNOWN_ISSUES.md`).
- No guarda credenciales ni nada que vos no hayas escrito ya en el propio `.sipi` (la caché es literalmente un reflejo del código fuente, ni más ni menos).

## ¿Cuándo se crea?

La primera vez que ejecutás un `.sipi` sin que exista ya un `.sipic` al lado (mismo nombre, misma carpeta), o corriendo `sipi_cli.py compilar` / `generar_docs.py` sobre un archivo.

## ¿Cuándo se usa (en vez de re-parsear)?

Solo si **las tres condiciones siguientes se cumplen a la vez**: existe el `.sipic`, la versión de SiPi que lo generó coincide con la que está corriendo ahora, Y el tamaño+hash SHA-256 del `.sipi` actual coincide exactamente con el que se guardó. Cualquier archivo `.sipic` corrupto, de otra versión de SiPi, o que no matchee el hash se ignora silenciosamente y SiPi vuelve a parsear normal — una caché rota o vieja **nunca** puede romper la ejecución del programa, en el peor caso solo se pierde la ventaja de velocidad esa vez.

## ¿Cuándo se actualiza?

Automáticamente, cada vez que el `.sipi` cambió respecto al `.sipic` existente (el hash no matchea): se vuelve a generar desde cero con el contenido nuevo. No hace falta borrarla a mano para que se actualice.

## ¿Cuándo se borra?

- Manualmente, borrándola vos (es un archivo normal, no tiene nada especial en el sistema de archivos).
- Corriendo con la bandera `--sin-cache`: `python sipi.py --sin-cache archivo.sipi` fuerza a ignorar cualquier `.sipic` existente y **no genera uno nuevo** en esa corrida — útil si sospechás que la caché está desincronizada.
- Automáticamente al usar el editor Visual (`editor_visual`) o `--corregir`: como esos modifican el `.sipi` directamente, la caché vieja quedaría desactualizada, así que se elimina para forzar un re-parseo limpio en la próxima ejecución.

## Separación de la caché respecto a datos "reales"

- La caché de bytecode (`.sipic`) es **exclusivamente** una copia procesada del código fuente. Vive al lado del `.sipi`, con el mismo nombre.
- Los datos que un programa SiPi guarda de verdad (bases SQLite, archivos JSON/CSV que el programa escribe con `guardar_dato`/`sqlite_*`/etc.) son archivos completamente aparte, creados explícitamente por comandos del programa, nunca mezclados con `.sipic`.
- La memoria en tiempo de ejecución (variables, pila de llamadas, conexiones abiertas) vive únicamente en el proceso de Python mientras corre — no se persiste en ningún lado salvo que el programa lo pida explícitamente con un comando de guardado.

## Higiene: que no termine expuesta por accidente

Como parte de esta revisión se corrigieron dos cosas relacionadas a esto:
- Se agregó `.gitignore` con `*.sipic` — antes no existía ningún `.gitignore` en el proyecto, así que estos archivos se hubieran terminado versionando en Git sin querer.
- `publicar.py` ahora excluye explícitamente `*.sipic`/`__pycache__` al copiar `ejemplos/` y `tests/` a la carpeta de distribución pública (`PUBLICACION/`), para que un archivo de caché generado durante el desarrollo no termine empaquetado en lo que se comparte.

## Sobre "investigar la caché de Farei" antes de hacerla central

El feedback marcaba explícitamente que la idea de caché de Farei merece evaluarse aparte, demostrando ventaja real antes de volverla una característica central. Este documento describe la caché **que ya existe y ya está en uso** (bytecode/parseo, no relacionada a IA/ML) — si "la caché de Farei" se refiere a otra propuesta distinta (por ejemplo, cachear resultados de un modelo de IA), eso es un tema aparte, sin implementar todavía, y efectivamente necesitaría su propio análisis de costo/beneficio antes de construirse.
