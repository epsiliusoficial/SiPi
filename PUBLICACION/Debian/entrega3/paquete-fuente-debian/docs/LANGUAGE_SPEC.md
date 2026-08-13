# LANGUAGE_SPEC — Especificación de SiPi

Documento de referencia técnica sobre qué es SiPi como lenguaje: cómo se ejecuta, qué garantías de tipado ofrece, y su gramática de bloques. Para tutorial paso a paso, ver `DOCUMENTACION.md`. Para la lista de comandos, ver `FUNCTIONS.md`.

## 1. Naturaleza del lenguaje

- **Interpretado.** `sipi.py` parsea y ejecuta un archivo `.sipi` línea por línea. No hay paso de compilación a bytecode intermedio propio del lenguaje (más allá de la caché opcional `.sipic`, que es una optimización de re-ejecución, no un formato intermedio ejecutable por sí solo).
- **Tipado dinámico con anotaciones opcionales.** Las variables no requieren tipo. Si se anota uno (`variable x: entero = 5`), SiPi lo valida en asignación y lo revalida en cada reasignación posterior.
- **Basado en Python.** El intérprete está escrito en Python 3.10+; los objetos de SiPi (instancias de `clase`, diccionarios, listas) son estructuras de Python por dentro.
- **Multiplataforma** en el núcleo del lenguaje (cualquier SO con Python). Los módulos de GUI (`ventana`) dependen de tkinter, y los de juegos (`crear_juego`) de pygame — ambos disponibles en Windows/Linux/macOS, aunque el empaquetado final (`.bat`, instaladores) está más maduro en Windows.
- **Compilable a ejecutable standalone** vía `generar_exe.py` (usa PyInstaller por dentro), para distribuir sin requerir Python instalado en la máquina destino.
- **Código abierto** en su forma de desarrollo (`sipi.py` es legible y editable). Existe un modo de distribución protegido (`proteger_codigo.py`) pensado para cuando alguien quiere publicar una *aplicación* hecha en SiPi sin exponer el intérprete completo, no para ocultar el lenguaje en sí.

## 2. Estructura de un archivo `.sipi`

Todo programa empieza con una única línea obligatoria:

```sipi
programa "Nombre del programa"
```

Después de eso, el archivo es una secuencia de instrucciones. No hay una función `main` obligatoria: el código de nivel superior se ejecuta en orden, de arriba hacia abajo.

## 3. Bloques

Un bloque es cualquier instrucción que abre una sección de código que debe cerrarse. La lista de instrucciones que abren bloque:

`si`, `sino`, `mientras`, `repetir ... veces`, `funcion`, `para_cada`, `intentar`, `enum`, `estructura`, `clase`, `interfaz`, `ventana`, `crear_juego`, `pagina_web`, `formulario`, `pestanias`/`pestana`, `cada ... segundos`, `seleccionar`/`caso`.

Un bloque se cierra de dos formas intercambiables, incluso dentro del mismo archivo:

1. **`fin` explícito** (estilo por defecto, usado en toda esta documentación).
2. **Indentación consistente**, al estilo Python, sin escribir `fin`.

Los bloques se pueden anidar libremente. Una línea de la forma `palabra = valor` **nunca** se interpreta como apertura de bloque, aunque `palabra` coincida con una palabra reservada (esto existe específicamente para permitir variables/campos llamados igual que un comando, ej. un campo `clase` dentro de una `estructura`).

## 4. Comentarios

- Línea: `// comentario` (todo lo que sigue en esa línea se ignora).
- Bloque: `/* comentario que puede ocupar varias líneas */`.

## 5. Literales y expresiones

- **Texto**: entre comillas dobles, con interpolación `{variable}` o `{funcion(x)}` en tiempo real: `decir "Hola {nombre}"`. No se puede escapar `"` con `\"` dentro de un string (queda literal); para texto con comillas, usar comillas simples `'` en ese fragmento.
- **Números**: enteros y decimales, con operadores `+ - * /`.
- **Comparaciones**: `== != < > <= >=`.
- **Concatenación**: `+` entre texto y número convierte el número a texto automáticamente.
- **Llamadas a función dentro de expresiones**, incluso anidadas: `suma_uno(doble(3))`.
- **Asignación de resultado con `->`**: patrón usado por comandos que calculan un valor: `comando argumentos -> variable` (ej. `lista_mapear numeros con doble -> dobles`).

## 6. Sistema de tipos (opcional)

SiPi es dinámico por defecto, pero admite anotaciones opcionales que sí se validan en tiempo de ejecución:

```sipi
variable x: entero = 5
funcion suma(a: entero, b: entero) -> entero
    devolver a + b
fin
lista_crear numeros: lista<entero>
diccionario_crear precios: diccionario<decimal>
```

Los tipos soportados incluyen `entero`, `decimal`, `texto`, `booleano`, listas y diccionarios tipados (`lista<T>`, `diccionario<T>`), y tipos de clase para parámetros/retorno. Si una asignación no respeta el tipo declarado, SiPi lanza un error claro en el momento, no en tiempo de uso posterior.

## 7. Constantes

`const nombre = expr` declara un valor que no puede reasignarse; intentarlo lanza un error. `enum` y `estructura` generan constantes/plantillas de forma automática.

## 8. Programación orientada a objetos

```sipi
clase Animal
    campo nombre = ""
    metodo hacer_sonido()
        decir "..."
    fin
    metodo describir()
        decir "{este.nombre} hace: "
        llamar_metodo este "hacer_sonido"()
    fin
fin

clase Perro hereda_de Animal
    metodo hacer_sonido()
        decir "Guau"
    fin
fin

nuevo Perro() -> mi_perro
llamar_metodo mi_perro "describir"()
```

- `hereda_de` da herencia real, con sobreescritura de métodos (polimorfismo).
- `implementa Interfaz1, Interfaz2` obliga a que la clase tenga todos los métodos declarados en esas interfaces — se verifica al definir la clase, no recién al usarla.
- Dentro de un método, el objeto está disponible como la variable implícita `este` (equivalente a `self`/`this`).
- Los objetos son diccionarios de Python reales por dentro: `diccionario_asignar este "campo" valor` modifica el objeto real, no una copia.

## 9. Manejo de errores

```sipi
intentar
    lanzar_error "Algo salió mal"
capturar
    decir "Error atrapado: {error}"
fin
```

`error` es la variable implícita con el mensaje dentro de un bloque `capturar`.

## 10. Módulos

`importar "archivo.sipi"` importa otro archivo SiPi como módulo. `instalar_modulo "nombre_o_url"` descarga un módulo `.sipi` externo (no hay todavía un índice/registro público central, a diferencia de PyPI/npm).

## 11. Errores con sugerencias

Si el nombre de un comando no existe pero se parece a uno real, SiPi sugiere la corrección: `Comando desconocido: 'imprimr'. ¿Quisiste decir 'imprimir'?` — usa distancia de edición sobre `COMANDOS_CONOCIDOS`, la lista completa de comandos válidos del intérprete.

## 12. Extensión de la sintaxis: bloques de dominio específico

`ventana`, `crear_juego` y `pagina_web` son bloques con su propio mini-lenguaje interno (widgets, sprites, elementos HTML respectivamente) que también se cierran con `fin` y siguen las mismas reglas de anidado. Su gramática interna completa no está formalizada aparte del propio código fuente de `sipi.py`; la referencia más confiable es mirar los programas de ejemplo funcionando en `ejemplos/`.
