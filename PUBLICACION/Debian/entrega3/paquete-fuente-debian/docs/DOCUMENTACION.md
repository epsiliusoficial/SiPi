# Documentacion oficial de SiPi (v41.4)

Indice:
1. [Guia de instalacion](#1-guia-de-instalacion)
2. [Tutorial desde cero](#2-tutorial-desde-cero)
3. [Guia de sintaxis](#3-guia-de-sintaxis)
4. [Referencia de comandos](#4-referencia-de-comandos)
5. [Ejemplos por nivel](#5-ejemplos-por-nivel)

---

## 1. Guia de instalacion

### Requisitos
- Python 3.10 o superior instalado (con "Add Python to PATH" marcado en
  Windows, y con "tcl/tk and IDLE" tildado si queres usar el editor
  visual).

### Pasos (Windows)
1. Descomprimi el ZIP de SiPi en una carpeta, por ejemplo `C:\SiPi`.
2. Doble clic en `instalar.bat`. Esto revisa que Python este instalado,
   y descarga las librerias opcionales (`pygame` para juegos,
   `pyinstaller` para compilar a `.exe`, `Pillow` para imagenes).
3. Listo. Ya podes:
   - Ejecutar un programa: doble clic en `sipi.bat`, o
     `sipi.bat mi_programa.sipi` desde una terminal.
   - Abrir el editor visual: doble clic en `editor.bat`.
   - Compilar un programa a `.exe`: `compilar_programa.bat mi_programa.sipi`.

### Pasos (Linux / macOS)
```bash
python3 sipi.py mi_programa.sipi
python3 editor_sipi.py       # requiere tkinter instalado
```

### Publicar/distribuir tu propio proyecto hecho en SiPi
Corre `publicar.bat` (o `python publicar.py`). Esto arma una carpeta
`PUBLICACION/` limpia, con el motor de SiPi protegido (sin codigo fuente
legible) y todos los `.bat` ya apuntando a los archivos correctos. Esa
es la carpeta que subis/compartis, nunca la carpeta de desarrollo
completa.

> **Importante:** `PUBLICACION/` es para distribuir un PROGRAMA HECHO EN
> SiPi (tu app terminada), no el proyecto SiPi en si. Si estas subiendo
> el repositorio de SiPi a GitHub para que otros lo vean/contribuyan, el
> `README.md` tiene que estar en la raiz del repo (donde esta ahora),
> nunca adentro de una carpeta `PUBLICACION/` -- GitHub solo muestra
> automaticamente el README que esta en la raiz.

---

## 2. Tutorial desde cero

Todo programa de SiPi empieza con una linea `programa "Nombre"`. Los
bloques (funciones, condicionales, bucles) se pueden cerrar de dos
formas, mezclables libremente: escribiendo `fin` explicito (el estilo
de siempre), o con indentacion consistente y sin `fin` (como Python) --
ver la seccion **2.9 — Indentacion opcional** mas abajo para el detalle.
Los ejemplos de este tutorial usan `fin` explicito por claridad.

### 2.1 — Hola mundo
```sipi
programa "MiPrimerPrograma"
decir "Hola, mundo!"
```

### 2.2 — Variables y operaciones
```sipi
programa "Variables"
variable nombre = "Mateo"
variable edad = 20
sumar edad 1
decir "{nombre} tiene {edad} años"
```
`sumar`/`restar` modifican una variable existente. Para crear una
constante que no se puede reasignar despues, usa `const` en vez de
`variable`.

### 2.3 — Condicionales
```sipi
programa "Condicionales"
variable edad = 20
si edad >= 18
    decir "Sos mayor de edad"
sino
    decir "Sos menor de edad"
fin
```

### 2.3b — Pattern matching con `seleccionar`

Para comparar un mismo valor contra varias opciones, `seleccionar` es
mas limpio que anidar muchos `si`:
```sipi
programa "Dias"
variable dia = "viernes"
seleccionar dia
    caso "lunes"
        decir "Odio los lunes"
    caso "viernes"
        decir "Por fin!"
    otro
        decir "Dia normal"
fin
```
Se ejecuta el primer `caso` cuyo valor sea igual al de `seleccionar`
(comparando con `==`). Si ninguno coincide, se ejecuta `otro` (opcional).
`caso` y `otro` son continuaciones del mismo bloque, como `sino` -- no
hace falta darles su propio `fin`.

### 2.4 — Bucles, `romper` y `continuar`
```sipi
programa "Bucles"
variable i = 0
mientras i < 10
    sumar i 1
    si i == 3
        continuar
    fin
    si i == 7
        romper
    fin
    imprimir i
fin

repetir 5 veces
    decir "Otra vuelta"
fin
```

### 2.5 — Funciones (y llamadas dentro de expresiones)
```sipi
programa "Funciones"
funcion doble(x)
    devolver x * 2
fin

variable resultado = doble(21)   # las llamadas a funciones funcionan
                                   # dentro de cualquier expresion
imprimir resultado                 # 42

funcion factorial(n)
    si n <= 1
        devolver 1
    fin
    devolver n * factorial(n - 1)   # recursion real
fin
imprimir factorial(6)                 # 720
```

### 2.6 — Listas y programacion funcional
```sipi
programa "Listas"
lista_crear numeros
lista_agregar numeros 1
lista_agregar numeros 2
lista_agregar numeros 3

funcion doble(x)
    devolver x * 2
fin

lista_mapear numeros con doble -> dobles
imprimir dobles   # [2, 4, 6]
```

### 2.7 — Manejo de errores propios
```sipi
programa "Errores"
funcion validar_edad(edad)
    si edad < 0
        lanzar_error "La edad no puede ser negativa"
    fin
    devolver edad
fin

intentar
    llamar_valor validar_edad(-5) -> resultado
capturar
    decir "Error: {error}"
fin
```

### 2.8 — Tipos opcionales (para cuando el proyecto crece)

Todo lo anterior funciona sin declarar ningun tipo — SiPi es dinamico por
defecto, como siempre. Pero si tu proyecto crece y queres que SiPi te
avise apenas metas un dato del tipo equivocado (en vez de descubrirlo
mas tarde con un bug raro), podes anotar el tipo con `:` donde declares
algo. Es 100% opcional y se puede mezclar con codigo sin anotar.

```sipi
programa "TiposOpcionales"

// Variables y constantes
variable edad: entero = 20
const nombre: texto = "Mateo"

// Listas y diccionarios con un solo tipo de elemento/valor
lista_crear puntajes: lista<entero>
lista_agregar puntajes 90
lista_agregar puntajes 85

diccionario_crear precios: diccionario<decimal>
diccionario_asignar precios "pan" 2.5

// Funciones: tipo de cada parametro y tipo de retorno
funcion cuadrado(x: entero) -> entero
    devolver x * x
fin
llamar_valor cuadrado(6) -> resultado
decir "6 al cuadrado: {resultado}"
```

Tipos disponibles: `entero`, `decimal`, `numero` (entero o decimal),
`texto`, `booleano`, `lista`, `diccionario`. Si en algun momento el
programa intenta asignar un valor de otro tipo a algo anotado, SiPi
corta con un error claro que dice exactamente que variable, parametro o
retorno fallo — en vez de dejar pasar el bug para mas adelante.

### 2.9 — Indentacion opcional (alternativa a `fin`) y reasignar sin `variable`

SiPi acepta dos estilos para cerrar bloques, mezclables en el mismo
archivo:

```sipi
programa "DosEstilos"

// Estilo clasico: 'fin' explicito
funcion cuadrado(x)
    devolver x * x
fin

// Estilo nuevo: indentacion consistente, sin 'fin' (como Python)
variable i = 0
mientras i < 3
    decir "Hola {i}"
    sumar i 1

decir "Listo"
```

Un bloque en particular usa indentacion si su primera linea de cuerpo
esta mas sangrada que la linea que lo abre; si no, sigue exigiendo su
`fin` de siempre. No hay que elegir un estilo para todo el archivo.

Ademas, reasignar una variable que ya existe no necesita repetir la
palabra `variable`:
```sipi
variable puntaje = 0
puntaje = 10        // valido: 'puntaje' ya existia
decir "{puntaje}"
```
`variable` sigue siendo obligatorio solo para la primera declaracion.

---

## 3. Guia de sintaxis

- **Bloques**: toda instruccion que abre un bloque (`si`, `sino`,
  `mientras`, `repetir ... veces`, `funcion`, `para_cada`, `intentar`,
  `enum`, `estructura`, `ventana`, `crear_juego`, `pagina_web`,
  `formulario`, `pestanias`/`pestana`, `cada ... segundos`) se cierra
  siempre con `fin`, y pueden anidarse libremente.
- **Comentarios**: de una linea con `//` (todo lo que sigue en esa
  linea se ignora), y de bloque con `/* ... */` (puede abarcar varias
  lineas).
- **Texto e interpolacion**: los strings van entre comillas dobles y
  soportan `{variable}` o `{funcion(x)}` adentro para insertar valores
  en tiempo real: `decir "Hola {nombre}, tenes {edad} años"`. Nota: por
  ahora no se puede escapar una comilla doble dentro de un string con
  `\"` (queda tal cual, con la barra); si necesitas comillas dentro de
  un texto, usa comillas simples `'` para ese fragmento.
- **Expresiones**: soportan operadores matematicos (`+ - * /`),
  comparaciones (`== != < > <= >=`), concatenacion de texto con `+`, y
  llamadas a funciones definidas por el usuario, incluso anidadas
  (`suma_uno(doble(3))`).
- **Asignacion a variable con `->`**: muchos comandos que calculan un
  valor lo entregan con la sintaxis `comando argumentos -> variable`
  (por ejemplo `lista_mapear numeros con doble -> dobles`,
  `sqlite_consultar db "SELECT ..." en filas`).
- **Constantes**: declaradas con `const` (o creadas automaticamente por
  `enum`/`estructura`) no se pueden reasignar; intentarlo lanza un
  error claro.
- **Errores con sugerencias**: si escribis mal el nombre de un comando,
  SiPi te sugiere el mas parecido ("Comando desconocido: 'imprimr'.
  ¿Quisiste decir 'imprimir'?").

---

## 4. Referencia de comandos

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
| `instalar_modulo "nombre_o_url"` | Descarga un modulo `.sipi` (administrador de paquetes) |

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

> Nota sobre esta referencia: las categorias de Ventanas/Juegos/Web
> cubren muchisimos parametros propios de cada bloque (por ejemplo, las
> opciones exactas de `sprite` o `tarjeta`). La forma mas confiable de
> ver la sintaxis exacta de cada uno es mirando los ejemplos ya
> funcionando en la carpeta `ejemplos/`, que estan probados y corren
> tal cual.

---

## 5. Ejemplos por nivel

- **Nivel basico**: `ejemplos/hola_mundo.sipi` — variables, condicionales,
  bucles y funciones simples.
- **Nivel intermedio**: `ejemplos/base_de_datos.sipi` (guardado de datos
  persistente), `ejemplos/inventario_json_csv.sipi` (JSON/CSV reales),
  `ejemplos/enum_y_estructuras.sipi` (enums y structs).
- **Nivel avanzado**: `ejemplos/funciones_recursivas.sipi` (recursion
  real), `ejemplos/estructuras_recursivas.sipi` (listas
  enlazadas/arboles).
- **Nivel experto (v30+)**: base de datos SQLite real
  (`sqlite_conectar`/`sqlite_consultar`), backend con API web real
  (`escuchar_ruta` + `iniciar_api_web`), y administrador de paquetes
  (`instalar_modulo`) — ver los ejemplos de esta seccion en el
  [changelog del README](README.md) para el codigo completo de cada
  sistema.

Para cualquier duda puntual sobre un comando que no este 100% claro en
esta referencia, la forma mas rapida de confirmar la sintaxis exacta es
abrir `sipi.py` y buscar `if cmd == "nombre_del_comando"` — cada
instruccion del lenguaje esta implementada ahi mismo, en español, con
su propia expresion regular de sintaxis.

---

---

El historial de novedades por versión se movió a [`CHANGELOG.md`](CHANGELOG.md).
