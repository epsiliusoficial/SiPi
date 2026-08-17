# PACKAGES — Gestor de paquetes de SiPi

SiPi ya tiene un gestor de paquetes real, apoyado en GitHub en vez de un índice propio (no requiere infraestructura propia para funcionar). Este documento explica las cuatro formas de instalar código de terceros y el formato del manifiesto de dependencias.

## 1. Instalar un archivo `.sipi` suelto

```sipi
instalar_modulo "https://raw.githubusercontent.com/usuario/repo/main/util.sipi"
```

Descarga ese archivo y lo guarda en `modulos_instalados/util.sipi`. También podés instalarlo directamente con un alias de importación:

```sipi
instalar_modulo "https://.../util.sipi" como util
// ya queda importado, listo para usar
```

Si en vez de una URL pasás solo un nombre:

```sipi
instalar_modulo "telegram"
```

SiPi busca `telegram.sipi` en el registro configurado por la variable de entorno `SIPI_REGISTRO_MODULOS` (vos elegís qué URL base usar — no hay un registro central impuesto).

## 2. Instalar un repositorio completo de GitHub

Cuando un paquete tiene varios archivos `.sipi` (no uno solo), se instala el repo entero:

```sipi
instalar_repositorio "usuario/repo"
instalar_repositorio "usuario/repo" rama desarrollo
instalar_repositorio "https://github.com/usuario/repo"
```

Se descarga en `paquetes/<repo>/`. Para ver qué está instalado así:

```sipi
listar_repositorios
```

## 3. Buscar paquetes sin saber el nombre exacto

```sipi
buscar_paquete "juegos"
```

Usa la API pública de GitHub para encontrar repositorios reales relacionados con el tema — no hay un catálogo curado propio de SiPi, así que los resultados son cualquier repo público de GitHub que matchee la búsqueda. El comando imprime, para cada resultado, la línea exacta de `instalar_repositorio` para instalarlo.

## 4. Instalar todas las dependencias de un proyecto a la vez

Creá un archivo `sipi_paquetes.json` en la carpeta del proyecto (el equivalente de un `package.json` de Node o `requirements.txt` de Python):

```json
{
  "modulos": {
    "telegram": "https://raw.githubusercontent.com/usuario/repo/main/telegram.sipi",
    "reconocimiento_facial": "reconocimiento_facial"
  }
}
```

Cada valor puede ser una URL directa, o solo un nombre (se busca en `SIPI_REGISTRO_MODULOS`). Después, en tu programa o desde la CLI:

```sipi
instalar_dependencias
```

Instala todas las dependencias declaradas de una sola vez, y avisa cuáles fallaron sin frenar el resto.

## Gestionar módulos ya instalados

```sipi
listar_modulos
desinstalar_modulo "telegram"
```

## Publicar tu propio paquete

No hace falta pedir permiso ni subir nada a un índice central: alcanza con tener tu(s) archivo(s) `.sipi` en un repositorio público de GitHub (o cualquier URL accesible — un gist, tu propia web). Cualquiera puede instalarlo con `instalar_modulo`/`instalar_repositorio` apuntando a esa URL o repo. Esto es intencional: SiPi no controla ni modera lo que se publica, así que revisá el código de un paquete de terceros antes de instalarlo, como harías con cualquier paquete de npm o PyPI de un autor que no conocés.

## Limitación actual (honesta)

No hay todavía un índice/catálogo oficial y curado de "módulos recomendados para SiPi" — el descubrimiento vía `buscar_paquete` depende pura y exclusivamente de la búsqueda de GitHub, sin ranking de calidad ni verificación. Es una mejora pendiente del roadmap (ver `README.md`), no algo que este documento deba simular como si ya existiera.
