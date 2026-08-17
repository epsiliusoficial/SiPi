# SiPi para empresas

Resumen corto de por qué una empresa podría evaluar SiPi como lenguaje
interno, y qué necesita saber antes de decidirlo. No es material de
marketing -- es una lista honesta de lo que hay y lo que falta.

## Lo que ya tiene, hoy, verificable en este repo

- **Motor real, sin dependencias externas** (`src/sipi.py`) -- corre en
  cualquier maquina con Python 3, sin instalar nada mas.
- **Tipado opcional** (`variable x: entero = 10`) para el codigo que lo
  necesita, sin forzarlo en todo el programa.
- **POO real** (`clase`, `hereda_de`, `interfaz`/`implementa`, `metodo`).
- **Base de datos real** (SQLite integrado) y **backend HTTP real**
  (`iniciar_api_web`, `escuchar_ruta`) -- no son mocks educativos, son
  las mismas librerias que usaria un backend en Python.
- **Concurrencia real** (hilos de sistema operativo, no cooperativos)
  -- ver `docs/FUNCTIONS.md#concurrencia-hilos-reales` para las
  limitaciones (cada hilo copia su estado global al crearse).
- **LSP server** (`src/sipi_lsp.py`) -- autocompletado, diagnosticos y
  navegacion en cualquier editor que hable el protocolo LSP (VS Code,
  Neovim, etc.), no solo en el editor propio de SiPi.
- **Analizador estatico** (`--revisar`) y **formateador automatico**
  (`--formato`) integrados al motor, sin instalar un linter aparte.
- **Suite de tests / benchmarks** propios (`sipi_cli.py test`,
  `sipi_cli.py benchmarks`) para tener numeros reales de rendimiento
  antes de decidir, no promesas.
- **Despliegue estandar**: generacion de `Dockerfile` real desde el
  propio motor (ver `_generar_dockerfile` en `src/sipi.py`), asi que un
  programa SiPi se empaqueta y corre en cualquier nube o Kubernetes
  igual que cualquier otro servicio containerizado.
- **Codigo protegido para distribucion** (`herramientas/proteger_codigo.py`
  con `--publicacion`) -- para una empresa que quiera distribuir
  herramientas internas hechas en SiPi sin repartir el codigo fuente
  en texto plano a cada estacion de trabajo.
- **Licencia con excepcion de redistribucion** (ver `LICENSE`) que
  permite a distribuciones de sistema operativo empaquetar SiPi sin
  modificar, bajo condiciones explicitas -- pensado para que una
  empresa pueda integrarlo a su propio entorno sin ambiguedad legal.

## Por que "sintaxis en español" no es solo un gesto cosmetico

Para un equipo hispanohablante (o mixto), bajar la barrera de entrada
entre "sabe programar" y "puede leer y auditar este script puntual" es
un beneficio operativo real: un analista de datos, un administrativo,
o alguien de soporte puede leer y modificar un script SiPi sin ser
programador de profesion, de la misma forma que SQL o una macro de
Excel son accesibles a perfiles no-dev. Eso no reemplaza al equipo de
ingenieria en sistemas grandes, pero reduce dependencia del equipo de
IT para automatizaciones chicas y medianas.

## Lo que falta, honestamente, antes de un despliegue de produccion serio

Esto es una lista de gaps reales, no una lista para completar en esta
sesion -- una empresa evaluando SiPi para algo mas que scripts internos
deberia pedir/priorizar:

- **Sin gestor de paquetes con registro central propio** (hay
  `instalar_paquete`/`instalar_repositorio` sobre pip/GitHub, no un
  registro curado de modulos SiPi).
- **Sin story de CI/CD documentada** mas alla de "corre en Docker" --
  falta una guia de integracion con pipelines tipo GitHub Actions/
  GitLab CI especifica para proyectos SiPi.
- **Sin auditoria de seguridad externa** del motor -- el analizador
  estatico (`--revisar`) ayuda pero no reemplaza un audit real.
- **Ecosistema chico**: comparado con Python/JS/Go, hay muy pocos
  paquetes de terceros y poca comunidad -- para necesidades muy
  especificas (ML pesado, integraciones de nicho) probablemente haga
  falta interoperar con Python directo en vez de esperar un paquete
  SiPi nativo.
- **Sin soporte comercial/SLA** formal todavia -- es un proyecto de un
  desarrollador, no una empresa con equipo de soporte dedicado.

## Como probarlo sin comprometerse

1. `python3 src/sipi_cli.py benchmarks` -- numeros de rendimiento reales
   en la maquina de quien evalua, no numeros de marketing.
2. `python3 src/sipi_cli.py test` -- correr la suite de regresion propia
   para ver que el motor se mantiene estable entre versiones.
3. Portar un script interno chico (automatizacion, reporte, scraping
   simple) y medir cuanto tiempo lleva vs. la version en el lenguaje
   actual del equipo.
4. Generar el `Dockerfile` de un programa de prueba y confirmar que
   arranca igual en el entorno de despliegue real de la empresa.
