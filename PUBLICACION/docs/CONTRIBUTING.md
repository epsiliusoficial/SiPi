# CONTRIBUTING — Cómo contribuir a SiPi

Gracias por probar SiPi. Esta guía es para testers y colaboradores: cómo reportar un bug, sugerir una función, contribuir código, y dónde preguntar.

## Reportar un bug

1. Fijate primero en [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) si ya es un problema conocido.
2. Si no está, abrí un Issue en GitHub usando la plantilla de "Bug report" (se completa sola al crear el issue — ver `.github/ISSUE_TEMPLATE/bug_report.md`).
3. Cuanto más específico, más rápido se soluciona. Como mínimo, incluí:
   - Sistema operativo (y distro, si es Linux — ej. "Arch Linux" no es lo mismo que "Ubuntu" para estos fines).
   - Versión de SiPi (la ves con `python sipi.py --version` o mirando `VERSION` en `sipi.py`).
   - Qué hiciste, qué esperabas que pasara, qué pasó en realidad.
   - El mensaje de error completo, tal cual lo mostró la consola (no un resumen).
   - Si podés, el archivo `.sipi` mínimo que reproduce el problema (mientras más chico, mejor).

## Sugerir una función nueva

Abrí un Issue con la plantilla de "Feature request" (`.github/ISSUE_TEMPLATE/feature_request.md`). Contá:
- Qué querés poder hacer que hoy no se puede.
- Cómo te imaginás la sintaxis (no hace falta que sea perfecta, es un punto de partida).
- Un caso de uso real, no solo la idea abstracta — ayuda mucho a evaluar si encaja con la filosofía del lenguaje (ver "¿Para quién es SiPi?" en el `README.md`).

## Contribuir código

1. Los comandos del lenguaje viven todos en `sipi.py`, como bloques `if cmd == "nombre_comando":`. Buscar un comando parecido al que querés agregar es la forma más rápida de entender el patrón.
2. Después de cualquier cambio, corré la suite de tests antes de mandar el cambio:
   ```bash
   python -m pytest tests/test_suite.py -v
   ```
   El CI (`.github/workflows/ci.yml`) corre esto mismo automáticamente en Windows/Linux/macOS con Python 3.10/3.11/3.12 en cada Pull Request — si falla ahí, no se va a poder mergear.
3. Si agregás un comando nuevo, agregalo también a:
   - `COMANDOS_CONOCIDOS` (para que el autocompletado y las sugerencias de error lo reconozcan).
   - El diccionario de ayuda de comandos (para que `ayuda "comando"` funcione).
   - `FUNCTIONS.md`, con su firma y un ejemplo.
   - Si tiene sentido, un ejemplo nuevo en `ejemplos/` y una fila en `EXAMPLES.md`.
4. Mandá el Pull Request contra `main`, con una descripción de qué cambia y por qué.

## Dónde hacer preguntas

Por ahora, la vía es abrir un Issue en GitHub etiquetado como pregunta (o usar Discussions si está habilitado en el repo). No asumas que un canal de Discord/comunidad ya existe — revisá el `README.md` del repo para ver los canales activos en el momento en que leas esto.

## Filosofía a tener en cuenta al contribuir

SiPi prioriza que alguien sin experiencia previa pueda escribir su primer programa rápido, en español, sin configurar nada. Antes de proponer un cambio que agregue complejidad (una nueva forma de hacer algo que ya se puede hacer, una dependencia externa nueva, etc.), vale la pena preguntarse si eso ayuda o entorpece ese objetivo. Ver el `README.md`, sección "¿Por qué existe SiPi?", para más contexto.
