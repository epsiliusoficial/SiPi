# Instrucciones de empaquetado de SiPi para Vinari OS

Este documento acompaña al repositorio de SiPi y responde puntualmente
a lo que pidió Vinari Software: cómo debería empaquetarse el lenguaje.

## 1. Formato de entrega

SiPi se distribuye como **paquete Debian nativo** (`.deb`), separado en
cuatro binarios desde un único paquete fuente (`debian/control`,
adjunto en `debian/`):

| Paquete         | Contenido                                              | Depende de           |
|-----------------|----------------------------------------------------------|-----------------------|
| `sipi`          | Motor/runtime del intérprete, comando `sipi`, man page, completions, ícono, tipo MIME | `python3 (>= 3.10~)` |
| `sipi-cli`      | CLI profesional de gestión de proyectos (`sipi-cli`)      | `sipi`                |
| `sipi-editor`   | Editor visual GUI (`sipi-editor`), `.desktop`, integración de escritorio | `sipi`, `python3-tk` |
| `sipi-examples` | 47 programas de ejemplo listos para ejecutar               | `sipi`                |

Arquitectura: `all` en los cuatro (es Python puro, sin nada compilado
específico de una arquitectura).

## 2. Cómo reconstruir el paquete

```sh
sudo apt install debhelper devscripts dpkg-dev fakeroot
cd sipi-41.24.0/         # raiz del arbol fuente, con debian/ adentro
dpkg-buildpackage -us -uc -b
```

Esto genera `sipi_*.deb`, `sipi-cli_*.deb`, `sipi-editor_*.deb` y
`sipi-examples_*.deb` en el directorio padre.

**Importante para reproducibilidad**: reconstruir siempre desde el
mismo checkout (git clone o el `.tar.xz` de fuente generado con
`dpkg-buildpackage -S`), nunca desde una copia de carpeta hecha a mano
(`cp -r` entre sistemas de archivos puede reordenar el `tar` interno
del `.deb` aunque el contenido sea idéntico). Ver `debian/README.source`
para el detalle completo, verificado de forma empírica.

## 3. Verificación antes de aceptar el paquete

```sh
lintian --pedantic sipi_*.deb sipi-cli_*.deb sipi-editor_*.deb sipi-examples_*.deb
# esperado: 0 errores, 0 warnings (1 override documentado y explicado
# en debian/*.lintian-overrides, sobre un falso positivo de ortografia
# en espanol)

sudo apt install ./sipi_*.deb ./sipi-cli_*.deb ./sipi-editor_*.deb ./sipi-examples_*.deb
sipi --ayuda
man sipi
sipi /usr/share/sipi/examples/hola_mundo.sipi
```

También se incluye `debian/tests/` (formato `autopkgtest`) con 5
scripts de humo (uno por paquete + uno de integración de escritorio)
que corrimos en una instalación limpia real antes de esta entrega —
ver el resumen de resultados adjunto.

## 4. Licencia

SiPi tiene licencia propietaria (`debian/copyright`), pero incluye una
**excepción de distribución en paquetes** que autoriza explícitamente
este caso: cualquier distribución de sistema operativo puede incluir
SiPi en sus repositorios oficiales y redistribuirlo a sus usuarios,
siempre que:

1. Se redistribuya sin modificaciones al código fuente.
2. Se conserve el aviso de copyright/licencia íntegro (por ejemplo, el
   `debian/copyright` de este mismo paquete ya lo hace).
3. Se atribuya la autoría a Mateo -- NovaLab Corporation.
4. La distribución sea gratuita para el usuario final.

Texto completo en `LICENSE` (raíz del repositorio) y
`debian/copyright` (dentro de cada `.deb`, en
`/usr/share/doc/<paquete>/copyright`).

## 5. Datos de contacto y repositorio

`debian/control` y `debian/changelog` tienen placeholders
(`epsiliusoficial@gmail.com`, dominio reservado por RFC 2606 que nunca
resuelve a nada real) que hay que reemplazar por el contacto y el
repositorio real antes de la entrega definitiva a Vinari OS.
