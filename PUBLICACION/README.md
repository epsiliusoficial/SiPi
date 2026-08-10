# SiPi

![version](https://img.shields.io/badge/versi%C3%B3n-41.24.0-blue)
![licencia](https://img.shields.io/badge/licencia-propietaria%20(todos%20los%20derechos%20reservados)-red)
![python](https://img.shields.io/badge/python-3.10%2B-blue)
![estado](https://img.shields.io/badge/estado-en%20desarrollo%20activo-brightgreen)

> Los badges de ⭐ estrellas e issues se agregan solos apenas el repo esté en GitHub — reemplazá `TU_USUARIO/TU_REPO` más abajo por la ruta real:
> `![stars](https://img.shields.io/github/stars/TU_USUARIO/TU_REPO?style=social)` · `![issues](https://img.shields.io/github/issues/TU_USUARIO/TU_REPO)`

**Un lenguaje de programación en español, pensado para que alguien sin experiencia previa pueda crear programas de verdad — interfaces gráficas, juegos, páginas web, bases de datos — sin pelearse primero con sintaxis en inglés ni configuración.**

```sipi
programa "Mi Primer Programa"

variable nombre = "Mateo"
decir "Hola, {nombre}! Esto es SiPi funcionando de verdad."

variable contador = 0
repetir 5 veces
    sumar contador 1
    decir "Contador: {contador}"
fin

si contador == 5
    decir "El contador llego a 5 correctamente."
sino
    decir "Algo salio mal."
fin

funcion saludar(persona)
    decir "Hola desde una funcion, {persona}!"
fin

llamar saludar("NovaLab")
```

Correlo con `sipi.bat mi_programa.sipi` (Windows) o `python3 sipi.py mi_programa.sipi` (Linux/Mac). Nada más que instalar Python.

### De cero a tu primer programa corriendo, en 3 pasos

1. Creá un archivo de texto llamado `hola.sipi` con esto adentro:
   ```sipi
   programa "Hola Mundo"

   funcion saludar(nombre)
       decir "Hola " + nombre
   fin

   llamar saludar("Mundo")
   ```
2. Abrí una terminal en esa misma carpeta.
3. Ejecutalo:
   ```
   $ python3 sipi.py hola.sipi
   Hola Mundo
   ```
   (en Windows, `sipi.bat hola.sipi` en vez de `python3 sipi.py hola.sipi`).

Eso es todo — no hay paso de compilación, ni configuración de proyecto, ni nada más que instalar antes (ver la sección de [Instalación](#instalación) más abajo si todavía no tenés SiPi puesto).

**¿Preferís un editor con resaltado de sintaxis y autocompletado en vez de la terminal?** Abrilo con `editor.bat` (Windows) o `python3 editor_sipi.py` (Linux/Mac) — requiere `tkinter` (ver [Instalación](#instalación)).

**¿Querés ver los ejemplos ya hechos en vez de escribir el tuyo?** Corré cualquiera de los de la carpeta `ejemplos/`, por ejemplo: `python3 sipi.py ejemplos/hola_mundo.sipi`. El índice completo está en [`EXAMPLES.md`](EXAMPLES.md).

---

## ¿Por qué existe SiPi?

Casi todos los lenguajes que se usan para enseñar a programar (Python, JavaScript, C) tienen su sintaxis, sus palabras clave y sus mensajes de error en inglés. Para alguien que recién arranca — sobre todo en una escuela o facultad de habla hispana — eso agrega una barrera extra que no tiene nada que ver con aprender a programar: primero hay que traducir, después entender.

SiPi saca esa barrera. Las palabras clave (`si`, `mientras`, `funcion`, `repetir`, `decir`), los mensajes de error y los ejemplos están en español desde el primer día. La idea no es reemplazar a Python — es ser el lenguaje en el que alguien piensa su primer programa, antes de pasar a lenguajes de propósito general.

## ¿Qué problema resuelve?

- **La barrera del idioma al aprender a programar.** El código se lee como una instrucción en español, no como un jeroglífico en inglés.
- **La fricción de armar una interfaz gráfica, un juego o una página web desde cero.** En la mayoría de los lenguajes eso implica librerías externas, configuración y bastante código repetitivo antes de ver algo en pantalla. En SiPi, `ventana ... fin` o `crear_juego ... fin` son parte del lenguaje mismo.
- **El miedo a "romper todo".** Los mensajes de error son en español y, si te equivocás escribiendo un comando, SiPi sugiere el nombre correcto (`¿Quisiste decir 'imprimir'?`).

## ¿Para quién fue creado?

- Estudiantes que están aprendiendo a programar por primera vez, en español.
- Docentes que quieren un lenguaje sin barrera de idioma para introducir lógica de programación.
- Cualquiera que quiera prototipar rápido una interfaz gráfica, un juego 2D simple o una página web sin escribir HTML/CSS a mano.

**SiPi no está pensado** para reemplazar Python/JavaScript en un entorno profesional, ni para software de alto rendimiento (ver [cuándo NO conviene usar SiPi](#cuándo-no-conviene-usar-sipi) más abajo).

### Filosofía: ¿para aprender, o de propósito general?

Las dos cosas, pero en ese orden. La prioridad número uno de SiPi es bajar la barrera de entrada para aprender a programar en español — esa es la razón por la que existe. Al mismo tiempo, no es un lenguaje "de juguete" limitado a ejercicios de clase: tiene POO real, tipos opcionales, manejo de errores, persistencia, y puede armar aplicaciones con interfaz gráfica, juegos y sitios web de verdad, así que alguien puede quedarse en SiPi bastante más tiempo del que tardaría un lenguaje puramente educativo antes de sentir que "ya lo superó". Pero si tuvieras que elegir un solo eje para evaluar si una función nueva encaja en SiPi, es ese primero: ¿ayuda a que alguien sin experiencia previa entienda y programe más rápido?

---

## ¿Qué puede hacer hoy?

- Lo básico de cualquier lenguaje: variables, condicionales, bucles, funciones (con recursión real), manejo de errores propios, tipos opcionales, pattern matching (`seleccionar`/`caso`).
- Programación orientada a objetos real: `clase`, herencia (`hereda_de`), interfaces (`implementa`), polimorfismo.
- Listas, diccionarios, matrices y programación funcional (`lista_mapear`, `lista_filtrar`, `lista_reducir`).
- Interfaces gráficas de escritorio (`ventana ... fin`, botones, listas, pestañas, barras de progreso) sin tocar tkinter directamente.
- Juegos 2D con físicas, IA simple y partículas (`crear_juego ... fin`, sobre pygame).
- Páginas web declarativas y un backend HTTP real (`pagina_web`, `iniciar_api_web`).
- Persistencia real: JSON, CSV, y SQLite (`sqlite_conectar`, `sqlite_consultar`).
- **Gestor de paquetes real, sin depender de un catálogo propio.** `instalar_modulo` baja un `.sipi` suelto por URL; `instalar_repositorio "usuario/repo"` clona un repositorio de GitHub completo con varios `.sipi`; `buscar_paquete "tema"` busca repos reales en GitHub (API pública, sin catálogo inventado); `instalar_dependencias` lee un manifiesto `sipi_paquetes.json` (equivalente a `package.json`) e instala todo de una. Ver [`PACKAGES.md`](PACKAGES.md).
- Un editor visual propio, extensión de VS Code con resaltado de sintaxis y autocompletado, servidor LSP, depurador con "viaje en el tiempo", formateador de código, caché de bytecode (~7x más rápido en ejecuciones repetidas), y un compilador a `.exe`.
- Suite de pruebas automatizadas (17 tests) que corre programas `.sipi` reales contra el motor.

## ¿Qué no puede hacer todavía?

- El gestor de paquetes no tiene un índice central curado tipo PyPI/npm — depende de que el paquete esté en un repo público de GitHub (lo cual cubre la gran mayoría de casos reales, pero no hay un catálogo oficial de "módulos recomendados").
- El soporte 3D es básico (renderer de wireframes), no un motor 3D completo.
- No hay instalador nativo para Linux/Mac tan pulido como el de Windows (`instalar.sh` existe pero es más nuevo y menos probado).
- El LSP valida estructura de bloques y autocompleta comandos, pero todavía no valida la sintaxis interna de cada comando individual, ni tiene "ir a la definición".
- Es un intérprete escrito en Python: el techo de rendimiento es el de Python, no el de un lenguaje compilado a nativo.

## ¿Cuál es su objetivo?

Que aprender a programar en español sea tan directo como aprender en inglés lo es hoy — y que ese primer programa, si el estudiante quiere, ya pueda tener una ventana, un botón y algo pasando en pantalla, no solo texto en una consola.

---

## Instalación

**Windows:**
1. Descomprimí el ZIP en una carpeta (ej. `C:\SiPi`).
2. Doble clic en `instalar.bat` (revisa Python, instala `pygame`, `pyinstaller`, `Pillow`).
3. Ejecutá con `sipi.bat mi_programa.sipi`, o abrí el editor visual con `editor.bat`.

**Linux / macOS:**
```bash
python3 sipi.py mi_programa.sipi
python3 editor_sipi.py   # requiere tkinter
```

Requisito: Python 3.10+.

## Tabla de características

| Característica | Estado |
|---|---|
| Variables, condicionales, bucles, funciones | ✅ |
| Recursión real | ✅ |
| POO real (clases, herencia, interfaces, polimorfismo) | ✅ |
| Tipos opcionales, pattern matching, manejo de errores | ✅ |
| GUI de escritorio (`ventana`) | ✅ |
| Juegos 2D (`crear_juego`) | ✅ |
| Editor visual (arrastrar y tocar para editar, ver `ventana`/`pagina_web`/`crear_juego`) | ✅ |
| Páginas web y backend HTTP | ✅ |
| SQLite / JSON / CSV | ✅ |
| Gestor de paquetes (vía GitHub, ver `PACKAGES.md`) | ✅ |
| Editor con resaltado y autocompletado propio | ✅ |
| Corrector automático de errores tipográficos (`--corregir`) | ✅ |
| Revisor de código: bugs, seguridad, estilo (`--revisar`) | ✅ |
| REPL interactivo (`--repl`) | ✅ |
| CLI con subcomandos (`sipi ejecutar/repl/depurar/analizar/...`) | ✅ |
| Concurrencia real (`hilo_crear`, `con_bloqueo`) | ✅ (cada hilo con su propia copia de variables, ver `KNOWN_ISSUES.md`) |
| Extensión de VS Code | ✅ |
| LSP (resaltado/autocompletado en cualquier editor compatible) | 🧪 (valida bloques y nombres de comando; todavía no valida sintaxis interna de cada comando ni tiene "ir a la definición" — ver `KNOWN_ISSUES.md`) |
| Depurador con viaje en el tiempo | ✅ |
| Compilación a ejecutable (`.exe`/binario) | ✅ |
| CI automatizado (tests en cada cambio) | ✅ |
| Índice curado de paquetes | ❌ (pendiente, ver Roadmap) |
| 3D | 🧪 (wireframe básico, no un motor 3D completo) |

| Plataforma | Estado | Notas |
|---|---|---|
| Windows 10/11 | ✅ | Instalador (`instalar.bat`), `.bat` para todo, la más probada |
| Linux | ✅ | Instalador (`instalar.sh`), probado en Ubuntu/Debian y Arch. `tkinter` (para el editor visual) hay que instalarlo aparte con el gestor de paquetes de tu distro |
| macOS | 🧪 | Corre igual que Linux (`instalar.sh` funciona ahí también), pero con menos testing real que Windows/Linux |
| Android | 🧪 | Experimental, vía Kivy (`generar_apps`) |

## ¿Por qué la primera versión pública es tan alta (v31+)?

Las versiones anteriores a la v31 corresponden al desarrollo interno y privado del proyecto — la primera versión publicada no representa el inicio histórico del desarrollo, sino el punto en el que se decidió abrirlo. El changelog completo, versión por versión, está en [`CHANGELOG.md`](CHANGELOG.md).

## ¿Interpretado o compilado? ¿Multiplataforma? ¿Open source?

- **Interpretado.** `sipi.py` lee y ejecuta un archivo `.sipi` directamente. También existe una caché de bytecode propia (`.sipic`) que acelera ejecuciones repetidas del mismo archivo (no confundir con compilación a nativo).
- **Compilable a ejecutable.** `generar_exe.py` empaqueta un programa `.sipi` en un `.exe`/binario standalone usando PyInstaller — no requiere que quien lo reciba tenga Python instalado.
- **Multiplataforma en su núcleo** (Windows, Linux, macOS, ya que corre sobre Python), con soporte experimental para Android vía Kivy. `instalar.bat` (Windows) e `instalar.sh` (Linux/Mac) hacen las mismas comprobaciones reales (Python, pip, dependencias) y no dicen "completado" si algo falló — ver la tabla de plataformas más arriba para el detalle fino de qué está más probado en cada una.
- **Código abierto** para desarrollo. Existe además un modo "protegido" (`proteger_codigo.py`) para cuando alguien quiere distribuir una app hecha en SiPi sin exponer el intérprete completo — pensado para publicar proyectos de terceros, no para ocultar el lenguaje en sí.

## Comparación rápida

| | SiPi | Python | JavaScript | Lua |
|---|---|---|---|---|
| Palabras clave | Español | Inglés | Inglés | Inglés |
| Curva de entrada | Muy baja | Baja | Media | Baja |
| GUI de escritorio integrada al lenguaje | Sí (`ventana`) | No (requiere tkinter aparte) | No | No |
| Motor de juegos 2D integrado | Sí (`crear_juego`) | No (requiere pygame aparte) | No (requiere librería) | No (requiere Love2D) |
| Ecosistema de paquetes | Incipiente | Enorme (PyPI) | Enorme (npm) | Chico |
| Rendimiento | El de Python (más caché de bytecode propia) | Referencia | Más rápido (V8) | Más rápido |
| Uso recomendado | Aprender a programar en español, prototipos rápidos | Propósito general, producción | Web, producción | Scripting embebido, juegos |

## Cuándo NO conviene usar SiPi

- Si el objetivo final es conseguir trabajo como programador: en ese caso conviene aprender la lógica acá si ayuda, pero el destino final debería ser Python/JavaScript/lo que pida el mercado.
- Software que necesita rendimiento serio (procesamiento pesado, tiempo real estricto, miles de usuarios concurrentes): SiPi hereda el techo de rendimiento de Python.
- Proyectos que dependen de un ecosistema de librerías maduro: el de SiPi todavía es chico.
- Equipos grandes con necesidad de herramientas de tipado estricto, tooling corporativo, CI/CD complejo, etc.: la base ahí es más sólida en lenguajes establecidos.

---

## Documentación

| Documento | Para qué sirve |
|---|---|
| [`DOCUMENTACION.md`](DOCUMENTACION.md) | Guía de instalación, tutorial completo desde cero, guía de sintaxis y referencia de comandos |
| [`LANGUAGE_SPEC.md`](LANGUAGE_SPEC.md) | Especificación del lenguaje: gramática, tipos, semántica |
| [`SYNTAX.md`](SYNTAX.md) | Referencia rápida de sintaxis (bloques, comentarios, expresiones) |
| [`FUNCTIONS.md`](FUNCTIONS.md) | Referencia de todos los comandos, como una tabla de funciones |
| [`EXAMPLES.md`](EXAMPLES.md) | Índice de los ejemplos en `ejemplos/`, organizados por categoría |
| [`PACKAGES.md`](PACKAGES.md) | Cómo funciona el gestor de paquetes real de SiPi (`instalar_modulo`, `instalar_repositorio`, `buscar_paquete`, `sipi_paquetes.json`) |
| [`GLOSSARY.md`](GLOSSARY.md) | Terminología internacional: qué nombre tiene en inglés cada concepto de SiPi (`lambda`, `closure`, `callback`, etc.) |
| [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) | Problemas y limitaciones conocidas, para no reportar algo que ya sabemos |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Cómo reportar bugs, sugerir funciones, y contribuir código |
| [`AI_GUIDE.md`](AI_GUIDE.md) | Guía para que un asistente de IA (ChatGPT, Claude, etc.) entienda y genere código SiPi correctamente |
| [`PROMPTS.md`](PROMPTS.md) | Prompts ya armados para pedirle código SiPi a un asistente de IA |
| [`CHANGELOG.md`](CHANGELOG.md) | Historial completo de versiones |

## Roadmap

**Ya hecho:** editor visual, intérprete, compilador a ejecutable, GUI de escritorio, motor de juegos 2D, POO real, tipos opcionales, pattern matching, LSP, extensión de VS Code, depurador con viaje en el tiempo, caché de bytecode, runtime móvil (Android/Kivy).

**Pendiente:**
- [ ] Más testing real en macOS (el instalador y el intérprete deberían andar igual que en Linux, pero con menos casos probados)
- [ ] Catálogo/índice oficial curado de módulos recomendados (hoy el descubrimiento es vía `buscar_paquete` sobre GitHub, sin curaduría)
- [ ] Módulos oficiales mantenidos por el proyecto
- [ ] LSP: validación de sintaxis interna por comando, "ir a la definición"
- [ ] Publicación directa de sitios generados a internet (hosting con un clic)
- [ ] Importaciones entre archivos `.sipi` más maduras
- [ ] Mejoras de IA integradas al editor (sugerencias contextuales)

## Licencia

Propietaria — todos los derechos reservados. Solo el autor puede redistribuir el intérprete/código fuente de SiPi. Ver [`LICENSE`](LICENSE) para el texto completo.

Nota: eso no impide que uses SiPi para hacer y distribuir tus propios programas — un `.sipi` que escribís vos, o un `.exe` que compilás con `generar_exe.py`, son tuyos y los repartís como quieras. La restricción es sobre el lenguaje/intérprete en sí, no sobre lo que la gente construya con él.

## Estructura del proyecto

```
SiPi/
├── sipi.py                 <- el intérprete (motor real del lenguaje)
├── sipi.bat / sipi_cli.py   <- ejecutar archivos .sipi
├── editor_sipi.py            <- editor visual
├── generar_exe.py             <- compilador a .exe
├── sipi_lsp.py                 <- servidor LSP
├── vscode-sipi/                 <- extensión de VS Code
├── tests/                        <- suite de pruebas automatizadas
├── instalar.bat / instalar.sh
├── ejemplos/                      <- programas de ejemplo (ver EXAMPLES.md)
├── README.md                       <- este archivo
├── DOCUMENTACION.md
├── CHANGELOG.md
├── LANGUAGE_SPEC.md
├── SYNTAX.md
├── FUNCTIONS.md
├── EXAMPLES.md
├── AI_GUIDE.md
└── PROMPTS.md
```

— Epsilius (Novalab Corporation)
